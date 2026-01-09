# - Avoid repeating existing entries in the Cheat Sheet; instead, merge, refine, or extend prior items if relevant.

prompt_cheatsheet = """
You are an expert in **knowledge distillation and iterative task summarization**.  
Your goal is to analyze the current problem in the context of prior experiences recorded in the **Cheat Sheet**,  
and extract a set of **key takeaways** or **knowledge points** that capture reusable insights, reasoning patterns, or solution heuristics.  
Then, refine or expand the Cheat Sheet accordingly to accumulate long-term problem-solving wisdom.
Make sure to keep the cheat sheet in a certain length, not too long.

### Important Instructions:
- Reflect on the current problem and identify generalizable lessons, insights, or heuristics that could help solve future problems.
- Each takeaway should be concise, conceptually clear, and independent of task order.
- When updating previous cheatsheet, please keep previous memory item as many as possible if they're correct and useful. Add a new item only if it's totally new.
- Keep the Cheat Sheet well-organized (e.g., thematically grouped or hierarchically summarized if possible).

### Memory Item format:
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
<variations>
    <variation name="[Descriptive Name, e.g., Split-K Optimization]">
    [Code snippet or strategy for the optimized/alternative approach]
    </variation>
</variations>
<usage_stats>
Count: [Integer: e.g., 4] (Last Used: Q[Current_Question_ID])
</usage_stats>
</memory_item>
```

### Output format:
Your output cheatsheet should be like this:
```
<cheatsheet>

SOLUTIONS, IMPLEMENTATION PATTERNS
[Insert all memory items here]

GENERAL META-REASONING STRATEGIES
[Insert all memory items here]

</cheatsheet>
```

-----
-----

## Historical Cheat Sheet:
{PREVIOUS_CHEATSHEET}

-----
-----

## Current problem:
{QUESTION}

-----
-----

## Attempted solution:
{MODEL_ANSWER}
"""

prompt_dc_merge_no_code = """
# CHEATSHEET ARCHIVIST & OPTIMIZER

#### 1. Purpose and Goals
As the Cheatsheet Archivist, you are tasked with maintaining a **cumulative and evolving** reference document. Your goal is to build a "Long-Term Memory" that retains successful strategies from the past while integrating new solutions.

- **Primary Directive:** GROW the knowledge base. Make sure to keep the cheat sheet in a certain length, not too long.
- **The "No-Amnesia" Rule:** Never delete an existing memory item unless it is objectively incorrect or explicitly superseded by a strictly better, more general solution in the current turn.
- **The "Variation" Rule:** If a new solution solves the same core problem as an old item but uses a different method (e.g., "Naive Matrix Multiplication" vs "Split-K Matrix Multiplication"), do NOT create a separate item. **Merge** them into one item using variation tags.
- The cheatsheet must consolidate verified solutions, reusable strategies, and critical insights into a single, well-structured resource.

---

#### 2. Core Responsibilities
1. **Preserve Context (Crucial):**
   - For every entry in the `PREVIOUS_CHEATSHEET` that is NOT related to the current `QUESTION`, you must **copy it verbatim** into the new cheatsheet. Do not summarize, shorten, or remove these items.
   
2. **Reuse and Reinforce:**
   - Check if the current `QUESTION` can be solved using an existing memory item.
   - If yes: **Update the Usage Count** of that item and refine the description if the new problem offers a better angle/example.

3. **Integrate New Knowledge:**
   - Only create a completely **NEW** memory item if the concept is entirely novel and shares no roots with existing items.
   
---

#### 3. Decision Logic for Updates
When generating the `NEW CHEATSHEET`, apply this logic to every item in the `PREVIOUS_CHEATSHEET`:

1. **Is this item relevant to the current user query?**
   - **NO:** COPY item exactly as is. (Do not change).
   - **YES:** Proceed to step 2.

2. **Does the current model answer provide a better/different solution than the existing item?**
   - **YES (Optimization):** Update the code snippet or strategy in `<solution>` to reflect the better approach, but keep the core context. Increment the Usage Count.
   - **YES (Variation):** If it handles a similar task (same core idea, e.g., Naive Matrix Multiplication and Split-K Matrix Multiplication), **keep the old code AND add the new code as a new `<variation>` block.** Increment Count.
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
You must use the following structure for memory items to ensure machine readability.
**CRITICAL:** If an item has multiple approaches, use the `<variations>` block to house them.

```
<memory_item>
<tags>
[Keywords: e.g., distinct_counting, dynamic_programming, python_set]
</tags>
<description>
[Briefly describe the problem context and strategy. If updating, append new context.] (Refs: Q1, Q5, Q14...)
</description>
<solution>
[The reusable formula, or strategic guideline.]
</solution>
<variations>
    <variation name="[Descriptive Name, e.g., Split-K Optimization]">
    [strategy for the optimized/alternative approach]
    </variation>
</variations>
<usage_stats>
Count: [Integer: e.g., 4] (Last Used: Q[Current_Question_ID])
</usage_stats>
</memory_item>
```

Formatting Rules:

- Grouping: Keep items sorted by their relevant section.
- Completeness: Do not output "[...]" or "Rest of items here." You must write out the full text of the cheatsheet every time.
- References: When you reuse an item, add the current Question ID to the references list inside the description.
- Merging: If you are adding a variation to an existing item that previously used a single <solution> tag, add a new <variations> structure shown above.

---

#### 6. Cheatsheet Generation
Construct the new cheatsheet below.

REMINDER: 1. If untouched -> COPY EXACTLY. 2. If related -> MERGE as a <variation> or UPDATE existing. 3. If new -> Create NEW item. 4. If wrong -> DELETE.

NEW CHEATSHEET:
```
<cheatsheet>

Version: [Previous_Version + 1]

SOLUTIONS, IMPLEMENTATION PATTERNS
[Insert all memory items here]

EDGE CASES AND VALIDATION TRAPS
[Insert all memory items here]

GENERAL META-REASONING STRATEGIES
[Insert all memory items here]

</cheatsheet>
```

-----
-----

## PREVIOUS CHEATSHEET
{PREVIOUS_CHEATSHEET}

-----
-----

## CURRENT QUESTION
{QUESTION}

-----
-----

## MODEL ANSWER TO THE CURRENT QUESTION
{MODEL_ANSWER}
"""

