# V22 PIP Pattern — EXACT Recipe (Canonical Reference)

**Status:** VERIFIED 18/07/2026 — V80 SHIPPED, motion 33%/phase, PIP visible at CHART/PORT, CTA card canh giữa
**Failures that produced this lesson:** V72 (PIP 420×750 portrait sai), V74 (PNG tĩnh), V75 (PIP riêng overlay), V76 (4-layer ffmpeg), V77 (HyperFrames partial freeze), V78 (4 phases thiếu), V79 (sai PIP structure z-index)

---

## 🎯 V22 PIP STRUCTURE (EXACT — đừng đổi)

### HTML structure (FORENSIC từ `/tmp/hf_sacduphong_v22/index.html`):
```html
<!-- ✅ V22 pattern: div.pip-wrap wrapper chứa <video> bên trong -->
<div class="pip-wrap" id="pip-chart">
  <video id="video-pip-chart" data-start="7" data-duration="6"
         data-track-index="1"
         src="assets/source/pip/pip_chart.mp4"
         muted playsinline preload="auto"></video>
</div>

<div class="pip-wrap" id="pip-port">
  <video id="video-pip-port" data-start="19" data-duration="9"
         data-track-index="2"
         src="assets/source/pip/pip_port.mp4"
         muted playsinline preload="auto"></video>
</div>

<!-- ❌ V79 sai: <div class="pip"> với video id khác div id → PIP invisible -->
<div class="pip" id="pip-chart">                       ← SAI
  <video id="video-pip-chart" ...></video>             ← id trùng OK nhưng class sai + z-index sai
</div>
```

### CSS (V22 exact):
```css
.pip-wrap {
  position: absolute;
  z-index: 4;                                         ← QUAN TRỌNG: cao hơn black-bg (z=1) + video-bg (z=0)
  top: 80px; left: 80px;
  width: 420px; height: 420px;
  border-radius: 28px;
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 16px 48px rgba(0,0,0,0.6);
}

.pip-wrap video {
  width: 100%; height: 100%;
  object-fit: cover;
}
```

### Animation target (V22 dùng `pipChart.parentElement`):
```javascript
// V22 original
const pipChart = root.querySelector('#pip-chart');   ← target = DIV wrapper
tl.fromTo(pipChart.parentElement, { opacity: 0, scale: 0.85, x: -60 },
  { opacity: 1, scale: 1, x: 0, duration: 0.6, ease: 'back.out(1.2)' }, 7.4);

// V80 simplified — target div id (vì div giờ có id)
tl.fromTo('#pip-chart', { opacity: 0, scale: 0.85, x: -60 },
  { opacity: 1, scale: 1, x: 0, duration: 0.6, ease: 'back.out(1.5)' }, 7.4);
```

---

## 📐 CARD SAFE ZONE (Canh giữa, không tràn khung hình 1080×1920)

Safe zone = 80px-1020px width × 80px-1840px height = 960×1760

| Phase | Position | max-width | max-height |
|---|---|---|---|
| HOOK | top 1308, left 80, right 80 | 920px | 480px |
| PROBLEM | top 1288, left 80, right 80 | 920px | 480px |
| CHART | top 720, left 530 (ngang hàng PIP) | 470px | 480px |
| PORT | top 720, left 530 (ngang hàng PIP) | 470px | 600px |
| PRODUCT | top 1288, left 80, right 80 | 920px | 480px |
| USP | top 1308, left 80, right 80 | 920px | 480px |
| CTA-FINAL | top 10%, left 10%, right 10%, bottom 10% (80% × 80%) | 864px | 1536px |

**Anh đã flag (V79):** "không được để cạnh card bị mất ra khỏi khung hình mà phải luôn nằm trong khung hình canh giữa khung hình"

---

## 🎨 SMOOTH MOTION RECIPE

### Ease library (anh muốn "smooth hơn"):
```javascript
// Entrance — bouncy overshoot
ease: 'back.out(1.7)'                                  ← primary, anh đã approved V80

// Slide-in — natural
ease: 'power2.out'

// Chart bar width — smooth ease
ease: 'power1.inOut'

// Wiggle — subtle rotation
ease: 'sine.inOut'

// ❌ TUYỆT ĐỐI KHÔNG: ease linear → motion đơ cứng
```

