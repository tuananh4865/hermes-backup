#!/usr/bin/env bash
# Test Hermes File Log Hook end-to-end
# Run this AFTER anh restart gateway: bash ~/.hermes/restart-hermes-gateway.sh
#
# What this test does:
# 1. Capture current state of log file (count entries)
# 2. Wait for new session (anh gửi 1 message cho em)
# 3. Em write_file hoặc patch 1 file
# 4. Check log file có entry mới không

set -e

LOG_DIR="/Volumes/Storage-1/Hermes/logs/daily"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/$TODAY.jsonl"

echo "============================================"
echo "🧪 TEST HERMES FILE LOG HOOK"
echo "============================================"
echo ""
echo "📂 Log file: $LOG_FILE"
echo ""

# Step 1: Count current entries
if [[ -f "$LOG_FILE" ]]; then
    BEFORE=$(wc -l < "$LOG_FILE")
    echo "📊 Current log entries: $BEFORE"
else
    echo "📊 Log file not exist yet (today's first run)"
    BEFORE=0
fi

echo ""
echo "🔍 Step 2: INSTRUCTIONS FOR ANH"
echo "   1. Gateway restart: bash ~/.hermes/restart-hermes-gateway.sh"
echo "   2. Wait 30s for gateway fully up"
echo "   3. Start new Telegram session: gửi 'test log hook' cho em"
echo "   4. Em sẽ thấy file mới tạo → hook fires → log entry append"
echo "   5. Re-run this script to verify"
echo ""

# Step 3: Check current state
echo "============================================"
echo "📊 CURRENT LOG STATE"
echo "============================================"
if [[ -f "$LOG_FILE" ]]; then
    echo ""
    echo "Last 5 entries:"
    tail -5 "$LOG_FILE" | python3 -c "
import sys, json
for line in sys.stdin:
    if line.strip():
        e = json.loads(line)
        print(f\"  [{e['action']}] {e['file']}\")
        print(f\"    Reason: {e['reason']}\")"
    echo ""
    AFTER=$(wc -l < "$LOG_FILE")
    NEW=$((AFTER - BEFORE))
    echo "📈 New entries since you ran this script: $NEW"
    if [[ $NEW -gt 0 ]]; then
        echo "✅ HOOK IS WORKING!"
    else
        echo "⏳ Waiting for new tool calls... (run this script again after a session)"
    fi
else
    echo "❌ Log file not created yet (today)"
fi