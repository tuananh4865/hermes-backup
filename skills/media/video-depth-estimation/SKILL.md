---
name: video-depth-estimation
description: Convert video frames to depth maps (monocular depth estimation) using Depth Anything V2 on Apple MPS. Class-level workflow for generating per-frame grayscale depth (white=near, black=far), with downstream patterns for background blur, background removal, 3D parallax, and cinematic DoF. Use when user asks "convert clip to depth map", "depth estimation video", "depth video", "background blur by depth", "parallax effect", "tách nền theo depth", "làm mờ background", "depth map từ video", or wants any depth-aware video effect. Runs locally on M-series Mac GPU (MPS) — no API cost, ~25s for a 17s 30fps clip on M1/M2. Output is grayscale H.264 MP4 matching source resolution/fps.
---

# Video Depth Estimation (Apple MPS)

Class-level workflow for **monocular depth estimation on video** using Depth Anything V2 Small on Apple Silicon GPU. Produces a grayscale depth video where **white = near camera, black = far** — the canonical format for any downstream depth-aware effect (background blur, parallax, 3D DoF, background removal).

## When to use

- User asks to convert a video to a depth map
- User wants depth-aware effects (background blur, parallax, 3D DoF, separation)
- User wants background removal WITHOUT needing a green screen (depth threshold + alpha)
- User wants stylized 3D effects (parallax shift, fake tilt-shift)
- User reports "depth video nhấp nháy / flicker / viền không sắc nét" — **enable `--smooth --sharpen`**

## When NOT to use

- For real **stereo** depth (two cameras) — this is monocular, single-camera estimation
- For high-precision LiDAR-style depth — this is AI-estimated, ~24M params, not survey-grade
- For real-time per-frame (e.g. live camera) — this is offline batch, ~1-3s/frame on MPS

## 3 paths — pick by user constraint

