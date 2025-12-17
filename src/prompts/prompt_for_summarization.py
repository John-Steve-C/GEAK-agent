prompt_for_dc_full = """
# CHEATSHEET ARCHIVIST & OPTIMIZER

#### 1. Purpose and Goals
As the Cheatsheet Archivist, you are tasked with maintaining a **cumulative and evolving** reference document. Your goal is to build a "Long-Term Memory" that retains successful strategies from the past while integrating new solutions.

- **Primary Directive:** GROW the knowledge base. Do not shrink it. 
- **The "No-Amnesia" Rule:** Never delete an existing memory item unless it is objectively incorrect or explicitly superseded by a strictly better, more general solution in the current turn.
- The cheatsheet must consolidate verified solutions, reusable strategies, and critical insights into a single, well-structured resource.

---

#### 2. Core Responsibilities
1. **Preserve Context (Crucial):**
   - For every entry in the `PREVIOUS_CHEATSHEET` that is NOT related to the current `QUESTION`, you must **copy it verbatim** into the new cheatsheet. Do not summarize, shorten, or remove these items.
   
2. **Reuse and Reinforce:**
   - Check if the current `QUESTION` can be solved using an existing memory item.
   - If yes: **Update the Usage Count** of that item and refine the description if the new problem offers a better angle/example.

3. **Integrate New Knowledge:**
   - If the `QUESTION` introduces a novel problem or a verified trick not present in the memory, create a **NEW** memory item.
   - If the `QUESTION` reveals an edge case for an existing item, **MERGE** this insight into the existing item (e.g., add a "Warning" or "Edge Case" note to the existing entry).

---

#### 3. Decision Logic for Updates
When generating the `NEW CHEATSHEET`, apply this logic to every item in the `PREVIOUS_CHEATSHEET`:

1. **Is this item relevant to the current user query?**
   - **NO:** COPY item exactly as is. (Do not change).
   - **YES:** Proceed to step 2.

2. **Does the current model answer provide a better/different solution than the existing item?**
   - **YES (Optimization):** Update the code snippet or strategy to reflect the better approach, but keep the core context. Increment the Usage Count.
   - **YES (Expansion):** If it handles a new edge case, append the new logic to the existing item. Increment the Usage Count.
   - **NO (Same Strategy):** Keep the item as is. **Crucially: Increment the Usage Count.**

3. **Is there completely new information?**
   - **YES:** Create a new `<memory_item>` at the end of the appropriate section.

---

#### 4. Cheatsheet Structure
The cheatsheet is divided into the following sections. Ensure you maintain the headers:

1. **Solutions, Implementation Patterns, and Code Snippets:**
   - Reusable code, algorithms, and templates.
   - *Requirement:* Must include concrete Python/Algorithm examples.

2. **Edge Cases and Validation Traps:**
   - Scenarios that cause errors and how to handle them.

3. **General Meta-Reasoning Strategies:**
   - High-level frameworks (e.g., "In bipartite graphs, max matching = min vertex cover").

---

#### 5. Formatting Guidelines
You must use the following XML-style structure for memory items to ensure machine readability:

```
<memory_item>
<tags>
[Keywords: e.g., distinct_counting, dynamic_programming, python_set]
</tags>
<description>
[Briefly describe the problem context and strategy. If updating, append new context.] (Refs: Q1, Q5, Q14...)
</description>
<solution>
[The reusable code snippet, formula, or strategic guideline.]
</solution>
<usage_stats>
Count: [Integer: e.g., 4] (Last Used: Q[Current_Question_ID])
</usage_stats>
</memory_item>
```

Formatting Rules:

- Grouping: Keep items sorted by their relevant section.
- Completeness: Do not output "[...]" or "Rest of items here." You must write out the full text of the cheatsheet every time.
- References: When you reuse an item, add the current Question ID to the references list inside the description.

#### 6. Cheatsheet Generation
Construct the new cheatsheet below.

REMINDER: 1. If an entry from the PREVIOUS CHEATSHEET is not touched by the current question, COPY IT EXACTLY. 2. If the current solution uses an existing strategy, INCREMENT THE COUNT. 3. Only delete text if it is proven wrong.

NEW CHEATSHEET:
```
<cheatsheet>

SOLUTIONS, IMPLEMENTATION PATTERNS, AND CODE SNIPPETS
[Insert all memory items here]

EDGE CASES AND VALIDATION TRAPS
[Insert all memory items here]

GENERAL META-REASONING STRATEGIES
[Insert all memory items here]

</cheatsheet>
```

## PREVIOUS CHEATSHEET
{PREVIOUS_CHEATSHEET}

## CURRENT INPUT
{QUESTION}

## MODEL ANSWER TO THE CURRENT INPUT
{MODEL_ANSWER}

"""

