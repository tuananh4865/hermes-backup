---
name: watermark-remover
title: Remove static and floating watermarks with OpenCV inpaint
description: Remove watermarks from video clips (static OR floating). Use OpenCV cv2.inpaint for best quality, ffmpeg delogo for fast static removal.
version: 0.2.0
author: Hermes
platforms: [macos, linux]
metadata:
  hermes:
    Tags: [Video, Watermark, OpenCV, Inpaint, Media, Tracking]
---

# Watermark Remover — Hermes Skill

Remove watermarks from video clips. Two modes: **static** (logo at fixed position, single inpaint per frame) and **floating** (logo moves between positions, template matching + per-frame tracking). Static logos are far more common when user says "xoá logo X" — use static mode by default.

**Quality hierarchy:** OpenCV inpaint (Telea) > OpenCV inpaint (NS) > ffmpeg `delogo` (blur-only, leaves visible vertical smear — almost always wrong).

**VERIFIED 25/07:** Anh rejected delogo blur because "để lại vệt vertical rõ rệt trong vùng logo". When user pushes back on logo removal quality → switch to inpaint, do NOT defend delogo.

**Use when:** user says "xoá watermark", "xóa logo", "remove watermark", "logo SB" etc.

**Decision tree:**
1. Sample 9 frames evenly with `vision_analyze`. Does the logo stay at the same `(x, y)` in all 9 frames? → **Static mode** (skip to that section).
2. Logo position changes between frames? → **Floating mode** (template matching + tracking).
3. Single frame has issues? → both modes can handle per-frame inpainting.

## How to choose the variant

| Variant | When | Cost |
|---|---|---|
| **Static logo** (single position) | Logo at one fixed corner/region every frame | ~90s for 28s @60fps clip |
| **Floating watermark** (multi-position) | Logo jumps between N distinct positions | ~120s + ~(N templates × 5s) |

Sample 9 frames evenly with `ffmpeg -ss <t> -vframes 1` and use `vision_analyze` to determine which variant fits. If watermark position changes between sample frames → floating (multi-template). If watermark stays at same position → static (single template covers it).

## Prerequisites

- Python 3.11+ with `cv2`, `numpy`
- `ffmpeg`, `ffprobe` on PATH
- Read+write on source video path
- Read+write on output destination

### Python interpreter (CRITICAL)

Hermes venv (`/Users/tuananh4865/.hermes/hermes-agent/venv/bin/python3`) HAS `cv2` 5.0 installed — use it for `execute_code` blocks. But if running standalone script, `/opt/homebrew/bin/python3` 3.11+ also has `cv2` 4.13.

NEVER use `/usr/bin/python3` (system python) — no `cv2` installed, will fail with `ModuleNotFoundError`.

Quick test before running inpaint script:
```bash
python3 -c "import cv2, numpy; print('cv2:', cv2.__version__)"
# Must print version, not error
```

If cv2 missing, install: `pip3 install opencv-python-headless numpy` (headless = no GUI deps, ~30MB).

## Quick Reference

- **Detect FPS first** — `ffprobe -select_streams v:0 -show_entries stream=avg_frame_rate`
- **Extract frames:** `ffmpeg -i <src> -vsync 0 <tmp>/frame_%05d.png` (NO `-r` flag, see pitfall)
- **Template build:** crop watermark ROI + 10px padding each side
- **Match threshold:** TM_CCOEFF_NORMED, `conf > 0.4` minimum
- **Inpaint mask:** `|gray - bg_median| > max(15, 2*bg_std)` OR `brightness in 80-230` → OR both → dilate `5x5 + 2 iterations`
- **Inpaint radius:** `7` (Telea) — works for both static logos and floating watermarks
- **Re-encode:** `ffmpeg -framerate <FPS> -i <out>/frame_%05d.png -i <src> -map 0:v -map 1:a -c:v libx264 -preset fast -crf 23`

## Procedure

### Step 1: Detect FPS and duration

```python
fps_str = subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0",
     "-show_entries", "stream=avg_frame_rate",
     "-of", "default=nw=1:nk=1", VIDEO],
    capture_output=True, text=True
).stdout.strip()
FPS = float(fps_str.split('/')[0]) / float(fps_str.split('/')[1])
# Common: 30/1 = 30, 60/1 = 60
```

