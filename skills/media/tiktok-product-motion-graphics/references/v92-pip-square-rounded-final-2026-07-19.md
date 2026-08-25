# V92 PIP SQUARE CROP + ROUNDED CORNERS (FINAL) — 19/07/2026

**Context:** Anh đã thành công với V12 (1 video + GSAP keyframe scale+position). Tiếp theo anh muốn:
1. Crop video thành **hình vuông** (1:1) khi ở PIP mode
2. **Bo tròn góc** (borderRadius) cho PIP
3. **Reset về bình thường** khi về full screen (scale 1,1 + borderRadius 0)

**V13 attempt:** BorderRadius 28px OK, nhưng PIP vẫn portrait (giữ aspect ratio 9:16 gốc) vì dùng `scale: 0.42` uniform — V13 ship nhưng không square.

**V14 FINAL:** Dùng **`scaleX` + `scaleY` RIÊNG BIỆT** (non-uniform scale) để ép portrait thành square.

---

## ✅ APPROACH: GSAP keyframe scaleX/scaleY (non-uniform scale)

```javascript
// 1. Setup video element với transform-origin center
#video-clip {
  position: absolute;
  top: 0; left: 0;
  width: 1080px; height: 1920px;
  transform-origin: 540px 960px;  /* center để scale/position từ giữa */
  border-radius: 0;  /* mặc định không bo */
}

/* 2. CHART PIP - square 420×420 top-left */
tl.to(videoClip, {
  scaleX: 0.39,    // 420/1080 = 0.389 — compress width
  scaleY: 0.22,    // 420/1920 = 0.219 — compress height NHIỀU HƠN
  x: -222,         // center moves to (318, 410) = PIP top-left center
  y: -550,
  borderRadius: 28, // bo góc 28px
  duration: 0.6, ease: 'power2.out'
}, 7.0);

/* 3. PORT PIP - square 420×420 top-right */
tl.to(videoClip, {
  scaleX: 0.39,
  scaleY: 0.22,
  x: 222,          // center moves to (762, 410) = PIP top-right center
  y: -550,
  borderRadius: 28,
  duration: 0.6, ease: 'power2.out'
}, 19.0);

/* 4. RESET về full screen (scale 1,1 + borderRadius 0) */
tl.to(videoClip, {
  scaleX: 1, scaleY: 1,
  x: 0, y: 0,
  borderRadius: 0,
  duration: 0.5, ease: 'power2.in'
}, 12.8);  // hoặc 26.8 tùy phase
```

---

## 📐 MATH: Square từ Portrait

Video gốc 1080×1920 (portrait, ratio 9:16 = 0.5625).

Muốn 420×420 square (1:1):
- `scaleX = 420/1080 = 0.389` (compress width)
- `scaleY = 420/1920 = 0.219` (compress height NHIỀU HƠN)

Kết quả: video co lại thành 420×420 hoàn hảo.

---

## 📐 MATH: Position offset

- Video center gốc: (540, 960) (transform-origin: 540px 960px)
- CHART PIP target center: (108 + 420/2, 200 + 420/2) = **(318, 410)** (top-left)
- Offset CHART: `(318-540, 410-960)` = **(-222, -550)**

- PORT PIP target center: (1080 - 108 - 420/2, 200 + 420/2) = **(762, 410)** (top-right)
- Offset PORT: `(762-540, 410-960)` = **(222, -550)**

---

## ✅ VERIFIED V14 SHIPPED

| Phase | Width | Height | Ratio | Verdict |
|---|---:|---:|---:|---|
| CHART (t=10s) | 212px | 211px | **1.00** | ✅ SQUARE |
| PORT (t=22s) | 212px | 211px | **1.00** | ✅ SQUARE |

**Rounded corner gradient** (càng xa corner càng bright = bo góc càng rõ):

| Radius | Brightness |
|---:|---:|
| 0px (corner) | 102 (đỉnh mặt anh) |
| 5px | 64 |
| 10px | 58 |
| 15px | 46 |
| 20px | 42 |
| 30px | 38 |
| 50px | 37 (background) |

→ Gradient brightness giảm đều khi xa corner = **bo góc hoạt động**.

---

## 📂 V14 SHIPPED

**File**: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_V14_100s_FINAL_PIP_SQUARE_ROUNDED.mp4` (53.4 MB, 100s, H.264 1080×1920 + AAC)

**Samples** (ảnh PNG verify bằng mắt): `/Volumes/Storage-1/Hermes/scratch/v14_samples/`
- `t10_CHART_PIP_SQUARE.png` - PIP VUÔNG top-left ✓
- `t22_PORT_PIP_SQUARE.png` - PIP VUÔNG top-right ✓
- `t5_HOOK_full.png`, `t15_PRODUCT_full.png`, etc.

---

## 🔁 WORKFLOW CHO CLIP TIẾP THEO (copy-paste ready)

```html
<!-- 1. HTML: 1 video element -->
<video id="video-clip" class="video-clip" data-start="0" data-duration="100"
       src="assets/source/full_bg.mp4" muted playsinline></video>