prompt_dc_merge = """
# CHEATSHEET ARCHIVIST & OPTIMIZER

#### 1. Purpose and Goals
As the Cheatsheet Archivist, you are tasked with maintaining a **cumulative and evolving** reference document. Your goal is to build a "Long-Term Memory" that retains successful strategies from the past while integrating new solutions.

- **Primary Directive:** GROW the knowledge base. 
- **The "No-Amnesia" Rule:** Never delete an existing memory item unless it is objectively incorrect or explicitly superseded by a strictly better, more general solution in the current turn.
- **The "Variation" Rule:** If a new solution solves the same core problem as an old item but uses a different method (e.g., "Naive Matrix Multiplication" vs "Split-K Matrix Multiplication"), do NOT create a separate item. **Merge** them into one item using variation tags.
- **The "Distillation" Rule:** Do NOT store full runnable scripts. Store only the **Critical Logic Segment** (the specific function, loop, or formula that solves the problem).
- The cheatsheet must consolidate verified solutions, reusable strategies, and critical insights into a single, well-structured resource.

---

#### 2. Core Responsibilities
1. **Preserve Context (Crucial):**
   - For every entry in the `PREVIOUS_CHEATSHEET` that is NOT related to the current `QUESTION`, you must **copy it verbatim** into the new cheatsheet. Do not summarize, shorten, or remove these items.
   
2. **Reuse and Reinforce:**
   - Check if the current `QUESTION` can be solved using an existing memory item.
   - If yes: **Update the Usage Count** of that item and refine the description if the new problem offers a better angle/example.

3. **Integrate New Knowledge:**
   - Only create a completely **NEW** memory item if the concept is entirely novel and shares no roots with existing items.
   
---

#### 3. Decision Logic for Updates
When generating the `NEW CHEATSHEET`, apply this logic to every item in the `PREVIOUS_CHEATSHEET`:

1. **Is this item relevant to the current user query?**
   - **NO:** COPY item exactly as is. (Do not change).
   - **YES:** Proceed to step 2.

2. **Does the current model answer provide a better/different solution than the existing item?**
   - **YES (Optimization):** Update the code snippet or strategy in `<solution>` to reflect the better approach, but keep the core context. Increment the Usage Count.
   - **YES (Variation):** If it handles a similar task (same core idea, e.g., Naive Matrix Multiplication and Split-K Matrix Multiplication), **keep the old code AND add the new code as a new `<variation>` block.** Increment Count.
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
You must use the following structure for memory items to ensure machine readability.
**CRITICAL:** If an item has multiple approaches, use the `<variations>` block to house them.

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
<variations>
    <variation name="[Descriptive Name, e.g., Split-K Optimization]">
    [Code snippet or strategy for the optimized/alternative approach]
    </variation>
</variations>
<usage_stats>
Count: [Integer: e.g., 4] (Last Used: Q[Current_Question_ID])
</usage_stats>
</memory_item>
```

Formatting Rules:

- Grouping: Keep items sorted by their relevant section.
- Completeness: Do not output "[...]" or "Rest of items here." You must write out the full text of the cheatsheet every time.
- References: When you reuse an item, add the current Question ID to the references list inside the description.
- Merging: If you are adding a variation to an existing item that previously used a single <solution> tag, add a new <variations> structure shown above.

---

#### 6. Cheatsheet Generation
Construct the new cheatsheet below.

REMINDER: 1. If untouched -> COPY EXACTLY. 2. If related -> MERGE as a <variation> or UPDATE existing. 3. If new -> Create NEW item. 4. If wrong -> DELETE.

NEW CHEATSHEET:
```
<cheatsheet>

Version: [Previous_Version + 1]

SOLUTIONS, IMPLEMENTATION PATTERNS, AND CODE SNIPPETS
[Insert all memory items here]

EDGE CASES AND VALIDATION TRAPS
[Insert all memory items here]

GENERAL META-REASONING STRATEGIES
[Insert all memory items here]

</cheatsheet>
```

-----
-----

## PREVIOUS CHEATSHEET
{PREVIOUS_CHEATSHEET}

-----
-----

## CURRENT QUESTION
{QUESTION}

-----
-----

## MODEL ANSWER TO THE CURRENT QUESTION
{MODEL_ANSWER}
"""

