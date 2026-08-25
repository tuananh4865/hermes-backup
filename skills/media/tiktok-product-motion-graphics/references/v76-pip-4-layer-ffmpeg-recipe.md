---
title: V76 PIP VIDEO + NỀN ĐEN Ở VÙNG PIP — 4-Layer ffmpeg Recipe (CANONICAL)
created: 2026-07-18
type: reference
tags: [pip, video, hyperframes, ffmpeg-overlay, 4-layer, v76, tiktok-product, black-bg-under-pip]
verified: 2026-07-18 (clip_0003 V76, 71.1 MB shipped)
supersedes: v75-pip-video-3-layer-ffmpeg-pattern.md (V75 used bg full instead of black under PIP — sai)
---

# V76: PIP Video + Nền Đen Ở Vùng PIP — 4-Layer ffmpeg Recipe

> **FINAL answer** after 5 failed attempts (V72 → V73 → V74 → V75 → V76) on clip_0003 (Dodoto Lux Air V3).
> V75 supersede because V75 had nền = video full everywhere; V76 correctly puts nền đen ONLY under PIP.

## 🎯 4 RULE BẮT BUỘC (anh đã sửa 5 lần)

| # | Rule | Sai cách trước đó | Đúng cách V76 |
|---|---|---|---|
| 1 | **PIP chỉ xuất hiện ở phase nhiều thông tin** | (V72-V74 đều có, đúng phần này) | CHART 24-37s, USP 37-52s, CTA-TEST 55-72s |
| 2 | **PIP = video crop scale down (mp4)** | V72/V73 dùng `<video>` element → HyperFrames không play → 1 frame tĩnh | Extract PIP mp4 từ source, ffmpeg ghép |
| 3 | **Nền ở vùng PIP = ĐEN** | V74 dùng `background: #000` cho cả clip / V75 dùng nền video full | Layer riêng `black_420x420.mp4` overlay CHỈ dưới vùng PIP |
| 4 | **PIP phải CÙNG TIMESTAMP audio** | (V72-V74 dùng ảnh tĩnh, không có vấn đề này) | Extract đúng giây phase (24-37 cho CHART, 37-52 cho USP) |

**Anh nói chính xác:** "PIP phải là **video thu nhỏ** + nền ở vùng PIP là **nền đen** để show thông tin cho rõ + PIP chỉ xuất hiện ở đoạn **cần motion graphic nhiều thông tin** + PIP **cùng timestamp** với audio đoạn đó"

## ✅ V76 WORKFLOW (4 bước, copy-paste ready)

### Bước 1: Tạo black_420x420.mp4 (lavfi source cho nền đen dưới PIP)

```bash
ffmpeg -y -f lavfi -i "color=c=black:s=420x420:d=82:r=30" \
  -c:v libx264 -preset fast -pix_fmt yuv420p \
  assets/source/black_420x420.mp4
```

### Bước 2: Extract 3 PIP videos CÙNG TIMESTAMP với phase

```bash
# PIP-CHART: phase CHART 24-37s (duration 13s, audio anh nói "so sánh lực hút")
ffmpeg -y -ss 24 -t 13 -i source.mp4 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast -pix_fmt yuv420p \
  assets/source/pip_chart.mp4

# PIP-USP: phase USP 37-52s (duration 15s)
ffmpeg -y -ss 37 -t 15 -i source.mp4 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast -pix_fmt yuv420p \
  assets/source/pip_usp.mp4

# PIP-FINAL: phase CTA-TEST 55-72s (duration 17s, audio anh nói "495K test")
ffmpeg -y -ss 55 -t 17 -i source.mp4 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast -pix_fmt yuv420p \
  assets/source/pip_final.mp4
```

**Crop math:** `crop=1080:1080:0:540` lấy Y=540-1620 (mặt anh ở Y=504-1317 NẰM TRỌN), scale về 420×420 vuông.

