#!/bin/bash
# diagnose-telegram-video.sh
# Quick diagnostic for "user sent video but agent sees nothing" cases
# Usage: bash ~/.hermes/skills/media/telegram-video-analysis/scripts/diagnose-telegram-video.sh
#
# Output: prints 4 sections to stdout:
#   1. Newest file in ~/.hermes/cache/videos/ (with mtime)
#   2. Recent telegram errors in gateway.log
#   3. Recent "inbound message" log entries (with attachment markers)
#   4. Verdict + recommended action

set -e

CACHE_DIR="$HOME/.hermes/cache/videos"
LOG_FILE="$HOME/.hermes/logs/gateway.log"
SIZE_LIMIT=20971520  # 20MB in bytes

echo "=== 1. Newest file in cache ==="
if [ -d "$CACHE_DIR" ]; then
  ls -lt "$CACHE_DIR" 2>/dev/null | head -3
  NEWEST=$(ls -t "$CACHE_DIR" 2>/dev/null | head -1)
  if [ -n "$NEWEST" ]; then
    NEWEST_PATH="$CACHE_DIR/$NEWEST"
    NEWEST_SIZE=$(stat -f%z "$NEWEST_PATH" 2>/dev/null || stat -c%s "$NEWEST_PATH" 2>/dev/null)
    NEWEST_MTIME=$(stat -f%m "$NEWEST_PATH" 2>/dev/null || stat -c%Y "$NEWEST_PATH" 2>/dev/null)
    NOW=$(date +%s)
    AGE_SEC=$((NOW - NEWEST_MTIME))
    AGE_MIN=$((AGE_SEC / 60))
    echo ""
    echo "Newest: $NEWEST"
    echo "  Size: $NEWEST_SIZE bytes ($(echo "scale=2; $NEWEST_SIZE/1048576" | bc) MB)"
    echo "  Age: ${AGE_MIN} minutes"
    if [ "$NEWEST_SIZE" -gt "$SIZE_LIMIT" ]; then
      echo "  ⚠️  EXCEEDS 20MB Telegram Bot API limit"
    fi
  fi
else
  echo "  Cache dir missing: $CACHE_DIR"
fi

echo ""
echo "=== 2. Recent telegram errors in gateway.log ==="
if [ -f "$LOG_FILE" ]; then
  grep -E "File is too big|telegram.error|BadRequest|getFile" "$LOG_FILE" 2>/dev/null | tail -10
else
  echo "  Log file missing: $LOG_FILE"
fi

echo ""
echo "=== 3. Recent inbound messages with attachments ==="
if [ -f "$LOG_FILE" ]; then
  grep -E "inbound message|attachment|video.*file_id" "$LOG_FILE" 2>/dev/null | tail -10
else
  echo "  Log file missing: $LOG_FILE"
fi

echo ""
echo "=== 4. Verdict + recommended action ==="
if [ -f "$LOG_FILE" ] && grep -q "File is too big" "$LOG_FILE" 2>/dev/null; then
  echo "  DIAGNOSIS: Video > 20MB (Telegram Bot API hard limit)"
  echo "  ACTION: Propose 2-3 solutions to user:"
  echo "    1. Compress video to <20MB (CapCut/HandBrake H.264 CRF 28)"
  echo "    2. Upload to Drive/YouTube → send link → download via yt-dlp/curl"
  echo "    3. (Not recommended) Try sending as document — still >20MB will fail"
elif [ -d "$CACHE_DIR" ] && [ -n "$NEWEST" ] && [ "$AGE_MIN" -lt 10 ]; then
  echo "  DIAGNOSIS: Video present in cache (${AGE_MIN} min old)"
  echo "  ACTION: Read and analyze via vision tool"
elif [ -d "$CACHE_DIR" ] && [ -n "$NEWEST" ] && [ "$AGE_MIN" -gt 60 ]; then
  echo "  DIAGNOSIS: No new video in cache (last one ${AGE_MIN} min old)"
  echo "  ACTION: Ask user to re-send, OR check upstream gateway connection"
else
  echo "  DIAGNOSIS: No video in cache, no error in log"
  echo "  ACTION: Check gateway connection + Telegram bot token validity"
fi

echo ""
echo "=== Done ==="
