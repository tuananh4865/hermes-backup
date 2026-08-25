#!/usr/bin/env python3
"""
Floating watermark tracker v6: full ROI inpaint with background-comparison mask.
Verified workflow for watermark that moves between N distinct positions.

Run: /opt/homebrew/bin/python3 floating_watermark_tracker.py
Requires: cv2, numpy installed
"""
import cv2
import numpy as np
import subprocess
import os
import sys

# ========== CONFIG ==========
VIDEO = sys.argv[1] if len(sys.argv) > 1 else "/Volumes/Storage-1/Tiktok-Tuan-Anh/17si3J8buy_iphone.mp4"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/Volumes/Storage-1/Tiktok-Tuan-Anh/17si3J8buy_no_wm.mp4"

# Build N templates (x1, y1, w, h) for each known watermark position
# Replace these with actual bounding boxes from vision_analyze
TEMPLATES = [
    # (label, x, y, w, h) — relative to source video frame
    ("bottom", 0, 1600, 142, 113),    # Example: bottom-left watermark
    ("top", 670, 30, 420, 140),        # Example: top-right watermark
]
# =============================

if os.path.exists(OUT):
    os.remove(OUT)

# Get durations
def get_duration(path):
    s = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True
    ).stdout
    return float(s.strip()) if s else 0.0

def get_fps(path):
    s = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=avg_frame_rate",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True
    ).stdout.strip()
    return float(s.split('/')[0]) / float(s.split('/')[1])

v_dur = get_duration(VIDEO)
FPS = get_fps(VIDEO)
print(f"Video: {v_dur:.2f}s, FPS: {FPS}")

# Step 1: Extract all frames
FRAME_DIR = "/tmp/wm_frames"
os.makedirs(FRAME_DIR, exist_ok=True)
for f in os.listdir(FRAME_DIR):
    os.remove(f"{FRAME_DIR}/{f}")

result = subprocess.run(
    ["ffmpeg", "-y", "-i", VIDEO, "-vsync", "0", f"{FRAME_DIR}/frame_%05d.png"],
    capture_output=True, text=True
)
total = len(sorted(os.listdir(FRAME_DIR)))
print(f"Extracted {total} frames")

# Step 2: Build templates
print("Building templates...")
templates = []
PAD = 10
for label, x, y, w, h in TEMPLATES:
    sample_idx = min(total // 4, 100)  # sample early frame
    img = cv2.imread(f"{FRAME_DIR}/frame_{sample_idx:05d}.png")
    if img is None:
        print(f"  ⚠️  No frame for template {label}, skipping")
        continue
    y1, y2 = max(0, y - PAD), min(img.shape[0], y + h + PAD)
    x1, x2 = max(0, x - PAD), min(img.shape[1], x + w + PAD)
    tmpl = img[y1:y2, x1:x2]
    tmpl_gray = cv2.cvtColor(tmpl, cv2.COLOR_BGR2GRAY)
    templates.append((label, tmpl_gray, tmpl.shape, x, y, w, h))
    print(f"  ✅ {label}: {tmpl.shape}")

# Step 3: Track
print("Tracking...")
tracking = []
for i in range(total):
    frame_path = f"{FRAME_DIR}/frame_{i:05d}.png"
    if not os.path.exists(frame_path):
        continue
    frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
    if frame is None:
        continue

    best = (0, 0, 0, 0.0, None)
    for label, tmpl_gray, tmpl_shape, ox, oy, ow, oh in templates:
        result = cv2.matchTemplate(frame, tmpl_gray, cv2.TM_CCOEFF_NORMED)
        _, conf, _, loc = cv2.minMaxLoc(result)
        if conf > best[3] and conf > 0.4:
            best = (loc[0], loc[1], tmpl_gray.shape[1], tmpl_gray.shape[0], conf, label)

    if best[4] > 0.4:
        tracking.append((i, *best[:5]))

print(f"Tracked: {len(tracking)}/{total} frames")

# Step 4: Inpaint per frame
PROCESSED_DIR = "/tmp/wm_processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)
for f in os.listdir(PROCESSED_DIR):
    os.remove(f"{PROCESSED_DIR}/{f}")

track_dict = {t[0]: t[1:5] for t in tracking}

for i in range(total):
    frame_path = f"{FRAME_DIR}/frame_{i:05d}.png"
    frame = cv2.imread(frame_path)
    if frame is None:
        continue

    if i in track_dict:
        x, y, w, h = track_dict[i]
        x = max(0, min(x, frame.shape[1] - w))
        y = max(0, min(y, frame.shape[0] - h))

        roi = frame[y:y+h, x:x+w].copy()
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Background from edges
        edges = np.concatenate([
            gray_roi[:PAD, :].flatten(),
            gray_roi[-PAD:, :].flatten(),
            gray_roi[:, :PAD].flatten(),
            gray_roi[:, -PAD:].flatten()
        ])
        bg = np.median(edges)
        bg_std = np.std(edges)

        # Mask
        mask = (np.abs(gray_roi.astype(float) - bg) > max(15, bg_std * 2)).astype(np.uint8) * 255
        bright_mask = ((gray_roi > 80) & (gray_roi < 230)).astype(np.uint8) * 255
        mask = cv2.bitwise_or(mask, bright_mask)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)

        inpainted = cv2.inpaint(roi, mask, 7, cv2.INPAINT_TELEA)
        frame[y:y+h, x:x+w] = inpainted

    cv2.imwrite(f"{PROCESSED_DIR}/frame_{i:05d}.png", frame)

print(f"Processed {total} frames")

# Step 5: Re-encode
print(f"Re-encoding at {FPS} fps...")
cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", f"{PROCESSED_DIR}/frame_%05d.png",
    "-i", VIDEO,
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
    "-c:a", "aac", "-b:a", "128k",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    OUT
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
print(f"Re-encode: exit={result.returncode}")
if result.returncode != 0:
    print("STDERR:", result.stderr[-500:])

# Cleanup
import shutil
for d in [FRAME_DIR, PROCESSED_DIR]:
    shutil.rmtree(d, ignore_errors=True)

if os.path.exists(OUT):
    print(f"\n✅ {OUT} ({os.path.getsize(OUT)/1024/1024:.2f} MB)")
