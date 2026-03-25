import os
import json
import re
from typing import Optional
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.callbacks import get_openai_callback

# 严格按要求 import，不修改 Manager 源码
from memories.CheatsheetManager import CheatsheetManager
from dataloaders.TritonBench import TritonBench
from utils.utils import extract_function_signatures, clear_code, clear_json
# --- 1. 全局持久化逻辑 ---
CHEATSHEET_PATH = "tmp_cheatsheet.json"
DEFAULT_PATH = "first_cheatsheet.json"

def get_manager() -> CheatsheetManager:
    if os.path.exists(CHEATSHEET_PATH):
        with open(CHEATSHEET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        with open(DEFAULT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    return CheatsheetManager(initial_state=data)

def save_manager(manager: CheatsheetManager):
    with open(CHEATSHEET_PATH, "w", encoding="utf-8") as f:
        f.write(manager.to_json())

dict_to_save = []

def run_test_outside(code: str, filename: str) -> str:
        """
        返回包含 pass_call, pass_exe 以及相关的 stderr 或性能数据。
        """
        # --- 模拟原本 workflow 的调用方法 ---
        # 对应：pass_call, pass_exe, call_stdout, call_stderr, exe_stdout, exe_stderr = self.dataset.test_opt_correctness(...)
        try:
            # 假设 dataset 已在外部初始化
            pass_call, pass_exe, c_out, c_err, e_out, e_err = dataset.test_opt_correctness(
                code, 
                filename, 
                tmp_dir="triton_run_langchain_tmp/tmp", 
                exe_dir="triton_run_langchain_tmp/pass_exe"
            )
            
            result = {
                "pass_call": pass_call, 
                "pass_exe": pass_exe,
                "call_error": c_err if not pass_call else None,
                "exec_error": e_err if not pass_exe else None,
            }
            
            # 如果成功，尝试解析性能数据（模仿原有的解析逻辑）
            if pass_exe:
                # 这里可以根据 stdout 补充 latency 数据
                result["details"] = e_out[:200]
                
            return result
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

# --- 2. 封装 Tools (直接调用原有的 dataset 方法) ---

def create_triton_tools(dataset):
    """
    通过闭包将你的 dataset 实例注入到工具中
    """
    
    @tool
    def run_test_and_get_perf(code: str, filename: str) -> str:
        """
        [EXECUTION] 直接调用底层 dataset 接口进行正确性校验和性能测试。
        返回包含 pass_call, pass_exe 以及相关的 stderr 或性能数据。
        """
        # --- 模拟原本 workflow 的调用方法 ---
        # 对应：pass_call, pass_exe, call_stdout, call_stderr, exe_stdout, exe_stderr = self.dataset.test_opt_correctness(...)
        try:
            # 假设 dataset 已在外部初始化
            pass_call, pass_exe, c_out, c_err, e_out, e_err = dataset.test_opt_correctness(
                code, 
                filename, 
                tmp_dir="triton_run_langchain_tmp/tmp", 
                exe_dir="triton_run_langchain_tmp/pass_exe"
            )
            
            result = {
                "pass_call": pass_call, 
                "pass_exe": pass_exe,
                "call_error": c_err if not pass_call else None,
                "exec_error": e_err if not pass_exe else None,
            }
            
            # 如果成功，尝试解析性能数据（模仿原有的解析逻辑）
            if pass_exe:
                # 假设输出中包含 Latency 等关键字，或者 dataset 有其他属性记录了结果
                result["message"] = "Correctness check passed."
                # 这里可以根据 stdout 补充 latency 数据
                result["details"] = e_out[:200]
                
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    @tool
    def curate_cheatsheet(ops_json: str):
        """[CURATION] 将当前发现的优化策略或失败模式沉淀到知识库。"""
        manager = get_manager()
        manager.apply_operations(ops_json)
        save_manager(manager)
        return f"知识库已更新：{manager.get_stats()}"

    @tool
    def read_cheatsheet(top_k: int = 20):
        """[MEMORY] 读取知识库中最高热度的 20 条优化建议。"""
        manager = get_manager()
        return manager.to_string_for_prompt(top_k_hot=top_k)

    return [run_test_and_get_perf, curate_cheatsheet, read_cheatsheet]

# --- 3. 核心 Workflow 类 ---

class TritonLangChainWorkflow:
    def __init__(self, dataset, model_name="gpt-4.1-nano"):
        self.dataset = dataset
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.tools = create_triton_tools(dataset)
        
        # 这里的 System Prompt 替代了原本的 prompt_for_generation 和 prompt_for_reflection
        self.system_prompt = """You are a Triton kernel expert, you task is to write triton kernels according to given instructions. Here are some rules that you need to follow:

"""

        sys_for_gen = """You are an expert Python programmer specializing in NVIDIA Triton kernels, specifically targeting **AMD GPUs using the ROCm environment**.
Your task is to generate a Python code snippet containing a Triton kernel based on the following request:

**Target Platform:** AMD GPU (ROCm)

**Output Requirements:**
1.  **AMD Compatibility:** Generate code compatible with AMD GPUs and ROCm. **DO NOT use CUDA-specific features or functions (e.g., `tl.libdevice`).**
2.  **Complete Code:** Generate a single, complete, and syntactically correct Python code block.
3.  **Triton Kernel:** The core logic must be implemented within a Triton kernel function decorated with `@triton.jit`.
4.  **Imports:** ALWAYS include necessary imports at the beginning:
    ```python
    import torch
    import triton
    import triton.language as tl
    # import math # Only if standard math functions are truly needed outside the kernel
    ```
    Include other imports *only if absolutely necessary*.
5.  **Function Signature (CRITICAL):**
    *   Define EACH function with EXACTLY the signature shown above.
    *   DO NOT change parameter names, counts, or order.
    *   Ensure all parameters in function calls match their function definitions.
    *   **Type Hints:** Use PyTorch tensor type hints (e.g., `x: torch.Tensor`) for tensor arguments. **DO NOT use `tl.pointer`**. Use standard Python types (e.g., `int`, `float`) or `tl.constexpr` for others.
    *   **`constexpr`:** Use `tl.constexpr` **ONLY** for arguments that *must* be known at compile time, typically block sizes (like `BLOCK_SIZE`, `BLOCK_M`) or flags that change the kernel's structure (like `IS_EVEN_K`). Simple numerical values like `eps` or `dropout_p` are usually *not* `constexpr`.
6.  **Data Types:** Be precise with data types inside the kernel (e.g., `tl.float16`, `tl.float32`, `tl.int32`). Ensure type compatibility. Assume input tensors might be `torch.float16` or `torch.float32` unless specified otherwise. Pay attention to potential type promotion/conversion needs (e.g., using `.to(tl.float32)` for accumulations).
7.  **Triton Operations:**
    *   Use Triton language functions correctly (`tl.load`, `tl.store`, `tl.dot`, `tl.arange`, `tl.program_id`, `tl.where`, `tl.atomic_cas`, etc.).
    *   **Pointers & Masks:** Be extremely careful when constructing pointers using offsets and strides. Ensure masks in `tl.load`/`tl.store` are correctly computed and match pointer dimensions. Avoid `ValueError: Mask argument cannot be block type...` or `ValueError: Unsupported ptr type...`.
    *   **`tl.dot`:** Ensure inputs are 2D blocks and have compatible types (e.g., float16, bfloat16). Int32 is generally not supported directly as input.
    *   **`tl.arange`:** Arguments `start` and `end` **must be `tl.constexpr`**.
    *   **Math:** Use functions from `tl.math` where available (e.g., `tl.math.exp`, `tl.math.sqrt`). Check function existence; avoid assuming functions like `tanh` or `log1p` exist if they don't in `tl.math`.
8.  **Triton Version:** Assume Triton version 3.1.0 or later.
9.  Output your answer in json format, with the format as follows: {\"thought\": \"\", \"code\": \"\"}. Please strictly output in JSON format. The \"thought\" field contains the explicit cheatsheet IDs you referred to in such a format: [ID1, ID2, ...]. Generate the correct and optimized code without explanation, which we can run directly in the \"code\" field.

**FINAL VERIFICATION:**
Before completing, verify:
1. ALL functions defined in the code have EXACT signatures matching the required function signatures above.
2. ALL function calls exactly match their definitions in terms of parameter counts and names.
3. No functions are called without being defined.
4. No parameters are missing from your implementations.
"""
        tool_usage = """**Tool Description:**
1. When generating the triton code, you shouldn't change the filename and instruction. And you can use `read_cheatsheet` to access the historical experience and knowledege of triton kernel. And you can set the `top_k` parameter to choose how many most-related items you want to see.
2. After generating the code, you should use `run_test_and_get_perf` to get the execution result and error information. If `pass_exe` is False, you should analyze returned `exec_error` and reflect, then re-generate the solution.
3. Once the task is succeeded, please extract some common patterns or knowledges, then call `curate_cheatsheet` to store these into the cheatsheet. You have multiple operation choices, Available Operations:
    (1). ADD
    - section: one of [meta_reasoning, solutions_and_patterns, failed_attempts]
    - content: high-level natural-language strategy, knowledge or insight

    (2). UPDATE
    - target_id: memory item identifier
    - content: refined high-level description

    (3). VARIATION
    - target_id: memory item identifier
    - name: short variant name
    - content: high-level alternative approach

    (4). EXPAND
    - target_id: memory item identifier
    - content: new edge case or consideration
"""

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt= sys_for_gen + tool_usage
        )

    def run_sample(self, instruction: str, filename: str, function_signature: str, iter: int):
        """模拟原本 OptimAgent 处理单个样本的流程"""
        print(f"\n[Processing]: {filename}")
        
        with get_openai_callback() as cb:
            full_trace = ""
            
            # 使用 Stream 可视化 Agent 的思考过程
            for event in self.agent.stream(
                {"messages": [
                    {
                        "role": "user", 
                        "content": f"""**Request:**
{instruction}

**CRITICAL FUNCTION INFORMATION:**
Based on analysis, the implementation requires these EXACT function signatures:
{function_signature}

**Filename:**
{filename}
"""
                    }
                ]
                },
                stream_mode="values"
            ):
                final_response = None
                if "messages" in event:
                    last_msg = event["messages"][-1]
                    
                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        for tc in last_msg.tool_calls:
                            print(f"🧠 [Agent 决策]: 调用 {tc['name']}...")
                    
                    if last_msg.type == "ai" and last_msg.content:
                        if not (hasattr(last_msg, "tool_calls") and last_msg.tool_calls):
                            # print(f"🤖 [Final Response]:\n{last_msg.content}")
                            full_trace += last_msg.content
                            
                            # 保存生成的 response
                            final_response = last_msg.content
                            try:
                                code = clear_code(clear_json(final_response)["code"])
                                # code = json.loads(final_response).get("code", "")
                            except:
                                print(f"failed to extract code for {filename}, directly parse code")
                                raw_code = final_response.split("\"code\":")[1]
                                raw_code = raw_code.split("}")[0]
                                code = clear_code(raw_code)
                            
                            if not code:
                                print(f"⚠️ [JSON 解析失败]: {e}")
                                dict_to_save.append({
                                    "filename": filename,
                                    "instruction": instruction,
                                    "response": "",
                                    "pass_exe": False,
                                    "pass_call": False,
                                    "call_error": f"JSON 解析失败: {e}",
                                    "exec_error": None,
                                })
                            else:
                                try:
                                    # --- 直接调用工具函数获取结果 (不通过 Agent) ---
                                    tool_result = run_test_outside(code, filename)
                                    # print(f"🔧 [工具函数结果]: {tool_result}")
                                    if tool_result.get("status") == "error":
                                        print("⚠️ [执行失败 - 工具调用异常]")
                                        dict_to_save.append({
                                            "filename": filename,
                                            "instruction": instruction,
                                            "response": code,
                                            "pass_exe": False,
                                            "pass_call": False,
                                            "call_error": None,
                                            "exec_error": tool_result.get("message"),
                                        })
                                    else:
                                        if tool_result['pass_exe']:
                                            print(f"✅ [执行结果]: pass_call={tool_result['pass_call']}, pass_exe={tool_result['pass_exe']}")
                                        else:
                                            print(f"❌ [执行结果]: pass_call={tool_result['pass_call']}, pass_exe={tool_result['pass_exe']}")
                                        dict_to_save.append({
                                            "filename": filename,
                                            "instruction": instruction,
                                            "response": code,
                                            "pass_exe": tool_result["pass_exe"],
                                            "pass_call": tool_result["pass_call"],
                                            "call_error": tool_result.get("call_error"),
                                            "exec_error": tool_result.get("exec_error"),
                                        })
                                except Exception as e:
                                    print(f"⚠️ [JSON 解析失败]: {e}")
                                    dict_to_save.append({
                                        "filename": filename,
                                        "instruction": instruction,
                                        "response": "",
                                        "pass_exe": False,
                                        "pass_call": False,
                                        "call_error": f"JSON 解析失败: {e}",
                                        "exec_error": None,
                                    })


            # --- 运行结束后同步热度 (Record Usage) ---
            # 模仿原代码: self.cheatsheet_manager.record_usage(mem.thoughts, iter)
            final_manager = get_manager()
            final_manager.record_usage(model_thought=final_response, current_iter=iter)
            
            # 模仿原代码: self.cheatsheet_manager.prune_by_utility
            final_manager.prune_by_utility(min_usage_ratio=0.5)
            
            save_manager(final_manager)
            
            print(f"📊 Token 消耗: {cb.total_tokens} | 成本: ${cb.total_cost:.4f}")

# --- 4. 启动示例 ---

if __name__ == "__main__":
    # 假设你已经有了原本 workflow 里的 dataset 实例
    # from your_original_code import YourDatasetClass
    # my_dataset = YourDatasetClass(...)
    
    # 测试 tritonbench 数据集
    dataset = TritonBench(statis_path="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_comp_alpac_v1_fixed_with_difficulty.json", 
                          py_folder="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_v1", 
                          instruction_path="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_comp_alpac_v1_fixed_with_difficulty.json", 
                          py_interpreter="python", 
                          golden_metrics="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/performance_metrics/perf_G/golden_metrics",
                          perf_G_path="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/performance_metrics/perf_G",
                          )
    # 启动工作流
    workflow = TritonLangChainWorkflow(
        dataset=dataset,
        model_name='gpt-4.1-mini'
    )
    # workflow.run_sample(
    #     instruction="Implement a fast softmax kernel in Triton.",
    #     filename="softmax_kernel.py"
    # )

    # 只跑给定范围
    start_idx = 0
    length = -1
    epoch = 5
    for iter in range(epoch):
        for ps in dataset.problem_states[start_idx : start_idx + length if length > 0 else None]:
            # print all attributes of ps
            # for attr in dir(ps):
            #     print(f"{attr}")
            # print(ps.filename, extract_function_signatures(ps.label))

            workflow.run_sample(
                instruction=ps.instruction,
                filename=ps.filename,
                function_signature=extract_function_signatures(ps.label),
                iter=iter
            )

        # 保存结果到本地 JSON 文件
        with open(f"triton_run_langchain_tmp/results_iter_{iter}.json", "w", encoding="utf-8") as f:
            json.dump(dict_to_save, f, ensure_ascii=False, indent=4)
        
        # calculate accuracy
        acc = 0
        for item in dict_to_save:
            if item["pass_exe"]:
                acc += 1
        acc /= len(dict_to_save)
        print(f"Epoch {iter} - Accuracy: {acc:.4f}")

        dict_to_save.clear()  # 清空列表以准备下一轮迭代

