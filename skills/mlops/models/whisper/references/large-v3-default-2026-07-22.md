---
title: Whisper large-v3 default rollout — 2026-07-22
created: 2026-07-22
type: reference
tags: [whisper, large-v3, vietnamese, mlx, auto-fallback, technical-terms]
parent_skill: mlops/models/whisper
status: active
---

# Whisper large-v3 default rollout (2026-07-22)

> **Source**: Session 2026-07-22 — switched `~/.hermes/scripts/whisper-transcribe` default from medium to large-v3 after side-by-side benchmark on `clip_0036_V9_115s_FINAL_LENS_MACRO.mp4`. Wrapper `whisper-transcribe` was rewritten to default large-v3 with auto-fallback to medium on loop detection.

## Why the flip

Earlier verdict (2026-07-05 body-mist Dubai clip) said medium-mlx wins for Vietnamese TikTok editing. The 2026-07-22 clip-0036 retest reversed that for technical-term-heavy review clips:

| Term | medium-mlx | large-v3-mlx |
|------|-----------|--------------|
| "Pocket 3" | ❌ "pocket bar" | ❌ "pocket bar" (both hallucinate brand — known) |
| "CNC" | ❌ missed | ✅ caught (1×) |
| "focus" | ❌ "phó kết" × 2 | ✅ exact × 3 |
| "3cm" / "15cm" | ✅ / ✅ | ✅ / ✅ |
| "đặc thùng" hallucinate | ⚠️ present | cleaner (still 1× "đặc thù") |
| Latency (115s audio) | 19.3s | 36.0s |
| Segments produced | **13** clean grouping | 39 over-segmented |

User verdict: "chuyển sang dùng large v3 mặc định đi vì nó transcript chuẩn nhất!!!" — accepted the 4× slower latency as the cost of technical-term accuracy on review clips.

## Wrapper behavior

`~/.hermes/scripts/whisper-transcribe` (rewritten 2026-07-22):

1. Runs `mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi --output-format all --word-timestamps True "$INPUT"`.
2. After Whisper returns, Python auto-detector scans the output `.txt` for any 5-word phrase appearing **≥5 times** (the legacy 2026-07-02 DRIVE2 loop signature).
3. On loop detection: bad transcript backed up as `<basename>_large_v3_LOOP.txt`, then re-runs with `mlx-community/whisper-medium-mlx`.
4. On clean exit: prints "✅ Transcript clean (no loop detected)" and ships 5-format output.

Env override: `MLX_WHISPER_MODEL=mlx-community/whisper-medium-mlx whisper-transcribe input.mp4` for clips known to be loop-sensitive.

Backup of pre-change medium-default wrapper: `~/.hermes/scripts/whisper-transcribe.bak-medium-2026-07-22`.

## Verification matrix (this session)

| Clip | Audio | Loop detected | Fallback fired | Final output |
|------|-------|--------------:|----------------|--------------|
| `clip_0036_v9.wav` | 114.8s | 0 | no | large-v3 clean (CNC/focus/3cm caught) |
| `clip_0036_v9.wav` + 20s trailing silence → 134s | sine-style pre-pend | 0 | no | large-v3 clean (extra "Các bạn có thể nhận thêm những bài hát" boundary segment added) |
| `loop_5x.wav` (sine wave, 10s) | 10s | 0 | no | large-v3 returned single hallucinate line "Hãy subscribe cho kênh La La School..." (silence + edge content) |

→ Fallback did NOT trigger on either real clip. Auto-fallback armed but inert in this test window. **Do not assume fallback is broken — it simply never received a triggering loop in this session.**

## Known caveats that survive the flip

1. **Brand hallucinate "Pocket 3" → "pocket bar"** persists in large-v3 (verified on clip 0036 v9). Fallback to medium also produces "pocket bar". Both wrong; user manually corrects in transcript before voice replacement workflow (PITFALL #70 NAMMINH edition).
2. **"đặc thù" / "đặc thùng" / "đặc biệt" cluster** — large-v3 cleaner but still outputs "đặc thù" instead of "đặc biệt". Whisper treats speaker's phrasing literally.
3. **fps > 1 in video mode** worsens hallucinate per video test 22/07 — large-v3 at fps=2 on clip_0031 generated "BOTAF"/"gaming controller" instead of QCY/POCKETBAR. Stay at fps=1 for video workflow.

## Related

- `references/mlx-whisper-apple-silicon.md` — original 2026-07-05 benchmark (medium vs large-v3-turbo, NOT large-v3). The 2026-07-22 update supersedes the verdict for technical-term-heavy Vietnamese content.
- SKILL.md `Pitfall #3` — legacy 2026-07-02 loop risk, now mitigated by wrapper (see updated text).
- `SOUL.md MODEL REGISTRY — Whisper Transcription DEFAULT large-v3` — system-wide default entry.
- Test artifacts: `/Volumes/Storage-1/Hermes/scratch/whisper-compare-0036/` (3 model outputs SRT/TXT/JSON + `README-comparison-results.md`).
- Skill `tiktok-video-editor` PITFALL #71 — primary workflow carries the macro context.
