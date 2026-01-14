#!/bin/bash
# cleanup_service.sh
# robust cleanup trigger for systemd ExecStartPre

echo "[Cleanup] Starting VLM service cleanup..."

# 1. Stop Ray gracefully if possible
/home/ec2-user/miniconda3/bin/ray stop --force || true

# 2. Aggressive kill of any lingering Ray processes (Zombies)
# This addresses the "RpcError" and "EngineCore" initialization failures
# caused by orphaned workers holding GPU memory or ports.
echo "[Cleanup] Force killing lingering Ray processes..."
pkill -9 -f "ray::" || true
pkill -9 -f "raylet" || true
pkill -9 -f "gcs_server" || true

# 3. Ensure Port 8000 is free
fuser -k 8000/tcp || true

# 4. Wait for OS to reclaim resources
echo "[Cleanup] Waiting for resource release..."
sleep 3

echo "[Cleanup] System is clean and ready for start."
