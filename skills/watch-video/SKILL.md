---
name: watch-video
description: Watch a video (URL or local file). Downloads with yt-dlp, extracts auto-scaled frames with ffmpeg, transcribes via LOCAL mlx_whisper (offline, free, Apple Silicon) — no API key needed. Drops frame paths + transcript so the agent can answer questions about what's in the video.
version: 1.1.0
author: bradautomates (adapted by Tuấn Anh for Hermes, 27/07/2026)
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [video, transcript, frames, ffmpeg, yt-dlp, mlx-whisper, local, apple-silicon, offline]
    related_skills: [tiktok-video-editor, tiktok-transcript-pipeline, analyze-transcript]
    upstream: [bradautomates/claude-video v0.2.0]
---

# watch-video

Local-first video understanding for Hermes. A Python pipeline that downloads (or reads) a video, extracts frames, transcribes audio via `mlx-community/whisper-large-v3-mlx` (Apple Silicon, offline), and prints frame paths + a timestamped transcript so the model can `Read` the JPEGs and combine visuals with speech.

> Adapted from `bradautomates/claude-video` v0.2.0 — same pipeline shape, `whisper.py` swapped to local mlx_whisper (no Groq/OpenAI API key, no internet, no per-minute cost). Path resolution is `~/.hermes/skills/watch-video/` (Hermes-style absolute paths, not `${CLAUDE_SKILL_DIR}`).

## When to use

- User pastes a YouTube / Vimeo / X / TikTok / Twitch URL and asks about it.
- User points at a local video (`/Volumes/Storage-1/Pocket3/...mp4`, recordings, downloaded clips) and asks what's in it.
- User types `/watch-video <url-or-path> [question]`.
- Quick analysis: "summary", "what happens at 2:00", "key moments", "extract script".

## How to invoke

```bash
WATCH_DIR="$HOME/.hermes/skills/watch-video"
python3 "$WATCH_DIR/scripts/watch.py" "<source>" [--detail ...] [--start ...] [--end ...] [--timestamps ...] [--out-dir DIR]
```

### Resolve `WATCH_DIR` first

`WATCH_DIR` is the directory containing `SKILL.md` you just Read → always `~/.hermes/skills/watch-video` (absolute, harness-agnostic). Do NOT rely on env vars. Guard once at the start of a `/watch-video` run:

```bash
WATCH_DIR="$HOME/.hermes/skills/watch-video"
[ -f "$WATCH_DIR/scripts/watch.py" ] || { echo "watch-video not installed at $WATCH_DIR"; exit 1; }
```

### Sources

| Source | What happens |
|---|---|
| `https://youtu.be/abc` (or any yt-dlp site) | yt-dlp downloads; native captions used if present |
| `/path/to/file.mp4` / `.mov` / `.mkv` / `.webm` | Read directly; ffmpeg extracts audio |

### Optional flags

- `--detail transcript|efficient|balanced|token-burner` — fidelity/speed dial (default `balanced`)
  - `transcript` → no frames, transcript only (skips download if captions exist)
  - `efficient` → keyframes only, cap 50
  - `balanced` → scene-aware, cap 100
  - `token-burner` → scene-aware, uncapped
- `--start T` / `--end T` — focus on a section (`SS`, `MM:SS`, `HH:MM:SS`); auto-denser frames
- `--timestamps T1,T2,…` — pin frame at exact timestamp (e.g. transcript-cued "look here")
- `--max-frames N` — override cap
- `--resolution W` — frame width (default 512; bump to 1024 for reading on-screen text)
- `--fps F` — override auto-fps (clamped to 2 fps)
- `--out-dir DIR` — work dir (default: `$TMPDIR/watch-XXXXXX`)
- `--no-whisper` — disable local transcription (frames-only if no native captions)
- `--no-dedup` — keep near-duplicate frames (default: drop visually similar consecutive frames)

### After invocation

The script prints:

1. A markdown **report header** with duration, resolution, frame count, transcript status, file size.
2. List of **`/path/to/frame_NNNN.jpg`** entries with absolute timestamps.
3. **Transcript** as a code block with `[MM:SS] text` segments.

