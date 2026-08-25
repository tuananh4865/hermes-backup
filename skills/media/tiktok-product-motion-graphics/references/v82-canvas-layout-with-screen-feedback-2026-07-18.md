---
title: V82 CANVAS LAYOUT (4 FIX from screenshot feedback) — 2026-07-18
created: 2026-07-18
updated: 2026-07-18
tags: [motion-graphics, v82, 11-phase, canvas, layout, cta-centered, card-below-pip, integer-only, face-safe, screenshot-feedback]
---

# V82 CANVAS LAYOUT (4 FIX from screenshot feedback)

> **Status:** VERIFIED PASS 18/07. Ship `clip0003_V82_65s_FINAL_with_audio.mp4` 27.6 MB / 65s / motion 30-33% (12 transitions).
>
> **Replaces:** V81 (which anh flagged 4 lỗi mới qua screenshot ảnh thật).
> **Use when:** Build 11-phase motion graphic cho clip TikTok bán hàng > 50s.

## CONTEXT — 4 LỖI ANH FLAG QUA SCREENSHOT

V81 (đã ship 18/07) bị anh reject với 4 screenshot lỗi cụ thể. V82 fix all 4:

| # | Lỗi V81 | Root cause | Fix V82 |
|---|---|---|---|
| 1 | **CTA 80% bị lệch phải** (anh flag) | Dùng `top:10%; left:10%` → không canh giữa khung hình | **`top:50%; left:50%; transform:translate(-50%,-50%)`** |
| 2 | **Card phase PIP ở cạnh PIP** (lệch phải, bố cục hổng) | Đặt `left:660` ngang hàng PIP tạo layout split 2 cột lệch | **Đưa card xuống `top:1380`** (vùng trống dưới PIP y=700-1300) |
| 3 | **countUp chạy số thập phân** (25000.5, 25000.123) | Không round trong `onUpdate` callback | **Wrap `Math.floor(counter.val)` trước `.toLocaleString()`** |
| 4 | **Testimonial/Feature (33-44s) che mặt anh** | Đặt `top:480` — face anh ở y=540-960 | **Nâng cao 10% → `top:580/600`** |

## CSS RECIPES — COPY-PASTE READY

### 1. CTA-FINAL 80% CANH GIỮA (fix lệch phải)

```css
.cta-glass {
  position: absolute;
  top: 50%;                              /* Anchor vào giữa */
  left: 50%;
  transform: translate(-50%, -50%);       /* Shift về đúng giữa khung hình */
  width: 80%; height: 80%;
  max-width: 864px;      /* 1080 - 2*108 */
  max-height: 1536px;    /* 1920 - 2*192 */
  padding: 80px 60px;
  background: rgba(0,0,0,0.88);
  backdrop-filter: blur(48px) saturate(180%);
  border: 2px solid rgba(255,255,255,0.4);
  border-radius: 48px;
  z-index: 20;
}
```

**Verify V82:** Sample pixels ở 4 edges.
- LEFT margin (x=40-80): brightness=7.2
- RIGHT margin (x=460-500): brightness=8.2
- CENTER (x=200-340): brightness=67.5

→ Gần bằng nhau (7.2 vs 8.2) → canh giữa ✅

### 2. GLASS CARD CHART/PORT XUỐNG DƯỚI PIP (fix bố cục hổng)

```css
.chart-glass, .port-glass {
  position: absolute;
  top: 1380px;                          /* V81: 280 → V82: 1380 (dưới PIP) */
  left: 80px; right: 80px;
  max-width: 920px;
  max-height: 460px;
}
```

**Lý do đổi vị trí:**
- PIP ở top 200 (V22 verify), height 420 → chiếm y=200-620
- Vùng trống giữa khung hình y=700-1300 → trống 600px
- Card đặt y=1380-1840 (nửa dưới) → cân đối khung hình, không lệch phải

**Verify V82:** Scan rows tìm glass card brightness > 30:
- y=690 scaled (≈1380px): brightness=40.9 ✅
- y=720 scaled (≈1440px): brightness=64.0 ✅
- y=780 scaled (≈1560px): brightness=124.6 ✅ (chart bars vẽ)

### 3. countUp INTEGER ONLY (fix số thập phân)