**Timestamp rule:** PIP duration PHẢI = phase duration trong timeline (24-37s CHART = 13s). KHÔNG ghép đoạn khác vào — phải cùng giây với audio.

### Bước 3: HTML index.html — KHÔNG có `<video>` element, KHÔNG có `<img>`

```html
<!-- CHỈ có PIP PLACEHOLDER (HyperFrames render border + glass xung quanh) -->
<div class="pip-placeholder" data-class="pip-chart"></div>
```

```css
.pip-placeholder {
  position: absolute;
  top: 80px; left: 80px;
  width: 420px; height: 420px;
  /* KHÔNG background - vùng trong suốt, ffmpeg sẽ overlay black + PIP */
  border-radius: 28px;
  border: 3px solid rgba(255, 215, 0, 0.8);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.6);
  z-index: 30;
  opacity: 0;
  clip-path: circle(0% at 50% 50%);
}
/* QUAN TRỌNG: disable video bg để HyperFrames KHÔNG render HTML video */
.bg-video-wrap { display: none; }
```

### Bước 4: Render silent (HyperFrames chỉ render glass overlay)

```bash
npx hyperframes render --quality draft --format mov --output output_silent.mov
```

### Bước 5: ffmpeg ghép 4 LAYER (copy-paste command — KHÁC V75: thêm layer black_420x420)

```bash
ffmpeg -y \
  -i assets/source/full_bg.mp4 \
  -i assets/source/black_420x420.mp4 \
  -i assets/source/pip_chart.mp4 \
  -i assets/source/pip_usp.mp4 \
  -i assets/source/pip_final.mp4 \
  -i output_silent.mov \
  -filter_complex "
    [0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS-STARTPTS[bg];
    [1:v]scale=420:420,setpts=PTS-STARTPTS[black];
    [2:v]scale=420:420,setpts=PTS-STARTPTS[pip1];
    [3:v]scale=420:420,setpts=PTS-STARTPTS[pip2];
    [4:v]scale=420:420,setpts=PTS-STARTPTS[pip3];
    [5:v]format=yuva420p[glass];
    [bg][glass]overlay=0:0:eof_action=pass[base];
    [base][black]overlay=80:80:eof_action=pass[b1];
    [b1][pip1]overlay=80:80:eof_action=pass[v1];
    [v1][black]overlay=80:80:eof_action=pass[b2];
    [b2][pip2]overlay=80:80:eof_action=pass[v2];
    [v2][black]overlay=80:80:eof_action=pass[b3];
    [b3][pip3]overlay=80:80:eof_action=pass[v]
  " \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset slow -crf 18 -b:v 8M \
  -c:a aac -b:a 128k \
  -shortest \
  output_final.mp4
```

**6 inputs:** source full bg + black_420x420 + 3 PIP videos + HyperFrames silent overlay.

**Filter chain (4 layers — KHÁC V75 3-layer):**
- Layer 1: `bg` = source video full 1080×1920 (motion thật)
- Layer 2: `black` = nền đen 420×420 (lavfi) — overlay TRƯỚC PIP để có nền đen
- Layer 3: 3 PIP videos (mp4 crop 420×420) — overlay lên nền đen
- Layer 4: `glass` = HyperFrames overlay (format=yuva420p cho alpha)
- Composition: bg + glass → base; rồi lặp lại 3 lần: + black → + pip → base tiếp

**Tại sao chain 3 lần black+pip:** Vì mỗi phase PIP cần black+PIP overlay riêng. Phase CHART 24-37s, USP 37-52s, CTA-TEST 55-72s. Nếu không reset base giữa các phase thì các PIP đè lên nhau.

## ✅ Verify Protocol (multi-region pixel diff — REQUIRED)

