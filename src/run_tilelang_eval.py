# multi-thread version of v3

import os
import json
import shutil
import threading
from collections import OrderedDict
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.callbacks import get_openai_callback

# 严格按要求 import，不修改 Manager 源码
from memories.CheatsheetManager import CheatsheetManager
from dataloaders.TilelangBench import TilelangBench
from dataloaders.tilelang.prompt import template_prompt, template_with_cheatsheet
from utils.utils import extract_function_signatures, clear_code, clear_json

import tilelang

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
ERROR_TYPES = [
    "Compile / launch error",
    "Runtime error",
    "Wrong answer",
    "Boundary failure",
    "Performance fail",
]
BOUNDARY_KEYWORDS = [
    "mask",
    "boundary",
    "out of bounds",
    "out-of-bounds",
    "oob",
    "non-divisible",
    "non divisible",
    "not divisible",
    "divisible",
    "shape mismatch",
    "broadcast",
    "stride",
    "misaligned",
    "tilelang",
]
WRONG_ANSWER_KEYWORDS = [
    "generated output does not match reference output",
    "output mismatch against triton reference",
    "does not match reference",
    "allclose",
    "mismatch",
    "abs max diff",
    "reference and generated output results should be of the same type",
    "generated output is none",
]
PERF_EVAL_LOCK = threading.Lock()


def normalize_error_text(*parts) -> str:
    merged = "\n".join(str(part) for part in parts if part not in (None, "", "None"))
    return merged.lower()


def classify_result(result: dict) -> Optional[str]:
    pass_call = bool(result.get("pass_call"))
    pass_exe = bool(result.get("pass_exe"))
    pass_perf = bool(result.get("pass_perf"))

    if pass_exe and not pass_perf:
        return "Performance fail"
    if pass_perf or (pass_call and pass_exe):
        return None
    if not pass_call:
        return "Compile / launch error"

    error_text = normalize_error_text(result.get("call_error"), result.get("exec_error"))
    if any(keyword in error_text for keyword in BOUNDARY_KEYWORDS):
        return "Boundary failure"
    if any(keyword in error_text for keyword in WRONG_ANSWER_KEYWORDS):
        return "Wrong answer"
    return "Runtime error"


def init_error_distribution():
    return OrderedDict((error_type, 0) for error_type in ERROR_TYPES)


def collect_error_distribution(results):
    distribution = init_error_distribution()
    for item in results:
        error_type = item.get("error_type")
        if error_type in distribution:
            distribution[error_type] += 1
    return distribution


def evaluate_perf_outside(dataset, code: str, filename: str):
    safe_name = filename.replace(".py", "")
    exe_dir = f"{OUTPUT_DIR}/perf_exec/{safe_name}"
    perf_result_dir = f"{OUTPUT_DIR}/perf_results/{safe_name}"
    perf_script_dir = f"{OUTPUT_DIR}/tmp/perf_gen/{safe_name}"
    perf_log_dir = f"{OUTPUT_DIR}/perf_logs/{safe_name}"

    os.makedirs(exe_dir, exist_ok=True)
    with open(os.path.join(exe_dir, filename), "w", encoding="utf-8") as f:
        f.write(code)

    perf_file_name = f"{filename[:-3]}_perf.py"

    try:
        with PERF_EVAL_LOCK:
            dataset.write_perf_file_single(
                input_folder_path=exe_dir,
                results_path=perf_result_dir,
                tmp_dir=perf_script_dir,
                filename=filename,
            )
            dataset.run_perf_script_single(
                script_dir=perf_script_dir,
                log_dir=perf_log_dir,
                gpu_id=0,
                script_name=perf_file_name,
            )

        path_gen = os.path.join(perf_result_dir, f"{filename[:-3]}.json")
        if not os.path.exists(path_gen):
            return False, None, None, f"Performance result not found: {path_gen}"

        _, efficiency, ms = dataset.calculate(path_gen, path_ref=None)
        return True, ms, efficiency, None
    except Exception as e:
        return False, None, None, str(e)
    finally:
        for path in [exe_dir, perf_result_dir, perf_script_dir, perf_log_dir]:
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)

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

    # return [run_test_and_get_perf, curate_cheatsheet, read_cheatsheet]
    return [run_test_and_get_perf]

