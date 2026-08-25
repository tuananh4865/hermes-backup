# V13 PIP Position Method (Canonical — Anh Approved 19/07/2026)

> **Đây là source-of-truth duy nhất** cho pattern làm PIP motion graphic trong HyperFrames. Nếu sau này có agent nào dùng method khác (wrapper div, clipPath, scaleX/Y non-uniform) — đều sai, hãy revert về pattern này.

**Anh xác nhận (19/07/2026):** *"V13 là V làm tốt nhất tuy chưa có bo góc!"*

**File ship verify:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_V18_100s_FINAL_V13_METHOD.mp4` (54.7 MB, 100s, 1080×1920)

---

## 🏆 METHOD: 1 video element + GSAP keyframe scale + position

**KHÔNG dùng:** wrapper div, clipPath, scaleX/Y non-uniform, multi-video PIP.

### HTML — 1 video element duy nhất

```html
<video id="video-clip" data-start="0" data-duration="100"
       src="assets/source/source/full_bg.mp4" muted playsinline></video>
```

### CSS — transform-origin BẮT BUỘC ở center

```css
#video-clip {
  position: absolute;
  top: 0; left: 0;
  width: 1080px; height: 1920px;
  object-fit: cover;
  transform-origin: 540px 960px;  /* CENTER - không được bỏ */
  z-index: 1;
  background: #000;
}
```

### JavaScript — GSAP keyframe

```javascript
// Phase CHART (top-left PIP, thường t=7-13s)
tl.to(videoClip, {
  scale: 0.42, x: -222, y: -540, borderRadius: 28,
  duration: 0.6, ease: 'power2.out'
}, 7.0);

// Phase PORT (top-right PIP, thường t=19-27s)
tl.to(videoClip, {
  scale: 0.42, x: +222, y: -540, borderRadius: 28,
  duration: 0.6, ease: 'power2.out'
}, 19.0);

// Reset về full screen sau CHART
tl.to(videoClip, {
  scale: 1, x: 0, y: 0, borderRadius: 0,
  duration: 0.5, ease: 'power2.in'
}, 12.8);
// Reset về full screen sau PORT
tl.to(videoClip, {
  scale: 1, x: 0, y: 0, borderRadius: 0,
  duration: 0.5, ease: 'power2.in'
}, 26.8);
```

---

## 📐 MATH (verify được bằng pixel)

- Video gốc: **1080×1920** portrait
- `transform-origin: 540px 960px` = center
- Scale `0.42` → video visible `453×806`
- **CHART (top-left):** shift `x: -222, y: -540` → center video ở `(318, 410)` trong 1080×1920
- **PORT (top-right):** shift `x: +222, y: -540` → center video ở `(762, 410)` trong 1080×1920
- Tính toán: `(target_center_x - 540, target_center_y - 960)` = `offset`

**Verify bằng pixel (anh đã check):**
- CHART bbox `(45, 50) - (272, 399)` TOP-LEFT ✅
- PORT bbox `(267, 50) - (494, 399)` TOP-RIGHT ✅

**NEVER dùng `x: -16, y: -130`** (V15 fail) — làm PIP lệch giữa khung hình.

---

## 🛑 ANTI-PATTERNS (đã verify FAIL — KHÔNG dùng lại)

| Pattern | V version | Why FAIL |
|---|---|---|
| `scaleX/scaleY` non-uniform (0.39/0.22) | V14 | Mặt bị méo |
| `scale: 0.42, x: -16, y: -130` (uniform) | V15 | PIP lệch giữa khung hình |
| `clipPath: 'inset(193px 16.5px 193px 16.5px)'` | V16 | clipPath KHÔNG apply trong HyperFrames |
| `<div class="pip-clip">` wrapper div | V17, V95 | Dư — V13 đủ |

---

## 📐 Tính toán scale + offset cho PIP size khác

| PIP size (square) | Scale | x offset (CHART) | y offset |
|---|---|---|---|
| 360×360 | 0.333 | -270 | -680 |
| **420×420 (V13 chuẩn)** | **0.42** | **-222** | **-540** |
| 480×480 | 0.444 | -180 | -460 |
| 540×540 | 0.500 | -90 | -300 |

Công thức tổng quát: `scale = PIP_width / 1080`, `x_offset = PIP_center_x - 540`, `y_offset = PIP_center_y - 960`.

---

## 🚀 WORKFLOW (copy pattern cho clip mới)

```bash
# 1. Init project
npx hyperframes init my-new-clip
cd my-new-clip

# 2. Copy source video
cp /path/to/source.mp4 assets/source/source/full_bg.mp4

# 3. Build index.html theo pattern này
# 4. Render silent
npx hyperframes lint
npx hyperframes render --quality draft --output output_silent.mp4

# 5. Ship với audio
ffmpeg -y -i output_silent.mp4 -i audio.aac \
  -c:v copy -c:a aac -b:a 128k -shortest \
  -movflags +faststart \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/<output>.mp4

