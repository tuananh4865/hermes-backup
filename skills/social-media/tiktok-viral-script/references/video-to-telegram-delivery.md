# Video → Telegram Delivery Workflow (TikTok + YouTube + others)

> Created: 2026-06-10 (TikTok) | Extended 2026-06-12 (YouTube)
> Source sessions: @anhsacanh.vn silent TikTok (2026-06-10), YouTube Shorts OXXoI2MF-Gs (2026-06-12)

---

## Problem Statement

When downloading videos via `yt-dlp` and sending to Telegram:

1. **Video may be SILENT from the source** — TikTok (and some YouTube) allow posting videos without audio
2. **HEVC/H.265 codec** — TikTok serves HEVC; Telegram may not play it on all clients
3. **File size** — Videos >50MB timeout on Telegram upload
4. **Format mismatch** — `.mp4` from yt-dlp may have no audio track
5. **URL quoting in bash** — Parentheses in TikTok/YouTube URLs break the command
6. **Shorts detection** — YouTube Shorts are SHORT (<60s) but the workflow still works

---

## When to Use This Workflow

Anh says: "tải về", "tải giùm anh", "gửi qua đây", "send me the video" + URL.

| Source | Access | Action |
|--------|--------|--------|
| TikTok (vt.tiktok.com, www.tiktok.com) | ✅ yt-dlp | Download → probe → send |
| YouTube (youtube.com, youtu.be, Shorts) | ✅ yt-dlp | Download → probe → send |
| Facebook / Instagram | ⚠️ May need cookies | Try yt-dlp first, fallback to report |
| Telegram attachment | ❌ Cannot access | Tell Anh to save to ~/Downloads/ + filename |

---

## Universal Pipeline (works for both TikTok and YouTube)

### Step 1: Download (with URL quoting!)
```bash
# ALWAYS quote the URL — parentheses in URLs break bash
yt-dlp -f "best[height<=720][ext=mp4]/best[ext=mp4]/best" \
  --merge-output-format mp4 \
  -o "VIDEO_ID.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

**URL quoting rules:**
- ALWAYS wrap URL in double quotes — `youtube.com/watch?v=OXXoI2MF-Gs` works, but URLs with `(...)` from TikTok shop or similar need quotes
- If yt-dlp returns "unexpected token '('" → URL not quoted

### Step 2: Probe streams (BEFORE sending)
```bash
ffprobe -v quiet -print_format json -show_streams "VIDEO_ID.mp4" | \
  jq '.streams[] | {codec_type, codec_name, duration, width, height}'
```

**Decode the output:**
- `codec_type: video` only? → Silent video (content style, not error)
- `codec_type: audio` present? → Has sound
- `codec_name: hevc`? → Needs conversion for Telegram
- `codec_name: h264`? → Universal support, send as-is
- `duration: <10`? → Likely a Short, may not need compression

### Step 3: Convert ONLY if needed

**Skip conversion when:**
- YouTube video with H.264 + AAC + size <50MB → send as-is
- YouTube Shorts (<60s, typically <5MB) → send as-is

**Convert when:**
- TikTok video with HEVC codec → convert to H.264+AAC
- Any video >50MB → compress to 720p
- Any video >100MB → MUST reduce quality

```bash
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
- **> 100MB** → Must reduce quality

### Step 5: Send to Telegram
```
MEDIA:/Users/tuananh4865/Downloads/VIDEO_ID.mp4
```

Include a short Vietnamese caption with the metadata from ffprobe:
- Resolution (1280x720)
- Duration
- Codec (H.264 + AAC)
- File size

---

## Platform-Specific Notes

### YouTube (incl. Shorts)
- **Default codec is H.264 + AAC** → usually no conversion needed
- **yt-dlp format 95 (720p)** is a safe default for Shorts
- **Shorts are <60s, typically <5MB** → no Telegram size risk
- **URL formats accepted:** `youtube.com/watch?v=ID`, `youtu.be/ID`, `/shorts/ID`
- **Filename convention:** `VIDEO_ID.mp4` (11-char ID)
- **If file is suspiciously small (<200KB) and you picked 720p** → check ffprobe, may be a very short Short (4-6s) — this is NORMAL, not an error

### TikTok
- **Default codec is HEVC/H.265** → almost always needs conversion
- **Many TikToks are SILENT by design** (text overlay content) → don't treat as error
- **Use `vt.tiktok.com/...` short URLs or full `tiktok.com/@user/video/ID`**
- **Filename convention:** `tiktok_VIDEO_ID.mp4` (numeric ID)
- **Probe streams first** — silent video is content style, not download error

### Other platforms
- **Facebook:** `yt-dlp` works with `--add-header "User-Agent:..."` sometimes
- **Instagram:** May require login cookies, often fails
- **X/Twitter:** Use `xurl` skill, not yt-dlp

