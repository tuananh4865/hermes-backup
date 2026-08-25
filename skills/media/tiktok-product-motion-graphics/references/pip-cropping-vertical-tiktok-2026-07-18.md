---
title: "PIP Cropping Pattern for TikTok Vertical (Portrait 1080x1920)"
created: 2026-07-18
type: reference
tags: [pip, ffmpeg, tiktok-vertical, motion-graphics, clip-0003]
---

# PIP Cropping for TikTok Vertical Videos

## Problem (Pitfall 59 - FIRST-CLASS, verified 18/07 clip_0003 V72 FAIL)

When extracting a Picture-in-Picture (PIP) from a 1080×1920 portrait source video to overlay on a TikTok vertical clip, the naive command:

```bash
# ❌ WRONG - this is what created the black-background PIP clip_0003 V72 (anh rejected 18/07)
ffmpeg -i source.mp4 -vf "crop=ih*9/16:ih:0:0,scale=420:750" pip.mp4
```

Results in:
- **`crop=ih*9/16` = `1080*9/16` = 607px wide** — only crops a 607×720 region from the top of the 1080×1920 source
- The face (Y=504-1317) gets **cropped out** entirely
- The remaining region (Y=0-720) is mostly **black background** because talking-head source videos have black wall above the subject's head

Result: PIP shows a small black rectangle instead of the speaker's face. User rejection: *"pip em làm sai, clip được crop thu nhỏ và background màu đen"*

## Correct Recipe (verified V73 18/07/2026)

```bash
# ✅ CORRECT - crop vuông từ giữa source 1080x1920, scale về 420x420 square
ffmpeg -i source.mp4 \
  -ss <start> -t <duration> \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast \
  assets/source/pip_<phase>.mp4
```

**Crop math explained:**
| Step | Value | Effect |
|---|---|---|
| Source | 1080×1920 portrait | Talking head full frame |
| `crop=1080:1080:0:540` | w=1080, h=1080, x=0, y=540 | Crop vuông 1080×1080 bắt đầu Y=540 → bao phủ Y=540-1620 |
| Face position | Y=504-1317 | **NẰM TRỌN** trong khung 1080×1080 crop |
| `scale=420:420` | w=420, h=420 | Resize vuông 420×420 cho PIP |

## Multi-PIP Pattern (verified clip_0003 V73)

For a 81.78s talking-head clip with 3 PIP segments:

```bash
# Phase 4: PIP-CHART (24-37s, 13s duration)
ffmpeg -i source.mp4 -ss 30 -t 13 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast \
  assets/source/pip_chart.mp4

# Phase 5: PIP-USP (37-52s, 15s duration)
ffmpeg -i source.mp4 -ss 40 -t 15 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast \
  assets/source/pip_usp.mp4

# Phase 8: CTA-FINAL (73-82s, 9s duration)
ffmpeg -i source.mp4 -ss 55 -t 9 \
  -vf "crop=1080:1080:0:540,scale=420:420" \
  -an -c:v libx264 -preset fast \
  assets/source/pip_final.mp4
```

## CSS for Square PIP (HyperFrames index.html)

```css
.pip-wrap {
  position: absolute;
  top: 80px;         /* TikTok safe zone: TOP 280 max */
  left: 80px;        /* TikTok safe zone: LEFT 56 */
  width: 420px;
  height: 420px;     /* VUÔNG - KHÔNG 420:750 portrait */
  border-radius: 28px;
  overflow: hidden;
  border: 3px solid rgba(255, 215, 0, 0.8);  /* gold accent border */
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.6);
  z-index: 30;
  opacity: 0;
  clip-path: circle(0% at 50% 50%);  /* mask reveal animation */
}
```

## Glass Card Ngang Hàng Với PIP

Khi có PIP top-left 420×420 ở position (80, 80-500), glass card đặt ở:

```css
/* Chart bar phía phải ngang hàng với PIP */
.glass-chart-right {
  position: absolute;
  top: 720px;          /* Y=80 (PIP top) + 420 (PIP height) + 220 (gap) */
  right: 56px;
  left: 530px;         /* X=80 (PIP left) + 420 (PIP width) + 30 (gap) */
  bottom: 200px;
  padding: 36px 32px;
  /* ... V7.1 liquid glass recipe: opacity 0.18, blur 48px, etc. */
}
```

## MANDATORY PIP Content Verify (anh's rule - NEVER skip)

After rendering, sample pixels in PIP region to verify it's NOT BLACK:

```python
from PIL import Image

img = Image.open('final_frame_at_pip_phase.jpg')
# Sample 9 điểm trong vùng PIP (top-left 420×420 starting at 80,80)
pixels = []
for x in [150, 290, 430]:
    for y in [150, 290, 430]:
        pixels.append(img.getpixel((x, y)))

avg_rgb = tuple(sum(p[i] for p in pixels) // 9 for i in range(3))
print(f"PIP average RGB: {avg_rgb}")

# Decision tree
if avg_rgb[0] < 50 and avg_rgb[1] < 50 and avg_rgb[2] < 50:
    # ❌ BLACK = sai (anh đã reject 18/07 V72)
    print("PIP IS BLACK - re-extract với crop=1080:1080:0:540")
elif avg_rgb[0] > 100 and avg_rgb[1] > 70 and avg_rgb[2] > 60:
    # ✅ Skin tones visible
    print("PIP shows face correctly")
else:
    print(f"PIP mixed content (RGB={avg_rgb}) - manual check needed")
```

## Anti-patterns (TUYỆT ĐỐI KHÔNG)

1. ❌ **`crop=ih*9/16`** trên source đã portrait → kết quả = black background, no face
2. ❌ **PIP size 420×750 portrait** → bị crop thu nhỏ, không phải format TikTok dọc
3. ❌ **Crop từ Y=0** → chỉ lấy background, không có mặt
4. ❌ **Skip PIP content verify** → ship clip PIP đen mà không biết (anh đã bắt lỗi này)

## Why Square 420×420 (không portrait)

- TikTok safe zones: TOP 280 max, LEFT 56, RIGHT 120 → 420×420 fits in safe zones
- Square PIP looks balanced with portrait source (1080×1920)
- Glass card ngang hàng tận dụng được không gian bên phải PIP (left:530 → right:56)
- Face detection: face area Y=504-1317 → vuông 1080×1080 từ Y=540 cover trọn mặt

## Verified Real Case (clip_0003 V73 18/07/2026)

| Field | Value |
|---|---|
| Source | `clip_0003_V3_troncau_may-hut-bui-cam-tay-2in1_speed13.mp4` (1080×1920, 81.78s) |
| Output | `clip0003_V73_82s_FINAL_PIP_FIXED.mp4` (70.7 MB, 81.76s) |
| PIP files | `pip_pip_chart.mp4` (347KB), `pip_pip_usp.mp4` (464KB), `pip_pip_final.mp4` (821KB) |
| Verify PIP content | RGB (96, 98, 87) = skin tones (không đen) ✅ |
| Motion verified | PIP chart d(1-78)=225 ✅, Face chin d(1-28)=160 ✅ |
| Bit rate | 6,774 Kbps (production quality) |

## Cross-references

- SKILL.md § "PIP CROPPING PATTERN FOR TIKTOK VERTICAL" (this file)
- SKILL.md § "8-PHASE BREAKDOWN CHO CLIP 80s+"
- SKILL.md § "WIKI PRODUCT GROUND TRUTH RULE"
- `wiki-product-ground-truth` skill (lấy specs từ wiki)
- `motion-static-video-pitfall.md` (motion failure mode)
