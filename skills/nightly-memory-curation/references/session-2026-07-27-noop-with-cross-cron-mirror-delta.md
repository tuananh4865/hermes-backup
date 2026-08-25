# No-op Pass with Cross-Cron Mirror Delta — 2026-07-27 02:00

## Context

Tuấn Anh's setup fires `memory-curator` cron at 02:00 nightly. The 2026-07-26 02:00 curator run completed normally (2 concept pages, 1 entity lesson update, 1 catalog update, full mirror). The 2026-07-27 02:00 curator woke up needing to decide: re-curate (nothing to curate — 0 sessions in 24h) OR detect no-op.

The 2026-07-26 06:00 `daily-ingest` cron (a DIFFERENT cron job, different profile) appended entries to `wiki/log.md` + `wiki/index.md` AFTER the 2026-07-26 02:00 curator had mirrored both files to vault. This created a 4h mirror delta that the original noop protocol (06-24) would have missed because:

- `find ~/.hermes/sessions -newer log.md` = 0 files (correct: no new sessions)
- `find raw/transcripts/2026-07-27/` = 0 files (correct: no new transcripts)
- BUT vault `log.md` (36198B at 26/07 02:05) ≠ source `log.md` (36567B at 26/07 06:00)

The naive noop decision tree (sessions=0 + transcripts=0 → noop) would have walked away without catching the cross-cron mirror delta.

## What the enhanced noop protocol (L68) detected

| Check | Result |
|-------|--------|
| `find ~/.hermes/sessions -newermt "2026-07-26 02:05"` | 0 files |
| `find /Volumes/Storage-1/Hermes/wiki/raw -newermt "2026-07-26 02:05"` | 0 files |
| `stat -f "%Sm %z" $WIKI/log.md` vs vault | source 26/07 06:00 36567B ≠ vault 26/07 02:05 36198B (delta = 4h) |
| `stat -f "%Sm %z" $WIKI/index.md` vs vault | source 26/07 02:05 23547B == vault 26/07 02:05 23547B (in sync) |
| `stat -f "%Sm %z" $WIKI/entities/learned-about-tuananh.md` vs vault | in sync (1721 lines) |

→ Caught a single-file mirror delta on `log.md`. Re-classified as **gap-fill with cross-cron root cause**.

## What the noop protocol did

1. **Verified "0 new sessions"** with explicit evidence: `find ~/.hermes/sessions -name "*.jsonl" -newermt "2026-07-26 02:05" | wc -l` = 0.
2. **Ran 3-file cross-cron mirror delta check** (L69): caught `log.md` 4h behind vault due to `daily-ingest` cron 26/07 06:00.
3. **Sequential mirror recovery**: `sleep 5 + cp -f $WIKI/log.md $VAULT/log.md` → size 36198B → 36567B; `sleep 3 + cp -f $WIKI/index.md $VAULT/index.md` → size 23547B unchanged; verified via `diff -q` returning empty.
4. **L-number collision check (L70)** before adding new lesson: `grep -oE "L[0-9]+" learned-about-tuananh.md | sort -un | tail` → max existing = L67. Picked L68 for the noop protocol lesson.
5. **Wrote minimal no-op log entry** to `wiki/log.md` with evidence block (sessions=0, mirror delta=4h, root cause=daily-ingest cross-cron write, recovery=catch-up mirror, verification=diff -q empty).
6. **Added L68 lesson** to `learned-about-tuananh.md` (1721 → 1724 lines) describing the no-op protocol.
7. **Final mirror**: 3 files (log.md, index.md, learned-about-tuananh.md) — all verified byte-identical via `diff -q` (size-match + no output).

## Key learnings encoded (L68, L69, L70)

- **L68 — No-op days require explicit protocol, not silent skip.** A 2-line "no-op" log entry without evidence is a documentation lie. The 5-step protocol (verify 0 new → check cross-cron delta → catch-up mirror if stale → write evidence block → L-collision check) produces verifiable output even when synthesis is not needed.
- **L69 — Cross-cron mirror delta is a 5th gap-fill failure mode.** Beyond (a) skip-always-mirror, (b) single-file-staleness, (c) scope-bounded-to-always-mirror, (d) set-diff-not-count — the new mode is: another cron writes to source wiki AFTER memory-curator mirrored. The naive "0 new sessions → noop" decision tree misses this. Always run the 3-file mtime comparison in Step 0 BEFORE deciding noop.
- **L70 — L-number collision check is mandatory.** Before proposing L-N in a curator log entry or anti-pattern, `grep -oE "L[0-9]+" learned-about-tuananh.md | sort -un | tail` to find max. The 07-27 run initially assigned L65 → found L65 taken (workflow batch scalability from 25/07) → renumbered to L66 → found L66 taken (lặp câu bug from 25/07) → renumbered to L67 → found L67 taken (Mode B duration exception) → final L68. The collision-and-renumber cycle cost 2 extra patches.

## Reusable shell snippet

```bash
# Cross-cron mirror delta check (Step 0.6, mandatory in noop)
for f in log.md learned-about-tuananh.md index.md; do
  src="/Volumes/Storage-1/Hermes/wiki/$f"
  [ "$f" = "learned-about-tuananh.md" ] && src="/Volumes/Storage-1/Hermes/wiki/entities/$f"
  dst="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/$f"
  src_m=$(stat -f "%m" "$src" 2>/dev/null || echo 0)
  dst_m=$(stat -f "%m" "$dst" 2>/dev/null || echo 0)
  if [ "$dst_m" -lt "$src_m" ]; then
    echo "STALE: $f is $((src_m - dst_m))s behind"
    # → catch-up mirror required
  fi
done

# L-number collision check (mandatory before writing L-N)
grep -oE "L[0-9]+" /Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md | sort -un | tail -5
```

## Why this complements session-2026-06-24-noop.md

The 06-24 reference covers the original noop protocol (state verification + log + mirror). The 07-27 reference EXTENDS it with the cross-cron mirror delta check (L69) + the L-number collision protocol (L70). Future curators should read BOTH references when encountering a noop day — the 06-24 covers the "no synthesis needed" case, the 07-27 covers the "no synthesis BUT vault may still be stale" case.

## Verified

- Mirror catch-up: log.md 36198B → 36567B, index.md unchanged, learned-about-tuananh.md 116512B → 117146B (after L68 addition)
- All 3 files byte-identical via `diff -q` returning empty
- L-number L68 confirmed unique in `learned-about-tuananh.md` (max existing before addition was L67)
- Vault iCloud state in sync with source — Obsidian graph view will see same nodes as last curator run