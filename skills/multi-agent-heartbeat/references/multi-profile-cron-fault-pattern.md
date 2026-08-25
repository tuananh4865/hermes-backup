# Multi-Profile Cron Fault Pattern (the 3rd-instance detector)

> When 2+ specialist cron jobs go overdue simultaneously, this is a system-wide cron delivery issue, NOT a per-cron fault. Document the co-occurrence, escalate ONCE, and stop treating each as independent.

## The pattern (3+ confirmed instances, real data from heartbeat sweep 2026-06-26 12:00)

| Date | ops-manager | code-reviewer | security-engineer | qa-agent (H series) | Diagnosis |
|---|---|---|---|---|---|
| 2026-06-24 | 30h+ stale | noon watch 36h+ stale | daily sweep 19h+ stale | 12+ idle sweeps | System-wide cron delivery issue |
| 2026-06-25 06:00 | 54h stale (9 ticks missed) | 202h idle (no daily check cron) | 51h idle (last 2026-06-23 03:03) | H8 (8 consecutive idle) | Same pattern, 3rd observation |
| 2026-06-25 06:00–10:00 | **RECOVERED to FRESH (1h)** — see Drift-Recover-Drift pitfall below | 217h idle (H28, persistent) | 52h stale | H10 (1h, fresh) | Brief recovery |
| 2026-06-25 11:00+ | Started drifting again (2h → 15h → 30h across sweeps H11–H20) | 217h idle (H28, persistent) | 67h → 81h | H11–H21 (idle accumulation) | **Drift resumed** |
| 2026-06-26 12:00 | 30h stale (5 ticks missed) | 217h idle (H28) | 81h stale (H29 within daily tolerance) | H21 (21 idle sweeps) | **H34 NEW: 3rd persistent instance after drift-recover-drift oscillation** |

### Drift-Recover-Drift oscillation pitfall (NEW, 2026-06-26)

Real pattern observed in 2026-06-25 06:00 → 2026-06-26 12:00 window:

1. **06:00**: ops-manager cron 54h stale (9 ticks missed) — H34 fault detected
2. **06:01 → 10:00**: cron recovered, ops-manager fired normally, qa-agent H10 cross-validated as FRESH (1h) at 07:01
3. **11:00+**: cron started drifting again (H11: 2h stale boundary → H13: 15h → H17: 19h → H21: 23h at-massively-stale-boundary → 2026-06-26 12:00: 30h stale)

**Diagnosis:** Recovery was a single-tick blip, not a permanent fix. The cron daemon (or its dispatcher) failed intermittently — not a one-time fault. Common root causes on macOS:
- LaunchAgent plist `StartCalendarInterval` not handling missed firings (no `RunAtLoad` fallback, no missed-fire recovery)
- Hermes gateway restart wiping in-memory cron schedule cache
- Profile-specific hook (`~/.hermes/hooks/<profile>/*.sh`) erroring silently and being skipped

**How to detect drift oscillation in an audit:**

```bash
# Read ops-manager Routing Log entries — count gaps vs cadence
grep -E "^- [0-9]{4}-[0-9]{2}-[0-9]{2}" ~/.hermes/profiles/operations-manager/state.md | tail -10
# Each entry should be ~6h apart. Gaps >6h = drift. Multiple non-zero gaps with at least one recovery = oscillation.
```

**How to record it in the audit:**

In the `Multi-Profile Cron Fault Pattern (Tracking)` table inside state.md, add a `Status` column with one of:
- `PERSISTENT` — never recovered (e.g. code-reviewer H28)
- `WITHIN TOLERANCE` — long cadence, single missed tick is normal (e.g. security-engineer H29)
- `DRIFT-OSCILLATING` — recovered then drifted again (e.g. operations-manager H34)

**Anti-pattern (do NOT do):** Once you've seen a profile recover, do NOT remove it from the persistent-fault list. Drift-oscillating profiles are MORE dangerous than persistently broken ones because they create false confidence ("cron was fine 6h ago, must be a one-off"). The real-world equivalent: a flaky cron that intermittently fails will burn through trust and budget before anyone audits it properly.

## Detection recipe (apply in any heartbeat or routing audit)

When the audit or heartbeat completes, scan the freshness of all periodic crons:

```bash
# 1. Compute idle hours for every active profile
for d in ~/.hermes/profiles/*/; do
  profile=$(basename "$d")
  mtime_sec=$(stat -f %m "$d/state.md" 2>/dev/null) || continue
  [ -z "$mtime_sec" ] && continue
  now=$(date +%s)
  idle_h=$(( (now - mtime_sec) / 3600 ))
  echo "$profile: ${idle_h}h"
done

# 2. Apply the co-trigger matrix
```

