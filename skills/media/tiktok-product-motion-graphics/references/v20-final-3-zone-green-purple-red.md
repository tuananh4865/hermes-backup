# V20 FINAL — 3 vùng XANH/TÍM/ĐỎ theo ảnh Tuấn Anh vẽ (verified 17/07/2026)

## Bối cảnh

Sau V18 (anh đã ưng glass Y=1320 + caption Y=480 + bỏ watermark), **anh vẽ 1 ảnh mockup TikTok UI overlay** với 3 vùng màu rõ ràng:

- 🟢 **3 vùng XANH LÁ** → ƯU TIÊN đặt liquid glass card khi phase KHÔNG crop PIP
- 🟣 **Vùng TÍM** → đặt info khi phase CÓ crop PIP
- 🔴 **Vùng ĐỎ** (trán) → **KHÔNG ĐƯỢC ĐẶT BẤT CỨ THỨ GÌ**

## Vùng chính xác theo ảnh anh vẽ (1080×1920)

| Vùng | Màu | Tọa độ | Mục đích |
|---|---|---|---|
| 🟢 XANH 1 | Xanh lá | Y=100-240 (full-width: X=56-1024) | Glass TOP — title, eyebrow |
| 🟢 XANH 2 | Xanh lá | Y=720-880, X=60-680 (trái ngang mặt) | Glass MID khi không crop |
| 🟢 XANH 3 | Xanh lá | Y=970-1100 (trái dưới cằm) | Glass BOTTOM — stats |
| 🟣 TÍM | Tím | Y=400-950 quanh mặt (vùng talking head center) | Info elements khi CROP PIP |
| 🔴 ĐỎ | Đỏ | Y=250-400 (vùng trán) | **KHÔNG ĐƯỢC ĐẶT GÌ** (KHÔNG BAO GIỜ) |

## Layout V20 — phase-by-phase coords

### Phase thường (HOOK, PROBLEM, STAMP, PRODUCT, USP, CTA)

Khi phase KHÔNG có PIP, dùng video gốc full-frame. Đặt glass card ở **3 vùng XANH** (KHÔNG ở vùng ĐỎ, KHÔNG ở giữa mặt khi không crop):

| Phase | Vùng XANH 1 (top) | Vùng XANH 2 (trái ngang mặt) | Vùng XANH 3 (trái dưới cằm) |
|---|---|---|---|
| HOOK | — | "ĐỜI MỚI" pill + "Sạc iPhone không cần dây" | 3 stats (80g / ⚡ / 5K mAh) |
| PROBLEM | "⚡ THỜI ĐẠI 2026" eyebrow | 3 rows "01 / 02 / 03 nhỏ gọn" | — |
| STAMP | ☕ emoji center | — | "NẶNG!" + sub |
| PRODUCT | "⚡ Gochodoc" pill + "Củ sạc mini gắn iPhone" | "80 gram · Lightning · Sạc ngay" | — |
| USP | "Tại sao chọn củ sạc này?" title | 4 cards (80g / Lightning / 5.000mAh / 499K) | — |
| CTA | "Sẵn sàng nhẹ hơn" title | "MUA NGAY" button + "499K" | — |

### Phase crop (CHART, PORT) — dùng vùng TÍM

Khi phase có PIP + nhiều info, dùng **free-position elements** (chart-title, chart-bars, chart-result, mini-stats) ở vùng TÍM (xung quanh talking head), KHÔNG dùng 1 glass card wrapper lớn:

```html
<div class="chart-title" style="top: 540px; left: 480px; right: 60px;">
  ⚖️ So sánh trọng lượng
</div>
<div class="chart-bars" style="top: 620px; left: 480px; right: 60px;">
  <!-- 2 rows chart bars -->
</div>
<div class="chart-result" style="top: 880px; left: 480px;">
  Kết quả: Nhẹ hơn 6.2 lần
</div>
<div class="chart-mini-stats" style="top: 1080px; left: 60px; right: 60px;">
  <!-- 3 mini-stat pills -->
</div>
```

### Liquid glass opacity = 0.15 (anh yêu cầu V19)

```css
.glass {
  background: rgba(255, 255, 255, 0.15);  /* ← ANH CHỌN 0.15 */
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border: 1.5px solid rgba(255, 255, 255, 0.4);
  border-radius: 32px;
  padding: 24px 28px;
}
```

KHÔNG dùng 0.18 (đục) hoặc 0.08 (quá trong suốt) — 0.15 là sweet spot anh đã chọn.

## CSS implementation (copy-paste ready)