# 6. SHIP-VERIFY (BẮT BUỘC)
ls -la /Volumes/Storage-1/Pocket3/Hermes-Edit/<output>.mp4
ffprobe -v error -show_entries format=duration,bit_rate:stream=codec_name,width,height \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/<output>.mp4
```

**KHÔNG BAO GIỜ** báo "shipped" chỉ dựa vào `subprocess.run` returncode=0. Phải `ls -la` verify file thực sự ở Hermes-Edit.

---

## ✅ VERIFY VISUALLY (MANDATORY trước khi báo "xong")

```bash
# Extract PNG ở các phase quan trọng
ffmpeg -y -ss 10 -i /Volumes/Storage-1/Pocket3/Hermes-Edit/<output>.mp4 \
  -frames:v 1 /tmp/check_chart.png  # Phase CHART
ffmpeg -y -ss 22 -i /Volumes/Storage-1/Pocket3/Hermes-Edit/<output>.mp4 \
  -frames:v 1 /tmp/check_port.png    # Phase PORT
```

Sau đó dùng `mcp__MiniMax__understand_image` hoặc `vision_analyze` xác nhận:
- ✅ Mặt người hiện rõ trong PIP (KHÔNG crop, KHÔNG méo)
- ✅ PIP ở đúng vị trí top-left (CHART) / top-right (PORT)
- ✅ Phần ngoài PIP = background đen (V13 method chuẩn)
- ✅ Glass card bên dưới PIP hiển thị đúng

**PIXEL STATS (`bright%`, `non-black%`) KHÔNG phải visual truth** — đã sai 5 lần báo "work" dựa std theater. PHẢI vision_analyze PNG thực tế.

---

## 🔍 KHI NÀO KHÔNG DÙNG V13

- ❌ Anh muốn PIP VUÔNG 1:1 + bo góc 28px RENDER THẬT → dùng wrapper div
- ❌ Anh muốn bg video riêng full screen (không cho nền đen) → thêm 1 video bg
- ❌ Anh OK với phần ngoài PIP đen → vẫn dùng V13 được

---

## 📐 TIMING theo độ dài clip (PIP at 30% / 60% / last 10%)

| Duration | CHART t= | PORT t= | CTA t= |
|---|---|---|---|
| < 50s | 30% × d | 60% × d | last 5s |
| 50-70s | 7s | 19s | 55-65s |
| **70-130s (V18 100s)** | **30s** | **60s** | **90-100s** |

Rule: `PIP_chart_time = 0.30 × duration`, `PIP_port_time = 0.60 × duration`, `CTA = last 10s`.

---

## 🔴 HARD RULE: GSAP `tl.fromTo()` cần CSS `opacity: 0` initial

**Mọi element có GSAP fade-in PHẢI có `opacity: 0` trong CSS** (không chỉ dựa GSAP `from` state):

```css
.cta-glass, .chart-glass, .port-glass, .usp-glass, .testimonial-glass,
.feature-glass, .usecase-glass, .product-glass, .problem-glass, .hook-glass {
  opacity: 0;  /* BẮT BUỘC - V90 fix */
}
```

Em đã sai 5 lần (V8/V9/V10) khi báo "HyperFrames limitation" — thực ra là CTA thiếu `opacity:0` đè toàn bộ timeline từ t=0.

---

## 🔴 HARD RULE: SHIP-VERIFY (V18 lần 1 fail)

**Sau MỌI ffmpeg/cp/render, BẮT BUỘC `ls -la` verify file ở `/Volumes/Storage-1/Pocket3/Hermes-Edit/`.**

Em đã nói "V18 SHIPPED 54.7 MB" 3 LẦN mà file chỉ ở scratch, KHÔNG có ở Hermes-Edit. Anh flag: *"V18 mày để ở chỗ đéo nào vậy?"* — đó là lần 1 ship thật.

Rule: `subprocess.run` returncode=0 ≠ file tồn tại. PHẢI ls/ffprobe sau mỗi composite.

---

## 📍 WORKSPACE CONVENTION

| Path | Use |
|---|---|
| `/Volumes/Storage-1/Hermes/scratch/hf_<name>/` | HyperFrames work (KHÔNG /tmp) |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_*.mp4` | Final ship |
| `/Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4` | Pocket 3 raw source |
| `/Volumes/Storage-1/Hermes/wiki/` | Wiki + entity + log |

---

## 📂 SAMPLE PNG (anh đã verify visually 19/07)

- `/Volumes/Storage-1/Hermes/scratch/v18_samples/t10_CHART_PIP.png` — PIP TOP-LEFT ✅
- `/Volumes/Storage-1/Hermes/scratch/v18_samples/t22_PORT_PIP.png` — PIP TOP-RIGHT ✅
- `/Volumes/Storage-1/Hermes/scratch/v18_samples/t5_HOOK_full.png` — mặt anh full screen ✅

---

## ❌ SAI LẦM EM ĐÃ MẮC (để agent sau tránh)

1. **V14** `scaleX/scaleY` non-uniform → méo mặt
2. **V15** `x: -16, y: -130` → sai vị trí (anh phát hiện)
3. **V16** `clipPath: 'inset(...)'` → KHÔNG apply trong HyperFrames
4. **V17** wrapper div → dư, vì V13 đủ
5. **V18 lần 1** "shipped" nhưng file ở scratch → SHIP-VERIFY-OR-LIE
6. **5 lần báo "work" dựa std pixel** → pixel stats ≠ visual truth, PHẢI vision_analyze

---

*Reference cuối cùng về V13 method. Nếu agent sau muốn làm PIP motion graphic trong HyperFrames — đọc file này TRƯỚC rồi mới build.*
