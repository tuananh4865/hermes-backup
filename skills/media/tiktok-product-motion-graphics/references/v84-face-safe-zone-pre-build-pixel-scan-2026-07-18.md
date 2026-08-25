---
title: V84 — Face-Safe-Zone Pre-Build Pixel Scan Protocol
created: 2026-07-18
type: reference
version: 1.0
applies-to: Mọi clip TikTok dọc có mặt người nói/cầm sản phẩm
priority: FIRST-CLASS — đọc TRƯỚC mọi build mới
---

# V84 Face-Safe-Zone Pre-Build Pixel Scan Protocol

> **Context:** Em đã sai 6 lần liên tiếp (V78→V84) trong cùng 1 session vì đặt card CHART/PORT và TESTIMONIAL/FEATURE sai vị trí CHE MẶT anh. Mỗi lần anh flag, em patch, lần sau lại sai. **Protocol này fix root cause: pixel scan screenshot TRƯỚC khi build** để xác định vùng mặt chính xác thay vì đoán.

## BÀI HỌC LỚN NHẤT TỪ V78-V84

**Không bao giờ dời card lên/xuống dựa trên cảm tính.** Lúc nào cũng pixel scan screenshot TRƯỚC:
- Tìm `y_top_of_head` (đỉnh tóc)
- Tìm `y_bottom_of_head` (cằm)
- Tìm `y_center_of_face` (giữa mặt)
- Tính `face_zone` = y_top_of_head → y_bottom_of_face
- Card PHẢI nằm NGOÀI face_zone (y < y_top_of_head HOẶC y > y_bottom_of_face)

**Anh explicit feedback (18/07/2026):**
> *"2 chỗ này nâng cao lên tới đỉnh đầu của anh còn lại giữ nguyên"*

Anh KHÔNG nói "nâng cao 10%" — anh nói **"tới đỉnh đầu"** = top < 200-300 (cách đỉnh tóc 50-100px).

## PROTOCOL 5 BƯỚC — CHẠY TRƯỚC MỌI BUILD

### Step 1: SCAN Screenshot anh cung cấp

```python
from PIL import Image
img = Image.open("screenshot.png")
w, h = img.size
print(f"Image: {w}×{h} (scale 1080×1920 reference)")

# Tìm mặt anh — skin tone R>G>B
skin_y_min, skin_y_max = h, 0
for y in range(0, h, 20):
    row = img.crop((w//4, y, 3*w//4, y+5))
    pixels = list(row.getdata())
    r_avg = sum(p[0] for p in pixels) / len(pixels)
    g_avg = sum(p[1] for p in pixels) / len(pixels)
    b_avg = sum(p[2] for p in pixels) / len(pixels)
    # Skin tone: 60 < R < 200, 50 < G < 180, 40 < B < 160, R > G
    if 60 < r_avg < 200 and 50 < g_avg < 180 and 40 < b_avg < 160 and r_avg > g_avg:
        skin_y_min = min(skin_y_min, y)
        skin_y_max = max(skin_y_max, y)

print(f"Face zone (scaled 1080×1920): y={int(skin_y_min*1920/h)} → y={int(skin_y_max*1920/h)}")
```

### Step 2: Xác định vùng safe

```python
# Safe zones cho card placement trên 1080×1920
SAFE_TOP_LIMIT = 192        # 10% × 1920 (PIP có thể đặt từ đây)
FACE_BOTTOM_SAFE = skin_y_min * 1920 / h  # y_top_of_head scaled
FACE_TOP_DANGER = skin_y_max * 1920 / h  # y_bottom_of_face scaled

print(f"SAFE_TOP_LIMIT: {SAFE_TOP_LIMIT} (PIP bắt đầu từ đây)")
print(f"FACE_BOTTOM_SAFE: {FACE_BOTTOM_SAFE} (card ở trên y này = không che mặt)")
print(f"FACE_TOP_DANGER: {FACE_TOP_DANGER} (card ở dưới y này = KHÔNG che mặt)")
```

