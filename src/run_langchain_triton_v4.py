# multi-thread version of v3

import os
import json
import threading
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.callbacks import get_openai_callback

# 严格按要求 import，不修改 Manager 源码
from memories.CheatsheetManager import CheatsheetManager
from dataloaders.TritonBench import TritonBench
from utils.utils import extract_function_signatures, clear_code, clear_json

# --- 1. 线程安全的全局内存知识库 ---
CHEATSHEET_PATH = "tmp_cheatsheet.json"
DEFAULT_PATH = "new_first_cheatsheet.json"
OUTPUT_PATH = "triton_run_langchain_tmp"

class ThreadSafeCheatsheetManager:
    """包装原始的 CheatsheetManager，添加线程锁以支持并发操作"""
    def __init__(self, tmp_path, default_path):
        self.lock = threading.Lock()
        self.save_path = tmp_path
        
        # 仅在初始化时读一次文件
        load_path = tmp_path if os.path.exists(tmp_path) else default_path
        with open(load_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.manager = CheatsheetManager(initial_state=data)

    def apply_operations(self, ops_json: str):
        with self.lock:
            self.manager.apply_operations(ops_json)

    def get_stats(self):
        with self.lock:
            return self.manager.get_stats()

    def to_string_for_prompt(self, top_k_hot: int):
        with self.lock:
            return self.manager.to_string_for_prompt(top_k_hot=top_k_hot)

    def record_usage(self, model_thought, current_iter):
        with self.lock:
            self.manager.record_usage(model_thought=model_thought, current_iter=current_iter)

    def prune_by_utility(self, min_usage_ratio):
        with self.lock:
            self.manager.prune_by_utility(min_usage_ratio=min_usage_ratio)

    def save_to_disk(self):
        """仅在 Epoch 结束或需要持久化时调用"""
        with self.lock:
            with open(self.save_path, "w", encoding="utf-8") as f:
                f.write(self.manager.to_json())

# 初始化全局单例管理器
global_manager = ThreadSafeCheatsheetManager(CHEATSHEET_PATH, DEFAULT_PATH)


def run_test_outside(dataset, code: str, filename: str) -> str:
    """外部执行函数，注意隔离 tmp_dir"""
    try:
        # 【关键修改】基于 filename 生成独立的编译目录，避免多线程冲突
        safe_name = filename.replace(".py", "")
        tmp_dir = f"OUTPUT_PATH/tmp_{safe_name}"
        exe_dir = f"OUTPUT_PATH/exe_{safe_name}"
        
        pass_call, pass_exe, c_out, c_err, e_out, e_err = dataset.test_opt_correctness(
            code, 
            filename, 
            tmp_dir=tmp_dir, 
            exe_dir=exe_dir
        )
        
        result = {
            "pass_call": pass_call, 
            "pass_exe": pass_exe,
            "call_error": c_err if not pass_call else None,
            "exec_error": e_err if not pass_exe else None,
        }
        
        if pass_exe:
            result["details"] = e_out[:200]
            
        return result
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- 2. 封装 Tools ---

def create_triton_tools(dataset, safe_manager: ThreadSafeCheatsheetManager):
    """注入 dataset 和 线程安全的 manager"""
    
    @tool
    def run_test_and_get_perf(code: str, filename: str) -> str:
        """[EXECUTION] 直接调用底层 dataset 接口进行正确性校验和性能测试。"""
        # 调用分离出来的安全执行函数
        result = run_test_outside(dataset, code, filename)
        if result.get("status") == "error":
            return json.dumps(result)
            
        if result.get("pass_exe"):
            result["message"] = "Correctness check passed."
            
        return json.dumps(result)

    @tool
    def curate_cheatsheet(ops_json: str):
        """[CURATION] 将当前发现的优化策略或失败模式沉淀到知识库。"""
        # 直接使用内存里的 manager，有锁保护，无需读写文件
        safe_manager.apply_operations(ops_json)
        return f"知识库已更新：{safe_manager.get_stats()}"

    @tool
    def read_cheatsheet(top_k: int = 20):
        """[MEMORY] 读取知识库中最高热度的 20 条优化建议。"""
        return safe_manager.to_string_for_prompt(top_k_hot=top_k)

    return [run_test_and_get_perf, curate_cheatsheet, read_cheatsheet]

# --- 3. 核心 Workflow 类 ---

class TritonLangChainWorkflow:
    def __init__(self, dataset, manager, model_name="gpt-4.1-nano"):
        self.dataset = dataset
        self.manager = manager
        self.llm = ChatOpenAI(model=model_name, temperature=1.0)
        self.tools = create_triton_tools(dataset, manager)
        
        self.system_prompt = """You are an expert Python programmer specializing in NVIDIA Triton kernels, specifically targeting **AMD GPUs using the ROCm environment**.
Your task is to generate a Python code snippet containing a Triton kernel based on the following request:

**Target Platform:** AMD GPU (ROCm)

**YOUR WORKFLOW (CRITICAL):**
You are an autonomous agent. You must not just guess the answer, but actively use the tools provided to test and refine your code. Follow these steps strictly:
1. **Research:** Use `read_cheatsheet` to check for past experiences or patterns related to this task. And there is a parameter `top_k` you can set to choose how many most-related items you want to see.
2. **Draft & Test:** Write the initial kernel and IMMEDIATELY use `run_test_and_get_perf` to test its correctness. 
3. **Reflect & Fix:** If the test fails (`pass_exe` is False), analyze the `exec_error`, modify your code, and test again. Repeat this until it passes.
4. **Curate:** Once the code passes, use `curate_cheatsheet` to save generalized insights (successful patterns or failure reasons). Provide a strict JSON string mapping your updates:

```json
{
  "reasoning": "Briefly explain what you learned from this task.",
  "operations": [
    // Use one or more of these operation objects as needed:
    { "type": "ADD", "section": "<meta_reasoning | solutions_and_patterns | failed_attempts>", "content": "<High-level new insight>" },
    { "type": "UPDATE", "target_id": "<ID>", "content": "<Refined description for existing memory>" },
    { "type": "VARIATION", "target_id": "<ID>", "name": "<Variant name>", "content": "<Alternative approach>" },
    { "type": "EXPAND", "target_id": "<ID>", "content": "<New edge case or consideration>" }
  ]
}
```

5. **Final Verification:**
Before completing, verify:
    (1). ALL functions defined in the code have EXACT signatures matching the required function signatures above.
    (2). ALL function calls exactly match their definitions in terms of parameter counts and names.
    (3). No functions are called without being defined.
    (4). No parameters are missing from your implementations.
6. **Final Output:** ONLY AFTER the code has successfully passed the test, output your final response. Do NOT output the final code until you have verified it using the test tool!

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
9. At last, output your answer in json format, with the format as follows: {\"thought\": \"\", \"code\": \"\"}. Please strictly output in JSON format. The \"thought\" field contains the explicit cheatsheet IDs you referred to in such a format: [ID1, ID2, ...]. Generate the correct and optimized code without explanation, which we can run directly in the \"code\" field.
""" 
# Your final response must contain the explicit cheatsheet IDs you referred to (e.g., [ID1, ID2]) and the final working code wrapped in standard Python markdown blocks (```python ... ```).

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )

    def run_sample(self, instruction: str, filename: str, function_signature: str, iter: int) -> dict:
        """处理单个样本并返回结果字典，不操作全局变量"""
        print(f"\n[Processing]: {filename}")
        
        result_dict = {
            "filename": filename,
            "instruction": instruction,
            "response": "",
            "pass_exe": False,
            "pass_call": False,
            "call_error": None,
            "exec_error": None,
        }

        with get_openai_callback() as cb:
            final_response = ""
            
            try:
                for event in self.agent.stream(
                    {"messages": [{"role": "user", "content": f"**Request:**\n{instruction}\n\n**CRITICAL FUNCTION INFORMATION:**\n{function_signature}\n\n**Filename:**\n{filename}"}]},
                    stream_mode="values"
                ):
                    if "messages" in event:
                        last_msg = event["messages"][-1]
                        
                        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                            for tc in last_msg.tool_calls:
                                print(f"🧠 [{filename}] 决策: 调用 {tc['name']}...")
                        
                        if last_msg.type == "ai" and last_msg.content:
                            if not (hasattr(last_msg, "tool_calls") and last_msg.tool_calls):
                                final_response = last_msg.content
                
                            # 解析代码
                            # print(final_response)
                            try:
                                code = clear_code(clear_json(final_response)["code"])
                            except Exception as e:
                                print(f"⚠️ [{filename}] JSON 解析失败，尝试强制提取。")
                                try:
                                    raw_code = final_response.split("\"code\":")[1].split("}")[0]
                                    code = clear_code(raw_code)
                                except Exception as e_inner:
                                    result_dict["call_error"] = f"解析完全失败: {e_inner}"
                                    return result_dict
                            
                            result_dict["response"] = code
                            
                            # 最终测试
                            tool_result = run_test_outside(self.dataset, code, filename)
                            if tool_result.get("status") == "error":
                                result_dict["exec_error"] = tool_result.get("message")
                            else:
                                result_dict["pass_exe"] = tool_result["pass_exe"]
                                result_dict["pass_call"] = tool_result["pass_call"]
                                result_dict["call_error"] = tool_result.get("call_error")
                                result_dict["exec_error"] = tool_result.get("exec_error")
                                
                                status = "✅ 成功" if tool_result['pass_exe'] else "❌ 失败"
                                print(f"{status} [{filename}]: pass_call={tool_result['pass_call']}")

                            # 记录 Manager 统计
                            self.manager.record_usage(model_thought=final_response, current_iter=iter)
                
            except Exception as outer_e:
                result_dict["call_error"] = f"Agent 运行异常: {outer_e}"
                
            print(f"📊 [{filename}] Token: {cb.total_tokens} | 成本: ${cb.total_cost:.4f}")
            
        return result_dict

