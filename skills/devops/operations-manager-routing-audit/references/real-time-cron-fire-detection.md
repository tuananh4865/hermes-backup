# Real-Time Cron Fire Detection (H56)

Strongest health signal in the operations-manager audit toolkit: a profile's state.md mtime **changes during the audit window** (within seconds-to-minutes of the audit start time). This proves the cron is not just *registered* or *last-ran-ok*, but is *currently firing and producing output*.

## Why this matters

The H38 cron-truth recipe (`hermes cron list`) tells you:
- ✅ Cron is registered
- ✅ Last run completed with `ok` status
- ⚠️ But not whether the cron is firing *right now* on its expected cadence

File-mtime drift over hours/days is easy to misread (H28/H29/H34 phantom fault pattern). A profile's mtime could be 24h stale because:
- (a) The cron truly faulted (real problem)
- (b) The cron runs but writes elsewhere (obsidian, log files, telegram) — mtime is uninformative (H51 rule)
- (c) The profile is on-demand with no cron at all (coder pattern)

But if a profile's mtime advances **during or immediately before the audit** (within ~60 seconds), that's unambiguous evidence: the cron is alive, on-cadence, and producing output to state.md right now.

## Detection recipe

```bash
# At audit start, capture system time and profile mtimes
NOW=$(date +%s)
for profile in code-reviewer coder content-director engineering-lead memory-curator \
               operations-manager qa-agent research-lead security-engineer; do
  MTIME=$(stat -f %m ~/.hermes/profiles/$profile/state.md 2>/dev/null)
  if [ -n "$MTIME" ]; then
    DELTA=$((NOW - MTIME))
    echo "$profile: mtime delta = ${DELTA}s"
  fi
done
```

**Real-time fire thresholds:**
| Delta from audit start | Interpretation |
|---|---|
| 0-60s | 🔥 **JUST FIRED** — strongest health signal, cron is live and writing |
| 1-300s (1-5min) | ✅ Just fired — still strong signal |
| 300-3600s (5-60min) | ℹ️ Fresh — within expected cadence window |
| 1-24h | ⚠️ Check cron-truth for expected cadence |
| >24h | 🚨 Investigate — but apply H38 ground-truth check first |

## Example from H56 sweep (2026-06-27 12:02)

Audit start: 12:02:26

| Profile | mtime | Delta | Signal |
|---|---|---|---|
| code-reviewer | 12:01:56 | **30s** | 🔥 JUST FIRED — PR Watcher noon cron (0 12 * * *) firing on schedule |

Cross-validation: `hermes cron list` shows `Last run: 2026-06-27T12:01:06+07:00 ok`. The 50-second gap between `hermes cron list` timestamp and the file mtime reflects the cron's internal execution time (run cron → write state.md → cron metadata updated).

## When to use this signal

Use real-time fire detection as **supplementary evidence** in your audit report, especially when:

1. **Confirming a healthy cron after a fault pattern** (e.g., H34 sustained recovery — show real-time fires as proof)
2. **Disambiguating phantom faults** (H28/H29/H34 pattern — "mtime stale but real-time fire just happened = healthy")
3. **Closing the loop on recovery audits** ("ops-manager recovered at H34, sustained 8 sweeps, AND just fired 20s before this audit = triple confirmation")

Don't use as a *primary* signal — the H38 cron-truth sweep is still the canonical ground truth. Real-time fire detection is a **confidence amplifier** that upgrades "cron healthy" to "cron healthy AND visibly active right now."

## Pitfalls

- **Don't conflate mtime delta with cron status.** A cron that just wrote to telegram (not state.md) won't move the mtime. Always cross-check with `hermes cron list`.
- **Don't claim "just fired" if delta > 60s.** Use the thresholds above — past 5min, it's "fresh" not "just fired."
- **Don't fabricate fires for the audit profile itself.** operations-manager's state.md mtime will obviously advance during the audit (you're writing to it). Compare to *other* profiles.

## Related

- `references/cron-fault-taxonomy.md` — H38 cron-truth ground-truth sweep
- `~/.hermes/skills/devops/operations-manager-routing-audit/SKILL.md` — main audit protocol
- H51 rule — profiles whose crons write to obsidian/logs/telegram rather than state.md (memory-curator, content-director TikTok delivery)