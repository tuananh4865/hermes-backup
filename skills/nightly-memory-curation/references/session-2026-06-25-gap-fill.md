# Gap-Fill Follow-up Pass — 2026-06-25 03:02

## Context

Tuấn Anh's setup fires `memory-curator` cron twice nightly (02:00 + 03:00 local). The 02:00 main pass already completed full curation of June 24 sessions (5 watchdog stubs filled, 1 new concept page `telegram-video-20mb-limit.md`, 1 entity page update, iCloud mirror for entities + concepts). The 03:02 cron woke up needing to decide: re-curate (waste of work + duplicates), run noop (would miss real gaps), or detect gap-fill mode (the actual correct answer).

## Why noop was WRONG here

Standard noop check: `find ... -newer wiki/log.md` returns 0 files → no new content. Result on this run: TRUE (no new transcripts, no new sessions). A strict noop would have exited cleanly. But:

1. **Previous pass (02:00) DID NOT mirror `log.md`** to iCloud. iCloud `log.md` last modified 2026-06-24 03:02 (yesterday). Wiki `log.md` last modified 2026-06-25 02:06. **1-day mirror lag.**
2. **Previous pass (02:00) flagged pending work** ("Patch `~/.hermes/skills/media/telegram-video-analysis/SKILL.md` to add 20MB cap as Pitfall #N") that no mechanism auto-resolves. Strict noop leaves pending work hanging.

So noop = correct surface behavior, wrong outcome.

## Detection signals (now codified in skill Step 0)

```bash
# Signal 1: Pending work section in last log entry
PENDING_WORK=$(grep -c "^### Pending work" /Volumes/Storage-1/Hermes/wiki/log.md | tail -1)

# Signal 2: iCloud log.md mtime older than wiki log.md mtime
ICLOUD_LOG_MTIME=$(stat -f "%m" "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/log.md" 2>/dev/null || echo 0)
WIKI_LOG_MTIME=$(stat -f "%m" /Volumes/Storage-1/Hermes/wiki/log.md)

if [ "$ICLOUD_LOG_MTIME" -lt "$WIKI_LOG_MTIME" ] || [ "$PENDING_WORK" -gt "0" ]; then
  echo "GAP-FILL MODE TRIGGERED"
fi
```

## Gap-fill protocol (executed in this run)

| Step | Action | Outcome |
|------|--------|---------|
| 1 | Read log.md's "Pending work for next nightly" section | Found 3 items, item #1 was the SKILL.md patch |
| 2 | Patch `~/.hermes/skills/media/telegram-video-analysis/SKILL.md` with Pitfall #34 | DONE: 20MB RECEIVE limit pitfall added |
| 3 | `diff -q` wiki vs iCloud for log.md | Confirmed 1-day lag |
| 4 | `cp` log.md to iCloud vault | DONE |
| 5 | `diff -q` post-mirror to verify byte-identical | PASS |
| 6 | Append new log entry to wiki/log.md describing gap-fill | DONE (66 new lines) |
| 7 | Mirror updated log.md to iCloud again | DONE |

## Pending work status table (mandatory addition to every gap-fill log entry)

| Item | Status | Notes |
|------|--------|-------|
| (item 1 from prev pass) | ✅ DONE | How resolved |
| (item 2 from prev pass) | ⏸️ DEFERRED | Why deferred |
| (item 3 from prev pass) | ⏸️ DEFERRED | Why deferred |

This table closes the loop on previous pass's pending work. Without it, the next noop run can't distinguish "still pending" from "deferred by design."

## Key learnings encoded in skill

1. **Step 0 — Run mode classification** added BEFORE Step 1 (Discover). The 3-mode classifier (main / noop / gap-fill) is now first-class in the skill workflow.
2. **Mirror step now includes `log.md`** + verification via `diff -q`. Log.md is the most-frequently-changed file; mirror it EVERY run.
3. **Two new anti-patterns added**: "Treating noop as the ONLY alternative to main pass" + "Mirror without copying `log.md`".
4. **Pending work loop closure** — every gap-fill log entry MUST end with a "Pending work status table" closing the loop on previous pass's flagged items.
5. **Verification list updated** — adds "log.md mirrored AND byte-identical" check + "Classified run mode at Step 0".

## Reusable shell snippet

```bash
# Full gap-fill detection at start of curator cron
WIKI="/Volumes/Storage-1/Hermes/wiki"
VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain"

NEW_TRANSCRIPTS=$(find "$WIKI/raw/transcripts/$(date +%Y-%m-%d)" -type f 2>/dev/null | wc -l | tr -d ' ')
NEW_SESSIONS=$(find ~/.hermes/sessions -type f -newer "$WIKI/log.md" 2>/dev/null | grep -v watchdog | wc -l | tr -d ' ')

if [ "$NEW_TRANSCRIPTS" = "0" ] && [ "$NEW_SESSIONS" = "0" ]; then
  PENDING=$(grep -c "^### Pending work" "$WIKI/log.md" | tail -1)
  ICLOUD_MTIME=$(stat -f "%m" "$VAULT/log.md" 2>/dev/null || echo 0)
  WIKI_MTIME=$(stat -f "%m" "$WIKI/log.md")
  
  if [ "$ICLOUD_MTIME" -lt "$WIKI_MTIME" ] || [ "$PENDING" -gt "0" ]; then
    echo "GAP-FILL MODE: resolving pending work and mirror gaps"
    # → Run gap-fill protocol (read pending work, resolve, re-mirror log.md, log entry)
  else
    echo "NOOP MODE: prior curator pass consumed all material"
    # → Run no-op protocol
  fi
else
  echo "MAIN PASS MODE: new content since last curator"
  # → Run full 6-step workflow
fi
```

## Future improvement opportunity

Self-verify step in main pass: assert that mirror step completed BEFORE declaring the run done. Currently a failed `cp` to iCloud would only be caught by the NEXT curator run (or never, if cron is broken). Options:
- Inline `diff -q` after each `cp`
- Post-mirror md5 check against expected set
- iCloud-side sentinel file with run timestamp

Recommend inline `diff -q` as the lightest-weight option. Can be added to step 5 of skill workflow.