#!/bin/bash
# recheck.sh — Re-transcript final.mp4 → verify
# Usage: bash recheck.sh <clip_id>
#
# So sánh recheck.json với keep_plan KEEP ranges:
# - Có filler cũ sót? → FAIL
# - Có câu treo? → FAIL
# - Có pricing bị sót? → FAIL
# - Duration drift >5s? → FAIL
# - 100% clean → PASS

# KHÔNG dùng 'set -e' vì verify_recheck.py cần exit 1 để signal FAIL

CLIP_ID="${1:-}"
if [ -z "$CLIP_ID" ]; then
    echo "Usage: $0 <clip_id>"
    exit 1
fi

WS="/Volumes/Storage-1/Hermes/Edit/$CLIP_ID"
EDIT="/Volumes/Storage-1/Pocket3/Hermes-Edit/$CLIP_ID"
FINAL="$EDIT/final.mp4"
WORK="$WS/work"

if [ ! -f "$FINAL" ]; then
    echo "❌ Final not found: $FINAL"
    exit 1
fi

echo "═══ STEP 8: RE-TRANSCRIPT VERIFY ═══"

# Extract audio from final
AUDIO_TMP="/tmp/${CLIP_ID}_final_audio.wav"
ffmpeg -y -i "$FINAL" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$AUDIO_TMP" 2>&1 | tail -2

# Re-transcript
mkdir -p "$WORK/recheck_dir"
~/.hermes/scripts/whisper-transcribe "$AUDIO_TMP" "$WORK/recheck_dir" 2>&1 | tail -5

# Move recheck.json to standard location
RECHECK_JSON="$WORK/recheck_dir/$(basename $AUDIO_TMP | sed 's/\.[^.]*$//').json"
if [ ! -f "$RECHECK_JSON" ]; then
    ALTERNATE=$(ls "$WORK/recheck_dir"/*.json 2>/dev/null | head -1)
    if [ -n "$ALTERNATE" ]; then
        RECHECK_JSON="$ALTERNATE"
    fi
fi

if [ ! -f "$RECHECK_JSON" ]; then
    echo "❌ Re-transcript failed"
    exit 1
fi

echo ""
echo "═══ VERIFY ═══"
echo "Recheck JSON: $RECHECK_JSON"
echo ""

# Run verify (Python exit code signal FAIL/PASS)
# Capture exit code from verify_recheck.py (NOT from tee)
set +e
python3 /Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/scripts/verify_recheck.py \
    "$WORK/keep_plan.json" "$RECHECK_JSON" 2>&1 > /tmp/recheck_report.txt
VERIFY_EXIT=$?
set -e

cat /tmp/recheck_report.txt
echo ""
if [ $VERIFY_EXIT -eq 0 ]; then
    echo "✅ VERIFY PASS — Ready to ship"
    echo "Next: bash ship.sh $CLIP_ID"
    exit 0
else
    echo "❌ VERIFY FAIL — Quay lại step 6 (chọn lại content)"
    echo "Report: /tmp/recheck_report.txt"
    echo "Exit code: $VERIFY_EXIT"
    exit $VERIFY_EXIT
fi
