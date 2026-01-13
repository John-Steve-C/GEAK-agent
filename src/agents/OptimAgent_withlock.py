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


class OptimAgent(Reflexion_Oneshot):
    def __init__(self, model, dataset, corpus_path, max_perf_debug_num=5, mem_file=None):
        super().__init__(model, dataset, corpus_path, mem_file)
        self.max_perf_debug_num = max_perf_debug_num
        self.global_cheat_sheet = ""
        self.lock = Lock()

    def memory_init(self, mem_file=None):
        """
        Args:
            mem_file: previous stored memories, which can be loaded to continue run
        """
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
                
                # print("First iteration, use instruction retriever")
                # print("original problem: ", ps.instruction)
                # print("similar problem: ", os_mem["original instruction"])
                # # print("similar code: ", os_mem["code"])
                # print("-" * 50)

                # with open("tmp_output_for_instruction_retrieve.json", "a") as f:
                #     json.dump({
                #         "original_instruction": ps.instruction,
                #         "original_code": ps.solution,
                #         "retrieved_instruction": os_mem["original instruction"],
                #         "retrieved_code": os_mem["code"],
                #         "score": os_mem["similarity score"]
                #     }, f, indent=4)
                
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
        """
        Args:
            output_path: the folder to store the final result
            multi_thread: whether use multithreading for generating
            datalen: for debug, to specify how many data from the dataset you want to use
            iteration_num: how many iterations you want to run
            temperature: LLM temperature
            ancestor_num: how many samples you want to add in the prompt when optimize the code
            start_idx: start idx of the data rows
            gpu_id: which gpu you want to use when you test the scripts
            start_iter: which iteration you want to start with. useful when you load previous result and memory
        """
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
                        
                        # global_cheatsheet = prompt_for_summarization.prompt_dc_cu.format(
                        #     PREVIOUS_CHEATSHEET=self.global_cheat_sheet,
                        #     QUESTION=mem.ps.instruction,
                        #     MODEL_ANSWER=mem.raw_code[0]
                        # )
                        # global_cheat_msg = [
                        #     {
                        #         "role": "user",
                        #         "content": global_cheatsheet
                        #     }
                        # ]
                        # self.global_cheat_sheet = self.model.generate(global_cheat_msg, temperature=temperature)
                        
                        # [Modified] Disabled manual update here since we now update in generate_solution
                        # self.global_cheat_sheet += f"#### Previous Input #{idx}:\n\n{mem.ps.instruction}\n\n#### Model Solution to Previous Input #{idx}:\n\n{mem.raw_code[0]}\n---\n---\n\n"
                        
                        # logger.info(f"global cheatsheet: \n{self.global_cheat_sheet}")
            
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
                # logger.warning(f"No scripts passed correctness checks in iteration {iter}. Skipping performance evaluation.")
            else:
                # run performance evaluation
                # This block now only runs if there are files to evaluate.
                # logger.info("\nrun performance evaluation")
                perf_results_dict = {}

                if hasattr(self.dataset, 'rocm_tests') and self.dataset.rocm_tests:
                    perf_results_dict = self.dataset.run_perf_evaluation(
                        exec_folder=exe_dir, 
                        gen_perf_folder=perf_result_dir
                    )
                else:
                    # TritonBench performance evaluation flow
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
                    # For TritonBench, results are on disk, so the dict remains empty.
                    # The logic below will handle reading from files.

                # get ms and efficiency
                # logger.info("\nparsing performance results")
                for mem in tqdm(self.memories[start_idx:(start_idx + data_len)],desc="Performance Evaluation"):
                    if not mem.pass_exe: # Only check performance if correctness passed
                        continue
                    
                    ms = None
                    efficiency = None

                    # Parse results based on the dataset type
                    if hasattr(self.dataset, 'rocm_tests') and self.dataset.rocm_tests:
                        # Create a list of memory objects that passed the correctness check
                        passed_mems = [mem for mem in self.memories[start_idx:(start_idx + data_len)] if mem.pass_exe]
                        
                        # Convert the performance results dictionary to a list of its values (the dicts with ms, efficiency)
                        perf_results_list = list(perf_results_dict.values())
                        
                        # Check for size mismatch, which indicates a problem in the pipeline
                        if len(passed_mems) != len(perf_results_list):
                            pass
                            # logger.error(f"Mismatch in number of passed scripts ({len(passed_mems)}) and performance results ({len(perf_results_list)}). Cannot reliably assign performance metrics.")
                        else:
                            # Iterate through both lists in parallel
                            for mem, perf_data in zip(passed_mems, perf_results_list):
                                ms = perf_data.get("ms")
                                efficiency = perf_data.get("efficiency")
                                
                                if ms is not None and efficiency is not None:
                                    # logger.info(f"Assigning to {mem.ps.filename}: ms={ms}, efficiency={efficiency}")
                                    mem.pass_perf = True
                                    mem.raw_code.extend([ms, efficiency])
                                    mem.ms = ms
                                    mem.efficiency = efficiency
                                else:
                                    # logger.warning(f"Incomplete performance data for {mem.ps.filename}: {perf_data}")
                                    mem.pass_perf = False
                                    mem.ms = None
                                    mem.efficiency = None
                    else:
                        # For TritonBench, read results from files
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
                    f.write(f"Iter {iter}\n{self.global_cheat_sheet}")

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

        # for the one that has perf_candidates, and the code generated in this round pass_exe, we need to generate a new code
        # for the one that has perf_candidates, but the code generated in this round not pass_exe, if the debug_num has exceeds the man_debug_num, then generate a new code
        # otherwise, go to debug
        if len(mem.perf_candidates) > 0 and (mem.pass_exe or (not mem.pass_exe and mem.perf_debug_num >= self.max_perf_debug_num)):
            # print("performance improvement!")
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
                # print("choose memory oneshot!")
                text += f"\nHere is an example snippet of code: {mem.oneshot}"
            else:
                # print("choose retrieve oneshot!")
                # one_shot = self.code_retriever.query(mem.raw_code[0])[0]["code"]
                ret = self.code_retriever.query(mem.raw_code[0])[0]
                one_shot = ret["code"]

                # ret_2 = self.code_retriever_2.query(mem.raw_code[0])[0]
                # one_shot = ret_2["code"]      # core_to_whole retriever
                # one_shot = ret_2["core code"]   # core_to_core

                # print("One shot is: ", one_shot)

                # print("Not first iteration")
                # logger.info(f"Original problem: {mem.ps.instruction}")
                
                # logger.info(f"Scores from two retrievers: {ret['similarity score']}, {ret_2['similarity score']}")
                # if ret["code"] == ret_2["code"]:
                #     logger.info("Retrieved code from coreToWholeRetriever is the same as from EmbeddingRetriever.")
                # else:
                #     logger.info("Different from EmbeddingRetriever!")
                # logger.info(f"Cheat sheet:\n{mem.cheat_sheet}")
                
                # print("original problem: ", mem.ps.instruction)
                # print("original code: ", mem.raw_code[0])
                # print("similar problem: ", ret["original instruction"])
                # print("similar code: ", ret["code"])
                # print("similarity score: ", ret["similarity score"])
                # print("similar problem 2: ", ret_2["original instruction"])
                # print("similar code 2: ", ret_2["code"])
                # print("Core code: ", ret_2["core code"])
                # print("similarity score 2: ", ret_2["similarity score"])
                # print("-" * 50)

                # with open("tmp_output_for_code_retrieve.json", "a") as f:
                #     json.dump({
                #         "original_instruction": mem.ps.instruction,
                #         "original_code": mem.raw_code[0],
                #         "retrieved_instruction": ret["original instruction"],
                #         "retrieved_code": one_shot,
                #         "score": ret["similarity score"]
                #     }, f, indent=4)
                
                # with open("tmp_output_for_code_retrieve_core.json", "a") as f:
                #     json.dump({
                #         "original_instruction": mem.ps.instruction,
                #         "original_code": mem.raw_code[0],
                #         "retrieved_instruction": ret_2["original instruction"],
                #         "retrieved_code": one_shot,
                #         "score": ret_2["similarity score"]
                #     }, f, indent=4)


                # persist retrieved one_shot into memory so later steps see it
                # keep correct code unchanged
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
            
            
            if mem.reflection:
                text += f"\nReflection on previous attempt:{mem.reflection}"

            # if mem.cheat_sheet:
            #     text += f"\nCheat sheet of this task, and you can borrow some take-aways:{mem.cheat_sheet}"
            if self.global_cheat_sheet:
                text += f"\nHere is the global cheat sheet: {self.global_cheat_sheet}"

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
        
        logger.info(f"Current response: \n{response}")

        try:
            mem.raw_code = [clear_code(clear_json(response)["code"])]
        except:
            print(f"failed to extract code for {mem.ps.filename}")
            # fail_dir = "failed_to_extract"
            # fail_path = os.path.join(fail_dir, mem.ps.filename)
            # os.makedirs(fail_dir, exist_ok=True)

            # with open(fail_path, "w") as f:
            #     f.write(response)

            if "\"code\":" in response:
                raw_code = response.split("\"code\":")[1]
                raw_code = raw_code.split("}")[0]
                mem.raw_code = [clear_code(raw_code)]
            else:
                raw_code = response
                mem.raw_code = [raw_code]
        # finally:
        
        if mem.raw_code[0] is None or mem.raw_code is None:
            print(f"raw code for {mem.ps.filename} is None")
            mem.raw_code = [""]

        # [Added] Update global cheatsheet in real time
        self.update_global_cheatsheet(mem, temperature)

        mem.pass_call = False
        mem.pass_exe = False
        mem.pass_perf = False

        return mem

    # [Added] Helper method for thread-safe updates
    def update_global_cheatsheet(self, mem, temperature):
        with self.lock:
            try:
                # Assuming prompt_dc_cu is available and suitable for summarization
                global_cheatsheet_prompt = prompt_for_summarization.prompt_dc_cu.format(
                    PREVIOUS_CHEATSHEET=self.global_cheat_sheet,
                    QUESTION=mem.ps.instruction,
                    MODEL_ANSWER=mem.raw_code[0]
                )
                global_cheat_msg = [
                    {
                        "role": "user",
                        "content": global_cheatsheet_prompt
                    }
                ]
                # Update the shared variable
                self.global_cheat_sheet = self.model.generate(global_cheat_msg, temperature=temperature)
                logger.info(f"Global cheatsheet updated for {mem.ps.filename}")
            except Exception as e:
                logger.error(f"Failed to update global cheatsheet: {e}")
    
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

        # ===================================== generate problem-wise cheatsheet
        # cheatsheet_txt = prompt_for_summarization.prompt_cheatsheet.format(
        #     problem=mem.ps.instruction,
        #     solution=mem.raw_code[0],
        #     cheat_sheet=mem.cheat_sheet
        # )
        # cheatsheet_txt = prompt_for_summarization.prompt_dc_cu.format(
        #     PREVIOUS_CHEATSHEET=mem.cheat_sheet,
        #     QUESTION=mem.ps.instruction,
        #     MODEL_ANSWER=mem.raw_code[0]
        # )
        # cheat_msg = [
        #     {
        #         "role": "user",
        #         "content": cheatsheet_txt
        #     }
        # ]
        # mem.cheat_sheet = self.model.generate(cheat_msg, temperature=temperature)
        # logger.info(f"response:  {mem.cheat_sheet}")

        # ===================================== generate global cheatsheet
        # global_cheatsheet = prompt_for_summarization.prompt_dc_cu.format(
        #     PREVIOUS_CHEATSHEET=self.global_cheat_sheet,
        #     QUESTION=mem.ps.instruction,
        #     MODEL_ANSWER=mem.raw_code[0]
        # )
        # global_cheat_msg = [
        #     {
        #         "role": "user",
        #         "content": global_cheatsheet
        #     }
        # ]
        # self.global_cheat_sheet = self.model.generate(global_cheat_msg, temperature=temperature)
        # logger.info(f"global cheatsheet: \n{self.global_cheat_sheet}")

        return mem