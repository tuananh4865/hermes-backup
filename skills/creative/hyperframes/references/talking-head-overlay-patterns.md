# Talking-head overlay patterns (HyperFrames)

Lessons from a 10-version rebuild loop on one TikTok clip (Gochodoc power bank, 32s, Pocket3 vertical 1728×3072). The user said "Layout vẫn nằm lộn xộn nặng" and "phần nền đen ở trung tâm bị trống" repeatedly. The patterns below are what finally worked.

## When to load this

Load this file when the request is something like:
- "make a TikTok / Shorts / Reel from this raw clip"
- "edit video with motion graphics"
- "add captions / labels to talking-head footage"
- "liquid glass style on top of video"

Do NOT load for general video editing, color grading, or non-overlay work.

## Step 0 — STOP and ask for input

Before writing any HTML, confirm you know:

1. **Where the face is** in the source frame. If you haven't run face detection yet, do that now using the workflow below.
2. **Which layout zones the user wants** in plain English. If the user can't describe it in one sentence, ask for either:
   - A reference video they approve, OR
   - A wireframe (text + arrow positions), OR
   - A one-sentence zone statement like "text only top + bottom, glass card center during PIP crop".

Do NOT guess positions. The user has corrected 10 rebuilds of one clip. The next one without input will fail the same way.

## Step 1 — Detect the face position with Vision framework

OpenCV `CascadeClassifier` is NOT available in the Hermes hermes-agent venv (the python module does not expose it; the venv is missing the `cv2.data` haarcascades). On macOS the cleanest path is a small Swift binary using `VNDetectFaceRectanglesRequest`:

```bash
cat > /tmp/detect_face.swift << 'EOF'
import Foundation
import Vision
import AppKit

let url = URL(fileURLWithPath: CommandLine.arguments[1])
let image = NSImage(contentsOf: url)
guard let cgImage = image?.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("ERROR: load"); exit(1)
}
let request = VNDetectFaceRectanglesRequest { request, _ in
    if let obs = request.results as? [VNFaceObservation] {
        for o in obs {
            let b = o.boundingBox
            print("FACE \(b.origin.x) \(b.origin.y) \(b.size.width) \(b.size.height)")
        }
    }
}
try VNImageRequestHandler(cgImage: cgImage, options: [:]).perform([request])
EOF
swiftc /tmp/detect_face.swift -o /tmp/detect_face   # ~70KB native binary
```

Vision's coordinate origin is bottom-left. Convert to top-left and pixel space:

```python
# Vision gives normalized (x, y, w, h) where y=0 is bottom
y_top = 1.0 - y - h
x_px = int(x * frame_w)
y_px = int(y_top * frame_h)
w_px = int(w * frame_w)
h_px = int(h * frame_h)
```

Sample at least 5–8 frames covering all phases (e.g. every 3 seconds of a 32s clip). Average bbox per phase for the layout, and take the union (max top, min bottom, max extent left/right) for safe-zone math.

## Step 2 — Derive the 3 layout zones

Once you know the face bbox range across all phases:

```
TOP zone    = 0            → face_top − 60     (header / eyebrow / title)
CENTER     = face_top − 60 → face_bottom + 60   (MUST stay clear if no PIP)
BOTTOM     = 1500         → 1920              (stats, CTA, captions)
```

For Pocket3 vertical (1728×3072) talking head with face center around Y=850, this typically becomes:
- TOP safe for content: 0–480
- Face zone (no content): 480–1430
- BOTTOM safe: 1500–1800

Add 60–100 px buffer on each face boundary because face position drifts as the speaker moves their head.

## Step 3 — Phase classification

Decide per phase whether the face is "full" or "PIP" visible:

| Phase type | When | Background | Where face is | Where to put text |
|---|---|---|---|---|
| **Full-face** | phase has no detail crop, speaker explains a low-info point | original video | bottom half of CENTER zone | text in TOP + BOTTOM only |
| **PIP-face** | phase conveys a comparison/diagram that needs screen real estate | black underlay | top-left 340×340 inset | liquid glass card spans center to fill the empty zone, smaller stat cards on the right |

