# V26: "status=ok" but "last_run=stale" — the missed-tick detection gap

**Discovered:** 2026-06-30 17:02 +07 (orchestrator 30m heartbeat, post-12:00 sweep).
**Complements:** H38 cron-truth (V8 + V15), V23/V24/V25 kanban-DB-false-positive family.
**One-line rule:** `hermes cron list` shows `ok` for the LAST EXECUTION, not the SCHEDULED one. A cron that fired yesterday at 07:00 with `ok` and was supposed to fire today at 07:00 but didn't, still displays `ok` — the system has no built-in "missed-tick" alert.

## The pattern (and why H38's check 2 doesn't catch it)

H38's recipe (Check 2 of `quick-reference-6check.md`) classifies:

| `hermes cron list` | state.md mtime | Verdict |
|---|---|---|
| `Last run: <recent>  ok` | stale or recent | ✅ HEALTHY |
| `Last run: <stale>  error` | any | ❌ REAL FAULT |
| Not in registry | any | ⚠️ IDLE |

The gap: **what about `Last run: <stale>  ok`?** H38 implicitly classes that as "HEALTHY" (the cell only marks `error` as fault). But "stale + ok" is its own failure mode: the job last ran successfully YESTERDAY, and today's scheduled tick never fired. Status `ok` is technically true (the last run was ok) but misleading.

**The exact failure that produced V26** (2026-06-30 17:02 heartbeat):

```
Name:      Hermes Autoresearch Nightly
Schedule:  0 7 * * *
Last run:  2026-06-29T07:04:55  ok            ← yesterday, NOT today (2026-06-30)

Name:      Hermes Agent X Research Daily
Schedule:  30 7 * * *
Last run:  2026-06-29T07:32:21  ok            ← yesterday, NOT today

Name:      Wiki Health Daily
Schedule:  0 4 * * *
Last run:  2026-06-29T04:00:51  ok            ← 36h stale

Name:      Memory Curator Nightly Consolidation
Schedule:  0 2 * * *
Last run:  2026-06-29T02:04:58  ok            ← yesterday, NOT today

Name:      Orchestrator Nightly Reflection
Schedule:  0 23 * * *
Last run:  2026-06-29T23:05:56  ok            ← today 23:00 tick NOT YET MISSED (sweep at 17:02)
```

5 crons missed the 2026-06-30 morning tick (Autoresearch, X Research, Wiki Health, Memory Curator; the Nightly Reflection one is a pre-fire at 17:02 and will be evaluated again at next sweep). ALL show `ok`. None show `error`. The heartbeat must compute staleness against the SCHEDULE, not the last_run.

## Detection recipe

```bash
# Get cron list with schedule + last_run
hermes cron list 2>/dev/null | grep -E "Name:|Schedule:|Last run:" | paste -d'|' - - - | \
  while IFS='|' read -r name_line sched_line run_line; do
    # Extract schedule pattern (e.g. "0 7 * * *")
    sched=$(echo "$sched_line" | sed -E 's/.*Schedule:[[:space:]]+//')
    # Extract last_run ISO timestamp
    last_run=$(echo "$run_line" | sed -E 's/.*Last run:[[:space:]]+([0-9T:+\.-]+).*/\1/')
    # Convert to epoch for arithmetic (strip subseconds; macOS BSD date)
    last_epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${last_run%.*}" "+%s" 2>/dev/null)
    now_epoch=$(date "+%s")
    age_hours=$(( (now_epoch - last_epoch) / 3600 ))
    # Cron schedule → max expected interval (heuristic)
    # Daily cadences (single hour, all other stars) → 25h threshold
    # 6h cadences (0 */6) → 7h threshold
    # 30m cadences (*/30) → 1h threshold
    threshold=25
    case "$sched" in
      *"*/30"*) threshold=1 ;;
      *"*/6"*)  threshold=7 ;;
      *"0 0 "*|*"0 1 "*|*"0 2 "*|*"0 3 "*|*"0 4 "*|*"0 7 "*|*"0 8 "*|*"0 9 "*|*"0 18 "*|*"0 23 "*) threshold=25 ;;
    esac
    if [ "$age_hours" -gt "$threshold" ]; then
      echo "MISSED_TICK: $name_line (last_run ${age_hours}h ago, threshold ${threshold}h, sched=$sched)"
    fi
  done
```

**Simpler one-liner (use this in heartbeats, full recipe above only for debugging):**

