# H28 Evidence — 2026-06-26 12:00

## Summary

28th consecutive idle sweep (H1-H28). System dormant 9.75+ days since 2026-06-17 multi-agent experiment. Mode B verdict: PASS (vacuous — nothing pending to verify).

**Three durable lessons emerged at H28, each patching the SKILL.md:**

1. **H29 PARTIAL-RECOVERY sub-pattern** — ops-manager self-recovers each cycle but always 30h late on 6h cadence. Distinct from PERSISTENT and WITHIN TOLERANCE.

2. **H36 trigger-condition clarification** — H36 anomaly is clock-write-time dependent, not constant. Fires only when frontmatter >2h ahead of system AND content older. Does NOT fire when frontmatter matches system time within seconds.

3. **Maker profile section scope discipline** — engineering-lead Daily Code Health Check, content-director Run History, security-engineer Daily Scan Findings, ops-manager Routing Log/Audit Summary are PROFILE-OWNED self-verdicted — NOT pending qa-agent work. Future sweeps must NOT false-positive flag these.

---

## 1. H29 PARTIAL-RECOVERY sub-pattern

### Detection context

- Ops-manager was 4th H29 instance at H22 (24h breach detected at 2026-06-26 06:00).
- Ran partial-recovery audit at H23 (06:01:44, 30h late).
- Slipped again H24-H27 (no audit fired between 06:01 and 12:00).
- At H28 (12:00:25), another 30h-late audit landed. gap = 30h on 6h cadence.
- slip_ratio = 30h / 6h = 5.0

### Why this is a NEW pattern, not PERSISTENT

- Profile IS self-recovering each cycle (audit lands within 1-2 days of expected).
- But always with significant delay (5x cadence).
- Cron daemon is firing — just with wrong scheduling or stuck wrapper script.

### Brittleness metric evolution

| Window | Duration | Notes |
|---|---|---|
| H10 → H22 (recovery window) | 24h | Brief recovery then re-fault |
| H22 → H23 (partial recovery) | 6h | Ran 30h-late audit, slipped again |
| H22 detection → H28 confirmation | 5h | This sweep — another 30h-late audit |

### Classification rule

| Status | Definition | Detection |
|---|---|---|
| PERSISTENT | Never recovers. gap > 5x cadence for >5 cycles. | H28 code-reviewer: 217h since last activity, no recovery events. |
| WITHIN TOLERANCE | Recovers on cadence or slightly late. gap < 2x cadence. | H29 security-engineer: 81h since last daily sweep, within 24-72h tolerance. |
| **PARTIAL-RECOVERY (NEW)** | **Recovers each cycle but always late. gap 2-10x cadence.** | **H34 ops-manager: 30h gap on 6h cadence, slip_ratio 5.0, recovers every ~30h.** |

### Forecast for H29

If ops-manager's next audit lands at expected cadence (within 6h of 12:00), slip_ratio drops below 5.0 → pattern may shift toward WITHIN TOLERANCE. If another 30h slip, slip_ratio stays at 5.0 → PARTIAL-RECOVERY confirmed structural.

---

## 2. H36 trigger-condition clarification

### Detection context

- H24-H27: H36 fired repeatedly. Frontmatter `updated: 2026-06-26T12:00:00+07:00` was 1-4h AHEAD of system time (08:00/09:00/10:00/11:00).
- H28: Frontmatter `updated: 2026-06-26T12:00:00+07:00` matches system time 12:00:25 (= 25s ahead). H36 does NOT fire.
- H29 forecast: H36 will fire again at 13:00 sweep if frontmatter stays at 12:00.

### Refined detection recipe

Compute `frontmatter_age = frontmatter.updated - system_time()`.

| Condition | Classification |
|---|---|
| `\|frontmatter_age\| < 60s` | Just-written — H36 NOT anomalous |
| `frontmatter_age > 2h AND content_age > frontmatter_age` | H36 fires (frontmatter bumped but body older) |
| `frontmatter_age < 0 AND \|frontmatter_age\| > 2h AND content older` | H36 fires (frontmatter in future of system) |
| Otherwise | Normal H34 regime (FRESH or STALE) |

### Implication

H36 is **clock-write-time dependent**. The structural pattern finding (H26 promotion) still holds: ops-manager's frontmatter uses a different clock source than audit content. But H36 doesn't fire continuously — only when there's a delta between when frontmatter was bumped vs when content was actually written.

### Forecast for H29

