import json
import sys
import tempfile
import threading
import time
import unittest
from contextlib import contextmanager
from unittest import mock
from pathlib import Path
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from experiments.config import ModelConfig
from experiments.memory import MemoryBackend, MemoryRead
from experiments.model_controller import ModelController
from experiments.output import RunOutput
from experiments.runner import _commit_staged
from experiments.records import (
    AttemptRecord,
    CandidateResult,
    TaskBudget,
    TaskContext,
    TaskExecution,
    TaskResult,
)
from experiments.workflows import FixedWorkflow, LangChainWorkflow


try:
    import langchain_core  # noqa: F401
except ImportError:
    class _Message:
        def __init__(self, content="", **kwargs):
            self.content = content
            self.tool_calls = kwargs.get("tool_calls", [])

    class _AIMessage(_Message):
        pass

    class _StructuredTool:
        def __init__(self, function):
            self.function = function
            self.name = function.__name__

        @classmethod
        def from_function(cls, function):
            return cls(function)

        def invoke(self, arguments):
            return self.function(**arguments)

    langchain_core = ModuleType("langchain_core")
    messages_module = ModuleType("langchain_core.messages")
    tools_module = ModuleType("langchain_core.tools")
    messages_module.AIMessage = _AIMessage
    messages_module.HumanMessage = _Message
    messages_module.SystemMessage = _Message
    messages_module.ToolMessage = _Message
    tools_module.StructuredTool = _StructuredTool
    sys.modules["langchain_core"] = langchain_core
    sys.modules["langchain_core.messages"] = messages_module
    sys.modules["langchain_core.tools"] = tools_module


class RecordingProgress:
    def __init__(self, records, **kwargs):
        self.record = {
            "desc": kwargs.get("desc"),
            "total": kwargs.get("total"),
            "updates": 0,
        }
        records.append(self.record)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()
        return False

    def update(self, amount=1):
        self.record["updates"] += amount

    def close(self):
        return None


class DelayedProvider:
    def __init__(self):
        self._local = threading.local()
        self._lock = threading.Lock()
        self._active = {"generate": 0, "reflect": 0, "update": 0}
        self.max_active = {"generate": 0, "reflect": 0, "update": 0}

    @property
    def last_usage(self):
        return getattr(self._local, "usage", {})

    def generate(self, messages, **kwargs):
        prompt = messages[-1]["content"]
        if "generate the reflection wrapped" in prompt:
            kind = "reflect"
        elif prompt.startswith("update:"):
            kind = "update"
        else:
            kind = "generate"
        with self._lock:
            self._active[kind] += 1
            self.max_active[kind] = max(self.max_active[kind], self._active[kind])
        try:
            time.sleep(0.025)
            self._local.usage = {"prompt_tokens": 5, "completion_tokens": 3}
            if kind == "reflect":
                return "repair the indexing"
            if kind == "update":
                return json.dumps({"task": prompt.removeprefix("update:")})
            return json.dumps(
                {"thought": "[item-1]", "code": "def kernel():\n    return 1"}
            )
        finally:
            with self._lock:
                self._active[kind] -= 1


class SerialEvaluator:
    def __init__(self, correct=False):
        self.correct = correct
        self.active = 0
        self.max_active = 0
        self.calls = []

    def evaluate_candidate(self, code, context, attempt):
        self.active += 1
        self.max_active = max(self.max_active, self.active)
        try:
            self.calls.append((context.filename, attempt))
            time.sleep(0.003)
            return CandidateResult(
                filename=context.filename,
                code=code,
                pass_call=True,
                pass_correctness=self.correct,
                perf_evaluated=self.correct,
                normalized_speedup=float(attempt) if self.correct else None,
            )
        finally:
            self.active -= 1


class SnapshotMemory(MemoryBackend):
    kind = "flat"

    def read(self, query, top_k):
        return MemoryRead(text="epoch snapshot", item_ids=["snapshot-item"])

    def build_update_prompt(self, question, answer, reflection):
        raise RuntimeError("snapshot mutation")

    def update(self, response):
        raise RuntimeError("snapshot mutation")

    def record_usage(self, *args, **kwargs):
        raise RuntimeError("snapshot mutation")


