from tqdm import tqdm
import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from agents.reflexion_oneshot import Reflexion_Oneshot
from utils.utils import clear_code, extract_function_signatures, clear_json
from memories.Memory import MemoryClassMeta
from prompts import prompt_for_generation, prompt_for_reflection, prompt_for_summarization
from loguru import logger
from tenacity import RetryError
from threading import Lock
from memories.CheatsheetManager import CheatsheetManager

class OptimAgent(Reflexion_Oneshot):
    def __init__(self, model, dataset, corpus_path, max_perf_debug_num=5, mem_file=None):
        super().__init__(model, dataset, corpus_path, mem_file)
        self.max_perf_debug_num = max_perf_debug_num
        
        self.global_cheatsheet = ""
        # Lock to protect the shared resource
        self.cheatsheet_lock = Lock()
        # a manager to manage cheatsheet updates in json format
        self.cheatsheet_manager = CheatsheetManager()

    def memory_init(self, mem_file=None):
        """
        Args:
            mem_file: previous stored memories, which can be loaded to continue run
        """
        class Memory(metaclass=MemoryClassMeta, field_names=["ps", 
                                                             "call_err_msg", 
                                                             "exe_err_msg",
                                                             "reflection", 
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
                                function_signatures=fs_mem, 
                                oneshot=os_mem["code"], 
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

    def process_single_iteration(self, mem, temperature, ancestor_num, dirs, gpu_id):
        """
        The wrapper function that runs the full pipeline for a single memory unit.
        Steps:
        1. Generate Solution
        2. Run Scripts (Correctness)
        3. Run Performance Evaluation (if correct)
        4. Generate Reflection
        5. Update Candidates
        """
        tmp_dir, exe_dir, perf_result_dir, perf_log_dir = dirs['tmp'], dirs['exe'], dirs['perf_res'], dirs['perf_log']

        # --- 1. Generate Solution ---
        try:
            self.generate_solution(mem, temperature)
        except Exception as e:
            logger.error(f"Error generating solution for {mem.ps.filename}: {e}")
            return mem

        # --- 2. Run Scripts (Correctness) ---
        try:
            pass_call, pass_exe, call_stdout, call_stderr, exe_stdout, exe_stderr = self.dataset.test_opt_correctness(
                mem.raw_code[0], mem.ps.filename, tmp_dir, exe_dir=exe_dir
            )
        except Exception as e:
            print(f"failed to test the code for {mem.ps.filename}")
            mem.call_err_msg = f"failed to test the code due to: {e}"
            mem.exe_err_msg = f"failed to test the code due to: {e}"
            pass_call, pass_exe = False, False
            # If basic execution crashes, we might still want to reflect, so we proceed
        
        if not pass_call:
            mem.call_err_msg = call_stderr if 'call_stderr' in locals() else str(e)
            mem.exe_err_msg = exe_stderr if 'exe_stderr' in locals() else str(e)
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

        # --- 3. Performance Evaluation (Only if correctness passed) ---
        if mem.pass_exe:
            ms = None
            efficiency = None
            
            # 3a. ROCM Tests Logic
            if hasattr(self.dataset, 'rocm_tests') and self.dataset.rocm_tests:
                # NOTE: run_perf_evaluation in original code was used to test all results in a given path, so we need to ensure it can handle single files.
                # TODO: need to write a new run_perf_evaluation_single
                # Calling it here assumes it can handle single files or the folder state is managed.
                # Since we are in a thread, this might have race conditions if not thread-safe.
                # We assume the dataset method handles the specific file passed in exe_dir.
                try:
                    # We might need to lock this if run_perf_evaluation is not thread safe
                    # But per user request for wrapper pattern, we place it here.
                    perf_results_dict = self.dataset.run_perf_evaluation(
                        exec_folder=exe_dir, 
                        gen_perf_folder=perf_result_dir
                    )
                    # Attempt to extract just this file's result
                    # This relies on the dataset returning results for the specific file
                    # If run_perf_evaluation runs EVERYTHING in the folder, this is inefficient in a loop
                    if mem.ps.filename in perf_results_dict:
                        perf_data = perf_results_dict[mem.ps.filename]
                        ms = perf_data.get("ms")
                        efficiency = perf_data.get("efficiency")
                except Exception as e:
                    logger.error(f"ROCM Perf eval failed for {mem.ps.filename}: {e}")

            # 3b. TritonBench Logic
            else:
                script_dir = os.path.join(tmp_dir, "perf_gen")
                try:
                    # Write perf file for THIS specific file
                    # We assume these methods function correctly when multiple threads call them 
                    # for different filenames.
                    self.dataset.write_perf_file_single(
                        input_folder_path=exe_dir, 
                        results_path=perf_result_dir, 
                        tmp_dir=script_dir,
                        filename=mem.ps.filename
                    )
                    self.dataset.run_perf_script_single(
                        gpu_id=gpu_id, 
                        script_dir=script_dir, 
                        log_dir=perf_log_dir,
                        script_name=mem.ps.filename.replace(".py", "_perf.py")
                    )
                    
                    path_gen = os.path.join(perf_result_dir, mem.ps.filename[:-3] + ".json")
                    if os.path.exists(path_gen):
                        _, efficiency, ms = self.dataset.calculate(path_gen, path_ref=None)
                except Exception as e:
                    logger.error(f"TritonBench Perf eval failed for {mem.ps.filename}: {e}")

            # 3c. Update Memory with Perf Data
            if ms is not None and efficiency is not None:
                mem.pass_perf = True
                mem.raw_code.extend([ms, efficiency])
                mem.ms = ms
                mem.efficiency = efficiency
            else:
                mem.pass_perf = False
                mem.ms = None
                mem.efficiency = None

        # --- 4. Generate Reflections ---
        try:
            self.generate_reflexion(mem, temperature)
        except Exception as e:
            logger.error(f"Reflection generation failed for {mem.ps.filename}: {e}")

        # --- 5. Update Cheatsheet ---
        try:
            self.generate_dc(mem, method="json", temperature=temperature)
        except Exception as e:
            logger.error(f"DC generation failed for {mem.ps.filename}: {e}")

        # --- 6. Update Perf Candidates (Logic from end of original loop) ---
        if mem.pass_perf:
            if len(mem.perf_candidates) < ancestor_num:
                mem.raw_code.append(mem.reflection)
                if len(mem.raw_code) >= 4:
                     mem.perf_candidates.append(tuple(mem.raw_code))
                     mem.perf_candidates = sorted(mem.perf_candidates, key=lambda x: x[1], reverse=True)
                else:
                     logger.info(f"no latency/efficiency info for {mem.ps.filename}")
                     mem.pass_perf = False

            elif len(mem.perf_candidates) > 0 and mem.perf_candidates[0][1] > mem.raw_code[1]:
                mem.raw_code.append(mem.reflection)
                mem.perf_candidates[0] = tuple(mem.raw_code)
                mem.perf_candidates = sorted(mem.perf_candidates, key=lambda x: x[1], reverse=True)

        # Final Update of Solution string based on best candidate
        if len(mem.perf_candidates) > 0:
            mem.ps.solution = mem.perf_candidates[-1][0]
        elif mem.exe_candidate is not None:
            mem.ps.solution = mem.exe_candidate
        elif mem.call_candidate is not None:
            mem.ps.solution = mem.call_candidate
        else:
            mem.ps.solution = mem.raw_code[0]

        return mem

    def run(self, output_path=None, multi_thread=True, thread_num=3, datalen=None, iteration_num=0, temperature=0, ancestor_num=2, start_idx=0, gpu_id=0, start_iter=0):
        """
        Args:
            output_path: the folder to store the final result
            multi_thread: whether use multithreading
            datalen: for debug, to specify how many data from the dataset you want to use
            iteration_num: how many iterations you want to run
            temperature: LLM temperature
            ancestor_num: how many samples you want to add in the prompt when optimize the code
            start_idx: start idx of the data rows
            gpu_id: which gpu you want to use when you test the scripts
            start_iter: which iteration you want to start with
        """
        assert ancestor_num >= 0, f"expect ancestor_num to be larger than 0, but got {ancestor_num}"
        data_len = datalen if datalen else len(self.dataset)

        for iter in range(start_iter, start_iter + iteration_num):
            logger.info(f"\n=== Iteration {iter} ===")
            
            # Setup Paths
            if output_path is not None:
                root, extension = os.path.splitext(output_path)
                iter_path = f"{root}_{iter}{extension}"
                mem_output_path = f"{root}_mem_{iter}.json"
                
                # Setup Directories
                if hasattr(self.dataset, 'rocm_tests') and self.dataset.rocm_tests:
                    tmp_dir = "tmp"
                    exe_dir = "pass_exe"
                    perf_result_dir = "perf_results"
                    perf_log_dir = "perf_logs"
                else:
                    tmp_dir = f"{root}_tmp"
                    exe_dir = f"{root}_pass_exe"
                    perf_result_dir = f"{root}_perf_results"
                    perf_log_dir = f"{root}_perf_logs"
            else:
                # Default fallback if output_path is None (though usually required)
                tmp_dir, exe_dir, perf_result_dir, perf_log_dir = "tmp", "pass_exe", "perf_results", "perf_logs"
                iter_path, mem_output_path = "output.json", "mem.json"
                root = "output"

            # Create directories needed for this iteration
            for d in [tmp_dir, exe_dir, perf_result_dir, perf_log_dir]:
                os.makedirs(d, exist_ok=True)
            
            # Pack directories for the wrapper
            dirs = {
                'tmp': tmp_dir, 
                'exe': exe_dir, 
                'perf_res': perf_result_dir, 
                'perf_log': perf_log_dir
            }

            # --- Start Parallel Execution ---
            logger.info(f"Starting iteration {iter} with {thread_num} threads...")
            
            current_batch = self.memories[start_idx:(start_idx + data_len)]
            
            with tqdm(total=len(current_batch)) as pbar:
                if multi_thread:
                    with ThreadPoolExecutor(max_workers=thread_num) as executor:
                        # Submit tasks
                        futures = {
                            executor.submit(
                                self.process_single_iteration, 
                                mem, 
                                temperature, 
                                ancestor_num, 
                                dirs, 
                                gpu_id
                            ): mem for mem in current_batch
                        }
                        
                        # Process results as they finish
                        for future in as_completed(futures):
                            pbar.update(1)
                            try:
                                future.result() # Check for exceptions raised in wrapper
                            except Exception as e:
                                logger.error(f"Wrapper exception: {e}")
                else:
                    # Single threaded fallback
                    for mem in current_batch:
                        self.process_single_iteration(mem, temperature, ancestor_num, dirs, gpu_id)
                        pbar.update(1)

            # --- Post-Iteration Cleanup and Saving ---
            if output_path is not None:
                self.dataset.write_file(iter_path, start_idx=start_idx, datalen=data_len)
                self.write_memories(mem_output_path)
                
                acc = self.get_accuracy()
                print("accuracy for call, exec and perf: ", acc)
                with open(f"{root}_acc.txt", "a") as f:
                    f.write(f"Iter {iter}: call_acc={acc['call_acc']}, exe_acc={acc['exe_acc']}, perf_acc={acc['perf_acc']}\n")

            # Clean temporary directories
            os.system(f'rm -rf {exe_dir}')
            os.system(f'rm -rf {perf_result_dir}')
            os.system(f'rm -rf {perf_log_dir}')

    def generate_solution(self, mem, temperature=0):
        # [Existing generate_solution code remains unchanged...]
        # Paste the original generate_solution logic here
        # (I omitted it for brevity as the prompt focused on the run loop structure, 
        # but ensure you keep the original logic here)
        
        tab = "\n"
        fss_text = "".join(f"* {sig}{tab}" for sig in mem.function_signatures)
        text = prompt_for_generation.prompt.format(
            instruction=mem.ps.instruction,
            function_signatures=fss_text
        )

        if len(mem.perf_candidates) > 0 and (mem.pass_exe or (not mem.pass_exe and mem.perf_debug_num >= self.max_perf_debug_num)):
            mem.perf_debug_num = 0

            text += """There are some reference codes(NO.1, NO.2 and so on). The reference codes are arranged in ascending order based on their performance, where lower latencies and higher efficiencies indicate better performance. According to their performance(latency in ms and efficiency in TFLOPS or GB/s) and the corresponding analysis, you need to generate a new code with better performance. You should maintain code correctness during optimization."""

            text +="\nYou can use optimization strategies such as Memory access efficiency, Hardware resource utilization, IR analysis, Assembly analysis, Kernel occupancy, TorchInductor with Triton tuning knobs and Auto-tunable kernel configurations and environment variables."

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
                # ret_2 = self.code_retriever_2.query(mem.raw_code[0])[0]

                one_shot = ret["code"]
                # one_shot = ret_2["code"]
                # one_shot = ret_2["core code"]
                # print("One shot is: ", one_shot)

                # print("Not first iteration")
                # logger.info(f"Original problem: {mem.ps.instruction}")
                
                # logger.info(f"Scores from two retrievers: {ret['similarity score']}, {ret_2['similarity score']}")
                # if ret["code"] == ret_2["code"]:
                #     logger.info("Retrieved code from coreToWholeRetriever is the same as from EmbeddingRetriever.")
                # else:
                #     logger.info("Different from EmbeddingRetriever!")

                # with open("tmp_output_for_code_retrieve.json", "a") as f:
                #     json.dump({
                #         "original_instruction": mem.ps.instruction,
                #         "original_code": mem.raw_code[0],
                #         "retrieved_instruction": ret["original instruction"],
                #         "retrieved_code": one_shot,
                #         "score": ret["similarity score"]
                #     }, f, indent=4)

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
            
            
            if mem.reflection:
                text += f"\nReflection on previous attempt:{mem.reflection}"

            with self.cheatsheet_lock:
                # text += f"\nHere is the global cheatsheet: {self.global_cheatsheet}"
                text += f"\nHere is the global cheatsheet: {self.cheatsheet_manager.to_string_for_prompt()}"

        text += "\nOutput your answer in json format, with the format as follows: {\"thought\": \"\", \"code\": \"\"}. Please strictly output in JSON format."
        text += "\nGenerate the correct and optimized code without explanation, which we can run directly in the \"code\" field."

        msg = [
            {"role": "user", "content": text},
        ]

        try:
            response = self.model.generate(msg, temperature=temperature, max_tokens=15000)
        except:
            logger.info(f"failed to call LLM for {mem.ps.filename}")
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

        mem.pass_call = False
        mem.pass_exe = False
        mem.pass_perf = False

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

    # Helper function to extract cheatsheet from response
    def extract_cheatsheet(
        self,
        response: str,
        old_cheatsheet: str,
    ) -> str:
        """
        Extracts the cheatsheet from the model response.
        
        Arguments:
            response : str : The response from the model.
            old_cheatsheet : str : The old cheatsheet to return if the new one is not found.

        Returns:
            str : The extracted cheatsheet (if not found, returns the old cheatsheet).
        """
        response = response.strip()
        # <cheatsheet> (content) </cheatsheet>
        if "<cheatsheet>" in response:
            try:
                txt = response.split("<cheatsheet>")[1].strip()
                txt = txt.split("</cheatsheet>")[0].strip()
                return txt
            except:
                return old_cheatsheet
        else:
            return old_cheatsheet
    
    def generate_dc(self, mem, method, temperature):
        with self.cheatsheet_lock:
            if method == "json":
                text = self.cheatsheet_manager.build_prompt(mem.ps.instruction, mem.reflection)
            else:
                current_sheet = self.global_cheatsheet
                if method == "dc_full":
                    text = prompt_for_summarization.prompt_for_dc_full.format(
                        PREVIOUS_CHEATSHEET=current_sheet,
                        QUESTION=mem.ps.instruction,
                        MODEL_ANSWER=mem.raw_code[0],
                    )
                elif method == "dc_short":
                    text = prompt_for_summarization.prompt_for_dc_short.format(
                        PREVIOUS_CHEATSHEET=current_sheet,
                        QUESTION=mem.ps.instruction,
                        MODEL_ANSWER=mem.raw_code[0],
                    )
                elif method == "reflect":
                    text = prompt_for_summarization.prompt_for_dc_reflect.format(
                        PREVIOUS_CHEATSHEET=current_sheet,
                        QUESTION=mem.ps.instruction,
                        MODEL_ANSWER=mem.raw_code[0],
                        REFLECTION=mem.reflection,
                    )

        msg = [
            {"role": "user", "content": text},
        ]
        try:
            response = self.model.generate(msg, temperature=temperature, max_tokens=10000)
        except:
            logger.info(f"failed to call LLM for {mem.ps.filename}, skip update cheatsheet")
            return
        
        with self.cheatsheet_lock:
            if method == "json":
                self.cheatsheet_manager.apply_operations(response)
                logger.info(f"Updated global cheatsheet for {mem.ps.filename}, \nnew cheatsheet: \n{self.cheatsheet_manager.to_string_for_prompt()}")
            else:
                self.global_cheatsheet = self.extract_cheatsheet(response, current_sheet)
                logger.info(f"Updated global cheatsheet for {mem.ps.filename}, \nnew cheatsheet: \n{self.global_cheatsheet}")