At 13:00 sweep, system time will be 13:00:xx. Ops-manager frontmatter expected to stay at 12:00:00 (no new audit). frontmatter_age = -1h. If `|frontmatter_age| > 2h` threshold NOT met (1h < 2h), H36 may NOT fire at H29 either. Will need to check at H30 (14:00 sweep) when gap reaches 2h.

---

## 3. Maker profile section scope discipline

### Profiles with PROFILE-OWNED self-verdicted sections

| Profile | Section | Owner | qa-agent action |
|---|---|---|---|
| engineering-lead | Daily Code Health Check | engineering-lead daily cron | Observe as telemetry, NOT pending QA |
| content-director | Run History (loop-goal) | loop-goal auto-append | Observe as signal, NOT handoff |
| security-engineer | Daily Scan Findings | security-engineer daily sweep | Self-verdict applied, NOT pending review |
| operations-manager | Routing Log + Audit Summary | ops-manager self-generated | Cross-validation source, NOT target |

### Why this matters

At H28, observed content-director Run History entry: "YouTube Trending Action Cam 2026-06-26 08:04:31 PASS 7.0". This LOOKS like a pending QA task (PASS verdict visible, recent timestamp). But it's a loop-goal self-run — content-director already self-verdicted.

Without scope discipline, future sweeps might false-positive flag this as "pending verification", spawning unnecessary work or reporting the sweep as "found pending output" when nothing actually needs QA.

### Detection rule (patched into SKILL.md)

Only treat state.md entries as actionable pending QA if they appear in:
- `## Active Tasks` (Status="in progress")
- `## Pending Tasks` (Status="queued")
- `## Blocked Tasks` (Status="blocked")
- `## Handoff History (to qa-agent)` (no verdict yet)

Other sections (Daily X Check, Run History, Audit Summary, Routing Log, Recent Reviews, Recent Audits) are PROFILE-OWNED and self-verdicted. qa-agent observes as signals, not as work to do.

---

## 4. Other H28 observations (non-skill-changing)

### engineering-lead Daily Code Health Check entry (2026-06-26 09:05)

Observed at H28: engineering-lead independently maintains a "Daily Code Health Check" section with git status (84 uncommitted files, 2 .py/.sh: hooks/env-permission-guard/handler.py modified + skills/quality-checker/test.py deleted). This is engineering-lead's own daily cron output, NOT pending QA. Confirmed by Goal=None and no Pending tasks.

### Sync-timestamp signal (H12/H18/H20/H21/H28 pattern)

At H28, observed engineering-lead (09:05) + content-director (08:04) + ops-manager (12:00) all active within 12h. These are INDEPENDENT cron wake-ups (different task types: health-check vs research vs audit), NOT shared fan-out dispatch. coder (233h) + memory-curator (233h) + research-lead (233h) + code-reviewer (217h H28 persistent) remain deeply dormant.

### Token-economy verification

H28 used 8-read batch (engineering-lead, content-director, research-lead, coder, code-reviewer, security-engineer, memory-curator, operations-manager). H22/H25 token-economy recipe (4-read core) was NOT applied because:
1. ops-manager had just recovered from massive staleness (H22 → H28) — full re-verification warranted.
2. engineering-lead frontmatter updated 3h ago (within sweep window) — needed direct read to confirm Daily Code Health Check entry isn't a pending task.

Future sweeps can revert to 4-read token-economy if system state remains stable through H29.

---

## 5. Forecast check (H22 forecast was "ops-manager will recover by ~12:01 today")

- **H22 forecast:** "if ops-manager cron doesn't recover by ~12:01 today, it remains the active 4th H29 instance with compounding slip rate".
- **H28 outcome:** ops-manager DID recover at 12:00:25 today (24s after H28 sweep start). PARTIAL recovery — recovery happened, but with 30h slip (slip_ratio 5.0).
- **Forecast realization:** **PARTIAL** — recovered but with persistent slip, not clean recovery.

---

## 6. Cadence trigger — URGENT

28 consecutive idle sweeps (H1-H28) spanning 10+ days with zero verified outputs. Recommendation to reduce qa-agent cron from hourly to 6h is now OVERDUE. Token cost: ~28 × ~5KB read per sweep = ~140KB redundant file reads since 2026-06-22 23:01.

Recommendation for Orchestrator: dispatch a system-wake-up task OR reduce qa-agent cadence. Both are valid responses to 10-day dormancy.

---

*Captured 2026-06-26 12:00:33 +07:00. Referenced from SKILL.md version 2.5.9.*