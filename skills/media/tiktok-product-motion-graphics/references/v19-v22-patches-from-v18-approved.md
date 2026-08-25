# V19-V22: Patches và Bounce Back sau V18 Approved

## Context

V18 đã được Tuấn Anh approve (xem `references/v18-final-tuan-anh-approved.md`). Nhưng session tiếp theo, V19-V22 xảy ra:
- V19: Phase crop KHÔNG dùng glass card (anh muốn chart/infographic/text motion lấp đầy khoảng trống)
- V20: Build theo mockup ảnh 3 vùng màu (XANH/TÍM/ĐỎ) — bị HỦY vì "đặt lung tung"
- V21: Surgical patches V17 base (back track) — FINAL AFTER V20
- V22: Hạ glass card xuống 20% (Y=1308) — từ V21

**Lesson quan trọng: V18 "approved" KHÔNG có nghĩa là frozen state. Anh vẫn tiếp tục iterate thêm 4 versions (V19-V22). Pitfall 34 (STOP after "OK đẹp") chỉ dừng auto-iterate, không có nghĩa dừng KHI ANH GỬI FEEDBACK MỚI.**

## V19 (sau V18 approved) - Phase crop không dùng glass card

**Anh V19 verbatim:**
> *"Ở các đoạn crop video để show nhiều thông tin thì có thể không dùng card để biểu đạt nữa mà thay bằng chart, infographic hoặc motion graphic text chạy ra thôi vì những lúc như vậy có rất nhiều chỗ trống dưới phần video crop"*

**Refinement:** Phase có PIP (CHART, PORT) → KHÔNG dùng 1 glass card wrapper, dùng 4 free-position elements lấp đầy khoảng trống dưới PIP.

**V19 vs V18 layout (CHART phase):**

```html
<!-- ❌ V18: 1 glass card wrapper -->
<div class="glass chart-glass" style="top: 720px; left: 56px; right: 56px;">
  <div class="chart-title">⚖️ So sánh trọng lượng</div>
  <div class="chart-row">...</div>
</div>

<!-- ✅ V19: 4 free-position elements, không glass wrapper -->
<div class="chart-title" style="position: absolute; top: 560px; left: 500px;">
  ⚖️ So sánh trọng lượng
</div>
<div class="chart-bars" style="position: absolute; top: 640px; left: 500px; right: 80px;">
  <!-- 2 rows chart bars trực tiếp -->
</div>
<div class="chart-result" style="position: absolute; top: 880px; left: 50%; transform: translateX(-50%);">
  Kết quả - Nhẹ hơn <span style="color: #00e676;">6.2 lần</span>
</div>
<div class="chart-mini-stats" style="position: absolute; top: 1080px; left: 60px; right: 60px;">
  <!-- 3 mini-stat pills -->
</div>
```

**Liquid glass alpha rule từ V19:** Anh yêu cầu "tăng độ trong suốt 10%" — em interpret là GIẢM 10% opacity:
- V18 default: `rgba(255, 255, 255, 0.18)` (18% opacity)
- V19: `rgba(255, 255, 255, 0.08)` (8% opacity = 18% - 10%)
- Compensate bằng `backdrop-filter: blur(48px)` (tăng từ 32px → 48px)
- Verify: text trong glass vẫn đọc được trên talking head background

**Verified V19:** Frame 10s CHART phase vision_analyze PASS — chart rõ, mini-stats lấp đầy, không có vùng đen thừa. Output: `sac_du_phong_v19_32s_with_audio.mp4` 12.7MB.

## V20 (sau V19) - Layout theo mockup 3 vùng màu - BỊ HỦY

**Anh V20 verbatim:**
> *"Trong hình anh chia làm 3 phần màu xanh lá là nơi ưu tiên đặt liquid glass card khi video không crop pip"*

**Anh attach ảnh:** TikTok frame vẽ 3 vùng màu XANH (XANH-1 trên, XANH-2 ngang mặt trái, XANH-3 dưới cằm) = nơi đặt glass. Vùng TÍM = info khi CROP PIP. Vùng ĐỎ (Y=250-400 trán) = KHÔNG ĐƯỢC ĐẶT.

**Mistake V20:** Em build FULL architecture từ zero (file mới `/tmp/hf_sacduphong_v20/index.html`) theo mockup.

**Anh V21 verbatim (reject V20):**
> *"Không được em lại đặt bố cục lung tung hết lên rồi. Back về v17 không đổi layout nữa..."*

**Root cause:**
1. V20 base ≠ V18/V19 base → 1 base mới không verified
2. Mockup ảnh 3 vùng màu có thể KHÔNG khớp với layout V17/V18 → conflict với approved state
3. Em phá vỡ principle "approved state = baseline for iterations"

