from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import nullcontext
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from prompts import prompt_for_reflection
from utils.utils import extract_function_signatures
from tqdm import tqdm

from .code_utils import parse_model_response
from .memory import MemoryBackend, MemoryRead
from .records import (
    AttemptRecord,
    CandidateResult,
    MemoryUpdateIntent,
    MemoryUsageEvent,
    TaskBudget,
    TaskContext,
    TaskExecution,
    TaskResult,
)


ProgressCallback = Optional[Callable[[TaskExecution], None]]


def choose_best_candidate(candidates: List[CandidateResult]) -> Optional[CandidateResult]:
    correct = [candidate for candidate in candidates if candidate.pass_correctness]
    if correct:
        return max(
            correct,
            key=lambda candidate: (
                candidate.normalized_speedup is not None,
                candidate.normalized_speedup or float("-inf"),
            ),
        )
    evaluated = [
        candidate
        for candidate in candidates
        if candidate.error_type not in {"LLM_PROVIDER_FAILURE", "PARSING_FAILURE"}
    ]
    return evaluated[-1] if evaluated else (candidates[-1] if candidates else None)


def tool_names_for_condition(dsl: str, memory: str, phase: str) -> List[str]:
    names = ["evaluate_candidate"]
    if memory != "none":
        names.append("read_memory")
        if phase == "adaptation":
            names.append("update_memory")
    if dsl == "triton":
        names.append("retrieve_examples")
    return names


def describe_retrieved_example(example: Dict[str, Any], mode: str) -> Dict[str, Any]:
    code = str(example.get("code", ""))
    return {
        "mode": mode,
        "score": float(example.get("similarity score", 0.0)),
        "instruction": example.get("original instruction", ""),
        "code_hash": sha256(code.encode("utf-8")).hexdigest(),
    }


def task_key(context: TaskContext) -> str:
    return f"{context.phase}:{context.epoch}:{context.filename}"


class RetrieverBundle:
    def __init__(self, corpus_path: str):
        from retrievers.retriever import BM25Retriever

        self.instruction = BM25Retriever(mode="instruction")
        self.code = BM25Retriever(mode="code")
        self.instruction.process(corpus_path)
        self.code.process(corpus_path)

    def query(self, text: str, mode: str = "instruction") -> Dict[str, Any]:
        retriever = self.instruction if mode == "instruction" else self.code
        return retriever.query(text, top_k=1)[0]


class Workflow:
    def run_task(self, context: TaskContext, budget: TaskBudget) -> TaskResult:
        raise NotImplementedError

    def run_batch(
        self,
        contexts: Sequence[TaskContext],
        budget: TaskBudget,
        model_workers: int,
        *,
        memory_view: Optional[MemoryBackend] = None,
        on_execution: ProgressCallback = None,
    ) -> List[TaskExecution]:
        raise NotImplementedError


@dataclass
class _TaskState:
    context: TaskContext
    started_at: float
    usage_start: Dict[str, Any]
    usage_cursor: Dict[str, Any]
    attempts: List[AttemptRecord] = field(default_factory=list)
    candidates: List[CandidateResult] = field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    usage_events: List[MemoryUsageEvent] = field(default_factory=list)
    model_calls: int = 0
    evaluator_calls: int = 0
    active: bool = True
    last_memory_read: Optional[MemoryRead] = None