### Step 3: Quyết định vị trí card

```python
# Decision tree:
# - Card testimonial/feature (text lớn): PHẢI trên FACE_BOTTOM_SAFE (y < 400)
# - Card hook/problem/product/usp/usecase (text ngắn): CÓ THỂ dưới FACE_TOP_DANGER (y > 1300)
# - Card CHART/PORT (nhiều data): KHÔNG BAO GIỜ ở giữa (y 400-1300)

if card_type in ['testimonial', 'feature', 'cta']:
    required_top = min(SAFE_TOP_LIMIT, FACE_BOTTOM_SAFE - 50)  # Cách đỉnh đầu 50px
    required_bottom = None  # Không quan trọng nếu đã ở trên đầu
elif card_type in ['hook', 'problem', 'product', 'usp', 'usecase']:
    required_top = FACE_TOP_DANGER + 50  # Dưới cằm 50px
    required_bottom = 1728  # Trên CTA 80%
elif card_type in ['chart', 'port']:
    # CHART/PORT có thể ở BÊN PIP, không che mặt
    required_top = PIP_TOP + PIP_HEIGHT + 100  # Dưới PIP 100px
    required_bottom = FACE_TOP_DANGER - 50  # Trên mặt 50px
```

### Step 4: Apply vị trí đã verify

```python
# Ví dụ: Testimonial card PHẢI đặt ở top < FACE_BOTTOM_SAFE
if FACE_BOTTOM_SAFE = 280:
    testimonial_top = min(200, FACE_BOTTOM_SAFE - 50)  # = 200
    print(f"Testimonial top = {testimonial_top} ✓ (cao hơn đỉnh đầu {FACE_BOTTOM_SAFE})")

# Feature card cũng ở vùng đỉnh đầu (y < 400) nhưng dưới testimonial 20px
feature_top = testimonial_top + 20
print(f"Feature top = {feature_top} ✓")
```

### Step 5: Verify sau khi render

```bash
# Extract frame tại phase có card, check card position
for t in 32 33 34 35 36 37 38 39 40 41 42 43; do
  ffmpeg -ss $t -i final.mp4 -frames:v 1 /tmp/verify_t$t.jpg
done

# Pixel scan: card PHẢI có brightness > 50 ở vùng đỉnh đầu (y < 400 scaled)
python3 -c "
from PIL import Image
img = Image.open('/tmp/verify_t33.jpg')
w, h = img.size
# Check y=0-100 scaled (= y=0-200 1080×1920) — phải có card brightness
for y in range(0, 100, 10):
    row = img.crop((50, y, w-50, y+3))
    pixels = list(row.getdata())
    avg = sum(sum(p) for p in pixels) / (len(pixels) * 3)
    if avg > 40:
        print(f'y={y} (~{int(y*1920/h)}px): brightness={avg:.1f} ✓')
"
```

## DECISION TREE — VỊ TRÍ CARD DỌC 1080×1920

| Phase card | Vùng y tốt | Vùng y CẤM (che mặt) | Lý do |
|---|---|---|---|
| HOOK | 1280-1380 | 240-1300 | Title ngắn, đọc 1 lần |
| PROBLEM | 1280-1380 | 240-1300 | 3 rows ngắn |
| CHART (PIP phase) | 700-1300 (ngang hàng PIP) | 240-700 | Chart bars animate |
| STAMP | 50% center | không quan trọng | Center flash |
| PRODUCT | 1280-1380 | 240-1300 | Tên sản phẩm |
| PORT (PIP phase) | 700-1300 (ngang hàng PIP) | 240-700 | 3 step flow |
| USP | 1280-1380 | 400-1280 | 4 specs grid |
| **TESTIMONIAL** | **0-400 (đỉnh đầu)** | **400-1700** | Text dài quote, dễ che mặt |
| **FEATURE (countUp)** | **0-400 (đỉnh đầu)** | **400-1700** | Số liệu lớn, dễ che mặt |
| USE-CASE | 1280-1380 | 400-1280 | 3 use cases grid |
| **CTA-FINAL 80%** | center 80% | viền 20% | Liquid glass full |

