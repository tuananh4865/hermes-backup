# TikTok Full Video Path — Session 2026-06-18 (Content Creator)

## Discovery

Khi `yt-dlp -F URL` trả về **multiple formats** (video mp4 + audio kèm theo) → TikTok cho phép download full MP4. Khác với audio-only case 13/06, lần này em get được video 5.6MB đầy đủ.

**Confirmed example session 18/06:** `https://vt.tiktok.com/ZSQt1SY3m/` (video "ánh sáng 0đ", 43s, @hi.imdung style hoặc tương tự).

## Workflow (4 bước, ~30s end-to-end)

```bash
# Step 1: Download full MP4 (no format flag, default = best)
cd ~/Downloads
yt-dlp --no-warnings --quiet \
  -o "tiktok-anh-sang-0d.%(ext)s" \
  "https://vt.tiktok.com/ZSQt1SY3m/"
# → 5.6MB MP4 trong 3 giây

# Step 2: Extract audio 16kHz mono WAV
ffmpeg -y -i tiktok-anh-sang-0d.mp4 \
  -vn -acodec pcm_s16le -ar 16000 -ac 1 \
  /tmp/tiktok-anh-sang-0d.wav
# → 1.4MB WAV trong 1 giây

# Step 3: Whisper SRT (force Vietnamese)
mlx_whisper /tmp/tiktok-anh-sang-0d.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language vi --task transcribe \
  --output-dir /tmp/tiktok-transcript --output-format srt
# → 25 segments trong 20 giây (trên M1/M2)

# Step 4: Visual frame analysis (optional, khi cần hiểu hook layout)
mkdir -p /tmp/anh-sang-0d-frames
ffmpeg -y -i tiktok-anh-sang-0d.mp4 -vf fps=1 /tmp/anh-sang-0d-frames/frame_%02d.jpg
# 12 frames trong 1 giây
# Dùng mcp_MiniMax_understand_image trên 3-4 frame quan trọng
```

## Khi nào dùng full video path thay vì audio-only

| Use case | Path |
|----------|------|
| Phân tích competitor (hook layout, text overlay, B-roll, framing) | **Full video** ✅ |
| Research viral framework (visual + voiceover structure) | **Full video** ✅ |
| Lấy text quote cho blog/Twitter thread | **Full video** ✅ |
| Chỉ cần transcript text cho translate/notes | Audio-only (nhanh hơn 5-10s) |
| Video > 5 phút | Audio-only (file lớn, download chậm) |

## Tại sao quan trọng cho Content Creator

Session 18/06 phát hiện 1 video TikTok "ánh sáng 0đ" 43s dùng framework "Contradiction + Con số cụ thể + Show 3 cases + Specific CTA". Áp dụng framework này vào 15 ÁNH SÁNG scripts của project, có khả năng tăng retention + share rate. Nếu chỉ dùng audio-only path, em sẽ miss hoàn toàn:
- Visual hook "0Đ = ĐÈN 5TR" text overlay
- Mirror effect + grayscale filter
- 3 cases visual (ngược sáng / chính diện / nghiêng 45°)
- Text overlay animation (fade in/out theo step)

## Pitfalls đã gặp (18/06)

1. **Lần đầu em cố dùng `vision_analyze` local** — fail với "No models loaded. Please load a model in the developer page or use the 'lms load' command." Dù LM Studio server ON port 1234, không có model nào cached. **Fix: dùng `mcp_MiniMax_understand_image` thay thế, work ngay với file path local.**

2. **Lần đầu em extract 12 frames 1 lúc rồi gọi vision từng cái** — chậm vì phải đợi 4 round-trips. **Fix: chỉ check 3-4 frame QUAN TRỌNG** (frame_00 hook, frame_N body, frame_last CTA). Whisper SRT đã cho biết timestamp các phần, dùng timestamp đó để chọn frame chính xác.

3. **Anh nhắc "Tải video về được thì dùng whisper mà transcript cho nhanh chứ!"** — em đang mất 5 phút check frame-by-frame thay vì 20s whisper. **Lesson: KHI USER GỬI VIDEO TIKTOK, LUÔN BẮT ĐẦU BẰNG WHISPER SRT (audio path) TRƯỚC. Chỉ extract frames khi cần visual analysis chi tiết.** User rất ghét lãng phí thời gian xử lý 1 cách chậm.

## Files output từ session 18/06

- `~/Downloads/tiktok-anh-sang-0d.mp4` (5.6MB)
- `/tmp/tiktok-anh-sang-0d.wav` (1.4MB, intermediate)
- `/tmp/tiktok-transcript/tiktok-anh-sang-0d.srt` (1946 bytes, 25 segments)
- `/tmp/anh-sang-0d-frames/frame_00.jpg` → `frame_11.jpg` (12 frames)
- Wiki deliverable: `wiki/projects/content-creator/research/competitor-anh-sang-0d-tiktok-2026-06.md` (9.8KB)

## Transcript highlight từ video này (sample)

```
1
00:00:00,000 --> 00:00:02,200
Cách đúng ngồi nghiêng 45 độ so với cửa sổ

2
00:00:02,200 --> 00:00:04,920
Cửa sổ nhà bạn đang là cái đèn studio 5 triệu mà bạn không hề biết

3
00:00:04,920 --> 00:00:06,720
Cùng là tôi, cùng chiếc điện thoại này

(... 22 segments nữa)

20
00:00:32,460 --> 00:00:35,960
Cùng nội dung, ánh sáng quyết định 80% người ta có xem tiếp video của bạn hay không
```

**Key insights extracted:** 4-part framework (Proof → Problem → Solution → Payoff), "Contradiction + Con số" hook, 3 cases trong 1 video, "Specific action + Tease ngày mai" CTA, 0% bán hàng.

## Speed comparison

| Path | Time | Output |
|------|------|--------|
| Full video + SRT (no visual) | 25s | MP4 + SRT |
| Full video + SRT + 4 frames visual | 35s | MP4 + SRT + 4 frames analyzed |
| Full video + SRT + 12 frames visual | 60s | MP4 + SRT + 12 frames analyzed |
| Audio-only + SRT | 25s | MP3 + SRT (no video) |

Default: full video + SRT (no visual) → anh sẽ tell em nếu cần visual dive deeper.
