---
name: youtube-shorts-to-iphone-download
title: YouTube Shorts download + iPhone-friendly convert
description: Download YouTube Shorts and convert to iPhone-playable format.
version: 0.1.0
author: Hermes
platforms: [macos]
metadata:
  hermes:
    tags: [Video, Download, YouTube, Shorts, iPhone, Telegram]
---

# YouTube Shorts Download + iPhone-Ready Convert

Download a YouTube Shorts URL, transcode the file so it plays natively on iPhone (H.264/AAC/+faststart, no re-encoding of layout), and save it to the canonical Tuấn Anh folder ready for `MEDIA:` resend. Does NOT crop, scale, or alter source framing — strict goal is "file plays in iPhone Photos/CapCut/iMovie", nothing more.

## When to Use

- Anh sends a `youtube.com/shorts/<id>` link and says "tải về" / "gửi qua telegram"
- Default project: badminton highlights or any short-form content Tuấn Anh wants archived to `/Volumes/Storage-1/Tiktok-Tuan-Anh/`
- Source is already 9:16 vertical (YouTube Shorts native) — pipeline does NOT touch aspect
- **NEW 2026-07-14:** Facebook Reel share URL `facebook.com/share/r/<id>` cũng work với cùng pipeline — verified clip 1CQgRjNAy6 (42.56s, 576×1024 native 9:16, không crop). Chỉ thay URL trong command yt-dlp.

Trigger phrases: "tải clip này", "download shorts", "gửi qua tele cho iphone", "lưu vào tiktok-tuan-anh rồi gửi", "tải facebook reel".

## Prerequisites

- `yt-dlp` ≥ 2026.07.04 on PATH (Homebrew, not the bundled Python user version)
- `ffmpeg` + `ffprobe` on PATH
- Read+write on `/Volumes/Storage-1/Tiktok-Tuan-Anh/`

## How to Run

Pass the YouTube Shorts URL. The skill returns a single `MEDIA:/Volumes/Storage-1/Tiktok-Tuan-Anh/<id>_iphone.mp4` line ready to embed in the Telegram reply.

## Quick Reference

- **Canonical folder:** `/Volumes/Storage-1/Tiktok-Tuan-Anh/`
- **Filename pattern:** `<VIDEO_ID>_iphone.mp4`
- **Target spec:** H.264 video + AAC audio at 44100 Hz, `+faststart` MP4 container
- **Verify tool:** `ffprobe` against the output before any `MEDIA:` send

## Procedure

1. **Resolve the video ID** from the URL (11 chars after `/shorts/`).
2. **Delete any prior file** for that ID in `/Volumes/Storage-1/Tiktok-Tuan-Anh/` (avoid duplicate sends).
3. **Run `yt-dlp`** with the iPhone-ready postprocessor chain:

   ```bash
   yt-dlp \
     -f "bv*[ext=mp4][vcodec^=avc]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b" \
     --merge-output-format mp4 \
     --remux-video mp4 \
     --postprocessor-args "ffmpeg:-c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -movflags +faststart" \
     -o "/Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO_ID>_iphone.%(ext)s" \
     "<URL>"
   ```

4. **Verify with `ffprobe`** — must show:
   - `codec_name=h264` for video stream
   - `codec_name=aac` and `sample_rate=44100` for audio
   - `format_name` containing `mp4`
5. **Extract one mid-clip frame** with `ffmpeg -ss <mid> -vframes 1` and confirm content looks correct (NO scope judgement, just "frame loaded").
6. **Reply with a 5-row summary table** (Video ID, Size, Duration, Codec/spec line, file path) and the `MEDIA:` line.

## Pitfalls

- **Do NOT auto-crop "banda đen".** If the source has letterbox bars, leave them. Tuấn Anh explicitly opted out of cropping on 2026-07-14 (rejected the auto-crop pass after I auto-cropped WJJhUbnhx4Q → he said *"Không cần, giữ nguyên bản là được rồi!!! Chỉ cần tải phiên bản phù hợp với chuẩn đọc file của iphone là được!!!"*). Only crop if Tuấn Anh asks again.
- **Do NOT touch resolution.** Source 720x1280 stays 720x1280; source 1080x1920 stays 1080x1920. Re-scaling belongs to a separate edit skill.
- **`yt-dlp` fallback chain.** The format selector `bv*[vcodec^=avc]+ba` covers H.264 + AAC Shorts. `bv*+ba/b` is the final fallback. Don't list formats manually.
- **Filenames with `_iphone` suffix** mark "iPhone-friendly, untouched layout". Use a different suffix if Tuấn Anh asks for edits downstream (e.g. `_with_voice.mp4`, `_vi_voice.mp4` for voice overlays).
- **Save folder path is case-sensitive on purpose.** macOS APFS is case-insensitive at the volume level but treat `/Volumes/Storage-1/Tiktok-Tuan-Anh/` (capital T) as canonical to avoid stray lowercase duplicates.
- **Always delete old file for the same ID before re-download.** Tuấn Anh re-asks for the same clip = wants a fresh download, not the cached file. Verified 2026-07-14 with PaxRmpR_S-Y (deleted both `_iphone.mp4` 28.97MB + `_ORIGINAL.mp4` 13.41MB before re-fetching 26.84MB).
- **Verify file SPEC + DURATION matches expectation before ship.** Multiple consecutive rapid requests (4 clips in 30 minutes) → easy to confuse which one is which. Always cross-check Video ID + duration in the summary table.
- **Don't over-engineer — keep this skill PURE download.** When user says "tải clip về" + later says "ghép voice vào" → that's a NEW task with a separate skill (voice overlay), not a download-and-edit combo. Empirically I tried to auto-crop WJJhUbnhx4Q thinking it was a feature — was wrong.

