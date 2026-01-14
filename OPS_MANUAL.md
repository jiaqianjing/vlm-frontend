# VLM Backend Operations Manual

## Service Overview
The VLM Backend is managed by `systemd` as a robust, background service.

- **Service Name:** `vlm-backend`
- **Port:** `8000`
- **Logs:** Managed by `journalctl`
- **Control Script:** `backend/service_manager.sh`

---

## 🚀 Service Management

You can use the helper script `backend/service_manager.sh` or standard `systemctl` commands.

### Using the Helper Script
```bash
./backend/service_manager.sh start
./backend/service_manager.sh stop
./backend/service_manager.sh restart
./backend/service_manager.sh status
./backend/service_manager.sh logs
```

### Standard Systemd Commands
#### Check Status
Verify if the service is active and running:
```bash
sudo systemctl status vlm-backend
```

### Start the Service
```bash
sudo systemctl start vlm-backend
```

### Stop the Service
```bash
sudo systemctl stop vlm-backend
```

### Restart (e.g., after code changes)
```bash
sudo systemctl restart vlm-backend
```

---

## 📜 Logs & Monitoring

### View Real-time Logs (Tail)
To follow the latest logs (like `tail -f`):
```bash
sudo journalctl -u vlm-backend -f
```

### View Recent Logs
View the last 50 log lines:
```bash
sudo journalctl -u vlm-backend -n 50 --no-pager
```

### View Logs for a Specific Boot
If you need to debug a previous crash:
```bash
sudo journalctl -u vlm-backend -b
```

---

## 🛠️ Deployment & Maintenance

### Deploying Code Changes
1.  **Pull latest code:**
    ```bash
    cd /home/ec2-user/fsx/vlm-frontend
    git pull
    ```
2.  **Restart the service:**
    ```bash
    sudo systemctl restart vlm-backend
    ```
3.  **Verify Health:**
    ```bash
    curl http://localhost:8000/health
    ```

### Troubleshooting

#### 1. Service fails to start (OOM / Connection Refused)
The model requires significant GPU memory (approx 62GB).
The service is configured with a **Systematic Cleanup** script (`cleanup_service.sh`) that runs automatically before every start.
- It force-kills all Ray processes (`pkill -9 ray::`).
- It clears port 8000.
- It waits for resource release.

If issues persist:
- **Check Logs:** `sudo journalctl -u vlm-backend -n 50 --no-pager`
- **Check GPU Usage:** `nvidia-smi`

#### 2. Port 8000 is occupied
If the service fails with "Address already in use":
1.  Find the process: `lsof -i :8000`
2.  Kill it: `kill -9 <PID>`
3.  Restart service: `sudo systemctl restart vlm-backend`

---

## ⚙️ Configuration
- **Unit File:** `/etc/systemd/system/vlm-backend.service`
- **Working Directory:** `/home/ec2-user/fsx/vlm-frontend/backend`
- **Environment:**
    - `CUDA_VISIBLE_DEVICES`: 0-7 (All 8 A100 GPUs)
    - `max_model_len`: 16384 (Hardcoded in `inference_engine.py`)