```bash
# Compute per-cron staleness; flag anything >25h for daily/nightly, >7h for 6h, >1h for 30m
NOW=$(date "+%s")
hermes cron list 2>/dev/null | awk '
  /Name:/      { name=$0; sub(/.*Name:[[:space:]]+/, "", name) }
  /Schedule:/  { sched=$0; sub(/.*Schedule:[[:space:]]+/, "", sched) }
  /Last run:/  {
    run=$0; sub(/.*Last run:[[:space:]]+/, "", run); gsub(/\..*/, "", run)
    cmd="date -j -f \"%Y-%m-%dT%H:%M:%S\" \"" run "\" \"+%s\""
    cmd | getline epoch; close(cmd)
    age = ('"$NOW"' - epoch) / 3600
    thresh = (sched ~ /\*\/30/) ? 1 : (sched ~ /\*\/6/) ? 7 : 25
    if (age > thresh) printf "MISSED_TICK: %-50s sched=%-15s age=%dh thresh=%dh\n", name, sched, age, thresh
  }'
```

## Decision matrix (V26 update to H38)

| `hermes cron list` | state.md mtime | Verdict |
|---|---|---|
| `Last run: <recent>  ok` | stale or recent | ✅ HEALTHY |
| `Last run: <stale>  error` | any | ❌ REAL FAULT (job failed) |
| `Last run: <stale>  ok` | any | ⚠️ **MISSED TICK** (scheduler gap, not job failure) — V26 |
| Not in registry | any | ⚠️ IDLE (no cron scheduled) |

**Treatment:**
- ✅ HEALTHY → no action
- ❌ REAL FAULT (job error) → nudge owner profile, surface error to user
- ⚠️ MISSED TICK → check `hermes cron status` for scheduler health; report aggregate N missed, recommend `hermes cron run <id>` to manually fire stale jobs OR accept delay until next natural fire
- ⚠️ IDLE → no action (H51 HEALTHY-by-design rule for no-cron profiles)

## Why the system has no built-in missed-tick detector

`hermes cron list` reads from `~/.hermes/cron/jobs.json` (or jobs SQLite). Each job entry stores `last_run` (timestamp of last invocation) and `last_exit_status` (ok/error from that run). The schema has no `next_expected_run` field, no `missed_count`, no `last_missed_at`. So the scheduler doesn't know when the job SHOULD have fired, only when it last DID. **This is a known gap in the cron implementation** (and likely the same in many cron-style schedulers — they optimize for "what ran" not "what should have run").

The heartbeat is the only layer that can detect this — and only if it computes "expected next fire" from the schedule string.

## When to apply V26

Apply V26 in EVERY heartbeat sweep alongside H38. The V26 missed-tick detection is cheap (~1 tool call, <1s) and catches a class of failure the existing 6+1 checks do not:

- After Mac sleep/wake cycles (crontab may pause during sleep; jobs scheduled during sleep window silently skip)
- After `hermes update` (cron daemon restart may drop pending queue)
- After long-running tasks block the scheduler (back-to-back slow cron jobs)

**Cost note:** V26 is unconditional — always run it in the heartbeat. The cost is one `hermes cron list` + one awk pipeline, which is already part of Check 2 (H38 cron-truth). V26 is a *reinterpretation* of Check 2's output, not a separate tool call.

## False-positive guard

A "missed tick" can be a legitimate skip if the cron has a `--skip` flag or condition. Verify by checking the cron command itself:

```bash
hermes cron list 2>/dev/null | grep -A 3 "MISSED_JOB_ID"
# Look for --skip-on, --only-if, or conditional logic in the command
```

For Tuấn Anh's current cron fleet, no crons have skip conditions — all 5 missed ticks on 2026-06-30 morning are REAL scheduler gaps. Recovery is automatic at next natural fire (i.e. tomorrow 02:00 for Memory Curator, 04:00 for Wiki Health, 07:00 for Autoresearch, etc.) — no manual intervention needed unless the user explicitly wants the missed run's output today.

## Root cause confirmation via `pmset` (H78 sweep, 2026-06-30 18:05)

When V26 fires with multiple missed ticks concentrated in a contiguous time window (e.g. all 5 crons in 02:00-07:30), the likely cause is **Mac sleep / low-power state** during that window. Confirm with:

```bash
# Find sleep/wake/assertion events during the missed window
pmset -g log 2>/dev/null | grep -E "$(date -v-1d '+%Y-%m-%d') 0[2-7]:" | head -30
```

**What to look for:**

- `Assertions ... [System: PrevIdle SysAct]` — system is in low-power state (Pre-idle), background processes can run
- `Assertions ... [System: PrevIdle]` (no SysAct) — fully idle, only wake-triggered processes run
- `Sleep Entry` / `Wake` lines — explicit sleep/wake transitions
- The cron daemon (PID varies) should appear holding an `ApplePushServiceTask` or `NSURLSessionTask` assertion — if MISSING, the daemon was suspended

**Real H78 root cause (5 missed crons, 2026-06-30 02:00-07:30):** Mac was in `PrevIdle` state during the entire window. `Hermes Daily Backup` (Schedule `0 3 * * *`) STILL fired at 03:05 because backup scripts include their own `pmset noidle` wrapper; the other 5 crons (Memory Curator, Wiki Memory Forget, Wiki Health, Autoresearch, X Research) don't have wake-from-sleep handling and were silently skipped.