class BaseWorkflow(Workflow):
    def __init__(
        self,
        *,
        experiment_id: str,
        model,
        evaluator,
        memory: MemoryBackend,
        memory_top_k: int,
        retriever: Optional[RetrieverBundle] = None,
    ):
        self.experiment_id = experiment_id
        self.model = model
        self.evaluator = evaluator
        self.memory = memory
        self.memory_top_k = memory_top_k
        self.retriever = retriever

    def run_task(self, context: TaskContext, budget: TaskBudget) -> TaskResult:
        execution = self.run_batch(
            [context],
            budget,
            model_workers=1,
            memory_view=self.memory.snapshot_view(),
        )[0]
        self.prepare_memory_update(execution, budget)
        self.apply_memory_update(execution)
        return execution.result

    def _task_stats(self, key: str) -> Dict[str, Any]:
        if hasattr(self.model, "task_stats"):
            return self.model.task_stats(key)
        if hasattr(self.model, "snapshot_stats"):
            return self.model.snapshot_stats()
        return {
            "request_count": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_latency_seconds": 0.0,
            "error_count": 0,
        }

    def _task_scope(self, key: str):
        if hasattr(self.model, "task_scope"):
            return self.model.task_scope(key)
        return nullcontext(self.model)

    def _new_state(self, context: TaskContext, state_type=_TaskState):
        stats = self._task_stats(task_key(context))
        return state_type(
            context=context,
            started_at=time.monotonic(),
            usage_start=dict(stats),
            usage_cursor=dict(stats),
        )

    def _attempt_record(
        self,
        state: _TaskState,
        candidate: CandidateResult,
        *,
        examples=None,
        example_scores=None,
        memory_read=None,
    ) -> AttemptRecord:
        usage = self._task_stats(task_key(state.context))
        prompt_tokens = usage.get("prompt_tokens", 0) - state.usage_cursor.get(
            "prompt_tokens", 0
        )
        completion_tokens = usage.get(
            "completion_tokens", 0
        ) - state.usage_cursor.get("completion_tokens", 0)
        state.usage_cursor = dict(usage)
        context = state.context
        return AttemptRecord(
            experiment_id=self.experiment_id,
            phase=context.phase,
            epoch=context.epoch,
            seed=context.seed,
            dsl=context.dsl,
            workflow=context.workflow,
            memory=context.memory,
            provider=self.model.backend,
            model_id=self.model.model_id,
            filename=context.filename,
            attempt=len(state.attempts) + 1,
            model_calls=state.model_calls,
            evaluator_calls=state.evaluator_calls,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            retrieved_examples=list(examples or []),
            retrieved_example_scores=list(example_scores or []),
            retrieved_item_ids=list(memory_read.item_ids if memory_read else []),
            retrieved_tree_paths=list(memory_read.tree_paths if memory_read else []),
            memory_prompt_chars=len(memory_read.text) if memory_read else 0,
            candidate=candidate,
        )

    def _flush_usage(self, state: _TaskState) -> Dict[str, Any]:
        usage = self._task_stats(task_key(state.context))
        if state.attempts:
            state.attempts[-1].prompt_tokens += usage.get(
                "prompt_tokens", 0
            ) - state.usage_cursor.get("prompt_tokens", 0)
            state.attempts[-1].completion_tokens += usage.get(
                "completion_tokens", 0
            ) - state.usage_cursor.get("completion_tokens", 0)
            state.usage_cursor = dict(usage)
        return usage

    @staticmethod
    def _collect_jobs(
        executor: ThreadPoolExecutor,
        jobs: Sequence[Callable[[], Any]],
        progress=None,
    ):
        futures = {
            executor.submit(job): index for index, job in enumerate(jobs)
        }
        results = [None] * len(jobs)
        for future in as_completed(futures):
            index = futures[future]
            try:
                results[index] = (True, future.result())
            except BaseException as exc:
                results[index] = (False, exc)
            if progress is not None:
                progress.update(1)
        return results

    def _generate(self, key: str, messages, **kwargs):
        with self._task_scope(key):
            return self.model.generate(messages, **kwargs)

    def _invoke_langchain(self, key: str, messages, tools):
        with self._task_scope(key):
            return self.model.invoke_langchain(messages, tools)

    @staticmethod
    def _function_signatures(context: TaskContext) -> List[str]:
        if not context.problem_state.label:
            return []
        if context.dsl == "tilelang":
            return extract_function_signatures(
                context.problem_state.label,
                mode="tilelang",
                test_code=context.problem_state.test_code,
            )
        return extract_function_signatures(context.problem_state.label)

    def _finish_result(self, state: _TaskState) -> TaskResult:
        usage = self._flush_usage(state)
        return TaskResult(
            filename=state.context.filename,
            phase=state.context.phase,
            epoch=state.context.epoch,
            model_calls=state.model_calls,
            evaluator_calls=state.evaluator_calls,
            prompt_tokens=usage.get("prompt_tokens", 0)
            - state.usage_start.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0)
            - state.usage_start.get("completion_tokens", 0),
            attempts=state.attempts,
            best_candidate=choose_best_candidate(state.candidates),
            tool_calls=state.tool_calls,
            wall_time_seconds=time.monotonic() - state.started_at,
        )

    def prepare_memory_update(
        self, execution: TaskExecution, budget: TaskBudget
    ) -> TaskExecution:
        intent = execution.update_intent
        if intent.kind != "fixed" or intent.prepared:
            return execution
        intent.prepared = True
        if not intent.answer:
            return execution

        before = self._task_stats(intent.task_key)
        execution.result.model_calls += 1
        try:
            prompt = self.memory.build_update_prompt(
                intent.question, intent.answer, intent.reflection
            )
            intent.prepared_operation = self._generate(
                intent.task_key,
                [{"role": "user", "content": prompt}],
                max_tokens=budget.max_tokens_per_call,
            )
            execution.result.tool_calls.append(
                {"name": "update_memory", "status": "prepared"}
            )
        except Exception as exc:
            execution.result.tool_calls.append(
                {"name": "update_memory", "status": "error", "error": str(exc)}
            )
        after = self._task_stats(intent.task_key)
        prompt_delta = after.get("prompt_tokens", 0) - before.get("prompt_tokens", 0)
        completion_delta = after.get("completion_tokens", 0) - before.get(
            "completion_tokens", 0
        )
        execution.result.prompt_tokens += prompt_delta
        execution.result.completion_tokens += completion_delta
        if execution.result.attempts:
            execution.result.attempts[-1].prompt_tokens += prompt_delta
            execution.result.attempts[-1].completion_tokens += completion_delta
        return execution

    def apply_memory_update(self, execution: TaskExecution) -> TaskExecution:
        intent = execution.update_intent
        if intent.kind == "none":
            return execution
        for event in intent.usage_events:
            try:
                self.memory.record_usage(
                    event.model_thought,
                    event.current_iter,
                    pass_call=event.pass_call,
                    pass_correctness=event.pass_correctness,
                )
            except Exception as exc:
                execution.result.tool_calls.append(
                    {"name": "record_memory_usage", "status": "error", "error": str(exc)}
                )

        operations = list(intent.staged_operations)
        if intent.prepared_operation:
            operations.append(intent.prepared_operation)
        for index, operation in enumerate(operations):
            try:
                self.memory.update(operation)
                execution.result.tool_calls.append(
                    {"name": "update_memory", "status": "applied", "staged_order": index}
                )
            except Exception as exc:
                execution.result.tool_calls.append(
                    {
                        "name": "update_memory",
                        "status": "error",
                        "staged_order": index,
                        "error": str(exc),
                    }
                )
        return execution


