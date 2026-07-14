#!/usr/bin/env bash
set -euo pipefail

# Optional one-time install path. Network access is required for this step:
#   conda create -n sglang python=3.11 -y
#   conda activate sglang
#   uv pip install "sglang[all]"

export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0,1,2,3}
model_path=${MODEL_PATH:-/shared/models/hf/Qwen3.6-35B-A3B}
port=${PORT:-8002}
tp_size=${TP_SIZE:-4}
context_length=${CONTEXT_LENGTH:-65536}
mem_fraction_static=${MEM_FRACTION_STATIC:-0.8}

echo "$model_path"
sglang serve \
    --model-path "$model_path" \
    --port "$port" \
    --tp-size "$tp_size" \
    --mem-fraction-static "$mem_fraction_static" \
    --context-length "$context_length" \
    --reasoning-parser qwen3 \
    --language-only
# Add this only when using tool/function calling:
#   --tool-call-parser qwen3_coder