```css
/* === PADDING CHÍNH XÁC === */
.glass { left: 56px; right: 56px; }

/* === VÙNG XANH (phase thường) === */
.g-top     { top: 100px; }          /* XANH 1 - trên cùng */
.g-mid     { top: 720px; width: 620px; }   /* XANH 2 - trái ngang mặt */
.g-low     { top: 970px; width: 620px; }   /* XANH 3 - trái dưới cằm */

/* === VÙNG TÍM (phase crop - free-position elements) === */
.chart-right { top: 540px; left: 480px; right: 60px; }
.chart-bottom { top: 970px; left: 60px; right: 60px; }

/* === VÙNG ĐỎ (TRÁN) - KHÔNG ĐƯỢC ĐẶT GÌ === */
/* Y=250-400 = FORBIDDEN */

/* === PIP - GIỮ NGUYÊN V6 === */
.pip-wrap { top: 120px; left: 80px; width: 360px; height: 360px; }
```

## V20 verified frames (vision_analyze thật)

| Frame | Verify |
|---|---|
| 2s HOOK | ✅ Glass ở vùng XANH 2 (Y=720-880 ngang mặt trái) "ĐỜI MỚI + Sạc iPhone không dây" + Glass XANH 3 (Y=970-1100) "80g / ⚡ / 5K". Vùng đỏ trống. Mặt anh cực rõ. |
| 6s PROBLEM | ✅ Glass TOP ở vùng XANH 1 "⚡ THỜI ĐẠI 2026" + Glass XANH 2 "01 / 02 / 03 nhỏ gọn". Mặt anh rõ. |
| 10s CHART (crop) | ✅ BLACK bg + PIP 360×360 trái (mặt anh) + chart infographic ở vùng TÍM (Y=540-1080) "Sạc cũ 500g vs Củ sạc này 80g + Kết quả Nhẹ hơn 6.2 lần" + 3 mini stats ở vùng XANH 3 (Y=1080). |
| 16s STAMP | ✅ ☕ emoji trung tâm + "NẶNG!" ở vùng XANH 3. |
| 22s PORT (crop) | ✅ BLACK bg + PIP trái + port infographic ở vùng TÍM "⚡ Cắm vào là sạc + 🔌 → 📱 → 🔋 + Không cần dây cáp" + mini stats. |
| 28s USP | ✅ Glass TOP XANH 1 "Tại sao chọn củ sạc này?" + 4 cards ở XANH 2. |
| 30s CTA | ✅ Glass TOP XANH 1 "Sẵn sàng nhẹ hơn" + MUA NGAY button + 499K ở XANH 2. |

## Anti-patterns (CẤM)

### ❌ Đặt element ở vùng ĐỎ (Y=250-400)
```css
/* CẤM! */
.eyebrow { top: 300px; }  /* vùng đỏ! */
```
Anh V19: "Ở trung tâm trước mặt anh có một điểm đen lớn!!!" — khi overlay gradient ở giữa, hoặc text ở vùng đỏ tạo cảm giác "điểm đen giữa mặt".

### ❌ Glass card lớn chiếm cả vùng tím khi không có PIP
```css
/* CẤM! */
.chart-glass { top: 200px; height: 1100px; left: 60px; right: 60px; }
/* → Che kín mặt anh */
```

### ❌ Glass đặt ở giữa khi không có PIP
```css
/* CẤM! */
.cta-glass { top: 50%; transform: translateY(-50%); }
/* → KHÔNG CÓ transform khi không có context. Dùng top: cố định */
```

### ❌ Dùng dark glass thay vì frosted white
```css
/* CẤM! */
.glass { background: rgba(15, 20, 30, 0.92); }
/* → "Liquid glass cũng không còn" — frosted white mới đúng */
```

## Phân loại phase

| Đoạn có nhiều thông tin | → CROP PIP + free-position elements ở vùng TÍM |
| Đoạn bình thường (HOOK, STAMP, PRODUCT, USP, CTA) | → Video full-frame + glass ở 3 vùng XANH |

**Rule (FIRST-CLASS):** Phân loại phase dựa trên **LƯỢNG THÔNG TIN**, không phải thời lượng. Phase 2-3s nhưng nói nhiều info vẫn cần crop PIP. Phase 30s nhưng chỉ có 1 thông tin thì không cần crop.

## Lessons extracted

1. **Ảnh mockup của anh = ground truth** — khi anh vẽ/mockup, đó là layout anh thấy ưng. Dùng làm starting coords cho future clips.
2. **3 zones color system** — Green (glass allowed), Purple (info khi crop), Red (forbidden). Universal pattern across all phase layouts.
3. **Liquid glass opacity 0.15** — anh đã chọn sau khi thử 0.18 (đục) và 0.08 (quá trong). 0.15 = sweet spot.
4. **PIP + chart 2-cột** — đã pass qua V5/V14/V16/V20. Pattern ổn định.
5. **Caption bar ở `top: 480px`** (= 25% từ trên) — verified V18 ✓
6. **No watermark** — bỏ @tuancuaban từ V18 trở đi, trừ khi anh yêu cầu lại.

## Source

V20 output: `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v20_32s_with_audio.mp4` (12.9 MB, 1080×1920, AAC 48000Hz stereo)

V20 source: `/tmp/hf_sacduphong_v20/index.html` (single file, base = V18 + 3-zone green/purple/red)
