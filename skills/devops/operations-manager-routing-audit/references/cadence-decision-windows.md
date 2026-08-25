# Cadence-Decision-Windows & Pre-Fire Patterns (H50/H51/H60 codified)

Codifies three new patterns observed across 60+ operations-manager sweeps and qa-agent H<N> verdict history since 2026-06-26.

## H50 — Pre-Fire Window (≤60s Tolerance)

**Problem:** A cron is "due" to fire within seconds of audit time. If audit reports it as OVERDUE, that's a false alarm — the cron will fire within seconds/minutes.

**Detection:**
```bash
hermes cron list 2>&1 | grep -B1 -A3 "Next run"
# Compare "Next run" timestamp to sweep time
```

**Triage rule (≤60s window):**
- If `Next run` is **within 60 seconds** of sweep time → **PRE-FIRE**, NOT overdue
- If `Next run` is **>60s away** but within ~60min → **NORMAL cadence, do not classify**
- If `Next run` is **past** by >1min → genuine slip, classify per H34 taxonomy

**Pre-fire log format:**
```
H50 PRE-FIRE: <cron-name> fires <HH:MM> = <N>min away
```

**Examples from 2026-06-27 17:00 sweep (qa-agent H61):**
- Operations Manager Routing Audit: Next run 18:00, sweep 17:01 → 59min away = NORMAL
- Research Lead Trend Scan: Next run 18:00, sweep 17:01 → 59min away = NORMAL (with ~1m late tolerance for cron startup variance)

**Pitfall:** Do NOT classify crons in the 60min pre-fire window as "overdue" — they're not. Use H34 thresholds (12-24h+) for actual fault classification.

## H60 — Auto-Suspend Decision Window (H60→H65)

**Problem:** When a recommendation has been repeated >5 times without action (per H44 cadence-decay), the signal becomes overhead. But you can't just drop it — the underlying need may still be valid.

**Progression (codified at qa-agent H60, 2026-06-27 16:00):**

| Sweep | Action | Description |
|---|---|---|
| H44 | First cadence-decay note | "Noted, no action needed" — switch focus to cron-truth signal |
| H45-H54 | Continued re-derivation | Repeat note each sweep, don't escalate |
| H55 | **Final warning** | Explicit "if no action by H60, auto-suspend will fire" |
| H60 | **Auto-suspend issued** | Concrete command recommended: `hermes cron update <name> --schedule "0 */6 * * *"` OR `hermes cron disable <name>` |
| H61-H64 | Decision window open | Track elapsed sweeps, no new actions — give Orchestrator time to respond |
| H65 | **Terminal** | If no response by H65, take the recommended action automatically |

**Cost tracking (token cost if no action):**
- Per-sweep token cost: ~3K (qa-agent hourly gate context)
- Cumulative: H60=180K, H61=183K, H62=186K, H63=189K, H64=192K, H65=195K
- Breakeven with action: if Orchestrator acts at H62, ~6K tokens saved vs continuing to H65

**H60 sweep log format:**
```
H60 AUTO-SUSPEND THRESHOLD REACHED: 60+ idle sweeps, 0 pending outputs, all recipes still holding.
Recommendation to Orchestrator:
(a) NOTED NO ACTION NEEDED
(b) EXPLICIT SUSPENSION REQUEST: hermes cron update <name> --schedule "0 */6 * * *"
(c) AUTO-SUSPEND PER H51: hermes cron disable <name>
Decision window: H60 → H65.
```

**Cross-pollination:** operations-manager audit (6h cadence) tracks this window for Orchestrator visibility even though qa-agent is the one running hourly.

## H51 — By-Design Idle Rules

**Problem:** File mtime says profile is "idle" but the profile is HEALTHY by design. Don't flag these as faults.

### H51a — Coder-No-Cron Rule

Coder profile has NO cron registered. Stale mtime (200+ days) is normal — coder is event-driven, only fires when an explicit task is routed to it.

**Verdict:** HEALTHY by default. Do NOT flag as fault in idle reports.

### H51b — Memory-Curator-Obsidian Rule

Memory-curator nightly consolidation cron runs successfully (writes to Obsidian vault, NOT to `state.md`). So `state.md` mtime stays stale indefinitely even though the cron is firing daily.

**Detection:**
```bash
hermes cron list | grep -A3 "Memory Curator"
# Verify last_run timestamp is recent (within 24h for daily cron)
```

**Verdict:** HEALTHY. State.md mtime stale is by-design — not a fault signal.

### H51c — Default-Profile-Active-Sessions Rule

Default profile is shared across all Telegram/CLI sessions. Each session-end writes a row to default/state.md Run History. So default mtime is the most-recent-session-end, not "active agent" indicator.

**Verdict:** mtime 0-1h = recent session ended (normal, not "active agent"). Idle reporting must distinguish "session-ended" from "agent-running".

## Combined Idle-Verdict Heuristic

When a profile appears "idle" by mtime (>4h since last state.md write), apply this triage:

1. **Coder** → H51a, HEALTHY by default
2. **Memory-curator** → H51b, verify cron last_run, HEALTHY
3. **Default** → H51c, not a maker profile, excluded from idle count
4. **All other maker profiles** → Cross-check with `hermes cron list` for the profile's cron:
   - If cron healthy + recent last_run → HEALTHY (mtime stale is cosmetic, cron-truth wins per H38)
   - If cron errored or >24h late → REAL FAULT, flag in audit report
5. **If cron doesn't exist for profile** → H51a analogue, document as by-design

**Net rule:** "Idle" reports should be ~N profiles-by-mtime MINUS (H51a + H51b + H51c + cron-healthy-but-stale-mtime) to get the TRUE idle count requiring Orchestrator attention.

## Cross-Reference

- `cron-fault-taxonomy.md` — H34 slip ratio table
- `real-time-cron-fire-detection.md` — H56 technique (detect crons fired within seconds)
- `false-positive-triage-recipes.md` — H5/H10 patterns
- `30min-heartbeat-pattern.md` — LITE variant output format
