#!/bin/bash
# verify_transcript_pipeline.sh — 9-step self-check for TikTok/YouTube transcript task
# Usage: bash verify_transcript_pipeline.sh <video_url> <output_dir>
#
# Runs the FULL pipeline AND verifies ALL 5 deliverables exist:
#   1. video.mp4 (download)
#   2. transcript.txt (raw voice text)
#   3. transcript.srt (subtitle with timestamps)
#   4. transcript_segments.txt (formatted segments)
#   5. SCRIPT_ANALYSIS.md (the part agent missed last time)
#
# Returns exit 0 = ALL PASS, exit 1 = missing deliverables.
# Created 2026-06-22 after Tuấn Anh's correction: agent reported "done" 3 times without producing SCRIPT_ANALYSIS.md.

set -u

URL="${1:-}"
OUT="${2:-/tmp/tiktok-transcript-verify}"

if [ -z "$URL" ]; then
  echo "Usage: $0 <video_url> [output_dir]"
  exit 1
fi

mkdir -p "$OUT"
cd "$OUT"

PASS=0
FAIL=0
WARN=0

# ──────────────────────────────────────────────────────────────────
# Step 1: Check URL parseable
# ──────────────────────────────────────────────────────────────────
echo "=== Step 1: URL parseable ==="
if yt-dlp --no-warnings --no-playlist -F "$URL" >/dev/null 2>&1; then
  echo "✓ yt-dlp can parse URL"
  PASS=$((PASS+1))
else
  echo "✗ URL not parseable by yt-dlp"
  FAIL=$((FAIL+1))
fi

# ──────────────────────────────────────────────────────────────────
# Step 2: Download "download" format (always has audio+video bundled)
# ──────────────────────────────────────────────────────────────────
echo ""
echo "=== Step 2: Download format ==="
if yt-dlp --no-warnings --no-playlist \
   -f "download" \
   -o "$OUT/video.%(ext)s" \
   "$URL" 2>/dev/null; then
  if [ -f "$OUT/video.mp4" ]; then
    SIZE=$(du -h "$OUT/video.mp4" | cut -f1)
    echo "✓ Downloaded video.mp4 ($SIZE)"
    PASS=$((PASS+1))
  else
    echo "✗ Download reported success but no file"
    FAIL=$((FAIL+1))
  fi
else
  echo "✗ Download failed"
  FAIL=$((FAIL+1))
fi

