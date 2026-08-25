#!/bin/bash
# audio-mux-ffmpeg.sh
# Mux source audio into HyperFrames-rendered silent MP4
# Usage: ./audio-mux-ffmpeg.sh <silent_render.mp4> <source_with_audio.mp4> <output.mp4>
#
# Always tell the user: HyperFrames render produces silent MP4.
# This script restores audio from original source.

set -euo pipefail

SILENT_RENDER="${1:?Usage: $0 <silent.mp4> <source.mp4> <output.mp4>}"
SOURCE_AUDIO="${2:?Need source-with-audio.mp4}"
OUTPUT="${3:?Need output path}"

# Verify inputs exist
test -f "$SILENT_RENDER" || { echo "❌ Missing: $SILENT_RENDER"; exit 1; }
test -f "$SOURCE_AUDIO"   || { echo "❌ Missing: $SOURCE_AUDIO"; exit 1; }

# Verify durations
SILENT_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SILENT_RENDER")
SOURCE_DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SOURCE_AUDIO")

echo "Silent render duration: ${SILENT_DUR}s"
echo "Source audio duration:   ${SOURCE_DUR}s"

# Pick shortest duration (usually both same length)
SHORTER=$(awk "BEGIN{print ($SILENT_DUR < $SOURCE_DUR) ? $SILENT_DUR : $SOURCE_DUR}")

# Mux audio
ffmpeg -y \
  -i "$SILENT_RENDER" \
  -i "$SOURCE_AUDIO" \
  -map 0:v:0 \
  -map 1:a:0 \
  -c:v copy \
  -c:a aac \
  -b:a 192k \
  -shortest \
  "$OUTPUT"

echo "✅ Mux complete: $OUTPUT"
ls -la "$OUTPUT"