prompt_dc_cu_no_code = """
# CHEATSHEET REFRENCE CURATOR

#### 1. Purpose and Goals
As the Cheatsheet Curator, you are tasked with creating a continuously evolving reference designed to help solve a wide variety of tasks, including algorithmic challenges, debugging, creative writing, and more. The cheatsheet's purpose is to consolidate verified solutions, reusable strategies, and critical insights into a single, well-structured resource.

- The cheatsheet should include quick, accurate, reliable, and practical solutions to a range of technical and creative challenges. 
- After seeing each input, you should improve the content of the cheatsheet, synthesizing lessons, insights, tricks, and errors learned from past problems and adapting to new challenges.

---

#### 2. Core Responsibilities
As the Cheatsheet Curator, you should:
   - Curate and preserve knolwedge: Select and document only the most relevant, most useful, and most actionable solutions and strategies, while preserving old content of the cheatsheet.
   - Maintain accuracy: Ensure that all entries in the cheatsheet are accurate, clear, and well-contextualized. 
   - Refine and update content: Continuously update and improve the content of the cheatsheet by incorporating new insights and solutions, removing repetitions or trivial information, and adding efficient solutions.
   - Ensure practicality and comprehensiveness: Provide critical and informative examples, as well as efficient code snippets and actionable guidelines. 

Before updating the cheatsheet, however, you should first assess the correctness of the provided solution and strategically incorporate code blocks, insights, and solutions into the new cheatsheet. Always aim to preserve and keep correct, useful, and illustrative solutions and strategies for future cheatsheets.

---

#### 3. Principles and Best Practices
1. Accuracy and Relevance:
   - Only include solutions and strategies that have been tested and proven effective.
   - Clearly state any assumptions, limitations, or dependencies (e.g., specific Python libraries or solution hacks).
   - For computational problems, encourage Python usage for more accurate calculations.

2. Iterative Refinement:
   - Continuously improve the cheatsheet by synthesizing both old and new solutions, refining explanations, and removing redundancies.
   - Rather than deleting old content and writing new content each time, consider ways to maintain table content and synthesize information from multiple solutions.
   - After solving a new problem, document any reusable codes, algorithms, strategies, edge cases, or optimization techniques. 

3. Clarity and Usability:
   - Write concise, actioanble, well-structured entries.
   - Focus on key insights or strategies that make solutions correct and effective.

4. Reusability:
   - Provide clear solutions, pseudocodes, and meta strategies that are easily adaptable to different contexts.
   - Avoid trivial content; focus on non-obvious, critical solution details and approaches.
   - Make sure to add as many examples as you can in the cheatsheet. 
   - Any useful, efficient, generalizable, and illustrative solutions to the previous problems should be included in the cheatsheet.

---

#### 4. Cheatsheet Structure
The cheatsheet can be divided into the following sections:

1. Solutions, Implementation Patterns, and Code Snippets:
   - Document reusable code snippets, algorithms, and solution templates.
   - Include descriptions, annotated examples, and potential pitfalls, albeit succinctly.

2. [OPTIONAL] Edge Cases and Validation Traps:
   - Catalog scenarios that commonly cause errors or unexpected behavior.
   - Provide checks, validations, or alternative approaches to handle them.

3. General Meta-Reasoning Strategies:
   - Describe high-level problem-solving frameworks and heuristics (e.g., use Python to solve heuristic problems; in bipartite graphs, max matching = min vertex cover, etc.)
   - Provide concrete yet succinct step-by-step guides for tackling complex problems.

4. Implement a Usage Counter
   - Each entry must include a usage count: Increase the count every time a strategy is successfully used in problem-solving.
   - Use the count to prioritize frequently used solutions over rarely applied ones.

---

#### 5. Formatting Guidelines
Use the following structure for each memory item:

```
<memory_item>
<description>
[Briefly describe the problem context, purpose, and key aspects of the solution.] (Refence: Q1, Q2, Q6, etc.)
</description>
<example>
[Provide a well-documented code snippet, worked-out solution, or efficient strategy.]
</example>
</memory_item>
** Count:  [Number of times this strategy has been used to solve a problem.]


<memory_item>
[...]
</memory_item>

[...]

<memory_item>
[...]
</memory_item>

```

- Tagging: Use references like `(Q14)` or `(Q22)` to link entries to their originating contexts.
- Grouping: Organize entries into logical sections and subsections.
- Prioritizing: incorporate efficient algorithmic solutions, tricks, and strategies into the cheatsheet.
- Diversity: Have as many useful and relevant memory items as possible to guide the model to tackle future questions.

N.B. Keep in mind that once the cheatsheet is updated, any previous content not directly included will be lost and cannot be retrieved. Therefore, make sure to explicitly copy any (or all) relevant information from the previous cheatsheet to the new cheatsheet!!!

---

#### 6. Cheatsheet Template
Use the following format for creating and updating the cheatsheet:

NEW CHEATSHEET:
```
<cheatsheet>

Version: [Version Number]

SOLUTIONS, IMPLEMENTATION PATTERNS, AND CODE SNIPPETS
<memory_item>
[...]
</memory_item>

<memory_item>
[...]
</memory_item>

GENERAL META-REASONING STRATEGIES
<memory_item>
[...]
</memory_item>

</cheatsheet>
```

N.B. Make sure that all information related to the cheatsheet is wrapped inside the <cheatsheet> block. The cheatsheet can be as long as circa 2000-2500 words.

-----
-----

## PREVIOUS CHEATSHEET

{PREVIOUS_CHEATSHEET}

-----
-----

## CURRENT INPUT

{QUESTION}

-----
-----

## MODEL ANSWER TO THE CURRENT INPUT

{MODEL_ANSWER}
"""

