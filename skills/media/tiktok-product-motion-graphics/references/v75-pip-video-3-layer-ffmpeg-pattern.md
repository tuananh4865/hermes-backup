---
title: V75 PIP VIDEO + NỀN VIDEO FULL — 3-Layer ffmpeg Pattern (CORRECT)
created: 2026-07-18
type: reference
tags: [pip, video, hyperframes, ffmpeg-overlay, 3-layer, v75, tiktok-product]
verified: 2026-07-18 (clip_0003 V75, 71.5 MB shipped)
---

# V75: PIP Video + Nền Video Full — 3-Layer ffmpeg Pattern

> **Final answer** after 4 failed attempts (V72 → V73 → V74 → V75) on clip_0003 (Dodoto Lux Air V3).

## 🎯 Bài học cốt lõi (anh đã sửa 3 lần)

| Sai cách | Tại sao sai | Đúng cách (V75) |
|---|---|---|
| `<img src="pip.png">` (V74) | Ảnh tĩnh, KHÔNG motion | `<div class="pip-placeholder">` + ffmpeg ghép PIP mp4 |
| `<video>` element (V72, V73) | HyperFrames KHÔNG play HTML video background trong headless Chrome | Extract PIP mp4 thực sự, ghép bằng ffmpeg filter_complex |
| `background: #000` (V74) | Anh không muốn nền đen | Background = source video full 1080×1920 |

**Anh yêu cầu chính xác:** "PIP phải là **video thu nhỏ** + nền **vẫn là video full** chứ không phải nền đen"

---

## ✅ V75 Workflow (4 bước, copy-paste ready)

### Bước 1: Extract 3 PIP videos (mp4 crop 420×420 vuông từ Y=540)

```bash
# Crop source 1080×1920 thành vuông 1080×1080 từ Y=540 → bao phủ mặt
# Rồi scale xuống 420×420 PIP vuông
# Duration mỗi PIP = thời gian phase tương ứng trong clip

# PIP-CHART: phase chart 24-37s (duration 13s, lấy 30-37s crop từ Y=540)
ffmpeg -y -ss 30 -t 7 -i source.mp4 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast -pix_fmt yuv420p \
  assets/source/pip_chart.mp4

# PIP-USP: phase USP 37-52s (lấy 40-50s)
ffmpeg -y -ss 40 -t 10 -i source.mp4 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast -pix_fmt yuv420p \
  assets/source/pip_usp.mp4

# PIP-FINAL: phase CTA-TEST 61-73s (lấy 55-72s)
ffmpeg -y -ss 55 -t 17 -i source.mp4 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast -pix_fmt yuv420p \
  assets/source/pip_final.mp4
```

**Crop math:** `crop=1080:1080:0:540` lấy Y=540-1620 (bao phủ mặt anh Y=504-1317), scale về 420×420 vuông.

### Bước 2: HTML index.html — KHÔNG có `<video>` element, KHÔNG có `<img>`

```html
<!-- CHỈ có PIP PLACEHOLDER (HyperFrames render border + glass xung quanh) -->
<div class="pip-placeholder" data-class="pip-chart"></div>
```

```css
.pip-placeholder {
  position: absolute;
  top: 80px; left: 80px;
  width: 420px; height: 420px;
  /* KHÔNG background - vùng trong suốt, ffmpeg sẽ overlay PIP video */
  border-radius: 28px;
  border: 3px solid rgba(255, 215, 0, 0.8);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.6);
  z-index: 30;
  opacity: 0;
  clip-path: circle(0% at 50% 50%);
}
/* QUAN TRỌNG: disable video bg */
.bg-video-wrap { display: none; }
```

### Bước 3: Render silent (HyperFrames chỉ render glass)

```bash
npx hyperframes render --quality draft --format mov --output output_silent.mov
```

### Bước 4: ffmpeg ghép 3 LAYER (copy-paste command)