## Co-trigger matrix (decision tree)

| ops-manager gap | Other cron gap | Diagnosis | Action |
|---|---|---|---|
| <6h (on cadence) | <6h (on cadence) | Healthy | Continue normal |
| 6-12h (1-2 ticks late) | 6-12h (1-2 ticks late) | One cron drifted, others fine | Investigate the drifting cron, leave others |
| 12-24h (3-4 ticks late) | 12-24h (3-4 ticks late) | Two+ crons drifted | System-wide cron audit task (single escalation) |
| >24h (5+ ticks late) | >24h (5+ ticks late) | Cron delivery broken | STOP individual cron fixes, escalate to user as ONE issue |
| 24h+ | cron never existed | Initial cron setup missing | Install the missing cron, document |

**Real pattern (2026-06-25 06:00):** ops-manager 54h stale + security-engineer daily sweep 51h stale + code-reviewer 202h idle (no daily check cron) + qa-agent H8 1h ago (still running) = **3rd instance of multi-profile cron fault**. The right action was: 1 escalation in Routing Log ("same pattern as code-reviewer H28 + security-engineer H29"), 1 entry in Persistent Findings ("3rd instance — system-wide cron audit task needed"), and STOP trying to fix each cron individually.

## Why "fix the cron" doesn't work for this pattern

Each individual cron that goes overdue has a separate root cause:
- ops-manager: launchd plist `ai.hermes.operations-manager` likely has an error in the start calendar interval, or the previous run hung
- security-engineer: daily sweep is part of a chained cron, one link in the chain may have failed silently
- code-reviewer: noon watch was a manual cron that was never re-set after a Hermes restart
- qa-agent: hourly sweep has been running fine — it's the OTHER crons that are broken

**The common factor is NOT a single root cause.** It's that the user (or another operator) hasn't audited cron delivery recently. The fix is meta: do a cron audit, not a per-cron fix.

## Escalation format (1 message, 1 escalation)

When the co-trigger matrix indicates "system-wide cron audit task", emit ONE message in the heartbeat/audit report:

```
### ⚠️ PERSISTENT FINDINGS
1. **Multi-profile cron fault (3rd instance)**: ops-manager 54h stale + security-engineer 51h stale + code-reviewer 202h idle. Co-trigger matrix: 24h+ gap across 3 profiles = cron delivery broken. Recommend: 1) check `launchctl list | grep hermes` for failed services, 2) re-validate each cron's schedule string, 3) consider consolidating crons to a single orchestrator that dispatches to specialists.
```

That's the entire escalation. Don't repeat it in 5 different sections. Don't try to fix any specific cron. The next heartbeat (6h later) will re-confirm or show movement.

## What NOT to do (anti-patterns observed in real audits)

1. **Don't fix the cron in the audit** — ops-manager is a router, not a cron administrator. The audit's job is to record the fault, not fix it.
2. **Don't recommend specific cron fix commands** — the user has shell access and Hermes restart capability. They don't need `crontab -e` instructions.
3. **Don't try to wake up the dormant profiles** — the system is dormant by design (9.4 days idle since the 2026-06-17 multi-agent experiment). Trying to artificially activate profiles just to "test the routing" is noise.
4. **Don't include dormant profiles in the escalation count** — code-reviewer 202h idle is just "no work to do", not "cron broken". Only include profiles with **expected periodic activity** (ops-manager 6h, qa-agent 1h, security-engineer 24h) in the cron-fault pattern.
5. **Don't restart the system** — restart cascades through all 13 profiles, breaks the append-only invariant on state.md, and destroys the H1-H8 verdict history. The audit works even with 8 idle profiles.

## When the pattern breaks (system healthy, 1 cron drifted)

If only ONE cron is overdue and others are fresh, the matrix says "fix the drifting cron" — different action. Example: ops-manager 9h stale but qa-agent 1h fresh and security-engineer 1h fresh = ops-manager alone drifted, suggest investigating that specific cron.

The "system-wide" diagnosis only applies when **2+ periodic crons are simultaneously overdue** AND the gap is **>12h** for at least one.

## Cross-references

- `references/operations-manager-audit-template.md` §10 — self-overdue recovery mode (the inverse scenario)
- `references/cron-cadence-triggers.md` — when to recommend cadence changes
- `references/h24-profiles-perm-blind-spot.md` — H24 security perm regression that ran while crons were drifting
- `references/h26-silent-kill-mode.md` — Mode 8 silent-kill (different scenario: qa-agent's own verdict history, not the ops-manager audit)