class TrackingMemory(MemoryBackend):
    kind = "flat"

    def __init__(self):
        self.updates = []
        self.usage = []

    def snapshot_view(self):
        return SnapshotMemory()

    def build_update_prompt(self, question, answer, reflection):
        return f"update:{question}"

    def update(self, response):
        self.updates.append(json.loads(response))

    def record_usage(
        self,
        model_thought,
        current_iter,
        *,
        pass_call=False,
        pass_correctness=False,
    ):
        self.usage.append((model_thought, current_iter, pass_call, pass_correctness))


class ScopedLangChainModel:
    backend = "openai"
    model_id = "fake-langchain"

    def __init__(self):
        self._local = threading.local()
        self._lock = threading.Lock()
        self._stats = {}
        self._active = 0
        self.max_active = 0

    @contextmanager
    def task_scope(self, key):
        previous = getattr(self._local, "key", None)
        self._local.key = key
        try:
            yield self
        finally:
            self._local.key = previous

    def task_stats(self, key):
        with self._lock:
            return dict(
                self._stats.get(
                    key,
                    {
                        "request_count": 0,
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_latency_seconds": 0.0,
                        "error_count": 0,
                    },
                )
            )

    def invoke_langchain(self, messages, tools):
        from langchain_core.messages import AIMessage

        key = self._local.key
        filename = key.rsplit(":", 1)[-1]
        with self._lock:
            self._active += 1
            self.max_active = max(self.max_active, self._active)
        try:
            time.sleep(0.025)
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "read_memory",
                        "args": {"query": filename},
                        "id": f"read-{filename}",
                        "type": "tool_call",
                    },
                    {
                        "name": "evaluate_candidate",
                        "args": {
                            "code": "def kernel():\n    return 1",
                            "filename": filename,
                        },
                        "id": f"eval-{filename}",
                        "type": "tool_call",
                    },
                    {
                        "name": "update_memory",
                        "args": {"ops_json": json.dumps({"task": filename})},
                        "id": f"update-{filename}",
                        "type": "tool_call",
                    },
                ],
            )
        finally:
            with self._lock:
                self._active -= 1
                stats = self._stats.setdefault(
                    key,
                    {
                        "request_count": 0,
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_latency_seconds": 0.0,
                        "error_count": 0,
                    },
                )
                stats["request_count"] += 1
                stats["prompt_tokens"] += 7
                stats["completion_tokens"] += 4


