import json
import uuid
from typing import List, Dict, Any, Optional
import re

class CheatsheetManager:
    def __init__(self, initial_state: Optional[Dict] = None):
        """
        Initialize the KnowledgeBase (Cheatsheet).
        Structure:
        {
            "meta_reasoning": []
            "solutions_and_patterns": [],
            "failed_attempts": []
        }
        """
        self.sections = [
            "meta_reasoning",
            "solutions_and_patterns",
            "failed_attempts"
        ]
        self.current_iteration = 0

        if initial_state:
            self.data = initial_state
        else:
            self.data = {section: [] for section in self.sections}

    def _generate_id(self) -> str:
        """Generates a short, unique 8-char ID for new items."""
        return str(uuid.uuid4())[:8]

    def to_json(self) -> str:
        """Returns the cheatsheet as a JSON string (for storage)."""
        return json.dumps(self.data, indent=4)

    def to_string_for_prompt(self, top_k_hot=-1) -> str:
        """
        Formats the cheatsheet for the LLM prompt.
        Crucially, this MUST include IDs so the LLM can reference them 
        in UPDATE/VARIATION/EXPAND operations.
        """
        output = []
        for section in self.sections:
            output.append(f"=== {section.upper().replace('_', ' ')} ===")
            items = self.data.get(section, [])
            if not items:
                output.append("(Empty)")
            
            if top_k_hot == -1:
                # updating mode, show all items
                recent_items = items
            else:
                # inference mode, only show top_k_hot by usage_count
                sorted_items = sorted(items, key=lambda x: x.get('usage_count', 0), reverse=True)
                recent_items = sorted_items[:top_k_hot]

            for item in recent_items:
                output.append(f"[ID: {item['id']}] {item['content']}")
                
                if top_k_hot == -1:
                    output.append(f"  - Usage Count: {item['usage_count']}, Last Used Iteration: {item['last_used_iter']}, Created Iteration: {item['created_iter']}")
                # Render variations if present
                if 'variations' in item and item['variations']:
                    for v in item['variations']:
                        output.append(f"  - Variation ({v['name']}): {v['content']}")
                
                # Render edge_cases if present
                if 'edge_cases' in item and item['edge_cases']:
                    for e in item['edge_cases']:
                        output.append(f"  - Note: {e['content']}")
            
            output.append("") # Empty line for spacing
            
        return "\n".join(output)

    def get_stats(self) -> str:
        """Returns a string summary of the current token usage/item counts."""
        stats = []
        total_items = 0
        for section in self.sections:
            count = len(self.data.get(section, []))
            stats.append(f"{section}: {count} items")
            total_items += count
        total_length = self.to_string_for_prompt().__len__()
        return f"Total Items: {total_items} | Sections: {', '.join(stats)} | Total Length: {total_length} characters"

    def build_prompt_no_qa(self, raw_prompt) -> str:
        """Constructs the final prompt without Q&A context."""
        
        # This is a simplified template without question/answer
        template = """
You are a master curator of long-term technical knowledge. Your task is to determine what new or refined insights should be added to an existing cheatsheet based on the model’s latest answer.

**Context:**
- The cheatsheet serves as long-term memory to help solve future, similar questions.
- The current model answer reflects reasoning that may not be available later, so extracted insights must be generalized and reusable.
- The cheatsheet prioritizes high-level natural-language descriptions over concrete code.

**CRITICAL: You MUST respond with valid JSON only. Do not use markdown, code blocks, or extra text.**

**Instructions:**
- Review the existing cheatsheet and the current model answer.
- Identify ONLY new, missing, or improved insights that should be added or merged.
- Avoid redundancy: if a similar strategy already exists, extend or vary it instead of duplicating.
- Do NOT regenerate the full cheatsheet.
- Prefer clarity and abstraction over detail.
- Describe logic at a high level; do not store code snippets.
- Copying unrelated items is handled by the system—ONLY specify updates.

**Token Budget Rules:**
- Target total cheatsheet length ≈ 10,000 tokens.
- If the cheatsheet exceeds the budget, older or low-usage items may be summarized or refined.
- Do not propose deletions unless an item is incorrect or strictly superseded.

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet:**
{previous_cheatsheet}

**Current Context:**
{raw_prompt}

**Your Task:**
Output ONLY a valid JSON object with these exact fields:
- reasoning: brief justification for adding or not adding content
- operations: list of operations to apply to the cheatsheet

Available Operations:
1. ADD
   - section: one of [meta_reasoning, solutions_and_patterns, failed_attempts]
   - content: high-level natural-language strategy, knowledge or insight

2. UPDATE
   - target_id: memory item identifier
   - content: refined high-level description

3. VARIATION
   - target_id: memory item identifier
   - name: short variant name
   - content: high-level alternative approach

4. EXPAND
   - target_id: memory item identifier
   - content: new edge case or consideration

If no new information should be added, return an empty operations list.

RESPONSE FORMAT (JSON ONLY):
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
"""
        return template.format(
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),
            raw_prompt=raw_prompt
        )

    def build_prompt_qa(self, question: str, model_answer: str) -> str:
        """Constructs the final prompt using the user's template."""
        
        # This is the template provided in your description
        template = """
You are a master curator of long-term technical knowledge. Your task is to determine what new or refined insights should be added to an existing cheatsheet based on the model’s latest answer.

**Context:**
- The cheatsheet serves as long-term memory to help solve future, similar questions.
- The current model answer reflects reasoning that may not be available later, so extracted insights must be generalized and reusable.
- The cheatsheet prioritizes high-level natural-language descriptions over concrete code.

**CRITICAL: You MUST respond with valid JSON only. Do not use markdown, code blocks, or extra text.**

**Instructions:**
- Review the existing cheatsheet and the current model answer.
- Identify ONLY new, missing, or improved insights that should be added or merged.
- Avoid redundancy: if a similar strategy already exists, extend or vary it instead of duplicating.
- Do NOT regenerate the full cheatsheet.
- Prefer clarity and abstraction over detail.
- Describe logic at a high level; do not store code snippets.
- Copying unrelated items is handled by the system—ONLY specify updates.

**Token Budget Rules:**
- Target total cheatsheet length ≈ 10,000 tokens.
- If the cheatsheet exceeds the budget, older or low-usage items may be summarized or refined.
- Do not propose deletions unless an item is incorrect or strictly superseded.

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet:**
{previous_cheatsheet}

**Current Question:**
{question}

**Model Answer:**
{model_answer}

**Your Task:**
Output ONLY a valid JSON object with these exact fields:
- reasoning: brief justification for adding or not adding content
- operations: list of operations to apply to the cheatsheet

Available Operations:
1. ADD
   - section: one of [solutions_and_patterns, edge_cases_and_pitfalls, meta_reasoning]
   - content: high-level natural-language strategy, knowledge or insight

2. UPDATE
   - target_id: memory item identifier
   - content: refined high-level description

3. VARIATION
   - target_id: memory item identifier
   - name: short variant name
   - content: high-level alternative approach

4. EXPAND
   - target_id: memory item identifier
   - content: new edge case or consideration

If no new information should be added, return an empty operations list.

RESPONSE FORMAT (JSON ONLY):
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
"""
        return template.format(
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),
            question=question,
            model_answer=model_answer
        )
    
    def build_prompt_reflect(self, question: str, model_reflection: str) -> str:
        """Constructs the final prompt using the user's template."""
        
        # This is the template provided in your description
        template = """
You are a master curator of long-term technical knowledge. Your task is to determine what new or refined insights should be added to an existing cheatsheet based on the model’s latest answer.

**Context:**
- The cheatsheet serves as long-term memory to help solve future, similar questions.
- The current model answer reflects reasoning that may not be available later, so extracted insights must be generalized and reusable.
- The cheatsheet prioritizes high-level natural-language descriptions over concrete code.

**CRITICAL: You MUST respond with valid JSON only. Do not use markdown, code blocks, or extra text.**

**Instructions:**
- Review the existing cheatsheet and the current model answer.
- Identify ONLY new, missing, or improved insights that should be added or merged.
- Avoid redundancy: if a similar strategy already exists, extend or vary it instead of duplicating.
- Do NOT regenerate the full cheatsheet.
- Prefer clarity and abstraction over detail.
- Describe logic at a high level; do not store code snippets.
- Copying unrelated items is handled by the system—ONLY specify updates.

**Token Budget Rules:**
- Target total cheatsheet length ≈ 10,000 tokens.
- If the cheatsheet exceeds the budget, older or low-usage items may be summarized or refined.
- Do not propose deletions unless an item is incorrect or strictly superseded.

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet:**
{previous_cheatsheet}

**Current Question:**
{question}

**Model Reflection:**
{model_reflection}

**Your Task:**
Output ONLY a valid JSON object with these exact fields:
- reasoning: brief justification for adding or not adding content
- operations: list of operations to apply to the cheatsheet

Available Operations:
1. ADD
   - section: one of [solutions_and_patterns, edge_cases_and_pitfalls, meta_reasoning]
   - content: high-level natural-language strategy, knowledge or insight

2. UPDATE
   - target_id: memory item identifier
   - content: refined high-level description

3. VARIATION
   - target_id: memory item identifier
   - name: short variant name
   - content: high-level alternative approach

4. EXPAND
   - target_id: memory item identifier
   - content: new edge case or consideration

If no new information should be added, return an empty operations list.

RESPONSE FORMAT (JSON ONLY):
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
"""
        return template.format(
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),
            question=question,
            model_reflection=model_reflection
        )
    
    def build_prompt(self, question: str, model_answer: str, model_reflection: str) -> str:
        """Constructs the final prompt using the user's template."""
        
        # This is the template provided in your description
        template = """
You are a master curator of long-term technical knowledge. Your task is to determine what new or refined insights should be added to an existing cheatsheet based on the model’s latest answer.

**Context:**
- The cheatsheet serves as long-term memory to help solve future, similar questions.
- The current model answer reflects reasoning that may not be available later, so extracted insights must be generalized and reusable.
- The cheatsheet prioritizes high-level natural-language descriptions over concrete code.

**CRITICAL: You MUST respond with valid JSON only. Do not use markdown, code blocks, or extra text.**

**Instructions:**
- Review the existing cheatsheet and the current model answer.
- Identify ONLY new, missing, or improved insights that should be added or merged.
- Avoid redundancy: if a similar strategy already exists, extend or vary it instead of duplicating.
- Do NOT regenerate the full cheatsheet.
- Prefer clarity and abstraction over detail.
- Describe logic at a high level; do not store code snippets.
- Copying unrelated items is handled by the system—ONLY specify updates.

**Token Budget Rules:**
- Target total cheatsheet length ≈ 10,000 tokens.
- If the cheatsheet exceeds the budget, older or low-usage items may be summarized or refined.
- Do not propose deletions unless an item is incorrect or strictly superseded.

Current Cheatsheet Stats:
{cheatsheet_stats}

**Previous Cheatsheet:**
{previous_cheatsheet}

**Current Question:**
{question}

**Model Answer:**
{model_answer}

**Model Reflection:**
{model_reflection}

**Your Task:**
Output ONLY a valid JSON object with these exact fields:
- reasoning: brief justification for adding or not adding content
- operations: list of operations to apply to the cheatsheet

Available Operations:
1. ADD
   - section: one of [meta_reasoning, solutions_and_patterns, failed_attempts]
   - content: high-level natural-language strategy, knowledge or insight

2. UPDATE
   - target_id: memory item identifier
   - content: refined high-level description

3. VARIATION
   - target_id: memory item identifier
   - name: short variant name
   - content: high-level alternative approach

4. EXPAND
   - target_id: memory item identifier
   - content: new edge case or consideration

If no new information should be added, return an empty operations list.

RESPONSE FORMAT (JSON ONLY):
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
"""
        return template.format(
            cheatsheet_stats=self.get_stats(),
            previous_cheatsheet=self.to_string_for_prompt(),    # use full cheatsheet when updating dc itself
            question=question,
            model_answer=model_answer,
            model_reflection=model_reflection
        )
    
    def prune_length(self, max_length: int = 1000000, max_items: int = 100):
        """Prunes the cheatsheet to keep only the most recent items up to max_items."""
        # for section in self.sections:
        #     items = self.data.get(section, [])
        #     if len(items) > max_items:
        #         self.data[section] = items[-max_items:]
        #         print(f"Pruned {section} to last {max_items} items.")
        
        total_length = self.to_string_for_prompt().__len__()
        if total_length > max_length:
            print(f"Pruning cheatsheet from {total_length} to {max_length} characters.")
            # Simple strategy: remove oldest items across all sections until under limit
            # You should remove item in different sections in round-robin fashion
            # except for the meta_reasoning strategy
            while self.to_string_for_prompt().__len__() > max_length:
                for section in self.sections:
                    if section == "meta_reasoning":
                        continue
                    items = self.data.get(section, [])
                    if items:
                        removed_item = items.pop(0)
                        print(f" - Removed from {section}: {removed_item['id']}")
                    if self.to_string_for_prompt().__len__() <= max_length:
                        break
    
    def prune_by_utility(self, min_usage_ratio: float = 0.5, age_threshold: int = 2):
        """
        根据使用率清理 Cheatsheet。
        :param min_usage_ratio: 最小使用率（usage_count / 存在轮数）
        :param age_threshold: 冷却期。新创建的条目在 N 轮内不会被清理。
        """
        print(f"\n--- Starting Utility Pruning (Iter {self.current_iteration}) ---")
        
        for section in self.sections:
            # if section == "meta_reasoning": continue # 元规则通常保留
            
            original_items = self.data[section]
            keep_items = []
            
            for item in original_items:
                age = self.current_iteration - item['created_iter']
                
                # 如果条目还很新，保留它以观察效果
                if age < age_threshold:
                    keep_items.append(item)
                    continue
                
                # 计算“热度”：平均每轮被使用的次数
                heat = item['usage_count'] / age
                
                if heat >= min_usage_ratio:
                    keep_items.append(item)
                else:
                    print(f" - Pruned cold item {item['id']} (Heat: {heat:.2f})")
            
            self.data[section] = keep_items
            print(f"Section {section}: {len(original_items)} -> {len(keep_items)} items after pruning.")
            print(f"Current Cheatsheet Stats: {self.get_stats()}")

    def build_prompt_for_pruning(self, target_length: int = 1000000) -> str:
        """Builds a prompt to ask the LLM to summarize or refine the cheatsheet."""
        template = """
You are a master curator of long-term technical knowledge. The current cheatsheet has exceeded the desired {target_length} character limit. Please help summarize or refine the cheatsheet to fit within this limit.

Current Cheatsheet Stats:
{cheatsheet_stats}

**Current Cheatsheet:**
{cheatsheet}

**Your Task:**
Output ONLY a valid JSON object with these exact fields:
- reasoning: brief justification for adding or not adding content
- operations: list of operations to apply to the cheatsheet

Available Operations:

1. REMOVE
    - target_id: memory item identifier

2. UPDATE
   - target_id: memory item identifier
   - content: refined high-level description

RESPONSE FORMAT (JSON ONLY):
{{
  "reasoning": "...",
  "operations": [
    {{
      "type": "REMOVE",
      "target_id": "item_id_here"
    }}
  ]
}}
"""
        return template.format(
            target_length=target_length,
            cheatsheet_stats=self.get_stats(),
            cheatsheet=self.to_string_for_prompt()
        )

    def _find_item_by_id(self, target_id: str):
        """Helper to locate an item and its parent section list."""
        for section in self.sections:
            for item in self.data[section]:
                if item['id'] == target_id:
                    return item, self.data[section]
        return None, None

    def record_usage(self, model_thought: str, current_iter: int):
        """
        解析格式如 [ID1, ID2, ID3] 的引用列表并更新热度。
        """
        self.current_iteration = current_iter
        unique_ids_in_this_run = set()

        if isinstance(model_thought, str):
            # 匹配方括号内的所有内容，例如 [8a2b3c4d, f5e6d7c8]
            bracket_matches = re.findall(r"\[(.*?)\]", model_thought)
            for content in bracket_matches:
                # 按逗号分割内容
                potential_ids = [item.strip() for item in content.split(",")]
                
                for pid in potential_ids:
                    # 验证是否为 8 位 16 进制 ID 格式，防止误触普通文字
                    if re.fullmatch(r"[a-f0-9]{8}", pid):
                        unique_ids_in_this_run.add(pid)
        elif isinstance(model_thought, list):
            for pid in model_thought:
                if re.fullmatch(r"[a-f0-9]{8}", pid):
                    unique_ids_in_this_run.add(pid)
        else:
            print("Warning: model_thought is neither str nor list, neglecting usage recording.")
            return

        # 更新命中条目的统计数据
        for target_id in unique_ids_in_this_run:
            item, _ = self._find_item_by_id(target_id)
            if item:
                item['usage_count'] += 1
                item['last_used_iter'] = self.current_iteration
                # print(f" >>> [Memory Hit] ID: {target_id} | New Count: {item['usage_count']}")
        
    def apply_operations(self, llm_response: str):
        """
        Parses the LLM JSON response and manually executes the operations.
        This is the 'Manual' step where code modifies the state, not the LLM.
        """
        try:
            # Handle cases where LLM might wrap JSON in markdown blocks
            clean_response = llm_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3]
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3]
            
            parsed = json.loads(clean_response)
            ops = parsed.get("operations", [])
            reasoning = parsed.get("reasoning", "No reasoning provided.")
            
            # print(f"Applying changes based on: {reasoning}")
            
            for op in ops:
                op_type = op.get("type", "").upper()
                
                if op_type == "ADD":
                    self._op_add(op)
                elif op_type == "UPDATE":
                    self._op_update(op)
                elif op_type == "VARIATION":
                    self._op_variation(op)
                elif op_type == "EXPAND":
                    self._op_expand(op)
                elif op_type == "REMOVE":
                    self._op_remove(op)
                # Edge case for misunderstood operation naming
                elif op_type == "META_REASONING":
                    op.section = "meta_reasoning"
                    self._op_add(op)  # Treat as ADD to meta_reasoning
                elif op_type == "SOLUTIONS_AND_PATTERNS":
                    op.section = "solutions_and_patterns"
                    self._op_add(op)  # Treat as ADD to solutions_and_patterns
                elif op_type == "FAILED_ATTEMPTS":
                    op.section = "failed_attempts"
                    self._op_add(op)  # Treat as ADD to failed_attempts
                elif op_type == "EDGE_CASES_AND_PITFALLS":
                    op.section = "edge_cases_and_pitfalls"
                    self._op_add(op)  # Treat as ADD to edge_cases_and_pitfalls
                elif op_type == "API_USAGE":
                    op.section = "api_usage"
                    self._op_add(op)  # Treat as ADD to API_usage
                # last resort: try to infer from content
                else:
                    print(f"Warning: Unknown operation type {op_type}")
                    
        except json.JSONDecodeError:
            print("Error: Failed to parse LLM response as JSON.")
        except Exception as e:
            print(f"Error applying operations: {e}")

    # --- Operation Implementations ---

    def _op_add(self, op):
        section = op.get("section").lower()
        content = op.get("content")
        
        if section not in self.sections:
            # Fallback if LLM hallucinates a section
            print(f" ! UNKNOWN SECTION '{section}', defaulting to 'solutions_and_patterns'.")
            section = "solutions_and_patterns"
            
        new_item = {
            "id": self._generate_id(),
            "content": content,
            "usage_count": 0,
            "last_used_iter": -1,      
            "created_iter": self.current_iteration, # when this item was created
            "variations": [],          
            "edge_cases": []           
        }
        self.data[section].append(new_item)
        print(f" + ADDED to {section}: {content[:50]}...")

    def _op_update(self, op):
        target_id = op.get("target_id")
        content = op.get("content")
        item, _ = self._find_item_by_id(target_id)
        
        if item:
            old_content = item['content']
            item['content'] = content
            print(f" ~ UPDATED {target_id}: {old_content[:30]}... -> {content[:30]}...")
        else:
            print(f" ! FAILED UPDATE: ID {target_id} not found.")

    def _op_variation(self, op):
        target_id = op.get("target_id")
        name = op.get("name")
        content = op.get("content")
        item, _ = self._find_item_by_id(target_id)
        
        if item:
            if "variations" not in item:
                item["variations"] = []
            item["variations"].append({"name": name, "content": content})
            print(f" > VARIATION on {target_id}: {name}")
        else:
            print(f" ! FAILED VARIATION: ID {target_id} not found.")

    def _op_expand(self, op):
        target_id = op.get("target_id")
        content = op.get("content")
        item, _ = self._find_item_by_id(target_id)
        
        if item:
            if "edge_cases" not in item:
                item["edge_cases"] = []
            item["edge_cases"].append({"content": content})
            print(f" > EXPANDED {target_id}: {content[:50]}...")
        else:
            print(f" ! FAILED EXPAND: ID {target_id} not found.")
    
    def _op_remove(self, op):
        target_id = op.get("target_id")
        item, parent_list = self._find_item_by_id(target_id)
        
        if item and parent_list is not None:
            parent_list.remove(item)
            print(f" - REMOVED {target_id}")
        else:
            print(f" ! FAILED REMOVE: ID {target_id} not found.")

