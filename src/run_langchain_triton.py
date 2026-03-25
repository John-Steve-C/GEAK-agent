import json
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from langchain_openai import ChatOpenAI
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.store.memory import InMemoryStore
from langchain.agents.structured_output import ToolStrategy

# --- 1. 定义上下文和结构化响应 ---

@dataclass
class TritonContext:
    user_id: str
    current_iteration: int = 0

@dataclass
class CuratorResponse:
    """策展人 Agent 的输出格式"""
    reasoning: str
    # 我们直接让 LLM 返回操作列表，然后在工具中调用你的 apply_operations 逻辑
    operations: List[Dict] 

# --- 2. 将 Cheatsheet 逻辑封装为 LangChain Tools ---

@tool
def get_cheatsheet_for_prompt(runtime: ToolRuntime[TritonContext]) -> str:
    """
    获取当前的 Triton 优化手册（Cheatsheet）。
    Agent 在思考前应先调用此工具获取长期记忆。
    """
    store = runtime.store
    # 从 Store 中获取数据，如果没有则初始化
    mem = store.get(("cheatsheet",), runtime.context.user_id)
    data = mem.value if mem else {"meta_reasoning": [], "solutions_and_patterns": [], "failed_attempts": []}
    
    # 模拟你代码中的 to_string_for_prompt 逻辑
    output = []
    for section, items in data.items():
        output.append(f"=== {section.upper()} ===")
        if not items: output.append("(Empty)")
        for item in items:
            output.append(f"[ID: {item['id']}] {item['content']} (Usage: {item.get('usage_count', 0)})")
    return "\n".join(output)

@tool
def update_cheatsheet(ops_json: str, runtime: ToolRuntime[TritonContext]) -> str:
    """
    根据 LLM 提供的 JSON 操作指令更新 Cheatsheet。
    支持操作: ADD, UPDATE, VARIATION, EXPAND, REMOVE。
    """
    store = runtime.store
    user_id = runtime.context.user_id
    
    # 1. 获取当前状态
    mem = store.get(("cheatsheet",), user_id)
    current_data = mem.value if mem else {"meta_reasoning": [], "solutions_and_patterns": [], "failed_attempts": []}
    
    # 2. 实例化你的管理器（这里复用你的逻辑）
    from memories.CheatsheetManager import CheatsheetManager
    manager = CheatsheetManager(initial_state=current_data)
    manager.current_iteration = runtime.context.current_iteration
    
    # 3. 应用操作
    manager.apply_operations(ops_json)
    
    # 4. 写回 Store 实现持久化
    store.put(("cheatsheet",), user_id, manager.data)
    
    return f"Cheatsheet 已更新。当前统计信息: {manager.get_stats()}"

# --- 3. 构建“策展人” Agent ---

# 这里的 System Prompt 结合了你 build_prompt 中的要求
CURATOR_SYSTEM_PROMPT = """
You are a master curator of Triton GPU knowledge. 
Your goal is to extract high-level patterns from Triton kernel development.

**Memory Instructions:**
1. Use 'get_cheatsheet_for_prompt' to see what we already know.
2. If you find a new optimization (e.g., related to GTX 1650 shared memory), use 'update_cheatsheet' to add it.
3. Prefer high-level descriptions over code.
4. Use the specific JSON format for operations: ADD, UPDATE, VARIATION, etc.
"""

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
global_store = InMemoryStore() # 实际生产中可以换成数据库

curator_agent = create_agent(
    model=model,
    tools=[get_cheatsheet_for_prompt, update_cheatsheet],
    system_prompt=CURATOR_SYSTEM_PROMPT,
    store=global_store,
    context_schema=TritonContext,
    # 我们可以让 Agent 直接输出结构化操作，也可以让它通过工具调用
    response_format=ToolStrategy(CuratorResponse) 
)

# --- 4. 模拟一次 Triton 任务后的记忆提取 ---

config = {"configurable": {"thread_id": "wentao_session_1"}}
task_context = """
User wanted to optimize Vector Addition. 
The final solution used 'tl.max_contiguous' to fix alignment issues on non-power-of-2 arrays.
This is a key insight for Triton kernels.
"""

result = curator_agent.invoke(
    {"messages": [{"role": "user", "content": f"Review this task and update memory: {task_context}"}]},
    config=config,
    context=TritonContext(user_id="wentao_001", current_iteration=5)
)

print(f"Reasoning: {result['structured_response'].reasoning}")