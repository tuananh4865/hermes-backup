# Temporal Flicker Fix for Per-Frame Monocular Depth Estimation

**Lesson captured:** 2026-07-17 (real case: 17s clip of woman walking, Depth Anything V2 Small on M-series Mac)

**Anh's verbatim complaint:** *"Anh thấy các viền và chi tiết hay bị nhấp nháy và thiếu sắc nét"*

## The problem in detail

Monocular depth estimators (Depth Anything V2, MiDaS, ZoeDepth, Depth Pro) all have the same architecture: encoder → decoder → per-frame depth map. The depth map is computed **independently for each frame** — there is no temporal modeling.

This causes:

1. **Per-frame noise** — Each frame's prediction has small (1-2px) pixel-level noise. At 30fps, the eye sees this as a "boil" at edges.
2. **Edge shimmer** — Flat regions (sky, walls) are robust because depth gradient is ~0 → noise invisible. Edges (subject outline, hair, fingers) have steep gradient → noise = visible position shift = "edges boil".
3. **Static scene, still flickers** — Even when the camera AND subject don't move, edges still flicker because the model has stochastic per-frame variation.

## Why it's a class issue, not a model bug

All current monocular depth estimators share this property:
- Depth Anything V1/V2 (Yang et al., 2024)
- MiDaS (Ranftl et al., 2022)
- ZoeDepth (Bhat et al., 2023)
- Depth Pro (Bochkovskii et al., 2024)

The only way to truly fix this at the model level would be **video-depth** models (e.g., NVDS, Consistent Video Depth Estimation) that explicitly model temporal coherence. These are 10-50× larger and slower.

For the small/fast models we run on MPS, the workaround is post-hoc temporal filtering.

## The fix: Temporal Median Filter (Stage 6)

Median of 5 consecutive frames per pixel:

```python
for i in range(len(raw_depths)):
    lo = max(0, i - 2)
    hi = min(len(raw_depths), i + 3)
    window = np.stack(raw_depths[lo:hi], axis=0)  # TxHxW
    median = np.median(window, axis=0).astype(np.uint8)
    smoothed.append(median)
```

**Why median instead of mean?** Mean smooths edges (blurs the subject outline). Median keeps edges sharp because it picks the actual value that appears in 3 of 5 frames, not the average.

**Why window=5?** Odd number (median has a center). Window too small (3) → not enough averaging for noise. Too large (7-9) → motion blur when subject moves fast. 5 = sweet spot for typical 30fps talking-head / walking clips.

**Cost:** ~5s overhead for 500 frames. Negligible vs 23s depth inference.

## The edge recovery: Unsharp Mask (Stage 7)

Temporal median softens edges slightly (because neighboring frames contribute). Unsharp mask brings back crispness:

```python
img = Image.fromarray(arr, mode="L")
blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
arr_orig = np.array(img, dtype=np.int16)
arr_blur = np.array(blurred, dtype=np.int16)
mask = (arr_orig - arr_blur) * 2.0  # factor=2.0
arr_sharp = np.clip(arr_orig + mask, 0, 255).astype(np.uint8)
```

**Why radius=2, factor=2.0?**
- radius=2 = blur kernel of 4px → captures edge width typical in subject outlines
- factor=2.0 = double the high-frequency component → noticeable sharpening without ringing artifacts
- factor>3.0 → ringing (white halos around dark edges, dark halos around bright edges)

**Cost:** ~3s overhead for 500 frames.

## Verification: how to know it worked

Extract 2-3 frames at different timestamps and vision-compare:

```bash
ffmpeg -y -i OUTPUT.mp4 -vf "select=eq(n\,50)" -vframes 1 /tmp/frame50.png
ffmpeg -y -i OUTPUT.mp4 -vf "select=eq(n\,250)" -vframes 1 /tmp/frame250.png
```

Then vision_analyze: "Subject outline should be at the SAME pixel position in both frames (no boil). Edges should be sharp, not soft."

## When to apply

| Scenario | Recommend flags |
|---|---|
| Static camera + static scene (product still, landscape) | No flags (no motion → no flicker) |
| Talking head (mostly static subject, slight motion) | `--smooth` only |
| Walking / dancing / fast motion | `--smooth --sharpen` (default for shipping) |
| Long clip (>1 min) where every 5s matters | Skip --smooth, use video-depth model instead |
| Preview / sanity check (want fast iteration) | No flags |

## Real case 2026-07-17

**Setup:** 17s clip @ 30fps = 504 frames, woman walking in front of building. M-series Mac, MPS GPU.

**Without flags (30s):**
- Subject outline "boils" between frames — visible shimmer
- Edges soft, depth transitions gradual
- 2.0 MB output

**With `--smooth --sharpen` (35s):**
- No flicker on subject outline across all 504 frames
- Edges crisp with visible halo at subject/background boundary
- 2.5 MB output (+25%, acceptable)

**5s overhead worth it** — anh verified by visual comparison and accepted.

## Future: alternative approaches

If `--smooth --sharpen` doesn't suffice (e.g., very fast motion with motion blur), consider:

1. **Bilateral filter across frames** (preserves edges better than median) — slower, ~3x
2. **Optical flow guided smoothing** — shift previous frames by motion vectors before median — best quality, complex impl
3. **Video depth models** — NVDS, Consistent Video Depth, DepthCrafter — 10-50x slower, larger models
4. **Sliding window with weighted median** — weight center frame higher → preserves motion better

For Anh's current use case (product clips, talking heads), `--smooth --sharpen` is the sweet spot.