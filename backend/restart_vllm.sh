#!/bin/bash
# Restart VLM backend (vLLM version)

set -e

BACKEND_DIR="/home/ec2-user/fsx/vlm-frontend/backend"
cd "$BACKEND_DIR"

echo "=== Stopping existing VLM backend ==="
# Kill the specific vlm process
pkill -f "uvicorn main_vllm:app" || echo "No existing process found"

# Wait for process to fully exit and release GPU memory
echo "Waiting for shutdown..."
sleep 10

echo "=== Starting vLLM backend on port 8000 ==="
# Using all 8 GPUs
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

# Start with nohup
nohup python3 -m uvicorn main_vllm:app --host 0.0.0.0 --port 8000 > /tmp/vlm_vllm.log 2>&1 &

echo "=== Waiting for service to start (this may take 30-60s for vLLM to initialize) ==="
sleep 10

# Check if it's running
for i in {1..60}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "Service started successfully!"
        curl -s http://localhost:8000/health | python3 -m json.tool
        exit 0
    fi
    echo "Waiting... ($i/60)"
    sleep 5
done

echo "ERROR: Service failed to start. Check /tmp/vlm_vllm.log"
tail -50 /tmp/vlm_vllm.log
exit 1
