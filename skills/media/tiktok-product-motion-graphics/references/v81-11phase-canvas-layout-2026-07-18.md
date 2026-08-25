---
title: V81 11-PHASE CANVAS LAYOUT (canonical) — 2026-07-18
created: 2026-07-18
updated: 2026-07-18
tags: [motion-graphics, v81, 11-phase, canvas, layout, pip-center, cta-short]
---

# V81 11-PHASE CANVAS LAYOUT (canonical)

> **Status:** VERIFIED PASS. Em đã ship `clip0003_V81_65s_FINAL_with_audio.mp4` từ layout này.
> Motion 30-33%/12 transitions, PIP visible @ CHART/PORT, CTA chỉ 10s cuối, 3 phase motion graphic mới ở 32-55s.

## TẠI SAO V81 (KHÔNG PHẢI V22)

V22 (sac-du-phong 32s) thì 8 phase đủ vì clip ngắn. Clip > 50s (như clip 0003 65s) cần **11 phase** để tránh CTA quá dài, thêm emotional build-up (testimonial + feature + use-case) trước khi bán.

V80 (đã fail): 8 phase với CTA 80% từ 32-65s (33s liên tục) → quá dài, mất motion graphic info ở giữa.

V81 layout: 11 phase, CTA rút gọn 10s cuối, 3 phase motion graphic mới (testimonial/feature/usecase) chiếm 32-55s.

## LAYOUT CHUẨN — 11 PHASES

Khugn hình 1080×1920. Safe zone: 80px-1000px width × 80px-1840px height.

| # | Phase | Time | Position | Size | BG | Nội dung |
|---|---|---|---|---|---|---|
| 1 | HOOK | 0-3s | top 1380, left 80 right 80 | max-w 920 | Video bg | Title + eyebrow pill |
| 2 | PROBLEM | 3-7s | top 1280, left 80 right 80 | max-w 920 | Video bg | 3-5 pain points |
| 3 | CHART | 7-13s | **PIP top 240 left 180** + card top 280 left 660 | PIP 420×420 + card max-w 360 | **NỀN ĐEN** | 4 chart bars animate stagger |
| 4 | STAMP | 13-16s | center 50% 50% | 600×600 | Video bg | "CHÍNH HÃNG" flash |
| 5 | PRODUCT | 16-19s | top 1380, left 80 right 80 | max-w 920 | Video bg | Tên sản phẩm + brand |
| 6 | PORT | 19-27s | **PIP top 240 left 180** + card top 280 left 660 | PIP 420×420 + card max-w 360 | **NỀN ĐEN** | 3-5 step flow |
| 7 | USP | 27-32s | top 1280, left 80 right 80 | max-w 920 grid 2x2 | Video bg | 4 specs |
| 8 | TESTIMONIAL | 32-37s | top 480, left 80 right 80 | max-w 920 | Video bg | ⭐⭐⭐⭐⭐ + quote + author |
| 9 | FEATURE HIGHLIGHT | 37-44s | top 480, left 80 right 80 | max-w 920 center | Video bg | **countUp** 0 → 25.000 (5s) |
| 10 | USE-CASE DEMO | 44-55s | top 1280, left 80 right 80 | max-w 920 grid 3 cols | Video bg | 🚗💻🏠 |
| 11 | CTA-FINAL 80% | **55-65s** (CHỈ 10s cuối) | top 10% bottom 10% left 10% right 10% | max-w 864 max-h 1536 | Liquid glass full | Giá + specs + BH |

## LAYOUT VALUES — TỪNG PHẦN TỬ

### PIP (CHART + PORT phase)

```css
.pip-wrap {
  position: absolute;
  z-index: 4; opacity: 0;
  top: 240px; left: 180px;          /* MUST top 240 (V80 fail: top 80) */
  width: 420px; height: 420px;       /* MUST vuông — không 420×750 portrait */
  border-radius: 28px; overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 16px 48px rgba(0,0,0,0.6);
}
```

**Lý do top 240px:** V80 top 80px → PIP sát lề trên, anh flag. Top 240px canh giữa khung hình (240 + 420 = 660 từ trên xuống, centered).