---

## Critical Distinction: Silent ≠ Error

**CONFIRMED in multiple sessions:** Silent video is often a CONTENT CHOICE.

| Video Type | Audio | Example |
|------------|-------|---------|
| Music/Reels content | Has audio | Standard TikTok with trending sounds |
| Text overlay content | SILENT | @anhsacanh.vn video — text + graphic overlay only |
| Tutorial/voiceover | Has audio | Creator speaking on camera |
| YouTube Shorts demo | Has audio | Usually but not always |

**When video is silent:**
1. Do NOT re-download thinking it's an error
2. Do NOT try to "add audio" — the content is meant to be silent
3. Document it as "silent content" in any analysis
4. If Anh wants audio, ask for a DIFFERENT video (one with sound)

---

## Pitfalls

### ❌ yt-dlp URL without quoting
TikTok short URLs with parentheses (`vt.tiktok.com/ZSQYqMofg/`) cause bash syntax error. Always wrap URL in double quotes.

### ❌ Assuming silent video = download error
Some content is intentionally silent. Probe streams first. If video-only HEVC with no audio track → silent is the content style, not an error. Do NOT re-download.

### ❌ Sending HEVC video directly to Telegram
TikTok serves HEVC/H.265 which many Telegram clients can't play. Convert to H.264 + AAC first.

### ❌ Large file upload timeout
Telegram times out at >50MB. Always compress to 720p before sending. For YouTube Shorts (<10s), this is usually a non-issue.

### ❌ Skipping ffprobe before sending
Always run ffprobe first to know what you're dealing with — codec, duration, has-audio. This avoids wasted conversion cycles and identifies silent content.

### ❌ Picking wrong yt-dlp format
For YouTube, `best[height<=720][ext=mp4]/best` is safe. For TikTok, `--merge-output-format mp4` is essential (TikTok often serves separate audio+video streams that need merging).

### ❌ Downloading twice on first failure
If yt-dlp returns a tiny file (~100KB) and you picked 720p, check duration first. A 4-second Short IS legitimately 100KB at 720p. Don't re-download thinking the first attempt failed.

### ❌ Filename with special characters
Use `VIDEO_ID.mp4` (alphanumeric only) — avoids path issues across systems.

---

## Session Transcripts

### Session 1: @anhsacanh.vn Silent TikTok (2026-06-10)
```
Video: https://vt.tiktok.com/ZSQBX2mTj/
Downloaded: tiktok_7644892443644808468.mp4 (20.93MB)
Probe result: Video only (HEVC), no audio track, duration 308s
First conversion attempt: H.264 but still silent → sent anyway
Second attempt: 720p H.264 + AAC → 33MB → sent successfully
```
**Issue:** Video was silently posted (text overlay content), not a download error.

### Session 2: YouTube Shorts OXXoI2MF-Gs (2026-06-12)
```
Video: https://www.youtube.com/watch?v=OXXoI2MF-Gs
First attempt: yt-dlp best[height<=720] → 144KB file (looked suspicious)
Verification: ffprobe showed 1280x720 H.264 + AAC, duration 4.6s
Conclusion: 144KB IS correct for a 4.6s Short at 720p — no re-download needed
Sent: 97KB file via Telegram successfully
```
**Learning:** YouTube Shorts at 720p for <10s = ~100KB. Don't panic on small file size — verify with ffprobe first.

---

## Quick Reference

```bash
# Download (universal)
yt-dlp -f "best[height<=720][ext=mp4]/best[ext=mp4]/best" \
  --merge-output-format mp4 \
  -o "VIDEO_ID.%(ext)s" \
  "URL_HERE"

# Probe streams
ffprobe -v quiet -print_format json -show_streams "VIDEO_ID.mp4" | \
  jq '.streams[] | {codec_type, codec_name, duration, width, height}'

# Convert (only if HEVC OR >50MB)
ffmpeg -i input.mp4 \
  -c:v libx264 -preset fast -crf 26 \
  -vf "scale=720:-2" \
  -c:a aac -b:a 96k \
  -movflags +faststart \
  output_720p.mp4

# Check size
ls -lh output_720p.mp4

# Send via Telegram
MEDIA:/Users/tuananh4865/Downloads/VIDEO_ID.mp4
```

---

## Related

- `references/tiktok-video-analysis-workflow.md` — Full analysis pipeline (yt-dlp → ffmpeg → vision)
- `references/tiktok-content-writing-2026.md` — Hook patterns, script structure
- `references/tiktok-monitor-workflow-june-2026.md` — 5-channel nightly monitor
- `references/tiktok-browser-access.md` — TikTok CAPTCHA workarounds