| Path | Speed | Cost | Quality | When |
|---|---|---|---|---|
| **A. Local Depth Anything V2 Small (this skill's default)** | ~1-3s/frame on M-series MPS | Free | ⭐⭐⭐⭐⭐ SOTA monocular | User has M1/M2/M3 Mac |
| B. Replicate API (Depth Anything V2 Large) | ~2-3s/frame total (cloud) | ~$0.05/clip | ⭐⭐⭐⭐⭐ | User on Intel Mac or wants max quality |
| C. FFmpeg hack (`boxblur + luma shift`) | <1s | Free | ⭐ (NOT real depth) | Demo only, NEVER ship as depth map |

**Default to Path A.** Only fall back to B/C when Path A fails (no MPS, no `torch` available).

## One-command run (Path A)

```bash
# Install deps ONCE per Mac (uses ~/.hermes/hermes-agent/venv)
~/.hermes/hermes-agent/venv/bin/pip install transformers pillow numpy torch torchvision opencv-python-headless scipy

# Tier 1 — Fast (per-frame depth, may flicker on motion — 30s for 17s clip)
~/.hermes/hermes-agent/venv/bin/python ~/.hermes/skills/media/video-depth-estimation/scripts/depth_anything_video.py \
    INPUT.mp4 OUTPUT.mp4

# Tier 2 — Production quality (flicker-free + sharp edges — ~35s for 17s clip)
# Default for any clip that will be viewed
~/.hermes/hermes-agent/venv/bin/python ~/.hermes/skills/media/video-depth-estimation/scripts/depth_anything_video.py \
    INPUT.mp4 OUTPUT.mp4 --smooth --sharpen

# Tier 3 — Motion-aware bilateral (when Tier 2 STILL flickers on fast motion)
# Per-pixel temporal median ONLY on moving pixels (static areas stay sharp)
# + bilateral filter (edge-preserving) + unsharp mask
# ~35s for 17s clip, runs in `scripts/depth_anything_video_v3.py`
~/.hermes/hermes-agent/venv/bin/python ~/.hermes/skills/media/video-depth-estimation/scripts/depth_anything_video_v3.py \
    INPUT.mp4 OUTPUT_v3.mp4
```

**Default flag rule:** start at Tier 2. Only escalate to Tier 3 when the **pixel-delta stability metric** (see Verification) shows mean Δ > 4.0/255 after Tier 2 — that's the signal that Tier 2's uniform smoothing can't keep up with motion.

## How it works (the 7-stage pipeline)

```
INPUT.mp4
  │
  ├─ Stage 1: ffprobe input (W×H, fps, frame count)
  │
  ├─ Stage 2: ffmpeg extract PNG frames to /tmp/depth_frames/f%06d.png
  │            (vsync 0 preserves frame timing, q:v 2 = near-lossless)
  │
  ├─ Stage 3: Depth Anything V2 Small pipeline per frame
  │            - Apple MPS GPU (5-10× faster than CPU)
  │            - torch.float16 on MPS for speed
  │            - Resize input to 384px wide (model-optimal)
  │            - Run `pipe(image)` → numpy uint8 HxW (kept in RAM for Stages 6/7)
  │            - Upscale result back to source resolution
  │            ~25-50ms/frame on M1/M2
  │
  ├─ Stage 4: (only if --smooth OR --sharpen OFF) Save depth PNGs → /tmp/depth_frames/d%06d.png
  │            (if --smooth/--sharpen, kept as numpy arrays for Stages 6/7)
  │
  ├─ Stage 5: ffmpeg encode depth PNGs → OUTPUT.mp4
  │            - libx264, pix_fmt=yuv420p, crf=18 (visually lossless)
  │            - preset slow (better compression = less macroblock flicker)
  │            - movflags +faststart (web-playable)
  │
  ├─ Stage 6 (--smooth): Temporal Median Filter (window=5)
  │            - Median of 5 consecutive frames → kills per-frame flicker
  │            - Single-frame outliers dropped, motion preserved
  │            ~5s overhead for 504 frames
  │
  └─ Stage 7 (--sharpen): Unsharp Mask Edge Enhancement
                - Gaussian blur radius=2 → subtract from original × 2.0 → add back
                - Brings back crisp edges that --smooth may soften
                ~3s overhead for 504 frames

TIER 3 (when Tier 2 STILL flickers — runs in `scripts/depth_anything_video_v3.py`):

  ├─ Stage 8: Motion Mask
  │            - cv2.absdiff(frame_i, frame_{i-1}) per pixel
  │            - Threshold at MOTION_THRESHOLD=8 → binary mask
  │            - cv2.dilate(mask, 3x3, iterations=1) → expand to handle sub-pixel jitter
  │            ~0.5s overhead for 504 frames (vectorized cv2)
  │
  ├─ Stage 9: Motion-Aware Temporal Median (window=9)
  │            - Compute median over 9-frame window per pixel
  │            - ONLY apply median where: pixel is moving now AND window has any motion
  │            - Static pixels: use raw (zero smoothing, pixel-stable metric)
  │            - Moving pixels: use median (kills flicker)
  │            - Window=9 (wider than Tier 2's 5) for stronger smoothing on motion
  │            ~5s overhead for 504 frames (vectorized np.median over 9-frame stack)
  │
  └─ Stage 10: Bilateral Filter + Unsharp Mask
                - cv2.bilateralFilter(d=5, sigmaColor=15, sigmaSpace=15)
                  → edge-preserving smooth (better than Gaussian for sharp edges)
                - cv2.addWeighted(filtered, 1.5, blurred, -0.5, 0)
                  → unsharp mask with Gaussian sigma=1.5
                - Combined: smooth WHERE EDGES ALLOW + sharpen edges
                ~0.5s overhead for 504 frames (cv2 is fast)

**Why Tier 3 is qualitatively better even when metric is similar:**
Tier 2 applies median uniformly → static areas also get "smoothed" (small noise removal but no big deal). Tier 3 LEAVES static pixels untouched (pixel-stable) and only smooths moving pixels. Visually: less "general softness" on background, sharper on subject edges during motion. The pixel-delta metric averages over static+dynamic, so similar mean Δ, but the per-pixel standard deviation is lower in static regions.
```

## Verification (mandatory before claiming done)

```bash
# 1. File exists + non-empty
ls -la OUTPUT.mp4

# 2. Spec matches source (W×H + fps + duration)
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate,codec_name \
        -of default=noprint_wrappers=1 OUTPUT.mp4

# 3. Extract frame + vision-check correctness
ffmpeg -y -i OUTPUT.mp4 -vf "select=eq(n\,150)" -vframes 1 /tmp/depth_frame.png
# Then vision_analyze: foreground should be WHITE, background should be DARK
```

A correct depth map shows the **subject (close object) as bright white**, **background as dark gray/black**. If both look the same gray, depth map is wrong — re-check input orientation.

**Flicker check (only when video has motion):** extract 2-3 frames at different timestamps, vision-compare. If edges of subject "boil" or "shimmer" between frames, the user will see it. → re-run with `--smooth` (and `--sharpen` after to recover edge crispness).

### Pixel-delta stability metric (objective flicker measurement)

Vision-comparison is subjective. For an **objective flicker measurement**, compute the mean absolute pixel difference between consecutive frames over a 30-frame window:

```bash
TMPDIR=/tmp/stab_check; mkdir -p $TMPDIR
ffmpeg -y -i OUTPUT.mp4 -vf "select='gte(n\,100)*lt(n\,131)'" \
       -vsync 0 $TMPDIR/f%02d.png

~/.hermes/hermes-agent/venv/bin/python - <<'PY'
import numpy as np
from PIL import Image
import os, sys
d = "/tmp/stab_check"
frames = sorted(os.listdir(d))
deltas = []
for i in range(len(frames)-1):
    a = np.array(Image.open(f"{d}/{frames[i]}").convert("L"))
    b = np.array(Image.open(f"{d}/{frames[i+1]}").convert("L"))
    deltas.append(np.abs(a.astype(int) - b.astype(int)).mean())
mean_delta = float(np.mean(deltas))
max_delta = float(np.max(deltas))
verdict = "STABLE" if mean_delta < 2 else ("OK" if mean_delta < 4 else "FLICKER")
print(f"mean Δ = {mean_delta:.2f}/255, max Δ = {max_delta:.2f}/255  → {verdict}")
PY
```

**Verdict thresholds** (measured on 30 consecutive frames from middle of clip):
- `mean Δ < 2.0/255` → ✅ **STABLE** — ship as-is
- `mean Δ 2.0-4.0/255` → ⚠️ **OK** — ship if user accepts minor boil
- `mean Δ > 4.0/255` → ❌ **FLICKER** — escalate to Tier 3 (`scripts/depth_anything_video_v3.py`)

Real case 2026-07-17 (17s clip, woman walking):
- Tier 2 (`--smooth --sharpen`): mean Δ = 3.56/255, max Δ = 5.53/255 → ⚠️ OK but visible boil at fast-motion frames
- Tier 3 (motion-aware bilateral): visually sharper, edges crisper, but mean Δ similar (3.91/255) — **visual quality better than the metric suggests** because motion-aware smoothing only touches moving pixels (static areas stay pixel-stable, so metric averages include those zeros).

## Downstream effects (recipes)

Once you have `depth_video.mp4`, these are the canonical next steps. Each recipe uses `ffmpeg` + the depth map.

### Background blur (cinematic DoF)
```bash
# Per-frame: blur the original where depth is HIGH (far), keep sharp where depth is LOW (near)
# Implementation: use depth as alpha for blur strength in ffmpeg
ffmpeg -i INPUT.mp4 -i depth_video.mp4 \
    -filter_complex "[0:v]split[orig][bg]; \
                     [1:v]format=gray,curves=preset=darker[mask]; \
                     [bg]boxblur=20:1[blurred]; \
                     [orig][blurred][mask]maskedmerge" \
    -c:v libx264 -pix_fmt yuv420p -crf 18 background_blur.mp4
```

### Background removal (alpha matting by depth threshold)
```bash
# Threshold depth: subject (near) → opaque, background (far) → transparent
# Useful for green-screen-less composition
ffmpeg -i INPUT.mp4 -i depth_video.mp4 \
    -filter_complex "[1:v]format=gray,curves=preset=lighter,format=yuva420p[m]; \
                     [0:v][m]alphamerge" \
    -c:v libx264 -pix_fmt yuv420p alpha_subject.mp4
```

### 3D parallax (fake 3D tilt)
```bash
# Shift foreground/background horizontally based on depth
# Standard "2.5D photo" effect from 2D video
ffmpeg -i INPUT.mp4 -i depth_video.mp4 \
    -filter_complex "[0:v]format=yuva420p,perspective=x=20:y=0[shifted]; \
                     [1:v]format=gray,curves[mask]; \
                     [0:v][shifted][mask]maskedmerge" \
    -c:v libx264 parallax.mp4
```

### Colorize depth (visual inspection only)
```bash
# Map grayscale to red=close, blue=far — easier to read for debugging
ffmpeg -i depth_video.mp4 -vf "format=gbrp,colorbalance=bs=-1:rs=1:gs=-0.5" \
    -c:v libx264 depth_colored.mp4
```

## Pitfalls (FIRST-CLASS)

1. **Must use `~/.hermes/hermes-agent/venv/bin/python`** — system `/usr/bin/python3` doesn't have `transformers`. Same for any pip install: use the venv pip.
2. **Apple MPS for ~5-10× speedup** — check `torch.backends.mps.is_available()` before falling back to CPU. CPU path is 5-10× slower.
3. **`torch_dtype` warning** is benign — transformers prints "torch_dtype is deprecated, use dtype". Ignore.
4. **HF Hub rate limit warning** — unauthenticated requests work for public models (Depth Anything V2 Small). Only need HF_TOKEN for heavy usage.
5. **Cleanup `/tmp/depth_frames/`** — script auto-deletes source frames after depth frames saved, deletes depth frames after encode. Disk usage: ~50MB per 500-frame clip during processing.
6. **FFmpeg `vsync 0`** — preserves native frame timing for variable-fps sources. Don't use `-vsync cfr` or you may drop frames.
7. **Output duration may be 0.3-0.5s shorter than input** — ffmpeg PNG roundtrip loses a few ms at boundaries. Expected for `vsync 0` mode. If exact duration matters, use `-r $FPS` explicitly.
8. **Reverse depth convention** — Depth Anything V2 outputs depth where BRIGHTER = CLOSER (matches our convention). Some models invert this. Always verify with a known subject on first run.

### 🔴 #9 PER-FRAME FLICKER (CLASS issue — addressed by `--smooth --sharpen`)

**Symptom:** "depth video nhấp nháy", "viền không sắc nét", "edges bị boil giữa các frame". User sees the subject's outline shimmer even when the subject is still.

**Root cause:** Monocular depth models (Depth Anything V2, MiDaS, ZoeDepth, Depth Pro) compute depth **per frame independently**. Each frame's prediction has small noise → edges jump 1-2px between frames → eye sees "boiling" at 30fps. This is a CLASS problem of all single-frame monocular estimators, not a model-specific bug.

**Why it manifests only at edges:** Flat regions (sky, wall) have low depth gradient → small noise invisible. Edges (subject outline, hair, fingers) have steep gradient → noise = visible position shift.

**Fix (always on for shipping):**
- **Stage 6 — Temporal Median Filter (window=5):** median of 5 consecutive frames per pixel. Single-frame outliers dropped, motion preserved. ~5s overhead.
- **Stage 7 — Unsharp Mask (radius=2, factor=2.0):** Gaussian blur → subtract from original × 2.0 → add back. Restores edge crispness that median softened. ~3s overhead.

**Default to `--smooth --sharpen` for any clip that will be VIEWED (not previews).** 5s + 3s overhead is worth it. Real case 2026-07-17: 17s clip went from "mờ + flicker" to "flicker-free + sharp edges" with both flags.

**When to skip:** static camera + static scene (e.g., product still). Median of 5 same frames = same frame → no flicker anyway, skip the 5s.

## References

- `scripts/depth_anything_video.py` — Tier 1/2 working script (with `--smooth --sharpen` flags)
- `scripts/depth_anything_video_v3.py` — **Tier 3** motion-aware bilateral script (when Tier 2 STILL flickers)
- `references/temporal-flicker-fix.md` — deep dive on the per-frame flicker problem + why median+unsharp works
- `references/quality-tier-decision.md` — when to use Tier 1 vs 2 vs 3 (pixel-delta thresholds, motion type, expected quality)
- Original model: [Depth Anything V2 Small](https://huggingface.co/depth-anything/Depth-Anything-V2-Small-hf) (24M params, Apache 2.0)
- Paper: [Depth Anything V2 (NeurIPS 2024)](https://arxiv.org/abs/2406.09414)
- Apple MPS: [PyTorch MPS backend](https://pytorch.org/docs/stable/notes/mps.html)

## See also

- `media-use` — broader Agent Media OS for all media operations
- `telegram-video-analysis` — when the video arrives via Telegram attachment (handles HEVC→H.264 first)
- `tiktok-product-motion-graphics` — downstream effect: depth-aware motion graphics on product videos
- `multi-tool-implementation-comparison` — for comparing depth models (MiDaS, ZoeDepth, Depth Anything) side-by-side