# ==========================================
# Example Usage Flow
# ==========================================

if __name__ == "__main__":
    # 1. Initialize Manager
    kb = CheatsheetManager()
    
    # 2. Simulate an existing state (optional)
    kb.apply_operations(json.dumps({
        "operations": [
            {
                "type": "ADD",
                "section": "solutions_and_patterns",
                "content": "Use binary search when dealing with sorted arrays to achieve O(log n) complexity."
            }
        ]
    }))

    # 3. Define the current interaction
    current_q = "How do I find an element in a rotated sorted array efficiently?"
    current_a = "You can still use a modified binary search. Check which half is sorted (left or right) and adjust pointers accordingly."

    # 4. Generate Prompt for LLM
    prompt = kb.build_prompt(current_q, current_a)
    print("\n--- GENERATED PROMPT ---")
    # print(prompt) # Uncomment to see full prompt
    print("(Prompt ready to send to LLM...)")

    print('current cheatsheet: ', kb.to_string_for_prompt())

    # 5. Simulate LLM Response (This would normally come from OpenAI/Anthropic API)
    # The LLM sees the existing ID and decides to make a VARIATION or UPDATE.
    existing_id = kb.data["solutions_and_patterns"][0]["id"]
    
    simulated_llm_response = f"""
    {{
        "reasoning": "The new insight is a specific variation of the binary search pattern for rotated arrays.",
        "operations": [
            {{
                "type": "VARIATION",
                "target_id": "{existing_id}",
                "name": "Rotated Array Search",
                "content": "Check which half is sorted first. If left is sorted and target is in range, search left; else search right."
            }},
            {{
                "type": "ADD",
                "section": "edge_cases_and_pitfalls",
                "content": "In rotated binary search, duplicates can degrade performance to O(n) because strict half-checking fails."
            }}
        ]
    }}
    """

    # 6. Parse and Apply Operations
    print("\n--- APPLYING OPS ---")
    kb.apply_operations(simulated_llm_response)

    # 7. View Result
    print("\n--- FINAL CHEATSHEET ---")
    print(kb.to_string_for_prompt())