@dataclass
class _FixedState(_TaskState):
    reflection: str = ""
    last_thought: str = ""
    pending_memory_read: Optional[MemoryRead] = None
    pending_example: Optional[Dict[str, Any]] = None
    pending_mode: str = "instruction"
    pending_code: str = ""


class FixedWorkflow(BaseWorkflow):
    def run_batch(
        self,
        contexts: Sequence[TaskContext],
        budget: TaskBudget,
        model_workers: int,
        *,
        memory_view: Optional[MemoryBackend] = None,
        on_execution: ProgressCallback = None,
    ) -> List[TaskExecution]:
        if model_workers < 1:
            raise ValueError("model_workers must be at least 1")
        read_memory = memory_view or self.memory.snapshot_view()
        states = [self._new_state(context, _FixedState) for context in contexts]
        self._run_window(states, budget, model_workers, read_memory)

        executions: List[TaskExecution] = []
        for state in states:
            result = self._finish_result(state)
            best = result.best_candidate
            intent = MemoryUpdateIntent(
                kind=(
                    "fixed"
                    if state.context.phase == "adaptation"
                    and state.context.memory != "none"
                    else "none"
                ),
                task_key=task_key(state.context),
                usage_events=state.usage_events,
                question=state.context.instruction,
                answer=best.code if best else "",
                reflection=state.reflection,
            )
            execution = TaskExecution(result=result, update_intent=intent)
            executions.append(execution)
            if on_execution:
                on_execution(execution)
        return executions

    def _run_window(
        self,
        states: List[_FixedState],
        budget: TaskBudget,
        model_workers: int,
        read_memory: MemoryBackend,
    ) -> None:
        with ThreadPoolExecutor(max_workers=model_workers) as executor:
            generation_states: List[_FixedState] = []
            generation_jobs = []
            for state in states:
                if (
                    time.monotonic() - state.started_at
                    >= budget.task_timeout_seconds
                ):
                    state.active = False
                    continue

                memory_read = read_memory.read(
                    state.context.instruction, self.memory_top_k
                )
                state.pending_memory_read = memory_read
                state.last_memory_read = memory_read
                if memory_read.text:
                    state.tool_calls.append(
                        {
                            "name": "read_memory",
                            "item_ids": memory_read.item_ids,
                            "tree_paths": memory_read.tree_paths,
                        }
                    )

                example = None
                mode = "instruction"
                if state.context.dsl == "triton" and self.retriever is not None:
                    example = self.retriever.query(
                        state.context.instruction,
                        mode=mode,
                    )
                    state.tool_calls.append(
                        {
                            "name": "retrieve_examples",
                            "mode": mode,
                            "score": float(example["similarity score"]),
                            "code_hash": sha256(
                                str(example["code"]).encode("utf-8")
                            ).hexdigest(),
                        }
                    )
                state.pending_example = example
                state.pending_mode = mode
                prompt = self._build_generation_prompt(
                    context=state.context,
                    signatures=self._function_signatures(state.context),
                    memory_text=memory_read.text,
                    example_code=example["code"] if example else "",
                )
                state.model_calls += 1
                key = task_key(state.context)
                generation_states.append(state)
                generation_jobs.append(
                    lambda key=key, prompt=prompt: self._generate(
                        key,
                        [{"role": "user", "content": prompt}],
                        max_tokens=budget.max_tokens_per_call,
                    )
                )

            with tqdm(
                total=len(generation_jobs),
                desc="Generate",
                unit="task",
                disable=None,
            ) as progress:
                responses = self._collect_jobs(
                    executor, generation_jobs, progress=progress
                )

            for state, (succeeded, value) in zip(generation_states, responses):
                example = state.pending_example
                mode = state.pending_mode
                described = (
                    [describe_retrieved_example(example, mode)] if example else []
                )
                scores = [float(example["similarity score"])] if example else []
                if not succeeded:
                    candidate = CandidateResult(
                        filename=state.context.filename,
                        code="",
                        call_error=str(value),
                        error_type="LLM_PROVIDER_FAILURE",
                    )
                    state.candidates.append(candidate)
                    state.attempts.append(
                        self._attempt_record(
                            state,
                            candidate,
                            examples=described,
                            example_scores=scores,
                            memory_read=state.pending_memory_read,
                        )
                    )
                    continue

                state.last_thought, code = parse_model_response(
                    value, state.context.dsl
                )
                if not code.strip():
                    candidate = CandidateResult(
                        filename=state.context.filename,
                        code="",
                        error_type="PARSING_FAILURE",
                    )
                    state.candidates.append(candidate)
                    state.attempts.append(
                        self._attempt_record(
                            state,
                            candidate,
                            examples=described,
                            example_scores=scores,
                            memory_read=state.pending_memory_read,
                        )
                    )
                    continue
                state.pending_code = code

            # Deliberately coordinator-only: correctness and performance
            # evaluation never overlap on the benchmark GPU.
            with tqdm(
                total=len(states),
                desc="Evaluate",
                unit="task",
                disable=None,
            ) as progress:
                for state in states:
                    if state.pending_code:
                        state.evaluator_calls += 1
                        try:
                            candidate = self.evaluator.evaluate_candidate(
                                state.pending_code,
                                state.context,
                                state.evaluator_calls,
                            )
                        except Exception as exc:
                            candidate = CandidateResult(
                                filename=state.context.filename,
                                code=state.pending_code,
                                call_error=str(exc),
                                error_type="EVALUATOR_FAILURE",
                            )
                        state.candidates.append(candidate)
                        state.tool_calls.append(
                            {
                                "name": "evaluate_candidate",
                                "code_hash": candidate.code_hash,
                                "pass_correctness": candidate.pass_correctness,
                                "normalized_speedup": candidate.normalized_speedup,
                            }
                        )
                        example = state.pending_example
                        mode = state.pending_mode
                        state.attempts.append(
                            self._attempt_record(
                                state,
                                candidate,
                                examples=(
                                    [describe_retrieved_example(example, mode)]
                                    if example
                                    else []
                                ),
                                example_scores=(
                                    [float(example["similarity score"])]
                                    if example
                                    else []
                                ),
                                memory_read=state.pending_memory_read,
                            )
                        )

                    candidate = state.candidates[-1] if state.candidates else None
                    if (
                        candidate is not None
                        and state.context.phase == "adaptation"
                        and state.context.memory != "none"
                    ):
                        state.usage_events.append(
                            MemoryUsageEvent(
                                model_thought=state.last_thought,
                                current_iter=state.context.epoch,
                                pass_call=candidate.pass_call,
                                pass_correctness=candidate.pass_correctness,
                            )
                        )
                    progress.update(1)

            reflection_states: List[_FixedState] = []
            reflection_jobs = []
            for state in states:
                if (
                    time.monotonic() - state.started_at
                    >= budget.task_timeout_seconds
                ):
                    continue
                reflect_prompt = self._build_reflection_prompt(state)
                state.model_calls += 1
                key = task_key(state.context)
                reflection_states.append(state)
                reflection_jobs.append(
                    lambda key=key, prompt=reflect_prompt: self._generate(
                        key,
                        [{"role": "user", "content": prompt}],
                        max_tokens=min(2048, budget.max_tokens_per_call),
                    )
                )

            with tqdm(
                total=len(reflection_jobs),
                desc="Reflect",
                unit="task",
                disable=None,
            ) as progress:
                reflections = self._collect_jobs(
                    executor, reflection_jobs, progress=progress
                )
            for state, (succeeded, value) in zip(
                reflection_states, reflections
            ):
                if succeeded:
                    state.reflection = value
                else:
                    state.tool_calls.append(
                        {"name": "reflect", "status": "error", "error": str(value)}
                    )

    @staticmethod
    def _build_reflection_prompt(state: _FixedState) -> str:
        candidate = state.candidates[-1] if state.candidates else None
        if candidate is not None and candidate.pass_correctness:
            return prompt_for_reflection.prompt_ga.format(
                problem=state.context.instruction,
                code=state.pending_code,
                latency=(
                    candidate.latency_ms
                    if candidate.latency_ms is not None
                    else ""
                ),
                efficiency=(
                    candidate.efficiency
                    if candidate.efficiency is not None
                    else ""
                ),
            )
        if candidate is not None and candidate.pass_call:
            return prompt_for_reflection.prompt_exe.format(
                problem=state.context.instruction,
                solution=state.pending_code,
                call_test_result="succeed",
                exe_test_result=(
                    candidate.correctness_error
                    or candidate.error_type
                    or "correctness test failed"
                ),
            )
        return prompt_for_reflection.prompt.format(
            problem=state.context.instruction,
            solution=state.pending_code,
            test_result=(
                candidate.call_error
                if candidate is not None and candidate.call_error
                else (
                    candidate.error_type
                    if candidate is not None and candidate.error_type
                    else "no executable code was generated"
                )
            ),
        )

    @staticmethod
    def _build_generation_prompt(
        *,
        context: TaskContext,
        signatures: List[str],
        memory_text: str,
        example_code: str,
    ) -> str:
        parts = [
            f"Implement and optimize this task in {context.dsl}:\n{context.instruction}",
            "Required public signatures:\n" + "\n".join(f"- {sig}" for sig in signatures),
        ]
        if memory_text:
            parts.append("Persistent memory:\n" + memory_text)
        if example_code:
            parts.append("Retrieved example:\n" + example_code)
        parts.append(
            'Return only JSON with the shape {"thought":"[memory IDs used]","code":"complete code"}.'
        )
        return "\n\n".join(parts)