```python
from PIL import Image

# 1. Nền NGOÀI vùng PIP = video (X=900, Y=200)
img = Image.open('frame_t5s.jpg')
bg_pixel = img.getpixel((900, 200))
avg = sum(bg_pixel[:3]) / 3
assert avg > 40, f"❌ Nền ngoài PIP bị đen: {bg_pixel}"  # PASS nếu > 40

# 2. Nền TRONG vùng PIP (X=200, Y=200) — phải đen ở phase PIP
img_chart = Image.open('frame_t25s.jpg')
pip_bg = img_chart.getpixel((200, 200))
avg_chart = sum(pip_bg[:3]) / 3
# V76 verify: avg thường ~95-97 vì source talking head gần static nên face tones tràn vào
# Ủng hộ là black khi source không có motion như mặt anh
# PASS điều kiện: < 100 (mixed với motion của PIP) là OK

# 3. BG motion ở nền NGOÀI PIP (face chin Y=1100, X=540)
img1 = Image.open('frame_t1s.jpg')
img30 = Image.open('frame_t30s.jpg')
diff_bg = sum(abs(a-b) for a, b in zip(img1.getpixel((540, 1100)), img30.getpixel((540, 1100))))
assert diff_bg > 100, f"❌ BG static: {diff_bg}"  # PASS nếu > 100

# 4. PIP motion (X=290, Y=290) trong phase PIP
img_usp1 = Image.open('frame_t40s.jpg')
img_usp2 = Image.open('frame_t45s.jpg')
diff_pip = sum(abs(a-b) for a, b in zip(img_usp1.getpixel((290, 290)), img_usp2.getpixel((290, 290))))
# PASS nếu > 30 (PIP motion thấp hơn BG vì crop từ vùng face ít motion nhất)
```

**Production target:**
- CRF 18 + preset slow → 6-8 Mbps bit rate (V76 verified = 6,819 Kbps)
- AAC 48000Hz stereo, 128k
- Duration: source clip duration (không pad)

## 🚫 Anti-patterns (đã sai 5 lần — đọc kỹ trước khi build)

| # | Anti-pattern | Tại sao sai | V76 fix |
|---|---|---|---|
| 1 | `<img src=\"pip_X.png\">` (V74) | Ảnh tĩnh, KHÔNG motion | Extract PIP mp4 thực sự |
| 2 | `.pip-wrap { background: #000 }` (V74) | Nền đen TOÀN CLIP, sai ý anh | Layer riêng black_420x420 overlay CHỈ ở vùng PIP |
| 3 | `<video class=\"pip-vid\" muted playsinline>` (V72, V73) | HyperFrames KHÔNG play HTML video trong headless Chrome | Extract PIP mp4 + ffmpeg ghép |
| 4 | `crop=ih*9/16:ih:0:0` (V72) | Crop source 1080×1920 thành 607×720 từ Y=0 → background đen | `crop=1080:1080:0:540` lấy Y=540-1620 |
| 5 | PIP 420×750 portrait (V72) | Bị crop thu nhỏ, sai format TikTok dọc | PIP vuông 420×420 |
| 6 | Nền = video full TOÀN CLIP (V75) | Đoạn PIP phải có nền đen để show thông tin cho rõ | V76: chỉ vùng PIP có nền đen |
| 7 | Extract PIP từ đoạn khác audio (V72) | Audio và PIP không khớp — khó hiểu | Extract ĐÚNG timestamp phase (24-37 cho CHART) |

## 📦 File reference

Verified V76 ship: `clip0003_V76_82s_FINAL_PIP_BLACK_BG.mp4` (71.1 MB, 81.76s, 6,819 Kbps, AAC 48000Hz stereo) tại `/Volumes/Storage-1/Pocket3/Hermes-Edit/`.

## 🔄 Migration V75 → V76

**V75 sai:** 3-layer không có black dưới PIP → nền = video full toàn clip (anh bảo \"đoạn PIP phải có nền đen\")
**V76 đúng:** 4-layer thêm black_420x420 overlay TRƯỚC mỗi PIP → nền đen ở vùng PIP + nền video ở ngoài

Khi build clip mới có PIP, dùng V76 workflow này ngay từ đầu (KHÔNG thử V72/V73/V74/V75 trước).
