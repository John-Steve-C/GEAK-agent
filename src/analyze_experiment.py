from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiments.analysis import analyze_observations, load_primary_observations


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze paired GEAK-agent experiment results")
    parser.add_argument("--root", default="outputs/main_experiment")
    parser.add_argument("--output", default=None)
    parser.add_argument("--bootstrap-samples", type=int, default=10000)
    parser.add_argument("--bootstrap-seed", type=int, default=0)
    args = parser.parse_args()

    observations = load_primary_observations(args.root)
    if not observations:
        raise RuntimeError(f"no primary task_results.jsonl files found under {args.root}")
    analysis = analyze_observations(
        observations,
        bootstrap_samples=args.bootstrap_samples,
        bootstrap_seed=args.bootstrap_seed,
    )
    output_path = Path(args.output or (Path(args.root) / "analysis.json"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