**Cron daemon self-recovery (verified 2026-06-30 09:52:14 in `~/.hermes/logs/agent.log`):**

```
INFO cron.jobs: Job 'Hermes Autoresearch Nightly' missed its scheduled time (2026-06-30T07:00:00+07:00, grace=7200s). Fast-forwarding to next run: 2026-07-01T07:00:00+07:00
```

The cron daemon's `grace=7200s` (2h) is the **patience window**: if a job doesn't fire within 2h of its scheduled time, the scheduler fast-forwards to the NEXT natural fire instead of running the stale one.

**Treatment update:** V26 detected missed-ticks in a contiguous window + `pmset -g log` confirms `PrevIdle` → **root cause = Mac sleep, not daemon failure, not script bug**. Action: report the missed-tick aggregate + the `pmset` evidence + recommend the user add `pmset noidle` or `caffeinate -d` wrappers to the 5 affected scripts. Do NOT escalate as a Hermes fault.

## V28 (H79 heartbeat, 2026-06-30 19:30 — V27 auto-recovery prediction FALSIFIED)

V27 stated: "no manual `hermes cron run <id>` needed — scheduler fast-forwards to next natural fire automatically." Empirical test at H79 (2.5h after V27 was written, 12+ hours after the original 02:00–07:30 misses) shows the 5 missed crons STILL have `last_run = 2026-06-29T*`. The scheduler logged the "missed scheduled time" warning at 09:52 but did NOT fast-forward within the day — recovery is at tomorrow's natural fire (2026-07-01 02:00/03:00/04:00/07:00/07:30, 6.5–12h away).

**V28 rule:** the `grace=7200s` fast-forward is to the **NEXT scheduled occurrence**, not within hours. For a daily cron that missed today's 07:00, auto-recovery is tomorrow 07:00 — NOT today.

**V28 update to V27 treatment:**
- ✅ If the missed cron is non-critical AND user accepts next-day output → no action (V27 still holds)
- ⚠️ If missed cron is user-critical (e.g. Autoresearch for daily knowledge building, Wiki Health for hygiene) → recommend manual `hermes cron run <id>` AND add `pmset noidle` / `caffeinate -d` wrapper to the script
- 🚨 If 2+ consecutive missed ticks (H79 evidence: same 5 crons may miss both 2026-06-30 AND 2026-07-01) → `pmset noidle` wrapper fix becomes priority, not "wait for next natural fire"

**H79 ground truth table (for future heartbeat cross-validation):**

| Cron | Schedule | last_run @ 19:30 | Tick missed | Auto-recovery |
|---|---|---|---|---|
| Hermes Autoresearch Nightly | `0 7 * * *` | 2026-06-29T07:04:55 | 2026-06-30 07:00 | 2026-07-01 07:00 (~11.5h) |
| Hermes Agent X Research Daily | `30 7 * * *` | 2026-06-29T07:32:21 | 2026-06-30 07:30 | 2026-07-01 07:30 (~12h) |
| Wiki Health Daily | `0 4 * * *` | 2026-06-29T04:00:51 | 2026-06-30 04:00 | 2026-07-01 04:00 (~8.5h) |
| Wiki Memory Forget Daily | `0 3 * * *` | 2026-06-29T03:00:47 | 2026-06-30 03:00 | 2026-07-01 03:00 (~7.5h) |
| Memory Curator Nightly | `0 2 * * *` | 2026-06-29T02:04:58 | 2026-06-30 02:00 | 2026-07-01 02:00 (~6.5h) |

**Verification recipe (for next heartbeat):** at 2026-07-01 12:00, check if the same 5 crons STILL have `last_run = 2026-06-29T*`. If yes → 2026-07-01 morning tick ALSO missed → V28 confirmed at 2 consecutive cycles → recommend user add `pmset noidle` wrapper immediately. If last_run updated to 2026-07-01 morning timestamps → V27's "next natural fire recovers" holds, and H79 false-positive pattern was an isolated `grace=7200s` edge case.

## Changelog

- 2026-06-30 19:30 — H79 heartbeat: V28 lesson — `grace=7200s` fast-forward is to NEXT scheduled occurrence (next day for daily crons), NOT same-day auto-recovery. V27's "no manual intervention needed" was too optimistic for user-critical crons. V28 added.
- 2026-06-30 18:05 — H78 sweep root-caused V26 via `pmset -g log` PrevIdle evidence. Added root cause confirmation recipe + cron daemon `grace=7200s` auto-recovery behavior. Real H78 case: 5 crons in 02:00-07:30 window, Hermes Daily Backup at 03:05 succeeded (has `pmset noidle` wrapper), other 5 don't.
- 2026-06-30 17:02 — V26 discovered, reference created.
- 2026-06-30 17:02 — H38 decision matrix in `quick-reference-6check.md` Check 2 should be updated to add the ⚠️ MISSED TICK row (deferred to next touch of that file or via follow-up patch).