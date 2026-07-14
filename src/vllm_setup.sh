export CUDA_VISIBLE_DEVICES=0,1

# reference:
# https://docs.vllm.ai/en/latest/serving/distributed_serving.html

# model_path=/home/wentao/models/codellama/CodeLlama-7b-Python-hf
# model_path=/home/wentao/sft_model/results/deepseek_coder_V2_lite_base

# for 10 epoch
# model_path=/home/wentao/models/Qwen/Qwen2.5-Coder-7B
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-29
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-58
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-87
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-116
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-145
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-174
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-203
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-232
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-261
# model_path=/home/wentao/sft_model/results/Qwen2.5-Coder-7B_new/checkpoint-290

# llama2-7b
# model_path=/data/wentao/models/llama-2/Llama-2-7b-hf
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-29
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-58
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-87
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-116
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-145
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-174
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-203
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-232
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-261
# model_path=/home/wentao/sft_model/results/llama2-7b_10epoch/checkpoint-290

# llama3-8b
# model_path=/data/wentao/models/llama-3/Meta-Llama-3-8B
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-29
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-58
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-87
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-116
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-145
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-174
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-203
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-232
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-261
# model_path=/home/wentao/sft_model/results/Llama-3-8B_10epoch/checkpoint-290

# new codellama model
# model_path=/home/wentao/models/codellama/CodeLlama-7b-hf
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-29
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-58
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-87
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-116
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-145
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-174
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-203
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-232
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-261
# model_path=/home/wentao/sft_model/results/CodeLlama-7b-hf_10epoch/checkpoint-290

# model_path=/shared/models/hf/Qwen2.5-Coder-7B
# model_path=/shared/models/hf/Llama-2-7b-chat-hf


# model_path=/shared/models/hf/AutoTriton
# model_path=/shared/models/hf/KernelLLM
# model_path=/shared/models/hf/Qwen3-Coder-30B-A3B-Instruct
# model_path=/shared/models/hf/Qwen3.6-35B-A3B
# model_path=/shared/models/hf/Qwen3-32B

# model_path=/shared/models/hf/Qwen3.5-27B
model_path=/shared/models/hf/Qwen3.5-35B-A3B



echo $model_path
vllm serve $model_path --dtype bfloat16 --api-key token-abc123 --port 8001 --trust-remote-code \
    --tensor-parallel-size 2 \
    --gpu-memory-utilization 0.9 \
    --enable-prefix-caching \
    --reasoning-parser qwen3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder
    # --max-model-len 65536 \
    # --language-model-only
    # --pipeline-parallel-size 4

# --max_model_len 22208
