# V91 — GSAP keyframe scale+position PIP pattern (CHUẨN CUỐI CÙNG)

**Added 19/07/2026 (V12 ship)** — Anh explicit: *"crop + scale down + reposition cho clip vào đúng vùng pip hiện tại luôn là được dùng kĩ năng keyframe của hyperframe để làm"*

## Tại sao đây là pattern CHUẨN

**4 cách em đã thử** (rank từ TỆ → TỐT):

| # | Pattern | Khi nào work | Verdict |
|---|---|---|---|
| ❌ | 2-3 video riêng (full_bg + pip_chart + pip_port) | KHÔNG BAO GIỜ | Em đã thử 5 versions (V5/V6/V7/V8/V9) đều fail hoặc partial. HyperFrames KHÔNG play real-time multi `<video>` element. **ĐÃ BỎ.** |
| ⚠️ | `<div class="pip-wrap" data-class="pip-X">` + `<video id="pip-X">` (V22 chính gốc) | Timeline ≤ 32s | Work ở V22 (32s clip) NHƯNG fail ở timeline >32s do HyperFrames headless timeout. |
| ⚠️ | **Thêm `opacity:0` initial cho CTA-glass** (V90 fix) | CTA đè full màn hình | BẮT BUỘC khi dùng V22 pattern — CTA 80%×80% + z-index 25 che timeline nếu thiếu opacity:0. |
| ✅ | **1 video element + GSAP keyframe scale+position** (V12, V91) | **Mọi timeline length, talking head clips** | **ĐÂY LÀ PATTERN CHUẨN.** 1 video, scale 0.42 + translate x/y → crop visible vào PIP bounds. KHÔNG cần 2-3 video riêng. |

## APPROACH V12/V91

```html
<!-- 1 VIDEO DUY NHẤT -->
<video id="video-clip" class="video-clip" data-start="0" data-duration="100"
       src="assets/source/full_bg.mp4" muted playsinline></video>
```

```javascript
// Phase CHART (7-13s) — Scale + position top-left
tl.to(videoClip, { scale: 0.42, x: -222, y: -540, duration: 0.6 }, 7.0);
// Phase PORT (19-27s) — Scale + position top-right
tl.to(videoClip, { scale: 0.42, x: 222, y: -540, duration: 0.6 }, 19.0);
// Reset về full screen
tl.to(videoClip, { scale: 1, x: 0, y: 0, duration: 0.5 }, 12.8);
tl.to(videoClip, { scale: 1, x: 0, y: 0, duration: 0.5 }, 26.8);
```

## Tính toán scale + position

- Video 1080×1920, transform-origin: `540px 960px` (center)
- PIP CHART top-left target center (318, 410) → offset `(-222, -540)`
- PIP PORT top-right target center (762, 410) → offset `(222, -540)`
- scale 0.42 → 453×806 visible, top-left corner at (318-226, 410-403) = (92, 7)

**Tính offset formula:**
- new_x = target_center_x - video_center_x * scale = 318 - 540*0.42 = 318 - 227 = 91 → WAIT không đúng
- Actual: `translate_x = target_center_x - video_center_x` (sau scale, video center moves to video_center + translate)
- new_center = video_center + translate = (540 + (-222), 960 + (-540)) = (318, 420) ✓

## Lợi ích

- KHÔNG cần 2-3 video riêng
- KHÔNG cần `<div class="pip-wrap">` wrapper
- KHÔNG cần `.black-bg` overlay (bg mặc định #000 OK)
- KHÔNG cần GSAP fade in/out riêng cho PIP — scale + position tự làm
- Work với mọi timeline length

## Khi nào KHÔNG dùng V12/V91

- Pure product showcase KHÔNG talking head (sac-du-phong 32s) → V22 OK
- Timeline ≤ 32s với 2-3 phases đơn giản → V22 chính gốc work

## Real case study (V12 clip_0006)

| Phase | t | CHART area | PORT area |
|---|---:|---|---|
| HOOK | 1s | ✅ 95.7% | ✅ 87.7% |
| CHART (PIP active) | 10s | **✅ 92.6%** (PIP) | (hidden) |
| PRODUCT | 15s | ✅ 98.2% | ✅ 92.1% |
| PORT (PIP active) | 20s | (hidden) | **✅ 90.7%** (PIP) |
| USP | 35s | ✅ 100% | ✅ 86% |
| FEATURE | 55s | ✅ 108% | ✅ 94% |
| CTA-FINAL | 95s | CTA 80% covers (correct) | CTA 80% covers (correct) |

**File**: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_V12_100s_FINAL_PIP_KEYFRAME.mp4` (54.7 MB, 100s)

## Templates — copy-paste starting point

Xem `templates/v80-tiktok-8phase-template.html` cho structure cơ bản, sau đó thay thế PIP logic bằng V12/V91 pattern nếu talking head.

## Pitfalls

1. ❌ Quên `transform-origin: 540px 960px` → scale không phải từ center
2. ❌ Scale quá nhỏ (≤0.3) → PIP hẹp, content khó đọc
3. ❌ Scale quá lớn (≥0.6) → PIP vẫn gần full màn hình
4. ❌ Translate sai hướng → PIP ở vị trí khác mong đợn
5. ❌ Quên reset về scale 1, x=0, y=0 sau phase PIP → tiếp tục ở PIP

## Verify pre-ship

```bash
# Extract PNG tại phase CHART/PORT
ffmpeg -ss 10 -i output_silent.mp4 -frames:v 1 t10_CHART.png
ffmpeg -ss 20 -i output_silent.mp4 -frames:v 1 t20_PORT.png

# Verify bright% trong PIP bounds
python3 -c "
from PIL import Image
img = Image.open('t10_CHART.png')
pixels = [p for p in img.crop((54, 100, 264, 310)).getdata() if isinstance(p, tuple)]
bright = sum(1 for p in pixels if (p[0]+p[1]+p[2])/3 > 80)
print(f'CHART bright%: {100*bright/len(pixels):.0f}%')
"
```

**Pass criteria:** CHART bright% > 80%, PORT bright% > 80% ở phase PIP active.