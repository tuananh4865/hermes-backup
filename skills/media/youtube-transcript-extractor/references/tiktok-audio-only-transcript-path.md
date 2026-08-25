# TikTok Audio-Only Path — Transcript Session 2026-06-13

## Discovery

Khi `yt-dlp -F URL` chỉ hiện `audio mp3 audio only | https | audio only mp3` (chỉ 1 format duy nhất, audio-only) → TikTok video KHÔNG cho download video stream, chỉ cho audio. **Đây là format mới của TikTok** (impersonation/auth wall), kể cả khi xem video vẫn có hình bình thường trên app.

## Ví dụ từ session 2026-06-13

URL: `https://vt.tiktok.com/ZSQm9pYrV/` (resolves to `@tuan_anh.review` video 7650439370519940370)

```
$ yt-dlp -F "https://vt.tiktok.com/ZSQm9pYrV/"
[info] Available formats for 7650439370519940370:
ID    EXT RESOLUTION | PROTO | VCODEC     ACODEC
---------------------------------------------------
audio mp3 audio only | https | audio only mp3
```

`yt-dlp -f best` cũng rơi xuống audio-only này. Format "best" sẽ trigger warning nhưng vẫn work.

## Workflow cho TikTok audio-only

### Step 1: Download MP3 trực tiếp (skip video extraction)
```bash
cd ~/Downloads
yt-dlp -f best --merge-output-format mp3 \
  -o "tiktok-VIDEO_ID.%(ext)s" "https://vt.tiktok.com/XXX/"
# hoặc: yt-dlp -f audio -o "tiktok-VIDEO_ID.%(ext)s" URL
```

### Step 2: Feed MP3 trực tiếp vào Whisper (NO ffmpeg step needed)
```bash
mlx_whisper --model mlx-community/whisper-large-v3-mlx \
  --output-format txt \
  --output-name tiktok-VIDEO_ID-transcript \
  /Users/tuananh4865/Downloads/tiktok-VIDEO_ID.mp3
```

mlx-whisper tự xử lý MP3 → WAV decode internally. Skip bước `ffmpeg -i mp4 → wav`.

### Step 3: Read transcript
```bash
cat /tmp/tiktok-VIDEO_ID-transcript.txt
```

## Tại sao quan trọng

- TikTok hiện đang chặn video stream download từ phần lớn region/format (impersonation target missing trong yt-dlp warning)
- Workaround: vẫn lấy được audio → Whisper → transcript
- Trade-off: MẤT video file, chỉ có audio. Nếu anh muốn xem video → phải dùng browser-harness hoặc computer_use để capture từ web (KHÔNG có workflow tự động reliable)

## Nếu anh muốn cả video + transcript TikTok

Phải dùng 2 bước:
1. **Audio-only download + Whisper** (workflow này) → transcript text
2. **Browser-based video download** (skill `browser-harness`) → mở TikTok URL trong Chrome, lưu file bằng DevTools network tab

CHƯA có end-to-end automated pipeline. Manual workflow only.

## Tham khảo

- Source: `~/Downloads/tiktok-ZSQm9pYrV.mp3` (745KB, 47s audio)
- Transcript: `/tmp/tiktok-ZSQm9pYrV-transcript.txt`
- Whisper: `mlx-community/whisper-large-v3-mlx` (cached)
- Detected language: Vietnamese (auto-detect chuẩn 47s audio)
