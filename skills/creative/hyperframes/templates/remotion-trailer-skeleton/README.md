# Remotion Trailer Skeleton (minimal viable)

Edit `src/Trailer.tsx` and add `src/Scenes.tsx` to start building your trailer.

## Quick start

```bash
# from project root
npm install
npx remotion render src/index.ts Trailer out/trailer.mp4 \
  --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --concurrency=2
```

## What's here

- `package.json` — version pins (Remotion 4.0.290, React 19, TypeScript 5.7.3)
- `tsconfig.json` — JSX transform `react-jsx`, ESNext modules
- `remotion.config.ts` — 1080×1080 @ 24fps, 30s duration
- `src/index.ts` — entry that registers the Remotion root
- `src/Root.tsx` — `<Composition id="Trailer" ... />`

## What you need to add

- `src/Trailer.tsx` — timeline with `<Sequence>` blocks per scene
- `src/Scenes.tsx` — your scene components (one per shot)

See the `hyperframes` skill at `~/.hermes/skills/creative/hyperframes/references/remotion-quickstart.md`
for the full pattern (FilmFX layer, scene wrappers, ASCII overlay recipe, etc.).