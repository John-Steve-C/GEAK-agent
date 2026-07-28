from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Optional

from .config import DatasetConfig
from .records import CandidateResult


REFERENCE_LOCK = threading.Lock()
HASH_LINE = "#" * 146


def create_dataset(dsl: str, config: DatasetConfig):
    common = {
        "statis_path": config.statis_path,
        "py_folder": config.py_folder,
        "instruction_path": config.instruction_path,
        "py_interpreter": config.py_interpreter,
        "golden_metrics": config.golden_metrics,
        "perf_G_path": config.perf_G_path,
    }
    if dsl == "triton":
        from dataloaders.TritonBench import TritonBench

        return TritonBench(**common)
    if dsl == "tilelang":
        from dataloaders.TilelangBench import TilelangBench

        os.environ["TILELANG_EVAL_GPU"] = str(config.correctness_gpu)
        return TilelangBench(**common)
    raise ValueError(f"unsupported DSL: {dsl}")


class Evaluator:
    """Shared correctness and performance adapter for both benchmark loaders."""

    def __init__(
        self,
        dataset,
        dsl: str,
        dataset_config: DatasetConfig,
        run_root: str,
        reference_cache_root: str,
    ):
        self.dataset = dataset
        self.dsl = dsl
        self.config = dataset_config
        self.run_root = Path(run_root)
        self.reference_cache_root = (
            Path(reference_cache_root) / dsl / f"gpu_{dataset_config.performance_gpu}"
        )

    def evaluate_candidate(self, code: str, task, attempt: int = 1) -> CandidateResult:
        filename = task.filename if hasattr(task, "filename") else str(task)
        start = time.monotonic()
        safe_name = Path(filename).stem
        attempt_root = self.run_root / "evaluation" / safe_name / f"attempt_{attempt}"
        tmp_dir = attempt_root / "correctness_tmp"
        exe_dir = attempt_root / "correctness_pass"
        result = CandidateResult(filename=filename, code=code)
        try:
            pass_call, pass_exe, _, call_stderr, _, exe_stderr = self.dataset.test_opt_correctness(
                code,
                filename,
                tmp_dir=str(tmp_dir),
                exe_dir=str(exe_dir),
            )
            result.pass_call = bool(pass_call)
            result.pass_correctness = bool(pass_exe)
            if not result.pass_call:
                result.call_error = str(call_stderr)
            elif not result.pass_correctness:
                result.correctness_error = str(exe_stderr)
        except Exception as exc:
            result.call_error = str(exc)

        if result.pass_correctness:
            try:
                reference_path = self._reference_metrics(filename)
            except Exception as exc:
                result.performance_error = str(exc)
                result.error_type = "REFERENCE_EVALUATION_FAILURE"
            else:
                try:
                    generated_path = self._run_performance(
                        code=code,
                        filename=filename,
                        root=attempt_root / "performance",
                    )
                    speedup, efficiency, latency = self.dataset.calculate(
                        str(generated_path),
                        path_ref=str(reference_path),
                    )
                    _, _, reference_latency = self.dataset.calculate(
                        str(reference_path), path_ref=None
                    )
                    result.perf_evaluated = True
                    result.latency_ms = latency
                    result.reference_latency_ms = reference_latency
                    result.normalized_speedup = speedup
                    result.efficiency = efficiency
                except Exception as exc:
                    result.performance_error = str(exc)
                    result.error_type = "PERFORMANCE_EVALUATION_FAILURE"

        result.error_type = result.error_type or classify_candidate_result(result)
        result.wall_time_seconds = time.monotonic() - start
        return result

    def _reference_metrics(self, filename: str) -> Path:
        destination = self.reference_cache_root / f"{Path(filename).stem}.json"
        if destination.exists() and _has_metrics(destination):
            return destination
        with REFERENCE_LOCK:
            if destination.exists() and _has_metrics(destination):
                return destination
            reference_file = Path(self.dataset.py_folder) / filename
            with reference_file.open("r", encoding="utf-8") as handle:
                reference_code = handle.read().split(HASH_LINE, 1)[0].strip()
            generated = self._run_performance(
                code=reference_code,
                filename=filename,
                root=self.reference_cache_root / "_work" / Path(filename).stem,
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(generated, destination)
        return destination

    def _run_performance(self, code: str, filename: str, root: Path) -> Path:
        exe_dir = root / "code"
        result_dir = root / "results"
        script_dir = root / "scripts"
        log_dir = root / "logs"
        exe_dir.mkdir(parents=True, exist_ok=True)
        (exe_dir / filename).write_text(code, encoding="utf-8")
        self.dataset.write_perf_file_single(
            input_folder_path=str(exe_dir),
            results_path=str(result_dir),
            tmp_dir=str(script_dir),
            filename=filename,
        )
        self.dataset.run_perf_script_single(
            script_dir=str(script_dir),
            log_dir=str(log_dir),
            gpu_id=self.config.performance_gpu,
            script_name=f"{Path(filename).stem}_perf.py",
        )
        metrics_path = result_dir / f"{Path(filename).stem}.json"
        if not metrics_path.exists() or not _has_metrics(metrics_path):
            raise RuntimeError(f"performance metrics were not produced: {metrics_path}")
        return metrics_path


def _has_metrics(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(data, list) and bool(data)


def classify_candidate_result(result: CandidateResult) -> Optional[str]:
    if result.call_error:
        lowered = result.call_error.lower()
        if "timeout" in lowered:
            return "TIMEOUT"
        if "reference" in lowered or "evaluation" in lowered:
            return "REFERENCE_EVALUATION_FAILURE"
        return "COMPILE_OR_LAUNCH_FAILURE"
    if result.correctness_error:
        lowered = result.correctness_error.lower()
        if "timeout" in lowered:
            return "TIMEOUT"
        if "does not match" in lowered or "mismatch" in lowered:
            return "WRONG_OUTPUT"
        return "RUNTIME_FAILURE"
    if result.pass_correctness and not result.perf_evaluated:
        return "PERFORMANCE_EVALUATION_FAILURE"
    return None