# --- 4. 启动示例 ---

if __name__ == "__main__":
    dataset = TritonBench(statis_path="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_comp_alpac_v1_fixed_with_difficulty.json", 
                          py_folder="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_v1", 
                          instruction_path="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_comp_alpac_v1_fixed_with_difficulty.json", 
                          py_interpreter="python", 
                          golden_metrics="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/performance_metrics/perf_G/golden_metrics",
                          perf_G_path="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/performance_metrics/perf_G",
                          )
    
    workflow = TritonLangChainWorkflow(
        dataset=dataset,
        manager=global_manager,
        model_name='gpt-4.1-mini'
    )

    start_idx = 0
    length = -1
    epoch = 10
    max_workers = 64 # 【关键】设置多线程并发数

    for iter_num in range(epoch):
        tasks = dataset.problem_states[start_idx : start_idx + length if length > 0 else None]
        epoch_results = []
        
        print(f"\n========== 开始 Epoch {iter_num} ==========")
        
        # 使用线程池并发执行 Agent 任务
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_file = {
                executor.submit(
                    workflow.run_sample, 
                    ps.instruction, 
                    ps.filename, 
                    extract_function_signatures(ps.label), 
                    iter_num
                ): ps.filename for ps in tasks
            }
            
            # 收集结果
            for future in as_completed(future_to_file):
                filename = future_to_file[future]
                try:
                    result = future.result()
                    epoch_results.append(result)
                except Exception as exc:
                    print(f"⚠️ {filename} 生成异常: {exc}")

        # Epoch 结束后的清理和保存操作
        global_manager.prune_by_utility(min_usage_ratio=0.5)
        
        # 【统一写盘】
        global_manager.save_to_disk()
        
        # 保存结果日志
        with open(f"OUTPUT_PATH/results_iter_{iter_num}.json", "w", encoding="utf-8") as f:
            json.dump(epoch_results, f, ensure_ascii=False, indent=4)
        
        # 统计正确率
        if epoch_results:
            acc = sum(1 for item in epoch_results if item.get("pass_exe")) / len(epoch_results)
            print(f"\n🏆 Epoch {iter_num} - Accuracy: {acc:.4f} \n")

    # get accumulated accuracy
    flag = [0] * 184
    for iter in range(epoch):
        root = "OUTPUT_PATH/results_iter"
        with open(f"{root}_{iter}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for idx, item in enumerate(data):
            if item['pass_exe']:
                flag[idx] = 1
        acc = sum(flag) / 184
        print(f"Epoch {iter}, accumulated acc = {acc}")

