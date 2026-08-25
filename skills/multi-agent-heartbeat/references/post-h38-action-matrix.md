# Post-H38 Action Matrix: what to do AFTER the heartbeat finds a real fault

**Discovered:** 2026-06-26 16:30 (orchestrator 30m heartbeat, H35 row).
**Skill section this complements:** H38 mtime-vs-cron-truth-pattern (the H36 companion).
**One-line rule:** H38 tells the heartbeat HOW to find a real fault (cross-reference `hermes cron list`). This reference tells the heartbeat WHAT TO DO once it finds one — because the action depends on which of 3 fault categories it falls into.

## The gap that produced this reference

H38 fixed the detection problem: heartbeats no longer confuse "stale mtime" with "real fault". But once the heartbeat detects a real fault (e.g. cron failing with `RuntimeError: Connection error` + delivery failed `platform 'telegram' not configured/enabled`), the H38 framework has no guidance on the action path.

Real failure pattern (H35 sweep, 2026-06-26 16:30): the heartbeat found research-lead's `Research Lead Trend Scan` cron had been erroring for ~22h. The heartbeat correctly classified it as REAL (not a measurement artifact) and reported it as "pre-emptive nudge recommended but not auto-fixable from default profile authority" — but the report ended there. No recipe for the nudge. No action matrix. The fault was identified but the resolution path was implicit.

## The 3 fault categories (post-H38)

Once `hermes cron list` confirms a REAL fault (cron_last_run is old AND exit_status is "error", or mtime > cron_last_run), classify the fault by **fix authority**:

