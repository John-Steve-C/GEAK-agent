from __future__ import annotations

import json
import os
import platform
import sys
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

import yaml

from .records import TaskExecution, TaskResult


class RunOutput:
    def __init__(self, root: str, resume: bool):
        self.root = Path(root)
        if self.root.exists() and any(self.root.iterdir()) and not resume:
            raise FileExistsError(
                f"run output already exists: {self.root}; use --resume instead of overwriting it"
            )
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "memory").mkdir(exist_ok=True)
        (self.root / "task_records").mkdir(exist_ok=True)
        (self.root / "pending").mkdir(exist_ok=True)

    def write_resolved_config(self, config: Dict[str, Any]) -> None:
        self._atomic_text(
            self.root / "resolved_config.yaml",
            yaml.safe_dump(config, sort_keys=False),
        )

    def validate_resume_config(self, config: Dict[str, Any]) -> None:
        path = self.root / "resolved_config.yaml"
        if not path.exists():
            return
        existing = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        existing_run = existing.get("run", {})
        requested_run = config.get("run", {})
        if existing_run.get("run_id") != requested_run.get("run_id"):
            raise RuntimeError(
                "resume configuration does not match the existing run: "
                f"{existing_run.get('run_id')!r} != {requested_run.get('run_id')!r}"
            )
        existing_workers = (existing.get("parallelism") or {}).get("model_workers", 1)
        requested_workers = (config.get("parallelism") or {}).get("model_workers", 1)
        if existing_workers != requested_workers:
            raise RuntimeError("cannot change parallelism.model_workers while resuming a run")

    def write_environment(self) -> None:
        environment = {
            "python": sys.version,
            "platform": platform.platform(),
            "executable": sys.executable,
        }
        try:
            import torch

            environment["torch"] = torch.__version__
            environment["cuda_available"] = torch.cuda.is_available()
            if torch.cuda.is_available():
                environment["gpu"] = torch.cuda.get_device_name(0)
        except ImportError:
            pass
        self._atomic_json(self.root / "environment.json", environment)

    def append_task_result(self, result: TaskResult) -> None:
        """Legacy append API retained for compatibility wrappers and tests."""
        self._append_jsonl(self.root / "task_results.jsonl", result.to_dict())
        for attempt in result.attempts:
            self._append_jsonl(self.root / "attempts.jsonl", attempt.to_dict())
        for index, tool_call in enumerate(result.tool_calls):
            self._append_jsonl(
                self.root / "tool_calls.jsonl",
                {
                    "filename": result.filename,
                    "phase": result.phase,
                    "epoch": result.epoch,
                    "order": index,
                    **tool_call,
                },
            )

    @staticmethod
    def _key_name(completion_key: str) -> str:
        digest = sha256(completion_key.encode("utf-8")).hexdigest()
        return f"{digest}.json"

    def write_pending_execution(
        self, completion_key: str, execution: TaskExecution, order: int
    ) -> None:
        self._atomic_json(
            self.root / "pending" / self._key_name(completion_key),
            {
                "completion_key": completion_key,
                "order": order,
                "execution": execution.to_dict(),
            },
        )

    def load_pending_execution(self, completion_key: str) -> Optional[TaskExecution]:
        path = self.root / "pending" / self._key_name(completion_key)
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("completion_key") != completion_key:
            raise RuntimeError(f"pending task key mismatch in {path}")
        return TaskExecution.from_dict(payload["execution"])

    def remove_pending_execution(self, completion_key: str) -> None:
        path = self.root / "pending" / self._key_name(completion_key)
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def write_task_record(
        self, completion_key: str, result: TaskResult, order: int
    ) -> None:
        self._atomic_json(
            self.root / "task_records" / self._key_name(completion_key),
            {
                "completion_key": completion_key,
                "order": order,
                "result": result.to_dict(),
                "attempts": [attempt.to_dict() for attempt in result.attempts],
            },
        )

    def completed_task_keys(self) -> Set[str]:
        keys = set()
        for path in (self.root / "task_records").glob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            key = payload.get("completion_key")
            if key:
                keys.add(key)
        return keys

    def rebuild_jsonl(self) -> None:
        """Rebuild all public JSONLs atomically from canonical task records."""
        records = []
        for path in (self.root / "task_records").glob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            records.append(payload)
        records.sort(key=lambda item: (int(item["order"]), item["completion_key"]))

        task_lines = []
        attempt_lines = []
        tool_lines = []
        for payload in records:
            result_data = dict(payload["result"])
            result_data["attempts"] = payload.get("attempts", [])
            result = TaskResult.from_dict(result_data)
            task_lines.append(json.dumps(result.to_dict(), ensure_ascii=False))
            attempt_lines.extend(
                json.dumps(attempt.to_dict(), ensure_ascii=False)
                for attempt in result.attempts
            )
            tool_lines.extend(
                json.dumps(
                    {
                        "filename": result.filename,
                        "phase": result.phase,
                        "epoch": result.epoch,
                        "order": index,
                        **tool_call,
                    },
                    ensure_ascii=False,
                )
                for index, tool_call in enumerate(result.tool_calls)
            )

        self._atomic_text(
            self.root / "task_results.jsonl",
            "".join(line + "\n" for line in task_lines),
        )
        self._atomic_text(
            self.root / "attempts.jsonl",
            "".join(line + "\n" for line in attempt_lines),
        )
        self._atomic_text(
            self.root / "tool_calls.jsonl",
            "".join(line + "\n" for line in tool_lines),
        )

    def load_checkpoint(self) -> Dict[str, Any]:
        path = self.root / "checkpoint.json"
        if not path.exists():
            return {"completed": [], "pruned_epochs": []}
        return json.loads(path.read_text(encoding="utf-8"))

    def write_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        self._atomic_json(self.root / "checkpoint.json", checkpoint)

    def write_metrics(self, model_stats: Dict[str, Any]) -> None:
        if any((self.root / "task_records").glob("*.json")):
            self.rebuild_jsonl()
        task_rows = list(self._read_jsonl(self.root / "task_results.jsonl"))
        attempt_rows = list(self._read_jsonl(self.root / "attempts.jsonl"))
        attempts_by_task: Dict[tuple, List[Dict[str, Any]]] = defaultdict(list)
        for row in attempt_rows:
            attempts_by_task[(row["phase"], row["epoch"], row["filename"])].append(row)
        groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for row in task_rows:
            key = f"{row['phase']}:{row['epoch']}"
            groups[key].append(row)
        metrics = {"model": model_stats, "groups": {}}
        for key, rows in groups.items():
            best = [row.get("best_candidate") for row in rows if row.get("best_candidate")]
            correct = [row for row in best if row.get("pass_correctness")]
            perf = [row for row in correct if row.get("perf_evaluated")]
            speedups = [
                row["normalized_speedup"]
                for row in perf
                if row.get("normalized_speedup") is not None
            ]
            latencies = [
                row["latency_ms"] for row in perf if row.get("latency_ms") is not None
            ]
            errors = Counter(row.get("error_type") for row in best if row.get("error_type"))
            total = len(rows)
            group_attempts = [
                attempts_by_task[(row["phase"], row["epoch"], row["filename"])]
                for row in rows
            ]
            first_correct = []
            anytime = {}
            for task_attempts in group_attempts:
                correct_attempts = [
                    item["attempt"]
                    for item in task_attempts
                    if (item.get("candidate") or {}).get("pass_correctness")
                ]
                if correct_attempts:
                    first_correct.append(min(correct_attempts))
            for attempt_index in range(1, 6):
                anytime[str(attempt_index)] = (
                    sum(
                        any(
                            item["attempt"] <= attempt_index
                            and (item.get("candidate") or {}).get("pass_correctness")
                            for item in task_attempts
                        )
                        for task_attempts in group_attempts
                    )
                    / total
                    if total
                    else 0
                )
            metrics["groups"][key] = {
                "tasks": total,
                "call_success_rate": sum(bool(row.get("pass_call")) for row in best) / total
                if total
                else 0,
                "correctness_rate": len(correct) / total if total else 0,
                "performance_coverage": len(perf) / total if total else 0,
                "mean_normalized_speedup": sum(speedups) / len(speedups)
                if speedups
                else None,
                "mean_fastest_correct_latency_ms": sum(latencies) / len(latencies)
                if latencies
                else None,
                "mean_attempts_to_first_correct": sum(first_correct) / len(first_correct)
                if first_correct
                else None,
                "anytime_success_by_attempt": anytime,
                "mean_prompt_tokens": sum(row.get("prompt_tokens", 0) for row in rows)
                / total
                if total
                else 0,
                "mean_completion_tokens": sum(
                    row.get("completion_tokens", 0) for row in rows
                )
                / total
                if total
                else 0,
                "mean_model_calls": sum(row["model_calls"] for row in rows) / total
                if total
                else 0,
                "mean_evaluator_calls": sum(row["evaluator_calls"] for row in rows)
                / total
                if total
                else 0,
                "mean_wall_time_seconds": sum(
                    row.get("wall_time_seconds", 0.0) for row in rows
                )
                / total
                if total
                else 0,
                "errors": dict(errors),
            }
        self._atomic_json(self.root / "metrics.json", metrics)

    @staticmethod
    def _read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
        if not path.exists():
            return []
        rows = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    @staticmethod
    def _append_jsonl(path: Path, data: Dict[str, Any]) -> None:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(data, ensure_ascii=False) + "\n")

    @staticmethod
    def _atomic_json(path: Path, data: Dict[str, Any]) -> None:
        RunOutput._atomic_text(path, json.dumps(data, indent=2, ensure_ascii=False))

    @staticmethod
    def _atomic_text(path: Path, text: str) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
