# Operations-Manager Audit — Mature Steady-State Format (5+ consecutive on-cadence sweeps)

> **When to use this reference:** You've completed 5+ consecutive operations-manager 6h routing audits with `slip_ratio = 0/6h = 0.0` and the system is in deep idle (no active tasks, no pending QA, no escalations). The "verbose" template in `operations-manager-audit-template.md` was designed for the FIRST 1-3 audits where you're establishing the pattern. After that, the mature format is shorter, more signal-dense, and stops re-litigating recovered faults.

> **Discovered:** 2026-06-28 00:00 (5th consecutive on-cadence sweep, H34 sustained recovery at 10 sweeps).

## What changes in mature format

| Element | First 1-3 audits (verbose template) | Mature format (5+ sweeps) |
|---|---|---|
| Routing Log entry | 400-650 bytes, re-explains H38 caveat, H40 sibling-collision, H50 PRE-FIRE, cross-validation chain | **1-line** summary: "0 stuck, 0 pending QA, 9 idle. System dormant ~Nh+ days. N consecutive on-cadence sweeps. N crons healthy per `hermes cron list`." |
| Audit Summary block | Full 7-line block: Scope, Stuck, Pending QA, Idle, Active, Cron, Verdict | **Compress to 5 lines:** Scope, Stuck/Pending/Idle (1 line), Cron health (1 line), Verdict (1 line), H-counters (1 line) |
| Persistent findings section | Re-state the recovery (H34, H28, H29) every time | **Just track counter:** "H34 sustained recovery now at N sweeps" — do NOT re-explain |
| Cross-validation language | Long form with H<N> reference, sweep number, "consecutive idle sweeps" detail | **Compress:** "qa-agent H<N> sweep (Xh ago) cross-validates" — no need to list "0 outputs awaiting verification" every time |
| Profile Activity Matrix | Full 10-row table | Keep full table (still queryable), but compress notes column |

## When to switch

Switch from verbose to mature format when ALL of these are true:

- **5+ consecutive on-cadence sweeps** with `slip_ratio = 0/6h = 0.0`
- **0 active tasks** in all profiles (Active Tasks tables empty across the board)
- **0 outputs awaiting QA verification** (pending/handoff scan = 0)
- **0 escalations** (no user attention required)
- **Cron registry stable** (all `ok`, no `error:` annotations)

If ANY of these break, revert to verbose template for the next audit and re-establish pattern.

## The "do not re-litigate recovered faults" rule

**Anti-pattern:** Routing Log entry says "H34 PERSISTENT FAULT" → "H34 PARTIALLY RECOVERED" → "H34 WITHIN TOLERANCE" → "H34 sustained recovery now at N sweeps" — that's fine, it's progression. But once you've reached "sustained recovery now at 10 sweeps" for 3+ consecutive audits, stop restating the recovery. The next audit just says "10 sweeps" or "11 sweeps" — no recovery narrative.

**Why this matters:** the LLM "always produce" bias tries to add value to every output. For a steady-state system, that means inventing new angles on the same finding. The fix is **counter-only updates** for stable findings.

## Real example — verbose (audit #1, 2026-06-25 06:00)

```
- 2026-06-25 06:00: 6h routing audit (cron). 0 stuck, 0 pending QA, 8 idle (>4h).
  System remains dormant ~225h (9.4 days) since 2026-06-17 multi-agent experiment.
  cron gap: this audit is 54h late vs expected 6h cadence (2026-06-23 00:00 →
  2026-06-25 06:00 = 9 ticks missed). Per H8 qa-agent observation: same
  multi-profile cron fault pattern as code-reviewer (H28) and security-engineer
  (H29).
```

(~510 bytes)

## Real example — mature (audit #10, 2026-06-28 00:00)

```
- 2026-06-28 00:00: 6h routing audit (cron, on-cadence from 18:00 ✅ — 5th
  consecutive on-cadence run, H34 sustained recovery now at 10 sweeps). 0 stuck,
  0 pending QA, 9 idle. System dormant ~270h. 18/18 crons healthy per
  `hermes cron list`. qa-agent H67 (2h ago) cross-validates.
```

(~280 bytes — 45% smaller, same signal density)

## Companion recipes to keep handy (don't re-write each audit)

These are STABLE — only re-cite them in routing log if something changes:

- **H34 sustained recovery** — just track counter, don't re-explain
- **H38 mtime-vs-cron-truth** — once per audit, briefly (e.g. "9 idle by file-mtime, 8 confirmed HEALTHY per `hermes cron list`")
- **H40 sibling-collision** — only when there's actual collision risk (multi-agent writing same file); skip in steady-state
- **H50 PRE-FIRE** — only when a cron is within ±60s of sweep time
- **H60 decision window** — only when it opens/closes, not every audit

## When to revert to verbose format

- **H34 sustained recovery breaks** (a sweep is late, slip_ratio > 0) → verbose with gap analysis
- **A profile becomes active** (new task, new handoff, new verdict) → verbose with profile details
- **A cron enters ERROR state** → verbose with full cron health table
- **User asks for full audit** (e.g. "audit kỹ lại") → verbose regardless of cadence
- **First audit after a cron self-overdue recovery** (H10-style 30h+ gap) → verbose

## Update history

- 2026-06-28 00:00 — Reference file created from 5th consecutive on-cadence audit. Mature format saves ~45% bytes per audit while preserving signal density.
