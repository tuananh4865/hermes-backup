# No-op Idempotency Pass — 2026-06-24 03:01

## Context

Tuấn Anh's setup fires `memory-curator` cron twice nightly (02:00 + 03:01 local). The 02:00 run already completed full curation of June 22-23 sessions (11 watchdog stubs filled, 4 new concept pages, 1 entity page update, 1 comparison page update, iCloud mirror synced). The 03:01 cron woke up needing to decide: re-curate (waste of work + duplicates) OR detect no-op and exit cleanly.

## What the skill detected

| Check | Result |
|-------|--------|
| `find raw/transcripts/2026-06-24/ -type f` | 0 files |
| `find ~/.hermes/sessions -newer wiki/log.md` | 0 files (last user session 2026-06-23 16:49) |
| `wiki/log.md` last entry timestamp | 2026-06-24 02:00 |
| `watchdog_state.json last_run` | 2026-06-24T03:00:00 |

→ No-op pass triggered.

## What the no-op protocol did

1. **Verified state** — md5-checked the 7 files the 02:00 run had modified:
   - `entities/learned-about-tuananh.md`
   - `comparisons/tuananh-system-wide-mandates.md`
   - `concepts/active-checklist-pattern.md`
   - `concepts/one-person-company-phase-01-deep-research.md`
   - `concepts/city-drift-game-spec.md`
   - `concepts/fabricated-completion-rule.md`
   - `concepts/over-engineering-trap.md`
2. **Verified iCloud mirror** — `ls "$VAULT/concepts/"` confirmed all 5 new concept pages present.
3. **Appended no-op log entry** to `wiki/log.md` (1998 → 2024 lines).
4. **Mirrored updated log.md** to iCloud vault.
5. **Updated `watchdog_state.json`** with `no_op_runs: ["2026-06-24T03:01:00"]`.
6. **Returned structured no-op report** to cron delivery target.

## Key learnings encoded in skill

- **Idempotency check** is now step 0 in the skill workflow (runs BEFORE step 1).
- The check uses `find ... -newer wiki/log.md` as a cheap proxy for "anything new since last curator ran." log.md is the right sentinel because the previous curator pass always touches it.
- **No-op is correct behavior**, not failure. The skill explicitly forbids fabricating work to look productive.
- **No-op must still log** — Tuấn Anh's cron monitoring expects every firing to leave a trace.
- **`watchdog_state.json`** has a `no_op_runs` array for telemetry — useful for spotting cron misfires (e.g. if ALL runs are no-ops for 3 days, something is wrong with session ingestion).

## Reusable shell snippet

```bash
# Idempotency check at start of curator cron
NEW_TRANSCRIPTS=$(find /Volumes/Storage-1/Hermes/wiki/raw/transcripts/$(date +%Y-%m-%d) -type f 2>/dev/null | wc -l | tr -d ' ')
NEW_SESSIONS=$(find ~/.hermes/sessions -type f -newer /Volumes/Storage-1/Hermes/wiki/log.md 2>/dev/null | grep -v watchdog | wc -l | tr -d ' ')

if [ "$NEW_TRANSCRIPTS" = "0" ] && [ "$NEW_SESSIONS" = "0" ]; then
  echo "No-op: prior curator pass consumed all material."
  # → Run no-op protocol (verify state, log, exit)
fi
```

## Future improvement opportunity

The `last_run` field in `watchdog_state.json` could be more granular — record `last_real_run` (last non-no-op pass) separately from `last_run` (any pass). Then the report could show "days since last real curation" as a health metric. Not blocking; can be added when telemetry needs grow.