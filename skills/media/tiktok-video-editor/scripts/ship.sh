#!/bin/bash
# ship.sh — Copy final.mp4 ra Pocket3/Hermes-Edit root với filename convention
# Usage: bash ship.sh <clip_id> [version=N] [duration=NNs] [sp_name]

set -e

CLIP_ID="${1:-}"
VERSION="${2:-V1}"
DURATION="${3:-}"
SP_NAME="${4:-AUTO}"

if [ -z "$CLIP_ID" ]; then
    echo "Usage: $0 <clip_id> [version=V1] [duration=NNs] [sp_name=AUTO]"
    echo "  clip_id: 4-digit (e.g. 0036)"
    echo "  version: V1, V2, ... (default V1)"
    echo "  duration: NNs from clip duration (default = auto detect)"
    echo "  sp_name: product/service name (default AUTO)"
    exit 1
fi

WS_POCKET="/Volumes/Storage-1/Pocket3/Hermes-Edit/$CLIP_ID"
FINAL="$WS_POCKET/final.mp4"
SHIP_DIR="/Volumes/Storage-1/Pocket3/Hermes-Edit"

if [ ! -f "$FINAL" ]; then
    echo "❌ Final not found: $FINAL"
    exit 1
fi

# Auto-detect duration nếu không truyền
if [ -z "$DURATION" ]; then
    DUR_DECIMAL=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL")
    DURATION=$(python3 -c "print(int(round(float('$DUR_DECIMAL'))))")s
fi

# Ship file
SHIP_FILE="$SHIP_DIR/clip_${CLIP_ID}_${VERSION}_${DURATION}_FINAL_${SP_NAME}.mp4"
echo "═══ STEP 9: SHIP ═══"
echo "Source: $FINAL"
echo "Ship:   $SHIP_FILE"
echo ""

cp "$FINAL" "$SHIP_FILE"

if [ ! -f "$SHIP_FILE" ]; then
    echo "❌ Ship failed"
    exit 1
fi

# Verify
SZ=$(stat -f%z "$SHIP_FILE")
SZ_MB=$(python3 -c "print(round($SZ/1024/1024, 2))")
echo "✅ SHIPPED: $SZ_MB MB"
echo ""
echo "📂 Final paths:"
echo "  Pocket3 project: $WS_POCKET/final.mp4"
echo "  Pocket3 ship:    $SHIP_FILE"
echo ""
echo "🎬 Anh xem iPhone xem clip được rồi!"
