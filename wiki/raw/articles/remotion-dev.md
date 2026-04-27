---
confidence: high
last_verified: 2026-04-13
sources: [https://github.com/remotion-dev/remotion]
relationships: []
---

# Remotion — Video from React Code

**Website:** https://www.remotion.dev  
**GitHub:** https://github.com/remotion-dev/remotion  
**License:** Free for individuals + companies ≤3 employees; commercial license required otherwise (remotion.pro)

## Overview

Remotion is a framework for creating videos programmatically using React. Instead of using a video editor, you write React components that render to video frames.

### Why Remotion?

- Leverage web technologies: CSS, Canvas, SVG, WebGL
- Leverage programming: variables, functions, APIs, math, algorithms
- Leverage React: reusable components, composition, Fast Refresh, npm ecosystem

### Created with Remotion

- GitHub Unwrapped (githubunwrapped.com) — personalized year in review
- Fireship video tutorials — animated code demos
- Many others in the Remotion Showcase

## Setup (CLI / Non-Interactive)

Remotion's interactive CLI (`npx create-video@latest`) does NOT work in non-interactive terminals. Use manual scaffold instead:

```bash
mkdir my-video && cd my-video
npm init -y
npm install remotion @remotion/cli@latest
npx remotion browser ensure  # install Chrome headless shell
npm install typescript @types/react --save-dev
```

## Quick Start

All code in `src/index.tsx`:

```tsx
import { registerRoot } from "remotion";
import { Composition, AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

const MyVideo: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 30, 90, 120], [0, 1, 1, 0]);
  const scale = interpolate(frame, [0, 60], [0.5, 1]);

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a2e", justifyContent: "center", alignItems: "center" }}>
      <div style={{ opacity, transform: `scale(${scale})`, color: "white", fontSize: "120px" }}>
        Hello, Remotion!
      </div>
    </AbsoluteFill>
  );
};

registerRoot(() => (
  <Composition
    id="MyVideo"
    component={MyVideo}
    durationInFrames={150}
    fps={30}
    width={1920}
    height={1080}
  />
));
```

## CLI Commands

```bash
npx remotion still src/index.tsx MyVideo output.png   # render 1 frame
npx remotion render src/index.tsx MyVideo output.mp4 # render full video
npx remotion compositions src/index.tsx               # list compositions
```

## Core APIs

| Function | Purpose |
|---------|---------|
| `useCurrentFrame()` | Get current frame number |
| `useVideoConfig()` | Get fps, durationInFrames, width, height |
| `interpolate(x, [in], [out])` | Map input range to output range |
| `AbsoluteFill` | Component that fills entire frame |
| `Sequence` | Sequence/composition layers |
| `spring()` | Physics-based spring animation |
| `registerRoot()` | Required entry point registration |

## Demo Project

Location: `~/remotion-demo/` — working demo with:
- Fade-in title animation
- Frame counter
- 1920x1080 @ 30fps, 150 frames (5 seconds)
