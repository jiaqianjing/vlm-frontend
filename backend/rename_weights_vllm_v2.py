#!/usr/bin/env python3
"""Rename model weights for vLLM compatibility v2
Based on error analysis:
- model.language_model.xxx -> model.xxx
- model.visual.xxx -> visual.xxx
- model.lm_head.weight -> lm_head.weight
"""
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

def rename_key(key):
    """Rename weight keys for vLLM Qwen3VL compatibility"""
    # model.language_model.xxx -> model.xxx
    if key.startswith("model.language_model."):
        return "model." + key[21:]  # len("model.language_model.") = 21

    # model.visual.xxx -> visual.xxx
    if key.startswith("model.visual."):
        return key[6:]  # Remove 'model.' prefix

    # model.lm_head.weight -> lm_head.weight
    if key.startswith("model.lm_head"):
        return key[6:]  # Remove 'model.' prefix

    return key

# Process weight shards
shards = sorted(glob.glob(os.path.join(MODEL_PATH, "model-*.safetensors")))
print(f"\nFound {len(shards)} weight shards")

# First pass: check what we're renaming
print("\nSample renames:")
first_shard = load_file(shards[0])
sample_keys = list(first_shard.keys())[:10]
for key in sample_keys:
    new_key = rename_key(key)
    if key != new_key:
        print(f"  {key} -> {new_key}")
del first_shard

# Process all shards
for shard in shards:
    print(f"\nProcessing {os.path.basename(shard)}...")
    tensors = load_file(shard)

    renamed = {}
    for key, value in tensors.items():
        new_key = rename_key(key)
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

    new_weight_map = {}
    for key, shard in index.get("weight_map", {}).items():
        new_key = rename_key(key)
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