```bash
ffmpeg -y \
  -i assets/source/full_bg.mp4 \
  -i assets/source/pip_chart.mp4 \
  -i assets/source/pip_usp.mp4 \
  -i assets/source/pip_final.mp4 \
  -i output_silent.mov \
  -filter_complex "
    [0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS-STARTPTS[bg];
    [1:v]scale=420:420,setpts=PTS-STARTPTS[pip1];
    [2:v]scale=420:420,setpts=PTS-STARTPTS[pip2];
    [3:v]scale=420:420,setpts=PTS-STARTPTS[pip3];
    [4:v]format=yuva420p[glass];
    [bg][glass]overlay=0:0:eof_action=pass[base];
    [base][pip1]overlay=80:80:eof_action=pass[v1];
    [v1][pip2]overlay=80:80:eof_action=pass[v2];
    [v2][pip3]overlay=80:80:eof_action=pass[v]
  " \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset slow -crf 18 -b:v 8M \
  -c:a aac -b:a 128k \
  -shortest \
  output_final.mp4
```

**5 inputs:** source full bg + 3 PIP videos + HyperFrames silent overlay.

**Filter chain:**
- Layer 1: `bg` = source video full 1080×1920 (motion thật)
- Layer 2-4: 3 PIP videos (mp4 crop 420×420)
- Layer 5: `glass` = HyperFrames overlay (format=yuva420p cho alpha)
- Composition: bg + glass → base; rồi + pip1 → v1; + pip2 → v2; + pip3 → v

---

## ✅ Verify Protocol (multi-region pixel diff)

```python
from PIL import Image

# 1. BG nền = video full (KHÔNG đen)
# Sample top area X=900, Y=200 (vùng KHÔNG có glass)
img = Image.open('frame_t30s.jpg')
bg_pixel = img.getpixel((900, 200))
avg = sum(bg_pixel[:3]) / 3
assert avg > 40, f"❌ BG đen: {bg_pixel}"  # PASS nếu > 40

# 2. BG motion (face chin Y=1100)
img1 = Image.open('frame_t1s.jpg')
img30 = Image.open('frame_t30s.jpg')
diff_bg = sum(abs(a-b) for a, b in zip(img1.getpixel((540, 1100)), img30.getpixel((540, 1100))))
assert diff_bg > 100, f"❌ BG static: {diff_bg}"  # PASS nếu > 100

# 3. PIP motion (X=290, Y=290)
img31 = Image.open('frame_t31s.jpg')
img34 = Image.open('frame_t34s.jpg')
diff_pip = sum(abs(a-b) for a, b in zip(img31.getpixel((290, 290)), img34.getpixel((290, 290))))
# PASS nếu > 30 (PIP motion thấp hơn BG vì crop từ vùng face ít motion)
```

**Production target:**
- CRF 18 + preset slow → 6-8 Mbps bit rate
- AAC 48000Hz stereo, 128k
- Duration: source clip duration (no padding)

---

## 🚫 Anti-patterns (đã sai 3 lần)

| # | Anti-pattern | Tại sao sai |
|---|---|---|
| 1 | `<img src="pip_X.png">` (V74) | Ảnh tĩnh, KHÔNG motion — anh không muốn |
| 2 | `.pip-wrap { background: #000 }` (V74) | Nền đen, anh muốn nền = video full |
| 3 | `<video class="pip-vid" muted playsinline>` (V72, V73) | HyperFrames KHÔNG play HTML video trong headless Chrome |
| 4 | `crop=ih*9/16:ih:0:0` (V72) | Crop source 1080×1920 thành 607×720 từ Y=0 → background đen |
| 5 | PIP 420×750 portrait (V72) | Bị crop thu nhỏ, sai format TikTok dọc |

---

## 📦 File reference

Verified V75 ship: `clip0003_V75_82s_FINAL_PIP_VIDEO.mp4` (71.5 MB, 81.76s, 6,858 Kbps, AAC 48000Hz stereo) tại `/Volumes/Storage-1/Pocket3/Hermes-Edit/`.

---

## 🔄 Migration V74 → V75

**V74 sai:** `<img>` PNG tĩnh + nền đen → ảnh tĩnh không motion.
**V75 đúng:** Extract PIP mp4 + ffmpeg 3-layer filter_complex → PIP motion + nền video full.

Khi build clip mới có PIP, dùng V75 workflow này ngay từ đầu (KHÔNG thử V72/V73/V74 trước).
