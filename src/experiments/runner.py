from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

from tqdm import tqdm

from .config import (
    ExperimentConfig,
    RunSpec,
    load_split_manifest,
    resolved_config_for_run,
)
from .evaluator import Evaluator, create_dataset
from .memory import create_memory_backend
from .model_controller import ModelController
from .output import RunOutput
from .records import TaskBudget, TaskContext, TaskExecution
from .workflows import RetrieverBundle, create_workflow


def validate_paired_datasets(config: ExperimentConfig, manifest: Dict[str, List[str]]) -> None:
    expected = manifest["adaptation"] + manifest["evaluation"]
    observed = {}
    for dsl in ("triton", "tilelang"):
        instruction_path = config.datasets[dsl].instruction_path
        with open(instruction_path, "r", encoding="utf-8") as handle:
            rows = json.load(handle)
        observed[dsl] = [row["file"] for row in rows]
        if observed[dsl] != expected:
            raise ValueError(f"{dsl} task order does not match the paired split manifest")
    if observed["triton"] != observed["tilelang"]:
        raise ValueError("Triton and TileLang task files are not exactly paired")


def run_spec(
    config: ExperimentConfig,
    spec: RunSpec,
    *,
    resume: bool,
    pilot: bool,
    validate_connection: bool,
) -> None:
    manifest = load_split_manifest(config.split_manifest)
    dataset_config = config.datasets[spec.dsl]
    dataset = create_dataset(spec.dsl, dataset_config)
    by_filename = {state.filename: state for state in dataset.problem_states}
    expected = set(manifest["adaptation"] + manifest["evaluation"])
    if set(by_filename) != expected:
        missing = sorted(expected - set(by_filename))
        extra = sorted(set(by_filename) - expected)
        raise ValueError(f"dataset/manifest mismatch; missing={missing}, extra={extra}")

    model = ModelController(
        config.model,
        seed=spec.seed,
        model_workers=config.parallelism.model_workers,
    )
    model.prepare(for_langchain=spec.workflow == "langchain")
    if validate_connection:
        model.validate_connection()

    output = RunOutput(spec.output_dir, resume=resume)
    resolved_config = resolved_config_for_run(config, spec)
    if resume:
        output.validate_resume_config(resolved_config)
    output.write_resolved_config(resolved_config)
    if not (output.root / "environment.json").exists():
        output.write_environment()
    checkpoint = output.load_checkpoint()
    completed = set(checkpoint.get("completed", [])) | output.completed_task_keys()
    pruned_epochs = set(checkpoint.get("pruned_epochs", []))
    memory_checkpoint = output.root / "memory" / "checkpoint.json"

    if resume and checkpoint.get("model"):
        model.restore_stats(checkpoint["model"])
    if resume and checkpoint.get("model_tasks"):
        model.restore_task_stats(checkpoint["model_tasks"])
    memory = create_memory_backend(
        spec.memory,
        spec.dsl,
        config.memory,
        state_path=str(memory_checkpoint) if resume and memory_checkpoint.exists() else None,
    )
    if not (output.root / "memory" / "initial.json").exists():
        memory.snapshot(str(output.root / "memory" / "initial.json"))

    evaluator = Evaluator(
        dataset=dataset,
        dsl=spec.dsl,
        dataset_config=dataset_config,
        run_root=spec.output_dir,
        reference_cache_root=str(Path(config.output_root) / "_reference_cache"),
    )
    retriever = None
    if spec.dsl in config.retrieval.enabled_dsls:
        retriever = RetrieverBundle(config.retrieval.corpus_path)
    workflow = create_workflow(
        spec.workflow,
        experiment_id=spec.run_id,
        model=model,
        evaluator=evaluator,
        memory=memory,
        memory_top_k=config.memory.top_k,
        retriever=retriever,
    )
    budget = TaskBudget(
        max_model_calls=config.budget.max_model_calls,
        max_candidate_evaluations=config.budget.max_candidate_evaluations,
        max_tokens_per_call=config.budget.max_tokens_per_call,
        task_timeout_seconds=config.budget.task_timeout_seconds,
    )

    adaptation_names = manifest["adaptation"]
    evaluation_names = manifest["evaluation"]
    if pilot:
        adaptation_names = adaptation_names[: config.pilot_adaptation_tasks]
        evaluation_names = evaluation_names[: config.pilot_evaluation_tasks]

    for epoch in range(spec.adaptation_epochs):
        task_names = list(adaptation_names)
        random.Random(spec.seed + epoch).shuffle(task_names)
        epoch_start = output.root / "memory" / f"epoch_{epoch}_start.json"
        if not epoch_start.exists():
            memory.snapshot(str(epoch_start))
        snapshot_source = create_memory_backend(
            spec.memory,
            spec.dsl,
            config.memory,
            state_path=str(epoch_start),
            precompute_embeddings=False,
        )
        memory_view = snapshot_source.snapshot_view()
        entries = []
        for position, filename in enumerate(task_names):
            completion_key = f"adaptation:{epoch}:{filename}"
            order = epoch * len(adaptation_names) + position
            context = TaskContext(
                dsl=spec.dsl,
                workflow=spec.workflow,
                memory=spec.memory,
                phase="adaptation",
                epoch=epoch,
                seed=spec.seed,
                problem_state=by_filename[filename],
            )
            entries.append((completion_key, order, context))

        _execute_and_stage(
            entries,
            completed,
            workflow,
            budget,
            config.parallelism.model_workers,
            memory_view,
            output,
            pruned_epochs,
            model,
        )
        _commit_staged(
            entries,
            completed,
            workflow,
            budget,
            memory,
            memory_checkpoint,
            output,
            pruned_epochs,
            model,
        )
        if epoch not in pruned_epochs:
            memory.prune(config.memory.prune_threshold, config.memory.prune_age_threshold)
            memory.snapshot(str(output.root / "memory" / f"epoch_{epoch}.json"))
            memory.snapshot(str(memory_checkpoint))
            pruned_epochs.add(epoch)
            _save_checkpoint(output, completed, pruned_epochs, model)
        output.rebuild_jsonl()

    memory.freeze()
    memory.snapshot(str(output.root / "memory" / "final_frozen.json"))
    evaluation_entries = []
    evaluation_base = spec.adaptation_epochs * len(adaptation_names)
    for position, filename in enumerate(evaluation_names):
        completion_key = f"evaluation:{filename}"
        context = TaskContext(
            dsl=spec.dsl,
            workflow=spec.workflow,
            memory=spec.memory,
            phase="evaluation",
            epoch=spec.adaptation_epochs,
            seed=spec.seed,
            problem_state=by_filename[filename],
        )
        evaluation_entries.append((completion_key, evaluation_base + position, context))

    _execute_and_stage(
        evaluation_entries,
        completed,
        workflow,
        budget,
        config.parallelism.model_workers,
        memory.snapshot_view(),
        output,
        pruned_epochs,
        model,
    )
    _commit_staged(
        evaluation_entries,
        completed,
        workflow,
        budget,
        memory,
        memory_checkpoint,
        output,
        pruned_epochs,
        model,
    )
    output.rebuild_jsonl()
    output.write_metrics(model.snapshot_stats())


