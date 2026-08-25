# PIP POSITION MATH — V13 vs V15 empirical analysis (19/07/2026)

Anh xác nhận V13 là version tốt nhất dù chưa có bo góc ("V13 là V làm tốt nhất tuy chưa có bo góc! V15 có bo góc một chút nhưng không đặt đúng vị trí!"). Đây là verification chi tiết.

## Source code diff (đọc từ HTML)

| Field | V13 ✅ (anh thích) | V15 ❌ (em sai) |
|---|---|---|
| `scale` | `0.42` | `0.42` |
| CHART `x` | **`-222`** | `-16` |
| CHART `y` | **`-540`** | `-130` |
| PORT `x` | **`+222`** | `-16` ← SAME AS CHART ❌ |
| PORT `y` | **`-540`** | `-130` ← SAME AS CHART ❌ |

## Pixel verification (ảnh PNG @ t=10s CHART)

| Metric | V13 | V15 |
|---|---|---|
| bbox | `(45,50)-(272,399)` | `(148,213)-(375,399)` |
| Size | **227×349** (portrait, top-left) | 227×186 (center) |
| ratio | 0.65 (portrait) | 1.22 (landscape — V15 clipPath fail) |
| Position | **TOP-LEFT ✅** | **GIỮA ❌** |

## The math behind V13 position

Video 1080×1920 với `transform-origin: 540px 960px` (center):

```javascript
tl.to(videoClip, {
  scale: 0.42,           // 1080×0.42 = 453, 1920×0.42 = 806 visible
  x: -222, y: -540,      // shift to put visible center at PIP target
  duration: 0.6
}, 7.0);
```

**Calculation:**
- Center của video sau scale = (540, 960) (vì transform-origin)
- Muốn center của video ở PIP CHART target center
- PIP CHART bounds V13 = `(45, 50)-(272, 399)` trong 540×960 display = real PIP center `(159, 225)` in 540×960 = `(318, 450)` in 1080×1920
- Offset needed = (target - current) = (318-540, 450-960) = (-222, -510)

**Quy tắc chung:**
- PIP CHART top-left (target center ~318,450):
  - `x = -(540 - target_x_center)` = `-(540-318)` = `-222`
  - `y = -(960 - target_y_center)` = `-(960-450)` ≈ `-540`
- PIP PORT top-right (target center ~762,450):
  - `x = +(target_x_center - 540)` = `+(762-540)` = `+222`
  - `y = -(540)` same
- Reset full screen: `x: 0, y: 0`

## Tại sao V15 sai

Em đổi sang `x: -16, y: -130` để "center mặt anh vào PIP" — nhưng 16/130 là quá nhỏ để đẩy PIP ra góc:
- `x: -16` shift nhẹ sang trái (16px) → PIP vẫn ở giữa
- `y: -130` shift lên trên (130px) không đủ để ra top
- CẢ 2 PIP (CHART + PORT) đều dùng CÙNG `(x: -16, y: -130)` → cả 2 ở giữa khung hình

## V17 wrapper dùng CSS (CHÍNH THỨC method)

V17 thay thế GSAP keyframe scale+position bằng **CSS hard-coded** (anh đã chấp nhận ở turn trước):

```css
.pip-clip {
  position: absolute;
  width: 420px;           /* FORCED square — KHÔNG cần scale */
  height: 420px;
  border-radius: 28px;    /* BO GÓC — KHÔNG GSAP needed */
  overflow: hidden;       /* CROP video */
  opacity: 0;             /* GSAP chỉ animate opacity */
  z-index: 5;
}
.pip-clip-chart { top: 200px; left: 108px; }    /* Top-left */
.pip-clip-port  { top: 200px; right: 108px; }   /* Top-right */
```

**Math check V17:**
- PIP size 420×420
- top 200px → top edge at y=200 (in 1920 height)
- left 108px (CHART) → left edge at x=108
- right 108px (PORT) → right edge at x=1920-420-108 = 1392

Cả 2 method đều đặt PIP ở **top-left và top-right** đúng cách. V13/V91 dùng GSAP transform math, V17 dùng CSS position hard-coded.

## Decision: chọn method nào?

| Method | Pros | Cons |
|---|---|---|
| GSAP transform (V12/V13/V91) | Animation mượt (scale up/down), reuse 1 video | Cần tính math transform-origin |
| CSS wrapper (V17) | Square + rounded guaranteed, dễ hiểu | Phải có bg video riêng cho full screen |

**Anh chọn**: anh cần V13 position chính xác (top-left/right) + V17 wrapper square + rounded → **V17 SHIPPED = KẾT HỢP cả 2**.

## VERIFY-CHECKLIST cho PIP mọi version (anh's feedback)

Sau render, **TRƯỚC KHI báo "work"** phải verify cả 4 check:

1. **Pixel bbox:** extract PNG @ t=phase-mid, tìm non-black bounding box
   - V13: `(45,50)-(272,399)` ✅ top-left
   - V15: `(148,213)-(375,399)` ❌ center
2. **Pixel ratio:**
   - square: 0.9 < w/h < 1.1
   - portrait: w/h < 0.9 (acceptable)
   - landscape: w/h > 1.1 (FAIL)
3. **Position check:**
   - Top-left PIP: bbox x1 < 100 (in 540×960)
   - Top-right PIP: bbox x2 > 440 (in 540×960)
   - Center: bbox x1 ~ 150, x2 ~ 380 (FAIL)
4. **Corner check (bo góc):**
   - exact-corner pixel brightness < 10
   - inside-corner (5px in) brightness > 50

Nếu CẢ 4 check pass → báo "verified". Nếu BẤT KỲ check nào fail → KHÔNG báo work, fix trước.

**Anh's mantra (V19 conversation):** "Pixel stats (`bright%`, `non-black%`) are NOT visual truth — user catches what I miss. Verify visually bằng PNG extract + vision_analyze."

## NEVER copy V15 position (x: -16, y: -130)

Code V15 đã deprecated. Mọi PIP motion graphic mới phải dùng **1 trong 2 method trên (V17 CSS wrapper hoặc V13 GSAP transform)** — không bao giờ copy `(x: -16, y: -130)` mà em đã tự ý thêm.

## Film to identify issues nhanh

```bash
# Extract frame tại giữa phase cần verify
ffmpeg -y -ss <phase_mid_time> -i output_silent.mp4 \
  -frames:v 1 -vf "scale=540:-1" /tmp/verify_t<t>.jpg

# Verify pixel bbox bằng Python
python3 -c "
from PIL import Image
img = Image.open('/tmp/verify_t<t>.jpg')
xs, ys = [], []
for y in range(50, 400):
    for x in range(20, 540):
        p = img.getpixel((x, y))
        if isinstance(p, tuple) and (p[0] > 30 or p[1] > 30 or p[2] > 30):
            xs.append(x); ys.append(y)
print(f'bbox: x={min(xs)}-{max(xs)}, y={min(ys)}-{max(ys)}')
print(f'position: {\"top-left\" if min(xs) < 100 else (\"top-right\" if max(xs) > 440 else \"center\")}')"
```

## Lesson vĩnh viễn

1. **V13 position math** (x: ±222, y: -540) vẫn là vị trí chuẩn — dùng cho GSAP transform approach
2. **V17 CSS wrapper** (top: 200px, left/right: 108px) là vị trí chuẩn — dùng cho wrapper approach
3. **Verify bằng pixel + vision** mỗi version — đừng báo "work" dựa trên stats
4. **Anh nhìn ra position sai** trước khi em đoán → tin feedback, không tự defend
