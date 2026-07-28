#!/usr/bin/env bash
set -euo pipefail

# Run the complete matrix from the selected configuration:
#   VLLM_API_KEY=EMPTY scripts/run_experiment.sh vllm
#   OPENAI_API_KEY=... scripts/run_experiment.sh openai
#
# Existing runner flags are forwarded:
#   scripts/run_experiment.sh vllm --dry-run
#   scripts/run_experiment.sh vllm --pilot
#   scripts/run_experiment.sh vllm --resume
#   MODEL_WORKERS=16 scripts/run_experiment.sh vllm --resume

# python src/run_experiment.py \
#   --config src/configs/main_experiment_openai.yaml \
#   --only dsl=tilelang \
#   --only workflow=fixed \
#   --only memory=tree \
#   --only seed=0 \

python src/run_experiment.py --config src/configs/main_experiment_openai.yaml --only workflow=fixed --only seed=0

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BACKEND="${1:-vllm}"
if [[ $# -gt 0 ]]; then
  shift
fi

case "$BACKEND" in
  vllm)
    CONFIG="src/configs/main_experiment.yaml"
    ;;
  openai)
    CONFIG="src/configs/main_experiment_openai.yaml"
    ;;
  *)
    echo "Usage: $0 {vllm|openai} [run_experiment.py options]" >&2
    exit 2
    ;;
esac

COMMAND=(python src/run_experiment.py --config "$CONFIG")
if [[ -n "${MODEL_WORKERS:-}" ]]; then
  COMMAND+=(--model-workers "$MODEL_WORKERS")
fi

exec "${COMMAND[@]}" "$@"
