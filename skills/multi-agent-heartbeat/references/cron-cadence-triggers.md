# Cron Cadence Triggers

> When and how to recommend cadence changes for orchestrator and specialist crons. Based on the 2026-06-23/24 15-sweep sequence.

## The trigger table

| Sweeps idle | Trigger | Recommendation | Escalation language |
|---|---|---|---|
| 1-6 | None | Keep cadence | (no flag) |
| 7-9 | Soft | Recommend reducing qa-agent cron 1h→6h | "soft recommendation" |
| 10-12 | Medium | URGENT — 0-pending pattern held 7+ days, ops-manager cron also overdue | "URGENT saturation" |
| 13+ | Hard + co-trigger | **System-wide cron audit task** — multiple specialists overdue, not just one cron over-firing | "system-wide cron delivery problem" |

## When co-trigger fires (the H9 lesson)

**Co-trigger condition:** Cadence trigger for qa-agent (X+ consecutive idle sweeps) AND another specialist's cron is also overdue (e.g. ops-manager 30h+ past expected next tick).

**Interpretation:** This is NOT a single cron over-firing. It's a system-wide cron delivery issue. The cron daemon, the gateway, or the orchestrator's cron is dropping jobs.

**Escalation language:**
> "CADENCE TRIGGER + co-trigger condition ACTIVE: 9 consecutive idle sweeps (H1-H9) for qa-agent + ops-manager 30h past expected 12:00 next tick + security-engineer daily scan 8h+ overdue. Pattern points to system-wide cron delivery fault, not single-cron over-firing. Recommend cron audit task — check `hermes cron list --all`, `hermes cron status`, and the cron daemon logs."

**What to actually check:**
```bash
# 1. Are all crons registered?
hermes cron list --all

# 2. Are they being delivered?
hermes cron status

# 3. Are they firing on time?
# Compare each cron job's "next run" against actual mtime of its target state.md

# 4. Is the cron daemon alive?
ps aux | grep -E "(cron|hermes-cron)" | grep -v grep

# 5. Are there cron errors?
tail -50 ~/.hermes/logs/cron.log 2>/dev/null
tail -50 ~/.hermes/logs/gateway.log 2>/dev/null | grep -i "cron"
```

## The "is this a real issue?" checklist

Before recommending a cadence change, answer:

1. **Has the 0-pending pattern held for 7+ days?**
   - Yes → real, recommend cadence reduction
   - No → false alarm, keep current cadence

2. **Is there an active task the cron is monitoring?**
   - Yes → don't reduce (the cron is needed)
   - No → safe to reduce

3. **Is the cron output being delivered somewhere useful?**
   - Yes (Telegram, log file, etc.) → keep
   - No (vanishing into /dev/null) → check delivery target first

4. **Has the user explicitly asked for this cadence?**
   - Yes → never reduce without asking
   - No → safe to recommend

5. **Are other crons also failing?**
   - Yes → system-wide cron audit, don't just touch this one
   - No → safe to reduce this one alone

## The "ACCEPT vs ESCALATE" decision

| Scenario | Verdict | Reason |
|---|---|---|
| 0-pending, all specialists active in last 24h | ACCEPT | System functioning normally |
| 0-pending, 1 specialist cron overdue (e.g. security daily scan 8h late) | ACCEPT with WATCH flag | Non-blocking, re-check next sweep |
| 0-pending, 2+ specialists cron overdue | ACCEPT with ESCALATION flag | Cron delivery issue, recommend audit |
| 0-pending, but >2h queue age (real stuck task) | ESCALATE | Stuck task = blocked work = notify user |
| 1+ outputs awaiting qa-agent verification >1h | ESCALATE | QA backlog = blocked work = notify user |
| Security CRITICAL finding | AUTO-FIX (per owner authority) + ESCALATE | Auto-fix is reversible; user must know |
| 2 agents on same file | RESOLVE per priority matrix + log | Conflict resolved, log it |
| 2 agents on same file AND no clear priority | ESCALATE | Defer to user |

**Rule of thumb:** ACCEPT is correct for "system stable, just nothing happening." ESCALATE is for "something is stuck or wrong."

## The "Idle" calculation

```python
from datetime import datetime, timezone, timedelta

TZ_VN = timezone(timedelta(hours=7))

def idle_str(last_iso: str, now: datetime = None) -> str:
    """Return human-readable idle duration."""
    now = now or datetime.now(TZ_VN)
    last = datetime.fromisoformat(last_iso)
    delta = now - last
    hours = delta.total_seconds() / 3600
    
    if hours < 1:
        return f"{int(delta.total_seconds() / 60)}m"
    if hours < 24:
        return f"{int(hours)}h{int((hours % 1) * 60)}m"
    days = hours / 24
    return f"{int(days)}h+"
```

**Examples:**
- 0h30m → "30m"
- 4h59m → "4h59m"
- 24h+ → "24h+"
- 165h+ → "165h+" (cap at days; "6d+" is fine too but "165h+" is more granular)

## "1-line summary" templates

**Idle system, all clean:**
> "System idle & stable, 0 stuck / 0 pending / 0 conflicts / 0 escalations."

**Idle system, cron overdue:**
> "System idle, but ops-manager + security-engineer cron overdue (4-8h) — recommend cron audit."

**Active system, real work:**
> "System active: 2 tasks in progress, 1 output awaiting qa-agent, 0 conflicts."

**Active system, escalation:**
> "ESCALATION: 1 task stuck >2h (T-123), 1 security CRITICAL auto-fixed, 0 conflicts."

**Cadence trigger fired:**
> "15 consecutive idle sweeps in qa-agent log; recommend reducing cadence from 1h→6h. No other issues."

## Reporting cadence to the user

The heartbeat report goes to the user via the cron delivery target (Telegram, log file, etc.). Make the 1-line summary the FIRST thing they see — they may not read the table.

**If the cron is delivered to a Telegram topic/group:** The table is the message body, the 1-line summary is the first sentence. Telegram will show both in the notification preview.

**If the cron is delivered to a log file only:** No formatting change needed, but the 1-line summary is what `grep` will find. Put it on the same line as the timestamp for easy `grep "Heartbeat" log.txt | head` filtering.
