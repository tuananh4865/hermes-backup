#!/bin/bash
# init_project.sh — Tạo folder structure cho 1 video project
# Usage: bash init_project.sh <clip_id> /path/to/raw.mp4
#
# Folder structure:
#   /Volumes/Storage-1/Hermes/Edit/<clip_id>/{source,work,notes}
#   /Volumes/Storage-1/Pocket3/Hermes-Edit/<clip_id>/

set -e

CLIP_ID="${1:-}"
RAW_PATH="${2:-}"

if [ -z "$CLIP_ID" ] || [ -z "$RAW_PATH" ]; then
    echo "Usage: $0 <clip_id> /path/to/raw.mp4"
    echo "  clip_id  = 4-digit (e.g. 0036)"
    echo "  raw_path = /path/to/source.mp4"
    exit 1
fi

if [ ! -f "$RAW_PATH" ]; then
    echo "❌ Source file not found: $RAW_PATH"
    exit 1
fi

WS_HERMES="/Volumes/Storage-1/Hermes/Edit/$CLIP_ID"
WS_POCKET="/Volumes/Storage-1/Pocket3/Hermes-Edit/$CLIP_ID"

echo "═══ INIT PROJECT — clip_$CLIP_ID ═══"

# Create Hermes folder structure (work artifacts)
for sub in source work notes; do
    mkdir -p "$WS_HERMES/$sub"
    echo "  📁 $WS_HERMES/$sub/"
done

# Create Pocket3 folder structure (output)
mkdir -p "$WS_POCKET"
echo "  📁 $WS_POCKET/  (output dir)"

# Copy source (không move — giữ nguyên ở Footages)
cp "$RAW_PATH" "$WS_HERMES/source/raw.mp4"
echo ""
echo "✅ Source copied: $WS_HERMES/source/raw.mp4"
ls -la "$WS_HERMES/source/raw.mp4"
echo ""

echo "═══ Folder structure ═══"
find "$WS_HERMES" -type d -maxdepth 2 | sort
echo "  $WS_POCKET (output)"
echo ""
echo "Next: bash transcribe.sh $CLIP_ID"
