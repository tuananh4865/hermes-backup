---
name: video-download-yt-dlp
title: Video Download & Resend via yt-dlp
description: Download videos from YouTube/YouTube Shorts/TikTok using yt-dlp, verify with ffprobe, and resend as native Telegram media. Use when Tuấn Anh sends a video link and wants the file back (not just analysis).
created: 2026-06-13
updated: 2026-06-13
type: skill
tags: [video, download, yt-dlp, telegram, youtube, tiktok]
confidence: high
---

# Video Download & Resend Workflow

When Tuấn Anh gửi một video link (YouTube, YouTube Shorts, TikTok), workflow chuẩn là:
**Download → Verify → Resend as Telegram media attachment** (KHÔNG chỉ analyze).

## Tại sao workflow này quan trọng

- Telegram gateway chỉ pass text/links, KHÔNG pass binary media. Em không "xem" được video anh gửi attachment.
- Khi anh gửi **link**, em download được bằng yt-dlp → gửi file về qua `MEDIA:/path` → anh xem trên Telegram.
- Đây là pattern anh dùng 100% mọi lần (xem memory: "yt-dlp → send MEDIA:/path → works 100%").

## Standard Workflow

### Step 1: Pick the right format
```bash
# List available formats first
yt-dlp -F "URL"
```

**Decision matrix:**
- **Long video (regular YouTube)**: pick highest resolution with audio (e.g. `137+140` for 1080p video-only + best audio, hoặc `22`/`18` cho combined)
- **YouTube Shorts**: thường chỉ có m3u8 HLS streams. Pick `96` (1080p) hoặc `95` (720p) — chọn variant có audio
- **TikTok**: thường có format `h264` + `aac` ready-to-play

### Step 2: Download
```bash
cd ~/Downloads
yt-dlp -f <FORMAT_ID> --merge-output-format mp4 \
  -o "VIDEO_ID.%(ext)s" "URL"
```

**Filename convention:** `VIDEO_ID.mp4` (11-char YouTube ID hoặc TikTok video ID). KHÔNG dùng tên dài.

### Step 3: Verify with ffprobe
```bash
ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 FILE.mp4
```

**Sanity checks:**
- `duration` > 0 (tránh file rỗng)
- `width` x `height` hợp lý (Shorts = 1080x1920, normal YouTube = 1920x1080 hoặc 1280x720)
- Có `codec_name=h264` (video) và `aac` (audio) — Telegram play được

**Red flag:** Nếu file < 200KB mà video > 10s → có thể chỉ tải được 1-2 fragment của HLS. Re-download với format khác.

### Step 4: Resend via Telegram
```bash
# Use send_message with MEDIA: prefix
send_message(
  action="send",
  target="telegram",
  message="📹 **VIDEO_ID.mp4**\n- Resolution: WxH\n- Duration: X.Xs\n- Codec: H.264 + AAC\n- Size: X.XMB\n\nMEDIA:/Users/tuananh4865/Downloads/VIDEO_ID.mp4"
)
```

**Telegram limits:**
- Timeout > 50MB → luôn compress nếu file lớn
- 720p H.264 + AAC thường đủ nhẹ (< 50MB cho video < 10 phút)
- Shorts thường < 10MB, không cần compress

## Common Pitfalls

### 1. yt-dlp tải HLS fragments không đầy đủ
Triệu chứng: file 100KB-200KB cho video dài 1+ phút. yt-dlp log hiện ra `ETA Unknown` và fragments size lởm (`~1.00KiB`, `~3.00KiB`...) — **ĐỪNG PANIC**, đây chỉ là m3u8 HLS stream estimate, file output vẫn đúng.
Fix: thêm `--hls-prefer-native` hoặc thử format khác (96 thay vì 95 cho Shorts).

**Verify sau khi tải** bằng ffprobe:
- `duration` phải khớp video gốc (không phải 0)
- `size` > 1MB cho video > 30s
- Codec h264 + aac (không phải video-only stream)

### 2. Short URL không resolve
Triệu chứng: `youtube.com/shorts/ID?si=...` — query string `?si=` thỉnh thoảng làm yt-dlp confused.
Fix: strip query string hoặc dùng full URL `https://www.youtube.com/shorts/ID`.

### 3. Format 95 vs 96 cho Shorts
- Format `95` = 720p HLS stream (~105KB hint nhưng thực tế ~5MB khi full)
- Format `96` = 1080p HLS stream
- Pick format có sẵn audio track (look cho `mp4a.40.2` = AAC, không phải video-only).

### 4. File downloaded to wrong location
Mặc định `yt-dlp` lưu vào cwd. **LUÔN `cd ~/Downloads` trước khi tải** để file nằm đúng chỗ anh expect.

### 5. Don't waste time analyzing
Khi anh chỉ muốn file về → KHÔNG phân tích nội dung video, KHÔNG transcript, CHỈ tải + gửi. Nếu anh muốn phân tích thêm thì hỏi sau khi file đã gửi.

### 6. "Tải về" + "Transcript" trong cùng request
Khi anh gửi link + nói "transcript" / "phân tích" / "review" → đây là **compound request**:
1. **First**: tải video về (workflow này) → gửi MEDIA:
2. **Then**: trigger transcript extraction → gửi transcript qua Telegram text
3. **Then**: nếu anh nói "phân tích" → thêm phần phân tích nội dung theo style kênh anh

KHÔNG skip bước 1 (gửi file) kể cả khi anh chỉ focus vào transcript — anh expect file + text cùng lúc.

Khi transcript needed → load skill `youtube-transcript-extractor` (đã có Vietnamese Subtitle Strategy + Local Whisper Fallback cho video không có sub).

## Sample End-to-End Command

```bash
# 1. List formats
yt-dlp -F "https://youtube.com/shorts/p7d0k_QDFhs"

# 2. Pick format 96-2 (1080p with Vietnamese original audio)
cd ~/Downloads
yt-dlp -f 96-2 --merge-output-format mp4 \
  -o "p7d0k_QDFhs.%(ext)s" "https://youtube.com/shorts/p7d0k_QDFhs"

# 3. Verify
ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 p7d0k_QDFhs.mp4
# → codec_name=h264, width=1080, height=1920, duration=94.6, size=4.4M ✓

# 4. Send via send_message with MEDIA: prefix
```

## Related
- [[transcript-cleanup]] — Cleanup media files sau khi dùng xong (tránh đầy disk)
- [[youtube-transcript-extractor]] — Extract transcript (KHÁC: workflow này giữ video, gửi qua Telegram)
- Memory: "yt-dlp → ffprobe streams → ffmpeg 720p H.264 AAC → send MEDIA:/path"
