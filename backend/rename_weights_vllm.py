#!/usr/bin/env python3
"""Rename model weights for vLLM compatibility - removes 'model.' prefix"""
from safetensors.torch import load_file, save_file
import glob
import os
import shutil
import json

MODEL_PATH = "/home/ec2-user/efs/vlm/experiments/phase3_qwen3_deepspeed/merged_model"
OUTPUT_PATH = "/home/ec2-user/efs/vlm/experiments/phase3_qwen3_deepspeed/merged_model_vllm"

print(f"Source: {MODEL_PATH}")
print(f"Output: {OUTPUT_PATH}")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# Process weight shards
shards = sorted(glob.glob(os.path.join(MODEL_PATH, "model-*.safetensors")))
print(f"\nFound {len(shards)} weight shards")

for shard in shards:
    print(f"Processing {os.path.basename(shard)}...")
    tensors = load_file(shard)

    # Rename keys: remove 'model.' prefix
    renamed = {}
    for key, value in tensors.items():
        if key.startswith("model."):
            new_key = key[6:]  # Remove 'model.' prefix
        else:
            new_key = key
        renamed[new_key] = value

    output_file = os.path.join(OUTPUT_PATH, os.path.basename(shard))
    save_file(renamed, output_file)
    print(f"  -> Saved {len(renamed)} tensors")

# Update model.safetensors.index.json
index_file = os.path.join(MODEL_PATH, "model.safetensors.index.json")
if os.path.exists(index_file):
    print("\nUpdating model.safetensors.index.json...")
    with open(index_file, 'r') as f:
        index = json.load(f)

    # Rename weight_map keys
    new_weight_map = {}
    for key, shard in index.get("weight_map", {}).items():
        if key.startswith("model."):
            new_key = key[6:]
        else:
            new_key = key
        new_weight_map[new_key] = shard

    index["weight_map"] = new_weight_map

    with open(os.path.join(OUTPUT_PATH, "model.safetensors.index.json"), 'w') as f:
        json.dump(index, f, indent=2)
    print("  -> Updated weight_map keys")

# Copy non-weight files
files_to_copy = [
    "config.json", "tokenizer.json", "tokenizer_config.json",
    "special_tokens_map.json", "preprocessor_config.json",
    "generation_config.json", "chat_template.jinja", "merges.txt",
    "added_tokens.json", "vocab.json"
]

print("\nCopying config files...")
for f in files_to_copy:
    src = os.path.join(MODEL_PATH, f)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(OUTPUT_PATH, f))
        print(f"  -> {f}")

print("\nDone! vLLM-compatible model saved to:", OUTPUT_PATH)
