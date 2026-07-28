from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional, Tuple


Condition = Tuple[str, str, str, str]
ObservationKey = Tuple[int, str]
Observations = Dict[Condition, Dict[ObservationKey, Dict[str, Any]]]


def load_primary_observations(root: str) -> Observations:
    observations: Observations = defaultdict(dict)
    root_path = Path(root)
    for path in sorted(root_path.glob("*/*/*/*/seed_*/task_results.jsonl")):
        provider, dsl, workflow, memory, seed_dir = path.relative_to(root_path).parts[:5]
        seed = int(seed_dir.removeprefix("seed_"))
        condition = (provider, dsl, workflow, memory)
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("phase") != "evaluation":
                    continue
                best = row.get("best_candidate") or {}
                observations[condition][(seed, row["filename"])] = {
                    "correct": bool(best.get("pass_correctness")),
                    "perf_evaluated": bool(best.get("perf_evaluated")),
                    "normalized_speedup": best.get("normalized_speedup"),
                    "latency_ms": best.get("latency_ms"),
                    "model_calls": row.get("model_calls", 0),
                    "evaluator_calls": row.get("evaluator_calls", 0),
                    "prompt_tokens": row.get("prompt_tokens", 0),
                    "completion_tokens": row.get("completion_tokens", 0),
                    "wall_time_seconds": row.get("wall_time_seconds", 0.0),
                }
    return dict(observations)


def analyze_observations(
    observations: Observations,
    *,
    bootstrap_samples: int = 10000,
    bootstrap_seed: int = 0,
) -> Dict[str, Any]:
    providers = sorted({condition[0] for condition in observations})
    return {
        "bootstrap_samples": bootstrap_samples,
        "bootstrap_seed": bootstrap_seed,
        "providers": {
            provider: _analyze_provider(
                observations,
                provider,
                bootstrap_samples=bootstrap_samples,
                bootstrap_seed=bootstrap_seed,
            )
            for provider in providers
        },
    }


def _analyze_provider(
    observations: Observations,
    provider: str,
    *,
    bootstrap_samples: int,
    bootstrap_seed: int,
) -> Dict[str, Any]:
    provider_conditions = {
        condition: rows for condition, rows in observations.items() if condition[0] == provider
    }
    conditions = {
        "/".join(condition[1:]): _condition_summary(rows)
        for condition, rows in sorted(provider_conditions.items())
    }
    memory_pairs = (("tree", "flat"), ("flat", "none"), ("tree", "none"))
    contrasts = []
    for dsl in ("triton", "tilelang"):
        for workflow in ("fixed", "langchain"):
            for memory_a, memory_b in memory_pairs:
                condition_a = (provider, dsl, workflow, memory_a)
                condition_b = (provider, dsl, workflow, memory_b)
                if condition_a in provider_conditions and condition_b in provider_conditions:
                    contrasts.append(
                        {
                            "dsl": dsl,
                            "workflow": workflow,
                            "contrast": f"{memory_a}-{memory_b}",
                            **paired_condition_contrast(
                                provider_conditions[condition_a],
                                provider_conditions[condition_b],
                                bootstrap_samples=bootstrap_samples,
                                bootstrap_seed=bootstrap_seed,
                            ),
                        }
                    )

    interactions = []
    for memory_a, memory_b in memory_pairs:
        for workflow in ("fixed", "langchain"):
            conditions_for_interaction = [
                (provider, dsl, workflow, memory)
                for dsl in ("triton", "tilelang")
                for memory in (memory_a, memory_b)
            ]
            if all(condition in provider_conditions for condition in conditions_for_interaction):
                interactions.append(
                    _interaction_report(
                        label=f"dsl:{workflow}:{memory_a}-{memory_b}",
                        positive_a=provider_conditions[(provider, "triton", workflow, memory_a)],
                        negative_a=provider_conditions[(provider, "triton", workflow, memory_b)],
                        positive_b=provider_conditions[(provider, "tilelang", workflow, memory_a)],
                        negative_b=provider_conditions[(provider, "tilelang", workflow, memory_b)],
                        bootstrap_samples=bootstrap_samples,
                        bootstrap_seed=bootstrap_seed,
                    )
                )
        for dsl in ("triton", "tilelang"):
            conditions_for_interaction = [
                (provider, dsl, workflow, memory)
                for workflow in ("fixed", "langchain")
                for memory in (memory_a, memory_b)
            ]
            if all(condition in provider_conditions for condition in conditions_for_interaction):
                interactions.append(
                    _interaction_report(
                        label=f"workflow:{dsl}:{memory_a}-{memory_b}",
                        positive_a=provider_conditions[(provider, dsl, "fixed", memory_a)],
                        negative_a=provider_conditions[(provider, dsl, "fixed", memory_b)],
                        positive_b=provider_conditions[(provider, dsl, "langchain", memory_a)],
                        negative_b=provider_conditions[(provider, dsl, "langchain", memory_b)],
                        bootstrap_samples=bootstrap_samples,
                        bootstrap_seed=bootstrap_seed,
                    )
                )
    return {"conditions": conditions, "contrasts": contrasts, "interactions": interactions}


def _condition_summary(rows: Dict[ObservationKey, Dict[str, Any]]) -> Dict[str, Any]:
    values = list(rows.values())
    speedups = [row["normalized_speedup"] for row in values if row["normalized_speedup"] is not None]
    return {
        "observations": len(values),
        "filenames": len({filename for _, filename in rows}),
        "correctness": mean(row["correct"] for row in values) if values else None,
        "performance_coverage": mean(row["perf_evaluated"] for row in values) if values else None,
        "mean_normalized_speedup": mean(speedups) if speedups else None,
        "mean_model_calls": mean(row["model_calls"] for row in values) if values else None,
        "mean_evaluator_calls": mean(row["evaluator_calls"] for row in values) if values else None,
        "mean_total_tokens": (
            mean(row["prompt_tokens"] + row["completion_tokens"] for row in values)
            if values
            else None
        ),
        "mean_wall_time_seconds": mean(row["wall_time_seconds"] for row in values) if values else None,
    }


