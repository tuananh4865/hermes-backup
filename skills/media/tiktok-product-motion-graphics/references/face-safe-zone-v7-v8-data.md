# Face-Safe Zone — Empirical Data from V7/V8 (17/07/2026)

> Use this reference WHENEVER designing a new layout for tiktok-product-motion-graphics. The safe-zone coordinates below are derived from Vision-framework face detection across the 32s Pocket3 clip. Use them as **starting coordinates**, then re-detect for any new source.

## Empirical face position data (Pocket3 1728×3072 → scaled 1080×1920)

Anh (Tuấn Anh) talking head position was detected using Apple Vision framework at 1-second intervals across the full 32-second clip. Coordinates are CENTER of face bbox, in **pixels of the 1080×1920 scaled output frame**:

| Time | Face center X | Face center Y | Width | Height | Notes |
|------|---------------|----------------|-------|--------|-------|
| 0.0s | 577 | 890 | 508 | 508 | HOOK phase |
| 1.0s | 552 | 911 | 532 | 532 | |
| 2.0s | 395 | 938 | 599 | 599 | Close-up product |
| 3.0s | 439 | 935 | 600 | 600 | |
| 4.0s | 522 | 947 | 607 | 607 | |
| 5.0s | 529 | 909 | 583 | 583 | PROBLEM phase |
| 6.0s | 505 | 952 | 605 | 605 | |
| 7.0s | 547 | 920 | 565 | 565 | CHART phase start |
| 8.0s | 489 | 838 | 522 | 522 | |
| 9.0s | 562 | 928 | 529 | 529 | |
| 10.0s | 503 | 879 | 537 | 537 | |
| 11.0s | 550 | 895 | 516 | 516 | |
| 12.0s | 547 | 823 | 542 | 542 | |
| 13.0s | 555 | 882 | 590 | 590 | STAMP phase |
| 14.0s | 575 | 873 | 529 | 529 | |
| 15.0s | 487 | 949 | 551 | 551 | |
| 16.0s | 508 | 913 | 521 | 521 | PRODUCT phase |
| 18.0s | 562 | 991 | 643 | 643 | Close-up product |
| 19.0s | 484 | 922 | 555 | 555 | PORT phase start |
| 20.0s | 597 | 900 | 550 | 550 | |
| 21.0s | 969 | 1185 | 448 | 448 | Edge position (anh going off frame) |
| 22.0s | 622 | 988 | 586 | 586 | |
| 23.0s | 807 | 1175 | 499 | 499 | |
| 24.0s | 619 | 878 | 530 | 530 | |
| 27.0s | 354 | 953 | 507 | 507 | USP phase |
| 28.0s | 350 | 854 | 458 | 458 | |
| 29.0s | 463 | 911 | 555 | 555 | |
| 30.0s | 587 | 843 | 559 | 559 | CTA phase |
| 32.0s | 354 | 944 | 442 | 442 | End |

## Derived safe zones (1080×1920 output frame)

Based on the above data, the **face-safe text placement zones** are:

### Primary safe zones (text-safe, zero risk of covering face):

| Zone | X range | Y range | Use for |
|------|---------|---------|---------|
| **TOP band** | 0-1080 | **0-580** | HOOK pill, big text, eyebrows, brand pill |
| **LEFT strip** | **0-270** | 0-1920 | Small badges, bullets (when no PIP) |
| **RIGHT strip** | **810-1080** | 0-1920 | Side labels, mini info cards |
| **BOTTOM band** | 60-1020 | **1620-1860** | Caption bar, CTA button, price tag |

### FORBIDDEN zone (face region, never place text here WITHOUT PIP):

| Zone | X range | Y range | Risk |
|------|---------|---------|------|
| **CENTER zone** | 270-810 | **580-1320** | **100% overlap with face** (face is always Y=823-913 ± 50px) |

### Verification rule:

For ANY new layout decision, ask: "Would this card element have any pixel inside X=[270, 810] AND Y=[580, 1320]?"

- **YES** → Either (a) move the card, (b) add a PIP that crops the face to a different position, or (c) crop the source video so face is shifted away from that zone.
- **NO** → Safe to render.

## Face bbox to ffmpeg crop conversion

When PIP-cropping for chart-heavy phases, use the **AVG bbox across the target phase** with 30-40% padding:

```python
# CHART phase 7.3-13.3s — face bbox samples at 8s, 10s, 12s
# 8s:  center (489,838)  size 522×522  → bbox top-left (228, 577)  → 522×522
# 10s: center (503,879)  size 537×537  → bbox top-left (235, 611)  → 537×537
# 12s: center (547,823)  size 542×542  → bbox top-left (276, 552)  → 542×542
#
# AVG top-left: (246, 580)  AVG size: 534×534
# With 40% padding: size = 748, expand from center

import json
samples_chart = [(489,838,522), (503,879,537), (547,823,542)]
xs = [c[0] - c[2]//2 for c in samples_chart]  # left edges
ys = [c[1] - c[2]//2 for c in samples_chart]
ws = [c[2] for c in samples_chart]
hs = [c[3] for c in samples_chart]

# Average, then expand 40%
avg_x = sum(xs) // len(xs)
avg_y = sum(ys) // len(ys)
crop_w = max(ws)
crop_h = max(hs)
pad_w = int(crop_w * 0.4)
pad_h = int(crop_h * 0.4)
final_w = crop_w + 2 * pad_w
final_h = crop_h + 2 * pad_h
final_x = max(0, avg_x - pad_w)
final_y = max(0, avg_y - pad_h)
# Re-center if clamped
if final_x + final_w > 1080:
    final_x = max(0, 1080 - final_w)
if final_y + final_h > 1920:
    final_y = max(0, 1920 - final_h)
```

## Generalization to other Pocket3 clips

These exact coordinates are for **one specific clip**. For another clip:

1. **Detect face every 1 second** using the `detect_face.swift` script (see `scripts/detect_face.swift`)
2. **Compute AVG center** across the full duration (or per-phase AVG if you want phase-accurate crops)
3. **Apply 30-40% padding** based on subject movement (more movement = more padding)
4. **Verify with `vision_analyze`** that the cropped face fills the PIP without looking too small (< 30% of PIP area)
5. **Document the data** in this file if the clip is a recurring product template (e.g., Gochodoc charging products)

## Reference: detect_face.swift pipeline

```bash
# Compile once
swiftc scripts/detect_face.swift -o detect_face

# Run on frame
./detect_face frame.jpg
# Output: FACE <x> <y> <w> <h>  (normalized 0-1, Vision BOTTOM-LEFT origin)

# Convert to pixel coords in 1080x1920 frame:
# px = x * 1080 (X from left)
# py = (1 - y - h) * 1920 (Y from top, flip Vision's bottom-left origin)
# pw = w * 1080
# ph = h * 1920
```

Full convert script: see `scripts/detect_face.swift` + the verification script in this skill's case 4.