# --- 3. 核心 Workflow 类 ---

class TritonLangChainWorkflow:
    def __init__(self, dataset, manager, model_name="gpt-4.1-nano"):
        self.dataset = dataset
        self.manager = manager
        self.llm = ChatOpenAI(model=model_name, temperature=1.0)
        self.tools = create_triton_tools(dataset, manager)
        
        self.system_prompt = template_prompt
        # self.system_prompt = template_with_cheatsheet

        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )

    def run_sample(self, instruction: str, filename: str, function_signature: list[str], iter: int) -> dict:
        """处理单个样本并返回结果字典，不操作全局变量"""
        print(f"\n[Processing]: {filename}")
        signature_text = "\n".join(f"- {sig}" for sig in function_signature) if function_signature else "- No explicit public signature found"
        
        result_dict = {
            "filename": filename,
            "instruction": instruction,
            "response": "",
            "pass_exe": False,
            "pass_call": False,
            "pass_perf": False,
            "call_error": None,
            "exec_error": None,
            "ms": None,
            "efficiency": None,
            "error_type": None,
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
**Task Instruction:**
{instruction}

**Required Public API Signatures:**
{signature_text}

Implement the operator in TileLang.
Preserve only the required public API above. Those are the tested wrapper entrypoints.
You may choose different private helper names and different low-level kernel argument shapes internally.
Do not reproduce Triton internal kernel signatures unless you need your own private helpers.
The public wrapper must allocate outputs / derive launch parameters / build the TileLang kernel / invoke the compiled TileLang kernel directly.
Do not use Triton launch syntax like `kernel[(grid,)](...)`.

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
                                print(f"{status} [{filename}]: pass_call={tool_result['pass_call']}, pass_exe={tool_result['pass_exe']}")
                                if not tool_result['pass_call']:
                                    print(f"  Call error: {tool_result.get('call_error')}")
                                elif not tool_result['pass_exe']:
                                    print(f"  Exec error: {tool_result.get('exec_error')}")

                                if result_dict["pass_exe"]:
                                    pass_perf, ms, efficiency, perf_error = evaluate_perf_outside(
                                        self.dataset,
                                        code,
                                        filename,
                                    )
                                    result_dict["pass_perf"] = pass_perf
                                    result_dict["ms"] = ms
                                    result_dict["efficiency"] = efficiency
                                    if perf_error is not None:
                                        result_dict["exec_error"] = perf_error

                            # 记录 Manager 统计
                            self.manager.record_usage(model_thought=final_response, current_iter=iter)
                
            except Exception as outer_e:
                result_dict["call_error"] = f"Agent 运行异常: {outer_e}"
                
            print(f"📊 [{filename}] Token: {cb.total_tokens} | 成本: ${cb.total_cost:.4f}")
            result_dict["token_usage"] = cb.total_tokens
            result_dict["money_cost"] = cb.total_cost
            result_dict["error_type"] = classify_result(result_dict)
            
        return result_dict

# --- 4. 启动示例 ---

if __name__ == "__main__":
    canary_targets = [
        "add_example.py",
        "masked_select.py",
        "lightning_attention.py",
    ]
    target_kernels_env = os.environ.get("TILELANG_TARGET_KERNELS")
    if target_kernels_env:
        target_kernels = [item.strip() for item in target_kernels_env.split(",") if item.strip()]
    elif os.environ.get("TILELANG_CANARY") == "1":
        target_kernels = canary_targets
    else:
        target_kernels = None

    # "/home/wentao/GEAK-agent/src/dataloaders/tilelang/renaming_instruction.json"
    # "/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_comp_alpac_v1_fixed_with_difficulty.json"
    # "/home/wentao/GEAK-agent/src/dataloaders/tilelang/tilelang_instruction.json"
    dataset = TilelangBench(statis_path="/home/wentao/GEAK-agent/src/dataloaders/tilelang/tilelang_instruction.json",
                            py_folder="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_v1", 
                            instruction_path="/home/wentao/GEAK-agent/src/dataloaders/tilelang/tilelang_instruction.json", 
                            py_interpreter="python", 
                            golden_metrics="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/performance_metrics/perf_G/golden_metrics",
                            perf_G_path="/home/wentao/GEAK-eval/geak_eval/data/TritonBench/performance_metrics/perf_G",
                            target_kernels=target_kernels,
                            )
    
    workflow = TritonLangChainWorkflow(
        dataset=dataset,
        manager=global_manager,
        model_name='gpt-4.1-mini'
    )

    start_idx = 0
    length = 50      # -1 means for all
    epoch = 1
    max_workers = 64 # 【关键】设置多线程并发数

    tasks = dataset.problem_states[start_idx : start_idx + length if length > 0 else None]
    filenames = [ps.filename for ps in tasks]
    flag_pass_call = OrderedDict((filename, False) for filename in filenames)
    flag_pass_exe = OrderedDict((filename, False) for filename in filenames)
    flag_pass_perf = OrderedDict((filename, False) for filename in filenames)

    for iter_num in range(epoch):
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
                    extract_function_signatures(ps.label, mode='tilelang', test_code=ps.test_code), 
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
        
        total = len(filenames)
        if total == 0:
            continue

        results_by_filename = {item["filename"]: item for item in epoch_results}
        for filename in filenames:
            item = results_by_filename.get(filename)
            if item is None:
                continue
            if item.get("pass_call"):
                flag_pass_call[filename] = True
            if item.get("pass_exe"):
                flag_pass_exe[filename] = True
            if item.get("pass_perf"):
                flag_pass_perf[filename] = True

        call_rate = sum(1 for item in epoch_results if item.get("pass_call")) / total
        exe_rate = sum(1 for item in epoch_results if item.get("pass_exe")) / total
        perf_rate = sum(1 for item in epoch_results if item.get("pass_perf")) / total
        accumulated_call_rate = sum(flag_pass_call.values()) / total
        accumulated_exe_rate = sum(flag_pass_exe.values()) / total
        accumulated_perf_rate = sum(flag_pass_perf.values()) / total
        error_distribution = collect_error_distribution(epoch_results)

        if epoch_results:
            print(
                f"\n🏆 Epoch {iter_num} - "
                f"call_rate={call_rate:.4f}, exe_rate={exe_rate:.4f}, perf_rate={perf_rate:.4f}\n"
            )
            print(
                f"Epoch {iter_num}, accumulated call_rate = {accumulated_call_rate:.4f}, "
                f"accumulated exe_rate = {accumulated_exe_rate:.4f}, "
                f"accumulated perf_rate = {accumulated_perf_rate:.4f}"
            )
            for error_type, count in error_distribution.items():
                print(f"  {error_type}: {count} ({count / total:.4f})")

        with open(f"{OUTPUT_DIR}/accumulated_acc.txt", "a", encoding="utf-8") as f:
            print(
                f"Epoch {iter_num}: "
                f"call_rate={call_rate:.4f}, exe_rate={exe_rate:.4f}, perf_rate={perf_rate:.4f}, "
                f"accumulated_call_rate={accumulated_call_rate:.4f}, "
                f"accumulated_exe_rate={accumulated_exe_rate:.4f}, "
                f"accumulated_perf_rate={accumulated_perf_rate:.4f}",
                file=f,
            )
            print("Error distribution:", file=f)
            for error_type, count in error_distribution.items():
                print(f"  - {error_type}: {count} ({count / total:.4f})", file=f)
