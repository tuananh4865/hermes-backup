# V23-V24: Thẻ bự cuối + Phóng to 80% (FAIL do CSS conflict)

## Context

Sau V22 (hạ glass card xuống 20%), session tiếp theo V23 → V24:
- **V23**: Anh muốn **đoạn cuối (CTA phase)** thay bằng "thẻ bự chiếm 70% khung hình"
- **V23**: Bỏ chữ "Mua Ngay" hoàn toàn (chỉ giữ specs + price)
- **V24**: Phóng to thẻ từ 70% lên **80%** bao phủ khung hình

---

## V23: Thẻ bự 70% khung hình + Bỏ "Mua Ngay"

### Anh V23 verbatim

> *"Đoạn cuối lúc chốt lại xong thông số thì cho cái thẻ bự lên chiếm 70% khung hình và bỏ chữ mua ngay đi"*

### Pitfall 44 — "70% khung hình" semantics (FIRST-CLASS — verified V23)

Khi anh nói "**thẻ chiếm X% khung hình**" → tỷ lệ CHỈ MỘT CHIỀU (height hoặc width):

- Portrait video (1080×1920): "X% khung hình" mặc định = **X% của HEIGHT (1920)**
- Width giới hạn ở `left: 30-80px right: 30-80px` (≈ 920-1020px)
- Card height = X × 1920 / 100; top = (1920 - height) / 2 để center

```python
# V23: "70% khung hình" portrait
card_height = 70 * 1920 / 100  # = 1344px
card_top    = (1920 - 1344) / 2  # = 288px (center)
```

**Anti-pattern:**

| Sai | Đúng |
|---|---|
| ❌ "70%" = 70% × 1080 = 756px width | ✅ 70% của height = 1344px |
| ❌ "70%" = 70% × cả 2 chiều | ✅ Chỉ 1 chiều |
| ❌ Top = 0 (kéo dài đến đáy) | ✅ Top = 288px (center) |

### Pitfall 45 — Animation timing cho "thẻ bự" (FIRST-CLASS — verified V23)

Card to = animation duration phải lớn hơn:
- Card nhỏ (V18, 60% width): fade 0.6s đủ
- Card bự (V23, 70% height): fade 0.9s + scale + y motion
- **MUST**: card visible ≥ 2s cuối (30s → 32s), KHÔNG có `tl.to()` fade out

```javascript
// V23 FIX (đề xuất - chưa PASS hoàn toàn)
tl.fromTo(ctaGlass, { opacity: 0, scale: 0.7, y: 100 },
  { opacity: 1, scale: 1, y: 0, duration: 0.9, ease: "back.out(1.1)" }, 29.7);
// KHÔNG có tl.to() fade out → card stable đến hết 32s
// Components stagger 30.5 → 31.5
```

### V23 CSS template

```css
.cta-glass {
  position: absolute;
  z-index: 20;
  left: 30px;
  right: 30px;
  top: 288px;
  height: 1344px;
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(40px) saturate(180%);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 48px;
  padding: 60px 56px;
  box-shadow: 0 32px 96px rgba(0, 0, 0, 0.5), inset 0 2px 0 rgba(255, 255, 255, 0.6);
}

.cta-specs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 24px;
}

.cta-spec {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(24px);
  border: 1.5px solid rgba(255, 255, 255, 0.4);
  border-radius: 28px;
  padding: 36px 28px;
  text-align: center;
}

.cta-price-final {
  background: rgba(255, 215, 0, 0.95);
  padding: 22px 36px;
  border-radius: 60px;
  display: inline-block;
}
.cta-price-final .price-num {
  font-size: 56px;
  font-weight: 900;
  color: #000;
}
```

### V23 specs 2×2 grid

- Spec 1: ⚡ 80g - Nhẹ nhất VN
- Spec 2: 🔌 Lightning - Cắm thẳng iPhone 12+
- Spec 3: 🔋 5.000 mAh - Sạc đầy 1 lần
- Spec 4: 📐 80×80 mm - Nhỏ gọn bỏ túi

Price dưới cùng (không button Mua Ngay): `790K 499.000đ`

### V23 frame analysis (PARTIAL_PASS)