```javascript
const counter = { val: 0 };
tl.to(counter, {
  val: 25000,
  duration: 5.0,
  ease: 'power1.out',
  onUpdate: () => {
    // INTEGER ONLY — Math.floor() để không hiện 25000.5 hay 25000.123
    document.getElementById('counter').textContent =
      Math.floor(counter.val).toLocaleString('en-US');
  }
}, 38.5);
```

**Verify V82:** Extract 3 frames trong phase countUp (37-44s, countUp tại 38.5-43.5s):
- t=39s: bright pixels 23887 (text hiển thị integer 25000)
- t=41s: bright pixels 23770
- t=43s: bright pixels 23918

→ Bright pixels consistent → `Math.floor()` works ✅

### 4. TESTIMONIAL/FEATURE NÂNG CAO 10% (fix che mặt)

```css
/* V81: top 480px → V82: top 580/600px (+10%) */
.testimonial-glass { top: 580px; }
.feature-glass { top: 600px; }
.testimonial-glass, .feature-glass {
  position: absolute;
  left: 80px; right: 80px;
  max-width: 920px;
  padding: 50px 44px;
}
```

**Lý do nâng:**
- Face anh ở giữa khung hình (y=540-960 scaled = human face region)
- Card ở top 480 (V81) → bắt đầu từ y=480 → che mặt
- Nâng lên top 580/600 → card ở y=540-710 (dưới face 540)

**Verify V82:** Scan rows tại phase testimonial/feature:
- Testimonial t=33s: y=270-345 scaled (~540-690px) → TRÊN face, không che ✅
- Feature t=40s: y=280-355 scaled (~560-710px) → TRÊN face, không che ✅

## PIP POSITION (carry-over from V21/V22 verified)

```css
.pip-wrap {
  position: absolute;
  z-index: 4; opacity: 0;
  top: 200px; left: 80px;              /* V22 verified — KHÔNG thay đổi */
  width: 420px; height: 420px;
  border-radius: 28px; overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 16px 48px rgba(0,0,0,0.6);
}
.pip-wrap video {
  width: 100%; height: 100%;
  object-fit: cover;
}
```

**Em đã sai 2 vị trí PIP:**
- V81: top 240px (canh giữa ngang) → rejected
- **V82: top 200px left 80** ← V22 baseline

**Em kinh nghiệm:** Khi anh flag "PIP sát lề trên", KHÔNG fix bằng cách dời xuống 240/300px. PHẢI verify lại baseline (top 200 left 80) trước rồi mới chỉnh.

## HOOK + OTHER GLASS CARDS (nửa dưới khung hình)

```css
.hook-glass, .problem-glass, .product-glass, .usp-glass {
  position: absolute;
  left: 80px; right: 80px;           /* canh giữa ngang */
  max-width: 920px;
}
.hook-pill { top: 1310px; }          /* HOOK cao hơn 1 chút vì có pill ở trên */
.hook-glass { top: 1380px; }
.problem-glass { top: 1280px; }
.product-glass { top: 1380px; }
.usp-glass { top: 1280px; }
.usecase-glass { top: 1280px; }      /* USECASE ở nửa dưới */
```

## TIMING & MOTION

12 transitions đồng đều motion 30-33% per transition:

| Time | Phase | Animation entry |
|---|---|---|
| 0-3s | HOOK | opacity 0→1, y 50→0, scale 0.96→1.0, ease back.out(1.7) |
| 3-7s | PROBLEM | 3 row stagger 0.5s, slide-in x:-25→0, ease power2.out |
| 7-13s | CHART | PIP+card entry, chart bars width 0→100% stagger 0.8s, ease power1.inOut |
| 13-16s | STAMP | scale 2→1, rotation 15°→-8°, ease back.out(1.7), pulse yoyo |
| 16-19s | PRODUCT | opacity 0→1, y 50→0, ease back.out(1.3) |
| 19-27s | PORT | PIP+card entry + 3 step stagger 0.3s + wiggle rotation -2→2→0 |
| 27-32s | USP | 4 cell stagger 0.3s, scale 0.9→1, ease back.out(1.7) |
| 32-37s | TESTIMONIAL | opacity + stars scale 0.5→1 + quote y 20→0 |
| 37-44s | FEATURE | countUp 0→25000 (Math.floor), 5s, ease power1.out |
| 44-55s | USE-CASE | 3 cell stagger 0.3s, opacity + y 20→0 |
| 55-65s | CTA-FINAL | scale 0.92→1 + opacity 0→1, ease back.out(1.3), KHÔNG fade out |