prompt_for_dc = """
# CHEATSHEET ARCHIVIST & OPTIMIZER

## 1. Purpose
Maintain a cumulative, evolving cheatsheet that grows over time. Integrate new strategies, refine existing ones, and never remove prior knowledge unless incorrect or strictly superseded.

Core Rules:
- **Grow:** Expand long-term memory with verified insights.
- **No-Amnesia:** Never delete unless wrong or replaced.
- **Merge Variants:** Different methods for same core task → merge under variations.
- **Distill:** Store only essential logic or high-level description—not full scripts.
- **High-Level Descriptions:** Summarize code behavior and strategy, no verbatim code.

---

## 2. Responsibilities
1. **Preserve Context:** Copy unrelated previous items exactly.
2. **Reuse:** If current question matches an item, increment usage and refine description if needed.
3. **Integrate:** Only add new items for genuinely new concepts.

---

## 3. Update Logic
For each prior item:
1. **Relevance:**  
   - Not relevant → copy unchanged.  
   - Relevant → evaluate improvements.

2. **Improvement Types:**  
   - **Optimization:** Replace solution with a clearer or better high-level strategy.  
   - **Variation:** Add alternative approach inside `<variations>`.  
   - **Expansion:** Add new considerations or edge cases.  
   - **Same:** Just increment usage.

3. **New Information:** Create a new memory item.

---

## 4. Cheatsheet Structure
Sections:
1. **Solutions & Patterns:** Reusable strategies and algorithmic insights (high-level, no specific code).  
2. **Edge Cases & Pitfalls:** Common failure modes and how to mitigate.  
3. **Meta-Reasoning:** General problem-solving frameworks.

---

## 5. Item Format
Each memory item must follow:

<memory_item>
<tags>
[Keyword list]
</tags>
<description>
High-level explanation of the strategy and its purpose. Add reference IDs when reused.
</description>
<solution>
High-level natural-language description of the algorithm or logic flow.
</solution>
<variations>
    <variation name="[Variant Name]">
    High-level description of alternative or optimized approach.
    </variation>
</variations>
<usage_stats>
Count: [n] (Last Used: Q[ID])
</usage_stats>
</memory_item>

Rules:
- Keep items grouped by section.
- No placeholders like "[...]".
- If adding variations to an item with only a <solution>, create a new <variations> block.

---

## 6. Generation Instructions
Produce the new cheatsheet:

<cheatsheet>

SOLUTIONS, IMPLEMENTATION PATTERNS, AND CODE SNIPPETS
[Items]

EDGE CASES AND VALIDATION TRAPS
[Items]

GENERAL META-REASONING STRATEGIES
[Items]

</cheatsheet>

-----

## PREVIOUS CHEATSHEET
{PREVIOUS_CHEATSHEET}

## CURRENT QUESTION
{QUESTION}

## MODEL ANSWER
{MODEL_ANSWER}
"""

prompt_for_dc_short = """
# CHEATSHEET ARCHIVIST & OPTIMIZER

## 1. Operating Principles
- Cumulative Memory: Maintain a growing, long-term cheatsheet. Never delete items unless incorrect or strictly superseded.
- Exact Preservation: Unrelated previous items must be copied verbatim.
- Merge Over Duplicate: Same core idea → one memory item with variations.
- Distillation Rule: Store only essential logic and strategy; no full code or low-level details.
- Abstraction First: Describe what & why, not how exactly.
- Length Discipline: Keep total output around 10,000 tokens. If the cheatsheet exceeds the limit:
   - Summarize and refine older or low-usage items.
   - Preserve intent, correctness, and key distinctions.
   - Compress—never drop knowledge outright.

## 2. Update & Integration Procedure
For each update cycle:

A. Process Existing Items
For every prior memory item:
- Irrelevant: Copy unchanged.
- Relevant: Apply exactly one:
  - Same: Increment usage stats only.
  - Optimization: Replace with a clearer or higher-quality high-level strategy.
  - Variation: Add an alternative approach under <variations>.
  - Expansion: Add new edge cases, constraints, or insights.

B. Add New Knowledge
- Create a new memory item only if the concept is genuinely new.

## Cheatsheet Structure & Output Template
<cheatsheet>
SOLUTIONS & PATTERNS
[Memory Items]

EDGE CASES & PITFALLS
[Memory Items]

META-REASONING STRATEGIES
[Memory Items]
</cheatsheet>

### Memory Item Schema (Strict)
<memory_item>
  <tags>[keywords]</tags>
  <description>
    High-level explanation of purpose and idea.
    Include reference IDs when reused.
  </description>
  <solution>
    Natural-language description of the algorithm or logic flow.
  </solution>
  <variations>
    <variation name="Variant Name">
      High-level alternative or optimized approach.
    </variation>
  </variations>
  <usage_stats>
    Count: [n] (Last Used: Q[ID])
  </usage_stats>
</memory_item>

Rules:
- Items must be grouped under the correct section.
- No placeholders (e.g., [...]).
- There should be multiple different memory items in each section for different tasks.
- If adding a variation to an item without <variations>, create the block.

## Inputs
- PREVIOUS CHEATSHEET: {PREVIOUS_CHEATSHEET}
- CURRENT QUESTION: {QUESTION}
- MODEL ANSWER: {MODEL_ANSWER}
"""

prompt_for_dc_human_update = """
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
   - content: high-level natural-language strategy or insight

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
{
  "reasoning": "...",
  "operations": [
    {
      "type": "ADD",
      "section": "solutions_and_patterns",
      "content": "High-level reusable insight..."
    }
  ]
}
"""