Then:

```bash
# Read all frames in parallel (the model renders JPEGs natively)
for f in /path/to/work/frames/*.jpg; do Read "$f"; done

# Synthesize answer from frames + transcript
```

## Recommended limits

- **Best accuracy: videos under 10 minutes.** Frame coverage scales inversely with duration.
- **Rate cap: 2 fps.**
- **Frame ceiling per detail mode:** `transcript`=0, `efficient`=50, `balanced`=100, `token-burner`=∞.
- **Budget by duration (full-video):** ≤30s → 12-30f, 30s-1min → 40, 1-3min → 60, 3-10min → 80, >10min → cap.

## Detail and frames

| Mode | Source | Cap | When |
|---|---|---:|---|
| `transcript` | captions (or local Whisper), 0 frames | — | Save tokens, just need speech |
| `efficient` | keyframes (`ffmpeg -skip_frame nokey`) | 50 | Quick scan |
| `balanced` (default) | scene-aware ffmpeg; uniform fallback | 100 | Most questions |
| `token-burner` | scene-aware uncapped | ∞ | Full fidelity on long videos |

## Transcription

**Local-first — no key, no internet.**

- **mlx_whisper** (`mlx-community/whisper-large-v3-mlx`) on Apple Silicon. ~0.3x real-time, 36 segments for a 73s clip in ~16s on M-series.
- Override model: `WATCH_WHISPER_MODEL=mlx-community/whisper-medium-mlx` env var.
- Override language: `WATCH_WHISPER_LANGUAGE=en` (default `vi`).
- Long-form chunking (e.g. >30min): set `WATCH_WHISPER_CHUNK_SECONDS=600` to chunk into ≤600s pieces.
- `--no-whisper` skips entirely.

If you have captions from yt-dlp, those are used first (free, instant).

## Fallback chain order

```
URL? → yt-dlp fetches captions + downloads (audio only if --detail transcript)
  ├─ captions found → use them, skip Whisper
  └─ no captions + video has audio → extract audio → mlx_whisper
  └─ no captions + no audio → frames-only
  └─ --no-whisper → frames-only (skip Whisper even if needed)
```

## Token efficiency

- 60 frames at 512px wide ≈ 35-50k image tokens.
- Transcript is cheap (~1-3k tokens for a 10min video).
- Bump `--resolution 1024` only for legible on-screen text (4x tokens per frame).

## Failure modes

- **Setup preflight failed** → `python3 ~/.hermes/skills/watch-video/scripts/setup.py` (auto-installs ffmpeg/yt-dlp via brew, scaffolds `~/.config/watch/.env`).
- **No transcript available** → captions missing AND mlx_whisper failed. Check `~/.hermes/scripts/whisper-transcribe` works on a known audio sample first.
- **Download fails** → yt-dlp prints to stderr; if login/region-locked, tell the user plainly.
- **Long-video warning** → re-run with `--start`/`--end` focused instead of full sparse scan.

## Pitfalls (verified 27/07/2026 on Pocket3 clips)

### P1: `extract_audio` must match `audio_out` suffix (silent transcript failure)

`watch.py` hardcodes `work / "audio.mp3"` as the second arg to `transcribe_video`. If your local `extract_audio` implementation hardcodes `.wav` + `pcm_s16le` codec, ffmpeg errors out with `[mp3 @ 0x…] Invalid audio stream. Exactly one MP3 audio stream is required.` `watch.py`'s `try/except SystemExit` then swallows the error and silently reports "no transcript available" — no exception surface to the user.

**Fix:** `extract_audio` picks codec from `out_path.suffix` — `.wav` → `pcm_s16le`, `.mp3` → `libmp3lame 64k`. Same module accepts both. The local `whisper.py` here does this; do not regress it back to a hardcoded codec.

### P2: Talking-head clips → scene-detect yields 0–3 candidates → uniform fallback

