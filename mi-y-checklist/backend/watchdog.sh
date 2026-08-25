#!/bin/bash
# Restart FastAPI backend nếu không phản hồi
LOG=/tmp/miy-backend-watchdog.log
echo "[$(date)] Checking backend..." >> $LOG

# Check health
if ! curl -sS -m 5 http://127.0.0.1:7891/healthz > /dev/null 2>&1; then
    echo "[$(date)] Backend DOWN. Restarting..." >> $LOG

    # Kill any zombie
    pkill -f "mi-y-checklist/backend/.venv/bin/python main.py" 2>/dev/null
    sleep 1

    # Restart
    cd /Volumes/Storage-1/Hermes/mi-y-checklist/backend
    nohup .venv/bin/python main.py >> /tmp/miy-backend-watchdog.log 2>&1 &
    NEW_PID=$!
    echo "[$(date)] Restarted as PID $NEW_PID" >> $LOG
    sleep 3

    # Verify
    if curl -sS -m 5 http://127.0.0.1:7891/healthz > /dev/null 2>&1; then
        echo "[$(date)] ✅ Backend healthy again" >> $LOG
    else
        echo "[$(date)] ❌ Backend STILL DOWN after restart" >> $LOG
    fi
fi