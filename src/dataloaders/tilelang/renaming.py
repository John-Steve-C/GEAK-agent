from openai import OpenAI
import os
import json
import sys
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Tuple
try:
    from tqdm import tqdm
except Exception:  # fallback if tqdm is unavailable
    def tqdm(iterable=None, total=None, **kwargs):
        return iterable if iterable is not None else range(total or 0)

system_prompt = """
You are an expert in GPU programming and kernel design.

Your task is to rewrite a kernel implementation instruction that was originally written for Triton into a **framework-neutral algorithm description** suitable for implementing with TileLang.

The goal is NOT to generate code.  
The goal is to rewrite the instruction so that it no longer biases the model toward Triton APIs.

------------------------
YOUR OBJECTIVES
------------------------

1. Convert Triton-specific terminology into **framework-neutral descriptions**.

Examples:

Triton-specific → Neutral form

- "_fwd_kernel", "_bwd_kernel"
    → "forward kernel", "backward kernel"

- "grid launch"
    → "parallel execution across dimensions"

- "tl.program_id"
    → "thread/block index"

- "cdiv"
    → "divide the dimension into fixed-size blocks"

- "Triton kernel"
    → "GPU kernel"

2. Preserve the **algorithmic meaning** of the instruction.

You must keep:
- the operator description
- kernel decomposition
- tensor roles
- important parameters
- parallelization strategy

3. Remove or rewrite ALL Triton-specific API references, including:

- @triton.jit
- triton.language / tl.*
- tl.constexpr
- tl.program_id
- tl.load / tl.store
- Triton grid launch syntax

4. Rewrite the description as a **clean algorithm specification** that could be implemented in any GPU DSL.

5. Do NOT add any code.

6. Do NOT mention Triton in the final instruction except when explaining that the original implementation was Triton-based.

------------------------
OUTPUT FORMAT
------------------------

Output ONLY the rewritten instruction.

Structure the instruction using the following sections:

1. Operator Overview
2. Kernel Decomposition
3. Forward Computation
4. Backward Computation
5. Parallelization Strategy
6. Important Parameters
7. Implementation Requirement

------------------------
INPUT
------------------------

The following instruction was originally designed for Triton kernels.
Rewrite it following the rules above.
"""


# 5. At the end of the rewritten instruction, add the following implementation requirement:

# "This operator should be implemented using TileLang.
# Use TileLang's @tl.jit wrapper and a T.prim_func kernel."

with open("/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_comp_alpac_v1_fixed_with_difficulty.json", "r") as f:
    data = json.load(f)

print_lock = None


def rewrite_instruction(idx: int, original_instruction: str) -> Tuple[int, str, Optional[str], Optional[Exception]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": original_instruction}
                ],
                temperature=1.0,
                max_tokens=2000,
            )
            rewritten_instruction = response.choices[0].message.content
            return idx, original_instruction, rewritten_instruction, None
        except Exception as exc:
            if attempt == 2:
                return idx, original_instruction, None, exc
            time.sleep(1.5 * (2 ** attempt) + random.random())


max_workers = int(os.environ.get("RENAME_THREADS", max(1, min(8, (os.cpu_count() or 4)))))
# print_lock = threading.Lock()
rewritten = [None] * len(data)

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [
        executor.submit(rewrite_instruction, idx, item["instruction"])
        for idx, item in enumerate(data)
    ]
    for future in tqdm(as_completed(futures), total=len(futures), desc="Rewriting"):
        idx, original_instruction, rewritten_instruction, err = future.result()
        if err is not None or rewritten_instruction is None:
            # with print_lock:
            print(f"[WARN] Failed to rewrite idx={idx}: {err}", file=sys.stderr)
            rewritten_instruction = original_instruction
        rewritten[idx] = rewritten_instruction
        # with print_lock:
        #     print("Original Instruction:\n", original_instruction)
        #     print("\nRewritten Instruction:\n", rewritten_instruction)
        #     print("\n" + "="*80 + "\n")

for idx, item in enumerate(data):
    item["instruction"] = rewritten[idx]
    # "You are a expert in writing tilelang operators for efficient GPU programming. Use tilelang language write a kernel and wrapper according following instruction.\n"
    # if idx > 2:
    #     break

with open("/home/wentao/GEAK-agent/src/dataloaders/tilelang/renaming_instruction.json", "w") as f:
    json.dump(data, f, indent=4)
