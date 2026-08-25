# Idle Escalation Recipe

> What does "stop and escalate" actually mean when the H20 cadence boundary fires?
> This is the recipe that was never exercised in real data until H21 (2026-06-24 16:01).

## Background: the H20 boundary (defined)

The SKILL.md H20 boundary says: "after 20+ idle sweeps, **stop recommending cadence changes** in every row. Instead, file a single **escalation** to the user (Orchestrator or human) and stop."

That was the rule. It was never tested in production. H21 (this session) is the first real-data test, and it revealed the rule is **ambiguous**:

- What does "file a single escalation" mean? A Telegram message? A wiki page? A cron job that fires once and silences itself?
- What does "stop" mean? The heartbeat cron still fires every 30m — does it still emit the report? Just skip the per-row cadence trigger text? Both?
- How does the heartbeat know when to RESUME normal cadence narration? When the user responds? When the system stops being idle? Never?

## The 3-state model (H21 realization)

The heartbeat has 3 operating modes. The transition rules were implicit; this is the first explicit definition.

| State | Trigger to enter | Behavior | Trigger to exit |
|---|---|---|---|
| **NORMAL** | Sweep 1-19 idle (or any non-idle event) | Full per-row cadence narration, escalation table, all 6 steps of protocol | 20+ consecutive idle sweeps |
| **STEADY-STATE IDLE** | 20+ consecutive idle sweeps, NO other anomalies (no security, no conflicts, no stuck tasks) | Compressed row (table + 1-line summary only), NO per-row cadence trigger, single "persistent escalations" footer | User responds OR non-idle event occurs (e.g. real task, security finding) |
| **DEGRADED** | 20+ idle sweeps AND at least one anomaly: cron overdue on another profile, security regression, conflict | Compressed row + repeat anomaly in EVERY row until resolved | Anomaly resolved |

**Key insight (H21):** The skill predicted a "60% row size reduction" in STEADY-STATE IDLE mode. The H21 row in this session was actually LARGER than H20 (~36094 bytes vs 32669). The prediction was wrong because:

1. The H21 row in this session was the FIRST time the boundary was tested — the agent copying the H20 row's narration pattern was the default behavior, requiring explicit override
2. The agent had not internalized that "the boundary is now active" — the skill's wording was aspirational, not enforced

**Fix:** When the heartbeat is at sweep ≥20, it must EXPLICITLY compare its row size to the prior row and shrink if growing. Concrete check:

```python
prev_size = get_file_size(state_file) - len(new_row_text)
if new_row_size > prev_size * 0.7:  # row grew >30% in steady-state → too verbose
    rewrite_compressed(new_row)  # drop the per-row "cadence trigger" repetition
```

## The escalation mechanism (H21 attempt)

When STEADY-STATE IDLE mode is entered for the FIRST time, the heartbeat should emit a single Telegram message (or whatever the cron's delivery target is) with the title "**SYSTEM ENTERING STEADY-STATE IDLE — 20 consecutive idle sweeps**" and body:

```
Trigger: <N> consecutive idle sweeps (H1-H<N>)
Last non-idle event: <date> <profile>
Persistent issues:
  - <list of cron overdue, security notes, etc.>
Recommendation: <single sentence>
Heartbeat will continue to fire every <X>m but will emit compressed rows from now on.
Resume normal cadence when:
  - User responds
  - Non-idle event occurs
  - Anomaly detected
```

**Real failure in H21:** This Telegram message was NOT sent. The "escalation" was implicit in the per-row text, which is exactly the noise pattern the H20 boundary was supposed to prevent.

**Fix (H22+):** When transitioning into STEADY-STATE IDLE for the first time, write a `~/.hermes/profiles/qa-agent/.steady-state-idle` marker file. The marker file's existence = STEADY-STATE IDLE mode. On every sweep, check for the marker; if present, suppress per-row cadence narration. The marker is removed when:
- User sends a message to qa-agent
- A non-idle event occurs (engineering-lead or any other profile produces real work)
- An anomaly is detected (security, conflict, stuck task)

## The "stop" semantics

**H21 attempt:** I kept emitting per-row "Cadence trigger fired again" text despite H20 saying to stop. The behavior is hard to override because the per-row template was never parameterized.

**Fix (H22+):** Update the sweep template to read like this in STEADY-STATE IDLE mode:

```
| H22 | <time> | ACCEPT | <score> | 0 | (steady-state idle) | 0 stuck, 0 pending, 0 conflicts. Persistent escalations: <list>. See qa-agent/.steady-state-idle marker. |
```

That's it. ~150 bytes per row instead of ~3500. The table still has 1 row per sweep, the report still emits, the structural-truth check still runs, but the noise floor drops to zero.

## What about Mode 7 (sibling-collision)?

When STEADY-STATE IDLE mode is active, sibling-collision is more likely to go unnoticed because each row is small and easier to duplicate without obvious visual bloat. The H21 incident (this session) was a real collision between the orchestrator 30m heartbeat and an hourly gate that fired 42 seconds apart. The file ended up with TWO `| H21 |` rows.

**Fix:** Even in STEADY-STATE IDLE mode, the post-append verification (`Counter` check for duplicate H<N> IDs) is MANDATORY. See `references/state-md-integrity-pattern.md` Mode 7.

## Decision tree for the heartbeat agent

```
At sweep start:
  1. Read all active profile state.md files
  2. Compute "idle sweep count" = current H counter
  3. Check for anomalies (cron overdue, security, conflict)
  4. If idle_count >= 20 AND no anomalies:
       Emit compressed row
       Suppress per-row cadence trigger
       If first time entering this state: write marker file + emit Telegram escalation
  5. If idle_count >= 20 AND anomalies:
       Emit compressed row + anomaly line
       (still suppress per-row cadence trigger, but report anomaly every sweep)
  6. If idle_count < 20:
       Emit full row per existing template
```

## H21+ when to add MORE restrictions (the H30+ question)

The H20 boundary is the current cap. If the system remains in STEADY-STATE IDLE for 30+ sweeps, the heartbeat should:

1. Reduce to 6h cadence (via cron schedule change — out of heartbeat's authority; file escalation)
2. Switch to "presence heartbeat" mode: just verify all profiles' state.md still exist and have valid frontmatter, no full read of body content
3. Eventually archive the loop-engineering system entirely (escalate to user with explicit "should we tear this down?")

**H21 status:** System has been idle 171h+ since 2026-06-17 multi-agent experiment. The H20 boundary fired at H20 (15:00, 20 sweeps). H21 is the first test of STEADY-STATE IDLE behavior and the behavior was incorrect. The 6h cadence reduction recommendation is now 21 sweeps old.

**Recommendation for H22:** The agent should explicitly check for the `.steady-state-idle` marker file and follow the compressed-row pattern, regardless of what the prior row's text looked like. Trust the marker file, not the prior row's pattern.
