#!/usr/bin/env bash
# Test verify_voice_script.py trên 3 script V4 ULANZI MA66.
# Pass = output shows "✅ 8/8 passed", "ready to generate voice!"

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$SKILL_DIR/scripts/verify_voice_script.py"

V4_DIR="/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/scripts"

PASS=0
FAIL=0

for f in ulanzi-ma66-tripod-pocket-3-natural-voice.md; do
    echo "=== Testing $f ==="
    if python3 "$SCRIPT" "$V4_DIR/$f" > /tmp/verify-result.txt 2>&1; then
        echo "✅ PASS"
        cat /tmp/verify-result.txt | grep -E "passed|Summary"
        PASS=$((PASS+1))
    else
        echo "❌ FAIL"
        cat /tmp/verify-result.txt
        FAIL=$((FAIL+1))
    fi
    echo ""
done

echo "=== Test summary: $PASS passed, $FAIL failed ==="
exit $FAIL