# References index — tiktok-verify-protocol

## Pitfall files (semantic pitfalls — load khi cần)

- **`pitfall-25-technical-spec-verify.md`** — PITFALL #25: Technical/Encoding 7-layer verify với tool thật (codec/duration/keyframes/visual integrity). Dùng khi user yêu cầu "verify spec kỹ thuật", KHÔNG cần whisper.
- **`pitfall-21jul-clip_0036-product-showcase.md`** — PITFALL cho product-showcase clip workflow.
- **`pitfall-anchor-lap-false-positive-2026-07-14.md`** — Anchor-lap heuristic false positive traps.
- **`pitfall-strict-matcher-blind-spot-2026-07-13.md`** — Strict matcher blind spots.
- **`pitfall-keep-boundaries-match-whisper-segments-2026-07-14.md`** — Keep boundaries phải khớp whisper segments.
- **`pitfall-manual-vs-subagent-cross-check-2026-07-18.md`** — Manual vs subagent cross-check workflow.
- **`pitfall-verify-2-layers-required-2026-07-14.md`** — Tối thiểu 2 layers verify.
- **`pitfall-success-pattern-clip-0731-v3-v5-fix-2026-07-14.md`** — Success pattern cho clip_0731 V3-V5 fix.
- **`pitfall-motion-verify-dark-source-2026-07-18.md`** — Motion verify trên dark source clips.

## Lesson files (session-specific — chronological)

- **`lesson-2026-07-21-verify-7-clip-batch-dji-0029-0038.md`** — Verify batch 7 clip DJI Pocket 3 (0029-0038 V1). PITFALL #23 (Layer 5 speed 1.3x literal criteria sai cho Mode B) + PITFALL #24 (verify-context filename mismatch).
- **`lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md`** — Verify clip 0038 V2 với `verify_clip_full.py` 7-layer transcript-level. PITFALL #26 (GOP/keyframe csv=p=0 empty) + #27 (lavfi stderr pattern với -v error) + #28 (L4 false-start re-whisper protocol) + #29 (L3 anchor-lap gap=0 = VN rhetoric) + #30 (FILLER `á` clip-end decision matrix).
- **`lesson-2026-07-21-verify-7-layer-L7-cau-treo-clip-0030.md`** — Verify clip 0030 L7 câu treo detection.
- **`lesson-2026-07-18-verify-clip-0007.md`** — Verify clip 0007 (parallel-reason rhetoric pitfall).
- **`lesson-2026-07-18-verify-clip-0004.md`** — Verify clip 0004.
- **`lesson-2026-07-18-verify-never-skip-clip-0003.md`** — Never-skip lesson từ clip 0003.
- **`lesson-source-natural-anchor-lap-pattern-2026-07-16.md`** — Source natural anchor-lap pattern.
- **`lesson-source-natural-anchor-lap-batch-3-3-2026-07-16.md`** — Batch 3-3 anchor-lap pattern.
- **`session-2026-07-11-step8-verify-fail.md`** — Step 8 verify fail session log.
- **`session-2026-07-12-verify-clip-tool.md`** — Verify clip tool session log.
- **`session-2026-07-12-system-wide-rule.md`** — System-wide rule session log.

## Recipe files (workflow templates)

- **`6-layer-clip-verify-recipe.md`** — 6-layer clip verify recipe (tổng quát, không pitfall-specific).

## Templates

- **`templates/keeps.json.template`** — Starter template cho keeps.json file.

## Scripts

- **`scripts/verify_clip.py`** — Single-clip verify (transcript-level, 5-dim strict).
- **`scripts/verify_clip_full.py`** — One-shot 7-layer verify (spec + 5-dim + anchor-lap + false-start + RMS + motion).
- **`scripts/check_anchor_lap.py`** — Standalone anchor-lap checker.
- **`scripts/verify_motion.py`** — Standalone motion verify (pixel diff).
- **`scripts/verify_with_keep_awareness.py`** — Verify với keep_plan awareness.

## Khi nào load reference nào?

| Task | Load file |
|---|---|
| User "verify clip spec kỹ thuật" / "check encoding integrity" | `pitfall-25-technical-spec-verify.md` |
| User "verify clip 7 layers" (transcript-level) | `lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md` |
| User "verify batch N clips" | `lesson-2026-07-21-verify-7-clip-batch-dji-0029-0038.md` |
| User flag "anchor-lap" issue | `pitfall-anchor-lap-false-positive-2026-07-14.md` + `lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md` (PITFALL #29) |
| User flag "false-start" candidate | `lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md` (PITFALL #28 re-whisper protocol) |
| User flag "GOP/keyframe" extraction issue | `lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md` (PITFALL #26) |
| User flag lavfi filter silent output | `lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md` (PITFALL #27) |
| User flag FILLER `á` ở clip end | `lesson-2026-07-21-verify-clip-0038-v2-7layer-full.md` (PITFALL #30) |