## Cross-Session Pitfalls (compounded 2026-07-14)

### CP1: Confirm which clip is "the one" before voice overlay

**Trigger:** User downloads clip A, then later says "ghép voice vào clip vừa tải" / "tiếp tục với clip này".

**Failure pattern (real case 2026-07-14):** Tuấn Anh asked "tiếp tục với clip vừa tải" but I had 4 clips in canonical folder from rapid-fire session (WJJhUbnhx4Q, PaxRmpR_S-Y, vsQ5ORUBimY, 1CQgRjNAy6). I picked `PaxRmpR_S-Y` (the OLDEST one I had previously worked on) instead of `vsQ5ORUBimY` (the most recent). Tuấn Anh caught it: *"M ghép lộn video rồi video mới kêu tải đâu?"* — had to redo the whole voice-over.

**Mandatory procedure BEFORE any voice/edit overlay:**
1. **List canonical folder with mtime** to confirm most recent download
2. **Cross-check with conversation history** — which ID was the LAST one Tuấn Anh sent + acknowledged?
3. **Embed the Video ID in your reasoning** — *"Anh muốn ghép voice vào `<ID>` vừa tải ở turn trước — verify bằng cách X"*

**Anti-pattern:**
- ❌ Guess from memory which clip is "the one"
- ❌ Pick the oldest / most familiar one
- ❌ Assume "vừa tải" = the one you've worked on most
- ✅ **Always confirm by mtime + last-acknowledged ID**

### CP2: YouTube Shorts banda đen có thể chỉ ở TOP (không phải top+bottom)

**Trigger:** User says *"video bị bóp vuông"* / *"có viền đen"* after download.

**Updated understanding (real case 2026-07-14, clip ZGOu1-J8Vb0):**
Pitfall 5D in `video-download-yt-dlp` describes letterbox ở TOP+BOTTOM đối xứng. **NHƯNG** YouTube Shorts player thực tế thường chỉ ép video broadcast 16:9 vào container 9:16 bằng cách **thêm banda đen ở TOP (~10-15% chiều cao)**, content broadcast chiếm ~75% còn lại, KHÔNG cộng thêm đáy. Detect pattern:

- `cropdetect` **FAIL** khi có text overlay (scoreboard, captions) chạy giữa frame → `limit=0.18` vẫn trả về `crop=1080:1920:0:0`
- Workaround: **Python pixel scan** ở x=540 (giữa frame), tìm các row có brightness < 30 (pure black) liên tục từ y=0 → đó là banda đen
- Real case ZGOu1-J8Vb0: y=0-192 (0-10%) pure black, y=200+ có content (scoreboard "COLDEST MATCHPOINT EVER !?" + sân)

**Mandatory procedure when user says "bị vuông" sau YouTube Shorts download:**
1. **Em load `video-download-yt-dlp` skill** xem Pitfall 5D
2. **Cropdetect với limit 0.18 + 0.25 + 0.35** — nếu tất cả đều return `crop=1080:1920:0:0` (full frame, no crop detected) → chuyển sang Python pixel scan
3. **Pixel scan** với PIL:
   ```python
   from PIL import Image
   import numpy as np
   img = Image.open("frame.png").convert("RGB")
   arr = np.array(img)
   gray = arr.mean(axis=2)
   for y in range(0, 1920, 5):
       brightness = arr[y, 540].mean()  # pixel tại giữa frame
       print(f"y={y}: {brightness:.1f}")
   ```
4. **Identify** ngưỡng: row nào brightness < 30 = banda đen; row nào brightness > 100 = content
5. **Crop** từ y=<sau banda đen> → y=1920, scale lên fill 9:16

**Anti-pattern:**
- ❌ Tin cropdetect 1 lần với default limit → skip Python scan khi cropdetect trả full frame
- ❌ Assume banda đen đối xứng top+bottom
- ❌ Skip việc hỏi user "anh muốn em crop luôn hay giữ nguyên?" — anh explicit opt-out lần trước (turn WJJhUbnhx4Q) nên mặc định là KHÔNG auto-crop
- ✅ Sau khi detect: **HỎI anh 1 câu confirm** trước khi crop (anh đã reject 1 lần — risk of repeating mistake)

## Verification

```bash
ffprobe -v error \
  -show_entries stream=codec_name,codec_type,sample_rate \
  -show_entries format=duration,size,format_name \
  -of default=nw=1 \
  /Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO_ID>_iphone.mp4
```

Pass criteria: `h264` + `aac` + `44100` Hz + `mp4` in format name. File size in MB reported in the reply.