**Why this matters:** hardcoded `FPS=30` on 60fps clip → re-encode doubles duration to 57.4s. Hardcoded `FPS=60` on 30fps clip → halves duration. ALWAYS detect.

### Step 2: Sample 9 frames + vision_analyze

```bash
for t in 0.5 2 4 6 8 10 12 14 16; do
  ffmpeg -y -ss $t -i <source.mp4> -vframes 1 -update 1 /tmp/sample_$t.png
done
```

Use `vision_analyze` on each to find all distinct watermark positions and bounding boxes `(x_min, y_min, x_max, y_max)`. If watermark stays in same corner → static. If jumps between positions → floating.

### Step 3: Extract all frames

```bash
ffmpeg -y -i <source.mp4> -vsync 0 <tmp_dir>/frame_%05d.png
```

⚠️ **DO NOT add `-r 60` or any framerate override** — ffmpeg rejects with "non-CFR -vsync/-fps_mode contradictory". Just `-vsync 0` is enough (passes through source FPS).

### Step 4: Build templates (static = 1, floating = N)

```python
import cv2
img = cv2.imread(f"<tmp_dir>/frame_<N>.png")
tmpl = img[y_min-10:y_max+10, x_min-10:x_max+10]  # +10px padding each side
tmpl_gray = cv2.cvtColor(tmpl, cv2.COLOR_BGR2GRAY)
```

Padding 10px that covers shadow halo around text.

### Step 5: Detect watermark (static OR floating)

**Static (one template covers all frames):**
```python
LOGO_X, LOGO_Y = 22, 531
LOGO_W, LOGO_H = 113, 132
PAD = 10
x1, y1 = max(0, LOGO_X - PAD), max(0, LOGO_Y - PAD)
x2, y2 = LOGO_X + LOGO_W + PAD, LOGO_Y + LOGO_H + PAD
# Skip tracking — apply same ROI every frame
```

**Floating (templates compete per frame):**
```python
for i in range(total):
    frame = cv2.imread(f"frame_{i:05d}.png", cv2.IMREAD_GRAYSCALE)
    best = (-1, 0, 0, 0.0, None)
    for tmpl_gray, tmpl_shape, label in templates:
        result = cv2.matchTemplate(frame, tmpl_gray, cv2.TM_CCOEFF_NORMED)
        _, conf, _, loc = cv2.minMaxLoc(result)
        if conf > best[3] and conf > 0.4:
            best = (i, loc[0], loc[1], conf, label)
    if best[3] > 0.4:
        tracking.append((best[0], best[1], best[2], tmpl_w, tmpl_h))
```

### Step 6: Inpaint ROI per frame

```python
for i in range(total):
    frame = cv2.imread(f"frame_{i:05d}.png")
    if frame is None:
        continue

    # Static: same ROI every frame
    # Floating: (x, y, w, h) from tracking
    x, y, w, h = x1, y1, x2-x1, y2-y1

    roi = frame[y:y+h, x:x+w].copy()
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Background sample from outer edges (PAD wide strip)
    edges = np.concatenate([
        gray_roi[:PAD, :].flatten(),
        gray_roi[-PAD:, :].flatten(),
        gray_roi[:, :PAD].flatten(),
        gray_roi[:, -PAD:].flatten()
    ])
    bg = np.median(edges)
    bg_std = np.std(edges)

    # Mask: pixels DIFFER from background + bright pixels (logo text/icon)
    mask = (np.abs(gray_roi.astype(float) - bg) > max(15, bg_std * 2)).astype(np.uint8) * 255
    bright_mask = ((gray_roi > 80) & (gray_roi < 230)).astype(np.uint8) * 255
    mask = cv2.bitwise_or(mask, bright_mask)

    # Dilate to cover shadow
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Inpaint Telea with radius 7
    inpainted = cv2.inpaint(roi, mask, 7, cv2.INPAINT_TELEA)
    frame[y:y+h, x:x+w] = inpainted

    cv2.imwrite(f"<out_dir>/frame_{i:05d}.png", frame)
```

### Step 7: Re-encode with original audio

