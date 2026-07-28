from __future__ import annotations

import copy
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml


VALID_DSLS = {"triton", "tilelang"}
VALID_WORKFLOWS = {"fixed", "langchain"}
VALID_MEMORIES = {"none", "flat", "tree"}
VALID_BACKENDS = {"openai", "vllm"}


@dataclass
class ModelConfig:
    backend: str = "vllm"
    model_id: str = "/shared/models/hf/Qwen3.5-35B-A3B"
    base_url: Optional[str] = "http://localhost:8001/v1"
    api_key_env: str = "VLLM_API_KEY"
    temperature: float = 1.0
    max_tokens: int = 8192
    top_p: float = 0.95
    min_p: float = 0.05
    top_k: int = 20
    repetition_penalty: float = 1.0
    enable_thinking: bool = True
    request_timeout_seconds: int = 300


@dataclass
class ParallelismConfig:
    model_workers: int = 8


@dataclass
class BudgetConfig:
    max_model_calls: int = 10
    max_candidate_evaluations: int = 5
    max_tokens_per_call: int = 8192
    model_timeout_seconds: int = 300
    correctness_timeout_seconds: int = 120
    performance_timeout_seconds: int = 600
    task_timeout_seconds: int = 3600


@dataclass
class MatrixConfig:
    dsls: List[str] = field(default_factory=lambda: ["triton", "tilelang"])
    workflows: List[str] = field(default_factory=lambda: ["fixed", "langchain"])
    memories: List[str] = field(default_factory=lambda: ["none", "flat", "tree"])
    seeds: List[int] = field(default_factory=lambda: [0, 1, 2])
    adaptation_epochs: int = 3


@dataclass
class MemoryConfig:
    top_k: int = 20
    use_fixed_categories: bool = False
    prune_threshold: float = 0.5
    prune_age_threshold: int = 2
    embedding_model: str = "/shared/models/hf/Qwen3-Embedding-0.6B"
    embedding_cache: str = "outputs/main_experiment/_embedding_cache.json"
    initial_files: Dict[str, str] = field(default_factory=dict)


@dataclass
class RetrievalConfig:
    enabled_dsls: List[str] = field(default_factory=lambda: ["triton"])
    corpus_path: str = "src/dataloaders/TB_eval/train_crawl.json"
    top_k: int = 1


@dataclass
class DatasetConfig:
    statis_path: str
    py_folder: str
    instruction_path: str
    golden_metrics: str
    perf_G_path: str
    py_interpreter: str = "python"
    correctness_gpu: int = 0
    performance_gpu: int = 0


@dataclass
class ExperimentConfig:
    name: str
    phase: str
    output_root: str
    split_manifest: str
    model: ModelConfig
    budget: BudgetConfig
    parallelism: ParallelismConfig
    matrix: MatrixConfig
    memory: MemoryConfig
    retrieval: RetrievalConfig
    datasets: Dict[str, DatasetConfig]
    pilot_adaptation_tasks: int = 5
    pilot_evaluation_tasks: int = 5
    pilot_adaptation_epochs: int = 1

    def validate(self) -> None:
        if self.model.backend not in VALID_BACKENDS:
            raise ValueError(f"model.backend must be one of {sorted(VALID_BACKENDS)}")
        if not self.model.model_id or not self.model.api_key_env:
            raise ValueError("model.model_id and model.api_key_env are required")
        if self.model.backend == "vllm" and not self.model.base_url:
            raise ValueError("model.base_url is required for the vllm backend")
        _validate_values("matrix.dsls", self.matrix.dsls, VALID_DSLS)
        if self.parallelism.model_workers < 1:
            raise ValueError("parallelism.model_workers must be at least 1")
        _validate_values("matrix.workflows", self.matrix.workflows, VALID_WORKFLOWS)
        _validate_values("matrix.memories", self.matrix.memories, VALID_MEMORIES)
        if not self.matrix.seeds or len(set(self.matrix.seeds)) != len(self.matrix.seeds):
            raise ValueError("matrix.seeds must be a non-empty list of unique integers")
        if self.matrix.adaptation_epochs <= 0:
            raise ValueError("matrix.adaptation_epochs must be positive")
        if self.budget.max_model_calls <= 0 or self.budget.max_candidate_evaluations <= 0:
            raise ValueError("model and candidate-evaluation budgets must be positive")
        expected_timeouts = (300, 120, 600, 3600)
        actual_timeouts = (
            self.budget.model_timeout_seconds,
            self.budget.correctness_timeout_seconds,
            self.budget.performance_timeout_seconds,
            self.budget.task_timeout_seconds,
        )
        if actual_timeouts != expected_timeouts:
            raise ValueError(f"main protocol timeouts must be {expected_timeouts}; got {actual_timeouts}")
        if self.model.request_timeout_seconds != self.budget.model_timeout_seconds:
            raise ValueError("model and budget request timeouts must match")
        if self.model.max_tokens != self.budget.max_tokens_per_call:
            raise ValueError("model and budget maximum completion tokens must match")
        if self.memory.top_k <= 0 or self.retrieval.top_k != 1:
            raise ValueError("memory.top_k must be positive and retrieval.top_k must be 1")
        missing = set(self.matrix.dsls) - set(self.datasets)
        if missing:
            raise ValueError(f"missing dataset configuration for: {sorted(missing)}")
        missing_initial = ({"triton", "tilelang"} & set(self.matrix.dsls)) - set(self.memory.initial_files)
        if missing_initial:
            raise ValueError(f"missing initial memory files for: {sorted(missing_initial)}")

    def to_dict(self, redact_secrets: bool = True) -> Dict[str, Any]:
        data = asdict(self)
        if redact_secrets:
            data["model"]["api_key_env"] = self.model.api_key_env
            data["model"].pop("api_key", None)
        return data


