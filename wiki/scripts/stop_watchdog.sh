#!/bin/bash
WIKI_DIR="$HOME/wiki"
PID_FILE="$WIKI_DIR/scripts/watchdog.pid"
[ -f "$PID_FILE" ] && PID=$(cat "$PID_FILE") && kill -0 "$PID" 2>/dev/null && kill "$PID"
rm -f "$PID_FILE"
echo "Watchdog stopped"
