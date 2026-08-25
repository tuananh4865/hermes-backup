# V18 — V13 PIP POSITION METHOD (CHÍNH THỨC, anh approved)

**Validated:** 19/07/2026 — anh xác nhận "V13 là V làm tốt nhất tuy chưa có bo góc!"

## TL;DR

```javascript
// 1 video element + GSAP keyframe scale + position
tl.to(videoClip, { scale: 0.42, x: -222, y: -540, borderRadius: 28, duration: 0.6 }, 7.0);   // CHART top-left
tl.to(videoClip, { scale: 0.42, x: 222, y: -540, borderRadius: 28, duration: 0.6 }, 19.0);    // PORT top-right
tl.to(videoClip, { scale: 1, x: 0, y: 0, borderRadius: 0, duration: 0.5 }, 12.8);            // Reset
```

## Tại sao V13 method tốt nhất

1. **ĐÚNG vị trí** — pixel bbox verify: CHART bbox `(45, 50) - (272, 399)` top-left, PORT bbox `(267, 50) - (494, 399)` top-right
2. **Mặt anh rõ** — không scaleY riêng nên không méo như V14 (scaleY 0.22)
3. **Phần ngoài PIP = nền đen** — anh OK với điều này ("khi không có gì ở bg thì tự động nền sẽ có màu đen")
4. **Đơn giản** — chỉ cần 1 video element, KHÔNG cần wrapper div, KHÔNG cần clipPath

## Math (verified by pixel)

- **Video gốc:** 1080×1920 portrait, transform-origin `540px 960px` (center)
- **Scale 0.42:** video → 453×806 visible
- **CHART PIP target** top-left, center `(318, 410)` (1080/2 = 540, 200+420/2 = 410)
- **Offset:** `(318-540, 410-960)` = `(-222, -540)`
- **PORT PIP target** top-right, center `(762, 410)` (1080-108-420/2 = 762)
- **Offset:** `(762-540, 410-960)` = `(+222, -540)`

## 5 versions em đã sai trước đó

| # | Method | Why FAIL |
|---|---|---|
| V14 | `scaleX: 0.39, scaleY: 0.22` non-uniform | scaleY 0.22 nén chiều dọc → mặt bị méo |
| V15 | `scale: 0.42, x: -16, y: -130` | Cả 2 PIP ở giữa khung hình, KHÔNG phải top-left/right |
| V16 | `scale: 0.42 + clipPath: 'inset(193px 16.5px 193px 16.5px)'` | clipPath KHÔNG apply trong HyperFrames headless render |
| V17 | wrapper `<div class="pip-clip">` CSS `width: 420px, border-radius: 28px` | Work nhưng DƯ — V13 cũng đủ work cho anh |
| V95 | wrapper approach | Không phải cách anh muốn — anh xác nhận V13 tốt hơn |

## Anchor về kinh nghiệm của anh

5 lần liên tiếp em báo sai về PIP, vì:

1. Em **trust std theater** (pixel bright%) thay vì PNG extract + vision verify
2. Em **không check z-index + opacity** trước khi báo "limit"
3. Em **không check GSAP keyframe work** với HyperFrames render
4. Em **trust memory recap** thay vì đọc V22 HTML source thật
5. Em **scaleY** để ra vuông (V14) — sai vì méo mặt

→ **Lesson vĩnh viễn:** PNG extract + sample pixel bounds TRỰC TIẾP bên trong element. KHÔNG dựa std ở vùng khác.

## Khi nào dùng method khác (KHÔNG dùng V13)

| Anh muốn | Method | Reference |
|---|---|---|
| PIP VUÔNG 1:1 + bo góc 28px render thật | Wrapper `<div>` với CSS | `references/v97-pip-square-rounded-wrapper-method.md` |
| Background video full screen (không nền đen) | Thêm 1 bg video riêng | (chưa có reference — embed trong HTML) |
| Không cần PIP (chỉ full screen) | V22 chính gốc, 2 video riêng | `references/v22-canonical-workflow-summary-2026-07-18.md` |

## Workflow chính thức cho clip tiếp theo