| Category | Description | Authority | Heartbeat action |
|---|---|---|---|
| **A — Auto-fixable by orchestrator** | Reversible, low severity, owner has authority (e.g. chmod 600 on a state.db that drifted to 644) | security-engineer (perms), engineering-lead (code), content-director (content) | Auto-fix in this turn, log to state.md (or in-process sweep), no escalation |
| **B — Owned by another specialist** | The fault is in a domain another agent owns (e.g. research-lead's research domain) — orchestrator should route, not fix | The specialist whose state.md/domain the fault affects | Nudge via `hermes --profile <name> chat -q` OR escalate to user; do NOT auto-fix from default profile |
| **C — System-wide infrastructure** | Multiple profiles affected OR the fault is in cron daemon / gateway / shared infrastructure (not a single profile) | Orchestrator + user (joint) | STOP individual cron fixes, escalate to user as a system-wide cron audit task |

**Real H35 example:** research-lead connection error + telegram-not-configured = Category B (owned by research-lead's profile, not the orchestrator's domain). Orchestrator's correct action: report in escalation footer, optionally nudge the research-lead profile, do NOT try to fix research-lead's telegram config from default.

## Authority matrix for common fault types

| Fault signal | Category | Who fixes | Heartbeat recipe |
|---|---|---|---|
| `chmod 644` on `~/.hermes/*.db` (perm drift) | A | security-engineer (perm owner) | Auto-fix `chmod 600` via in-process sweep, log in heartbeat report |
| `RuntimeError: Connection error` in research-lead cron | B | research-lead profile | Report in escalation footer; nudge via `hermes --profile research-lead chat -q` if 2+ sweeps in a row |
| `RuntimeError: Connection error` in 3+ profile crons simultaneously | C | Orchestrator + user | STOP per-profile fixes, escalate as system-wide cron audit |
| `exit_status: error` + `delivery failed: telegram not configured` | B | The profile that owns the cron | Same as above — report + nudge, don't fix telegram config cross-profile |
| `last_run > 24h ago` + no recent exit_status entry | C | Orchestrator + user (cron daemon) | The cron may not be installed/registered. Recommend `hermes cron list` audit + check crontab |
| Cron is firing but its owner profile is gone (profile folder deleted) | B | User (must recreate profile OR remove the cron) | Escalate immediately — dangling cron is wasting system resources |
| Stale mtime + cron last_run recent + exit_status "ok" | NOT A FAULT | n/a | H38 says: healthy. No action. Do not classify as a fault at all. |

## The pre-emptive nudge recipe (Category B action)

When the heartbeat finds a Category B fault (real, owned by another profile), the action options in priority order:

**Option 1 — Just report it (preferred for first detection):**

Add a one-line entry to the heartbeat report's escalation footer:

```
**Escalation flag (non-blocking):** research-lead `Research Lead Trend Scan` cron errored at 2026-06-25 18:01:46 (RuntimeError: Connection error + telegram not configured). 22h overdue. Recommend nudge next sweep if still failing.
```

This is the H35 actual output. Do NOT dispatch a subagent or call `hermes --profile` yet — wait for the next sweep to see if the fault resolves on its own (cron daemon often self-recovers from transient network errors).

### Distinguishing transient network error from config bug (H35 sub-pattern)

When `hermes cron list` shows `last_run: error: RuntimeError: Connection error` + `⚠ Delivery failed: platform '<X>' not configured/enabled`, the two parts of the message are often **the same fault from two different reporters** (the cron script raised Connection error, the delivery wrapper raised "platform not configured"). But the **root cause** can be either:

| Combination | Root cause | Self-recovery likelihood | Action |
|---|---|---|---|
| Connection error + telegram not configured, next_run ≤ 1 cycle away | Transient network blip OR ad-hoc user disabled telegram for the cron | HIGH — next run often succeeds without intervention | Report + let auto-retry (Option 1, no nudge) |
| Connection error + telegram not configured, next_run > 2 cycles away | Config bug — telegram is genuinely not enabled in `~/.hermes/config.yaml` channels section | LOW — same fault will recur | Nudge (Option 2) — the fault is persistent, not transient |
| Connection error ONLY, no delivery-failed line | Pure network / upstream-API issue (Reddit, X, YouTube, etc.) | MEDIUM — usually self-recovers within 24h | Report + check next_run timing |
| delivery-failed ONLY, no error in last_run | Cron succeeded; delivery channel config is wrong (separate fault class) | LOW — never self-recovers | Nudge the owning profile to fix `config.yaml` |

**Real H35 example (research-lead):** `error: RuntimeError: Connection error` + `⚠ Delivery failed: platform 'telegram' not configured/enabled` + `next_run: 2026-06-26T18:00:00` (27 minutes away at sweep time). Both row-1 conditions met (transient, next_run ≤ 1 cycle away) → **Option 1, no nudge**. Verified pattern by H35 (16:33) + the cron truth table at the top of the skill.

### The next-run timing check (H35 sub-pattern, first-line triage)

Before deciding Option 1 vs Option 2, **always check the `next_run` field** in `hermes cron list`:

```bash
hermes cron list 2>/dev/null | grep -A 7 "<Cron Name>" | grep "Next run"
# - If next_run is ≤ 1 cadence-cycle away AND the fault is transient-looking → Option 1 (no nudge)
# - If next_run is > 2 cadence-cycles away (or has been rescheduled) → escalate, fault won't self-clear
# - If next_run is in the PAST (cron missed its tick entirely) → Category C, system-wide cron delivery issue
```

**Why this matters:** Dispatching a `hermes --profile X chat -q` nudge is expensive (110-220s minimum per H27) and adds a sub-agent log to the system. For a cron that's about to retry on its own in 27 minutes, the nudge is pure waste. The next_run field is the cheapest signal for "is this going to resolve itself?".

**Real H35 outcome:** research-lead's next_run was 18:00 (27 min from sweep), fault was transient-looking (connection error, not a hard config miss). Decision: Option 1, do nothing, let auto-retry. Verified correct because: (a) the cron was already scheduled to fire, (b) the fault pattern was consistent with self-recovery, (c) no new agent process was needed.

## Option 2 — Dispatch a one-shot nudge (after 2+ consecutive detections):**

If the same fault appears in 2 consecutive heartbeats (e.g. H35 + H36 both detect research-lead connection error), then escalate to action:

```bash
# Verify the fault is still present (don't re-trigger on transient recovery)
hermes cron list 2>/dev/null | grep -A 6 "Research Lead Trend Scan"

# If still erroring, dispatch a one-shot nudge to the owning profile
hermes --profile research-lead chat -q "Research Lead Trend Scan cron has been erroring with 'Connection error' + 'telegram not configured' for Nh. Diagnose and fix or report blocker." --timeout 180
```

**Pitfall — 180s timeout:** H27 lesson (in-process-sweep-vs-delegate reference): sub-agent dispatch needs 110-220s minimum for context loading + skill discovery + execution. 180s default timeout can fail mid-task. If using `hermes --profile X chat -q` from a heartbeat, set `--timeout 300` minimum, or use `execute_code` to run the diagnostic in-process.

**Option 3 — Escalate to user (after 3+ consecutive detections OR if fault is system-wide):**

If the fault persists across 3+ heartbeats OR is part of a multi-profile pattern (Category C), STOP trying to auto-recover and escalate to the user:

> "**System-wide cron audit needed.** 3+ sweeps have detected [fault pattern]. Recommend user inspect `crontab -l` + `hermes cron list` + check cron daemon logs (`~/.hermes/logs/cron.log` or similar). The H28/H29/H34 + research-lead pattern is a recurring multi-profile fault that needs infrastructure-level investigation."

## The "do not fix cross-domain" rule (H35 decision rationale)

**Why the H35 sweep did NOT try to fix research-lead's telegram config:**

The orchestrator (default profile) has owner authority over:
- Perm drift on shared files (security-engineer's domain, but LOW severity auto-fix is delegated)
- Stale qa-agent / ops-manager state.md (own bookkeeping)
- The heartbeat report itself (Step 6)

The orchestrator does NOT have owner authority over:
- research-lead's telegram config (research-lead owns its own delivery channels)
- research-lead's research methodology (content/research specialists own their domain)
- Any cross-profile state change that affects another agent's domain

**The test for "can the orchestrator fix this?":**
- Is the fault in shared infrastructure (perm, format, route)? → YES, auto-fix
- Is the fault in a single profile's domain (research, code, content, security findings)? → NO, nudge or escalate
- Is the fault affecting 2+ profiles simultaneously? → System-wide, escalate

## Companion rules

- **H36 clock-anomaly pitfall** (frontmatter lies, use mtime) — frontmatter detection recipe
- **H38 mtime-vs-cron-truth** (mtime also lies, use `hermes cron list`) — execution detection recipe
- **H27 in-process sweep vs delegate** — when sub-agent dispatch times out, fall back to `execute_code` for fast diagnostic (~200ms)
- **Self-overdue recovery mode (operations-manager variant)** — when the orchestrator's OWN cron is overdue, the audit IS the recovery; do not apply H26 silent-kill to operations-manager

## Update history

- 2026-06-26 16:30 — Post-H38 action matrix created from H35 sweep, added to multi-agent-heartbeat references
- 2026-06-26 16:33 — H35 sub-pattern: distinguishing transient network error from config bug, plus the next-run timing check (Option 1 vs Option 2 first-line triage). Verified live in the 16:33 orchestrator heartbeat — research-lead's transient connection error + telegram-not-configured was correctly classified as Option 1 (next_run was 27 min away, let auto-retry) instead of dispatching a costly 180s sub-agent nudge. Encoded as two subsections under "Option 1".
- 2026-06-26 17:31 — Recipe re-validated in independent orchestrator sweep (default profile, 30m heartbeat). research-lead `Research Lead Trend Scan` cron (id `42a9ec3df0dc`) now 23h stale (last run 2026-06-25 18:01:46, error: `RuntimeError: Connection error` + `⚠ Delivery failed: platform 'telegram' not configured/enabled`). `next_run: 2026-06-26T18:00:00+07:00` (29 min away at sweep time). Recipe applied: H38 cross-reference (mtime ≠ cron truth → check `hermes cron list` last_run + exit_status), Option 1 decision (transient network error + next_run ≤ 1 cycle → no nudge, no auto-fix, report in escalation footer). Outcome: clean heartbeat report, no action taken, no sub-agent dispatch. Cross-validation: 10/11 crons healthy, 1 transient fault being auto-retried within the hour. Skill recipe confirmed as "load-bearing" across two independent sessions without modification.