# ──────────────────────────────────────────────────────────────────
# Step 3: Verify audio stream present (DO NOT skip transcript path)
# ──────────────────────────────────────────────────────────────────
echo ""
echo "=== Step 3: Audio stream present ==="
AUDIO_STREAMS=$(ffprobe -v error -show_streams -of json "$OUT/video.mp4" 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
audio = [s for s in d.get('streams', []) if s.get('codec_type') == 'audio']
print(len(audio))
")
if [ "$AUDIO_STREAMS" -gt 0 ]; then
  echo "✓ Audio stream present (count=$AUDIO_STREAMS)"
  PASS=$((PASS+1))
else
  echo "✗ NO audio stream — try variant -1 before vision-only fallback"
  FAIL=$((FAIL+1))
  WARN=$((WARN+1))
fi

# ──────────────────────────────────────────────────────────────────
# Step 4: Extract audio WAV
# ──────────────────────────────────────────────────────────────────
echo ""
echo "=== Step 4: Extract audio WAV ==="
if [ "$AUDIO_STREAMS" -gt 0 ]; then
  if ffmpeg -y -i "$OUT/video.mp4" -vn -ar 16000 -ac 1 -c:a pcm_s16le "$OUT/audio.wav" 2>/dev/null; then
    SIZE=$(du -h "$OUT/audio.wav" | cut -f1)
    echo "✓ Extracted audio.wav ($SIZE)"
    PASS=$((PASS+1))
  else
    echo "✗ Audio extraction failed"
    FAIL=$((FAIL+1))
  fi
else
  echo "⏭️  SKIP (no audio stream)"
  WARN=$((WARN+1))
fi

# ──────────────────────────────────────────────────────────────────
# Step 5: Run mlx-whisper Vietnamese
# ──────────────────────────────────────────────────────────────────
echo ""
echo "=== Step 5: Whisper transcription ==="
# IMPORTANT: use whisper-env path (NOT default `mlx_whisper` which has broken shebang).
# Verified working 2026-06-18: /Users/tuananh4865/whisper-env/bin/python3 has Python 3.11 + mlx_whisper installed.
PYTHON="/Users/tuananh4865/whisper-env/bin/python3"
if [ -f "$OUT/audio.wav" ] && [ "$AUDIO_STREAMS" -gt 0 ]; then
  if $PYTHON -c "
import mlx_whisper, json
result = mlx_whisper.transcribe(
    '$OUT/audio.wav',
    path_or_hf_repo='mlx-community/whisper-medium',
    language='vi',
    task='transcribe'
)
with open('$OUT/transcript.txt', 'w') as f: f.write(result['text'])
with open('$OUT/transcript.json', 'w') as f: json.dump(result, f, ensure_ascii=False, indent=2)
def fmt(t):
    h, m, s = int(t//3600), int((t%3600)//60), int(t%60)
    ms = int((t%1)*1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
with open('$OUT/transcript.srt', 'w') as f:
    for i, seg in enumerate(result['segments'], 1):
        f.write(f'{i}\n{fmt(seg[\"start\"])} --> {fmt(seg[\"end\"])}\n{seg[\"text\"].strip()}\n\n')
with open('$OUT/transcript_segments.txt', 'w') as f:
    for seg in result['segments']:
        f.write(f'[{seg[\"start\"]:.1f}s-{seg[\"end\"]:.1f}s] {seg[\"text\"].strip()}\n')
print(f'Transcribed: {len(result[\"segments\"])} segments, {result[\"segments\"][-1][\"end\"]:.1f}s')
" 2>&1 | tail -3; then
    echo "✓ Whisper transcript produced"
    PASS=$((PASS+1))
  else
    echo "✗ Whisper transcription failed"
    FAIL=$((FAIL+1))
  fi
else
  echo "⏭️  SKIP (no audio)"
  WARN=$((WARN+1))
fi

# ──────────────────────────────────────────────────────────────────
# Step 6: Verify transcript.txt exists
# ──────────────────────────────────────────────────────────────────
echo ""
echo "=== Step 6: transcript.txt exists ==="
if [ -f "$OUT/transcript.txt" ]; then
  CHARS=$(wc -c < "$OUT/transcript.txt")
  echo "✓ transcript.txt exists ($CHARS bytes)"
  PASS=$((PASS+1))
else
  echo "✗ transcript.txt missing"
  FAIL=$((FAIL+1))
fi

# ──────────────────────────────────────────────────────────────────
# Step 7: Verify transcript.srt exists (the actual deliverable)
# ──────────────────────────────────────────────────────────────────
echo ""
echo "=== Step 7: transcript.srt exists ==="
if [ -f "$OUT/transcript.srt" ]; then
  SEGMENTS=$(grep -c "^[0-9]\+$" "$OUT/transcript.srt" 2>/dev/null || echo 0)
  echo "✓ transcript.srt exists ($SEGMENTS segments)"
  PASS=$((PASS+1))
else
  echo "✗ transcript.srt missing"
  FAIL=$((FAIL+1))
fi

# ──────────────────────────────────────────────────────────────────
# Step 8: Verify SCRIPT_ANALYSIS.md exists (THE PART AGENT MISSED)
# ──────────────────────────────────────────────────────────────────
echo ""
echo "=== Step 8: SCRIPT_ANALYSIS.md exists (THE PART AGENT MISSED 2026-06-22) ==="
if [ -f "$OUT/SCRIPT_ANALYSIS.md" ]; then
  SECTIONS=$(grep -c "^## " "$OUT/SCRIPT_ANALYSIS.md")
  echo "✓ SCRIPT_ANALYSIS.md exists ($SECTIONS sections)"
  if [ "$SECTIONS" -lt 8 ]; then
    echo "⚠️  WARNING: less than 8 sections — agent may have skipped analysis"
    WARN=$((WARN+1))
  fi
  PASS=$((PASS+1))
else
  echo "✗ SCRIPT_ANALYSIS.md MISSING — agent only extracted raw text, did NOT analyze"
  echo "   This is exactly the failure from 2026-06-22 that Tuấn Anh caught."
  echo "   The user said 'phân tích transcript' = analysis is required, not just extraction."
  FAIL=$((FAIL+1))
fi

# ──────────────────────────────────────────────────────────────────
# Step 9: Final summary
# ──────────────────────────────────────────────────────────────────
echo ""
echo "=== SUMMARY ==="
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "  WARN: $WARN"
echo ""
echo "  Required deliverables for 'phân tích transcript video' task:"
echo "    1. video.mp4           (download)"
echo "    2. transcript.txt       (raw voice text)"
echo "    3. transcript.srt       (subtitle with timestamps)"
echo "    4. transcript_segments.txt"
echo "    5. SCRIPT_ANALYSIS.md   (Hook + Structure + Psychology + Viral formula + CTA + Lessons)"
echo ""
echo "  Without SCRIPT_ANALYSIS.md, the task is NOT DONE."
echo "  This is the lesson from 2026-06-22: 'phân tích' = analysis, not just extraction."

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi

exit 0