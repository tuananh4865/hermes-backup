# Case Study: TikTok VIDEO-only (HEVC + no audio) — @caocuongvuai reaction video

**Date:** 2026-06-22
**Source:** https://vt.tiktok.com/ZSCJB91YQ/ → https://www.tiktok.com/@caocuongvuai/video/7623055460836330772
**Duration:** 377.65s (6 phút 17s)
**File size:** 32.6 MB
**Resolution:** 1080×1920 @ 60fps
**Codec:** HEVC (H.265) — VIDEO ONLY, no audio stream
**Stats:** 113,800 views | 7,561 likes | 135 comments

## What this video is

A long-form Vietnamese TikTok (6+ minutes — much longer than typical 60-90s) by @caocuongvuai about AI tools + trend commentary. Format = split-screen reaction with:
- Talking head host (Asian male, black t-shirt, mic with deadcat) reacting to content
- Top half of frame: screen recording / article / YouTube video being reacted to
- PIP (picture-in-picture) showing the source video when needed
- VIETSUB karaoke-style captions throughout

## Workflow mistakes that happened this session

### Mistake 1: Asked for URL when user said "Tải video này về"
User message was "Tải về và phân tích transcript video này!" — no URL. Agent replied asking for a link. User frustrated "Anh gửi trực tiếp qua telegram mà".

**Lesson:** Any "video này" + no URL = check `~/.hermes/cache/videos/` FIRST. See Pitfall #36.

### Mistake 2: Tried `--extract-audio` on HEVC TikTok
Ran `yt-dlp -f "bestaudio[ext=m4a]/bestaudio/best" --extract-audio --audio-format mp3 --audio-quality 5`. Got exit code 0 BUT also `WARNING: unable to obtain file audio codec with ffprobe` and NO file output.

**Lesson:** Already covered in `video-download-yt-dlp` Pitfall #8 + #9. Must read pitfalls BEFORE executing.

### Mistake 3: `ffmpeg -i video.mp4 audio.wav` failed silently
Got error: `Output file does not contain any stream / Error opening output file`. Failed because video is HEVC video-only, no audio stream at all.

**Lesson:** Run ffprobe FIRST to detect stream count:
```bash
ffprobe -v error -show_streams -of json FILE.mp4
# Only HEVC video stream, 0 audio streams → skip Whisper, go vision-only
```

### Mistake 4: Vision analysis was slow but worked
Extracted 8 frames at fixed positions (every ~1500 frames = ~30s @ 60fps). Ran `mcp_MiniMax_understand_image` in parallel (4 at a time). Got back detailed Vietnamese analysis for each frame including VIETSUB caption extraction, background, character, action.

**Lesson:** Vision-only analysis IS the right path for TikTok HEVC video-only files. Whisper is not needed.

## What worked

### Frame extraction pattern for 6-min video @ 60fps
```bash
mkdir -p /tmp/tiktok-frames
ffmpeg -y -i VIDEO.mp4 \
  -vf "select='eq(n,30)+eq(n,1500)+eq(n,3000)+eq(n,4500)+eq(n,6000)+eq(n,7500)+eq(n,9000)+eq(n,10500)'" \
  -vsync vfr -q:v 2 /tmp/tiktok-frames/frame_%03d.jpg
```
Frame N at 60fps = timestamp N/60 seconds:
- frame 30 = 0.5s (intro/hook)
- frame 1500 = 25s (~minute 0.5)
- frame 3000 = 50s (~minute 1)
- frame 4500 = 75s (~minute 1.5)
- frame 6000 = 100s (~minute 2)
- frame 7500 = 125s (~minute 2.5)
- frame 9000 = 150s (~minute 3)
- frame 10500 = 175s (~minute 3.5)

For 6-min video, 8 frames is enough to capture the full arc.

### Vision analysis prompt template (worked well)
```
Phân tích chi tiết frame này của video TikTok. Mô tả:
1. Bối cảnh chính (background, màu sắc)
2. Nhân vật/đối tượng trong khung hình
3. Text/caption hiển thị (VIETSUB nguyên văn)
4. Hành động đang diễn ra
5. Phong cách visual (cinematic, talking head, slideshow, screen recording, animation...)
6. Đánh giá chất lượng production (lighting, composition, hook strength)
```

Parallel calls in batches of 4 worked without rate limits (this video is shorter than the 90s La La School one that triggered rate limits).

### Output deliverable structure (what user liked)
Markdown file with:
1. Metadata table (ID, URL, uploader, duration, upload date, views, likes, comments, engagement ratio)
2. Format analysis (talking head + split-screen + caption overlay + VIETSUB)
3. Content flow breakdown (8 frames → estimated phase boundaries)
4. Hook analysis (visual + gesture + text + expression = 4-layer hook)
5. Content insight (what works, what to learn)
6. Apply-to-channel section (HỌC gì / KHÔNG học gì cho kênh Tuấn Anh)
7. Next steps (3-4 options)

This structure was approved and Tuấn Anh was happy with the output.

## Reusable workflow summary

For **TikTok HEVC video-only files** (no audio stream):

1. Download: `yt-dlp -f "best" URL` (not --extract-audio)
2. Verify with ffprobe — confirm only 1 HEVC stream, 0 audio
3. Extract 8 frames at evenly-spaced positions: `ffmpeg -vf "select='eq(n,30)+...'" -vsync vfr`
4. Vision analyze parallel (4 at a time): use VIETSUB extraction + visual style template
5. Save analysis to wiki: `raw/tiktok-analysis/VIDEO_ID_ANALYSIS.md`
6. Append to `wiki/log.md` with timestamp

**Save wiki path:** `/Volumes/Storage-1/Hermes/wiki/raw/tiktok-analysis/`
**Naming:** `<VIDEO_ID>_ANALYSIS.md`

## When NOT to apply this workflow

- If video has audio stream → use full pipeline (Whisper + vision)
- If video < 60s → 1fps frame extraction is fine (no sparse sampling needed)
- If user wants ONLY transcript → use `youtube-transcript-extractor` instead
- If user wants file BACK (download only) → use `video-download-yt-dlp`