### Stagger pattern (rhythm cho phase có nhiều rows):
```javascript
// Stagger 0.3-0.5s giữa các row
tl.fromTo('#usp-1', { opacity: 0, scale: 0.9, y: 15 },
  { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: 'back.out(1.7)' }, 27.7);
tl.fromTo('#usp-2', ..., 28.0);                          ← +0.3s stagger
tl.fromTo('#usp-3', ..., 28.3);                          ← +0.3s
tl.fromTo('#usp-4', ..., 28.6);                          ← +0.3s

// Wiggle cho PIP
tl.to('#pip-port', { rotation: -2, duration: 0.3, ease: 'sine.inOut' }, 23.0);
tl.to('#pip-port', { rotation: 2, duration: 0.3, ease: 'sine.inOut' }, 23.5);
tl.to('#pip-port', { rotation: 0, duration: 0.3, ease: 'sine.inOut' }, 24.0);
```

---

## 🕐 8-PHASE TIMELINE TEMPLATE (V80 VERIFIED — 65s total)

| # | Phase | Time | Code template |
|---|---|---|---|
| 1 | HOOK | 0-3s | `tl.fromTo('#hook-pill', ... { duration: 0.5, ease: 'back.out(1.7)' }, 0.3);` |
| 2 | PROBLEM | 3-7s | `tl.fromTo('#problem-row-N', ... { duration: 0.4, ease: 'power2.out' }, 3.5 + 0.5*N);` |
| 3 | CHART | 7-13s | `tl.to('#black-bg', { opacity: 1 }, 7.2);` + `tl.fromTo('#pip-chart', ..., 7.4);` + bars animate stagger 0.8s |
| 4 | STAMP | 13-16s | `tl.fromTo('#stamp-glass', ..., { scale: 1, rotation: -8, ease: 'back.out(1.7)' }, 13.2);` |
| 5 | PRODUCT | 16-19s | `tl.fromTo('#product-glass', ..., 16.0);` |
| 6 | PORT | 19-27s | `tl.to('#black-bg', { opacity: 1 }, 18.8);` + `tl.fromTo('#pip-port', ..., 19.0);` + 3 steps stagger |
| 7 | USP | 27-32s | `tl.fromTo('#usp-N', ..., 27.7 + 0.3*N);` (grid stagger) |
| 8 | CTA-FINAL | 32-end | `tl.fromTo('#cta-glass', { scale: 0.92, y: 60 }, { scale: 1, y: 0, duration: 0.8, ease: 'back.out(1.3)' }, 32.5);` + giữ visible |

---

## ✅ VERIFY CHECKLIST (BẮT BUỘC trước khi ship)

```bash
# 1. PIP visible (anh flag V79)
for t in 10 23; do
  ffmpeg -y -ss $t -i output_silent.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/v_t${t}.jpg
done
# Check RGB tại vùng PIP (40-250, 40-250) — phải >25 (không đen)

# 2. CTA card canh giữa (anh flag V79)
# Check brightness 4 edges của CTA-FINAL @ t=55s — phải thấp (CTA visible)

# 3. Motion 7 transitions ≥30%
python3 -c "from PIL import Image, ImageChops; ..."  # pixel diff
```

---

## 🚨 ANTI-PATTERNS (đã fail 4 lần liên tiếp V72-V79)

1. ❌ `<div class="pip">` thay vì `<div class="pip-wrap">` (V79 fail)
2. ❌ Video id khác div id (V79 fail — `id="video-pip-chart"` khác `id="pip-chart"`)
3. ❌ PIP `z-index: 3` thay vì `z-index: 4` (V79 fail — che bởi black-bg)
4. ❌ Card không có `max-width/max-height` → tràn khung hình
5. ❌ Ease linear thay vì back.out/power2.out → motion đơ cứng
6. ❌ Animate nhiều row cùng lúc thay vì stagger 0.3-0.5s
7. ❌ Build không đọc V22 final shipped HTML trước → sai pattern (lặp lại 4 lần)

---

## 📚 SEE ALSO

- Skill `tiktok-product-motion-graphics/SKILL.md` § "V80 RECAP" + "V79 RECAP" + "V78 RECAP" — pattern history
- `/tmp/hf_sacduphong_v22/index.html` — canonical V22 HTML để forensic
- `/tmp/hf_clip0003_V80/index.html` — V80 verified build
- Wiki `concept/tiktok-video-pipeline-studio-2026-07-18.md` — pipeline 5 stages