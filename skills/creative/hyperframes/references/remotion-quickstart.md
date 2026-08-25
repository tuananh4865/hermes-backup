# Remotion Quickstart (sibling tool to HyperFrames)

Added 2026-07-16 after a 30s cyberpunk trailer was successfully rendered.

## When to use Remotion over HyperFrames

- You need 5+ distinct scenes with shared assets (component composition wins)
- Your team thinks in React/TypeScript already
- You need precise frame-by-frame control (Remotion is fundamentally `useCurrentFrame` based)
- You want to ship code that other engineers can review and extend
- The aesthetic isn't "glassmorphism ethereal" — e.g. B&W analog, terminal, neon, ASCII-overlay scenes

## Verified working stack (2026-07-16)

```
Node 26.4.0
npm 11.17.0
@remotion/cli 4.0.290
remotion 4.0.290
react 19.0.0
react-dom 19.0.0
@types/react 19.0.0
typescript 5.7.3
Google Chrome (for headless rendering)
ffprobe (for verification)
```

⚠️ **Version pin traps:**
- `typescript@5.5.0` does NOT exist on npm → install fails with ETARGET
- Use `typescript@5.7.3` (verified good as of 2026-07-16)
- Remotion 4.x requires React 19+. Older React 18 will fail peer-dep checks.

## Project skeleton (minimum viable)

```
trailer/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── src/
│   ├── index.ts        # entry: registerRoot(RemotionRoot)
│   ├── Root.tsx        # <Composition id="Trailer" .../>
│   ├── Trailer.tsx     # timeline + per-scene <Sequence>
│   └── Scenes.tsx      # 9 scene components + FilmFX layer
└── out/trailer.mp4     # rendered output
```

### package.json
```json
{
  "name": "trailer",
  "version": "0.1.0",
  "scripts": {
    "build": "remotion render src/index.ts Trailer out/trailer.mp4",
    "studio": "remotion studio src/index.ts"
  },
  "dependencies": {
    "@remotion/cli": "4.0.290",
    "remotion": "4.0.290",
    "react": "19.0.0",
    "react-dom": "19.0.0"
  },
  "devDependencies": {
    "@types/react": "19.0.0",
    "typescript": "5.7.3"
  }
}
```

### remotion.config.ts
```ts
import { Config } from '@remotion/cli/config';
export default { Config: { fps: 24, durationInFrames: 24*30, width: 1080, height: 1080, outDir: 'out' } satisfies Config };
```

### src/index.ts
```ts
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';
registerRoot(RemotionRoot);
```

### src/Root.tsx
```tsx
import React from 'react';
import { Composition } from 'remotion';
import { Trailer } from './Trailer';

export const FPS = 24;
export const DURATION_IN_FRAMES = FPS * 30; // 30s

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Trailer"
        component={Trailer}
        durationInFrames={DURATION_IN_FRAMES}
        fps={FPS}
        width={1080}
        height={1080}
      />
    </>
  );
};
```

## Render command

```bash
npx remotion render src/index.ts Trailer out/trailer.mp4 \
  --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --concurrency=2
```

- 720 frames (30s @ 24fps) renders in ~40s on M-series Mac with concurrency=2
- Output: H.264 video + AAC audio (silent by default, 48kHz), `pix_fmt=yuvj420p` (works everywhere)
- File size: ~6-8 MB for 30s of 1080×1080 with moderate complexity

## Verify output

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate \
  -of default=nw=1 out/trailer.mp4
```

Expected PASS: `h264` + `aac` + `1080×1080` + `24/1` + `~30s` duration.

## The 5 gotchas that broke the first render (and how to avoid them)

### 1. `random()` API confusion (Remotion 4.x)

```ts
// ❌ Throws TypeError: rng is not a function
const rng = random(`g-${seed}-${dots}`);
const x = rng() * 1080;

