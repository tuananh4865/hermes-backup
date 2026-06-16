#!/bin/bash
# analyze-telegram-video.sh
# One-shot script: detect latest video from Telegram Desktop, convert, extract frames + audio, transcribe.
# Usage: ./analyze-telegram-video.sh [optional-output-dir]
# Output: $OUTPUT_DIR/compressed.mp4, frame_NNN.jpg, audio.wav, transcript.txt

set -euo pipefail

OUTPUT_DIR="${1:-/tmp/frame-analysis}"
mkdir -p "$OUTPUT_DIR"

# 1. Find most recent video in Telegram Desktop or Downloads
echo "🔍 Detecting latest video..."
VIDEO_FILE=$(stat -f "%m %N" -t "%Y%m%d%H%M%S" \
  /Users/tuananh4865/Downloads/Telegram\ Desktop/*.mp4 \
  /Users/tuananh4865/Downloads/Telegram\ Desktop/*.MP4 \
  /Users/tuananh4865/Downloads/Telegram\ Desktop/*.mov \
  /Users/tuananh4865/Downloads/*.mp4 \
  /Users/tuananh4865/Downloads/*.MP4 \
  /Users/tuananh4865/Downloads/*.mov 2>/dev/null \
  | sort -r | head -1 | awk '{print $2}')

if [ -z "$VIDEO_FILE" ] || [ ! -f "$VIDEO_FILE" ]; then
  echo "❌ No video found in ~/Downloads"
  exit 1
fi

echo "📹 Found: $VIDEO_FILE"

# 2. ffprobe metadata
echo "🔬 Probing metadata..."
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_type,codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 "$VIDEO_FILE"

# 3. Convert to H.264 720p
echo "🔄 Converting HEVC→H.264 720p..."
cd "$OUTPUT_DIR"
ffmpeg -i "$VIDEO_FILE" \
  -vf "scale=720:-2" \
  -c:v libx264 -preset fast -crf 28 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  compressed.mp4 -y 2>&1 | tail -2

# 4. Extract frames @ 1fps
echo "🖼️ Extracting frames @ 1fps..."
ffmpeg -i compressed.mp4 -vf "fps=1" frame_%03d.jpg -y 2>&1 | tail -1
FRAME_COUNT=$(ls frame_*.jpg 2>/dev/null | wc -l | tr -d ' ')
echo "✅ Extracted $FRAME_COUNT frames"

# 5. Extract audio
echo "🔊 Extracting audio..."
ffmpeg -i compressed.mp4 -vn -acodec copy audio.aac -y 2>&1 | tail -1
ffmpeg -i audio.aac -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y 2>&1 | tail -1

# 6. Whisper transcription (Vietnamese)
echo "🎙️ Transcribing with mlx-whisper (Vietnamese)..."
if command -v mlx_whisper >/dev/null 2>&1; then
  mlx_whisper audio.wav \
    --model mlx-community/whisper-small-mlx \
    --language vi \
    --output-format txt \
    --output-name transcript 2>&1 | tail -3
  echo "---TRANSCRIPT---"
  cat transcript.txt 2>/dev/null || echo "(empty)"
else
  echo "⚠️ mlx_whisper not installed. Install: pip install mlx-whisper"
fi

# 7. Package summary video (frames + audio)
echo "📦 Packaging summary video..."
ffmpeg -framerate 1 -i frame_%03d.jpg -i audio.wav \
  -c:v libx264 -preset fast -crf 28 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -shortest \
  -vf "scale=540:-2" \
  -movflags +faststart \
  summary.mp4 -y 2>&1 | tail -1

echo ""
echo "✅ DONE. Outputs in: $OUTPUT_DIR"
echo "   compressed.mp4: $(ls -lh compressed.mp4 | awk '{print $5}')"
echo "   summary.mp4:    $(ls -lh summary.mp4 | awk '{print $5}')"
echo "   audio.wav:      $(ls -lh audio.wav | awk '{print $5}')"
echo "   frames:         $FRAME_COUNT files"
echo "   transcript.txt: $(wc -c < transcript.txt 2>/dev/null || echo 0) bytes"
