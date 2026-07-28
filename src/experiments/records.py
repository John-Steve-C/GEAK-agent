from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class TaskBudget:
    max_model_calls: int
    max_candidate_evaluations: int
    max_tokens_per_call: int
    task_timeout_seconds: int


@dataclass
class TaskContext:
    dsl: str
    workflow: str
    memory: str
    phase: str
    epoch: int
    seed: int
    problem_state: Any

    @property
    def filename(self) -> str:
        return self.problem_state.filename

    @property
    def instruction(self) -> str:
        return self.problem_state.instruction or ""


@dataclass
class CandidateResult:
    filename: str
    code: str
    pass_call: bool = False
    pass_correctness: bool = False
    perf_evaluated: bool = False
    latency_ms: Optional[float] = None
    reference_latency_ms: Optional[float] = None
    normalized_speedup: Optional[float] = None
    efficiency: Optional[float] = None
    call_error: Optional[str] = None
    correctness_error: Optional[str] = None
    performance_error: Optional[str] = None
    error_type: Optional[str] = None
    wall_time_seconds: float = 0.0

    @property
    def code_hash(self) -> str:
        return sha256(self.code.encode("utf-8")).hexdigest()

    def to_dict(self, include_code: bool = True) -> Dict[str, Any]:
        data = asdict(self)
        data["code_hash"] = self.code_hash
        if not include_code:
            data.pop("code", None)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CandidateResult":
        values = dict(data)
        values.pop("code_hash", None)
        values.setdefault("code", "")
        return cls(**values)


@dataclass
class AttemptRecord:
    experiment_id: str
    phase: str
    epoch: int
    seed: int
    dsl: str
    workflow: str
    memory: str
    provider: str
    model_id: str
    filename: str
    attempt: int
    model_calls: int
    evaluator_calls: int
    prompt_tokens: int
    completion_tokens: int
    retrieved_examples: List[Dict[str, Any]] = field(default_factory=list)
    retrieved_example_scores: List[float] = field(default_factory=list)
    retrieved_item_ids: List[str] = field(default_factory=list)
    retrieved_tree_paths: List[str] = field(default_factory=list)
    memory_prompt_chars: int = 0
    candidate: Optional[CandidateResult] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.candidate is not None:
            data["candidate"] = self.candidate.to_dict(include_code=False)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AttemptRecord":
        values = dict(data)
        candidate = values.get("candidate")
        if candidate is not None and not isinstance(candidate, CandidateResult):
            values["candidate"] = CandidateResult.from_dict(candidate)
        return cls(**values)


@dataclass
class TaskResult:
    filename: str
    phase: str
    epoch: int
    model_calls: int
    evaluator_calls: int
    prompt_tokens: int
    completion_tokens: int
    attempts: List[AttemptRecord]
    best_candidate: Optional[CandidateResult]
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    wall_time_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "phase": self.phase,
            "epoch": self.epoch,
            "model_calls": self.model_calls,
            "evaluator_calls": self.evaluator_calls,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "attempt_count": len(self.attempts),
            "best_candidate": self.best_candidate.to_dict() if self.best_candidate else None,
            "tool_calls": self.tool_calls,
            "wall_time_seconds": self.wall_time_seconds,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskResult":
        values = dict(data)
        values.pop("attempt_count", None)
        values["attempts"] = [
            item if isinstance(item, AttemptRecord) else AttemptRecord.from_dict(item)
            for item in values.get("attempts", [])
        ]
        best = values.get("best_candidate")
        if best is not None and not isinstance(best, CandidateResult):
            values["best_candidate"] = CandidateResult.from_dict(best)
        return cls(**values)


@dataclass
class MemoryUsageEvent:
    """A memory-usage mutation staged while an epoch snapshot is being read."""

    model_thought: str
    current_iter: int
    pass_call: bool = False
    pass_correctness: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryUsageEvent":
        return cls(**data)


@dataclass
class MemoryUpdateIntent:
    """Serializable memory work that the runner commits in seeded task order."""

    kind: str = "none"
    task_key: str = ""
    usage_events: List[MemoryUsageEvent] = field(default_factory=list)
    question: str = ""
    answer: str = ""
    reflection: str = ""
    staged_operations: List[str] = field(default_factory=list)
    prepared_operation: Optional[str] = None
    prepared: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryUpdateIntent":
        values = dict(data)
        values["usage_events"] = [
            item if isinstance(item, MemoryUsageEvent) else MemoryUsageEvent.from_dict(item)
            for item in values.get("usage_events", [])
        ]
        return cls(**values)


@dataclass
class TaskExecution:
    """A completed task plus deferred persistent-memory mutations."""

    result: TaskResult
    update_intent: MemoryUpdateIntent = field(default_factory=MemoryUpdateIntent)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result": self.result.to_dict(),
            "attempts": [attempt.to_dict() for attempt in self.result.attempts],
            "update_intent": self.update_intent.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskExecution":
        result = dict(data["result"])
        result["attempts"] = data.get("attempts", result.get("attempts", []))
        return cls(
            result=TaskResult.from_dict(result),
            update_intent=MemoryUpdateIntent.from_dict(data.get("update_intent", {})),
        )