// ✅ Remotion 4.x: random(key) returns a number directly
const rng = (k: string) => random(`g-${seed}-${dots}-${k}`);
const x = rng(`x${i}`) * 1080;
```

For deterministic per-frame variation: compose keys with `frame`, `seed`, and a unique suffix per pixel/data-point.

### 2. CSS `filter: grayscale()` doesn't override colored text

```tsx
// ❌ Looks grayscale in inspector, but renders brand color in browser
<div style={{ color: '#76b900', filter: 'grayscale(1) contrast(1.4)' }}>
  NVIDIA
</div>
```

Fix: replace CSS text with PNG/SVG logo, or use `mix-blend-mode: difference`, or hand-pick the gray hex. Browser font fallback can re-introduce brand color even with grayscale filter applied.

### 3. Bad npm version pin = silent ETARGET failure

```bash
# Bad — typescript 5.5.0 doesn't exist on npm
"typescript": "5.5.0"

# Good — verified 2026-07-16
"typescript": "5.7.3"
```

Always check `npm view <pkg> versions` before pinning. Remotion's template assumes you do.

### 4. Don't ship a video without verifying visually

After every render:
```bash
# Extract 6-10 sample frames spaced across the timeline
for t in 1 4 7 11 17 25 29; do
  ffmpeg -y -loglevel error -ss $t -i out/trailer.mp4 -frames:v 1 -q:v 2 contact/t_${t}.jpg
done

# Make a contact sheet with PIL
python3 -c "
from PIL import Image, ImageDraw, ImageOps
import glob
fs = sorted(glob.glob('contact/t_*.jpg'))
w = h = 540
s = Image.new('RGB', (w*3, h*((len(fs)+2)//3)), (20,20,20))
dr = ImageDraw.Draw(s)
for i, x in enumerate(fs):
    im = ImageOps.fit(Image.open(x).convert('RGB'), (w, h))
    s.paste(im, ((i%3)*w, (i//3)*h))
    dr.text(((i%3)*w+10, (i//3)*h+10), x.split('_t_')[1].split('.')[0]+'s', fill='red')
s.save('contact/_contact.jpg', quality=88)
"
```

Load the contact sheet through vision_analyze to spot:
- Empty/missing focal points in any scene
- Brand color bleed-through on B&W sections
- Vignette too dark in corners
- Logo end-card tonal mismatch

### 5. Stop iterating after 2 visual-feedback rounds on cosmetic issues

After the 1st round shipping a 30s trailer, the user reviewed the contact sheet. Round 2 fixed 2 of 3 flagged issues (added ASCII log overlay + B&W-ed NVIDIA wordmark). The third issue (Stripe wordmark staying purple) couldn't be cleanly fixed via CSS — would require swapping to a PNG logo.

Lesson: spend max 2 rounds on visual polish. After that, ship the working version with the remaining issues noted, and let the user decide if another pass is worth the time.

## Reusable scene component pattern

Each scene is a thin wrapper around the underlying scene component, plus a FilmFX layer:

```tsx
// src/Trailer.tsx
import { Sequence, AbsoluteFill, useCurrentFrame } from 'remotion';

export const Trailer: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <Sequence from={0} durationInFrames={72}><SceneServerOrMain /></Sequence>
      <Sequence from={72} durationInFrames={72}><SceneMonitorWallOrMain /></Sequence>
      {/* ... */}
    </AbsoluteFill>
  );
};

const SceneServerOrMain: React.FC = () => {
  const frame = useCurrentFrame(); // local frame inside this Sequence
  return (
    <>
      <SceneServer frame={frame} />
      <FilmFX seed={1} grain={0.45} scanline={0.3} vignette={0.9} />
    </>
  );
};
```

The wrapper pattern lets each scene own its own FilmFX parameters (different grain intensity per scene) while keeping the scene components pure and reusable.

## When NOT to use Remotion

- 5-second one-shot reveal with no scene transitions → use HyperFrames (less setup)
- Math/algorithm explainer → use [[manim-video]] (LaTeX + math objects)
- Need to render >100 variations → batch Remotion is slow; HyperFrames or After Effects wins
- Audio-reactive content → Manim or a different tool (Remotion doesn't have built-in audio analysis)