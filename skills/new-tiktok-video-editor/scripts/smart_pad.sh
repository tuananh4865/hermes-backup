# smart_pad.sh — Pad KEEP ranges to align with word boundaries
# Usage: bash smart_pad.sh <clip_id>

set -e

CLIP_ID="${1:-}"
if [ -z "$CLIP_ID" ]; then
    echo "Usage: $0 <clip_id>"
    exit 1
fi

WS="/Volumes/Storage-1/Hermes/Edit/$CLIP_ID"

# Inputs
WHISPER="$WS/work/audio.json"
ORIG="$WS/work/keep_plan.json"
OUTPUT="$WS/work/keep_plan.json"

# Backup
if [ -f "$OUTPUT" ]; then
    cp "$OUTPUT" "$WS/work/keep_plan.v1.json"
fi

echo "═══ SMART PAD — word-align KEEP ranges ═══"

python3 /Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/scripts/smart_keep_plan.py \
    "$WHISPER" "$ORIG" --output "$OUTPUT"
