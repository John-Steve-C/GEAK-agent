import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from experiments.config import (  # noqa: E402
    MemoryConfig,
    ModelConfig,
    expand_run_specs,
    load_experiment_config,
    load_split_manifest,
    resolved_config_for_run,
)
from experiments.analysis import exact_mcnemar_p, paired_bootstrap_ci  # noqa: E402
from experiments.embedding import LocalQwenEmbedder  # noqa: E402
from experiments.memory import create_memory_backend  # noqa: E402
from experiments.model_controller import ModelController  # noqa: E402
from experiments.output import RunOutput  # noqa: E402
from experiments.records import (  # noqa: E402
    AttemptRecord,
    CandidateResult,
    TaskBudget,
    TaskContext,
    TaskResult,
)
from experiments.runner import validate_paired_datasets  # noqa: E402
from experiments.workflows import (  # noqa: E402
    FixedWorkflow,
    choose_best_candidate,
    tool_names_for_condition,
)
from models.OpenAI import OpenAIModel  # noqa: E402


CONFIG_PATH = ROOT / "src/configs/main_experiment.yaml"


class FakeProvider:
    def __init__(self):
        self.last_usage = {}
        self.calls = []

    def generate(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        self.last_usage = {"prompt_tokens": 3, "completion_tokens": 2}
        return "ok"


class FakeEmbedder:
    def __call__(self, text):
        value = sum(ord(character) for character in text)
        return [float(value % 17), float(len(text) % 13), 1.0]


class ExperimentConfigTests(unittest.TestCase):
    def test_primary_and_pilot_matrix_sizes_and_ids(self):
        config = load_experiment_config(str(CONFIG_PATH))
        primary = expand_run_specs(config)
        pilot = expand_run_specs(config, pilot=True)

        self.assertEqual(len(primary), 36)
        self.assertEqual(len({spec.run_id for spec in primary}), 36)
        self.assertEqual(len(pilot), 12)
        self.assertEqual(len({spec.run_id for spec in pilot}), 12)
        self.assertTrue(all("/pilot/" in spec.output_dir for spec in pilot))
        self.assertTrue(all("/pilot/" not in spec.output_dir for spec in primary))

    def test_manifest_matches_both_instruction_files(self):
        config = load_experiment_config(str(CONFIG_PATH))
        manifest = load_split_manifest(config.split_manifest)

        self.assertEqual(len(manifest["adaptation"]), 147)
        self.assertEqual(len(manifest["evaluation"]), 37)
        self.assertFalse(set(manifest["adaptation"]) & set(manifest["evaluation"]))
        validate_paired_datasets(config, manifest)

    def test_resolved_config_contains_no_credential_value(self):
        config = load_experiment_config(str(CONFIG_PATH))
        spec = expand_run_specs(config)[0]
        with mock.patch.dict(os.environ, {"VLLM_API_KEY": "secret-value"}):
            rendered = json.dumps(resolved_config_for_run(config, spec))

        self.assertNotIn("secret-value", rendered)
        self.assertIn("VLLM_API_KEY", rendered)


class ModelControllerTests(unittest.TestCase):
    def test_openai_provider_selects_model_compatible_token_parameter(self):
        response = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))],
            usage=SimpleNamespace(
                prompt_tokens=3,
                completion_tokens=2,
                total_tokens=5,
            ),
        )
        for model_id, expected, omitted in (
            ("gpt-5.6-sol", "max_completion_tokens", "max_tokens"),
            ("gpt-4.1", "max_tokens", "max_completion_tokens"),
        ):
            with self.subTest(model_id=model_id):
                client = SimpleNamespace(
                    chat=SimpleNamespace(
                        completions=SimpleNamespace(
                            create=mock.Mock(return_value=response)
                        )
                    )
                )
                with mock.patch("models.OpenAI.openai.OpenAI", return_value=client):
                    model = OpenAIModel(api_key="token", model_id=model_id)
                self.assertEqual(
                    model.generate(
                        [{"role": "user", "content": "x"}], max_tokens=123
                    ),
                    "ok",
                )
                kwargs = client.chat.completions.create.call_args.kwargs
                self.assertEqual(kwargs[expected], 123)
                self.assertNotIn(omitted, kwargs)

    def test_common_and_vllm_specific_generate_arguments(self):
        provider = FakeProvider()
        config = ModelConfig(backend="vllm", api_key_env="VLLM_API_KEY")
        controller = ModelController(config, seed=7, provider=provider)

        self.assertEqual(controller.generate([{"role": "user", "content": "x"}]), "ok")
        kwargs = provider.calls[0][1]
        self.assertEqual(kwargs["seed"], 7)
        self.assertEqual(kwargs["max_tokens"], 8192)
        self.assertIn("min_p", kwargs)
        self.assertEqual(controller.snapshot_stats()["request_count"], 1)
        self.assertEqual(controller.snapshot_stats()["prompt_tokens"], 3)

    def test_openai_generate_omits_vllm_only_arguments(self):
        provider = FakeProvider()
        config = ModelConfig(backend="openai", api_key_env="OPENAI_API_KEY")
        controller = ModelController(config, seed=2, provider=provider)

        controller.generate([{"role": "user", "content": "x"}])
        kwargs = provider.calls[0][1]
        self.assertEqual(kwargs["seed"], 2)
        self.assertNotIn("min_p", kwargs)
        self.assertNotIn("top_k", kwargs)

    def test_backend_selects_configured_provider_class(self):
        cases = (
            ("vllm", "VLLM_API_KEY", "models.Vllm.VLLMModel"),
            ("openai", "OPENAI_API_KEY", "models.OpenAI.OpenAIModel"),
        )
        for backend, key_name, class_path in cases:
            provider = FakeProvider()
            with mock.patch.dict(os.environ, {key_name: "token"}):
                with mock.patch(class_path, return_value=provider) as constructor:
                    controller = ModelController(
                        ModelConfig(backend=backend, api_key_env=key_name)
                    )
                    controller.generate([{"role": "user", "content": "x"}])
            constructor.assert_called_once()

    def test_missing_credentials_fail_at_startup(self):
        config = ModelConfig(backend="vllm", api_key_env="MISSING_TEST_KEY")
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "MISSING_TEST_KEY"):
                ModelController(config)

    def test_langchain_model_uses_controller_settings(self):
        captured = {}

        class FakeChatOpenAI:
            def __init__(self, **kwargs):
                captured.update(kwargs)

        module = types.ModuleType("langchain_openai")
        module.ChatOpenAI = FakeChatOpenAI
        config = ModelConfig(
            backend="vllm",
            api_key_env="TEST_VLLM_KEY",
            base_url="http://localhost:9999/v1",
        )
        with mock.patch.dict(os.environ, {"TEST_VLLM_KEY": "token"}):
            with mock.patch.dict(sys.modules, {"langchain_openai": module}):
                controller = ModelController(config, seed=11)
                controller.as_langchain_chat_model()

        self.assertEqual(captured["base_url"], config.base_url)
        self.assertEqual(captured["model"], config.model_id)
        self.assertEqual(captured["seed"], 11)
        self.assertEqual(captured["api_key"], "token")
        self.assertIn("extra_body", captured)

    def test_gpt5_langchain_model_uses_max_completion_tokens(self):
        captured = {}

        class FakeChatOpenAI:
            def __init__(self, **kwargs):
                captured.update(kwargs)

        module = types.ModuleType("langchain_openai")
        module.ChatOpenAI = FakeChatOpenAI
        config = ModelConfig(
            backend="openai",
            model_id="gpt-5.6-sol",
            api_key_env="OPENAI_API_KEY",
        )
        with mock.patch.dict(sys.modules, {"langchain_openai": module}):
            controller = ModelController(config, provider=FakeProvider())
            controller.as_langchain_chat_model()

        self.assertEqual(captured["max_completion_tokens"], config.max_tokens)
        self.assertNotIn("max_tokens", captured)


