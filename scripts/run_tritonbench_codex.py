#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from experiments.code_utils import parse_model_response
from experiments.config import load_experiment_config, load_split_manifest
from experiments.evaluator import Evaluator, create_dataset
from utils.utils import extract_function_signatures


def build_parser(default_dsl: str = "triton") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate and evaluate GPU kernels with a Codex model"
    )
    parser.add_argument("--config", default="src/configs/main_experiment.yaml")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--dsl", choices=("triton", "tilelang"), default=default_dsl)
    parser.add_argument("--split", choices=("adaptation", "evaluation"), default="evaluation")
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--max-tasks", type=int, default=1)
    parser.add_argument(
        "--workers",
        "--model-workers",
        dest="workers",
        type=int,
        default=4,
        help="maximum concurrent Codex generation processes",
    )
    parser.add_argument("--output-dir")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--skip-eval", action="store_true")
    return parser


def build_prompt(problem, dsl: str) -> str:
    signature_kwargs = {}
    if dsl == "tilelang":
        signature_kwargs = {"mode": "tilelang", "test_code": problem.test_code}
        implementation_requirement = (
            "The code must be self-contained and use TileLang for the core operation. "
            "Import tilelang as tl and tilelang.language as T. "
            "Do not call `@T.prim_func` function directly; return it from a private `@tl.jit` factory and call the compiled factory result."
            # "Use a private @tl.jit factory containing a nested @T.prim_func named main and return main without "
            # "calling it. In each public wrapper, assign the factory result to a differently "
            # "named variable such as compiled_kernel, then invoke compiled_kernel with the "
            # "PyTorch tensors. Never reuse the inner prim-func name for that callable. "
            "Do not emit Triton kernels or add type annotations to the required public "
            "signatures. When a TileLang dtype string is needed, derive it with exactly "
            "str(x.dtype).replace('torch.', ''); do not use raw str(x.dtype), dtype.name, "
            "lower(), or removeprefix()."
        )
    else:
        implementation_requirement = (
            "The code must be self-contained and use a @triton.jit kernel for the core "
            "operation."
        )
    signatures = extract_function_signatures(problem.label or "", **signature_kwargs)
    return "\n\n".join(
        [
            f"Implement and optimize this task in {dsl}:\n{problem.instruction or ''}",
            "Required public signatures:\n"
            + "\n".join(f"- {signature}" for signature in signatures),
            (
                "Return only JSON with the shape "
                '{"thought":"brief implementation rationale","code":"complete code"}. '
                + implementation_requirement
                + " Preserve every required public signature exactly."
            ),
        ]
    )


def generate(codex: str, model: str, prompt: str, response_path: Path, timeout: int) -> str:
    with tempfile.TemporaryDirectory(prefix="tritonbench_codex_") as workdir:
        command = [
            codex,
            "exec",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "--model",
            model,
            "--color",
            "never",
            "--output-last-message",
            str(response_path.resolve()),
            "-",
        ]
        completed = subprocess.run(
            command,
            cwd=workdir,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"Codex generation failed ({completed.returncode}): {detail}")
    return response_path.read_text(encoding="utf-8")


def generate_problem(
    *,
    codex: str,
    model: str,
    dsl: str,
    problem,
    response_dir: Path,
    code_dir: Path,
    timeout: int,
):
    filename = problem.filename
    stem = Path(filename).stem
    response_path = response_dir / f"{stem}.txt"
    print(f"Generating {filename} with {model}", flush=True)
    response = generate(
        codex=codex,
        model=model,
        prompt=build_prompt(problem, dsl),
        response_path=response_path,
        timeout=timeout,
    )
    thought, code = parse_model_response(response, dsl)
    if not code.strip():
        raise RuntimeError(f"the model returned no parseable code for {filename}")
    code_path = code_dir / filename
    code_path.write_text(code, encoding="utf-8")
    return thought, code, response_path, code_path


def main(default_dsl: str = "triton") -> int:
    args = build_parser(default_dsl).parse_args()
    if args.index < 0 or args.max_tasks < 1 or args.workers < 1:
        raise ValueError(
            "--index must be non-negative; --max-tasks and --workers must be positive"
        )

    codex = shutil.which("codex")
    if codex is None:
        raise RuntimeError("codex CLI was not found on PATH")

    config = load_experiment_config(args.config)
    manifest = load_split_manifest(config.split_manifest)
    selected = manifest[args.split][args.index : args.index + args.max_tasks]
    if not selected:
        raise ValueError(f"no {args.split} tasks start at index {args.index}")

    dataset_config = config.datasets[args.dsl]
    dataset = create_dataset(args.dsl, dataset_config)
    problems = {problem.filename: problem for problem in dataset.problem_states}
    output_dir = Path(args.output_dir or f"outputs/{args.dsl}bench_codex")
    response_dir = output_dir / "responses"
    code_dir = output_dir / "generated"
    response_dir.mkdir(parents=True, exist_ok=True)
    code_dir.mkdir(parents=True, exist_ok=True)
    evaluator = None
    if not args.skip_eval:
        evaluator = Evaluator(
            dataset=dataset,
            dsl=args.dsl,
            dataset_config=dataset_config,
            run_root=str(output_dir),
            reference_cache_root=str(output_dir / "reference_cache"),
        )

    results_path = output_dir / "results.jsonl"
    worker_count = min(args.workers, len(selected))
    print(
        f"Generating {len(selected)} task(s) with {worker_count} worker(s)",
        flush=True,
    )
    had_failures = False
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            filename: executor.submit(
                generate_problem,
                codex=codex,
                model=args.model,
                dsl=args.dsl,
                problem=problems[filename],
                response_dir=response_dir,
                code_dir=code_dir,
                timeout=args.timeout,
            )
            for filename in selected
        }
        with results_path.open("a", encoding="utf-8") as results_file:
            for offset, filename in enumerate(selected):
                problem = problems[filename]
                record = {
                    "model": args.model,
                    "dsl": args.dsl,
                    "split": args.split,
                    "index": args.index + offset,
                    "filename": filename,
                }
                try:
                    thought, code, response_path, code_path = futures[filename].result()
                except Exception as exc:
                    record["generation_error"] = str(exc)
                    had_failures = True
                else:
                    record.update(
                        {
                            "thought": thought,
                            "response_path": str(response_path),
                            "code_path": str(code_path),
                        }
                    )
                    if evaluator is not None:
                        # Keep benchmark GPU work serialized and coordinator-only.
                        print(f"Evaluating {filename}", flush=True)
                        candidate = evaluator.evaluate_candidate(code, problem)
                        record["candidate"] = candidate.to_dict(include_code=False)
                results_file.write(json.dumps(record) + "\n")
                results_file.flush()
                print(json.dumps(record, indent=2), flush=True)

    return 1 if had_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
