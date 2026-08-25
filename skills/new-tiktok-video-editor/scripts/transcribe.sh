#!/bin/bash
# transcribe.sh — Whisper large-v3 word-by-word cho <clip_id>
# Output: <WS>/work/{transcript.json,transcript.txt,transcript.md}

set -e

CLIP_ID="${1:-}"
if [ -z "$CLIP_ID" ]; then
    echo "Usage: $0 <clip_id>"
    exit 1
fi

WS="/Volumes/Storage-1/Hermes/Edit/$CLIP_ID"
SOURCE="$WS/source/raw.mp4"
WORK="$WS/work"

if [ ! -f "$SOURCE" ]; then
    echo "❌ Source not found: $SOURCE"
    echo "   Run init_project.sh first"
    exit 1
fi

mkdir -p "$WORK"

echo "═══ STEP 2: TRANSCRIPT — Whisper large-v3 word-by-word ═══"
echo "Source: $SOURCE"
echo ""

# Extract audio 16k mono PCM (Whisper spec)
AUDIO="$WORK/audio.wav"
if [ ! -f "$AUDIO" ] || [ "$SOURCE" -nt "$AUDIO" ]; then
    echo "→ Extracting audio 16k mono PCM..."
    ffmpeg -y -i "$SOURCE" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$AUDIO" 2>&1 | tail -3
else
    echo "→ Audio extracted (cached)"
fi

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUDIO")
echo "  Duration: $DUR seconds"
echo ""

# Whisper large-v3 word-by-word via wrapper (auto-fallback to medium if loop)
echo "→ Running Whisper large-v3 (word-by-word timestamps)..."
~/.hermes/scripts/whisper-transcribe "$AUDIO" "$WORK" 2>&1 | tail -8
echo ""

# Find output
JSON=$(ls "$WORK"/*.json 2>/dev/null | head -1)
TXT=$(ls "$WORK"/*.txt 2>/dev/null | head -1)

if [ -z "$JSON" ]; then
    echo "❌ Whisper output not found"
    exit 1
fi

# Generate transcript.md (paragraph format for AI reading)
python3 /Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/scripts/generate_transcript_md.py \
    "$JSON" "$WORK/transcript.md" 2>&1 | tail -3

echo ""
echo "═══ TRANSCRIPT READY ═══"
echo "  Raw JSON: $JSON"
echo "  Text:     $TXT"
echo "  Markdown: $WORK/transcript.md"
echo ""
echo "Next step: AI đọc transcript.md + quyết định keep_plan.json"
