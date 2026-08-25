# Cron Fault Taxonomy (H34 codified)

Classifies cron slip patterns observed across 49+ operations-manager sweeps.

## Slip Ratio Table

| Slip ratio | Time late | Status | Action required |
|---|---|---|---|
| 0/6h | 0h | WITHIN TOLERANCE | Log, no action |
| 0.17/6h | 1h | STALE (boundary) | Note, no action |
| 2-3/6h | 12-18h | DEGRADING | Track in cron truth table |
| 4+/6h | 24h+ | CRITICAL FAULT | Investigate crontab entry, notify Orchestrator |
| Variable, recovery_acceleration >1.0 | n/a | RECOVERING | Track sustainability |

## Recovery Trajectory Pattern

**Example: ops-manager H34 recovery (2026-06-23 to 2026-06-25)**

```
H22: slip_ratio 4.0 (24h breach, 4 ticks missed)
H23: slip_ratio 5.0 (30h late, 5 ticks missed) — CRITICAL
H28: slip_ratio 5.0 (5h brittleness, oscillating)
H29: slip_ratio 0.17 (1h late, RECOVERY START)
H34: slip_ratio 0.0 (CRITICAL CORRECTION sweep, FULLY RECOVERED)
H35-H49: slip_ratio 0.0 sustained 15 sweeps ✅
```

**Recovery criteria:**
- slip_ratio = 0 for 2+ consecutive sweeps
- recovery_acceleration >1.0 (deceleration rate of slip)
- `hermes cron list` shows `Last run` matches expected cadence

## Multi-Profile Fault Pattern (H28/H29/H34 — RESCINDED)

Originally observed: code-reviewer (H28, 2026-06-17), security-engineer (H29, 2026-06-23), operations-manager (H34, 2026-06-23) all showed stale mtime but healthy crons.

**Lesson:** File mtime ≠ cron truth. A profile can have 217h stale mtime but fire its cron every 24h on schedule. Always cross-check with `hermes cron list` before declaring a fault.

**Rescission:** H38 false-positive correction — all 3 instances were measurement artifacts (mtime-vs-cron confusion), NOT real faults.

## Cron Registry Ground-Truth Sweep (H38 recipe)

```bash
hermes cron list 2>&1 | head -200
```

**Verify:**
- Number of active crons (expected: 18)
- ALL `Last run` end with `ok`
- ZERO `error:` annotations
- `Next run` timestamps in future per cadence

**Real fault indicators:**
- `Last run` ends with `error:` (not `ok`)
- `Last run` is way past expected cadence AND `Next run` is not adjusting
- Cron missing from registry entirely (was registered but no longer listed)

## When to Escalate

Escalate to Orchestrator if:
- Any cron shows `error:` annotation
- Any cron is >24h late with no recovery trend
- Multiple related crons fault simultaneously (suggests daemon issue)
- A profile's cron is missing from registry (was registered, now gone)
