---
title: HyperFrames GSAP timeline capture pitfalls
created: 2026-08-25
type: reference
applies_to: hyperframes skill
session_origin: dam-me-intro motion composition attempt (Dầm Mê)
---

# HyperFrames — GSAP Timeline Capture Pitfalls

## CRITICAL: HyperFrames does NOT render animations frame-by-frame

After multiple render attempts, the resulting MP4 only contains a SINGLE frame
repeated 240 times (verified via `md5` of frames extracted at different
timestamps). The file spec shows `nb_frames=240 duration=8.000000` but
visually only one state is captured.

**Root cause:** HyperFrames reads `timeline.duration()` to determine total
render time, then captures the composition state — but it does NOT seek the
timeline forward through each frame interval during capture. All frames
end up rendering the timeline at whatever `progress()` state it was when
the page loaded (typically time=0).

**What this means for your workflow:**

- ❌ HyperFrames is NOT suitable for character-by-character text reveals
- ❌ HyperFrames is NOT suitable for staggered animations
- ❌ HyperFrames is NOT suitable for any timeline where the visual changes over time
- ✅ HyperFrames IS suitable for static or near-static compositions (single state)
- ✅ HyperFrames IS suitable for ambient loops (particles, gradients) where the "static state" looks complete

**If you need actual frame-by-frame animation, use one of these instead:**
- Remotion (React-based, frame-by-frame native) — `remotion` skill
- Manim (Python, mathematical/programmatic animation) — `manim-video` skill
- Playwright manual frame capture: launch browser, seek timeline per frame, screenshot, ffmpeg concat
- Lottie (export from After Effects)

---

## Pitfall 1: `repeat: -1` causes infinite duration

GSAP timelines with any tween that has `repeat: -1` will have
`timeline.duration()` return `Infinity`. HyperFrames detects this and
**silently skips capture entirely** (warning: `sub_timeline_readiness_timeout`).

**Fix:**
```js
// BAD — infinite duration, HyperFrames skips
gsap.to(el, { x: 100, repeat: -1, yoyo: true })

// GOOD — finite duration
gsap.to(el, { x: 100, repeat: 2, yoyo: true })  // plays 3 times, stops
```

---

## Pitfall 2: External tweens block the browser when timeline is paused

If you write particle loops using `gsap.to()` directly (not added to the
master timeline), they keep running even when you call `tl.pause()`. In a
Playwright headless context, this causes the browser event loop to spin
forever on every frame — `page.screenshot()` will hang indefinitely
(timeout after 300+ seconds).

**Fix:** Add ALL tweens to the master timeline:
```js
// BAD — runs forever even when timeline paused
gsap.utils.toArray('.particle').forEach((el, i) => {
  gsap.to(el, { x: 'random(-150, 150)', repeat: -1 });
});

// GOOD — finite duration, controlled by master timeline
gsap.utils.toArray('.particle').forEach((el, i) => {
  tl.to(el, { x: 100, duration: 4, delay: i * 0.3 }, 0);
});
```

---

## Pitfall 3: Wrapping `duration()` doesn't fix capture

Attempting to override `hyperframesTimeline.duration` (either via
`Object.defineProperty` getter OR method assignment) does NOT cause
HyperFrames to seek through frames. Even if you successfully report a
finite duration, the capture still produces a single static state.

**This is a fundamental HyperFrames limitation, not a workaround-able bug.**

---

## What the Dầm Mê session demonstrated

Built a full Dầm Mê intro composition (sage green brand, brand name with
5-char split, decorative lines, hero card with mango, CTA pill, particle
background). Final render at `/Volumes/Storage-1/Pocket3/Hermes-Edit/dam-me-intro_V6_8s_FINAL_AUTO.mp4` (1.1MB, 1080×1920, 30fps) shows the **complete composition at time=0** with all elements visible and styled — it just doesn't animate over time.

**Useful conclusion:** for "intro card" or "product splash" style videos that
look good as a single state, HyperFrames works fine. For "narrative" or
"sequential reveal" animations, use Remotion.

---

## Verified diagnostic commands

```bash
# Check if MP4 has multiple unique frames
ffmpeg -y -ss 0.5 -i output.mp4 -update 1 frame1.png 2>/dev/null
ffmpeg -y -ss 4.0 -i output.mp4 -update 1 frame2.png 2>/dev/null
md5 frame1.png frame2.png
# If both MD5s are identical → only 1 frame rendered (no animation seek)

# Check timeline state in browser
window.__timelines['main-video'].paused()       # bool
window.__timelines['main-video'].duration()     # seconds (Infinity = bug)
window.__timelines['main-video'].time()          # current playhead
```

---

## Working render command (for static compositions)

```bash
cd /path/to/hyperframes-project
hyperframes render . \
  -o "/Volumes/Storage-1/Pocket3/Hermes-Edit/<name>_V1_<dur>s_FINAL_AUTO.mp4" \
  -f 30 \
  -q high \
  --format mp4
```

Output: ~15-20s render time for 8s video, file size scales with composition
complexity (static composition ~1MB, complex multi-layer ~10MB+).