The single most common failure was leaving the black-background PIP zone with **only the PIP** in the corner and nothing else. The center stays black and looks like a missing render. Fill it.

## Step 4 — Build the HTML layout

Conventions that survived review:

```html
<!-- 1. video bg full-frame -->
<video class="video-bg" data-start="0" data-duration="32"
       src="full_bg.mp4" muted playsinline />

<!-- 2. black underlay (only visible during PIP phases) -->
<div class="black-bg"></div>

<!-- 3. no face-protect / vignette over the face -->

<!-- 4. PIP wrapper, top-left corner, 340x340 ish -->
<div class="pip-wrap" style="top:80px; left:80px; width:340px; height:340px">
  <video src="pip.mp4" data-start="7" data-duration="6" muted /></video>
</div>

<!-- 5. glass card CENTER (only during PIP, fills the dead black zone) -->
<div class="liquid-glass center">...chart / diagram...</div>

<!-- 6. glass cards TOP + BOTTOM for full-face phases -->
<div class="liquid-glass top">...eyebrow + title...</div>
<div class="liquid-glass bottom">...stats...</div>

<!-- 7. caption bar at bottom (only zone below face) -->
<div class="caption-bar" style="bottom:50px">...voice transcript...</div>
```

The `.liquid-glass` class needs all five polish layers (see SKILL.md):

```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border: 1.5px solid rgba(255, 255, 255, 0.4);
  border-radius: 32px;
  padding: 32px 36px;
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: "";
  position: absolute; inset: 0;
  border-radius: 32px;
  background:
    radial-gradient(circle at 15% 0%, rgba(255, 255, 255, 0.5), transparent 45%),
    radial-gradient(circle at 100% 100%, rgba(255, 255, 255, 0.25), transparent 35%);
  pointer-events: none;
}
.liquid-glass > * { position: relative; }
```

Dark `rgba(15, 20, 30, 0.85)` panels are NOT liquid glass — they read as dark dashboards and the user will say "liquid glass gone".

## Step 5 — GSAP timeline with buffer zones

Each phase fade-in must start AFTER the previous fade-out finishes. A safe rule:

```
Phase N ends   = t
Phase N+1 starts = t + 0.5s  (buffer for visual separation)
```

If you tween both phases on top of each other, the user sees ghosting and labels it "chồng chữ". On the bottom-zone glass, use:

```js
tl.to([hookTop, hookUpper, hookBottom], { opacity: 0, duration: 0.4 }, 2.1);
tl.fromTo(problemTop, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.5 }, 2.6);
```

The 0.5s gap avoids simultaneous opacity tweens creating composite text artifacts.

## Step 6 — Render, extract frames, verify by EYE

After `npx hyperframes render` succeeds:

```bash
mkdir -p frames
for t in 1 5 8 12 16 20 25 30; do
  ffmpeg -y -ss $t -i output_silent.mp4 -frames:v 1 -q:v 2 frames/t_$t.jpg
done
# Audio mux
ffmpeg -y -i output_silent.mp4 -i <source.mp4> \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -shortest \
  output_with_audio.mp4
```

Run each extracted frame through `vision_analyze` with a question like:
- "Is the speaker's face occluded by any glass card or chart?"
- "Is the chart / port diagram fully visible, not cut off?"
- "Is there any text overlap between two simultaneously-visible zones?"

If ANY frame shows the face occluded or two zones' text overlapping, do NOT ship. Fix the layout (zone positioning or phase timing) and re-render. HyperFrames `check` will not catch this — it validates HTML and contrast, not visual stacking.

## Things that look fine in `npx hyperframes preview` and break in render

- `<video>` src paths that exist in preview cache but cause a black frame in render
- CSS `transform: translateY(-50%)` combined with `position: absolute; top: 540px` rendering at a different Y in render vs preview
- Phase transition overlapping by 0.05s — preview sometimes masks it, render does not

Always extract frames from `output_silent.mp4`, not from the preview server URL.
