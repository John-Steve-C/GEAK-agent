# Restructure GEAK-agent Around the Main 2×2×3 Experiment

## Summary

Replace [plan.md](/home/wentao/GEAK-agent/plan.md) with a repository-aware roadmap centered on:

1. Whether persistent memory improves kernel generation, and whether tree memory outperforms flat and no memory.
2. Whether these effects hold for Triton and TileLang.
3. Whether memory interacts differently with fixed OptimAgent and autonomous LangChain workflows.

The primary factorial design is:

| Factor | Conditions |
|---|---|
| DSL | Triton, TileLang |
| Workflow | Fixed OptimAgent, LangChain |
| Memory | None, flat, tree |

This produces 12 conditions and 36 primary runs across seeds `0`, `1`, and `2`. Use the existing aligned 184-task datasets with explicit filename manifests for the first-147 adaptation and final-37 held-out split.

Cross-DSL transfer, detailed memory-component ablations, model replication, and qualitative interventions become follow-up experiments rather than blockers for the main result.

## Implementation Changes

### Unified experiment runner

- Add one entry point: `python src/run_experiment.py --config src/configs/main_experiment.yaml [--dry-run|--resume]`.
- Expand the YAML matrix into deterministic run IDs containing provider, model, DSL, workflow, memory, phase, and seed.
- Introduce common interfaces:
  - `Workflow.run_task(context, budget) -> TaskResult`
  - `MemoryBackend.read/update/record_usage/prune/snapshot/freeze`
  - `Evaluator.evaluate_candidate(code, task) -> CandidateResult`
- Continue using `TritonBench`, `TilelangBench`, and `dataloaders/TB_eval` through adapters.
- Convert `main_optimagent_tritonbench.py`, `main_optimagent_tilelang.py`, `run_langchain_triton_v5.py`, and `run_tilelang_eval.py` into thin compatibility wrappers over the unified runner.

### Global model controller

- Add a single provider-neutral model controller constructed from configuration:

```yaml
model:
  backend: vllm          # vllm | openai
  model_id: /shared/models/hf/Qwen3.5-35B-A3B
  base_url: http://localhost:8001/v1
  api_key_env: VLLM_API_KEY
  temperature: 1.0
  max_tokens: 8192
  top_p: 0.95
  seed: 0
```

- `backend: vllm` constructs the existing `VLLMModel`; `backend: openai` constructs `OpenAIModel`.
- Experiment and fixed-workflow code must receive the controller and call only `model.generate(messages, ...)`. No workflow may instantiate a provider directly.
- Normalize the common arguments accepted by both providers: messages, temperature, maximum tokens, top-p, and seed. Keep local-only controls such as min-p, top-k, repetition penalty, and thinking mode in the vLLM provider configuration.
- Preserve the current string return value from `generate()` to avoid changing existing prompt/parsing code. The controller separately records request count, token usage, latency, provider errors, and resolved sampling settings.
- The LangChain adapter obtains its `BaseChatModel` from the same controller/configuration because LangChain requires native tool binding. It must not independently select a model, endpoint, key, or sampling configuration.
- Missing credentials or an unavailable endpoint must fail during startup validation. Never write resolved API keys to logs or output configs.
- The primary 12-condition matrix defaults to local vLLM. Selecting OpenAI creates a separate complete matrix or explicitly named replication; providers must not be mixed across cells in one comparison.

### Memory conditions

- `none`: no persistent cheatsheet, memory prompt, memory tools, or cross-task state.
- `flat`: adapt `CheatsheetManager` behind the common memory interface.
- `tree`: use `TreeCheatsheetManager_v3` with dynamic categories as the proposed method. Older tree managers remain legacy-only.
- Create one canonical documentation-derived item set per DSL:
  - Triton: `new_first_cheatsheet.json`
  - TileLang: `tilelang_first_cheatsheet.json`
- Load identical content and stable item IDs into flat and tree representations. Do not use the existing 452-item Triton tree file in the primary comparison.
- Replace implicit OpenAI embeddings with `/shared/models/hf/jina-embeddings-v3`; precompute/cache embeddings and fail rather than silently falling back.
- Use the task instruction for memory retrieval, top-k `20`, identical scoring weights, pruning threshold `0.5`, and age threshold `2`.
- Persist only flat/tree memory across adaptation tasks and epochs. Reset generated candidates, reflections, and tool history between tasks and epochs.
- Apply updates sequentially in the shared seeded task order. Freeze memory before held-out evaluation; evaluation-time mutation is an error.
- Each workflow learns and freezes its own memory.

### Workflow and retriever behavior

- Fixed workflow: preserve OptimAgent’s programmed retrieve–generate–evaluate–reflect–optimize–update sequence, routed through the common budgets and evaluator.
- LangChain workflow: expose condition-specific tools:
  - `evaluate_candidate`
  - `read_memory` and `update_memory` for flat/tree
  - `retrieve_examples` for Triton only
