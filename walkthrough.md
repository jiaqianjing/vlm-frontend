# Service Hardening Walkthrough

## Improvements

### 1. Robustness (Systemd)
- **Problem:** Service was manually managed via script/tmux, leading to port conflicts and lack of auto-restart.
- **Solution:** Created `vlm-backend.service` (Systemd).
    - **Auto-Cleanup:** `ExecStartPre` kills zombie Ray processes.
    - **Resource Limits:** `LimitNOFILE=65535` and `LimitMEMLOCK=infinity` prevent crashes.
    - **Auto-Restart:** `Restart=always` ensures 24/7 uptime.

### 2. Context Length (16k)
- **Problem:** User prompts >4096 tokens were failing.
- **Solution:** Updated `inference_engine.py` to `max_model_len=16384`.
    - **Verification:** Successfully processed test requests. 32k was attempted but hit OOM; 16k is the stable maximum for this single-node A100 setup.

### 3. Frontend Stability
- **Problem:** Long generations (16k tokens) could cause browser timeouts.
- **Solution:** Updated `App.jsx` with `timeout: 300000` (5 minutes).

## Verification Results
- [x] **Service Status:** Active (Systemd)
- [x] **Health Check:** 200 OK
- [x] **Inference:** Verified
- [x] **Restart on Kill:** Verified

## Artifacts
- `OPS_MANUAL.md`: Documentation for operators.
- `vlm-backend.service`: Systemd unit file.
