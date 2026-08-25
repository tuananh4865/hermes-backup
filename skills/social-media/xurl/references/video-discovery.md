# Video File Discovery Pattern

When looking for recently-generated video files (Remotion, render outputs, etc.), check these locations in order:

1. **`/tmp/`** — Remotion and many CLI video tools default to `/tmp/` for output
   - Pattern: `*.mp4`, `*.mov`, etc.
   - Filter by recent timestamp: `find /tmp -name "*.mp4" -newer /reference/file.mp4`
   - Example: `/tmp/google-io-2026-draft.mp4`

2. **`~/Downloads/`** — Browser downloads, Telegram Desktop, etc.

3. **`~/.hermes/`** — Agent output directory

4. **`/var/folders/`** — macOS temporary directories (less predictable)

## Quick probe command
```bash
find /tmp -maxdepth 1 -name "*.mp4" -newer /reference/file 2>/dev/null | head -5
```

## Why /tmp/
- Remotion (React-to-video): writes to `/tmp/` by default unless `--output` is specified
- Short-lived renders often land there before being moved to final destination
- No Spotlight/mdfind indexing → must search directly