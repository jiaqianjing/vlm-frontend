#!/usr/bin/env python3
"""vLLM with Qwen3VL - Final Test"""
import os
import sys

# Environment setup
os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import multiprocessing
try:
    multiprocessing.set_start_method("spawn", force=True)
except RuntimeError:
    pass

import time
print(f"[{time.strftime('%H:%M:%S')}] Starting vLLM Qwen3VL test...")

from vllm import LLM, SamplingParams

MERGED_MODEL_PATH = "/home/ec2-user/efs/vlm/experiments/phase3_qwen3_deepspeed/merged_model"

def main():
    print(f"[{time.strftime('%H:%M:%S')}] Initializing vLLM engine...")
    start = time.time()

    try:
        llm = LLM(
            model=MERGED_MODEL_PATH,
            tensor_parallel_size=8,
            gpu_memory_utilization=0.9,
            dtype="bfloat16",
            trust_remote_code=True,  # Use remote code for Qwen3VL
            enforce_eager=False,  # Enable CUDA graphs
            max_model_len=4096,
            limit_mm_per_prompt={"image": 1},
        )
        load_time = time.time() - start
        print(f"[{time.strftime('%H:%M:%S')}] Model loaded in {load_time:.2f}s")

        # Test text generation
        print(f"[{time.strftime('%H:%M:%S')}] Testing text generation...")
        t0 = time.time()
        output = llm.generate("Hello, how are you?", SamplingParams(max_tokens=50, temperature=0.1))
        gen_time = time.time() - t0
        print(f"[{time.strftime('%H:%M:%S')}] Generation time: {gen_time:.2f}s")
        print(f"Output: {output[0].outputs[0].text}")

        return 0

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
