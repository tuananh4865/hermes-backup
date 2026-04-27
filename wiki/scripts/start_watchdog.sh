#!/bin/bash
# Start Wiki Watchdog Daemon
WIKI_DIR="$HOME/wiki"
PID_FILE="$WIKI_DIR/scripts/watchdog.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Watchdog already running (PID: $PID)"
        exit 0
    fi
    rm -f "$PID_FILE"
fi

cd "$WIKI_DIR"
nohup python3 "$WIKI_DIR/scripts/watchdog_daemon.py" --daemon > "$WIKI_DIR/scripts/watchdog.out" 2>&1 &
PID=$!
echo "Started PID: $PID"
echo "$PID" > "$PID_FILE"
sleep 2
if kill -0 "$PID" 2>/dev/null; then
    echo "Watchdog running"
else
    echo "Check watchdog.out"
    cat "$WIKI_DIR/scripts/watchdog.out"
fi
