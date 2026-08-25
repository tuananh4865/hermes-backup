"""
Depth Anything V2 Small + Motion-Aware Temporal Median + Bilateral Filter.

TIER 3 quality — use when Tier 2 (--smooth --sharpen) STILL flickers.
Adds per-pixel motion masking so static areas stay pixel-stable, and
bilateral filter for edge-preserving smoothing on moving areas.

Usage:
    ~/.hermes/hermes-agent/venv/bin/python scripts/depth_anything_video_v3.py \
        INPUT.mp4 OUTPUT_v3.mp4

Pipeline (10 stages):
  1. Probe input (ffprobe)
  2. Extract frames to /tmp/depth_v3_frames/ (ffmpeg vsync 0)
  3. Depth Anything V2 Small per frame (Apple MPS, ~25s for 504 frames)
  4. Build motion masks (cv2.absdiff + threshold + dilate)
  5. Per-pixel temporal median (window=9) ONLY on moving pixels
  6. Bilateral filter (edge-preserving) + unsharp mask
  7. Save depth PNGs
  8. Encode H.264 libx264 (crf 18, preset slow)

Cost: ~30s for 17s 30fps clip on M-series MPS.
Output: grayscale H.264 MP4 matching source W×H, fps, ~2.3 MB.
"""
import os, sys, time, subprocess
import numpy as np
import torch
import cv2
from PIL import Image
from transformers import pipeline

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if DEVICE == "mps" else torch.float32

INPUT = sys.argv[1]
OUTPUT = sys.argv[2]
TEMPORAL_WINDOW = 9
MOTION_THRESHOLD = 8

print(f"📹 Input: {INPUT}")
print(f"📤 Output: {OUTPUT}")
print(f"⚙️ Device: {DEVICE} | Window: {TEMPORAL_WINDOW} | Motion threshold: {MOTION_THRESHOLD}")

# Load model
print("🔄 Loading Depth Anything V2 Small...")
t0 = time.time()
pipe = pipeline(
    task="depth-estimation",
    model="depth-anything/Depth-Anything-V2-Small-hf",
    device=DEVICE,
    torch_dtype=TORCH_DTYPE,
)
print(f"✅ Loaded in {time.time()-t0:.1f}s")

# Probe input
r = subprocess.run(
    ["ffprobe", "-v", "error", "-select_streams", "v:0",
     "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
     "-count_frames", "-of", "csv=p=0", INPUT],
    capture_output=True, text=True, timeout=30
)
parts = r.stdout.strip().split(",")
W, H = int(parts[0]), int(parts[1])
fps_parts = parts[2].split("/")
FPS = float(fps_parts[0]) / float(fps_parts[1]) if len(fps_parts) == 2 else float(fps_parts[0])
NB_FRAMES = int(parts[3]) if len(parts) > 3 else None
print(f"📐 {W}×{H}, {FPS:.2f} fps, {NB_FRAMES or '?'} frames")

# Extract frames
WORK = "/tmp/depth_v3_frames"
os.makedirs(WORK, exist_ok=True)
for f in os.listdir(WORK):
    os.remove(os.path.join(WORK, f))
print("📦 Extracting frames...")
r = subprocess.run(
    ["ffmpeg", "-y", "-i", INPUT, "-vsync", "0", "-q:v", "2",
     os.path.join(WORK, "f%06d.png")],
    capture_output=True, text=True, timeout=120
)
if r.returncode != 0:
    print("FFMPEG extract FAILED:", r.stderr[-500:])
    sys.exit(1)
frames = sorted([f for f in os.listdir(WORK) if f.endswith(".png")])
print(f"   Extracted {len(frames)} frames")

# Stage 3: Run depth model
print(f"🎨 Running Depth Anything V2 → raw depth maps...")
raw_depths = []
t0 = time.time()
target_w = 384
for i, fname in enumerate(frames, 1):
    img = Image.open(os.path.join(WORK, fname)).convert("RGB")
    scale = target_w / img.width
    img_small = img.resize((target_w, int(img.height * scale)), Image.LANCZOS)
    result = pipe(img_small)
    depth = result["depth"]
    depth_full = depth.resize((W, H), Image.LANCZOS)
    raw_depths.append(np.array(depth_full, dtype=np.uint8))
    if i % 50 == 0 or i == len(frames):
        elapsed = time.time() - t0
        eta = elapsed / i * (len(frames) - i)
        print(f"   {i}/{len(frames)} ({i/len(frames)*100:.0f}%) — {elapsed:.1f}s, ETA {eta:.0f}s")
for f in frames:
    os.remove(os.path.join(WORK, f))
print(f"💾 Raw depth maps: {len(raw_depths)} frames")

