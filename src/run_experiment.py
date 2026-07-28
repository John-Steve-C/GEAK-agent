from __future__ import annotations

import argparse
import json
from typing import Dict, Iterable, Optional

from experiments.config import expand_run_specs, load_experiment_config, load_split_manifest
from experiments.runner import run_spec, validate_paired_datasets


DEFAULT_CONFIG = "src/configs/main_experiment.yaml"


def parse_filters(values: Iterable[str]) -> Dict[str, str]:
    filters = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"--only expects key=value, got {value!r}")
        key, selected = value.split("=", 1)
        if key not in {"dsl", "workflow", "memory", "seed"}:
            raise ValueError(f"unsupported --only key: {key}")
        filters[key] = selected
    return filters


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the unified GEAK-agent experiment matrix")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--resume", action="store_true")
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--only", action="append", default=[], metavar="KEY=VALUE")
    parser.add_argument(
        "--model-workers",
        type=int,
        default=None,
        metavar="N",
        help="maximum concurrent model API calls inside each experiment cell",
    )
    return parser


def main(argv: Optional[Iterable[str]] = None, default_filters: Optional[Dict[str, str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    config = load_experiment_config(args.config)
    filters = {**(default_filters or {}), **parse_filters(args.only)}
    if args.model_workers is not None:
        config.parallelism.model_workers = args.model_workers
        config.validate()
    specs = expand_run_specs(config, pilot=args.pilot, filters=filters)
    manifest = load_split_manifest(config.split_manifest)
    validate_paired_datasets(config, manifest)
    if args.dry_run:
        print(json.dumps({"count": len(specs), "runs": [spec.to_dict() for spec in specs]}, indent=2))
        return 0
    if not specs:
        raise RuntimeError("the selected filters produced no experiment runs")
    for index, spec in enumerate(specs):
        print(f"[{index + 1}/{len(specs)}] {spec.run_id}")
        run_spec(
            config,
            spec,
            resume=args.resume,
            pilot=args.pilot,
            validate_connection=index == 0,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
