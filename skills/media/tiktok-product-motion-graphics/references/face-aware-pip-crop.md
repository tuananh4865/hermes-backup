# Face-Aware PIP Crop — Apple's Vision Framework Approach

Pitfall 12 (verified 17/07 V5) — crop PIP must be face-aware, never blind percentage cut.

## Why OpenCV doesn't work in venv

CascadeClassifier is not auto-imported via pip `opencv-python`. Default venv doesn't ship `data/haarcascades/`. You'll get:

```python
import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# AttributeError: module 'cv2' has no attribute 'data'
```

## Apple Vision framework — native, fast, accurate on macOS

Compile Swift script, run on extracted frames, convert coords to ffmpeg crop.

### Step 1: Compile

```bash
swiftc scripts/detect_face.swift -o scripts/detect_face
chmod +x scripts/detect_face
```

Verify:

```bash
./scripts/detect_face --help    # exits 1, prints usage
./scripts/detect_face frame.jpg  # exits 0, prints "FACE x y w h"
```

### Step 2: Run on extracted frames

```bash
# Extract 1 frame per second from the heavy-info phase window
ffmpeg -y -ss 7.3 -i src.mp4 -frames:v 1 -vf "scale=864:1536" frame_7.3.jpg
ffmpeg -y -ss 8.0 -i src.mp4 -frames:v 1 -vf "scale=864:1536" frame_8.0.jpg
ffmpeg -y -ss 9.0 -i src.mp4 -frames:v 1 -vf "scale=864:1536" frame_9.0.jpg
# ...

for f in frame_*.jpg; do
  ./scripts/detect_face "$f"
done
```

Each line: `FACE x y w h` (normalized 0-1, Vision bottom-left origin).

### Step 3: Convert Vision coords → ffmpeg crop

⚠ **Vision uses BOTTOM-LEFT origin** (y=0 bottom, y=1 top). ffmpeg uses TOP-LEFT. **Always flip y.**

```python
# Vision output: x, y, w, h (normalized 0-1)
# Want: ffmpeg crop=W:H:x:y (pixels, top-left)

y_top = 1.0 - y - h           # flip
px = int(x * SRC_W)           # 1728 for Pocket3 portrait
py = int(y_top * SRC_H)       # 3072 for Pocket3 portrait
pw = int(w * SRC_W * 1.4)    # 40% padding for safety
ph = int(h * SRC_H * 1.4)    # 40% padding

# Clamp to source bounds
if px + pw > SRC_W: pw = SRC_W - px
if py + ph > SRC_H: ph = SRC_H - py
if px < 0: pw += px; px = 0
if py < 0: ph += py; py = 0
```

Batch script (Python):

```python
import subprocess, json

SRC_W, SRC_H = 1728, 3072
samples = []
for sec in range(7, 13):
    jp = f"frame_{sec}.jpg"
    subprocess.run(["ffmpeg", "-y", "-ss", str(sec), "-i", "src.mp4",
                    "-frames:v", "1", "-vf", "scale=864:1536", jp],
                   capture_output=True, timeout=10)
    r = subprocess.run(["./detect_face", jp], capture_output=True, text=True, timeout=10)
    for line in r.stdout.split("\n"):
        if line.startswith("FACE "):
            parts = line.split()
            x, y, w, h = map(float, parts[1:5])
            y_top = 1.0 - y - h
            samples.append((int(x*SRC_W), int(y_top*SRC_H),
                            int(w*SRC_W*1.4), int(h*SRC_H*1.4)))

# Robust average (trim 20% outliers)
xs = sorted([s[0] for s in samples])
ys = sorted([s[1] for s in samples])
n = len(samples); trim = max(1, n // 5)
xs_trim, ys_trim = xs[trim:n-trim], ys[trim:n-trim]
avg_x, avg_y = sum(xs_trim)//len(xs_trim), sum(ys_trim)//len(ys_trim)
ws, hs = [s[2] for s in samples], [s[3] for s in samples]
avg_w = max(ws); avg_h = max(hs)  # use MAX to ensure face fits

# Clamp
if avg_x + avg_w > SRC_W: avg_w = SRC_W - avg_x
if avg_y + avg_h > SRC_H: avg_h = SRC_H - avg_y

print(f"crop={avg_w}:{avg_h}:{avg_x}:{avg_y}")
```

### Step 4: ffmpeg crop + scale

```bash
ffmpeg -y -ss 7.3 -i src.mp4 -t 6.0 \
  -vf "crop=1536:1536:192:698,scale=400:400" \
  -c:v libx264 -preset fast -crf 23 -an \
  -movflags +faststart pip_chart.mp4

ffmpeg -y -ss 18.9 -i src.mp4 -t 8.9 \
  -vf "crop=1480:1712:248:763,scale=400:400" \
  -c:v libx264 -preset fast -crf 23 -an \
  -movflags +faststart pip_port.mp4
```

## Sample timeline (sac-du-phong 17/07)

```
phase chart (7-13s):       face center (982,1488), size 1128×1128
                            → output 1536×1536 crop at (192,698) → 400×400 PIP
phase port (18.9-27.8s):  face center (1103,1618), size 1223×1223
                            → output 1480×1712 crop at (248,763) → 400×400 PIP
```

## HyperFrames composition

```html
<!-- Layer 5: PIP cropped video (face-aware) -->
<video id="pip-chart" class="pip-video"
       data-start="7.3" data-duration="6"
       src="assets/source/pip/chart.mp4" muted playsinline></video>

<video id="pip-port" class="pip-video"
       data-start="18.9" data-duration="8.9"
       src="assets/source/pip/port.mp4" muted playsinline></video>

<!-- Each video MUST have unique id (Pitfall 2) -->
```

```css
/* V6 FINAL: small góc trên trái (NOT center, NOT large) */
.pip-video {
  position: absolute; z-index: 4;
  top: 80px; left: 80px;
  width: 420px; height: 420px;
  border-radius: 28px;
  border: 3px solid rgba(255,255,255,0.8);
  box-shadow: 0 16px 48px rgba(0,0,0,0.6);
}
```

GSAP toggle:

```javascript
tl.to(blackBg, { opacity: 1, duration: 0.4 }, 7.3);   // black-bg swap
tl.fromTo(pipChart, { opacity: 0, scale: 0.85, x: -60 }, 
          { opacity: 1, scale: 1, x: 0, duration: 0.6, ease: "back.out(1.2)" }, 7.4);
tl.to(pipChart, { opacity: 0, duration: 0.3 }, 13.0);
tl.to(blackBg, { opacity: 0, duration: 0.3 }, 13.1);
```

## Performance notes

- Vision: 30-50ms per frame on M1/M2 (CPU only, no GPU)
- 6 samples × 50ms = 300ms total → < 1 second for full phase analysis
- Network: zero (Vision is on-device)
- Cost: zero (vs $0.001/image for cloud face detectors)
