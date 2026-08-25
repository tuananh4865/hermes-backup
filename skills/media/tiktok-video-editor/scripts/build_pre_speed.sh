#!/bin/bash
# build_pre_speed.sh — Concat KEEP ranges HARD CUT → final_pre_speed.mp4
# Usage: bash build_pre_speed.sh <clip_id>
#
# Concat segments bằng filter_complex + trim/setpts/asetpts.
# KHÔNG dùng fade (cả video lẫn audio) — HARD CUT giữa các KEEP ranges.
# Compatible với macOS bash 3.2 (KHÔNG dùng mapfile).

set -e

CLIP_ID="${1:-}"
if [ -z "$CLIP_ID" ]; then
    echo "Usage: $0 <clip_id>"
    exit 1
fi

WS="/Volumes/Storage-1/Hermes/Edit/$CLIP_ID"
EDIT="/Volumes/Storage-1/Pocket3/Hermes-Edit/$CLIP_ID"
SOURCE="$WS/source/raw.mp4"
WORK="$WS/work"

mkdir -p "$EDIT"

KEEP_PLAN="$WORK/keep_plan.json"

if [ ! -f "$KEEP_PLAN" ]; then
    echo "❌ keep_plan.json not found: $KEEP_PLAN"
    exit 1
fi

echo "═══ STEP 7a: BUILD PRE-SPEED (concat HARD CUT) ═══"

RANGES_FILE=$(mktemp)
python3 <<PYEOF > "$RANGES_FILE"
import json
with open("$KEEP_PLAN") as f: p = json.load(f)
ranges = []
for r in p.get("ranges", []):
    if r.get("action") == "KEEP":
        s = r.get("start_padded", r.get("start"))
        e = r.get("end_padded", r.get("end"))
        ranges.append([float(s), float(e)])

# PITFALL #91: trim overlap với keep tiếp theo (audio + visual lặp nếu không trim)
trimmed = 0
for i in range(len(ranges) - 1):
    if ranges[i][1] > ranges[i+1][0]:
        overlap = ranges[i][1] - ranges[i+1][0]
        ranges[i][1] = ranges[i+1][0]
        trimmed += overlap

if trimmed > 0.05:
    print(f"# WARNING: PITFALL #91 — trimmed {trimmed:.3f}s overlap (defensive auto-trim)", file=__import__('sys').stderr)
print(f"TOTAL:{len(ranges)}")
for s, e in ranges:
    print(f"{s:.3f} {e:.3f}")
PYEOF

NUM_RANGES=$(grep "^TOTAL:" "$RANGES_FILE" | cut -d: -f2)
if [ -z "$NUM_RANGES" ] || [ "$NUM_RANGES" -eq 0 ]; then
    rm -f "$RANGES_FILE"
    echo "❌ No KEEP ranges in keep_plan"
    exit 1
fi
echo "Number of segments: $NUM_RANGES"
echo ""

i=0
FILTER_PARTS=""
while IFS=' ' read -r line; do
    if [ -z "$line" ] || [[ "$line" == TOTAL:* ]]; then continue; fi
    start=$(echo "$line" | awk '{print $1}')
    end=$(echo "$line" | awk '{print $2}')

    FILTER_PARTS="${FILTER_PARTS}[0:v]trim=start=${start}:end=${end},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v${i}];"
    FILTER_PARTS="${FILTER_PARTS}[0:a]atrim=start=${start}:end=${end},asetpts=PTS-STARTPTS,aresample=44100[a${i}];"
    i=$((i+1))
done < "$RANGES_FILE"

rm -f "$RANGES_FILE"

FILTER_JOIN=""
for x in $(seq 0 $((NUM_RANGES - 1))); do
    FILTER_JOIN="${FILTER_JOIN}[v${x}][a${x}]"
done

FILTER="${FILTER_PARTS}${FILTER_JOIN}concat=n=${NUM_RANGES}:v=1:a=1[outv][outa]"

PRE_SPEED="$EDIT/final_pre_speed.mp4"
echo "→ Rendering pre-speed (HARD CUT)..."
ffmpeg -y -i "$SOURCE" \
    -filter_complex "$FILTER" \
    -map "[outv]" -map "[outa]" \
    -c:v libx264 -preset medium -crf 18 \
    -c:a aac -b:a 192k \
    "$PRE_SPEED" 2>&1 | tail -3
echo ""

if [ ! -f "$PRE_SPEED" ]; then
    echo "❌ Pre-speed render failed"
    exit 1
fi

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$PRE_SPEED")
SZ=$(stat -f%z "$PRE_SPEED")
SZ_MB=$(python3 -c "print(round($SZ/1024/1024, 2))")
echo "✅ Pre-speed: ${DUR}s, ${SZ_MB}MB"
echo "  Path: $PRE_SPEED"
echo ""
echo "Next: bash render_speed.sh $CLIP_ID"