@dataclass
class _LangChainState(_TaskState):
    messages: List[Any] = field(default_factory=list)
    tools: List[Any] = field(default_factory=list)
    tools_by_name: Dict[str, Any] = field(default_factory=dict)
    retrieved_examples: List[Dict[str, Any]] = field(default_factory=list)
    staged_operations: List[str] = field(default_factory=list)


class LangChainWorkflow(BaseWorkflow):
    def run_batch(
        self,
        contexts: Sequence[TaskContext],
        budget: TaskBudget,
        model_workers: int,
        *,
        memory_view: Optional[MemoryBackend] = None,
        on_execution: ProgressCallback = None,
    ) -> List[TaskExecution]:
        if model_workers < 1:
            raise ValueError("model_workers must be at least 1")
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
        except ImportError as exc:
            raise RuntimeError("langchain-core is required for the LangChain workflow") from exc

        read_memory = memory_view or self.memory.snapshot_view()
        executions: List[TaskExecution] = []
        for offset in range(0, len(contexts), model_workers):
            window_contexts = contexts[offset : offset + model_workers]
            states: List[_LangChainState] = []
            for context in window_contexts:
                state = self._new_state(context, _LangChainState)
                signatures = self._function_signatures(context)
                state.messages = [
                    SystemMessage(
                        content=(
                            f"You are an autonomous {context.dsl} kernel optimization agent. "
                            "Use available tools to retrieve context, evaluate candidates, and "
                            "improve performance. Never exceed the provided tool budgets. Finish "
                            "with JSON containing thought and complete code."
                        )
                    ),
                    HumanMessage(
                        content=(
                            f"Task:\n{context.instruction}\n\nRequired public signatures:\n"
                            + "\n".join(f"- {signature}" for signature in signatures)
                            + f"\n\nFilename: {context.filename}"
                        )
                    ),
                ]
                state.tools, state.tools_by_name = self._make_tools(
                    state, budget, read_memory
                )
                states.append(state)
            self._run_langchain_window(states, budget, model_workers)
            for state in states:
                result = self._finish_result(state)
                intent = MemoryUpdateIntent(
                    kind=(
                        "langchain"
                        if state.context.phase == "adaptation"
                        and state.context.memory != "none"
                        else "none"
                    ),
                    task_key=task_key(state.context),
                    usage_events=state.usage_events,
                    staged_operations=state.staged_operations,
                    prepared=True,
                )
                execution = TaskExecution(result=result, update_intent=intent)
                executions.append(execution)
                if on_execution:
                    on_execution(execution)
        return executions

    def _run_langchain_window(
        self,
        states: List[_LangChainState],
        budget: TaskBudget,
        model_workers: int,
    ) -> None:
        with ThreadPoolExecutor(max_workers=model_workers) as executor:
            while True:
                active = []
                jobs = []
                for state in states:
                    if not state.active:
                        continue
                    if (
                        state.model_calls >= budget.max_model_calls
                        or time.monotonic() - state.started_at
                        >= budget.task_timeout_seconds
                    ):
                        state.active = False
                        continue
                    state.model_calls += 1
                    key = task_key(state.context)
                    active.append(state)
                    jobs.append(
                        lambda key=key, state=state: self._invoke_langchain(
                            key, state.messages, state.tools
                        )
                    )
                if not active:
                    break

                responses = self._collect_jobs(executor, jobs)
                # Responses and tools are consumed in seeded task order even if
                # provider futures completed in a different order.
                for state, (succeeded, value) in zip(active, responses):
                    if not succeeded:
                        candidate = CandidateResult(
                            filename=state.context.filename,
                            code="",
                            call_error=str(value),
                            error_type="LLM_PROVIDER_FAILURE",
                        )
                        state.candidates.append(candidate)
                        state.attempts.append(self._attempt_record(state, candidate))
                        state.active = False
                        continue

                    response = value
                    state.messages.append(response)
                    calls = getattr(response, "tool_calls", None) or []
                    if calls:
                        self._execute_tools(state, calls)
                        continue

                    content = response.content
                    if isinstance(content, list):
                        content = "\n".join(
                            block.get("text", "") if isinstance(block, dict) else str(block)
                            for block in content
                        )
                    _, code = parse_model_response(content, state.context.dsl)
                    if code.strip() and state.evaluator_calls < budget.max_candidate_evaluations:
                        tool = state.tools_by_name["evaluate_candidate"]
                        tool.invoke({"code": code, "filename": state.context.filename})
                    elif not code.strip():
                        candidate = CandidateResult(
                            filename=state.context.filename,
                            code="",
                            error_type="PARSING_FAILURE",
                        )
                        state.candidates.append(candidate)
                        state.attempts.append(self._attempt_record(state, candidate))
                    state.active = False

    def _execute_tools(self, state: _LangChainState, calls: Sequence[Dict[str, Any]]) -> None:
        from langchain_core.messages import ToolMessage

        for call in calls:
            name = call.get("name", "")
            tool = state.tools_by_name.get(name)
            if tool is None:
                result = json.dumps({"error": f"unknown tool: {name}"})
            else:
                try:
                    # Tool invocation is coordinator-only. In particular,
                    # evaluate_candidate and memory mutation never enter workers.
                    result = tool.invoke(call.get("args", {}))
                except Exception as exc:
                    result = json.dumps({"error": str(exc)})
                    state.tool_calls.append(
                        {"name": name, "status": "error", "error": str(exc)}
                    )
            state.messages.append(
                ToolMessage(content=str(result), tool_call_id=call.get("id", name))
            )

    def _make_tools(
        self,
        state: _LangChainState,
        budget: TaskBudget,
        memory_view: MemoryBackend,
    ) -> Tuple[List[Any], Dict[str, Any]]:
        from langchain_core.tools import StructuredTool

        context = state.context

        def evaluate_candidate(code: str, filename: str = context.filename) -> str:
            """Compile, check correctness, and benchmark one candidate implementation."""
            if state.evaluator_calls >= budget.max_candidate_evaluations:
                return json.dumps({"error": "candidate evaluation budget exhausted"})
            state.evaluator_calls += 1
            try:
                candidate = self.evaluator.evaluate_candidate(
                    code, context, state.evaluator_calls
                )
            except Exception as exc:
                candidate = CandidateResult(
                    filename=context.filename,
                    code=code,
                    call_error=str(exc),
                    error_type="EVALUATOR_FAILURE",
                )
            state.candidates.append(candidate)
            state.attempts.append(
                self._attempt_record(
                    state,
                    candidate,
                    examples=state.retrieved_examples,
                    example_scores=[item["score"] for item in state.retrieved_examples],
                    memory_read=state.last_memory_read,
                )
            )
            if context.phase == "adaptation" and context.memory != "none":
                ids = state.last_memory_read.item_ids if state.last_memory_read else []
                state.usage_events.append(
                    MemoryUsageEvent(
                        model_thought="[" + ", ".join(ids) + "]",
                        current_iter=context.epoch,
                        pass_call=candidate.pass_call,
                        pass_correctness=candidate.pass_correctness,
                    )
                )
            state.tool_calls.append(
                {
                    "name": "evaluate_candidate",
                    "code_hash": candidate.code_hash,
                    "pass_correctness": candidate.pass_correctness,
                    "normalized_speedup": candidate.normalized_speedup,
                }
            )
            return json.dumps(candidate.to_dict(include_code=False))

        def read_memory(query: str) -> str:
            """Retrieve relevant persistent memory for the current task."""
            result = memory_view.read(query, self.memory_top_k)
            state.last_memory_read = result
            state.tool_calls.append(
                {
                    "name": "read_memory",
                    "item_ids": result.item_ids,
                    "tree_paths": result.tree_paths,
                }
            )
            return result.text

        def update_memory(ops_json: str) -> str:
            """Stage JSON memory operations learned from this adaptation task."""
            if not isinstance(ops_json, str):
                ops_json = json.dumps(ops_json)
            try:
                json.loads(ops_json)
            except json.JSONDecodeError as exc:
                state.tool_calls.append(
                    {"name": "update_memory", "status": "error", "error": str(exc)}
                )
                return json.dumps({"error": f"invalid JSON memory operations: {exc}"})
            state.staged_operations.append(ops_json)
            state.tool_calls.append(
                {
                    "name": "update_memory",
                    "status": "staged",
                    "staged_order": len(state.staged_operations) - 1,
                }
            )
            return json.dumps(
                {
                    "status": "staged",
                    "message": "The update will be applied in seeded order and visible next epoch.",
                }
            )

        def retrieve_examples(query: str, mode: str = "instruction") -> str:
            """Retrieve the top Triton example from the shared BM25 corpus."""
            mode = mode if mode in {"instruction", "code"} else "instruction"
            result = self.retriever.query(query, mode=mode)
            state.retrieved_examples.append(describe_retrieved_example(result, mode))
            state.tool_calls.append(
                {
                    "name": "retrieve_examples",
                    "mode": mode,
                    "score": float(result["similarity score"]),
                }
            )
            return json.dumps(result)

        functions = {
            "evaluate_candidate": evaluate_candidate,
            "read_memory": read_memory,
            "update_memory": update_memory,
            "retrieve_examples": retrieve_examples,
        }
        names = tool_names_for_condition(context.dsl, context.memory, context.phase)
        if self.retriever is None and "retrieve_examples" in names:
            names.remove("retrieve_examples")
        tools = [StructuredTool.from_function(functions[name]) for name in names]
        return tools, {tool.name: tool for tool in tools}


def create_workflow(kind: str, **kwargs) -> Workflow:
    if kind == "fixed":
        return FixedWorkflow(**kwargs)
    if kind == "langchain":
        return LangChainWorkflow(**kwargs)
    raise ValueError(f"unsupported workflow: {kind}")
