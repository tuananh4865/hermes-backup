# H60+ Mode B Idle Sweep Protocol (2026-06-27)

Codified recipe for sweeps that land in the H60+ regime (60+ consecutive idle sweeps, H60→H65 decision window open for qa-agent cadence auto-suspend, H34 fully recovered). Validated at H60/H61/H62/H63.

## Pre-conditions

- 60+ consecutive idle sweeps with 0 pending outputs
- All recipes (H38, H40, H44, H50, H23) holding
- H60 decision window open: H60→H65 for qa-agent cadence change
- H34 ops-manager WITHIN TOLERANCE sustained (slip_ratio 0/6h ≥ 5 consecutive sweeps)
- H37 phantom-cron claim fully rescinded (research-lead cron real + healthy)

## Sweep Protocol (4-step)

### Step 1: Pre-patch integrity check
- `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` → expected count
- Verify H1-H(N-1) all have clean format
- Check for sibling writes since last sweep (H40 critical-override recipe)

### Step 2: Anchor selection (H44 decision tree)
- If `## Verdict History` count ≤ 9: use H15 simple boundary
- If count 2-9: use H25 4-line context anchor
- If count ≥10 AND prior row tail ≤40 chars: use **H44 2-line fallback** (PREFERRED)
- If count ≥10 AND tail >40 chars: use H42 unique-phrase anchor
- **H52 bold-marker variant** (NEW H63): if tail contains `**...** |` ending, use `**closing phrase.** |\n## Verdict History` — count verified = 1

### Step 3: H38 cron-truth sweep (token-economized)
- `hermes cron list` fresh read
- 18 active crons expected (post-H39 registry growth)
- ALL must show `ok` exit_status, ZERO `error:` annotations
- Capture Operations Manager last_run → confirm H34 WITHIN TOLERANCE
- Capture Research Lead last_run → confirm H37 phantom-cron rescission holds

### Step 4: H50 pre-fire + H60 forecast-realization
- H50 pre-fire: check any cron whose `Schedule:` next-fire is ≤60s away
- H60 forecast: check if Orchestrator actioned (a/b/c) recommendation
  - (a) NOTED NO ACTION NEEDED
  - (b) `hermes cron update QA Agent Quality Gate --schedule "0 */6 * * *"`
  - (c) `hermes cron disable QA Agent Quality Gate` (auto-suspend per H51)
- Forecast to next sweep

## Token-economy rules (H22/H25 reduction)

- Skip primary reads (engineering-lead, content-director, research-lead, etc.) — ops-manager cross-validation per H23 suffices when audit is FRESH
- 6-check heartbeat protocol: 0 pending, 0 outputs, 0 security, 0 conflicts, 0 escalations, dormant count
- Spot-check rule (H23): every 6th sweep, do 1-2 primary reads even when ops-manager is FRESH

## Patch construction

```yaml
old: <anchor with content.count == 1>
new: |
  | H<N> | <ISO timestamp> | N/A | N/A | 0 | (<sweep type>) | <sweep body> |
  <boundary>
```

## H63 worked example

- Anchor: `**H60→H65 window decision pending Orchestrator action.** |\n## Verdict History` (count=1)
- New row: H63 with 18/18 cron-health summary, H34 sustained recovery note, H50 pre-fire (heartbeat 19:00), H60 forecast-realization PARTIAL (no action yet), decision window 2 sweeps remaining
- Post-patch row count: 48 → 49 ✅

## Decision window action matrix (H60→H65)

| Sweep | Action |
|---|---|
| H60 | AUTO-SUSPEND recommendation published |
| H61-H63 | Monitor for Orchestrator action; if none, re-state options (a/b/c) |
| H64 | FINAL WARNING (per H51 timeline) |
| H65 | AUTO-SUSPEND executes if no action by H65 |
| H66+ | Hourly cron disabled; qa-agent re-runs only on orchestrator dispatch |

## Recipe hold rate at H63

- H38 cron-truth: 18/18 healthy (held)
- H40 sibling-collision: count=48→49 (held, no collision)
- H44 2-line anchor: count=1 pre-patch (held)
- H52 bold-marker variant: 2nd consecutive use (held)
- H50 pre-fire: 1 captured (heartbeat 19:00) (held)
- H23 cross-validation: ops-manager last_run 18:02:17 (FRESH) (held)

6/6 recipes held. Sweep succeeded first-try with zero retries.