**Verified V20:** HOOK/PROBLEM/CHART PASS vision_analyze (3 frames), nhưng anh reject vì "lung tung".

## V21 - RECYCLE V17 base + 6 surgical patches (ĐÚNG CÁCH)

**Lesson từ V20 reject:** Khi anh nói "back về X" → RECYCLE X nguyên trạng + apply feedback mới, KHÔNG đổi architecture.

**Anh V21 verbatim (6 requests):**
> *"Back về v17 không đổi layout nữa thay vào đó giảm độ trong xuống 0.15 thay toàn bộ black card thành liquid card. Loại bỏ hoàn toàn 'anh đang nói' ở crop pip. Bỏ luôn caption. Và hơi nâng cao glass card lên một chút khoảng 5%"*

**Parsed 6 patches:**

| # | Patch | Before (V17) | After (V21) | CSS change |
|---|---|---|---|---|
| 1 | Liquid glass opacity | 0.18 (rgba) | **0.15** | `background: rgba(255, 255, 255, 0.15)` |
| 2 | Black card → Liquid card | `rgba(15, 20, 30, 0.92)` | `rgba(255, 255, 255, 0.15)` | `.chart-glass`, `.port-glass` |
| 3 | BỎ "ANH ĐANG NÓI" | `.pip-rec` có | **REMOVED** | CSS + HTML element |
| 4 | BỎ caption bar | `.caption-bar` có | **REMOVED** | CSS + HTML element |
| 5 | Nâng glass card lên 5% | top: 1020 → **924** | `top: 924px` | `5% × 1920 = 96px` |
| 6 | (ngầm) BỎ watermark | `.watermark` có từ V17 | **REMOVED** | CSS + HTML element |

**Critical lesson từ V21:**

**Patch 5 ("nâng cao 5%")** = "tăng Y lên 5% của canvas" → cộng `5% × 1920 = 96px` vào Y cũ:
- V17: `top: 1020px`
- V21: `top: 1020 - 96 = 924px`

**Patch 2 ("thay black card")** — multi-step, không chỉ đổi background:
```css
/* ❌ V17 (black) - WRONG */
.chart-glass {
  background: rgba(15, 20, 30, 0.92);    /* dark */
  color: rgba(255, 255, 255, 0.95);       /* white text */
  border: 1.5px solid rgba(255, 255, 255, 0.18);
}
.chart-name { color: rgba(255, 255, 255, 0.95); }

/* ✅ V21 (liquid frosted white) - CORRECT */
.chart-glass {
  background: rgba(255, 255, 255, 0.15);  /* light */
  color: #1a1a1a;                          /* dark text */
  border: 1.5px solid rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(40px) saturate(180%);
}
.chart-name { color: #1a1a1a; }
.chart-bar-track { background: rgba(0, 0, 0, 0.08); }  /* darken for contrast on white */
```

Khi chuyển dark → light glass: phải đổi cả text color (white → dark), contrast backgrounds, vì glass dùng light text sẽ mất contrast trên nền sáng.

**Verified V21 (vision_analyze 4 frames):**
- HOOK (2s): ✅ Glass "Sạc iPhone không cần dây" Y=924, NO @tuancuaban, NO ANH ĐANG NÓI, NO caption, mặt anh rõ
- CHART (10s): ✅ LIQUID GLASS frosted white 0.15, "Sạc cũ 500g vs 80g → Nhẹ hơn 6.2 lần"
- USP (28s): ✅ 4 cards "80g / Lightning / 5.000mAh / 499K"
- CTA (30s): ✅ "Sẵn sàng nhẹ hơn" + MUA NGAY + 499K (verify sau V21b fix)

**V21B fix:** Sau V21 vision verify thấy:
- Watermark vẫn còn (CSS class chưa bị ẩn) → patch `.watermark { display: none }` + `<div style="display: none">`
- CHART glass vẫn DARK ở phần text (border 0.18 thay vì 0.5) → patch border alpha
- CTA animation không hiện ở frame 30s → adjust timeline

Output V21b: `sac_du_phong_v21_32s_with_audio.mp4` 12.2MB. Final V21 PASS.

## V22 - Hạ glass card xuống 20% từ V21

**Anh V22 verbatim:**
> *"Hạ thấp glass card xuống 20%"*

**Critical interpretation rule (X% semantics):**

Khi anh nói "**hạ X%**" hoặc "**nâng X%**" → X% của CANVAS HEIGHT (1920px):
- "**Hạ X%**" = cộng `X% × 1920 = X × 19.2px` vào Y
- "**Nâng X%**" = trừ `X% × 1920` khỏi Y
- "**Gấp đôi**" (V18 refinement) = cộng khoảng cách trước đó × 1 thêm, KHÔNG phải × 2 tuyệt đối

