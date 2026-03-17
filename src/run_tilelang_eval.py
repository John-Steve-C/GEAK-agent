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
from dataloaders.tilelang.prompt import template_prompt, template_with_cheatsheet
from utils.utils import extract_function_signatures, clear_code, clear_json


def fix_tilelang_prim_func_indent(code: str) -> str:
    lines = code.splitlines()
    out = list(lines)
    i = 0
    while i < len(out):
        line = out[i]
        if line.lstrip().startswith("@T.prim_func"):
            indent = line[:len(line) - len(line.lstrip())]
            j = i + 1
            while j < len(out) and out[j].strip() == "":
                j += 1
            if j < len(out) and out[j].lstrip().startswith("def main"):
                out[j] = indent + out[j].lstrip()
                i = j
        i += 1
    return "\n".join(out)

# --- 1. 线程安全的全局内存知识库 ---
DEFAULT_PATH = "tilelang_first_cheatsheet.json"
OUTPUT_DIR = "../outputs/tilelang_langchain_v4_dc"
CHEATSHEET_PATH = f"{OUTPUT_DIR}/cheatsheet"

class ThreadSafeCheatsheetManager:
    """包装原始的 CheatsheetManager，添加线程锁以支持并发操作"""
    def __init__(self, tmp_path, default_path):
        self.lock = threading.Lock()
        self.save_path = tmp_path
        
        # 仅在初始化时读一次文件
        # load_path = tmp_path if os.path.exists(tmp_path) else default_path
        with open(default_path, "r", encoding="utf-8") as f:
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

    def save_to_disk(self, iter):
        """仅在 Epoch 结束或需要持久化时调用"""
        with self.lock:
            with open(f"{self.save_path}_{iter}.json", "w", encoding="utf-8") as f:
                f.write(self.manager.to_json())

# 初始化全局单例管理器
global_manager = ThreadSafeCheatsheetManager(CHEATSHEET_PATH, DEFAULT_PATH)


def run_test_outside(dataset, code: str, filename: str) -> str:
    """外部执行函数，注意隔离 tmp_dir"""
    try:
        # code = fix_tilelang_prim_func_indent(code)
        # 【关键修改】基于 filename 生成独立的编译目录，避免多线程冲突
        safe_name = filename.replace(".py", "")
        tmp_dir = f"{OUTPUT_DIR}/tmp/{safe_name}"
        exe_dir = f"{OUTPUT_DIR}/exe/{safe_name}"
        
        pass_call, pass_exe, c_out, c_err, e_out, e_err = dataset.test_opt_correctness(
            code, 
            filename, 
            tmp_dir=tmp_dir, 
            exe_dir=exe_dir,
            backend="tilelang",
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
    # return [run_test_and_get_perf]

# --- 3. 核心 Workflow 类 ---

class TritonLangChainWorkflow:
    def __init__(self, dataset, manager, model_name="gpt-4.1-nano"):
        self.dataset = dataset
        self.manager = manager
        self.llm = ChatOpenAI(model=model_name, temperature=1.0)
        self.tools = create_triton_tools(dataset, manager)
        
        # self.system_prompt = template_prompt
        self.system_prompt = template_with_cheatsheet

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
            "token_usage": 0,
            "money_cost": None,
        }

        with get_openai_callback() as cb:
            final_response = ""
            
            try:
                for event in self.agent.stream(
                    {"messages": [{
                        "role": "user", 
                        "content": f"""
**Request:**
You are a expert in writing tilelang operators for efficient GPU programming. Use tilelang language write a kernel and wrapper according following instruction.
{instruction}

**CRITICAL FUNCTION INFORMATION:**
{function_signature}

You MUST start from the following template and then fill in the kernel body.
Template:
```python
@tl.jit
def function_signature(...):

    @T.prim_func
    def main(...):      # Remember to keep the same indent as @T.prim_func

        # kernel body

    return main
```
**Filename:**
{filename}
"""
}]},
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
                            # print('final_response: ', final_response)
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
                            # print("parse code:\n", code)
                            
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
            result_dict["token_usage"] = cb.total_tokens
            result_dict["money_cost"] = cb.total_cost
            
        return result_dict

# --- 4. 启动示例 ---

if __name__ == "__main__":
    dataset = TritonBench(statis_path="/home/wentao/GEAK-agent/src/dataloaders/tilelang/renaming_instruction.json",
                          py_folder="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_v1", 
                          instruction_path="/home/wentao/GEAK-agent/src/dataloaders/tilelang/renaming_instruction.json", 
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
    length = -1      # -1 means for all
    epoch = 5
    max_workers = 64 # 【关键】设置多线程并发数

    # Move accumulated accuracy calculation into the main epoch loop
    flag = [0] * (length if (length > 0) else 184)
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
                    extract_function_signatures(ps.label, mode='tilelang'), 
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
        global_manager.save_to_disk(iter_num)
        
        # 保存结果日志
        with open(f"{OUTPUT_DIR}/results_iter_{iter_num}.json", "w", encoding="utf-8") as f:
            json.dump(epoch_results, f, ensure_ascii=False, indent=4)
        
        # 统计正确率
        if epoch_results:
            acc = sum(1 for item in epoch_results if item.get("pass_exe")) / len(epoch_results)
            print(f"\n🏆 Epoch {iter_num} - Accuracy: {acc:.4f} \n")
        
        # 累计正确率统计
        for idx, item in enumerate(epoch_results):
            if item.get('pass_exe'):
                flag[idx] = 1
        accumulated_acc = sum(flag) / len(epoch_results)    # total number is 184
        print(f"Epoch {iter_num}, accumulated acc = {accumulated_acc}")
        # save result to the file
        with open(f"{OUTPUT_DIR}/accumulated_acc.txt", "a", encoding="utf-8") as f:
            print(f"Epoch {iter_num}, accumulated acc = {accumulated_acc}", file=f)