**Lý do left 180px:** (1080 - 420) / 2 = 330, nhưng trừ thêm 150 để có khoảng trống bên trái cho tiêu đề/pill → 180. Hoặc tuỳ content — nếu chỉ cần centered thuần thì dùng left 330.

### Glass Card (CHART/PORT)

```css
.chart-glass, .port-glass {
  position: absolute;
  top: 280px; left: 660px;          /* MUST top 280 left 660 (V80 fail: top 720 left 530) */
  max-width: 360px;                 /* MUST max 360 (V80 fail: max 470 lệch) */
  max-height: 560px;                /* MUST max 560 (V80 fail: max 480) */
}
```

**Lý do top 280 left 660:** Top 280 = top 240 (PIP) + 40 (đệm). Left 660 = left 180 (PIP) + 420 (PIP width) + 60 (gap). Tổng: 180 + 420 + 60 + 360 = 1020px → còn 60px margin phải → canh giữa ngang.

**Lý do max-width 360:** Card width không quá PIP width (420). Nếu lớn hơn sẽ tràn khung hình.

### Glass Card (HOOK/PROBLEM/PRODUCT/USP) — nửa dưới

```css
.hook-glass, .problem-glass, .product-glass, .usp-glass {
  position: absolute;
  left: 80px; right: 80px;            /* MUST left/right 80 = canh giữa ngang */
  max-width: 920px;
  max-height: 480px;
}
/* HOOK/PRODUCT cao hơn (1380) vì có pill ở trên */
/* PROBLEM/USP thấp hơn (1280) */
```

### Testimonial/Feature/Usecase (32-55s)

```css
.testimonial-glass {
  position: absolute;
  top: 480px; left: 80px; right: 80px;  /* Centered VERTICALLY */
  max-width: 920px;
  padding: 50px 44px;
}

.feature-glass {
  position: absolute;
  top: 480px; left: 80px; right: 80px;
  max-width: 920px;
  text-align: center;                  /* Big number center */
}

.usecase-glass {
  position: absolute;
  top: 1280px; left: 80px; right: 80px;
  max-width: 920px;
  /* usecase grid: 3 columns x 1 row (no margin nửa dưới) */
}
```

### CTA-FINAL 80% (CHỈ 10s cuối)

```css
.cta-glass {
  position: absolute;
  top: 10%; left: 10%; right: 10%; bottom: 10%;   /* MUST 80% khung hình */
  width: 80%; height: 80%;
  max-width: 864px;      /* 1080 - 2*108 = 864 */
  max-height: 1536px;    /* 1920 - 2*192 = 1536 */
  padding: 80px 60px;
}
```

**Lý do KHÔNG từ 32s:** V80 CTA 32-65s (33s liên tục) → quá dài, anh flag. V81 CTA 55-65s (10s) → chỉ tổng hợp thông tin giá + specs + BH, KHÔNG cản trở 3 phase motion graphic ở 32-55s.

## SMOOTH MOTION RECIPE — ĐÃ VERIFY

```javascript
// Entrance — bouncy overshoot
tl.fromTo('#hook-glass', { opacity: 0, y: 50, scale: 0.96 },
  { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: 'back.out(1.7)' }, 0.5);

// Slide-in
tl.fromTo('#problem-row-1', { opacity: 0, x: -25 },
  { opacity: 1, x: 0, duration: 0.4, ease: 'power2.out' }, 3.5);

// Chart bar width — smooth ease
tl.to('#bar-good', { width: '100%', duration: 2.0, ease: 'power1.inOut' }, 8.2);

// Stagger 0.3-0.5s
tl.fromTo('#usp-1', ..., 27.7);
tl.fromTo('#usp-2', ..., 28.0);  // +0.3s
tl.fromTo('#usp-3', ..., 28.3);  // +0.3s

// Wiggle
tl.to('#pip-port', { rotation: -2, duration: 0.3, ease: 'sine.inOut' }, 23.0);
tl.to('#pip-port', { rotation: 2, duration: 0.3, ease: 'sine.inOut' }, 23.5);
tl.to('#pip-port', { rotation: 0, duration: 0.3, ease: 'sine.inOut' }, 24.0);

// CountUp — PHẢI dùng power1.out KHÔNG linear
const counter = { val: 0 };
tl.to(counter, { val: 25000, duration: 5.0, ease: 'power1.out',
  onUpdate: () => {
    document.getElementById('counter').textContent = counter.val.toLocaleString('en-US');
  }
}, 38.5);
```

