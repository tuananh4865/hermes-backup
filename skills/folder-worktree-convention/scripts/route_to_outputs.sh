#!/bin/bash
# route_to_outputs.sh — Helper route file lẻ vào /Volumes/Storage-1/Hermes/outputs/<sub>/
# Created: 2026-07-10 (anh mandate worktree mặc định)
# Usage:
#   route_to_outputs.sh video my-clip.mp4
#   route_to_outputs.sh telegram_file report.pdf
#   route_to_outputs.sh screenshot capture.png
#   route_to_outputs.sh transcript audio.vtt
#
# Subdir mapping (see /Volumes/Storage-1/Hermes/outputs/.worktree-routing.yaml):
#   video, youtube_download, tiktok_download → videos/
#   telegram_file, browser_download           → downloads/
#   pdf, docx, xlsx                            → documents/
#   image, image_generate, vision_input        → images/
#   audio, tts, mp3                            → audio/
#   screenshot                                 → screenshots/
#   transcript, vtt, srt, json                 → transcripts/
#   cron_deliverable                           → cron-output/
#   temp, scratch, throwaway                   → scratch/

set -e

OUTPUTS_ROOT="/Volumes/Storage-1/Hermes/outputs"

if [ $# -lt 2 ]; then
    echo "Usage: $0 <file_type> <filename> [subdir_override]"
    echo ""
    echo "Common file_type values:"
    echo "  video, youtube_download, tiktok_download → videos/"
    echo "  telegram_file, browser_download           → downloads/"
    echo "  pdf, docx, xlsx                            → documents/"
    echo "  image, image_generate, vision_input        → images/"
    echo "  audio, tts, mp3                            → audio/"
    echo "  screenshot                                 → screenshots/"
    echo "  transcript, vtt, srt, json                 → transcripts/"
    echo "  cron_deliverable                           → cron-output/"
    echo "  temp, scratch, throwaway                   → scratch/"
    exit 1
fi

FILE_TYPE="$1"
FILENAME="$2"
SUBDIR_OVERRIDE="${3:-}"

# Subdir mapping
case "$FILE_TYPE" in
    video|youtube_download|tiktok_download)
        SUBDIR="videos" ;;
    telegram_file|browser_download)
        SUBDIR="downloads" ;;
    pdf|docx|xlsx|document)
        SUBDIR="documents" ;;
    image|image_generate|vision_input)
        SUBDIR="images" ;;
    audio|tts|mp3)
        SUBDIR="audio" ;;
    screenshot)
        SUBDIR="screenshots" ;;
    transcript|vtt|srt|whisper_json)
        SUBDIR="transcripts" ;;
    cron_deliverable|cron_output)
        SUBDIR="cron-output" ;;
    temp|scratch|throwaway)
        SUBDIR="scratch" ;;
    *)
        # Unknown type → fallback to downloads/
        SUBDIR="downloads"
        echo "⚠️  Unknown file_type '$FILE_TYPE', defaulting to downloads/" >&2 ;;
esac

# Override if explicit
if [ -n "$SUBDIR_OVERRIDE" ]; then
    SUBDIR="$SUBDIR_OVERRIDE"
fi

# Ensure subdir exists
TARGET_DIR="$OUTPUTS_ROOT/$SUBDIR"
mkdir -p "$TARGET_DIR"

# Verify target is in allowlist (defensive check)
TARGET_PATH="$TARGET_DIR/$FILENAME"
echo "$TARGET_PATH"

# Sanity check: ensure we never route outside /Volumes/Storage-1/Hermes/outputs/
case "$TARGET_PATH" in
    /Volumes/Storage-1/Hermes/outputs/*)
        echo "✅ Routed: $TARGET_PATH" >&2
        ;;
    *)
        echo "❌ SAFETY: Refusing path outside outputs/: $TARGET_PATH" >&2
        exit 2
        ;;
esac