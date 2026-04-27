---
title: Remotion
created: 2026-04-13
updated: 2026-04-13
type: entity
tags: [product, video, react, animation]
sources: [raw/articles/remotion-github.md]
confidence: high
relationships: []
---

# Remotion

Remotion là framework tạo video bằng React code. Dùng code thay thế GUI editor — leverage programming để animate, compute, và generate video một cách programmatic.

## Core Concept

- **Video = React Component** — viết animation bằng JSX + hooks
- **Frame-driven** — mọi animation dựa trên `useCurrentFrame()`, không dùng CSS transitions/animations
- **FFmpeg rendering** — render ra MP4 thông qua Chrome headless

## Key Hooks

```tsx
useCurrentFrame()                          // frame hiện tại (0, 1, 2, ...)
useVideoConfig()                            // { fps, width, height, durationInFrames }
interpolate(frame, [0, 30, 90, 120], [0, 1, 1, 0])  // map frame → giá trị
Easing.bezier(0.16, 1, 0.3, 1)            // easing curve
```

## Key Components

```tsx
<AbsoluteFill>          // fill toàn bộ frame
<Sequence from={fps}>   // delay/animate theo timeline
<Series>                // chain animations tuần tự
<Composition>           // định nghĩa video composition
registerRoot()          // entry point bắt buộc
```

## Cài đặt

```bash
npm install remotion @remotion/cli@latest
npx remotion browser ensure  # cài Chrome headless shell
```

## Render Commands

```bash
npx remotion still src/index.tsx MyVideo output.png   # 1 frame
npx remotion render src/index.tsx MyVideo output.mp4   # full video
npx remotion studio src/index.tsx                     # preview UI
```

## Minimum Project Structure

```tsx
// src/index.tsx
import { registerRoot } from "remotion";
import { Composition } from "remotion";
import { MyVideo } from "./HelloWorld";

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

## Animation Pattern

```tsx
const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 30, 90, 120], [0, 1, 1, 0]);
  const scale = interpolate(frame, [0, 60], [0.5, 1], {
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a2e" }}>
      <div style={{ opacity, transform: `scale(${scale})` }}>
        Hello!
      </div>
    </AbsoluteFill>
  );
};
```

## Sequencing

```tsx
<Series>
  <Series.Sequence durationInFrames={45}>
    <Intro />
  </Series.Sequence>
  <Series.Sequence durationInFrames={60}>
    <MainContent />
  </Series.Sequence>
</Series>
```

## License

- **Miễn phí**: cá nhân + công ty ≤3 người
- **Company License**: >3 người → remotion.pro

## Remotion Skills (AI Agent)

Remotion có sẵn skill cho AI coding agents (Claude Code, Codex, OpenCode):

```
npx remotion skills add  # install Remotion best practices skill
```

Skill bao gồm rules:
- `animations.md` — fundamental animation patterns
- `sequencing.md` — Sequence/Series timing
- `charts.md` — bar, pie, line, stock charts
- `text-animations.md` — typography animations
- `3d.md` — Three.js + React Three Fiber
- `audio.md`, `voiceover.md` — audio + ElevenLabs TTS
- `transitions.md` — scene transitions
- `maps.md` — Mapbox map animations

## Prompt Showcase

Community videos tại remotion.dev/prompts — top 12:

| # | Video Type | Author | Likes |
|---|-----------|--------|-------|
| 1 | News article headline highlight | @Remotion | 157 |
| 2 | Travel Route on Map with 3D landmarks | @JNYBGR | 151 |
| 3 | Product Demo for Presscut | @Shpigford | 112 |
| 4 | Launch Video on X | @ghumare64 | 108 |
| 5 | Rocket Launches Timeline | @crispynotfound | 75 |
| 6 | Transparent Call-To-Action overlay | @Remotion | 63 |
| 7 | Cinematic Tech Intro | @tiw_ari_ayu | 56 |
| 8 | Three.js "Top 20 Games Sold" Ranking | @DilumSanjaya | 46 |
| 9 | Real Estate Investing | HarisShah2345 | 34 |
| 10 | Shape to words transformation | @tiw_ari_ayu | 31 |
| 11 | Bar + Line Chart (combined) | samohovets | 31 |
| 12 | Promotion video for VVTerm | @wiedymi | 29 |

## Links

- Website: https://www.remotion.dev
- GitHub: https://github.com/remotion-dev/remotion
- Docs: https://www.remotion.dev/docs
- Skills: https://github.com/remotion-dev/skills
- Showcase: https://www.remotion.dev/prompts
