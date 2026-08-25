# H38: state.md mtime is NOT cron-truth (the H36 companion pitfall)

**Discovered:** 2026-06-26 16:01 (orchestrator 30m heartbeat, H34 row).
**Skill section this complements:** H36 clock-anomaly pitfall (frontmatter lies — use file mtime).
**One-line rule:** When a profile's state.md mtime looks stale, ALWAYS cross-reference `hermes cron list` before classifying as a cron fault. A "0 findings" audit log entry is APPENDED only if there's something to report — clean cron runs don't always rewrite state.md.

## The pattern (and why it's the inverse of H36)

H36 already taught the heartbeat that **frontmatter `updated:` can lie** because of cron clock-skew or self-overdue recovery mode. The fix: trust file mtime + content body timestamp.

H38 is the **inverse problem**: file mtime can also lie — not because of clock drift, but because a state.md is only written-to when there's a NEW SIGNAL to record. A cron that fires on schedule, sees "0 stuck, 0 pending QA, 9 idle, 0 critical findings", and exits cleanly, may NOT rewrite state.md at all. So the mtime can lag cron reality by hours or even days.

**The exact failure that produced H38:**

| Profile | state.md mtime | hermes cron last_run | Real status |
|---|---|---|---|
| code-reviewer | 2026-06-26 12:01:01 | 2026-06-26 12:01:06 (5s later) | HEALTHY |
| security-engineer | 2026-06-25 20:16:09 | 2026-06-26 03:01:10 (7h later) | HEALTHY |
| operations-manager | 2026-06-26 12:00:54 | 2026-06-26 12:01:30 (36s later) | HEALTHY |
| memory-curator | 2026-06-16 20:12:50 | 2026-06-26 02:03:26 (~10d later) | HEALTHY |
| research-lead | 2026-06-25 20:16:09 | 2026-06-25 18:01:46 (2h before mtime) | **REAL: Connection error** |

The first 4 profiles all had stale mtimes (some by 7h, some by 10 days) but were actually firing cron successfully. Only research-lead had a real fault — and it was the one whose mtime was NEWER than the cron run, indicating the cron failed BEFORE producing a new audit.

## Recipe — before classifying any profile as having a cron fault

```bash
# 1. Read mtime (H36 taught us this is ground truth for "when was state.md actually written")
stat -f "%Sm" ~/.hermes/profiles/<profile>/state.md

# 2. Cross-reference hermes cron list (H38 — REQUIRED before fault classification)
hermes cron list 2>/dev/null | grep -A 6 "<Profile Name>" | grep "Last run"

# 3. Decision matrix:
#    - mtime < cron_last_run AND exit_status = "ok" → HEALTHY (just didn't write to state.md)
#    - mtime ≈ cron_last_run (within minutes) → HEALTHY (audit appended as expected)
#    - mtime > cron_last_run → REAL FAULT: cron failed but something else updated state.md
#    - cron_last_run far in past AND exit_status = "error" → REAL FAULT: cron not firing or failing
```

## The diagnostic trap that produced 32+ false-positive sweeps

The qa-agent profile ran its own hourly gate from 2026-06-22 through 2026-06-26 (33+ sweeps). Each sweep measured mtime on 5 profile state.md files and classified profiles as "H28 PERSISTENT", "H29 WITHIN TOLERANCE", "H34 PARTIALLY-RECOVERED" based on mtime-vs-ideal-cadence alone. **All 3 fault classifications were wrong.** The actual `hermes cron list` showed all 4 supposedly-faulted crons were firing on schedule, with recent successful runs.

The qa-agent essentially created a phantom "multi-profile cron fault pattern" out of 32+ sweeps of measuring the wrong signal. The H34 row (the H38 fix) is the first one that verified against `hermes cron list` and got the truth.

## When to apply H38

Apply H38 in EVERY heartbeat sweep before classifying any profile as having a cron fault, especially when:
- The system has been idle for many consecutive sweeps (mtime lag is more likely on idle systems)
- A profile has been reporting "0 findings" or "0 pending" consistently (no reason to rewrite state.md)
- The other heartbeat checks pass (0 stuck, 0 conflicts) — if the system is otherwise healthy, mtime staleness is more likely a measurement artifact than a real fault

Do NOT skip the `hermes cron list` cross-reference even if mtime looks obviously stale. The cost is ~50ms; the cost of a false-positive fault pattern tracked across dozens of sweeps is significant (corrupted state.md, lost user trust, wasted cron time).

## Companion to H36

H36 + H38 together form the **"neither timestamp is fully trustworthy"** rule:

| Source | Can lie because of | Trust for |
|---|---|---|
| Frontmatter `updated:` | Clock-skew, self-overdue recovery | Audit IDENTITY (which scheduled tick this fulfills) |
| File mtime | "0 findings" cron runs don't rewrite | Physical TIMESTAMP (when state.md was actually written) |
| `hermes cron list` last_run | Rare — only if the cron itself lies about success | EXECUTION TRUTH (was the cron actually invoked + did it succeed) |
| Content body timestamp | Most reliable, but depends on agent discipline | Audit CONTENT (what was the audit actually about) |

**The H36+H38 rule:** When classifying profile freshness, ALL FOUR sources should be consistent. If they disagree, audit content + cron last_run are the most reliable signals. Frontmatter and mtime are necessary but not sufficient.

## Update history

- 2026-06-26 16:01 — H38 pitfall created, added to multi-agent-heartbeat SKILL.md
- Backfilled to qa-agent state.md H34 row (the row that discovered the pattern)
