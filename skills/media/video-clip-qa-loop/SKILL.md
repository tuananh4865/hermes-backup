---
name: video-clip-qa-loop
description: Loop video clip QA until all gates pass.
version: 0.1.0
author: Hermes
platforms: [macos]
metadata:
  hermes:
    tags: [Video, QA, Loop, TikTok, FFMPEG]
---

# Video Clip QA Loop

Loop-driven QA for rendered video clips. Runs automated verification (duration, resolution, audio specs, transcript quality) against a goal checklist, fixes issues, re-renders, and re-verifies until the file is publish-ready. Built for TikTok specs (1080x1920 @ 44100Hz) but works for any video format.

## When to Use

- After rendering a video clip, before publishing.
- When user says "verify", "check file", "QA loop", "pass the goal", "đạt goal chưa".
- When previous render had known issues (filler, loops, hangs, wrong duration).
- When you have an `audio.json` from Whisper and a `keeps.json` describing source segments.

## Prerequisites

- Rendered `.mp4` file at known path.
- Source `audio.json` from Whisper with segment timestamps.
- `keeps.json` listing `(start, end)` pairs as `[[s, e], ...]`.
- `ffmpeg` and `ffprobe` on PATH (macOS: `brew install ffmpeg`).
- `scripts/verify_clip.py` (ships with the `tiktok-video-editor` skill) in working directory.

## How to Run

Invoke through the `terminal` tool after every render:

```
python3 scripts/verify_clip.py <audio.json> <keeps.json> <render.mp4>
```

Exit code 0 = file passes all checks. Exit code 1 = issues found, listed in stdout.

## Quick Reference

- `python3 scripts/verify_clip.py audio.json keeps.json out.mp4` - run full QA
- `ffprobe -show_entries format=duration out.mp4` - check duration only
- `ffprobe -show_entries stream=width,height,sample_rate out.mp4` - check spec
- `ls -la out.mp4` - verify file exists and size > 0
- Exit 0 = pass, exit 1 = fail with issues

## Procedure

1. **Confirm artifacts exist.** Use `terminal` to run `ls -la <render.mp4>` and `ls -la <audio.json> <keeps.json>`. Stop if any missing.
2. **Render once** (if not already): use `terminal` with the `ffmpeg` command from the `tiktok-video-editor` skill. Spec is `-c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -movflags +faststart`, scaled to `1080:1920`.
3. **Run the verifier.** Invoke `terminal` with `python3 scripts/verify_clip.py <audio.json> <keeps.json> <render.mp4>`. Capture exit code.
4. **Read the report.** If exit 0, file passes - ship it. If exit 1, the report lists issues grouped by type: `FILLER`, `UM_O`, `TREO`, `LAP_NGHIA`, `HOOK_LAP`, plus TikTok spec violations (duration out of range, wrong resolution, wrong sample rate).
5. **Diagnose root cause** for each issue:
   - `FILLER`/`UM_O`: a filler word (ơ, ờ, ừm, ừ, ó, à, á) is isolated or at start/end of a kept segment. Fix: tighten the keep boundary or drop the segment.
   - `TREO`: a kept segment is 3-8 filler-only words with no predicate. Fix: drop it or merge with adjacent keep.
   - `LAP_NGHIA`: two adjacent kept segments share 2+ leading words. Fix: drop one, merge them, or split one keep between them.
   - `HOOK_LAP`: two distant kept segments share 3+ leading words. Fix: drop one or rephrase via tighter boundaries.
   - Duration > 180s: trim least-essential keeps first.
6. **Edit `keeps.json`** via `patch` or `write_file` to remove or merge the offending keeps.
7. **Re-render.** Re-run the ffmpeg command from step 2.
8. **Re-verify.** Jump back to step 3. Loop until exit 0.
9. **Ship.** Final render is the publish-ready file. Rename with descriptive kebab-case slug per the `tiktok-video-editor` naming convention.

## Pitfalls

- **Whisper verify lại không chính xác.** Re-running Whisper on the rendered file merges nearby segments and produces false `TREO` flags (>20 words). Always verify from the original `audio.json`, not from a re-transcription.
- **Hook lặp xa cũng tính.** The verifier flags hook repeats within 15 segments of each other. Two keeps separated by 3 minutes can still be flagged.
- **Duration gate is strict.** 180s ceiling is hard. Trimming duration often solves multiple LẶP/HOOK issues at once if the trimmed keeps were filler or transitional.
- **CTA hard-sell is allowed.** Verifier does NOT flag CTA phrases like "bấm link mua" - keep them.
- **"đó" và "thì" are NOT filler.** They have grammatical roles (pronoun, conditional connector). Don't strip them.
- **3-strike rule.** If the loop fails 3 times with the same issue class, stop and surface the problem to the user rather than chasing.

## Verification

One-shot proof the loop converged:

```
python3 scripts/verify_clip.py audio.json keeps.json out.mp4 && echo "PUBLISH READY"
```

If the loop terminates with this command printing `PUBLISH READY` on stdout, the file passes every check and is safe to ship.