# Stage 4: Build motion masks
print(f"🎬 Building motion masks...")
motion_masks = []
t0 = time.time()
for i in range(len(raw_depths)):
    if i == 0:
        mask = np.zeros((H, W), dtype=np.uint8)
    else:
        diff = cv2.absdiff(raw_depths[i], raw_depths[i-1])
        _, mask = cv2.threshold(diff, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
    motion_masks.append(mask)
    if (i+1) % 100 == 0 or i == len(raw_depths)-1:
        elapsed = time.time() - t0
        eta = elapsed / (i+1) * (len(raw_depths) - i - 1)
        print(f"   {i+1}/{len(raw_depths)} — {elapsed:.1f}s, ETA {eta:.0f}s")
print(f"✅ Motion masks done in {time.time()-t0:.1f}s")

# Stage 5: Per-pixel temporal median (only moving pixels)
print(f"🔧 Per-pixel temporal median (window={TEMPORAL_WINDOW}, moving pixels only)...")
half = TEMPORAL_WINDOW // 2
smoothed_stack = np.stack(raw_depths, axis=0)  # TxHxW uint8
motion_stack = np.stack(motion_masks, axis=0)  # TxHxW uint8
output_frames = []
moving_pixel_count = 0
total_moving = 0
t0 = time.time()
for i in range(len(raw_depths)):
    lo = max(0, i - half)
    hi = min(len(raw_depths), i + half + 1)
    window = smoothed_stack[lo:hi]
    motion_window = motion_stack[lo:hi]
    current_motion = motion_masks[i] > 0
    has_motion_in_window = (motion_window > 0).any(axis=0)
    needs_smoothing = has_motion_in_window & current_motion
    median = np.median(window, axis=0).astype(np.uint8)
    result = np.where(needs_smoothing, median, raw_depths[i])
    output_frames.append(result)
    moving_pixel_count += needs_smoothing.sum()
    total_moving += current_motion.sum()
    if (i+1) % 100 == 0 or i == len(raw_depths)-1:
        elapsed = time.time() - t0
        eta = elapsed / (i+1) * (len(raw_depths) - i - 1)
        pct = moving_pixel_count / max(1, total_moving) * 100
        print(f"   {i+1}/{len(raw_depths)} — {elapsed:.1f}s, ETA {eta:.0f}s, smoothed {pct:.0f}% of moving")
print(f"✅ Smoothed in {time.time()-t0:.1f}s")

# Stage 6: Bilateral + unsharp
print(f"🔪 Bilateral filter + unsharp mask...")
t0 = time.time()
for i in range(len(output_frames)):
    arr = output_frames[i]
    filtered = cv2.bilateralFilter(arr, d=5, sigmaColor=15, sigmaSpace=15)
    blurred = cv2.GaussianBlur(filtered, (0, 0), 1.5)
    sharpened = cv2.addWeighted(filtered, 1.5, blurred, -0.5, 0)
    output_frames[i] = np.clip(sharpened, 0, 255).astype(np.uint8)
    if (i+1) % 100 == 0 or i == len(output_frames)-1:
        elapsed = time.time() - t0
        eta = elapsed / (i+1) * (len(output_frames) - i - 1)
        print(f"   {i+1}/{len(output_frames)} — {elapsed:.1f}s, ETA {eta:.0f}s")
print(f"✅ Bilateral done in {time.time()-t0:.1f}s")

# Stage 7: Save depth frames
print(f"💾 Saving {len(output_frames)} frames...")
for i, arr in enumerate(output_frames, 1):
    Image.fromarray(arr, mode="L").save(os.path.join(WORK, f"d{i:06d}.png"))

# Stage 8: Encode video
print(f"🎬 Encoding final video...")
r = subprocess.run(
    ["ffmpeg", "-y", "-framerate", f"{FPS:.3f}",
     "-i", os.path.join(WORK, "d%06d.png"),
     "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
     "-preset", "slow", "-movflags", "+faststart",
     OUTPUT],
    capture_output=True, text=True, timeout=300
)
if r.returncode != 0:
    print("FFMPEG encode FAILED:", r.stderr[-500:])
    sys.exit(1)
size = os.path.getsize(OUTPUT)
print(f"✅ Output: {OUTPUT} ({size:,} bytes, {size/1024/1024:.1f} MB)")

r = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries",
     "format=duration:stream=width,height,codec_name,pix_fmt,r_frame_rate",
     "-of", "default=noprint_wrappers=1", OUTPUT],
    capture_output=True, text=True, timeout=15
)
print(f"\n📊 Output spec:\n{r.stdout}")
for f in os.listdir(WORK):
    os.remove(os.path.join(WORK, f))
print("🧹 Cleanup done")