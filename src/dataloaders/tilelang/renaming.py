# use relative import to import VLLM
# please run with `python -m src.dataloaders.tilelang.renaming`

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

from models.Vllm import VLLMModel

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

system_prompt_tilelang = """
You are a technical writer specializing in GPU Domain Specific Languages (DSLs). Your task is to rewrite an instruction that was originally written for a Triton implementation into a clean TileLang implementation instruction.

The goal is NOT to generate code. Output only the rewritten instruction.

## Strict Constraints

1. Preserve only tested public API integrity.
   - Preserve public wrapper function names, class names, input/output tensor names, and public behavior.
   - Do not require preserving private/internal kernel names, private low-level kernel signatures, Triton launch signatures, or Triton-specific helper arguments.
   - Private TileLang helper names and low-level TileLang kernel argument layouts may be different as long as the public wrapper API and behavior are preserved.

2. Remove Triton-specific wording and APIs.
   - Do not mention Triton in the final rewritten instruction except when unavoidable as historical source context.
   - Remove or rewrite references to @triton.jit, triton.language, tl.constexpr, tl.program_id, tl.load, tl.store, Triton launch syntax, pointer arithmetic, masks, and Triton grid syntax.
   - If the original instruction asks to preserve an original Triton kernel signature, rewrite that as preserving only the public wrapper API and functional behavior.

3. TileLang implementation style.
   - Describe private TileLang kernels as @tl.jit factories that return an inner @T.prim_func.
   - Public wrappers must be normal Python functions that allocate outputs, derive concrete shape/dtype/launch parameters, instantiate the private TileLang kernel factory, and invoke the compiled kernel object directly.
   - Use T.Kernel for launch structure and explicit T.serial/T.parallel loops where needed.
   - Use structured T.Buffer indexing; avoid flat pointer arithmetic.
   - Use T.alloc_shared/T.alloc_local or equivalent TileLang buffers where useful.
   - Use T.copy only for bulk region-to-region transfers. Use scalar assignment for element-wise, masked, or boundary-checked operations.

4. Math, casting, and reductions.
   - Prefer explicit reduction loops or supported TileLang primitives.
   - Use T.cast(value, dtype) or value.astype(dtype) for casting.
   - Do not instruct the implementer to use T.Cast, T.any, T.unary, T.cdiv, T.if_scope, T.get_block_id, T.constant, T.Any, None/-1 buffer dimensions, or Python typing objects inside T.Buffer declarations.

5. Output quality.
   - Keep the algorithmic meaning, tensor roles, shape relationships, boundary behavior, and parallelization strategy.
   - Do not add code.
   - Do not output markdown fences.
"""

# 5. At the end of the rewritten instruction, add the following implementation requirement:

# "This operator should be implemented using TileLang.
# Use TileLang's @tl.jit wrapper and a T.prim_func kernel."

with open("/home/wentao/GEAK-eval/geak_eval/data/TritonBench/data/TritonBench_G_comp_alpac_v1_fixed_with_difficulty.json", "r") as f:
    data = json.load(f)

print_lock = None

# data = data[:5]  # for testing, only process the first 20 items. Set to -1 for all.

FORBIDDEN_REWRITE_TERMS = (
    "@triton.jit",
    "triton.language",
    "tl.constexpr",
    "tl.program_id",
    "tl.load",
    "tl.store",
    "tl.arange",
    "tl.autotune",
    "tl.cumsum",
    "tl.dot",
    "tl.int32",
    "tl.rand",
    "tl.sum",
    "tl.where",
    "T.Cast",
    "T.any",
    "T.unary",
    "T.cdiv",
    "T.if_scope",
    "T.get_block_id",
    "T.constant",
    "T.Any",
    "original Triton signature",
    "Triton interface",
    "Triton kernel signature",
)