```

```javascript
// 2. GSAP keyframes cho mỗi PIP phase
const PIP_SCALE_X = 0.39;  // 420/1080
const PIP_SCALE_Y = 0.22;  // 420/1920 (non-uniform = square)
const PIP_BORDER_RADIUS = 28;
const PIP_DURATION = 0.6;

// CHART phase - top-left
tl.to(videoClip, {
  scaleX: PIP_SCALE_X,
  scaleY: PIP_SCALE_Y,
  x: -222, y: -550,
  borderRadius: PIP_BORDER_RADIUS,
  duration: PIP_DURATION, ease: 'power2.out'
}, 7.0);
tl.fromTo('#chart-glass', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 7.5);
// ... bars ...
tl.to('#chart-glass', { opacity: 0, duration: 0.3 }, 12.5);
tl.to(videoClip, { scaleX: 1, scaleY: 1, x: 0, y: 0, borderRadius: 0, duration: 0.5 }, 12.8);

// PORT phase - top-right
tl.to(videoClip, {
  scaleX: PIP_SCALE_X,
  scaleY: PIP_SCALE_Y,
  x: 222, y: -550,
  borderRadius: PIP_BORDER_RADIUS,
  duration: PIP_DURATION
}, 19.0);
tl.fromTo('#port-glass', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 19.5);
// ... steps ...
tl.to('#port-glass', { opacity: 0, duration: 0.3 }, 26.5);
tl.to(videoClip, { scaleX: 1, scaleY: 1, x: 0, y: 0, borderRadius: 0, duration: 0.5 }, 26.8);
```

```css
/* 3. CSS: video clip với transform-origin center + borderRadius default 0 */
.video-clip {
  position: absolute;
  top: 0; left: 0;
  width: 1080px; height: 1920px;
  transform-origin: 540px 960px;
  border-radius: 0;  /* reset khi full screen */
}
```

---

## 📏 TỶ LỆ PIP KHÁC (cho clip sau)

| PIP size | scaleX | scaleY | Use case |
|---|---|---|---|
| 360×360 | 0.333 | 0.188 | Small PIP (corner nhỏ) |
| **420×420** | **0.389** | **0.219** | **V14 default** ✓ |
| 480×480 | 0.444 | 0.250 | Large PIP |
| 540×540 | 0.500 | 0.281 | Maximum square (cover 1/2 height) |

---

## ⚠️ CRITICAL LESSON

**ĐỪNG dùng `scale: 0.42` (uniform)** — sẽ giữ aspect ratio gốc (portrait 9:16).
**PHẢI dùng `scaleX: 0.39, scaleY: 0.22`** (separate values) — non-uniform → square crop.

Em đã sai ở V13 (dùng uniform scale → portrait PIP), V14 fix mới work.

---

## 📜 COMPLETE LEARNING SEQUENCE (V78→V92)

| Version | Bài học |
|---|---|
| V78-V83 | Pixel scan face zone TRƯỚC khi build |
| V84 | TESTIMONIAL top 200, FEATURE top 220 (đỉnh đầu) |
| V85 | Vùng cấm mặt y=547-1140 - canvas layout verified |
| V86 | PIP timing scale theo duration (30%/60%) |
| V87-V89 | Em đã sai 3 lần (báo "HyperFrames limitation") |
| V90 | CTA-glass PHẢI có `opacity: 0` initial (anh đoán ĐÚNG "nền đen đè clip") |
| V91 | 1 video element + GSAP keyframe scale+position (final PIP pattern) |
| V92 | `scaleX` + `scaleY` non-uniform + `borderRadius` (square + rounded FINAL) |

---

## 🔗 RELATED REFERENCES

- `references/v91-gsap-keyframe-pip-pattern-2026-07-19.md` — 1 video + GSAP keyframe base pattern
- `references/v90-gsap-fadein-opacity-zero-rule-2026-07-19.md` — CTA opacity:0 HARD RULE
- `references/v88-pip-pattern-chinh-goc-5-fixes-2026-07-19.md` — V22 chính gốc 5 patterns
- `references/face-aware-pip-crop.md` — Face zone + PIP auto-detect pattern
- `references/v85-v87-v88-final-loop-2026-07-19.md` — Final loop V85→V88 with 11 frame screenshot
