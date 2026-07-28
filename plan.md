# GEAK-agent Main Experiment Roadmap

## Research focus

The main result is a controlled comparison of persistent memory for GPU-kernel generation. The experiment answers three questions:

1. Does persistent memory improve held-out kernel correctness and performance, and does the proposed tree memory outperform flat and no memory?
2. Do memory effects generalize across Triton and TileLang?
3. Does memory interact differently with the programmed OptimAgent workflow and the autonomous LangChain workflow?

The primary factorial design is:

| Factor | Conditions |
|---|---|
| DSL | Triton, TileLang |
| Workflow | Fixed OptimAgent, LangChain |
| Memory | None, flat, tree |

This is a 2×2×3 matrix: 12 conditions and, for seeds `0`, `1`, and `2`, 36 primary runs for one provider/model. Cross-DSL transfer, detailed tree-component ablations, model replication, and qualitative interventions are follow-up experiments. They do not block the primary result.

## Repository structure

The experiment is driven by one configuration and one entry point:

```bash
python src/run_experiment.py --config src/configs/main_experiment.yaml --dry-run
python src/run_experiment.py --config src/configs/main_experiment.yaml --pilot
python src/run_experiment.py --config src/configs/main_experiment.yaml --pilot --model-workers 16
python src/run_experiment.py --config src/configs/main_experiment.yaml --resume
```

The implementation is organized as follows:

- `src/run_experiment.py`: matrix expansion, CLI filters, dry-run, pilot, and resume.
- `src/configs/main_experiment.yaml`: provider, parallelism, matrix, budgets, memory, retriever, and dataset paths.
- `src/configs/paired_split.json`: explicit ordered 147-task adaptation and 37-task held-out filename manifests.
- `src/experiments/model_controller.py`: the only provider selection point.
- `src/experiments/workflows.py`: fixed and LangChain workflow adapters.
- `src/experiments/memory.py`: none, flat, and proposed tree memory backends.
- `src/experiments/evaluator.py`: common Triton/TileLang correctness and performance evaluation.
- `src/experiments/output.py`: immutable logs, metrics, environment capture, and checkpoints.
- `src/experiments/runner.py`: epoch-snapshot batching, ordered memory commits, pruning, freezing, held-out evaluation, and resume.
- `src/analyze_experiment.py`: paired bootstrap, McNemar, and DSL/workflow interaction analysis.

Legacy launchers remain available as thin, condition-specific wrappers:

- `src/main_optimagent_tritonbench.py`: Triton/fixed/tree.
- `src/main_optimagent_tilelang.py`: TileLang/fixed/tree.
- `src/run_langchain_triton_v5.py`: Triton/LangChain/tree.
- `src/run_tilelang_eval.py`: TileLang/LangChain/flat.

They no longer own provider, memory, budget, dataset, or output configuration.

## Global model controller

All non-LangChain workflow code receives one `ModelController` and calls only:

```python
model.generate(messages, ...)
```

The selected backend is global to a matrix:

```yaml
model:
  backend: vllm
  model_id: /shared/models/hf/Qwen3.5-35B-A3B
  base_url: http://localhost:8001/v1
  api_key_env: VLLM_API_KEY
  temperature: 1.0
  max_tokens: 8192
  top_p: 0.95

parallelism:
  model_workers: 8
```

`backend: vllm` constructs `VLLMModel`; `backend: openai` constructs `OpenAIModel`. Both preserve the current string return value and accept messages, temperature, maximum tokens, top-p, and seed. vLLM-only sampling controls remain in the vLLM configuration.

The controller bounds in-flight calls by `model_workers` and records request counts, prompt/completion tokens, provider errors, queue wait, request latency, and resolved sampling settings. Credentials are read from the configured environment variable, validated at startup, and never written to resolved configurations or logs.

LangChain requires a native chat model for tool binding. Its `BaseChatModel` is therefore built by the same controller from the same provider, endpoint, credential, seed, and sampling configuration. Workflows never instantiate provider clients directly.

The primary matrix uses local vLLM throughout. OpenAI runs must use a separate complete matrix or an explicitly named replication with a separate output root; providers are never mixed across comparison cells.

## Dataset and split