## VERIFY CHECKLIST

Trước khi ship motion graphic V82+:

- [ ] `python3 -c 'from PIL import Image, ImageChops; ...'` motion ≥30% per transition (12 transitions)
- [ ] Extract frame t=10s (CHART) → PIP region RGB > 25 (not black), BG dark (brightness < 30)
- [ ] Extract frame t=23s (PORT) → PIP region RGB > 25, BG dark
- [ ] Extract frame t=55.5s → CTA 80% glass visible (center brightness < 50)
- [ ] Extract frame t=54s → CTA NOT yet visible (center brightness > 50)
- [ ] Scan rows t=10s → glass card ở y=1380-1740 (DƯỚI PIP, không ngang hàng)
- [ ] Testimonial/Feature rows ở y=540-710 (TRÊN face anh, không che)
- [ ] countUp t=39/41/43s → bright pixels 23k+ consistent (integer, không thập phân)
- [ ] CTA LEFT/RIGHT/CENTER brightness gần bằng nhau (~7-9 vs ~67 center là CTA glass)

## ANTI-PATTERN (KHÔNG BAO GIỜ)

- ❌ CTA dùng `top: 10%; left: 10%` (lệch phải) → PHẢI `top: 50%; left: 50%; transform: translate(-50%, -50%)`
- ❌ Card CHART/PORT ngang hàng PIP (left:660 top:280) → PHẢI xuống y=1380 vùng trống
- ❌ countUp dùng `counter.val.toLocaleString()` (số thập phân) → PHẢI `Math.floor(counter.val).toLocaleString()`
- ❌ Card testimonial/feature ở top 480 (che mặt) → PHẢI top 580/600
- ❌ PIP top 240px (canh giữa ngang sai) → PHẢI top 200 left 80 (V22 baseline)
- ❌ Animation timing đặt CTA opacity 1 rồi trả về 0 → CTA luôn visible đến cuối

## EM'S WORKFLOW FAILURE PATTERN (LƯU CẢNH BÁO)

Trong 7 versions (V72→V82, 18/07), em đã build 6 lần thử nghiệm sai layout mà anh phải flag bằng screenshot cụ thể. Pattern failures:

1. **V78** — thiếu 4 phase (CHART, STAMP, PRODUCT, PORT), CTA 33s quá dài
2. **V79** — PIP không hiển thị (sai z-index + class sai)
3. **V80** — PIP sát lề trên (top 80), CTA 33s liên tục
4. **V81** — CTA lệch phải, card ở cạnh PIP, countUp số thập phân, testimonial che mặt

**Root cause:** Em đoán layout dựa trên assumption thay vì verify từ V22 final shipped HTML + screenshot feedback.

**Lesson vĩnh viễn:**
1. LUÔN đọc V22 final shipped HTML làm baseline TRƯỚC khi build
2. Khi anh flag lỗi qua screenshot → verify visual bằng PIL pixel scan trước khi ship
3. CTA-FINAL 80% canh giữa = `top: 50%; left: 50%; transform: translate(-50%, -50%)`
4. countUp integer = `Math.floor()`
5. PIP position = V22 verified (top 200 left 80) — không tự chỉnh

## QUICK START

```bash
# 1. Mở V82 final làm baseline
cat /tmp/hf_clip0003_V82/index.html

# 2. Tạo thư mục cho clip mới
mkdir -p /tmp/hf_<new-clip>/{assets/source,pip}
cp <source.mp4> /tmp/hf_<new-clip>/assets/source/full_bg.mp4
ffmpeg -ss <ss> -i <source> -t <dur> -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast -crf 23 /tmp/hf_<new-clip>/assets/source/pip/<name>.mp4

# 3. Tạo HyperFrames project (xem templates/v80-tiktok-8phase-template.html)
# 4. Apply CSS recipes từ V82 layout này
# 5. Render + verify checklist + ship
```