`ffmpeg scene detection` (the `select=gt(scene,...)` filter behind `balanced` mode) finds few or no scene changes on a single-camera talking-head clip. The report header will say e.g. `Frames: 60 selected from 3 candidates (uniform with uniform fallback, full range, budget 60, cap 100)`. This is **expected behavior**, not a bug. Uniform sampling actually gives better coverage for talking-head than scene-detect would, because every second has roughly equal visual signal.

**Heuristic:** if a video is mostly a static camera + person talking, expect the `uniform with uniform fallback` line in the report. If you need to capture a specific deictic gesture ("look here at this"), use `--timestamps T1,T2,…` instead of relying on scene-detect.

### P3: `--whisper groq|openai` is a no-op in this fork

The flag is accepted for upstream compatibility but the local `whisper.py` ignores it. The local backend is always used. Don't waste a turn asking the user which backend — there is no choice in this fork.

## Bundled scripts

- `scripts/watch.py` — entry point (download → frames → transcript → markdown report)
- `scripts/download.py` — yt-dlp wrapper
- `scripts/frames.py` — ffmpeg scene/keyframe extractor
- `scripts/transcribe.py` — VTT parser + range filter
- `scripts/whisper.py` — **Patched**: local mlx_whisper (replaces upstream Groq/OpenAI module)
- `scripts/setup.py` — preflight + installer
- `scripts/config.py` — `~/.config/watch/.env` reader

## Reference

- `references/port-session-claude-video-2026-07-27.md` — full port log: what changed, the 3 pitfalls hit during the port (extension mismatch, `load_api_key` shim shape, mlx_whisper's real format requirements), and a generalized "API→local port" pattern for future skill forks.

## Security & Permissions

**What this skill does:**
- Runs `yt-dlp` locally (public data; request goes directly to source host)
- Runs `ffmpeg`/`ffprobe` locally to extract frames + audio
- Runs **local** `mlx_whisper` (Apple Silicon GPU/MPS) — no data leaves the machine
- Writes working files to `$TMPDIR` (or `--out-dir`) for the model to `Read`
- Reads/creates `~/.config/watch/.env` (mode `0600`) for watch preferences only (no API keys in local mode)

**What this skill does NOT do:**
- Does NOT upload video or audio to any third-party API (unlike upstream Groq path)
- Does NOT require API keys, accounts, or internet connectivity (once `yt-dlp`/`ffmpeg`/`mlx_whisper` are installed)
- Does NOT access any platform account (no login, no cookies)
- Does NOT persist anything outside `$TMPDIR` (work dir) and `~/.config/watch/.env`

## Differences from upstream `bradautomates/claude-video`

| Feature | Upstream | Hermes fork |
|---|---|---|
| Whisper backend | Groq API / OpenAI API (key required) | **mlx_whisper local** (no key, offline) |
| Audio intermediate | mp3 (64 kbps) | mp3 OR wav (codec follows `audio_out` suffix) |
| Long-form chunks | forced (>24 MB upload cap) | opt-in via `WATCH_WHISPER_CHUNK_SECONDS` |
| Path resolution | `${CLAUDE_SKILL_DIR}` (Claude Code only) | `$HOME/.hermes/skills/watch-video` (absolute) |
| Required env | `GROQ_API_KEY` or `OPENAI_API_KEY` | none (uses already-installed mlx_whisper) |
| `--whisper` flag | `groq \| openai` | no-op (always local); flag accepted for compatibility |

## Verify before using

```bash
# 1. Module imports
python3 -c "import sys; sys.path.insert(0,'$HOME/.hermes/skills/watch-video/scripts'); import whisper; print('ok')"

# 2. Binaries present
which ffmpeg ffprobe yt-dlp

# 3. mlx_whisper installed
python3 -c "import mlx_whisper; print(mlx_whisper.__file__)"

# 4. End-to-end test on a short clip (≤5 min)
python3 ~/.hermes/skills/watch-video/scripts/watch.py /path/to/short.mp4 --detail balanced --out-dir /tmp/wv-test
ls /tmp/wv-test/frames/ | head -10     # → frames/*.jpg
cat /tmp/wv-test/report.md             # → transcript
```
