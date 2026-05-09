#!/bin/bash
# TRÁHN QA Gate — Block delivery if script violations found
# Usage: ./tráhn-qa-gate.sh <script_file.md>
# Exit 0 = pass, Exit 1 = BLOCK delivery until fixed

set -e

SCRIPT_FILE="${1:-}"

if [ -z "$SCRIPT_FILE" ]; then
    # Auto-detect latest content creator output
    SCRIPT_FILE=$(ls -t ~/.hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)
fi

if [ ! -f "$SCRIPT_FILE" ]; then
    echo "❌ No script file found"
    exit 1
fi

echo "🔍 Scanning: $SCRIPT_FILE"

VIOLATIONS=$(grep -c "đỉnh nóc\|quất một phát\|đỉnh nóc kịch trần" "$SCRIPT_FILE" 2>/dev/null || echo "0")

if [ "$VIOLATIONS" -gt 0 ]; then
    echo "🚨 TRÁHN BLOCK: $VIOLATIONS violation(s) found"
    grep -n "đỉnh nóc\|quất một phát" "$SCRIPT_FILE"
    echo ""
    echo "FIX REQUIRED — edit file, re-run gate before delivery"
    echo "Common fixes:"
    echo "  sed -i '' 's/đỉnh nóc luôn/ngon vậy/g' \"$SCRIPT_FILE\""
    echo "  sed -i '' 's/đỉnh nóc kịch trần/hơi bị đỉnh/g' \"$SCRIPT_FILE\""
    echo "  sed -i '' 's/quất một phát/mua liền/g' \"$SCRIPT_FILE\""
    exit 1
fi

echo "✅ TRÁHN PASS — script clean, ready to deliver"
exit 0