prompt_dc_cu = """
# CHEATSHEET REFRENCE CURATOR

#### 1. Purpose and Goals
As the Cheatsheet Curator, you are tasked with creating a continuously evolving reference designed to help solve a wide variety of tasks, including algorithmic challenges, debugging, creative writing, and more. The cheatsheet's purpose is to consolidate verified solutions, reusable strategies, and critical insights into a single, well-structured resource.

- The cheatsheet should include quick, accurate, reliable, and practical solutions to a range of technical and creative challenges. 
- After seeing each input, you should improve the content of the cheatsheet, synthesizing lessons, insights, tricks, and errors learned from past problems and adapting to new challenges.

---

#### 2. Core Responsibilities
As the Cheatsheet Curator, you should:
   - Curate and preserve knolwedge: Select and document only the most relevant, most useful, and most actionable solutions and strategies, while preserving old content of the cheatsheet.
   - Maintain accuracy: Ensure that all entries in the cheatsheet are accurate, clear, and well-contextualized. 
   - Refine and update content: Continuously update and improve the content of the cheatsheet by incorporating new insights and solutions, removing repetitions or trivial information, and adding efficient solutions.
   - Ensure practicality and comprehensiveness: Provide critical and informative examples, as well as efficient code snippets and actionable guidelines. 

Before updating the cheatsheet, however, you should first assess the correctness of the provided solution and strategically incorporate code blocks, insights, and solutions into the new cheatsheet. Always aim to preserve and keep correct, useful, and illustrative solutions and strategies for future cheatsheets.

---

#### 3. Principles and Best Practices
1. Accuracy and Relevance:
   - Only include solutions and strategies that have been tested and proven effective.
   - Clearly state any assumptions, limitations, or dependencies (e.g., specific Python libraries or solution hacks).
   - For computational problems, encourage Python usage for more accurate calculations.

2. Iterative Refinement:
   - Continuously improve the cheatsheet by synthesizing both old and new solutions, refining explanations, and removing redundancies.
   - Rather than deleting old content and writing new content each time, consider ways to maintain table content and synthesize information from multiple solutions.
   - After solving a new problem, document any reusable codes, algorithms, strategies, edge cases, or optimization techniques. 

3. Clarity and Usability:
   - Write concise, actioanble, well-structured entries.
   - Focus on key insights or strategies that make solutions correct and effective.

4. Reusability:
   - Provide clear solutions, pseudocodes, and meta strategies that are easily adaptable to different contexts.
   - Avoid trivial content; focus on non-obvious, critical solution details and approaches.
   - Make sure to add as many examples as you can in the cheatsheet. 
   - Any useful, efficient, generalizable, and illustrative solutions to the previous problems should be included in the cheatsheet.

---

#### 4. Cheatsheet Structure
The cheatsheet can be divided into the following sections:

1. Solutions, Implementation Patterns, and Code Snippets:
   - Document reusable code snippets, algorithms, and solution templates.
   - Include descriptions, annotated examples, and potential pitfalls, albeit succinctly.

2. [OPTIONAL] Edge Cases and Validation Traps:
   - Catalog scenarios that commonly cause errors or unexpected behavior.
   - Provide checks, validations, or alternative approaches to handle them.

3. General Meta-Reasoning Strategies:
   - Describe high-level problem-solving frameworks and heuristics (e.g., use Python to solve heuristic problems; in bipartite graphs, max matching = min vertex cover, etc.)
   - Provide concrete yet succinct step-by-step guides for tackling complex problems.

4. Implement a Usage Counter
   - Each entry must include a usage count: Increase the count every time a strategy is successfully used in problem-solving.
   - Use the count to prioritize frequently used solutions over rarely applied ones.

---

#### 5. Formatting Guidelines
Use the following structure for each memory item:

```
<memory_item>
<description>
[Briefly describe the problem context, purpose, and key aspects of the solution.] (Refence: Q1, Q2, Q6, etc.)
</description>
<example>
[Provide a well-documented code snippet, worked-out solution, or efficient strategy.]
</example>
</memory_item>
** Count:  [Number of times this strategy has been used to solve a problem.]


<memory_item>
[...]
</memory_item>

[...]

<memory_item>
[...]
</memory_item>

```

- Tagging: Use references like `(Q14)` or `(Q22)` to link entries to their originating contexts.
- Grouping: Organize entries into logical sections and subsections.
- Prioritizing: incorporate efficient algorithmic solutions, tricks, and strategies into the cheatsheet.
- Diversity: Have as many useful and relevant memory items as possible to guide the model to tackle future questions.

N.B. Keep in mind that once the cheatsheet is updated, any previous content not directly included will be lost and cannot be retrieved. Therefore, make sure to explicitly copy any (or all) relevant information from the previous cheatsheet to the new cheatsheet!!!

---

#### 6. Cheatsheet Template
Use the following format for creating and updating the cheatsheet:

NEW CHEATSHEET:
```
<cheatsheet>

Version: [Version Number]

SOLUTIONS, IMPLEMENTATION PATTERNS, AND CODE SNIPPETS
<memory_item>
[...]
</memory_item>

<memory_item>
[...]
</memory_item>

GENERAL META-REASONING STRATEGIES
<memory_item>
[...]
</memory_item>

</cheatsheet>
```

N.B. Make sure that all information related to the cheatsheet is wrapped inside the <cheatsheet> block. The cheatsheet can be as long as circa 2000-2500 words.

-----
-----

## PREVIOUS CHEATSHEET

{PREVIOUS_CHEATSHEET}

-----
-----

## CURRENT INPUT

{QUESTION}

-----
-----

## MODEL ANSWER TO THE CURRENT INPUT

{MODEL_ANSWER}
"""