## CTA TIMING — QUAN TRỌNG

| Time | Phase | CTA state |
|---|---|---|
| 0-32s | HOOK → USP | CTA opacity 0 |
| 32-37s | TESTIMONIAL | CTA opacity 0 |
| 37-44s | FEATURE | CTA opacity 0 |
| 44-55s | USE-CASE | CTA opacity 0 |
| 55-65s | CTA-FINAL | CTA opacity 1 (scale 0.92 → 1.0) |

**Animation CTA start:**
```javascript
tl.fromTo('#cta-glass', { opacity: 0, scale: 0.92, y: 60 },
  { opacity: 1, scale: 1, y: 0, duration: 0.8, ease: 'back.out(1.3)' }, 55.0);
// KHÔNG tl.to('#cta-glass', { opacity: 0 }) — CTA giữ visible đến cuối
```

**Verify CTA timing:**
```bash
for t in 54 55 55.5 56 57 60 62 64; do
  ffmpeg -ss $t -i output.mp4 -frames:v 1 -vf scale=420:-1 t=$t.jpg
done
# Sample center of 80% glass area (240, 300 in 420x747)
# t=54s brightness ~76 (CTA not visible)
# t=55.5s+ brightness ~20 (CTA full screen)
```

## SO SÁNH V22 vs V81

| Aspect | V22 (sac-du-phong) | V81 (clip 0003) |
|---|---|---|
| Số phase | 8 | **11** (8 + TESTIMONIAL + FEATURE + USECASE) |
| Clip length | 32s | 65s |
| CTA 80% | 32s-end (8s cuối) | **55-65s (10s cuối)** |
| PIP position | top 80px left 80px | **top 240px left 180px** (canh giữa) |
| Card CHART/PORT | top 720 left 530 max 470 | **top 280 left 660 max 360** (ngang hàng PIP) |
| HOOK glass position | top 1308 | **top 1380** (cao hơn 1 chút, dưới pill ở top 1280) |
| CTA card padding | 80px 24px | **80px 60px** (rộng hơn cho dễ đọc) |

## ANTI-PATTERN (KHÔNG BAO GIỜ)

- ❌ PIP top 80px (sát lề trên) → top 240px
- ❌ Card CHART/PORT max-width 470px lệch phải (top 720) → max-width 360px ngang hàng PIP (top 280)
- ❌ CTA 80% từ 32-65s (33s) → 55-65s (10s) + 3 phase motion graphic trước CTA
- ❌ Build < 11 phase cho clip > 50s
- ❌ CountUp dùng linear ease → dùng `power1.out`
- ❌ Animation timing đặt CTA opacity 1 rồi trả về 0 → CTA luôn visible đến cuối

## VERIFY CHECKLIST

Trước khi ship motion graphic:

- [ ] File duration = data-duration in HTML
- [ ] Bit rate 1.5-7 Mbps (verify ffmpeg)
- [ ] Motion ≥25% pixels/transition (verify PIL pixel diff)
- [ ] PIP @ CHART (t=10s) RGB > 25 (not black)
- [ ] PIP @ PORT (t=23s) RGB > 25 (not black)
- [ ] BG dark @ CHART/PORT (brightness < 30)
- [ ] CTA @ t=55-65s full visible (brightness < 50 center)
- [ ] CTA @ t=54s NOT visible (brightness > 50)
- [ ] Card canh giữa ngang (left+right 80px, max-width 920/360/864)
- [ ] Motion graphic phases 32-55s (testimonial/feature/usecase) có motion thật

## CẬP NHẬT TIẾP THEO

Khi áp dụng layout này cho clip mới:
1. Mở `/tmp/hf_<new-clip>/index.html`
2. Tìm tất cả `top: 80px`, `max-width: 470px`, `top: 530px` → replace theo V81 layout values
3. Thêm 3 phase motion graphic (TESTIMONIAL/FEATURE/USECASE) nếu clip > 50s
4. Chuyển CTA 80% từ phase 32 → phase 55 (nếu > 50s)

Xem `templates/v80-tiktok-8phase-template.html` làm starting base, scale to 11 phase nếu clip > 50s.