def paired_condition_contrast(
    condition_a: Dict[ObservationKey, Dict[str, Any]],
    condition_b: Dict[ObservationKey, Dict[str, Any]],
    *,
    bootstrap_samples: int,
    bootstrap_seed: int,
) -> Dict[str, Any]:
    keys = sorted(set(condition_a) & set(condition_b))
    correctness_differences = [
        (filename, float(condition_a[key]["correct"]) - float(condition_b[key]["correct"]))
        for key in keys
        for filename in [key[1]]
    ]
    a_only = sum(condition_a[key]["correct"] and not condition_b[key]["correct"] for key in keys)
    b_only = sum(condition_b[key]["correct"] and not condition_a[key]["correct"] for key in keys)
    mcnemar_by_seed = {}
    for seed in sorted({key[0] for key in keys}):
        seed_keys = [key for key in keys if key[0] == seed]
        seed_a_only = sum(
            condition_a[key]["correct"] and not condition_b[key]["correct"] for key in seed_keys
        )
        seed_b_only = sum(
            condition_b[key]["correct"] and not condition_a[key]["correct"] for key in seed_keys
        )
        mcnemar_by_seed[str(seed)] = {
            "a_only_correct": seed_a_only,
            "b_only_correct": seed_b_only,
            "exact_two_sided_p": exact_mcnemar_p(seed_a_only, seed_b_only),
        }
    speedup_differences = [
        (
            key[1],
            float(condition_a[key]["normalized_speedup"])
            - float(condition_b[key]["normalized_speedup"]),
        )
        for key in keys
        if condition_a[key]["normalized_speedup"] is not None
        and condition_b[key]["normalized_speedup"] is not None
    ]
    return {
        "paired_observations": len(keys),
        "paired_filenames": len({key[1] for key in keys}),
        "correctness_difference": paired_bootstrap_ci(
            correctness_differences,
            samples=bootstrap_samples,
            seed=bootstrap_seed,
        ),
        "mcnemar": {
            "a_only_correct": a_only,
            "b_only_correct": b_only,
            "exact_two_sided_p": exact_mcnemar_p(a_only, b_only),
        },
        "mcnemar_by_seed": mcnemar_by_seed,
        "joint_speedup_coverage": len(speedup_differences) / len(keys) if keys else 0.0,
        "normalized_speedup_difference": paired_bootstrap_ci(
            speedup_differences,
            samples=bootstrap_samples,
            seed=bootstrap_seed,
        ),
    }


def _interaction_report(
    *,
    label: str,
    positive_a,
    negative_a,
    positive_b,
    negative_b,
    bootstrap_samples: int,
    bootstrap_seed: int,
) -> Dict[str, Any]:
    keys = sorted(set(positive_a) & set(negative_a) & set(positive_b) & set(negative_b))
    correctness = [
        (
            key[1],
            (float(positive_a[key]["correct"]) - float(negative_a[key]["correct"]))
            - (float(positive_b[key]["correct"]) - float(negative_b[key]["correct"])),
        )
        for key in keys
    ]
    speedup = [
        (
            key[1],
            (
                float(positive_a[key]["normalized_speedup"])
                - float(negative_a[key]["normalized_speedup"])
            )
            - (
                float(positive_b[key]["normalized_speedup"])
                - float(negative_b[key]["normalized_speedup"])
            ),
        )
        for key in keys
        if all(
            rows[key]["normalized_speedup"] is not None
            for rows in (positive_a, negative_a, positive_b, negative_b)
        )
    ]
    return {
        "interaction": label,
        "paired_observations": len(keys),
        "correctness_gain_difference": paired_bootstrap_ci(
            correctness, samples=bootstrap_samples, seed=bootstrap_seed
        ),
        "joint_speedup_coverage": len(speedup) / len(keys) if keys else 0.0,
        "normalized_speedup_gain_difference": paired_bootstrap_ci(
            speedup, samples=bootstrap_samples, seed=bootstrap_seed
        ),
    }


def paired_bootstrap_ci(
    filename_differences: Iterable[Tuple[str, float]],
    *,
    samples: int = 10000,
    seed: int = 0,
) -> Dict[str, Optional[float]]:
    by_filename: Dict[str, List[float]] = defaultdict(list)
    for filename, difference in filename_differences:
        by_filename[filename].append(float(difference))
    values = [mean(differences) for _, differences in sorted(by_filename.items())]
    if not values:
        return {"estimate": None, "ci95_low": None, "ci95_high": None}
    estimate = mean(values)
    if len(values) == 1 or samples <= 0:
        return {"estimate": estimate, "ci95_low": estimate, "ci95_high": estimate}
    rng = random.Random(seed)
    draws = sorted(mean(rng.choice(values) for _ in values) for _ in range(samples))
    return {
        "estimate": estimate,
        "ci95_low": _quantile(draws, 0.025),
        "ci95_high": _quantile(draws, 0.975),
    }


def exact_mcnemar_p(a_only: int, b_only: int) -> float:
    discordant = a_only + b_only
    if discordant == 0:
        return 1.0
    lower = min(a_only, b_only)
    tail = sum(math.comb(discordant, value) for value in range(lower + 1)) / (2 ** discordant)
    return min(1.0, 2.0 * tail)


def _quantile(values: List[float], probability: float) -> float:
    index = (len(values) - 1) * probability
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return values[lower]
    weight = index - lower
    return values[lower] * (1.0 - weight) + values[upper] * weight
