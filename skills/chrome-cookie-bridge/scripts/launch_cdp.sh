#!/bin/bash
# Launch Chrome CDP with debug port + empty profile
# Usage: ./launch_cdp.sh [profile_dir] [port]
# Default: /tmp/chrome-cdp 9222

PROFILE_DIR="${1:-/tmp/chrome-cdp}"
PORT="${2:-9222}"

mkdir -p "$PROFILE_DIR"

osascript <<EOF
do shell script "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=$PORT --user-data-dir=$PROFILE_DIR --no-first-run --no-default-browser-check > /tmp/chrome-cdp.log 2>&1 &"
EOF

sleep 5

# Verify
if curl -s -m 3 "http://localhost:$PORT/json/version" > /dev/null; then
    echo "✅ Chrome CDP ready on port $PORT"
    echo "Profile: $PROFILE_DIR"
    curl -s -m 3 "http://localhost:$PORT/json/version" | python3 -c "
import json, sys
v = json.load(sys.stdin)
print(f'Browser: {v["product"]}')
print(f'WS: {v["webSocketDebuggerUrl"]}')
"
else
    echo "❌ Chrome CDP failed to start"
    tail -20 /tmp/chrome-cdp.log
fi
