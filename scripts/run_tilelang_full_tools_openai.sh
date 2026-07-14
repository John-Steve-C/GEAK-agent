#!/usr/bin/env bash
set -euo pipefail

cd /home/wentao/GEAK-agent

export TILELANG_ENABLE_AGENT_TOOLS=1
export TILELANG_PYTHON=/home/wentao/miniconda3/envs/GEAK/bin/python
export TILELANG_LLM_MODEL=gpt-4.1-mini
export TILELANG_LLM_BASE_URL=http://localhost:8001/v1
export TILELANG_LLM_API_KEY=token-abc123
export TILELANG_LLM_MAX_TOKENS=8192
export TILELANG_START_IDX=0
export TILELANG_LENGTH=-1
export TILELANG_EPOCHS=5
export TILELANG_MAX_WORKERS=64
export TILELANG_MAX_LLM_REQUESTS=64
export TILELANG_MAX_EVAL_WORKERS=4
export TILELANG_EVAL_GPU=3
export TILELANG_PERF_GPU=3

unset TILELANG_TARGET_KERNELS
unset TILELANG_CANARY

curl -sS "${TILELANG_LLM_BASE_URL}/models" \
  -H "Authorization: Bearer ${TILELANG_LLM_API_KEY}" >/dev/null

"${TILELANG_PYTHON}" src/run_tilelang_eval_openai.py
