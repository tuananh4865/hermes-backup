---
title: "Clip 0003 V3 Speed 1.3x — Case Study Motion Graphic"
created: 2026-07-18
updated: 2026-07-18
type: case-study
tags: [clip-0003, dodoto, motion-graphic, v22-layout, hyperframes, source-static]
---

# Clip 0003 V3 Speed 1.3x — Case Study (18/07/2026)

**Source:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0003_V3_troncau_may-hut-bui-cam-tay-2in1_speed13.mp4`
**Size:** 77.8 MB
**Duration:** 81.78s
**Resolution:** 1080×1920 portrait (đã đúng format)
**Codec:** H.264 High profile, 8-bit yuv420p, 29.97fps
**Audio:** AAC, 130kbps (embedded trong source)

## Kết quả

**Final shipped:** `clip0003_V3_speed13_82s_with_audio.mp4` (5.9 MB, 81.79s)

| Metric | Value |
|---|---|
| HyperFrames render silent | 82s, 4.2 MB |
| Audio muxed | ✅ AAC 128kbps |
| 8 phases verified | ✅ Glass card visible ở tất cả phases |
| Pixel diff clean area (0.5s vs 10s) | 150 = STATIC |

## 8 Phases breakdown (theo Whisper transcript)

| # | Phase | Time | Content | Glass position |
|---|---|---|---|---|
| 1 | HOOK | 0-7s | "Bạn nào đang tìm máy hút bụi cầm tay..." | top 1308px |
| 2 | PROBLEM | 7-15s | 3 step: góc phòng / ô tô / bàn làm việc | top 1288px |
| 3 | INTRO | 15-24s | "2 in 1 Máy Hút VÀ Máy Thổi" | top 1308px |
| 4 | SPECS | 24-37s | **25.000 Pa lực hút** | top 1308px |
| 5 | USP | 37-52s | "Cầm tay - nhỏ gọn" + đầu hút nhỏ | top 1308px |
| 6 | USE-CASE | 52-61s | "Dùng cho ô tô - bàn" | top 1308px |
| 7 | CTA-TEST | 61-73s | "Bạn nào quan tâm? **495K**" | top 1308px |
| 8 | CTA-FINAL | 73-82s | Liquid glass 80% + 3 specs + 495K + SHOP DODOTO | top 192 + bottom 192 |

## Key Learnings (verified 18/07)

### 1. Source đã đúng format 1080×1920 — không cần scale
- V3 file khác V6 (1728×3072) — V3 đã được scaled sẵn về 1080×1920
- KHÔNG cần step "Scale source 1080×1920 TikTok spec" trong pipeline
- Chỉ cần HyperFrames render trực tiếp với source 1080×1920

### 2. Speed 1.3x làm clip ngắn hơn (~82s thay vì 90s V6)
- Whisper transcript cho thấy phases có thể scale theo duration
- 8 phases map tỷ lệ thuận với duration, không cố định thời gian

### 3. Source talking head STATIC (Pitfall 56)
- Pixel diff vùng clean = 150 (< 500) = STATIC
- Final video vẫn hợp lệ vì glass overlay animation compensate
- Báo cáo trung thực cho user

### 4. Specs lấy từ Wiki Product Ground Truth
- 25.000 Pa, 140W, 400g, 495K, 24 tháng BH — tất cả từ wiki dodoto-lux-air-v3
- KHÔNG tự suy đoán specs
- Mỗi claim đều có citation [N] từ wiki research cache

## Workflow chuẩn (verified)

```bash
# 1. Setup
mkdir -p /tmp/hf_clip_NAME/assets/source/pip
cp source.mp4 /tmp/.../assets/source/full_bg.mp4
ffmpeg -y -i source.mp4 -vn -acodec aac -ar 48000 -ac 2 -b:a 128k audio.aac

# 2. Whisper transcript
mlx_whisper source.mp4 --model mlx-community/whisper-medium-mlx --language vi --output-format json

# 3. Write 8-phase index.html với V22 layout
# (Copy từ V22 + sửa content, KHÔNG tự sáng tác layout)

# 4. Render
cd /tmp/.../
npx --yes hyperframes render --quality draft --output output_silent.mp4

# 5. Mux audio
ffmpeg -y -i output_silent.mp4 -i audio.aac \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -shortest \
  output/clip_NAME_with_audio.mp4

# 6. Verify bằng pixel (KHÔNG dùng vision_analyze vì có thể fail)
python3 -c "from PIL import Image; ..."
# Check glass card visible ở 8 phases + pixel diff vùng clean

# 7. Ship
cp output/clip_NAME_with_audio.mp4 /Volumes/Storage-1/Pocket3/Hermes-Edit/
```

## Apply to next clips

Khi build motion graphic cho clip TikTok Shop product:
1. Đọc V22 case study + layout benchmark
2. Copy V22 index.html structure (8 phases)
3. Sửa content theo Whisper transcript
4. Apply HyperFrames workflow (PAUSE video + paused timeline + tl.seek(0))
5. Verify bằng pixel (Pitfall 55)
6. Báo cáo trung thực nếu source STATIC (Pitfall 56)