**V21 → V22 calculation:**
- V21 glass: Y=924 (HOOK) và Y=904 (PROBLEM/PRODUCT/USP)
- "Hạ 20%" = `20% × 1920 = 384px`
- V22 glass: Y=924 + 384 = **1308** (HOOK/USP), Y=904 + 384 = **1288** (PROBLEM/PRODUCT)

**Code change V21 → V22:**
```css
/* V21 */
.hook-glass    { top: 924px; }
.problem-glass { top: 904px; }
.product-glass { top: 904px; }
.usp-glass     { top: 924px; }

/* V22 (after hạ 20%) */
.hook-glass    { top: 1308px; }   /* 924 + 384 */
.problem-glass { top: 1288px; }   /* 904 + 384 */
.product-glass { top: 1288px; }   /* 904 + 384 */
.usp-glass     { top: 1308px; }   /* 924 + 384 */

/* Phase crop GIỮ NGUYÊN */
.chart-glass   { top: 720px; }
.port-glass    { top: 680px; }
```

**Verified V22 (vision_analyze 3 frames):**
- HOOK (2s): ✅ "Sạc iPhone không cần dây" Y=1308. Mặt anh cầm củ sạc.
- PROBLEM (6s): ✅ "01 02 03 nhỏ gọn" Y=1288. Mặt anh đang nói.
- CHART (10s): ✅ Chart giữ Y=720 unchanged. Verify pass.

Output V22: `sac_du_phong_v22_32s_with_audio.mp4` 12.3MB.

## Lesson tổng kết V19-V22

### 1. "Approved" ≠ "Frozen"
- V18 đã approved, nhưng V19-V22 vẫn iterate với feedback MỚI
- Pitfall 34 ngăn auto-iterate, không ngăn feedback-iterate

### 2. "Back về X" = RECYCLE X nguyên trạng
- V20 build mockup từ zero → reject vì "lung tung"
- V21 RECYCLE V17 base + apply 6 patches → PASS
- Rule: "back về X" = `cp V17/index.html V21/index.html` + patches

### 3. X% semantics (PRECISE)
- "Hạ X%" = cộng `X% × canvas_height` vào Y
- "Nâng X%" = trừ `X% × canvas_height` khỏi Y
- "Gấp đôi" = cộng thêm khoảng cách đã dịch
- KHÔNG có ngoại lệ nào - công thức 1 dòng

### 4. Khi patch compound nhiều thứ, verify TỪNG patch 1 frame 1
- V21 em patch compound 6 thứ, chỉ verify HOOK → assume all OK → sai (watermark sót)
- V21b fix: verify ALL frames PASS trước khi ship
- Lesson: sau mỗi compound patch, verify lại TỪNG frame của TỪNG thay đổi

### 5. "Black → Liquid glass" không phải 1 dòng CSS change
- Phải đổi: background + text color + border + backdrop-filter + child colors
- Đây là 5 dòng CSS, không phải 1
- Verify visually: text trên light glass phải đọc được trên talking head

## Anti-pattern kết (5 lỗi V19-V22)

| Lỗi | Version | Cách tránh |
|---|---|---|
| Auto-iterate không có feedback mới | V19 sai lần 1 | Pitfall 34 |
| Build mockup từ zero, không từ approved | V20 destroy | RECYCLE base |
| Misinterpret "X%" semantic | V22 nếu không áp dụng công thức | Verified formula |
| Compound patches không verify từng cái | V21 verify incomplete | Verify 1-by-1 |
| Miss multi-step CSS change (dark → light) | V21 lần đầu | Surgical patch checklist |

## File outputs cuối cùng

| Version | Output | Status |
|---|---|---|
| V18 | `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v18_32s_with_audio.mp4` | Approved by anh |
| V19 | `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v19_32s_with_audio.mp4` | Refinement (free-position infographic) |
| V20 | `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v20_32s_with_audio.mp4` | Reject - lung tung |
| V21 | `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v21_32s_with_audio.mp4` | FINAL (sau V21b fix) |
| V22 | `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v22_32s_with_audio.mp4` | Final (hạ 20%) |

## Related

- `references/v18-final-tuan-anh-approved.md` — Base V18 (approved anchor)
- `references/v17-phase-thuong-motion-xuong-duoi.md` — V17 base (recycled cho V21)
- SKILL.md Pitfall 33 (V17/V18 coords) + Pitfall 34 (STOP after approval) + new Pitfall 41 (X% semantics)