## REAL CASE: V83 vs V84

**V83 sai** (em đặt TESTIMONIAL top 600, FEATURE top 620):
- Pixel scan screenshot → face ở y=240-1300
- Card ở y=600 → CHE MẶT giữa

**V84 fix** (em pixel scan trước, đặt TESTIMONIAL top 200, FEATURE top 220):
- Pixel scan → face zone y=240-1300
- Card top < 400 → KHÔNG che mặt ✓
- Verify: card ở y=0-280px (scaled) → trên đầu anh

## ANTI-PATTERN VĨNH VIỄN

- ❌ Đặt TESTIMONIAL/FEATURE ở vùng giữa (y=400-1300) khi clip có talking head → CHE MẶT
- ❌ Đoán vị trí card bằng cảm tính → sai 6 lần liên tiếp
- ❌ Chỉ scan 1 screenshot rồi build → 1 screenshot có thể không đủ (anh nhiều phase)
- ❌ Tin V22/V83 baseline khi clip mới có mặt người khác (cần pixel scan lại)
- ❌ Bỏ qua Step 1-2 (scan screenshot) vì "đã biết vị trí rồi" → false sense of security

## SCRIPT: Pixel Scan tự động

```bash
python3 scripts/pixel_scan_face_zone.py screenshot.png 1080 1920
```

Output:
```
face_zone: y_top=280 y_bottom=1320
safe_top: y < 280 (cards placed here safe)
safe_bottom: y > 1320 (cards placed here safe)
forbidden: y 280-1320 (glass cards OVERLAP face - DO NOT PLACE)
```

## KHI NÀO DÙNG PROTOCOL

**LUÔN LUÔN** trước mọi build mới:
1. Khi anh gửi screenshot từ build cũ (bắt buộc scan)
2. Khi clip có mặt người (dù không có screenshot → estimate face zone y=240-1300)
3. Khi build từ V22 baseline với talking head

## EM ĐÃ SAI 6 LẦN VỚI CÙNG VẤN ĐỀ

V78, V79, V80, V81, V82, V83 — tất cả đều sai vì em đặt card sai vị trí dựa trên:
- Đoán từ layout cũ
- Dùng V22 baseline mà không adjust cho talking head
- Quên check screenshot từ anh

**Protocol này fix root cause**: pixel scan → decision tree → verify sau render.

## VERIFY CHECKLIST 5 BƯỚC

1. ✅ Step 1: pixel scan screenshot, tìm face zone y_top/y_bottom
2. ✅ Step 2: tính SAFE_TOP_LIMIT = 192, FACE_BOTTOM_SAFE = skin_y_min
3. ✅ Step 3: dùng decision tree để quyết định card_type → required_top
4. ✅ Step 4: apply vị trí đã verify (TESTIMONIAL/FEATURE top < FACE_BOTTOM_SAFE - 50)
5. ✅ Step 5: render + pixel scan verify card ở y < 400 (đỉnh đầu)

## KHI ANH GỬI SCREENSHOT MỚI

1. Đọc ảnh ngay (em hay skip phần này)
2. Pixel scan để confirm face zone
3. So sánh với vị trí card hiện tại
4. Apply decision tree để dời card
5. KHÔNG đoán — dùng math

## Liên quan

- V22 baseline workflow: `## 🔴 V22 PIP + GLASS WORKFLOW CHÍNH GỐC` ở SKILL.md
- Hard rule safe zone 10%: `## 🟢 V83 RECAP` ở SKILL.md
- Anti-pattern chain-edit: `## 🟢 V78 FRESH-FROM-SOURCE WORKFLOW` ở SKILL.md
- Liquid glass CSS recipe: `## 🔴 V7.1 NATE HERK ALIGNMENT` ở SKILL.md
