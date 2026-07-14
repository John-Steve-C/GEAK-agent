#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python main_optimagent_tritonbench.py configs/tritonbench_optimagent_train_split_config.yaml
python main_optimagent_tritonbench.py configs/tritonbench_optimagent_test_split_config.yaml