Triton and TileLang use the same 184 filenames in the same order. `src/configs/paired_split.json` is the source of truth:

- adaptation: first 147 filenames;
- held-out evaluation: final 37 filenames;
- overlap: none.

Startup validation compares the manifest against both instruction JSON files and fails on a missing, additional, reordered, or duplicated filename. Each seed uses one deterministic adaptation order shared by all 12 cells. The order changes deterministically by epoch but remains paired across conditions.

## Memory conditions

### None

No cheatsheet, memory prompt, memory tool, or cross-task state. Generated candidates, reflections, and tool history are task-local.

### Flat

`src/memories/CheatsheetManager.py` is used through the common memory interface.

### Tree

`src/memories/TreeCheatsheetManager_v3.py` is the proposed memory. Dynamic categories are enabled. Older tree managers are legacy-only and are not used by the main runner.

Flat and tree initialize from the same stable documentation items for each DSL:

- Triton: `src/new_first_cheatsheet.json`;
- TileLang: `src/tilelang_first_cheatsheet.json`.

The tree is constructed from these canonical flat items while preserving their IDs and content. The existing larger Triton tree file is excluded from the primary comparison.

Memory retrieval uses the task instruction, top-k `20`, the manager's shared scoring weights, utility-pruning threshold `0.5`, and age threshold `2`. Embeddings use `Qwen/Qwen3-Embedding-0.6B` from the local mirror at `/shared/models/hf/Qwen3-Embedding-0.6B`; query embeddings receive a kernel-memory retrieval instruction, document embeddings remain unprefixed, and both use normalized last-token pooling. Vectors are cached under the experiment output root and precomputed for initial items. Missing model files or embedding failures stop the run instead of falling back to OpenAI.

Only flat/tree memory persists across adaptation tasks and epochs. Memory updates are sequential in the shared seeded order. After adaptation, memory is frozen and a mutation attempt during held-out evaluation is an error. Fixed and LangChain conditions learn separate memories.

## Workflow behavior

Both workflows implement the common contract:

```python
Workflow.run_task(context, budget) -> TaskResult
Workflow.run_batch(contexts, budget, model_workers) -> list[TaskExecution]
```

Within an epoch, all tasks read the same immutable memory snapshot. Fixed generation and reflection use concurrent stage barriers with `tqdm` progress, while candidate evaluation, fixed-workflow curation, and all persistent-memory mutations remain coordinator-only and deterministic.

The fixed workflow runs one programmed retrieve, generate, evaluate, reflect, and update sequence per filename per epoch. The LangChain workflow binds only the tools valid for its condition:

- all cells: `evaluate_candidate`;
- flat/tree cells: `read_memory`;
- flat/tree adaptation only: `update_memory`;
- Triton only: `retrieve_examples`.

Triton uses one shared BM25 implementation and `src/dataloaders/TB_eval/train_crawl.json`. Fixed OptimAgent retrieves top-1 by instruction once per epoch. LangChain autonomously calls the same top-1 retriever through its tool. TileLang has no static example retriever.

LangChain tasks have hard limits of 10 model requests and 5 candidate evaluations. Fixed tasks instead use one generation, at most one evaluation, and one reflection per epoch; flat/tree adaptation adds one sequential curation request. Per-call completion length is 8192 tokens. Model, correctness, performance, and whole-task timeouts are 300, 120, 600, and 3600 seconds respectively.

Every correct candidate is benchmarked. The workflow receives generated latency, same-DSL reference latency, and normalized speedup. The selected result is the fastest correct evaluated candidate; if no candidate is correct, it is the final evaluated candidate.

Evaluation uses per-run/per-attempt directories and cached reference measurements. The adapters write a private `performance_utils.py` beside each generated benchmark script and never modify the shared GEAK-eval copy.

## Output contract

Primary results are immutable under:

```text
outputs/main_experiment/{provider}/{dsl}/{workflow}/{memory}/seed_{seed}/
```

Pilot outputs are isolated under `outputs/main_experiment/pilot/` so they cannot collide with the primary matrix. Each run contains:

- `resolved_config.yaml` with secrets excluded;
- `environment.json`;
- `attempts.jsonl`;
- `tool_calls.jsonl`;
- `task_results.jsonl`;
- `metrics.json`;
- `memory/initial.json`, per-epoch snapshots, `checkpoint.json`, and `final_frozen.json`;
- top-level `checkpoint.json`.

Attempt records include phase, epoch, seed, paired filename, provider/model, model and evaluator counts, token usage, retrieved example scores, retrieved memory IDs and tree paths, generated-code hash, correctness and benchmark state, generated/reference latency, normalized speedup, failure type, and wall time.

Performance fields are explicit: `perf_evaluated`, `latency_ms`, `reference_latency_ms`, and `normalized_speedup`. The old ambiguous `pass_perf` field is not used in experiment logs.

## Execution protocol

### Pilot

Run all 12 conditions with vLLM, seed `0`, one adaptation epoch, the first five adaptation tasks, and the first five held-out tasks:

```bash
python src/run_experiment.py --config src/configs/main_experiment.yaml --pilot --model-workers 8
```

The pilot must validate provider startup, matrix expansion, memory parity, reset/freeze behavior, hard budgets, output generation, checkpoint resume, and metric recomputation.

### Primary matrix

Use local vLLM with `/shared/models/hf/Qwen3.5-35B-A3B` and seeds `0`, `1`, and `2`. Every condition processes all 147 adaptation tasks for three epochs and then the same 37 held-out tasks.

In `none`, no state survives between tasks; its repeated adaptation passes form the non-learning curve. In flat/tree, only persistent memory survives. Candidate code, reflections, model messages, and tool history reset for every task and epoch.

Useful scoped invocations are:

```bash
python src/run_experiment.py --only dsl=triton --only workflow=fixed --only memory=tree
python src/run_experiment.py --only dsl=tilelang --only workflow=langchain --model-workers 16
python src/run_experiment.py --only seed=0 --resume
python src/analyze_experiment.py --root outputs/main_experiment
```

## Metrics and planned comparisons

The primary outcome is held-out functional correctness within budget. Secondary outcomes are call success, correctness coverage, normalized speedup, fastest-correct latency, attempts to first correct result, anytime success, tokens, model calls, evaluator calls, and wall time.

Planned contrasts are:

- tree versus flat, flat versus none, and tree versus none within each DSL/workflow;
- memory-gain interaction between Triton and TileLang;
- memory-gain interaction between fixed and LangChain.

Analyze paired filenames with paired-bootstrap 95% confidence intervals and McNemar tests for correctness. Report correctness coverage before conditional speedup. Never compare raw Triton and TileLang latencies; compare normalized speedup against same-DSL, same-hardware references.

For Triton, report fixed automatic retrieval versus LangChain tool retrieval: call rate, selected examples, and downstream correctness/performance. Separate provider, parsing, compilation/launch, runtime, wrong-output, timeout, reference, and performance-evaluation failures.

## Verification and acceptance

Before the pilot:

1. Test OpenAI/vLLM controller selection, normalized arguments, usage/error accounting, LangChain client construction, startup failures, and secret redaction.
2. Confirm dry-run expands to 36 unique primary run IDs and 12 unique pilot run IDs.
3. Validate the exact 184-file pairing and 147/37 split.
4. Verify flat/tree item-ID and content parity, local embedding caching, query-aware retrieval, pruning, serialization, and frozen mutation rejection.
5. Use fake model/evaluator implementations to exercise every condition's tool set, hard budgets, fastest-correct selection, task-state reset, and adaptation-only memory updates.
6. Recompute aggregate metrics from JSONL logs and verify checkpoint resume.
7. Run one real Triton and one real TileLang canary through each workflow before launching the full pilot.

Acceptance requires no direct provider construction in workflows, no OpenAI credential or endpoint dependency for a vLLM-only run, no held-out memory mutation, no shared performance-helper modification, reconstructable metrics, and resumable deterministic execution.

## Follow-up experiments

After the main contrasts are complete:

1. Cross-DSL memory transfer and joint memory.
2. Tree routing, scoring, pruning, and update-component ablations.
3. Full-matrix replication with an OpenAI model and/or another local model.
4. Qualitative memory interventions and path-level case studies.

These analyses should reuse the same runner, output schema, paired manifest, and budgets, with separate experiment names and output roots.
