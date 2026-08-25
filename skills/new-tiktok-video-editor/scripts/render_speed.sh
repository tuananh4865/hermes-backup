#!/bin/bash
# render_speed.sh — Apply speed 1.3x + scale to TikTok 1080×1920 30fps → final.mp4
# Usage: bash render_speed.sh <clip_id>

set -e

CLIP_ID="${1:-}"
if [ -z "$CLIP_ID" ]; then
    echo "Usage: $0 <clip_id>"
    exit 1
fi

EDIT="/Volumes/Storage-1/Pocket3/Hermes-Edit/$CLIP_ID"
WS="/Volumes/Storage-1/Hermes/Edit/$CLIP_ID"
PRE_SPEED="$EDIT/final_pre_speed.mp4"
FINAL="$EDIT/final.mp4"

if [ ! -f "$PRE_SPEED" ]; then
    echo "❌ Pre-speed not found: $PRE_SPEED"
    exit 1
fi

echo "═══ STEP 7b: SPEED 1.3x + SCALE 1080×1920 30fps ═══"
PRE_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$PRE_SPEED")
FINAL_DUR=$(python3 -c "print(round($PRE_DUR / 1.3, 2))")
echo "Pre-speed: ${PRE_DUR}s"
echo "Final (÷ 1.3): ${FINAL_DUR}s"
echo ""

PRE_SIZE=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$PRE_SPEED")
echo "Pre-speed dimension: $PRE_SIZE"
echo ""

# Render: speed 1.3x + scale to 1080×1920 30fps
echo "→ Rendering (speed 1.3x + scale 1080×1920 30fps + h264 yuv420p + aac)..."
ffmpeg -y -i "$PRE_SPEED" \
    -filter_complex \
        "[0:v]setpts=PTS/1.3,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,fps=30,format=yuv420p[v];
         [0:a]atempo=1.3,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a]" \
    -map "[v]" -map "[a]" \
    -c:v libx264 -preset medium -crf 18 \
    -profile:v high -level 4.0 \
    -c:a aac -b:a 192k \
    -movflags +faststart \
    "$FINAL" 2>&1 | tail -5
echo ""

if [ ! -f "$FINAL" ]; then
    echo "❌ Render failed"
    exit 1
fi

ACTUAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL")
SZ=$(stat -f%z "$FINAL")
SZ_MB=$(python3 -c "print(round($SZ/1024/1024, 2))")
echo "✅ Final: ${ACTUAL}s, ${SZ_MB}MB"
echo "  Path: $FINAL"
echo ""

# HARD GATE: verify TikTok spec (1080×1920 30fps)
echo "═══ Verify TikTok spec ═══"
python3 /Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/scripts/check_tiktok_spec.py "$FINAL"
VERIFY_EXIT=$?

if [ $VERIFY_EXIT -ne 0 ]; then
    echo "❌ Final output KHÔNG đạt TikTok spec — re-render cần thiết"
    exit 2
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Next: bash recheck.sh $CLIP_ID"
