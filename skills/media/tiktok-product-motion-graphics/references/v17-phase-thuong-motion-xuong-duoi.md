# V17 Final Layout — Phase Thường Motion XUỐNG DƯỚI (verified 17/07/2026)

## Anh feedback verbatim (17/07 V17 trigger)

> *"Phân tích lại v6 đi anh thấy v6 là ưng ý anh nhất, chỉ cần chỉ cho các motion graphic ở các đoạn không crop video xuống dưới nữa là đẹp"*

Translation: **Anh thấy V6 layout đẹp nhất trong 17 versions**. Chỉ cần CHỈNH motion graphic ở phase **không có crop video (phase thường)** xuống PHÍA DƯỚI NỮA.

→ Decision: dùng **V6 layout làm base**, chỉnh `top:` của các glass cards ở phase thường từ 700 → 1020px (xuống nửa dưới màn hình). Phase crop (CHART/PORT) GIỮ NGUYÊN V6 layout (vì đã tận dụng khoảng giữa talking head).

## V17 → V16 evolution (chronology)

| Version | Phase thường (HOOK/PROBLEM/STAMP/PRODUCT/USP) top | Phase crop (CHART/PORT) top | Status |
|---|---|---|---|
| V14 | `top: 300px` | `top: 540px` (right column) | ❌ "Lộn xộn", CHÍNH/PHỤ chưa rõ |
| V16 | `top: 300px` (TOP) + `top: 1320px` (BOTTOM) | `top: 540px` (right column) | ✅ Về safe zones + CHÍNH/PHỤ, nhưng anh thấy motion thường vẫn ở giữa |
| **V17 (FINAL)** | **`top: 1020-1040px`** (CHỈ dưới, không top) | **`top: 720px` (V6 gốc)** | ✅ Anh ưng |

## V17 layout (final coordinates)

```css
/* ============================================================
 V17 — CHỈNH MOTION THƯỜNG XUỐNG DƯỚI, KEEP CROP PHASE V6
 ============================================================ */

/* Phase thường (HOOK, PROBLEM, PRODUCT, USP) — TẤT CẢ XUỐNG DƯỚI */
.hook-glass     { top: 1040px; left: 80px; right: 80px; }   /* "Sạc iPhone không cần dây" */
.hook-pill      { top: 920px; left: 50%; }                /* "⚡ ĐỜI MỚI" */
.problem-glass  { top: 1020px; left: 80px; right: 80px; } /* "01 02 03 nhỏ gọn" */
.product-glass  { top: 1020px; left: 80px; right: 80px; } /* "Củ sạc mini gắn iPhone" */
.usp-glass      { top: 1040px; left: 80px; right: 80px; } /* 4 cards 2x2 */

/* Phase crop (CHART, PORT) — GIỮ NGUYÊN V6 (top: 720 / 680) */
.chart-glass    { top: 720px; left: 80px; right: 80px; }   /* "Sạc cũ 500g vs 80g" */
.port-glass     { top: 680px; left: 80px; right: 80px; }   /* "Cắm vào là sạc 🔌→📱→🔋" */

/* STAMP — center (motion, không crop) */
.stamp-glass    { top: 50%; transform: translate(-50%, -50%) rotate(-8deg); }

/* CTA — bottom 100px (V6 gốc) */
.cta-glass      { bottom: 100px; }
```

## Lý do V17 PASS (so với V16 trước đó)

| Aspect | V16 | V17 |
|---|---|---|
| HOOK/PROBLEM motion | 2 zones (TOP Y=300 + BOTTOM Y=1320) | **1 zone DUY NHẤT ở dưới Y=1020** |
| Video full-frame top region | 0-580 (TRỐNG sau khi glass top bỏ) | 0-1020 (50% screen cho talking head trống tự nhiên) |
| Visual breathing room | Talking head bị che ở center | Talking head có **FULL không gian** từ Y=80 đến Y=920 |
| Nửa dưới màn hình | 1320-1920 chỉ có CTA/caption | 1020-1920 chứa TOÀN BỘ motion + CTA + caption |

## 8 phases layout map (V17 final)