class MemoryBackendTests(unittest.TestCase):
    def _config(self):
        return MemoryConfig(
            initial_files={
                "triton": str(ROOT / "src/new_first_cheatsheet.json"),
                "tilelang": str(ROOT / "src/tilelang_first_cheatsheet.json"),
            }
        )

    def test_flat_and_tree_preserve_same_initial_items(self):
        for dsl in ("triton", "tilelang"):
            flat = create_memory_backend(
                "flat",
                dsl,
                self._config(),
                embedder=FakeEmbedder(),
                precompute_embeddings=False,
            )
            tree = create_memory_backend(
                "tree",
                dsl,
                self._config(),
                embedder=FakeEmbedder(),
                precompute_embeddings=False,
            )
            flat_items = {
                item["id"]: item["content"]
                for section in flat.manager.sections
                for item in flat.manager.data[section]
            }
            tree_items = {
                item_id: item["content"]
                for item_id, item in tree.manager.data["items"].items()
            }
            self.assertEqual(flat_items, tree_items)

    def test_frozen_memory_rejects_updates_and_read_is_immutable(self):
        memory = create_memory_backend(
            "tree",
            "triton",
            self._config(),
            embedder=FakeEmbedder(),
            precompute_embeddings=False,
        )
        memory.freeze()
        before = json.dumps(memory.manager.data, sort_keys=True)
        result = memory.read("matrix multiplication", 3)
        after = json.dumps(memory.manager.data, sort_keys=True)

        self.assertTrue(result.item_ids)
        self.assertEqual(before, after)
        with self.assertRaisesRegex(RuntimeError, "frozen"):
            memory.update("{}")
        with self.assertRaisesRegex(RuntimeError, "frozen"):
            memory.prune(0.5, 2)

    def test_local_embedding_cache_avoids_recomputation(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            first = LocalQwenEmbedder("Qwen/Qwen3-Embedding-0.6B", str(cache_path))
            first_encoder = mock.Mock(return_value=[1.0, 2.0])
            first._encode_uncached = first_encoder
            expected = first("same query")

            second = LocalQwenEmbedder("Qwen/Qwen3-Embedding-0.6B", str(cache_path))
            second_encoder = mock.Mock(side_effect=AssertionError("cache miss"))
            second._encode_uncached = second_encoder
            actual = second("same query")

            self.assertEqual(expected, actual)
            first_encoder.assert_called_once()
            second_encoder.assert_not_called()

    def test_qwen_query_and_document_embeddings_use_separate_cache_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            embedder = LocalQwenEmbedder(
                "Qwen/Qwen3-Embedding-0.6B",
                str(Path(tmp) / "cache.json"),
            )
            encoder = mock.Mock(side_effect=([1.0], [2.0]))
            embedder._encode_uncached = encoder

            document = embedder.embed_document("same text")
            query = embedder.embed_query("same text")

            self.assertEqual(document, [1.0])
            self.assertEqual(query, [2.0])
            self.assertEqual(encoder.call_count, 2)
            self.assertTrue(encoder.call_args_list[1].args[0].startswith("Instruct:"))

    def test_memory_retrieval_dispatches_query_and_document_modes(self):
        class TrackingEmbedder:
            def __init__(self):
                self.query_calls = []
                self.document_calls = []

            def embed_query(self, text):
                self.query_calls.append(text)
                return [1.0, 0.0]

            def embed_document(self, text):
                self.document_calls.append(text)
                return [1.0, 0.0]

        embedder = TrackingEmbedder()
        memory = create_memory_backend(
            "flat",
            "triton",
            self._config(),
            embedder=embedder,
            precompute_embeddings=False,
        )

        memory.read("optimize a reduction", 3)

        self.assertEqual(embedder.query_calls, ["optimize a reduction"])
        self.assertTrue(embedder.document_calls)


class WorkflowTests(unittest.TestCase):
    def test_all_condition_tool_sets(self):
        for dsl in ("triton", "tilelang"):
            for memory in ("none", "flat", "tree"):
                adaptation = tool_names_for_condition(dsl, memory, "adaptation")
                evaluation = tool_names_for_condition(dsl, memory, "evaluation")
                self.assertIn("evaluate_candidate", adaptation)
                self.assertEqual("retrieve_examples" in adaptation, dsl == "triton")
                self.assertEqual("read_memory" in adaptation, memory != "none")
                self.assertEqual("update_memory" in adaptation, memory != "none")
                self.assertNotIn("update_memory", evaluation)

    def test_fastest_correct_candidate_is_selected(self):
        candidates = [
            CandidateResult(filename="x.py", code="a", pass_correctness=True, normalized_speedup=1.2),
            CandidateResult(filename="x.py", code="b", pass_correctness=False),
            CandidateResult(filename="x.py", code="c", pass_correctness=True, normalized_speedup=2.1),
        ]
        self.assertEqual(choose_best_candidate(candidates).code, "c")

    def test_fixed_workflow_uses_one_round_independent_of_langchain_caps(self):
        class FakeModel:
            backend = "vllm"
            model_id = "fake"

            def __init__(self):
                self.calls = 0
                self.prompt_tokens = 0
                self.completion_tokens = 0

            def generate(self, messages, **kwargs):
                self.calls += 1
                self.prompt_tokens += 5
                self.completion_tokens += 3
                return json.dumps({"thought": "", "code": "def kernel():\n    return 1"})

            def snapshot_stats(self):
                return {
                    "request_count": self.calls,
                    "prompt_tokens": self.prompt_tokens,
                    "completion_tokens": self.completion_tokens,
                    "total_latency_seconds": 0.0,
                    "error_count": 0,
                }

        class FakeEvaluator:
            def evaluate_candidate(self, code, task, attempt):
                return CandidateResult(
                    filename=task.filename,
                    code=code,
                    pass_call=True,
                    pass_correctness=True,
                    perf_evaluated=True,
                    latency_ms=10.0 / attempt,
                    reference_latency_ms=10.0,
                    normalized_speedup=float(attempt),
                )

        workflow = FixedWorkflow(
            experiment_id="test",
            model=FakeModel(),
            evaluator=FakeEvaluator(),
            memory=create_memory_backend("none", "tilelang", self._config_for_none()),
            memory_top_k=20,
        )
        context = TaskContext(
            dsl="tilelang",
            workflow="fixed",
            memory="none",
            phase="evaluation",
            epoch=3,
            seed=0,
            problem_state=SimpleNamespace(
                filename="x.py",
                instruction="write a kernel",
                label="",
                test_code="",
            ),
        )
        result = workflow.run_task(
            context,
            TaskBudget(
                max_model_calls=1,
                max_candidate_evaluations=5,
                max_tokens_per_call=8192,
                task_timeout_seconds=60,
            ),
        )

        self.assertEqual(result.model_calls, 2)
        self.assertEqual(result.evaluator_calls, 1)
        self.assertEqual(result.best_candidate.normalized_speedup, 1.0)
        self.assertEqual(len(result.attempts), 1)
        self.assertEqual(result.attempts[0].prompt_tokens, 10)

    @staticmethod
    def _config_for_none():
        return MemoryConfig(initial_files={})


class OutputTests(unittest.TestCase):
    def test_existing_output_requires_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = RunOutput(tmp, resume=True)
            output.write_checkpoint({"completed": ["evaluation:x.py"], "pruned_epochs": []})
            with self.assertRaises(FileExistsError):
                RunOutput(tmp, resume=False)
            resumed = RunOutput(tmp, resume=True)
            self.assertEqual(resumed.load_checkpoint()["completed"], ["evaluation:x.py"])

    def test_metrics_are_recomputed_from_jsonl(self):
        candidate = CandidateResult(
            filename="x.py",
            code="def kernel(): pass",
            pass_call=True,
            pass_correctness=True,
            perf_evaluated=True,
            latency_ms=2.0,
            reference_latency_ms=4.0,
            normalized_speedup=2.0,
        )
        attempt = AttemptRecord(
            experiment_id="test",
            phase="evaluation",
            epoch=3,
            seed=0,
            dsl="triton",
            workflow="fixed",
            memory="tree",
            provider="vllm",
            model_id="fake",
            filename="x.py",
            attempt=1,
            model_calls=1,
            evaluator_calls=1,
            prompt_tokens=5,
            completion_tokens=3,
            candidate=candidate,
        )
        result = TaskResult(
            filename="x.py",
            phase="evaluation",
            epoch=3,
            model_calls=1,
            evaluator_calls=1,
            prompt_tokens=5,
            completion_tokens=3,
            attempts=[attempt],
            best_candidate=candidate,
        )
        with tempfile.TemporaryDirectory() as tmp:
            output = RunOutput(tmp, resume=True)
            output.append_task_result(result)
            output.write_metrics({"request_count": 1})
            metrics = json.loads((Path(tmp) / "metrics.json").read_text(encoding="utf-8"))

        group = metrics["groups"]["evaluation:3"]
        self.assertEqual(group["correctness_rate"], 1.0)
        self.assertEqual(group["mean_normalized_speedup"], 2.0)
        self.assertEqual(group["anytime_success_by_attempt"]["1"], 1.0)


class AnalysisTests(unittest.TestCase):
    def test_filename_clustered_bootstrap_and_exact_mcnemar(self):
        interval = paired_bootstrap_ci(
            [("a.py", 1.0), ("a.py", 1.0), ("b.py", -1.0), ("b.py", -1.0)],
            samples=1000,
            seed=0,
        )

        self.assertEqual(interval["estimate"], 0.0)
        self.assertLessEqual(interval["ci95_low"], 0.0)
        self.assertGreaterEqual(interval["ci95_high"], 0.0)
        self.assertEqual(exact_mcnemar_p(0, 0), 1.0)
        self.assertAlmostEqual(exact_mcnemar_p(3, 0), 0.25)


if __name__ == "__main__":
    unittest.main()
