import io
import sys
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import run_experiment  # noqa: E402
from experiments.config import expand_run_specs, load_experiment_config  # noqa: E402
from experiments.model_controller import ModelController  # noqa: E402


CONFIG_PATH = ROOT / "src/configs/main_experiment.yaml"


class DelayedProvider:
    def __init__(self, delay=0.02):
        self.delay = delay
        self._local = threading.local()
        self._lock = threading.Lock()
        self.active = 0
        self.max_active = 0

    @property
    def last_usage(self):
        return getattr(self._local, "last_usage", {})

    def generate(self, messages, **kwargs):
        with self._lock:
            self.active += 1
            self.max_active = max(self.max_active, self.active)
        try:
            time.sleep(self.delay)
            value = int(messages[0]["content"])
            if value < 0:
                raise RuntimeError("provider failure")
            self._local.last_usage = {
                "prompt_tokens": value + 1,
                "completion_tokens": 1,
            }
            return str(value)
        finally:
            with self._lock:
                self.active -= 1


class ParallelConfigTests(unittest.TestCase):
    def test_yaml_and_run_specs_include_worker_count(self):
        config = load_experiment_config(str(CONFIG_PATH))
        specs = expand_run_specs(config)

        workers = config.parallelism.model_workers

        self.assertGreaterEqual(workers, 1)
        self.assertTrue(all(spec.model_workers == workers for spec in specs))
        self.assertTrue(all(f"workers_{workers}" in spec.run_id for spec in specs))

        config.parallelism.model_workers = 0
        with self.assertRaisesRegex(ValueError, "at least 1"):
            config.validate()

    def test_cli_worker_override_is_applied_before_expansion(self):
        config = load_experiment_config(str(CONFIG_PATH))
        seen = {}

        def expand(config, **kwargs):
            seen["workers"] = config.parallelism.model_workers
            return []

        with mock.patch.object(run_experiment, "load_experiment_config", return_value=config):
            with mock.patch.object(run_experiment, "expand_run_specs", side_effect=expand):
                with mock.patch.object(run_experiment, "load_split_manifest", return_value={}):
                    with mock.patch.object(run_experiment, "validate_paired_datasets"):
                        with redirect_stdout(io.StringIO()):
                            result = run_experiment.main(
                                ["--dry-run", "--model-workers", "16"]
                            )

        self.assertEqual(result, 0)
        self.assertEqual(seen["workers"], 16)


class ParallelModelControllerTests(unittest.TestCase):
    def _controller(self, provider, workers=2):
        config = load_experiment_config(str(CONFIG_PATH)).model
        return ModelController(
            config,
            provider=provider,
            model_workers=workers,
        )

    def test_bounded_parallel_calls_have_exact_global_and_task_usage(self):
        provider = DelayedProvider()
        controller = self._controller(provider, workers=2)

        def call(index):
            with controller.task_scope(f"task-{index % 3}"):
                return controller.generate(
                    [{"role": "user", "content": str(index)}]
                )

        with ThreadPoolExecutor(max_workers=6) as executor:
            results = list(executor.map(call, range(6)))

        self.assertEqual(results, [str(index) for index in range(6)])
        self.assertEqual(provider.max_active, 2)
        global_stats = controller.snapshot_stats()
        self.assertEqual(global_stats["request_count"], 6)
        self.assertEqual(global_stats["prompt_tokens"], 21)
        self.assertEqual(global_stats["completion_tokens"], 6)
        self.assertEqual(global_stats["max_concurrent_requests"], 2)
        self.assertGreater(global_stats["total_queue_wait_seconds"], 0)
        self.assertGreater(global_stats["total_request_latency_seconds"], 0)

        self.assertEqual(controller.task_stats("task-0")["request_count"], 2)
        self.assertEqual(controller.task_stats("task-0")["prompt_tokens"], 5)
        self.assertEqual(controller.task_stats("task-1")["prompt_tokens"], 7)
        self.assertEqual(controller.task_stats("task-2")["prompt_tokens"], 9)

    def test_task_stats_can_move_threads_and_round_trip_through_checkpoint(self):
        controller = self._controller(DelayedProvider(delay=0), workers=2)

        def call(value):
            with controller.task_scope("same-task"):
                controller.generate([{"role": "user", "content": str(value)}])

        with ThreadPoolExecutor(max_workers=2) as executor:
            list(executor.map(call, (1, 2)))

        checkpoint = controller.snapshot_task_stats()
        restored = self._controller(DelayedProvider(delay=0), workers=2)
        restored.restore_task_stats(checkpoint)

        self.assertEqual(
            restored.task_stats("same-task"),
            controller.task_stats("same-task"),
        )
        restored.clear_task_stats("same-task")
        self.assertEqual(restored.task_stats("same-task")["request_count"], 0)

    def test_provider_errors_release_capacity_and_are_counted(self):
        controller = self._controller(DelayedProvider(delay=0), workers=1)

        with controller.task_scope("failure"):
            with self.assertRaisesRegex(RuntimeError, "provider failure"):
                controller.generate([{"role": "user", "content": "-1"}])
        with controller.task_scope("success"):
            self.assertEqual(
                controller.generate([{"role": "user", "content": "0"}]),
                "0",
            )

        stats = controller.snapshot_stats()
        self.assertEqual(stats["request_count"], 2)
        self.assertEqual(stats["error_count"], 1)
        self.assertEqual(controller.task_stats("failure")["error_count"], 1)
        self.assertEqual(controller.task_stats("success")["request_count"], 1)


if __name__ == "__main__":
    unittest.main()