```
0-2s  HOOK:    ⚡ ĐỜI MỚI pill (Y=920) + glass (Y=1040)
2-7s  PROBLEM: ⚡ Thời đại 2026 eyebrow (Y=920) + glass 3 rows (Y=1020)
7-13s CHART:   ⚫ BLACK bg + PIP 420×420 (top:80) + chart glass (top:720) [V6 gốc]
13-17s STAMP:  ☕ + NẶNG! rotated center (top:50%) [center motion]
17-19s PRODUCT: ⚡ Gochodoc pill (Y=920) + glass (Y=1020)
19-28s PORT:   ⚫ BLACK bg + PIP 420×420 (top:80) + port flow glass (top:680) [V6 gốc]
28-30s USP:    "Tại sao chọn" eyebrow (Y=920) + 4 cards glass (Y=1040)
30-32s CTA:    MUA NGAY gold button (bottom:100) + price (bottom:100)
```

## Verification (vision_analyze thật)

Verified frames V17:
- **Frame 2s (HOOK):** Mặt anh CỰC RÕ, cầm iPhone cổng Lightning. "⚡ ĐỜI MỚI" pill ở Y=920 (ngang trán, không che). Glass "Sạc iPhone **không cần dây**" ở Y=1040 (dưới cằm). Caption "Các bạn ơi, các bạn ơi" ở Y=1370 (rìa dưới).
- **Frame 6s (PROBLEM):** Mặt anh cúi xuống thao tác củ sạc. Dark glass "01 Thời đại này / 02 Cái gì cũng phải / 03 **nhỏ gọn**" ở Y=1020 (dưới cằm, không che). "⚡ THỜI ĐẠI 2026" eyebrow phía trên pill.
- **Frame 10s (CHART):** ⚫ BLACK bg + PIP 420×420 trái (mặt anh cầm củ sạc) + chart glass "⚖️ So sánh trọng lượng / Sạc cũ **500g** / Củ sạc này **80g** / Nhẹ hơn **6.2 lần**" ở Y=720 (KHÔNG clip, V6 gốc).

## Khi nào dùng V17 pattern

| Điều kiện | Layout dùng |
|---|---|
| **Anh thấy video full-frame cần nhiều space cho mặt** (talking-head chính) | **V17** — phase thường motion XUỐNG DƯỚI |
| Anh muốn chia đều TOP + BOTTOM (balanced) | V16 |
| Talking head không phải focus chính (info-heavy sản phẩm) | V14/V16 với glass 2 zones |

## Rule (FIRST-CLASS) — Phase thường motion ở DƯỚI

Khi phase KHÔNG có PIP (HOOK/PROBLEM/STAMP/PRODUCT/USP/CTA):
- **CHÍNH element (title lớn, image hero)** ở **Y = 1020-1340** (nửa dưới màn hình, full-width)
- **PHỤ eyebrow/pill** ở **Y = 880-940** (transition giữa talking head và glass)
- **Video gốc từ Y = 80 đến Y = 880** (≈ 40% screen) là **TRỐNG** để talking head hiện tự nhiên, không che

Khi phase CÓ PIP (CHART/PORT):
- GIỮ nguyên V6 layout (PIP góc trên trái + glass TRUNG TÂM)
- Lý do: PIP chiếm vùng talking head → cần fill khoảng giữa bằng info

## Anti-pattern (đã fail)

```css
/* ❌ V18 sai - đặt motion ở TOP khi talking head full-frame */
.hook-glass { top: 80px; left: 80px; right: 80px; }
/* → talking head bị che từ Y=80-460, dù glass frosted white nhưng
   vẫn obscures face video → user feedback "vẫn lộn xộn" */
```

```css
/* ✅ V17 đúng - talking head full-frame, motion ở dưới */
.hook-glass { top: 1040px; left: 80px; right: 80px; }
/* → talking head rõ 100% từ 0-880 */
/* → motion ở nửa dưới, không conflict với talking head */
```

## Source

V17 output: `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v17_32s_with_audio.mp4` (12.1 MB, 1080×1920, AAC 48000Hz stereo).

V17 build script: `/tmp/hf_sacduphong_v17/index.html` (single file, base = V6, chỉnh 4 glass cards).

V18 attempt (build all phases as V18 with NO crop) – not yet started. Will follow V17 pattern automatically.
