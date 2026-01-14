#!/bin/bash
# Wrapper script for VLM Backend Service (Systemd)

echo "=== VLM Service Manager (Systemd) ==="

if ! command -v systemctl &> /dev/null; then
    echo "Error: systemctl not found."
    exit 1
fi

USAGE="Usage: $0 {start|stop|restart|status|logs}"

if [ -z "$1" ]; then
    echo "$USAGE"
    exit 1
fi

case "$1" in
    start)
        echo "Starting vlm-backend..."
        sudo systemctl start vlm-backend
        ;;
    stop)
        echo "Stopping vlm-backend..."
        sudo systemctl stop vlm-backend
        ;;
    restart)
        echo "Restarting vlm-backend..."
        sudo systemctl restart vlm-backend
        ;;
    status)
        sudo systemctl status vlm-backend --no-pager
        ;;
    logs)
        sudo journalctl -u vlm-backend -f
        ;;
    *)
        echo "$USAGE"
        exit 1
        ;;
esac