FORBIDDEN_REWRITE_REPLACEMENTS = {
    "@triton.jit": "the source JIT decorator",
    "triton.language": "the source DSL module",
    "tl.constexpr": "source compile-time annotations",
    "tl.program_id": "source program-index primitives",
    "tl.load": "source load primitives",
    "tl.store": "source store primitives",
    "tl.arange": "source range helpers",
    "tl.autotune": "TileLang-compatible tuning mechanisms",
    "tl.cumsum": "source cumulative-sum primitives",
    "tl.dot": "source dot-product primitives",
    "tl.int32": "32-bit integer accumulation types",
    "tl.rand": "source random primitives",
    "tl.sum": "source sum primitives",
    "tl.where": "source conditional primitives",
    "T.Cast": "unsupported cast helpers",
    "T.any": "unsupported any helpers",
    "T.unary": "unsupported unary helpers",
    "T.cdiv": "unsupported ceil-divide helpers",
    "T.if_scope": "unsupported scoped conditional helpers",
    "T.get_block_id": "unsupported block-id helpers",
    "T.constant": "unsupported constant helpers",
    "T.Any": "unsupported dynamic buffer markers",
    "original Triton signature": "original low-level signature",
    "Triton interface": "source framework interface",
    "Triton kernel signature": "source kernel signature",
}

model = VLLMModel()
# print(model.client, model.system_prompt)

def sanitize_rewrite_terms(rewritten_instruction: str) -> str:
    for term, replacement in FORBIDDEN_REWRITE_REPLACEMENTS.items():
        rewritten_instruction = rewritten_instruction.replace(term, replacement)
    return rewritten_instruction


def find_rewrite_issues(rewritten_instruction: str):
    return [term for term in FORBIDDEN_REWRITE_TERMS if term in rewritten_instruction]


def rewrite_instruction(idx: int, original_instruction: str, use_openai=True) -> Tuple[int, str, Optional[str], Optional[Exception]]:
    for attempt in range(3):
        try:
            rewritten_instruction = None
            msgs=[
                    {"role": "system", "content": system_prompt_tilelang},
                    {"role": "user", "content": f"""
## Source Triton Instruction to Rewrite
{original_instruction}

## Rewritten TileLang Instruction (NOT the kernel code)
"""
                        }]
            if use_openai:
                client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=msgs,
                    temperature=1.0,
                    max_tokens=2000,
                )
                rewritten_instruction = response.choices[0].message.content
            else:
                rewritten_instruction = model.generate(
                    messages=msgs,
                    max_tokens=8192,
                    temperature=0,
                    enable_thinking=True,
                )

            if rewritten_instruction:
                rewritten_instruction = sanitize_rewrite_terms(rewritten_instruction)
                print("Response: ", rewritten_instruction)
            else:
                print("Empty response!")
            issues = find_rewrite_issues(rewritten_instruction)
            if issues:
                raise ValueError(f"rewritten instruction still contains forbidden terms: {issues}")
            return idx, original_instruction, rewritten_instruction, None
        except Exception as exc:
            if attempt == 2:
                return idx, original_instruction, None, exc
            time.sleep(1.5 * (2 ** attempt) + random.random())


# max_workers = int(os.environ.get("RENAME_THREADS", max(1, min(8, (os.cpu_count() or 4)))))
max_workers = int(os.environ.get("RENAME_THREADS", 64))
print(f"Using max_workers={max_workers} for instruction rewriting.")
# print_lock = threading.Lock()
rewritten = [None] * len(data)

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [
        executor.submit(rewrite_instruction, idx, item["instruction"], False)
        for idx, item in enumerate(data)
    ]
    for future in tqdm(as_completed(futures), total=len(futures), desc="Rewriting"):
        idx, original_instruction, rewritten_instruction, err = future.result()
        if err is not None or rewritten_instruction is None:
            print(f"[ERROR] Failed to rewrite idx={idx}: {err}", file=sys.stderr)
            rewritten[idx] = None
            continue
        rewritten[idx] = rewritten_instruction
        # with print_lock:
        #     print("Original Instruction:\n", original_instruction)
        #     print("\nRewritten Instruction:\n", rewritten_instruction)
        #     print("\n" + "="*80 + "\n")

failed_indices = [idx for idx, item in enumerate(rewritten) if item is None]
if failed_indices:
    raise RuntimeError(f"Instruction rewriting failed for indices: {failed_indices[:20]}")

for idx, item in enumerate(data):
    item["instruction"] = rewritten[idx]
    # "You are a expert in writing tilelang operators for efficient GPU programming. Use tilelang language write a kernel and wrapper according following instruction.\n"
    # if idx > 2:
    #     break

with open("/home/wentao/GEAK-agent/src/dataloaders/tilelang/tilelang_instruction.json", "w") as f:
    json.dump(data, f, indent=4)
