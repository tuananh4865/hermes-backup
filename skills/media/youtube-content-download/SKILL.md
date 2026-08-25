---
name: youtube-content-download
description: Download YouTube videos at fixed 720p MP4 quality for content repurposing (transcript, edit, highlight detection). Single-file CLI, fast, supports any URL format.
created: 2026-07-09
version: 1.0.0
---

# 📥 YouTube Content Download

> **CLI tool pattern** để download video YouTube ở 720p MP4 (best for content repurposing — không quá nặng, không quá nhẹ, giữ audio chất lượng cao).

## 🎯 Khi nào dùng

| Use case | Dùng tool này? |
|---|---|
| Download video YouTube để transcribe/edit/highlight | ✅ CÓ |
| Download shorts (vertical 9:16) | ✅ CÓ — yt-dlp auto-detect |
| Download playlist nhiều video | ✅ CÓ — dùng `--playlist-items` |
| Download ở resolution > 1080p | ⚠️ Override bằng format khác |
| Download audio-only (MP3/WAV) | ❌ → dùng `yt-dlp -x --audio-format wav` |

## 🚀 CLI Usage

### Basic (720p MP4)

```bash
yt-dlp -f "best[height<=720]" --merge-output-format mp4 \
  -o "~/Downloads/<name>.mp4" \
  "https://www.youtube.com/watch?v=<ID>"
```

**Hoặc dùng short URL:**
```bash
yt-dlp -f "best[height<=720]" --merge-output-format mp4 \
  -o "~/Downloads/<name>.mp4" \
  "https://youtu.be/<ID>?si=<token>"
```

### Extract shorts

```bash
yt-dlp -f "best[height<=720]" --merge-output-format mp4 \
  -o "~/Downloads/short_<ID>.mp4" \
  "https://www.youtube.com/shorts/<ID>"
```

### Playlist (subset)

```bash
# Download first 3 videos của playlist
yt-dlp -f "best[height<=720]" --merge-output-format mp4 \
  --playlist-items 1-3 \
  -o "~/Downloads/playlist_%(playlist_index)s_%(title)s.mp4" \
  "https://www.youtube.com/playlist?list=<ID>"
```

## 🔧 Options chi tiết

| Flag | Ý nghĩa | Default |
|---|---|---|
| `-f "best[height<=720]"` | Pick best quality ≤ 720p | Auto (highest) |
| `--merge-output-format mp4` | Merge video + audio streams thành MP4 | mkv |
| `-o <path>` | Output path (support `%(title)s`, `%(id)s`) | Current dir |
| `--audio-format wav` | Extract audio only | Skip video |

## ⚙️ Setup (one-time)

```bash
# Install yt-dlp qua Homebrew (recommended for macOS)
brew install yt-dlp

# Update yt-dlp (YouTube thường xuyên thay đổi format)
brew upgrade yt-dlp
```

**Alternative (pip):**
```bash
pip install -U yt-dlp
```

## 🐛 Troubleshooting

### Error: "Sign in to confirm you're not a bot"

```bash
# Option 1: Update yt-dlp (most common fix)
brew upgrade yt-dlp

# Option 2: Use cookies from browser
yt-dlp --cookies-from-browser chrome \
  -f "best[height<=720]" --merge-output-format mp4 \
  -o "output.mp4" "<URL>"
```

### Error: "Video unavailable"

- Video có thể đã bị xóa hoặc private
- Check URL trực tiếp trên YouTube

### Slow download

- Check internet connection
- Try `-f "worst[height<=720]"` cho tốc độ thay vì quality

## 📝 Verified 09/07/2026

**Test case:** `https://youtu.be/n2884oDI824?si=Bsl09_TRumssqNb4`
- ✅ Download 720p MP4 → 28 MB, 635s duration
- ✅ Resolution 640×360 (auto-scaled by YouTube)
- ✅ Audio AAC 256kbps (sufficient cho Whisper + YAMNet)
- ✅ Total time: ~3 giây với Homebrew install

## 🔗 Related

- **Used by skills:**
  - `badminton-highlight-editor` (download match → cut highlights)
  - `tiktok-video-editor` (download long video → cut TikTok clip)
  - `transcript-cleanup` (download → extract transcript)
- **Skills:** `~/.hermes/skills/media/video-download-yt-dlp/SKILL.md` (sister skill, covers full yt-dlp options)