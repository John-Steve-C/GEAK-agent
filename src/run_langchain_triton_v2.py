import json
import os
import re
from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.callbacks import get_openai_callback

# 导入你提供的类
from memories.CheatsheetManager import CheatsheetManager

# --- 1. 持久化与 Manager 桥接逻辑 ---
CHEATSHEET_PATH = "tmp_cheatsheet.json"
DEFAULT_PATH = "new_first_cheatsheet.json"

def get_manager() -> CheatsheetManager:
    """加载本地 JSON 并返回 CheatsheetManager 实例"""
    if os.path.exists(CHEATSHEET_PATH):
        with open(CHEATSHEET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif os.path.exists(DEFAULT_PATH):
        with open(DEFAULT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # 如果都没有，初始化空结构
        data = {
            "meta_reasoning": [],
            "solutions_and_patterns": [],
            "failed_attempts": []
        }
    return CheatsheetManager(initial_state=data)

def save_manager(manager: CheatsheetManager):
    """将 Manager 的当前状态写回本地 JSON"""
    with open(CHEATSHEET_PATH, "w", encoding="utf-8") as f:
        json.dump(manager.data, f, indent=4)

# --- 2. 封装增强版 Tools ---

@tool
def curate_knowledge(operations_json: str):
    """
    根据 Agent 的推理结果更新 Triton 知识库。
    输入必须是包含 'reasoning' 和 'operations' 列表的 JSON 字符串。
    操作类型支持: ADD, UPDATE, VARIATION, EXPAND, REMOVE。
    """
    manager = get_manager()
    # 直接调用 CheatsheetManager 原有的 apply_operations 逻辑
    manager.apply_operations(operations_json)
    save_manager(manager)
    return f"知识库已更新。{manager.get_stats()}"

@tool
def read_knowledge(top_k: int = -1):
    """
    读取当前 Triton 优化技巧和历史失败尝试。
    top_k 为 -1 时显示全部，正整数则按热度显示前 K 条。
    """
    manager = get_manager()
    # 使用原有的 to_string_for_prompt 格式化输出
    return manager.to_string_for_prompt(top_k_hot=top_k)

# --- 3. 配置 Agent ---

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=1)

SYSTEM_PROMPT = """You are an expert Python programmer specializing in NVIDIA Triton kernels, specifically targeting **AMD GPUs using the ROCm environment**.
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

**FINAL VERIFICATION:**
Before completing, verify:
1. ALL functions defined in the code have EXACT signatures matching the required function signatures above.
2. ALL function calls exactly match their definitions in terms of parameter counts and names.
3. No functions are called without being defined.
4. No parameters are missing from your implementations.

**Tool Usage:**
You have access to two tools to assist you:
1. `curate_knowledge(operations_json: str)`: Use this tool to update the Triton knowledge base with new insights or optimizations you discover while generating the code. Provide a JSON string with your reasoning and operations.
    You can use the following operation types: ADD, UPDATE, VARIATION, EXPAND, REMOVE.
    (1) ADD
    - section: one of [meta_reasoning, solutions_and_patterns, failed_attempts]
    - content: high-level natural-language strategy, knowledge or insight

    (2) UPDATE
    - target_id: memory item identifier
    - content: refined high-level description

    (3) VARIATION
    - target_id: memory item identifier
    - name: short variant name
    - content: high-level alternative approach

    (4) EXPAND
    - target_id: memory item identifier
    - content: new edge case or consideration

    If no new information should be added, return an empty operations list.

    THE FORMAT OF operations_json MUST BE:
    {{
    "reasoning": "...",
    "operations": [
        {{
        "type": "ADD",
        "section": "solutions_and_patterns",
        "content": "High-level reusable insight..."
        }}
    ]
    }}

2. `read_knowledge(top_k: int)`: Use this tool to read existing Triton optimization techniques and past failed attempts. Set `top_k` to -1 to retrieve all knowledge, or a positive integer to get the top K most relevant entries.

**Response Format:**
Output your answer in json format, with the format as follows: {\"thought\": \"\", \"code\": \"\"}. Please strictly output in JSON format.
The \"thought\" field contains the explicit cheatsheet IDs you referred to in such a format: [ID1, ID2, ...].
Generate the correct and optimized code without explanation, which we can run directly in the \"code\" field.
"""

agent = create_agent(
    model=llm,
    tools=[curate_knowledge, read_knowledge],
    system_prompt=SYSTEM_PROMPT
)

# --- 4. 运行、监控与热度记录 (可视化核心) ---

def run_task(query: str):
    # 初始化 Manager 用于记录热度
    manager = get_manager()
    
    print(f"\n🚀 [任务启动]: {query}")
    print("="*60)

    with get_openai_callback() as cb:
        # full_response 用于最后的 record_usage 热度统计
        full_response = ""
        
        # 使用 stream 模式获取中间过程
        for event in agent.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="values"
        ):
            if "messages" in event:
                last_msg = event["messages"][-1]
                
                # 情况 A: Agent 正在思考并准备调用工具
                if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                    for tc in last_msg.tool_calls:
                        print(f"🧠 [思考]: 正在调用工具 -> {tc['name']}")
                
                # 情况 B: 工具返回了结果
                elif last_msg.type == "tool":
                    print(f"🛠️ [工具反馈]: 执行成功，正在整合信息...")
                
                # 情况 C: Agent 生成了最终内容输出
                elif last_msg.type == "ai" and last_msg.content:
                    # 只有在没有 tool_calls 的情况下才是真正的输出
                    if not (hasattr(last_msg, 'tool_calls') and last_msg.tool_calls):
                        full_response = last_msg.content

        # --- 输出 Agent 的 Response ---
        print("\n🤖 [Agent 回复]:")
        print("-" * 30)
        print(full_response)
        print("-" * 30)

        # --- 自动化热度统计 (record_usage) ---
        # 扫描回复中的 [ID: xxxxxxxx] 并更新本地 JSON
        # fresh_manager = get_manager()
        # fresh_manager.record_usage(model_thought=full_response, current_iter=1)
        # save_manager(fresh_manager)

        # --- 成本可视化 ---
        print(f"\n📊 [统计]: Tokens: {cb.total_tokens} | 费用: ${cb.total_cost:.4f}")
        print(f"🔥 [知识库]: 热度已自动更新并同步至 {CHEATSHEET_PATH}")

# --- 运行测试 ---
if __name__ == "__main__":
    run_task("帮我写一个 Triton 向量加法，并记录针对 GTX 1650 的 memory alignment 技巧。")