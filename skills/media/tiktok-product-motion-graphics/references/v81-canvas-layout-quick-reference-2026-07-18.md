# V81 LAYOUT VALUES — CANONICAL (Quick Reference)

> **Use khi build clip TikTok product motion graphics.** Đọc chi tiết: `references/v81-11phase-canvas-layout-2026-07-18.md`.

## PIP (CHART + PORT phase)

```css
.pip-wrap {
  position: absolute;
  z-index: 4; opacity: 0;
  top: 240px; left: 180px;          /* V80 sai: top 80px sát lề */
  width: 420px; height: 420px;
  border-radius: 28px; overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 16px 48px rgba(0,0,0,0.6);
}
```

## Glass Card CHART/PORT

```css
.chart-glass, .port-glass {
  position: absolute;
  top: 280px; left: 660px;          /* V80 sai: top 720 left 530 lệch */
  max-width: 360px; max-height: 560px; /* V80 sai: max 470 */
}
```

## Glass Card HOOK/PROBLEM/PRODUCT/USP

```css
.hook-glass, .problem-glass, .product-glass, .usp-glass {
  position: absolute;
  left: 80px; right: 80px;           /* canh giữa ngang */
  max-width: 920px; max-height: 480px;
}
/* HOOK/PRODUCT: top 1380 (cao hơn để có pill ở top 1280) */
/* PROBLEM/USP: top 1280 */
```

## Glass Card 3 phases mới (TESTIMONIAL/FEATURE/USECASE ở 32-55s)

```css
.testimonial-glass, .feature-glass {
  position: absolute;
  top: 480px; left: 80px; right: 80px;  /* centered vertically */
  max-width: 920px;
  padding: 50px 44px;
}
.usecase-glass {
  position: absolute;
  top: 1280px; left: 80px; right: 80px;
  max-width: 920px;
}
```

## CTA-FINAL 80% (CHỈ 10s cuối)

```css
.cta-glass {
  position: absolute;
  top: 10%; left: 10%; right: 10%; bottom: 10%;
  max-width: 864px; max-height: 1536px;
  padding: 80px 60px;                   /* rộng hơn V80: 24px → 60px */
}
```

**Animation CTA:**
```javascript
// Bắt đầu: tl.fromTo tại phase 55.0s (clip > 50s) hoặc tại phase 32s (clip ngắn)
// Kết thúc: KHÔNG tl.to('#cta-glass', { opacity: 0 }) — giữ visible đến cuối
tl.fromTo('#cta-glass', { opacity: 0, scale: 0.92, y: 60 },
  { opacity: 1, scale: 1, y: 0, duration: 0.8, ease: 'back.out(1.3)' },
  55.0  /* CLIPS > 50s: chỉ 10s cuối */
);
```

## 11-PHASE TIMELINE (clip > 50s)

| # | Phase | Time | Ghi chú |
|---|---|---|---|
| 1 | HOOK | 0-3s | pill + glass |
| 2 | PROBLEM | 3-7s | 3-5 rows stagger |
| 3 | **CHART** | 7-13s | PIP + nền đen + 4 bars |
| 4 | STAMP | 13-16s | "CHÍNH HÃNG" flash |
| 5 | PRODUCT | 16-19s | tên sản phẩm |
| 6 | **PORT** | 19-27s | PIP + 3 step flow |
| 7 | USP | 27-32s | 4 specs grid 2x2 |
| 8 | **TESTIMONIAL** | **32-37s** ⭐ | quote + author |
| 9 | **FEATURE HIGHLIGHT** | **37-44s** ⭐ | countUp 0 → 25.000 |
| 10 | **USE-CASE DEMO** | **44-55s** ⭐ | 3 cols 🚗💻🏠 |
| 11 | **CTA-FINAL 80%** | **55-65s** ⭐ | liquid glass 80% |

Cho clip < 50s: dùng 8 phase đầu + CTA từ phase 8 (32s) → tham khảo `v22-8phase-pattern-template-2026-07-18.md`.

## ANTI-PATTERN — KHÔNG BAO GIỜ

- ❌ PIP top 80px (sát lề trên)
- ❌ Card CHART/PORT max-width 470px @ left 530px (lệch phải)
- ❌ CTA 80% từ 32-65s cho clip > 50s
- ❌ Build < 11 phase cho clip > 50s
- ❌ countUp dùng linear ease

## VERIFY (trước ship)

```bash
python3 scripts/verify_tiktok_motion.py output_silent.mp4 audio.aac
```

Cần 5/5 evidence:
1. Spec TikTok 1080×1920 h264+aac
2. PIP @ CHART (t=10s) RGB > 25
3. PIP @ PORT (t=23s) RGB > 25
4. CTA @ t=55-65s full visible (center brightness < 50)
5. CTA @ t=54s NOT visible (brightness > 50)

**Motion threshold:** ≥25% pixels changed mỗi 5s đoạn đầu.

Xem chi tiết + CSS recipes + animation timing trong `references/v81-11phase-canvas-layout-2026-07-18.md`.