- Triton uses the same BM25 implementation and `train_crawl.json` corpus:
  - OptimAgent automatically retrieves top-1 by instruction initially and top-1 by prior code during repair.
  - LangChain autonomously calls a top-1 retriever tool over the same corpus.
- TileLang has no static example retriever in either workflow.
- LangChain receives at most 10 model calls and 5 candidate evaluations per task. Fixed OptimAgent uses one generation/evaluation/reflection pass per filename and performs flat/tree curation sequentially.
- Use 8192 completion tokens per call, 300-second model request timeout, 120-second correctness timeout, 600-second performance timeout, and 3600-second task timeout.
- Benchmark every correct candidate and return latency plus normalized speedup to the workflow.
- Select the fastest correct evaluated candidate. If none passes, retain the final evaluated candidate.
- Use isolated evaluation directories and cached references; do not mutate shared `performance_utils.py`.

### Outputs

Write immutable results under:

`outputs/main_experiment/{provider}/{dsl}/{workflow}/{memory}/seed_{seed}/`

Required files:

- `resolved_config.yaml` with secrets redacted
- `environment.json`
- `attempts.jsonl`
- `tool_calls.jsonl`
- `task_results.jsonl`
- `metrics.json`
- `memory/initial.json`, per-epoch snapshots, and `final_frozen.json`
- `checkpoint.json`

Each attempt records task ID, paired filename, epoch, model provider, token usage, model/evaluator/tool counts, retrieved examples and memory IDs, tree paths, generated-code hash, correctness state, benchmark state, latency, reference latency, normalized speedup, failure type, and wall time.

Replace ambiguous `pass_perf` reporting with separate `perf_evaluated`, `latency_ms`, `reference_latency_ms`, and `normalized_speedup` fields.

## Main Experiment Protocol

### Pilot

- Run all 12 conditions using the vLLM backend, seed `0`, one adaptation epoch, the first five adaptation tasks, and the first five held-out tasks.
- Require successful provider startup, matrix expansion, memory freeze/reset behavior, budget enforcement, output generation, and metric recomputation.

### Primary runs

- Use the vLLM backend with `/shared/models/hf/Qwen3.5-35B-A3B`.
- Run seeds `0`, `1`, and `2`.
- Process the same 147 adaptation tasks for three epochs in every condition.
- In `none`, tasks remain independent and no state survives; this supplies the non-learning adaptation curve.
- In flat/tree, retain only the configured persistent memory.
- Freeze memory and evaluate the same 37 held-out tasks from fresh per-task state.
- Use identical task ordering and budgets for all cells within each seed.

### Metrics and comparisons

- Primary outcome: held-out functional correctness within budget.
- Secondary outcomes: call success, normalized speedup, fastest correct latency, attempts to first correct result, anytime success, tokens, model calls, evaluator calls, and wall time.
- Planned contrasts:
  - Tree versus flat, flat versus none, and tree versus none within each DSL/workflow.
  - Memory-gain interaction between Triton and TileLang.
  - Memory-gain interaction between fixed and LangChain.
- Analyze filenames pairwise using paired bootstrap 95% confidence intervals and McNemar tests for correctness.
- Report correctness coverage before conditional speedup.
- Never compare raw Triton and TileLang latency; compare normalized speedup against same-DSL, same-hardware references.
- For Triton, report automatic OptimAgent retrieval versus LangChain retriever-tool behavior, including tool-call rate, retrieved examples, and downstream success.
- Separate LLM/provider, parsing, compilation, runtime, wrong-output, timeout, reference, and performance-evaluation failures.

## Verification

- Test model-controller selection for `openai` and `vllm`, common `generate()` behavior, provider-specific arguments, LangChain client construction, usage accounting, missing credentials, and secret redaction.
- Verify dry-run expansion produces 36 unique primary runs for one provider.
- Validate all 184 paired filenames, exact ordering, the 147/37 split, and absence of overlap.
- Verify flat/tree initial item parity and frozen-memory mutation rejection.
- With fake model and evaluator implementations, test all 12 tool combinations, hard caps, best-candidate selection, task-state reset, and adaptation-only updates.
- Test memory serialization, query-aware retrieval, local embedding caching, utility pruning, and tree construction from canonical flat items.
- Run one real Triton and one real TileLang canary through both workflows before the pilot.
- Acceptance requires no direct provider construction inside workflows, no OpenAI dependency for vLLM runs, reconstructable metrics from JSONL logs, and exact resume from checkpoints.

## Assumptions

- Local vLLM is the primary backend; OpenAI is globally selectable for later replication.
- A single experiment matrix uses one provider and model throughout.
- Flat and tree start from the same DSL-specific documentation knowledge.
- Fixed and LangChain workflows adapt separate memories.
- Triton alone includes the static code-retrieval comparison.
- Legacy entry points remain available but no longer define experiment configuration.