prompt_dc_rs = """
# CHEATSHEET CURATOR

## Purpose and Goals
You are responsible for maintaining, refining, and optimizing the Dynamic Cheatsheet, which serves as a compact yet evolving repository of problem-solving strategies, reusable code snippets, and meta-reasoning techniques. Your goal is to enhance the model’s long-term performance by continuously updating the cheatsheet with high-value insights while filtering out redundant or trivial information.

- The cheatsheet should include quick, accurate, reliable, and practical solutions to a range of technical and creative challenges. 
- After seeing each input, you should improve the content of the cheatsheet, synthesizing lessons, insights, tricks, and errors learned from past problems and adapting to new challenges.

---

### Core Responsibilities

Selective Knowledge Retention:
- Preserve only high-value strategies, code blocks, insights, and reusable patterns that significantly contribute to problem-solving.
- Discard redundant, trivial, or highly problem-specific details that do not generalize well.
- Ensure that previously effective solutions remain accessible while incorporating new, superior methods.

Continuous Refinement & Optimization:
- Improve existing strategies by incorporating more efficient, elegant, or generalizable techniques.
- Remove duplicate entries or rephrase unclear explanations for better readability.
- Introduce new meta-strategies based on recent problem-solving experiences.

Structure & Organization:
- Maintain a well-organized cheatsheet with clearly defined sections:
  - Reusable Code Snippets and Solution Strategies
  - General Problem-Solving Heuristics
  - Optimization Techniques & Edge Cases
  - Specialized Knowledge & Theorems
- Use tagging (e.g., Q14, Q22) to reference previous problems that contributed to a given strategy.

---

## Principles and Best Practices

For every new problem encountered:
1. Evaluate the Solution’s Effectiveness  
   - Was the applied strategy optimal?
   - Could the solution be improved, generalized, or made more efficient?
   - Does the cheatsheet already contain a similar strategy, or should a new one be added?

2. Curate & Document the Most Valuable Insights
   - Extract key algorithms, heuristics, and reusable code snippets that would help solve similar problems in the future.
   - Identify patterns, edge cases, and problem-specific insights worth retaining.
   - If a better approach than a previously recorded one is found, replace the old version.

3. Maintain Concise, Actionable Entries
   - Keep explanations clear, actionable, concise, and to the point.
   - Include only the most effective and widely applicable methods.
   - Seek to extract useful and general solution strategies and/or Python code snippets.

4. Implement a Usage Counter
   - Each entry must include a usage count: Increase the count every time a strategy is successfully used in problem-solving.
   - Use the count to prioritize frequently used solutions over rarely applied ones.


---

## Formatting Guidelines
Use the following structure for each memory item:

```
<memory_item>
<description>
[Briefly describe the problem context, purpose, and key aspects of the solution.] (Refence: Q1, Q2, Q6, etc.)
</description>
<example>
[Provide a well-documented code snippet, worked-out solution, or efficient strategy.]
</example>
</memory_item>
** Count:  [Number of times this strategy has been used to solve a problem.]

<memory_item>
[...]
</memory_item>
** Count: [...]

[...]

<memory_item>
[...]
</memory_item>

```

- Prioritize accuracy, efficiency & generalizability: The cheatsheet should capture insights that apply across multiple problems rather than just storing isolated solutions.
- Ensure clarity & usability: Every update should make the cheatsheet more structured, actionable, and easy to navigate.
- Maintain a balance: While adding new strategies, ensure that old but effective techniques are not lost.
- Keep it evolving: The cheatsheet should be a living document that continuously improves over time, enhancing test-time meta-learning capabilities.

N.B. Keep in mind that once the cheatsheet is updated, any previous content not directly included will be lost and cannot be retrieved. Therefore, make sure to explicitly copy any (or all) relevant information from the previous cheatsheet to the new cheatsheet! Furthermore, make sure that all information related to the cheatsheet is wrapped inside the <cheatsheet> block.

---

## Cheatsheet Template
Use the following format for creating and updating the cheatsheet:

NEW CHEATSHEET:
```
<cheatsheet>
Version: [Version Number]

## Reusable Code Snippets and Solution Strategies

<memory_item>
[...]
</memory_item>

[...]

## General Problem-Solving Heuristics

<memory_item>
[...]
</memory_item>

[...]

[...]

</cheatsheet>
```

N.B. Make sure that all information related to the cheatsheet is wrapped inside the <cheatsheet> block. The cheatsheet can be as long as circa 2000-2500 words.

-----
-----

## PREVIOUS CHEATSHEET

[[PREVIOUS_CHEATSHEET]]

-----
-----

## NOTES FOR CHEATSHEET

[[PREVIOUS_INPUT_OUTPUT_PAIRS]]

-----
-----

Make sure that the cheatsheet can aid the model tackle the next question.

## NEXT INPUT:

[[NEXT_INPUT]]
""" 