class ParallelWorkflowTests(unittest.TestCase):
    @staticmethod
    def contexts(workflow="fixed", memory="none", phase="evaluation"):
        return [
            TaskContext(
                dsl="tilelang",
                workflow=workflow,
                memory=memory,
                phase=phase,
                epoch=0,
                seed=0,
                problem_state=SimpleNamespace(
                    filename=f"task_{index}.py",
                    instruction=f"kernel {index}",
                    label="",
                    test_code="",
                ),
            )
            for index in range(3)
        ]

    def test_fixed_generation_and_reflection_overlap_but_evaluation_is_serial(self):
        provider = DelayedProvider()
        controller = ModelController(
            ModelConfig(backend="vllm"),
            provider=provider,
            model_workers=3,
        )
        evaluator = SerialEvaluator(correct=False)
        workflow = FixedWorkflow(
            experiment_id="parallel-fixed",
            model=controller,
            evaluator=evaluator,
            memory=MemoryBackend(),
            memory_top_k=20,
        )
        progress_records = []
        with mock.patch(
            "experiments.workflows.tqdm",
            side_effect=lambda **kwargs: RecordingProgress(
                progress_records, **kwargs
            ),
        ):
            executions = workflow.run_batch(
                self.contexts(),
                TaskBudget(3, 2, 8192, 60),
                model_workers=3,
                memory_view=MemoryBackend().snapshot_view(),
            )

        self.assertEqual(
            [
                (record["desc"], record["total"], record["updates"])
                for record in progress_records
            ],
            [
                ("Generate", 3, 3),
                ("Evaluate", 3, 3),
                ("Reflect", 3, 3),
            ],
        )
        self.assertGreaterEqual(provider.max_active["generate"], 2)
        self.assertGreaterEqual(provider.max_active["reflect"], 2)
        self.assertEqual(evaluator.max_active, 1)
        self.assertEqual(
            [execution.result.filename for execution in executions],
            [f"task_{index}.py" for index in range(3)],
        )
        self.assertTrue(all(execution.result.model_calls == 2 for execution in executions))
        self.assertTrue(all(execution.result.evaluator_calls == 1 for execution in executions))
        self.assertTrue(all(execution.result.prompt_tokens == 10 for execution in executions))
        self.assertEqual(controller.snapshot_stats()["max_concurrent_requests"], 3)

    def test_fixed_reflects_after_generation_and_parsing_failures(self):
        class FailureProvider(DelayedProvider):
            def generate(self, messages, **kwargs):
                prompt = messages[-1]["content"]
                if "generate the reflection wrapped" in prompt:
                    return super().generate(messages, **kwargs)
                if "kernel 0" in prompt:
                    raise RuntimeError("generation failed")
                if "kernel 1" in prompt:
                    self._local.usage = {
                        "prompt_tokens": 5,
                        "completion_tokens": 1,
                    }
                    return "{}"
                return super().generate(messages, **kwargs)

        provider = FailureProvider()
        controller = ModelController(
            ModelConfig(backend="vllm"),
            provider=provider,
            model_workers=3,
        )
        evaluator = SerialEvaluator(correct=False)
        workflow = FixedWorkflow(
            experiment_id="fixed-failures",
            model=controller,
            evaluator=evaluator,
            memory=MemoryBackend(),
            memory_top_k=20,
        )

        executions = workflow.run_batch(
            self.contexts(),
            TaskBudget(1, 5, 8192, 60),
            model_workers=3,
            memory_view=MemoryBackend().snapshot_view(),
        )

        self.assertEqual(
            [
                execution.result.best_candidate.error_type
                for execution in executions
            ],
            ["LLM_PROVIDER_FAILURE", "PARSING_FAILURE", None],
        )
        self.assertEqual(evaluator.calls, [("task_2.py", 1)])
        self.assertTrue(
            all(execution.result.model_calls == 2 for execution in executions)
        )
        self.assertGreaterEqual(provider.max_active["reflect"], 2)

    def test_fixed_cheatsheet_curation_is_deferred_and_sequential(self):
        provider = DelayedProvider()
        controller = ModelController(
            ModelConfig(backend="vllm"),
            provider=provider,
            model_workers=3,
        )
        evaluator = SerialEvaluator(correct=True)
        memory = TrackingMemory()
        workflow = FixedWorkflow(
            experiment_id="parallel-fixed-memory",
            model=controller,
            evaluator=evaluator,
            memory=memory,
            memory_top_k=20,
        )
        contexts = self.contexts(memory="flat", phase="adaptation")
        budget = TaskBudget(2, 1, 8192, 60)
        executions = workflow.run_batch(
            contexts,
            budget,
            model_workers=3,
            memory_view=memory.snapshot_view(),
        )

        self.assertEqual(memory.updates, [])
        for execution in executions:
            workflow.prepare_memory_update(execution, budget)
            workflow.apply_memory_update(execution)

        self.assertEqual(provider.max_active["update"], 1)
        self.assertEqual(
            [update["task"] for update in memory.updates],
            [context.instruction for context in contexts],
        )
        self.assertEqual(len(memory.usage), 3)
        self.assertTrue(all(execution.result.model_calls == 3 for execution in executions))

    def test_cheatsheet_update_progress_tracks_ordered_commit(self):
        provider = DelayedProvider()
        controller = ModelController(
            ModelConfig(backend="vllm"),
            provider=provider,
            model_workers=3,
        )
        evaluator = SerialEvaluator(correct=True)
        memory = TrackingMemory()
        workflow = FixedWorkflow(
            experiment_id="fixed-commit-progress",
            model=controller,
            evaluator=evaluator,
            memory=memory,
            memory_top_k=20,
        )
        contexts = self.contexts(memory="flat", phase="adaptation")
        budget = TaskBudget(1, 5, 8192, 60)
        executions = workflow.run_batch(
            contexts,
            budget,
            model_workers=3,
            memory_view=memory.snapshot_view(),
        )

        with tempfile.TemporaryDirectory() as tmp:
            output = RunOutput(tmp, resume=True)
            entries = []
            for order, (context, execution) in enumerate(
                zip(contexts, executions)
            ):
                completion_key = f"adaptation:0:{context.filename}"
                entries.append((completion_key, order, context))
                output.write_pending_execution(
                    completion_key, execution, order
                )

            progress_records = []
            completed = set()
            with mock.patch(
                "experiments.runner.tqdm",
                side_effect=lambda **kwargs: RecordingProgress(
                    progress_records, **kwargs
                ),
            ):
                _commit_staged(
                    entries,
                    completed,
                    workflow,
                    budget,
                    memory,
                    Path(tmp) / "memory" / "checkpoint.json",
                    output,
                    set(),
                    controller,
                )

        self.assertEqual(
            [
                (record["desc"], record["total"], record["updates"])
                for record in progress_records
            ],
            [("Cheatsheet Update", 3, 3)],
        )
        self.assertEqual(
            [update["task"] for update in memory.updates],
            [context.instruction for context in contexts],
        )
        self.assertEqual(
            completed,
            {f"adaptation:0:{context.filename}" for context in contexts},
        )

    def test_langchain_turns_overlap_and_memory_updates_are_staged_then_ordered(self):
        model = ScopedLangChainModel()
        evaluator = SerialEvaluator(correct=True)
        memory = TrackingMemory()
        workflow = LangChainWorkflow(
            experiment_id="parallel-langchain",
            model=model,
            evaluator=evaluator,
            memory=memory,
            memory_top_k=20,
        )
        contexts = self.contexts(
            workflow="langchain", memory="flat", phase="adaptation"
        )
        executions = workflow.run_batch(
            contexts,
            TaskBudget(1, 1, 8192, 60),
            model_workers=3,
            memory_view=memory.snapshot_view(),
        )

        self.assertGreaterEqual(model.max_active, 2)
        self.assertEqual(evaluator.max_active, 1)
        self.assertEqual(memory.updates, [])
        self.assertTrue(
            all(execution.update_intent.staged_operations for execution in executions)
        )
        self.assertTrue(
            all(
                any(
                    call.get("name") == "update_memory"
                    and call.get("status") == "staged"
                    for call in execution.result.tool_calls
                )
                for execution in executions
            )
        )

        for execution in executions:
            workflow.apply_memory_update(execution)

        self.assertEqual(
            [update["task"] for update in memory.updates],
            [context.filename for context in contexts],
        )
        self.assertEqual(len(memory.usage), 3)

    def test_canonical_output_is_deterministic_and_pending_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = RunOutput(tmp, resume=True)
            results = [
                TaskResult(
                    filename=f"task_{index}.py",
                    phase="evaluation",
                    epoch=1,
                    model_calls=1,
                    evaluator_calls=1,
                    prompt_tokens=2,
                    completion_tokens=1,
                    attempts=[
                        AttemptRecord(
                            experiment_id="parallel-output",
                            phase="evaluation",
                            epoch=1,
                            seed=0,
                            dsl="tilelang",
                            workflow="fixed",
                            memory="none",
                            provider="vllm",
                            model_id="fake",
                            filename=f"task_{index}.py",
                            attempt=1,
                            model_calls=1,
                            evaluator_calls=1,
                            prompt_tokens=2,
                            completion_tokens=1,
                        )
                    ],
                    best_candidate=CandidateResult(
                        filename=f"task_{index}.py",
                        code=f"code-{index}",
                    ),
                )
                for index in range(3)
            ]
            for index in reversed(range(3)):
                output.write_task_record(f"evaluation:task_{index}.py", results[index], index)
            pending = TaskExecution(result=results[0])
            output.write_pending_execution("pending:task_0.py", pending, 10)
            restored = output.load_pending_execution("pending:task_0.py")
            self.assertEqual(restored.result.best_candidate.code, "code-0")
            self.assertEqual(len(restored.result.attempts), 1)
            self.assertEqual(restored.result.attempts[0].filename, "task_0.py")

            output.rebuild_jsonl()
            rows = [
                json.loads(line)
                for line in (Path(tmp) / "task_results.jsonl").read_text().splitlines()
            ]
            attempts = [
                json.loads(line)
                for line in (Path(tmp) / "attempts.jsonl").read_text().splitlines()
            ]
            self.assertEqual(len(attempts), 3)
            self.assertEqual(
                [row["filename"] for row in rows],
                [f"task_{index}.py" for index in range(3)],
            )
            self.assertEqual(
                output.completed_task_keys(),
                {f"evaluation:task_{index}.py" for index in range(3)},
            )


if __name__ == "__main__":
    unittest.main()