```bash
ffmpeg -y -framerate <FPS> -i <out_dir>/frame_%05d.png -i <source.mp4> \
  -map 0:v -map 1:a \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -pix_fmt yuv420p -movflags +faststart \
  <clean_output.mp4>
```

### Step 8: Verify

```bash
# Spec
ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,sample_rate \
  -show_entries format=duration,size -of default=nw=1 <output.mp4>
# Vision: extract 3-5 sample frames, vision_analyze each
```

**PASS criteria:** H.264 + AAC 44100Hz STEREO + original resolution + duration within 50ms of source. `vision_analyze` confirms no watermark text visible.

## Pitfalls

### ffmpeg & extraction

- **Never use `-r <FPS> + -vsync 0` together.** ffmpeg rejects with: "One of -r/-fpsmax was specified together a non-CFR -vsync/-fps_mode. This is contradictory." → use only `-vsync 0` (passes through source FPS).
- **Always detect FPS from ffprobe** — hardcoded `FPS=30` on 60fps clip doubles duration (verified 24/07: clip 28.82s output as 57.4s).
- **Chain 2 `delogo` filters fails** — "Logo area is outside of the frame". Workaround: use inpaint (this skill) instead, or chain `delogo` + `drawbox` (mix methods).

### Inpaint quality

- **Inpaint radius too small (< 5) leaves artifacts.** Radius 7 works for both static logos and floating watermarks.
- **Mask too narrow:** watermark has shadow halo ~5-10px around text. Dilate `5x5 + 2 iterations` minimum.
- **Template too small (no padding):** watermark tails bleed. Always add 10px padding each side.
- **Brightness-only mask misses shadow:** use `|gray - bg_median| > max(15, 2*bg_std)` PLUS brightness 80-230, OR both.

### Tracking (floating only)

- **Threshold too high (>0.5) skips frames** — drop to `conf > 0.4` for partial alpha variations.
- **Templates compete correctly:** pick higher-confidence match per frame, not rounded distance.
- **>30% frames skipped** → your template doesn't match watermark at those frames. May need to rebuild from a different sample frame.

### Verification

- **Vision can hallucinate:** vision model may report "watermark still visible" when only inpaint blur remains. Always cross-check with `crop + scale 2x` + pixel diff.
- **Pixel diff alone insufficient:** subtle inpaint artifacts may pass diff but fail visually. Always include `vision_analyze` step.

## Verification

```bash
# Spec
ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,sample_rate \
  -show_entries format=duration,size -of default=nw=1 <output.mp4>

# Vision (sample 3-5 timestamps)
for t in 2 8 14 22 28; do
  ffmpeg -y -ss $t -i <output.mp4> -vf "crop=200:200:0:520,scale=400:400:flags=neighbor" \
    -vframes 1 -update 1 /tmp/check_${t}.png
done
# Then vision_analyze each /tmp/check_${t}.png
```

**PASS criteria:** ffprobe shows H.264 + AAC 44100Hz STEREO + 1080×1920 (or source res) + duration within 50ms of source. `vision_analyze` on 3+ sample timestamps confirms no watermark text visible.

## Reference

- **24/07 real use case (static):** clip `lGZQgDMMMac_iphone.mp4` (28.82s, 60fps, 1724 frames) — static logo "SB SMASHBERT" at top-left (x=22-135, y=531-663, size 113x132). Single inpaint per-frame → clean output. Final: `/Volumes/Storage-1/Tiktok-Tuan-Anh/lGZQgDMMMac_no_wm_v2.mp4` (3.80 MB).
- **24/07 real use case (floating):** clip `17si3J8buy_iphone.mp4` (16.39s, 30fps, 490 frames) — watermark "CẨU LỒN VBL" jumping between 2 positions: bottom-left and top-right. Templates tracked 489/490 frames. Needs further iteration on mask dilate params for visual edge quality.
- **Verified scripts:** `~/.hermes/skills/media/floating-watermark-remover/scripts/static_logo_inpaint.py` (static, verified work), `~/.hermes/skills/media/floating-watermark-remover/scripts/floating_watermark_tracker.py` (floating, workflow verified).
- **Concept page:** `/Volumes/Storage-1/Hermes/wiki/concepts/video-watermark-removal-2026-07-25.md`
