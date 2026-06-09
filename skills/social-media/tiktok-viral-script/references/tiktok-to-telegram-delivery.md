# TikTok Video → Telegram Delivery Workflow

>Created: 2026-06-10
>Source: Session — @anhsacanh.vn video download analysis

---

## Problem Statement

When downloading TikTok videos via `yt-dlp` and sending to Telegram:

1. **Video may be SILENT from the source** — TikTok allows posting videos without audio (text overlay content, music-free content)
2. **HEVC/H.265 codec** — TikTok serves in HEVC, which Telegram may not play on all clients
3. **File size** — Large videos (>50MB) timeout on Telegram upload
4. **Format mismatch** — `.mp4` from yt-dlp may have no audio track at all

---

## TikTok Video → Telegram Pipeline

### Step 1: Download
```bash
yt-dlp -o "tiktok_%(id)s.%(ext)s" "https://vt.tiktok.com/VIDEO_ID/"
```

### Step 2: Check streams (BEFORE sending)
```bash
ffprobe -v quiet -print_format json -show_streams video.mp4 | jq '.streams[] | {codec_type, codec_name, duration}'
```

**Key questions:**
- `codec_type: video` only? → Silent video (this is content style, not error)
- `codec_type: audio` present? → Has sound
- `codec_name: hevc`? → Needs conversion for Telegram

### Step 3: Convert for Telegram
```bash
# 720p H.264 + AAC audio (even if silent, AAC track needed for compatibility)
ffmpeg -i input.mp4 \
  -c:v libx264 -preset fast -crf 26 \
  -vf "scale=720:-2" \
  -c:a aac -b:a 96k \
  -movflags +faststart \
  output_720p.mp4
```

**Why this works:**
| Setting | Reason |
|---------|--------|
| `libx264` | H.264 — universal Telegram support |
| `720:-2` | Scale to 720px width, height divisible by 2 (required) |
| `crf 26` | Quality/size balance — good enough for Telegram |
| `aac -b:a 96k` | Audio track (even silent) prevents "invalid format" |
| `movflags +faststart` | Enables streaming playback during download |

### Step 4: Check output size
```bash
ls -lh output_720p.mp4
```

- **< 50MB** → Safe to send via Telegram
- **50-100MB** → Risky, may timeout
- **> 100MB** → Must reduce quality or use alternative delivery

### Step 5: Send to Telegram
```
MEDIA:/Users/tuananh4865/Downloads/output_720p.mp4
```

---

## Critical Distinction: Silent ≠ Error

**CONFIRMED (2026-06-10):** Some TikTok content is intentionally silent.

| Video Type | Audio | Example |
|------------|-------|---------|
| Music/Reels content | Has audio | Standard TikTok with trending sounds |
| Text overlay content | SILENT | @anhsacanh.vn video — text + graphic overlay only |
| Tutorial/voiceover | Has audio | Creator speaking on camera |
| Product showcase | Usually has audio | But can be silent if text-focused |

**When video is silent:**
1. Do NOT re-download thinking it's an error
2. Do NOT try to "add audio" — the content is meant to be silent
3. Document it as "silent content" in analysis
4. If Anh wants audio, ask for a DIFFERENT video (one with sound)

---

## Session Transcript: @anhsacanh.vn Video (2026-06-10)

```
Video: https://vt.tiktok.com/ZSQBX2mTj/
Downloaded: tiktok_7644892443644808468.mp4 (20.93MB)
Probe result: Video only (HEVC), no audio track, duration 308s
First conversion attempt: H.264 but still silent → sent anyway
Second attempt: 720p H.264 + AAC → 33MB → sent successfully
```

**Issue:** The video was **silently posted** (text overlay content), not a download error.

---

## Quick Reference

```bash
# Download TikTok video
yt-dlp -o "tiktok_%(id)s.%(ext)s" "https://vt.tiktok.com/VIDEO_ID/"

# Probe streams
ffprobe -v quiet -print_format json -show_streams video.mp4 | jq '.streams[] | {codec_type, codec_name, duration}'

# Convert for Telegram
ffmpeg -i input.mp4 -c:v libx264 -preset fast -crf 26 -vf "scale=720:-2" -c:a aac -b:a 96k -movflags +faststart output_720p.mp4

# Check size
ls -lh output_720p.mp4
```

---

## Related
- `references/tiktok-video-analysis-workflow.md` — Full analysis pipeline (yt-dlp → ffmpeg → vision)
- `references/tiktok-content-writing-2026.md` — Hook patterns, script structure
- `references/tiktok-monitor-workflow-june-2026.md` — 5-channel nightly monitor