@dataclass(frozen=True)
class RunSpec:
    experiment_name: str
    phase: str
    backend: str
    model_id: str
    dsl: str
    workflow: str
    model_workers: int
    memory: str
    seed: int
    adaptation_epochs: int
    output_root: str

    @property
    def model_slug(self) -> str:
        model_name = self.model_id.rstrip("/").split("/")[-1]
        return _slug(model_name)

    @property
    def run_id(self) -> str:
        return "__".join(
            [
                _slug(self.phase),
                _slug(self.backend),
                self.model_slug,
                _slug(self.dsl),
                _slug(self.workflow),
                f"workers_{self.model_workers}",
                _slug(self.memory),
                f"seed_{self.seed}",
            ]
        )

    @property
    def output_dir(self) -> str:
        root = Path(self.output_root)
        if self.phase != "main":
            root = root / self.phase
        return str(
            root
            / self.backend
            / self.dsl
            / self.workflow
            / self.memory
            / f"seed_{self.seed}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {**asdict(self), "run_id": self.run_id, "output_dir": self.output_dir}


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-").lower()


def _validate_values(name: str, values: Iterable[str], allowed: set[str]) -> None:
    values = list(values)
    invalid = set(values) - allowed
    if not values or invalid or len(set(values)) != len(values):
        raise ValueError(f"{name} must contain unique values from {sorted(allowed)}; got {values}")


def _dataset_from_dict(value: Dict[str, Any]) -> DatasetConfig:
    return DatasetConfig(**value)


def load_experiment_config(path: str) -> ExperimentConfig:
    config_path = Path(path).resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    experiment = raw.get("experiment", {})
    datasets = {
        dsl: _dataset_from_dict(value)
        for dsl, value in (raw.get("datasets", {}) or {}).items()
    }
    config = ExperimentConfig(
        name=experiment.get("name", "main_experiment"),
        phase=experiment.get("phase", "main"),
        output_root=experiment.get("output_root", "outputs/main_experiment"),
        split_manifest=experiment.get("split_manifest", "src/configs/paired_split.json"),
        model=ModelConfig(**(raw.get("model", {}) or {})),
        budget=BudgetConfig(**(raw.get("budget", {}) or {})),
        matrix=MatrixConfig(**(raw.get("matrix", {}) or {})),
        parallelism=ParallelismConfig(**(raw.get("parallelism", {}) or {})),
        memory=MemoryConfig(**(raw.get("memory", {}) or {})),
        retrieval=RetrievalConfig(**(raw.get("retrieval", {}) or {})),
        datasets=datasets,
        pilot_adaptation_tasks=experiment.get("pilot_adaptation_tasks", 5),
        pilot_evaluation_tasks=experiment.get("pilot_evaluation_tasks", 5),
        pilot_adaptation_epochs=experiment.get("pilot_adaptation_epochs", 1),
    )
    config.validate()
    return config


def expand_run_specs(
    config: ExperimentConfig,
    *,
    pilot: bool = False,
    filters: Optional[Dict[str, str]] = None,
) -> List[RunSpec]:
    filters = filters or {}
    seeds = [config.matrix.seeds[0]] if pilot else config.matrix.seeds
    phase = "pilot" if pilot else config.phase
    adaptation_epochs = config.pilot_adaptation_epochs if pilot else config.matrix.adaptation_epochs
    specs = []
    for dsl in config.matrix.dsls:
        for workflow in config.matrix.workflows:
            for memory in config.matrix.memories:
                for seed in seeds:
                    spec = RunSpec(
                        experiment_name=config.name,
                        phase=phase,
                        backend=config.model.backend,
                        model_id=config.model.model_id,
                        dsl=dsl,
                        workflow=workflow,
                        model_workers=config.parallelism.model_workers,
                        memory=memory,
                        seed=seed,
                        adaptation_epochs=adaptation_epochs,
                        output_root=config.output_root,
                    )
                    if all(str(getattr(spec, key)) == str(value) for key, value in filters.items()):
                        specs.append(spec)
    run_ids = [spec.run_id for spec in specs]
    if len(run_ids) != len(set(run_ids)):
        raise ValueError("matrix expansion produced duplicate run IDs")
    return specs


def load_split_manifest(path: str) -> Dict[str, List[str]]:
    with open(path, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    adaptation = manifest.get("adaptation", [])
    evaluation = manifest.get("evaluation", [])
    if len(adaptation) != 147 or len(evaluation) != 37:
        raise ValueError(
            f"paired split must contain 147 adaptation and 37 evaluation tasks; "
            f"got {len(adaptation)} and {len(evaluation)}"
        )
    if len(set(adaptation + evaluation)) != 184:
        raise ValueError("paired split filenames must be unique and non-overlapping")
    return {"adaptation": adaptation, "evaluation": evaluation}


def resolved_config_for_run(config: ExperimentConfig, spec: RunSpec) -> Dict[str, Any]:
    resolved = copy.deepcopy(config.to_dict(redact_secrets=True))
    resolved["run"] = spec.to_dict()
    resolved["model"]["seed"] = spec.seed
    return resolved
