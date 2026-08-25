# Clip 0003 V7.1 Final - Dodoto Lux Air V3 (Case Study 18/07/2026)

> **V7.1 SHIPPED:** `clip0003_V71_82s_FINAL.mp4` (45.4 MB, 81.75s) tại `/Volumes/Storage-1/Pocket3/Hermes-Edit/`
> **Verified:** face motion d(1-35)=364, hand mic d(1-20)=317, face mouth d(1-20)=195. Glass visible 4 phase: HOOK 175, INTRO 162, USP 122, CTA-FINAL 125.
> **V8 features applied:** text motion stagger 120ms + mask transition + gradient shift + camera shake.

## Source

- Path: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0003_V3_troncau_may-hut-bui-cam-tay-2in1_speed13.mp4`
- Size: 77.8 MB | Duration: 81.78s (speed 1.3x) | 1080×1920, H.264 + AAC
- Content: talking head + mic DJI về máy hút bụi cầm tay Dodoto Lux Air V3

## V7.1 Specs Applied

| Property | V7 (cũ) | **V7.1 (verified)** |
|---|---|---|
| Opacity | 0.15 | **0.18** (dày hơn) |
| Blur | 40px | **48px saturate 200%** |
| Border | 0.32 | **0.4** |
| Border-radius | 32px | **36px** |
| **Box-shadow** | 0 14px 42px 0.55 | **0 20px 56px 0.5** (cân bằng) |
| Padding | 30px 24px | **40px 36px** |
| Title | 48-56px | **64-72px** |
| Eyebrow | 26px | **36-48px** (Caveat font optional) |
| Number | 96-120px | **128-160px** |

## 8 Phases (V22 verified layout)

1. **HOOK** (0-7s): "Máy hút bụi cầm tay?" - glass top:1308
2. **PROBLEM** (7-15s): 3 step 01/02/03 - glass top:1288
3. **INTRO** (15-24s): "2 in 1 Máy Hút VÀ Máy Thổi" - glass top:1308
4. **SPECS** (24-37s): "25.000 Pa lực hút" - glass top:1308 + gradient shift cyan
5. **USP** (37-52s): "Cầm tay - nhỏ gọn" - glass top:1308 + gradient shift gold + camera shake
6. **USE-CASE** (52-61s): "Dùng cho ô tô - bàn" - glass top:1308
7. **CTA-TEST** (61-73s): "Bạn nào quan tâm? 495K" - glass top:1308
8. **CTA-FINAL** (73-82s): liquid glass 80% + 3 specs + 495K + SHOP DODOTO

## V8 Features Applied (Nate Herk alignment)

1. **Text motion stagger 120ms** với clipPath reveal từng dòng
2. **Mask transition** `clipPath: circle(0% → 150%)` mỗi phase
3. **Background gradient shift subtle** (cyan/gold/red tint theo phase)
4. **Camera shake subtle** ở USP + CTA-FINAL (~1.5-2px)
5. **Caveat font import** (Google Fonts ready) - chưa dùng vì title SF Pro đã rõ

## HyperFrames Workflow V22 (5-step verified)

1. **HTML**: `background: transparent` + `<video id="video-bg">` direct child of root
2. **Render silent**: `npx hyperframes render --format mov --output output_silent.mov` (alpha channel)
3. **FFmpeg ghép**: 
```bash
ffmpeg -y -i source.mp4 -i output_silent.mov \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS-STARTPTS[bg]; [1:v]scale=1080:1920,format=yuva420p,setpts=PTS-STARTPTS[v1]; [bg][v1]overlay=0:0:eof_action=pass[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset fast -crf 23 -c:a copy -shortest output_FINAL.mp4
```
4. **Verify 4 vùng** (face/chin/hand/background) - threshold d(1-N) > 100
5. **Ship file** vào Pocket3 với audio AAC 44100Hz

## Motion Verification (4-region diff)

| Region | d(1-20) | d(1-35) | d(1-50) | d(1-78) | Status |
|---|---:|---:|---:|---:|---|
| Top background | 21 | 12 | 15 | 32 | (always static) |
| Face mouth Y=900 | 195 | 86 | 3 | 28 | ✅ MOTION |
| Face chin Y=1100 | **303** | **364** | **213** | **138** | ✅ **MOTION RÕ** |
| Hand mic X=600 | **317** | 173 | 92 | 111 | ✅ MOTION |

## Glass Card Verification (4 phase brightness)

| Phase | Glass RGB | Brightness | Status |
|---|---|---:|---|
| HOOK (5s) | (215, 167, 144) | 175 | ✅ YES |
| INTRO (20s) | (156, 166, 165) | 162 | ✅ YES |
| USP (50s) | (151, 113, 102) | 122 | ✅ YES |
| CTA-FINAL (78s) | (171, 107, 98) | 125 | ✅ YES |

## Wiki Product Ground Truth Specs

- **25.000 Pa** lực hút (verified từ `wiki/projects/tuan-anh-review-tiktok/products/dodoto-lux-air-v3-...md`)
- **140W** công suất
- **400g** siêu nhẹ
- **495K** giá bán
- **24 tháng** bảo hành + 1 đổi 1
- **2 in 1** hút + thổi
- **HÀNG CHÍNH HÃNG SHOP DODOTO**

## Lesson Learned (FIRST-CLASS)

**Source talking head của anh gần như static ở top background NHƯNG motion thật ở face/chin/hand mic** (diff 150-400). Em đã fail 4 lần (V4/V5/V6/V5_proper) vì chỉ check pixel ở top-left corner (background) → báo "STATIC" sai. V7.1 fix bằng 4-region verify protocol.

**Anti-pattern (tuyệt đối KHÔNG):**
- ❌ Check pixel ở 1 vùng duy nhất (top-left) → báo sai
- ❌ Báo "clip bị đơ" khi chỉ check background
- ❌ Skip verify phase animation thay vì check glass brightness
- ❌ Tin báo cáo cũ khi chưa verify lại bằng 4-vùng

**Workflow V7.1 ship:**
1. Build V7.1 index.html với 8 phase + V8 features
2. Render `--format mov` (alpha)
3. FFmpeg ghép với `format=yuva420p` (giữ motion source)
4. Verify 4 vùng pixel diff (face/chin/hand > 100 = MOTION)
5. Verify 4 phase glass brightness > 100
6. Ship file với audio AAC 44100Hz

## Files Saved

- Source: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0003_V3_troncau_..._speed13.mp4`
- Final: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip0003_V71_82s_FINAL.mp4` (45.4 MB)
- Working dir: `/tmp/hf_clip0003_V71_proper/`
- HyperFrames render: `output_silent.mov` (2.4 GB intermediate)