```bash
# 1. Setup workspace
mkdir -p /Volumes/Storage-1/Hermes/scratch/hf_<clip>_v<n>
cd /Volumes/Storage-1/Hermes/scratch/hf_<clip>_v<n>

# 2. Copy source assets
mkdir -p assets/source/source
# Copy full_bg.mp4 và pip/*.mp4 nếu có

# 3. Write index.html with V13 method
# 1 video element + GSAP scale + position
# (see template in SKILL.md HARD RULE)

# 4. Render
npx --yes hyperframes render --quality draft --output output_silent.mp4

# 5. Verify visually
mkdir -p /tmp/verify
for t in 5 10 15 22 35 55 95; do
  ffmpeg -y -ss $t -i output_silent.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/verify/t${t}.png
done
# Use vision_analyze on each PNG to verify:
# - HOOK/PROBLEM/PRODUCT/USP/FEATURE: mặt anh full screen
# - CHART (t=10): PIP TOP-LEFT + mặt rõ
# - PORT (t=22): PIP TOP-RIGHT + mặt rõ
# - CTA (t=95): 80% full screen

# 6. Ship + ghép audio
ffmpeg -y -i output_silent.mp4 -i audio.aac \
  -c:v copy -c:a aac -b:a 128k -shortest \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<name>_v<n>_FINAL_V13_METHOD.mp4

# 7. Cleanup
rm -rf work-*/
```

## Verify checklist (4 bước trước khi ship)

```python
import subprocess
from PIL import Image

# Step 1: Pixel bbox CHART phase (t=10s)
subprocess.run(['ffmpeg', '-y', '-ss', '10', '-i', 'output_silent.mp4',
                '-frames:v', '1', '-vf', 'scale=540:-1', '/tmp/check.png'])

img = Image.open('/tmp/check.png')
# Find non-black bbox in top half
xs, ys = [], []
for y in range(50, 400):
    for x in range(20, 540):
        p = img.getpixel((x, y))
        if isinstance(p, tuple) and (p[0] > 30 or p[1] > 30 or p[2] > 30):
            xs.append(x); ys.append(y)

if xs and ys:
    bbox = (min(xs), min(ys), max(xs), max(ys))
    # CHART bbox MUST be in top-left (x < 300, y < 400)
    assert bbox[0] < 300, f"CHART PIP not top-left! bbox={bbox}"
    assert bbox[1] < 400, f"CHART PIP too low! bbox={bbox}"
    print(f"✅ CHART bbox: {bbox}")

# Step 2: Vision verify
# Call vision_analyze on /tmp/check.png
# Verify: PIP top-left, mặt rõ, glass card visible

# Step 3: Same for PORT phase (t=22s)
# bbox MUST be top-right (x > 250, y < 400)
```

## Anti-patterns to AVOID

| ❌ Anti-pattern | Why FAIL | ✅ Fix |
|---|---|---|
| `scaleX: 0.39, scaleY: 0.22` non-uniform | Méo mặt | `scale: 0.42` uniform |
| `clipPath: 'inset(...)'` GSAP keyframe | Không apply trong HyperFrames render | Scale + translate only |
| `x: -16, y: -130` (V15) | PIP lệch vào giữa | `x: ±222, y: -540` |
| `.cta-glass` thiếu `opacity: 0` | CTA đè full màn hình từ t=0 | `opacity: 0` CSS + GSAP fade in |
| Verify bằng std pixel ở vùng khác | Em đã sai 5 lần | PNG extract + sample pixel bounds TRỰC TIẾP |

## Sample PNG (V18 verified)

Anh có thể check V18 sample tại `/Volumes/Storage-1/Hermes/scratch/v18_samples/`:
- `t5_HOOK_full.png` — MẶT ANH + glass card "NGÀM NHANH THÁO LẮP"
- `t10_CHART_PIP.png` — PIP TOP-LEFT + glass "Thời gian thay lens" 3 bars ✅
- `t15_PRODUCT_full.png`
- `t22_PORT_PIP.png` — PIP TOP-RIGHT + glass "3 bước thay lens nhanh"
- `t35_USP_full.png`
- `t55_FEATURE.png`
- `t95_CTA.png`

V18 SHIPPED: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_V18_100s_FINAL_V13_METHOD.mp4` (54.6 MB, 100s)