def _execute_and_stage(
    entries: Sequence[Tuple[str, int, TaskContext]],
    completed: Set[str],
    workflow,
    budget: TaskBudget,
    model_workers: int,
    memory_view,
    output: RunOutput,
    pruned_epochs: Set[int],
    model: ModelController,
) -> None:
    order_by_filename = {context.filename: order for _, order, context in entries}
    key_by_filename = {context.filename: key for key, _, context in entries}
    missing_contexts = [
        context
        for completion_key, _, context in entries
        if completion_key not in completed
        and output.load_pending_execution(completion_key) is None
    ]

    def stage(execution: TaskExecution) -> None:
        filename = execution.result.filename
        completion_key = key_by_filename[filename]
        output.write_pending_execution(
            completion_key, execution, order_by_filename[filename]
        )
        _save_checkpoint(output, completed, pruned_epochs, model)

    if missing_contexts:
        workflow.run_batch(
            missing_contexts,
            budget,
            model_workers,
            memory_view=memory_view,
            on_execution=stage,
        )


def _commit_staged(
    entries: Sequence[Tuple[str, int, TaskContext]],
    completed: Set[str],
    workflow,
    budget: TaskBudget,
    memory,
    memory_checkpoint: Path,
    output: RunOutput,
    pruned_epochs: Set[int],
    model: ModelController,
) -> None:
    cheatsheet_keys = {
        completion_key
        for completion_key, _, context in entries
        if completion_key not in completed
        and context.workflow == "fixed"
        and context.phase == "adaptation"
        and context.memory != "none"
    }
    progress = (
        tqdm(
            total=len(cheatsheet_keys),
            desc="Cheatsheet Update",
            unit="task",
            disable=None,
        )
        if cheatsheet_keys
        else None
    )
    try:
        for completion_key, order, _ in entries:
            if completion_key in completed:
                continue
            execution = output.load_pending_execution(completion_key)
            if execution is None:
                raise RuntimeError(
                    f"missing staged task execution for {completion_key}"
                )

            workflow.prepare_memory_update(execution, budget)
            output.write_pending_execution(completion_key, execution, order)
            if (
                execution.update_intent.kind != "none"
                and not memory.has_commit(completion_key)
            ):
                workflow.apply_memory_update(execution)
                memory.mark_commit(completion_key)
                output.write_pending_execution(completion_key, execution, order)
                memory.snapshot(str(memory_checkpoint))

            output.write_task_record(completion_key, execution.result, order)
            output.remove_pending_execution(completion_key)
            completed.add(completion_key)
            _save_checkpoint(output, completed, pruned_epochs, model)
            if progress is not None and completion_key in cheatsheet_keys:
                progress.update(1)
    finally:
        if progress is not None:
            progress.close()


def _save_checkpoint(output, completed, pruned_epochs, model) -> None:
    output.write_checkpoint(
        {
            "version": 2,
            "completed": sorted(completed),
            "memory_commit_cursor": sum(
                key.startswith("adaptation:") for key in completed
            ),
            "pruned_epochs": sorted(pruned_epochs),
            "model": model.snapshot_stats(),
            "model_tasks": model.snapshot_task_stats(),
        }
    )
