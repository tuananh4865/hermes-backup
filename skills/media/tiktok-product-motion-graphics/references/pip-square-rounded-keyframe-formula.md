# PIP Square + Rounded Corners via GSAP Keyframe (FINAL FORMULA - V16)

## The full formula that passed visual verification on clip_0006 (anh approved after 15 failed attempts)

### The Three-Property Combination That Works

PIP square + face visible + rounded corners requires THREE coordinated GSAP properties animated together:
1. `scale` (UNIFORM — never scaleX/scaleY non-uniform, that distorts the face)
2. `clipPath` (GSAP-native keyframe property) with `inset(top right bottom left)` in pixels
3. `borderRadius` (GSAP animates CSS border-radius natively)

Reset all three back to defaults when leaving PIP phase.

### Why This Took 15 Tries (lesson log)

| Version | Approach | What Broke |
|---|---|---|
| V12 | `scale: 0.42, x: -222, y: -540` only | PIP was PORTRAIT (not square), no rounded corners |
| V13 | + `borderRadius: 28` | Rounded but still portrait |
| V14 | `scaleX: 0.39, scaleY: 0.22` (non-uniform) | Square achieved BUT face vertically squished (`scaleY: 0.22` compresses 1920→422 making the face look squeezed) |
| V15 | Reverted to uniform `scale: 0.42` | Face natural BUT PIP back to portrait |
| **V16 (final)** | Uniform scale + `clipPath: 'inset(193px 16.5px 193px 16.5px)'` | **All three: square + face natural + rounded corners** |

The key insight V14→V16: you CAN make a square PIP without distorting the face — scale uniformly for portrait, then use `clip-path: inset()` to crop the sides (not the face).

## Exact Code Template

### Video element setup
```css
#video-clip {
  position: absolute;
  top: 0; left: 0;
  width: 1080px; height: 1920px;
  object-fit: cover;
  transform-origin: 540px 960px;  /* MUST be at center for offset math */
}
```

### GSAP timeline — one full set of tweens for one PIP phase

```javascript
// === PIP enters (CHART at t=7s, top-left) ===
tl.to(videoClip, {
  scale: 0.42,                                          /* uniform keep aspect */
  x: -16,                                               /* shift left 16 */
  y: -193,                                              /* shift up 193 */
  borderRadius: 28,                                     /* 4 corners rounded */
  clipPath: 'inset(193px 16.5px 193px 16.5px)',        /* crop to square 420×420 */
  duration: 0.6,
  ease: 'power2.out'
}, 7.0);

// (show glass card beside/below PIP at same time)
tl.fromTo('#chart-glass', { opacity: 0, y: 50 },
  { opacity: 1, y: 0, duration: 0.6 }, 7.5);
// ... bars animate ...

// === PIP leaves (back to full screen) ===
tl.to('#chart-glass', { opacity: 0, duration: 0.3 }, 12.5);
tl.to(videoClip, {
  scale: 1, x: 0, y: 0,
  borderRadius: 0,
  clipPath: 'inset(0px 0px 0px 0px)',                  /* RESET clipPath too */
  duration: 0.5,
  ease: 'power2.in'
}, 12.8);
```

### The Math (deterministic — apply for any PIP size)

Given:
- Video source: `W_vid × H_vid` (e.g. 1080 × 1920 portrait)
- PIP target size: `W_pip × W_pip` (square 1:1, e.g. 420×420)

```
scale = W_pip / W_vid                                            /* 420/1080 = 0.389 */
scaled_W = W_vid * scale                                          /* 453 */
scaled_H = H_vid * scale                                          /* 806 */

inset_left   = (scaled_W - W_pip) / 2                            /* 16.5 */
inset_right  = (scaled_W - W_pip) / 2                            /* 16.5 */
inset_top    = (scaled_H - W_pip) / 2                            /* 193 */
inset_bottom = (scaled_H - W_pip) / 2                            /* 193 */

x = -inset_left                                                   /* -16 */
y = -inset_top                                                    /* -193 */

clipPath: 'inset(<top>px <right>px <bottom>px <left>px)'
```

### Other PIP sizes (pre-computed)

| PIP | scale | clipPath inset | x | y | Use case |
|---|---|---|---|---|---|
| 360×360 | 0.333 | inset(280 16.5 280 16.5) | -16 | -280 | small thumbnail |
| **420×420** | **0.389** | **inset(193 16.5 193 16.5)** | **-16** | **-193** | **standard (V16 used this)** |
| 480×480 | 0.444 | inset(140 16.5 140 16.5) | -16 | -140 | medium |
| 540×540 | 0.500 | inset(96 16.5 96 16.5) | -16 | -96 | large |

### Direction variants — same formula, different x

```javascript
// PIP top-LEFT  (V16 CHART)
tl.to(videoClip, { ..., x: -16, y: -193, ...}, 7.0);

// PIP top-RIGHT (V16 PORT)
// Just flip x to mirror
tl.to(videoClip, { ..., x: 16, y: -193, ...}, 19.0);
// (or keep -16 if the rounded-corner math works out symmetrically)
```

## Why It Took 15 Failed Attempts — Pattern Lessons

The user had to point out the problem SEVERAL times before I noticed:
1. V12–V13: "vẫn chưa được" (still not square)
2. V14: shipped with `scaleX/Y 0.22/0.39` — user spotted mặt bị crop immediately
3. V15: I reverted, traded face-natural for portrait — user rejected
4. V16: only user direction "bo góc tròn hơn, crop thành hình vuông, để đúng vị trí" + my solving for non-distortion produced correct formula

**The user's pattern**: high-level direction ("square + rounded + correct position"), ZERO interest in WHICH GSAP properties I use. They ship based on visual outcome.

**This means**: when iterating on visual output, the user's complaints are visual outcomes, not technical complaints. They don't say "you used scaleX/Y wrong"; they say "the face is squished". Translate visual complaints back to property changes without anchoring to the wrong diagnosis.

## Workflow rule for next clip

When the user says "square PIP + rounded corners":
1. Don't reach for `scaleX/scaleY` (distorts face — proven wrong in V14)
2. Don't try to add `border-radius` to a rectangular scale (still rectangular)
3. Combine uniform `scale` + `clipPath: 'inset(...)'` + `borderRadius` together
4. Always reset all three when leaving PIP phase (forgetting `clipPath` reset was a V12 leak)
5. **CRITICAL**: use `vision_analyze` on the rendered PNG before declaring it works. The user will catch it if you don't.

## Files

- Working template: `/Volumes/Storage-1/Hermes/scratch/hf_clip0006_V16/index.html`
- Final MP4: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_V16_100s_FINAL_PIP_SQUARE_FACE_OK.mp4`
- Sample PNGs: `/Volumes/Storage-1/Hermes/scratch/v16_samples/`
