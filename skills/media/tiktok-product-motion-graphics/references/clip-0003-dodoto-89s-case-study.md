---
title: "Clip 0003 - Dodoto Lux Air V3 89.6s motion graphic case study"
created: 2026-07-17
verified: yes
clip_id: clip_0003_Final_troncau_may-hut-bui-cam-tay-2in1.mp4
product: Dodoto Lux Air V3 (máy hút bụi cầm tay 2-in-1)
source_duration: 89.6 seconds
output_duration: ~90 seconds (V4 final)
related_versions: V4 of clip 0003 (V1-V3 already existed from prior session 16/07)
status: shipped + audio muxed
---

# Clip 0003 - Dodoto Lux Air V3 motion graphic (89.6s, V4)

> **Trích từ session 17/07/2026 22:30-22:55:** anh gửi clip 0003 (Dodoto Lux Air V3 89.6s talking-head product review) và nói *"Giờ làm motion cho clip 0003 trong Hermes-edit đi"*. Em đã base trên V22 layout (đã verified sẵn từ sạc dự phòng V1→V22 cycle) và extend cho clip dài 90s.

## Source clip
- Path: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0003_Final_troncau_may-hut-bui-cam-tay-2in1.mp4`
- Size: 52.8 MB | Duration: 89.6s | 1080×1920 portrait | H.264 + AAC 44100Hz

## Product verified data (wiki +4 citations)
- **Brand:** Dodoto (Vietnam brand, MST VN, OEM Trung Quốc)
- **Giá:** 495,000 VND
- **Specs:** 140W + 25,000Pa + 400g + sạc Type-C + pin lithium
- **Features:** Hút + thổi 2-in-1, hộp đựng + nhiều đầu hút/thổi tặng kèm
- **Bảo hành:** 24 tháng 1 đổi 1, dùng thử 15 ngày

## Transcript (Whisper medium-mlx verified)
Phases breakdown từ transcript:
- 0-12s: HOOK
- 12-20s: PROBLEM
- 20-30s: INTRO (2 in 1)
- 30-45s: SPECS (25.000Pa)
- 45-60s: USP
- 60-75s: USE-CASE (ô tô)
- 75-85s: CTA-TEST
- 85-90s: CTA-FINAL

## V4 implementation

**Base**: V22 layout coordinates (giữ nguyên, extend timeline)
**Phases**: 8 phase (HOOK/PROBLEM/INTRO/SPECS/USP/USE-CASE/CTA-TEST/CTA-FINAL)
**Glass opacity**: 0.15
**Bỏ watermark @tuancuaban**: ✓
**Bỏ caption bar**: ✓
**Bỏ "ANH ĐANG NÓI"**: ✓

### 8 phase positions (scaled cho 89.6s)
| Phase | Time (s) | Glass Y | Content |
|---|---|---|---|
| 1. HOOK | 0-12 | bottom 200px | Hook question |
| 2. PROBLEM | 12-20 | bottom | 3 step problem |
| 3. INTRO | 20-30 | bottom | "2 in 1" feature |
| 4. SPECS | 30-45 | 1020 (center mid) | "25.000Pa" + 140W + 24 tháng BH |
| 5. USP | 45-60 | bottom | "Cân bằng lực hút - gọn nhẹ" |
| 6. USE-CASE | 60-75 | bottom | "Dùng cho ô tô..." |
| 7. CTA-TEST | 75-85 | bottom | "Bạn nào quan tâm? 495K + bấm link" |
| 8. CTA-FINAL | 85-89.6 | top 192 (80% height big card) | "Hết video + 495K + HÀNG CHÍNH HÃNG" |

## Pipeline (verified)

```bash
# Setup assets
mkdir -p /tmp/hf_clip0003_v4/{assets/source/pip,output}
ffmpeg -y -i source.mp4 -an -c:v copy assets/source/full_bg.mp4
ffmpeg -y -i source.mp4 -vn -c:a aac -b:a 128k assets/source/audio.aac

# Whisper MLX transcript (Pitfall 48)
mlx_whisper source.mp4 --model mlx-community/whisper-medium-mlx --language vi \
  --output-format json --output-dir /tmp/clip_0003_whisper_mlx

# Render silent
cd /tmp/hf_clip0003_v4
npx --yes hyperframes render --quality draft --output output_silent.mp4

# Mux audio (Pitfall 1 - render is silent)
ffmpeg -y -i output_silent.mp4 \
    -i assets/source/audio.aac \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -shortest \
    output/sac_du_phong_clip0003_v4_90s_with_audio.mp4
```

## Kết quả verify
- File: `sac_du_phong_clip0003_v4_90s_with_audio.mp4` → 6.8 MB
- Frame HOOK 5s: ✅ HOÀN HẢO - glass "Bạn nào đang tìm Máy hút bụi góc nhỏ, góc phòng?"
- Frame INTRO 25s: ✅ HOÀN HẢO - glass "Đặc điểm / 2 in 1 / Máy Hút VÀ Máy Thổi"

## Lessons cho future product clips > 60s

1. **KHÔNG redesign** - extend V22 layout, keep Y coordinates verified
2. **Match data-duration** with source clip trên `#root` element (Pitfall tránh rồi)
3. **GSAP timeline duration** phải match
4. **CTA-FINAL phase** luôn reserve 5s cuối với liquid glass card lớn 80% (Pitfall 44/45)
5. **PIP crops** không cần cho talking-head phases
6. **CTA-TEST phase** trước CTA-FINAL để show price + CTA early

## Pitfalls avoided (theo skill tiktok-product-motion-graphics)
- ✅ Pitfall 47 - Single-file composition (90s vẫn ổn)
- ✅ Pitfall 48 - Whisper medium-mlx (large-v3 hallucinate)
- ✅ Pitfall 49 - (face detection không cần cho talking-head)
- ✅ Pitfall 46 - Single surgical write_file (không patch nhiều lần)
- ✅ Pitfall 50 - Recycle V22 base (không build mockup mới)
- ✅ Wiki Product Ground Truth - 4 citations cho Dodoto verified