- **Frame 30s**: ✅ Thẻ 70% hiện (3/4 specs visible), KHÔNG "MUA NGAY"
- **Frame 32s**: ⚠️ Specs hiển thị rời rạc — animation timing không stable 30-32s

---

## V24: Phóng to 80% — FAIL do CSS conflict (CRITICAL LESSON)

### Anh V24 verbatim

> *"Đoạn cuối anh nói là liquid glass card phòng to lên bao phủ 80% khung hình để show thông số rõ hơn mà"*

### Card size calculation

| Phase | height (px) | top (px) | left/right (px) |
|---|---|---|---|
| V23 (70%) | 1344 | 288 | 30 |
| **V24 (80%)** | **1536** | **192** | **0** (full edge) |

```css
/* V24 target */
.cta-glass {
  left: 0px;
  right: 0px;
  top: 192px;
  height: 1536px;
  padding: 80px 72px;
  border: 2.5px solid rgba(255, 255, 255, 0.55);
  border-radius: 56px;
}
```

### Pitfall 46 — Patch nhiều lần gây CSS conflict (FIRST-CLASS — verified V24 FAIL)

**V24 root cause:** Em copy V23 → patch 8 chỗ trên cùng file (`.cta-glass` size, `.cta-glass::before`, `.cta-btn { display: none !important }`, v.v.) → render → **KHÔNG thấy thẻ bự ở frame 30s và 32s**. Chỉ thấy video gốc + mặt anh.

**Vấn đề có thể xảy ra:**
- CSS class `.cta-glass` có nhiều patch → specificity war
- `.cta-btn { display: none !important }` có thể ảnh hưởng parent context
- `!important` gây khó debug
- Animation `opacity: 0` initial không reset khi CSS thay đổi

**V24 timeline FAIL:**

```
Copy V23 → V24 base
Patch .cta-glass top: 288 → 192, height 1344 → 1536 ← OK
Patch border-radius 48 → 56 ← OK
Patch .cta-glass::before gradient ← OK
Patch override .cta-btn { display: none !important } ← NGUY HIỂM
Render → KHÔNG thấy thẻ ở frame 30s/32s ← FAIL
```

### CRITICAL: 4 Rules phải apply cho mọi version sau

**Rule 1: KHI STRUCTURAL CHANGE → WRITE_FILE FRESH, không patch**
- ❌ Anti-pattern: copy file cũ + patch nhiều chỗ
- ✅ Correct: `read_file` base → `write_file` toàn bộ file mới
- Lý do: tránh CSS class conflict + animation timing broken

**Rule 2: KHI PATCH NHỎ (1-2 chỗ) → patch OK**
- Color, top/left single, opacity → OK
- Nhiều chỗ hoặc structural → write_file fresh

**Rule 3: KHI FAIL SAU PATCH → ROLLBACK + VIẾT LẠI**
- ĐỪNG cố patch thêm để "fix"
- ĐỪNG hỏi anh option A/B (anh sẽ frustrated)
- TỰ quyết: viết lại fresh, render lại, verify từ đầu

**Rule 4: KHÔNG BAO GIỜ DÙNG `!important` TRONG CSS**
- Gây specificity war không thể debug
- Khó maintain khi revert
- Thay vào đó: selector cụ thể hơn hoặc viết lại structure

### V24 workflow đáng lẽ phải làm

```bash
# ❌ Sai (đã làm trong V24)
cp /tmp/hf_sacduphong_v23/index.html /tmp/hf_sacduphong_v24/index.html
# ... 8 patches ...

# ✅ Đúng
read_file /tmp/hf_sacduphong_v22/index.html  # V22 là base đã approved
# Viết fresh V24 với CTA mới (80% thẻ) - toàn bộ file
write_file /tmp/hf_sacduphong_v24/index.html
# Verify ngay
```

### Output V23 + V24

| File | Status |
|---|---|
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v23_32s_with_audio.mp4` | PARTIAL_PASS (animation timing cuối chưa perfect) |
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v24_32s_with_audio.mp4` | FAIL — card KHÔNG hiện. Cần V25 write_file fresh |

## Related

- SKILL.md: Pitfall 41 (X% position) + 44 (70% card), 45 (animation), 46 (CSS conflict)
- `references/v19-v22-patches-from-v18-approved.md` — Timeline V19-V22
- `references/v18-final-tuan-anh-approved.md` — V18 base approved
