from tqdm import tqdm
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from agents.reflexion_oneshot import Reflexion_Oneshot
from utils.utils import clear_code, extract_function_signatures, clear_json
from memories.Memory import MemoryClassMeta
from prompts import prompt_for_generation, prompt_for_reflection, prompt_for_summarization
from loguru import logger
from tenacity import RetryError
import queue
import threading
import time

DEBUG = 1

class OptimAgent(Reflexion_Oneshot):
    def __init__(self, model, dataset, corpus_path, max_perf_debug_num=5, mem_file=None):
        super().__init__(model, dataset, corpus_path, mem_file)
        self.max_perf_debug_num = max_perf_debug_num

        # NOTE: use a single owner (updater) for the global cheatsheet
        self._latest_cheatsheet = ""
        self._cheat_lock = Lock()            # protect reads/writes to _latest_cheatsheet

        # queue of update tasks: workers push (instruction, code, temperature)
        self._update_queue = queue.Queue()
        self._updater_thread = threading.Thread(target=self._cheatsheet_updater_worker, daemon=True)
        self._updater_thread.start()

    def memory_init(self, mem_file=None):
        class Memory(metaclass=MemoryClassMeta, field_names=["ps", 
                                                             "call_err_msg", 
                                                             "exe_err_msg",
                                                             "reflection", 
                                                             "cheat_sheet",
                                                             "function_signatures", 
                                                             "oneshot", 
                                                             "perf_candidates",
                                                             "perf_strategy",
                                                             "raw_code",
                                                             "call_candidate",
                                                             "exe_candidate",
                                                             "perf_debug_num",
                                                             "pass_call", 
                                                             "pass_exe",
                                                             "pass_perf"]):
            pass
        
        if mem_file is not None:
            assert mem_file.endswith(".json"), f"expect a json file, but got {mem_file} instead"
            with open(mem_file, "r") as f:
                input_mems = json.load(f)
            assert len(input_mems) == len(self.dataset), f"expect {len(self.dataset)} samples, but got {len(input_mems)} instead"

        for ps in self.dataset.problem_states:
            if ps.label:
                fs_mem = extract_function_signatures(ps.label)
            else:
                fs_mem = None
            raw_code = [ps.solution] if ps.solution else [""]
            if mem_file is None:
                os_mem = self.instruction_retriever.query(ps.instruction)[0]

                tmp_mem = Memory(ps=ps, 
                                call_err_msg=None,
                                exe_err_msg=None, 
                                reflection=None, 
                                cheat_sheet=None,
                                function_signatures=fs_mem, 
                                oneshot=os_mem["code"],         # only update mem.oneshot once here
                                perf_candidates=[],
                                perf_strategy=None,
                                raw_code=raw_code,
                                call_candidate=None,
                                exe_candidate=None,
                                perf_debug_num=0,
                                pass_call=False,
                                pass_exe=False,
                                pass_perf=False,
                                )
            else:
                input_mem = input_mems[ps.filename]
                tmp_mem = Memory(
                    ps=ps,
                    call_err_msg=input_mem["call_err_msg"],
                    exe_err_msg=input_mem["exe_err_msg"], 
                    reflection=input_mem["reflection"], 
                    cheat_sheet=input_mem["cheat_sheet"],
                    function_signatures=fs_mem, 
                    oneshot=input_mem["oneshot"], 
                    perf_candidates=input_mem["perf_candidates"],
                    perf_strategy=input_mem["perf_strategy"],
                    raw_code=raw_code,
                    call_candidate=input_mem["call_candidate"],
                    exe_candidate=input_mem["exe_candidate"],
                    perf_debug_num=input_mem["perf_debug_num"],
                    pass_call=input_mem["pass_call"],
                    pass_exe=input_mem["pass_exe"],
                    pass_perf=input_mem["pass_perf"],
                )

            self.memories.append(tmp_mem)
    
    def write_memories(self, file_path):
        output_dict = {}
        with open(file_path, "w") as f:
            for mem in self.memories:
                output = {
                    "call_err_msg": str(mem.call_err_msg),
                    "exe_err_msg": str(mem.exe_err_msg),
                    "reflection": mem.reflection, 
                    "cheat_sheet": mem.cheat_sheet,
                    "oneshot": mem.oneshot, 
                    "perf_candidates": [list(cand) for cand in mem.perf_candidates],
                    "perf_strategy": mem.perf_strategy,
                    "call_candidate": mem.call_candidate,
                    "exe_candidate": mem.exe_candidate,
                    "perf_debug_num": mem.perf_debug_num,
                    "pass_call": mem.pass_call, 
                    "pass_exe": mem.pass_exe,
                    "pass_perf": mem.pass_perf,
                    "ms": mem.ms if hasattr(mem, 'ms') else None,
                    "efficiency": mem.efficiency if hasattr(mem, 'efficiency') else None
                }
                output_dict[mem.ps.filename] = output
            json.dump(output_dict, f)
        
    def get_accuracy(self):
        call_acc = sum(1 for mem in self.memories if mem.pass_call) / len(self.memories)
        exe_acc = sum(1 for mem in self.memories if mem.pass_exe) / len(self.memories)
        perf_acc = sum(1 for mem in self.memories if mem.pass_perf) / len(self.memories)
        return {"call_acc": call_acc, "exe_acc": exe_acc, "perf_acc": perf_acc}
        
    def run(self, output_path=None, multi_thread=True, thread_num=3, datalen=None, iteration_num=0, temperature=0, ancestor_num=2, start_idx=0, gpu_id=0, start_iter=0):
        assert ancestor_num >= 0, f"expect ancestor_num to be larger than 0, but got {ancestor_num}"
        data_len = datalen if datalen else len(self.dataset)
        for iter in range(start_iter, start_iter + iteration_num):
            logger.info(f"\n=== Iteration {iter} ===")
            if output_path is not None:
                root, extension = os.path.splitext(output_path)
                iter_path = f"{root}_{iter}{extension}"
                mem_output_path = f"{root}_mem_{iter}.json"

            if multi_thread:
                thread_num = thread_num
            
            # generate solution
            logger.info(f"\ngenerate solution")
            with tqdm(total=data_len) as pbar:
                if multi_thread:
                    with ThreadPoolExecutor(max_workers=thread_num) as executor:
                        futures = {executor.submit(self.generate_solution, mem, temperature): mem for mem in self.memories[start_idx:(start_idx + data_len)]}
                        for future in as_completed(futures):
                            pbar.update(1)
                else:
                    for idx, mem in enumerate(self.memories[start_idx:(start_idx + data_len)]):
                        self.generate_solution(mem, temperature=temperature)
                        pbar.update(1)

            # run scripts
            logger.info(f"\nrun scripts on gpu")
            if output_path is None or (hasattr(self.dataset, 'rocm_tests') and self.dataset.rocm_tests):
                tmp_dir = "tmp"
                exe_dir = "pass_exe"
                perf_result_dir = "perf_results"
                perf_log_dir = "perf_logs"
            else:
                root, extension = os.path.splitext(output_path)
                tmp_dir = f"{root}_tmp"
                exe_dir = f"{root}_pass_exe"
                perf_result_dir = f"{root}_perf_results"
                perf_log_dir = f"{root}_perf_logs"
            
            for mem in tqdm(self.memories[start_idx:(start_idx + data_len)]):
                try:
                    pass_call, pass_exe, call_stdout, call_stderr, exe_stdout, exe_stderr = self.dataset.test_opt_correctness(mem.raw_code[0], mem.ps.filename, tmp_dir, exe_dir=exe_dir)
                except Exception as e:
                    print(f"failed to test the code for {mem.ps.filename}")
                    mem.call_err_msg = f"failed to test the code due to: {e}"
                    mem.exe_err_msg = f"failed to test the code due to: {e}"
                    continue

                if not pass_call:
                    mem.call_err_msg = call_stderr
                    mem.exe_err_msg = exe_stderr
                elif pass_call and not pass_exe:
                    mem.pass_call = True
                    if exe_stderr == "None":
                        mem.exe_err_msg = None
                    else:
                        mem.exe_err_msg = exe_stderr
                    mem.call_candidate = mem.raw_code[0]
                else:
                    mem.pass_call = True
                    mem.pass_exe = True
                    mem.exe_candidate = mem.raw_code[0]
            
            
            logger.info(f"Exec passed files: {os.listdir(exe_dir)}")
            if not os.listdir(exe_dir):
                pass
            else:
                perf_results_dict = {}

                if hasattr(self.dataset, 'rocm_tests') and self.dataset.rocm_tests:
                    perf_results_dict = self.dataset.run_perf_evaluation(
                        exec_folder=exe_dir, 
                        gen_perf_folder=perf_result_dir
                    )
                else:
                    script_dir = os.path.join(tmp_dir, "perf_gen")
                    
                    self.dataset.write_perf_file(
                        input_folder_path=exe_dir, 
                        results_path=perf_result_dir, 
                        tmp_dir=script_dir
                    )
                    self.dataset.run_perf_scripts(
                        gpu_id=gpu_id, 
                        script_dir=script_dir, 
                        log_dir=perf_log_dir
                    )

                for mem in tqdm(self.memories[start_idx:(start_idx + data_len)],desc="Performance Evaluation"):
                    if not mem.pass_exe: # Only check performance if correctness passed
                        continue
                    
                    ms = None
                    efficiency = None

                    if hasattr(self.dataset, 'rocm_tests') and self.dataset.rocm_tests:
                        passed_mems = [mem for mem in self.memories[start_idx:(start_idx + data_len)] if mem.pass_exe]
                        perf_results_list = list(perf_results_dict.values())
                        
                        if len(passed_mems) != len(perf_results_list):
                            pass
                        else:
                            for mem, perf_data in zip(passed_mems, perf_results_list):
                                ms = perf_data.get("ms")
                                efficiency = perf_data.get("efficiency")
                                
                                if ms is not None and efficiency is not None:
                                    mem.pass_perf = True
                                    mem.raw_code.extend([ms, efficiency])
                                    mem.ms = ms
                                    mem.efficiency = efficiency
                                else:
                                    mem.pass_perf = False
                                    mem.ms = None
                                    mem.efficiency = None
                    else:
                        path_gen = os.path.join(perf_result_dir, mem.ps.filename[:-3] + ".json")
                        if not os.path.exists(path_gen):
                            continue
                        try:
                            _, efficiency, ms = self.dataset.calculate(path_gen, path_ref=None)
                            mem.pass_perf = True
                            mem.ms = ms
                            mem.efficiency = efficiency
                            mem.raw_code.extend([ms, efficiency])
                        except Exception as e:
                            logger.error(f"TritonBench performance calculation failed for {mem.ps.filename}: {e}")
                            mem.pass_perf = False
                            continue

            # generate reflections
            logger.info(f"\ngenerate reflections")
            with tqdm(total=data_len) as pbar:
                if multi_thread:
                    with ThreadPoolExecutor(max_workers=thread_num) as executor:
                        futures = {executor.submit(self.generate_reflexion, mem, temperature): mem for mem in self.memories[start_idx:(start_idx + data_len)]}
                        for future in as_completed(futures):
                            pbar.update(1)
                else:
                    for mem in self.memories[start_idx:(start_idx + data_len)]:
                        self.generate_reflexion(mem, temperature=temperature)
                        pbar.update(1)

            # update perf_candidates
            for mem in self.memories[start_idx:(start_idx + data_len)]:
                if not mem.pass_perf:
                    continue

                if len(mem.perf_candidates) < ancestor_num:
                    mem.raw_code.append(mem.reflection)
                    if len(mem.raw_code) < 4:
                        logger.info(f"no latency and efficiency info in the raw code for {mem.ps.filename}")
                        mem.pass_perf = False
                        continue
                    mem.perf_candidates.append(tuple(mem.raw_code))
                    mem.perf_candidates = sorted(mem.perf_candidates, key=lambda x: x[1], reverse=True)

                elif mem.perf_candidates[0][1] > mem.raw_code[1]:
                    mem.raw_code.append(mem.reflection)
                    mem.perf_candidates[0] = tuple(mem.raw_code)
                    mem.perf_candidates = sorted(mem.perf_candidates, key=lambda x: x[1], reverse=True)

            for mem in self.memories[start_idx:(start_idx + data_len)]:
                if len(mem.perf_candidates) > 0:
                    mem.ps.solution = mem.perf_candidates[-1][0]
                elif mem.exe_candidate is not None:
                    mem.ps.solution = mem.exe_candidate
                elif mem.call_candidate is not None:
                    mem.ps.solution = mem.call_candidate
                else:
                    mem.ps.solution = mem.raw_code[0]

            if output_path is not None:
                self.dataset.write_file(iter_path, start_idx=start_idx, datalen=data_len)
                self.write_memories(mem_output_path)
                print("accuracy for call, exec and perf: ", self.get_accuracy())
                with open(f"{root}_acc.txt", "a") as f:
                    acc_dict = self.get_accuracy()
                    f.write(f"Iter {iter}: call_acc={acc_dict['call_acc']}, exe_acc={acc_dict['exe_acc']}, perf_acc={acc_dict['perf_acc']}\n")
                with open(f"{root}_global_cheatsheet.txt", "a") as f:
                    f.write(f"Iter {iter}\n{self.get_latest_cheatsheet()}")

            os.system(f'rm -rf {exe_dir}')
            os.system(f'rm -rf {perf_result_dir}')
            os.system(f'rm -rf {perf_log_dir}')
    
    def generate_solution(self, mem, temperature=0):

        tab = "\n"
        fss_text = "".join(f"* {sig}{tab}" for sig in mem.function_signatures)
        text = prompt_for_generation.prompt.format(
            instruction=mem.ps.instruction,
            function_signatures=fss_text
        )

        if len(mem.perf_candidates) > 0 and (mem.pass_exe or (not mem.pass_exe and mem.perf_debug_num >= self.max_perf_debug_num)):
            mem.perf_debug_num = 0

            text += """There are some reference codes(NO.1, NO.2 and so on). The reference codes are arranged in ascending order based on their performance, where lower latencies and higher efficiencies indicate better performance. According to their performance(latency in ms and efficiency in TFLOPS or GB/s) and the corresponding analysis, you need to generate a new code with better performance. You should maintain code correctness during optimization."""

            text += "\nYou can use optimization strategies such as Memory access efficiency, Hardware resource utilization, IR analysis, Assembly analysis, Kernel occupancy, TorchInductor with Triton tuning knobs and Auto-tunable kernel configurations and environment variables."

            for i, cand in enumerate(mem.perf_candidates):
                text += f"\nreference code: {cand[0]}"
                text += f"\nOriginal latency(ms): {cand[1]}"
                text += f"\noriginal efficiency(TFLOPS, GB/s): {cand[2]}"
                text += f"\nAnalysis: {cand[3]}"
            
            text += "\nAnalyze and compare all optimization strategies based on correct codes and give a better strategy motivated by them. Generate a better optimization code based on the better strategy ."
            text += "\nThink before writing the optimization and no more explanation is required after the thinking."
            text += "\nYou should not suggest changes to the name of the function and parameter names, counts, or order."
        else:
            if not mem.raw_code or mem.raw_code[0] == "":
                text += f"\nHere is an example snippet of code: {mem.oneshot}"
            else:
                ret = self.code_retriever.query(mem.raw_code[0])[0]
                one_shot = ret["code"]

                mem.oneshot = one_shot  

                text += f"\nHere is an example snippet of code: {one_shot}"
                text += f"\nPrevious attempt implementation:{mem.raw_code[0]}"
                
                if not mem.pass_call:
                    text += f"\nTest messages for previous attempt:{mem.call_err_msg}"
                    text += f"\nTest messages for correctness check of previous attempt:{mem.exe_err_msg}"
                
                elif not mem.pass_exe:
                    text += "\nThe previous attempt implementation can be run successfully."
                    text += f"\nTest messages for correctness check of previous attempt:{mem.exe_err_msg}"
                
                if len(mem.perf_candidates) > 0:
                    mem.perf_debug_num += 1
            
            # IMPORTANT: fetch latest snapshot _just before_ calling the LLM
            latest = self.get_latest_cheatsheet()
            if latest:
                text += f"\nHere is the global cheat sheet: {latest}"

        text += "\nOutput your answer in json format, with the format as follows: {\"thought\": \"\", \"code\": \"\"}. Please strictly output in JSON format."
        text += "\nGenerate the correct and optimized code without explanation, which we can run directly in the \"code\" field."

        msg = [
            {"role": "user", "content": text},
        ]

        try:
            response = self.model.generate(msg, temperature=temperature, max_tokens=5000)
        except Exception as e:
            logger.info(f"failed to call LLM for {mem.ps.filename}")
            logger.info(f"Exception happened in calling LLM: {e}")
            response = {"code": ""}
        
        try:
            mem.raw_code = [clear_code(clear_json(response)["code"])]
        except:
            print(f"failed to extract code for {mem.ps.filename}")
            raw_code = response.split("\"code\":")[1]
            raw_code = raw_code.split("}")[0]
            mem.raw_code = [clear_code(raw_code)]
        
        if mem.raw_code[0] is None or mem.raw_code is None:
            print(f"raw code for {mem.ps.filename} is None")
            mem.raw_code = [""]

        # enqueue an update request instead of calling model.generate while holding a lock
        self.enqueue_cheatsheet_update(mem, temperature)

        mem.pass_call = False
        mem.pass_exe = False
        mem.pass_perf = False

        return mem

    # enqueue update task (non-blocking)
    def enqueue_cheatsheet_update(self, mem, temperature):
        try:
            self._update_queue.put_nowait((mem.ps.instruction, mem.raw_code[0], temperature))
        except queue.Full:
            logger.warning("cheatsheet update queue full, dropping update for %s", mem.ps.filename)

    # get latest cheat-sheet snapshot (thread-safe)
    def get_latest_cheatsheet(self):
        with self._cheat_lock:
            return self._latest_cheatsheet

    # updater owner thread: serializes calls to model.generate and publishes snapshots
    def _cheatsheet_updater_worker(self):
        """
        Worker that consumes pending update requests and issues a single model.generate
        to update the global cheatsheet. To reduce LLM calls, it will batch/merge
        multiple pending updates that arrive within a short window.
        """
        while True:
            try:
                # block until at least one update arrives
                instr, code, temperature = self._update_queue.get()
            except Exception:
                time.sleep(0.1)
                continue

            # gather any other pending updates quickly (non-blocking)
            pending = [(instr, code)]
            try:
                # pull up to a small burst of pending items
                while True:
                    item = self._update_queue.get_nowait()
                    pending.append((item[0], item[1]))
            except queue.Empty:
                pass

            # Build a merged prompt that incorporates previous cheatsheet + multiple Q/A
            prev = self.get_latest_cheatsheet() or ""
            merged_question = "\n\n".join([f"QUESTION: {p[0]}\nMODEL_ANSWER: {p[1]}" for p in pending])
            prompt_text = prompt_for_summarization.prompt_dc_cu.format(
                PREVIOUS_CHEATSHEET=prev,
                QUESTION=merged_question,
                MODEL_ANSWER=""
            )
            global_cheat_msg = [{"role": "user", "content": prompt_text}]

            try:
                # single LLM call per batch
                new_cheatsheet = self.model.generate(global_cheat_msg, temperature=temperature)
                with self._cheat_lock:
                    # publish the new snapshot
                    self._latest_cheatsheet = new_cheatsheet
                logger.info("Global cheatsheet updated by updater worker (batch size=%d)", len(pending))
            except Exception as e:
                logger.error(f"Updater worker: failed to call model.generate: {e}")
            finally:
                for _ in pending:
                    self._update_queue.task_done()

    def update_global_cheatsheet(self, mem, temperature):
        # Backwards-compatible alias: just enqueue
        self.enqueue_cheatsheet_update(mem, temperature)
    
    def generate_reflexion(self, mem, temperature):
        if mem.pass_perf:
            reflect_txt = prompt_for_reflection.prompt_ga.format(
                problem=mem.ps.instruction,
                code=mem.raw_code[0],
                latency=mem.raw_code[1],
                efficiency=mem.raw_code[2]
            )
        elif mem.pass_call and mem.pass_exe:
            reflect_txt = prompt_for_reflection.prompt_ga.format(
                problem=mem.ps.instruction,
                code=mem.raw_code[0],
                latency="",
                efficiency=""
            )
        elif mem.pass_call:
            reflect_txt = prompt_for_reflection.prompt_exe.format(
                problem=mem.ps.instruction,
                solution=mem.raw_code[0],
                call_test_result="succeed",
                exe_test_result=mem.exe_err_msg
            )
        else:
            reflect_txt = prompt_for_reflection.prompt.format(
                problem=mem.ps.instruction,
                solution=mem.raw_code[0],
                test_result=mem.call_err_msg
            )
        
        reflect_msg = [
            {
                "role": "user",
                "content": reflect_txt
            }
        ]
        mem.reflection = self.model.generate(reflect_msg, temperature=temperature)

        return mem
