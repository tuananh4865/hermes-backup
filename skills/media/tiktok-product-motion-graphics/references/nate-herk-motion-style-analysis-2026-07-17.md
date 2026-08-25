---
title: "Nate Herk Motion Graphics Style — Reference Analysis Aw3BkmhYu4I"
created: 2026-07-17
updated: 2026-07-18
type: reference
tags: [nate-herk, motion-graphics, reference-bar, liquid-glass, text-motion, tiktok-product, hyperframes]
source: https://www.youtube.com/watch?v=Aw3BkmhYu4I
relationships: [tiktok-product-motion-graphics, hyperframes-creative, v22-case-study]
---

# Nate Herk — Motion Graphics Style Reference

> **Video:** "Claude Video Editing Just Became Unrecognizable" — Nate Herk | AI Automation
> **Ngày:** 23/04/2026 | **Độ dài:** 26 phút | **Views:** cao
> **Concept:** Claude Code orchestrate end-to-end editing pipeline (raw footage → video-use → HyperFrames → final render)
> **Dùng làm:** Reference bar cho mọi clip TikTok product motion graphics của anh. KHÔNG copy 100% — adapt theo V7 specs.

---

## 1. 5 Element Reference → Adapt cho Project (verified V22)

| Element | Reference Nate Herk | Adapt V22 (verified) | V7 hiện tại |
|---|---|---|---|
| **Glass card style** | iOS 26 liquid glass + frosted backdrop blur | opacity 0.15, blur(40px) saturate(180%) | **opacity 0.18, blur(48px) saturate(200%)** |
| **PIP placement** | Top-left corner + talking head | 420×420 (V17) → 360×360 (V18+) | 420×420 |
| **Font** | Hand-drawn Caveat cho title | SF Pro Display + Caveat (optional) | SF Pro Display 64-72px |
| **Animations** | Slide-in + scale back.out per-element | GSAP back.out(1.2) + clip-path reveal | **Stagger 120ms từng dòng** |
| **Color palette** | Blue/purple accent + white text | Yellow #FFD700 accent + white text | Match |

---

## 2. V7 vs Nate Herk — Diff (cần biết để adapt)

| Thuộc tính | Nate Herk | V7 hiện tại | Đánh giá |
|---|---|---|---|
| **Opacity** | 0.15 | **0.18** | ✅ Đúng yêu cầu anh "trong suốt quá" |
| **Blur** | 40px | 48px | ✅ Dày hơn = mờ nhám hơn |
| **Border** | 0.35 | 0.4 | ✅ Border đậm hơn |
| **Border-radius** | 32px | 36px | ✅ Match |
| **Padding** | 40px 36px | 40px 36px | ✅ Match |
| **Box-shadow** | 0 24px 64px 0.4 | 0 14px 42px 0.55 | ⚠️ Nate Herk rộng + nhẹ hơn |
| **Title font** | Caveat (hand-drawn) | SF Pro Display 64-72px | ⚠️ Nate Herk dùng Caveat |
| **Animation** | Slide-in per-element | ✅ Stagger 120ms | ✅ Match |
| **PIP** | 360×360 | 420×420 | ⚠️ Lớn hơn (giữ vì mặt anh to) |
| **Text motion** | Per-element slide-in | ✅ Stagger 120ms | ✅ Match |

---

## 3. Liquid Glass Recipe Nate Herk (verbatim từ case study V22)

```css
.glass {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(40px) saturate(180%);
  border: 1.5px solid rgba(255, 255, 255, 0.35);
  border-radius: 32px;
  padding: 40px 36px;
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
}
```

**Phase crop layout (CHART/PORT) từ Nate Herk:**
- **PIP**: 360×360 TRÁI (X=80-440), Y=540-900
- **Chart/Port glass**: PHẢI (X=480-1024), Y=540-820
- **NO "ANH ĐANG NÓI" label** (đã bỏ V21+)
- **NO caption bar** (đã bỏ V21+)
- **NO @tuancuaban watermark** (đã bỏ V19+)

---

## 4. 5 Điều Nate Herk Làm Mà V7 Chưa Có (gợi ý V8)

1. **Mask transition giữa các phase** — dùng mask hình tròn/mặt nạ reveal nội dung mới
2. **Background gradient shift** theo phase (subtle) — mỗi phase tint nhẹ
3. **Camera shake** ở phase STAMP/USP (rất subtle ~1-2px)
4. **Caveat font cho title** — signature hand-drawn style
5. **Per-word highlight** — mỗi từ quan trọng có hiệu ứng riêng (underline, glow)

---

## 5. V7 Standard Liquid Glass (Final Approved 18/07)

```css
.phase-glass {
  position: absolute;
  z-index: 20;
  left: 56px;
  right: 56px;
  padding: 40px 36px;
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(48px) saturate(200%);
  -webkit-backdrop-filter: blur(48px) saturate(200%);
  border: 1.5px solid rgba(255, 255, 255, 0.4);
  border-radius: 36px;
  box-shadow:
    0 14px 42px rgba(0, 0, 0, 0.55),
    inset 0 2px 0 rgba(255, 255, 255, 0.22);
}
```

**Migration V6 → V7:**
| Property | V6 | V7 |
|---|---|---|
| opacity | 0.15 | **0.18** |
| blur | 40px | **48px** |
| border | 0.32 | **0.4** |
| radius | 32px | **36px** |
| padding | 30px 24px | **40px 36px** |
| Title | 48px | **64px** |
| Text motion | Cả card | **Stagger 120ms** |

---

## 6. Adapt cho dự án anh

Khi làm clip TikTok product mới:
1. Dùng V7 specs (đã approved) — KHÔNG dùng V6
2. Reference Nate Herk chỉ để check pattern (per-element motion, glass style, PIP)
3. Có thể thử Caveat font cho title nếu muốn "cá tính" hơn
4. Bỏ mask transition + camera shake cho V7.1 (nếu anh thích)
5. VẪN dùng wiki product specs (KHÔNG tự suy đoán specs/giá)

---

**Saved by:** transcript-saver hook | **Source:** raw transcript session 17/07/2026 + V22 case study
**Reference chain:** `sac-du-phong-mini-iphone-22-versions-case-study.md` → V7 liquid glass standards → file này
