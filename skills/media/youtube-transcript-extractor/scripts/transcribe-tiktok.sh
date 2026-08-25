#!/bin/bash
# transcribe-tiktok.sh — One-shot TikTok/YouTube transcript pipeline
# Created 2026-06-22 after Tuấn Anh corrected me for doing visual analysis when user asked for transcript.
#
# Usage: ./transcribe-tiktok.sh <video_url> [output_dir] [whisper_model]
#   video_url:      TikTok (vt.tiktok.com or tiktok.com/.../video/...) or YouTube URL
#   output_dir:     Default: ~/wiki/raw/tiktok-analysis/
#   whisper_model:  Default: mlx-community/whisper-medium (Vietnamese friendly)
#
# Pipeline (FIXED from session 2026-06-22):
#   1. yt-dlp -F → list ALL formats (NEVER skip — TikTok has variant -0/-1 pitfall)
#   2. yt-dlp -f "download" → watermarked, ALWAYS has audio+video bundled (safest)
#   3. ffprobe verify audio presence (CRITICAL — never conclude "no audio" without this)
#   4. ffmpeg extract WAV 16kHz mono
#   5. mlx-whisper transcribe (language=vi force, NOT auto-detect)

set -e

VIDEO_URL="$1"
OUTPUT_DIR="${2:-$HOME/wiki/raw/tiktok-analysis}"
WHISPER_MODEL="${3:-mlx-community/whisper-medium}"

if [ -z "$VIDEO_URL" ]; then
  echo "Usage: $0 <video_url> [output_dir] [whisper_model]"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# mlx-whisper requires CommandLineTools python (default python3 is broken Xcode stub)
PYTHON_BIN="/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/Current/bin/python3"

echo "=== STEP 1: List all available formats ==="
yt-dlp --no-warnings --no-playlist -F "$VIDEO_URL"

echo ""
echo "=== STEP 2: Download with -f 'download' (watermarked, has audio) ==="
# Use timestamp to avoid clobbering if same URL already downloaded
TIMESTAMP=$(date +%s)
TEMP_VIDEO="/tmp/transcribe-${TIMESTAMP}.mp4"
yt-dlp --no-warnings --no-playlist -f "download" -o "$TEMP_VIDEO" "$VIDEO_URL"

echo ""
echo "=== STEP 3: Verify audio presence (CRITICAL) ==="
STREAMS=$(ffprobe -v error -show_streams -of json "$TEMP_VIDEO" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
streams = d.get('streams', [])
video_count = sum(1 for s in streams if s.get('codec_type') == 'video')
audio_count = sum(1 for s in streams if s.get('codec_type') == 'audio')
print(f'video={video_count}, audio={audio_count}')
")
echo "$STREAMS"
echo "$STREAMS" | grep -q "audio=[1-9]" || {
  echo "ERROR: No audio stream in downloaded file. Try different format variant (e.g. -f 'bytevc1_1080p_*-1')"
  echo "DO NOT fall back to visual analysis — user asked for transcript, not vision."
  exit 2
}

echo ""
echo "=== STEP 4: Extract audio 16kHz mono WAV ==="
AUDIO_WAV="/tmp/transcribe-${TIMESTAMP}.wav"
ffmpeg -y -i "$TEMP_VIDEO" -vn -ar 16000 -ac 1 -c:a pcm_s16le "$AUDIO_WAV"

echo ""
echo "=== STEP 5: Transcribe with mlx-whisper (Vietnamese forced) ==="
$PYTHON_BIN <<EOF
import mlx_whisper
import json

result = mlx_whisper.transcribe(
    "$AUDIO_WAV",
    path_or_hf_repo="$WHISPER_MODEL",
    language="vi",
    task="transcribe",
)

# Save TXT
with open("$OUTPUT_DIR/transcript.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

# Save SRT
def fmt_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

with open("$OUTPUT_DIR/transcript.srt", "w", encoding="utf-8") as f:
    for i, seg in enumerate(result["segments"], 1):
        f.write(f"{i}\n")
        f.write(f"{fmt_time(seg['start'])} --> {fmt_time(seg['end'])}\n")
        f.write(f"{seg['text'].strip()}\n\n")

# Save JSON
with open("$OUTPUT_DIR/transcript.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Save segmented text
with open("$OUTPUT_DIR/transcript_segments.txt", "w", encoding="utf-8") as f:
    for seg in result["segments"]:
        f.write(f"[{seg['start']:.1f}s-{seg['end']:.1f}s] {seg['text'].strip()}\n")

print(f"Segments: {len(result['segments'])}")
print(f"Duration: {result['segments'][-1]['end']:.1f}s")
print(f"Language: {result.get('language', 'unknown')}")
print(f"Output files in: $OUTPUT_DIR/")
EOF

echo ""
echo "=== DONE ==="
echo "Files saved:"
ls -lh "$OUTPUT_DIR"/transcript.{txt,srt,json,segments.txt} 2>/dev/null

# Cleanup temp files
rm -f "$TEMP_VIDEO" "$AUDIO_WAV"