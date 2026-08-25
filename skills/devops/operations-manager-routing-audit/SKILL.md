---
name: operations-manager-routing-audit
description: "Cron-based routing audits across the multi-agent profile fleet. Use when running 6h routing audits, detecting stuck/pending/idle states, or verifying cron registry health."
version: 1.5.0
author: Hermes Agent + operations-manager profile (H1-H82 codified; H82 "kanban log mtime ≠ DB status" + 18:00 self-correction added 2026-06-30 after t_3a73b0af 12:00 false positive was caught and corrected)
license: MIT
metadata:
  hermes:
    tags: [operations, multi-agent, routing, cron, audit, fleet-health]
    homepage: https://hermes-agent.nousresearch.com/docs/user-guide/profiles
---

# Operations Manager Routing Audit

Class-level skill for periodic routing audits across the multi-agent profile fleet. Codifies 50+ sweeps of operational patterns refined by the operations-manager profile since 2026-06-17.

## When To Use

- Running 6h routing audit (cron-driven)
- Running 30m Orchestrator Heartbeat (lite variant — see `references/30min-heartbeat-pattern.md`)
- Detecting tasks pending >2h (stuck)
- Detecting outputs awaiting QA verification >1h
- Detecting idle agents (>4h no activity)
- Verifying cron registry health
- Cross-validating with qa-agent hourly gate

## Audit Protocol (7-Check Heartbeat)

Run these 7 checks every audit tick:

1. **Tasks pending >2h (profile state.md):** Scan all profile `state.md` files for non-empty Active/Pending/Blocked Tasks tables
2. **Tasks pending >2h (kanban queue):** `hermes kanban list` + `hermes kanban stats` + `sqlite3 ~/.hermes/kanban.db "SELECT id, status, started_at, completed_at FROM tasks WHERE status NOT IN ('done')"` — check for any task in `blocked`/`running`/`ready` status older than 2h. **🚨 PITFALL (H82, codified 2026-06-30 18:00): do NOT use `kanban/logs/<task_id>.log` mtime as task status.** The log file is the session transcript of the last time anyone opened a question about that task — NOT a record of when it completed. A task can be `done` in the DB for weeks while its log file still shows an unanswered prompt from weeks ago. **The kanban DB is the only ground truth for task status.** Real false-positive incident: ops-manager's 12:00 audit (2026-06-30) reported `t_3a73b0af` stuck for 31.6 days based on log file mtime, but the 18:00 audit self-corrected after querying the DB directly (status='done', completed_at=2026-06-30T12:34:36, finished 32min after the 12:00 audit was written). **Always cross-check the DB before escalating "1+ stuck task" claims.** qa-agent's hourly gate explicitly does NOT check kanban (H28 scope discipline), so operations-manager is the only sweep that catches stuck kanban tasks — but it must do so correctly via DB, not log mtime. For the 3rd verification layer (disk file presence — silent-recovery bug), see `multi-agent-heartbeat` V24.
3. **Outputs awaiting qa-agent verification >1h:** `find ~/.hermes/profiles -type f -name "pending*" -o -name "handoff*"` (apply false-positive triage — see Recipes)
4. **Security CRITICAL findings:** Read security-engineer state.md for latest audit verdict
5. **Agent conflicts:** Check if two profiles touched same file in same window
6. **Escalations needed:** Any task blocked >2h, any cron errored, any CRITICAL security finding
7. **System dormant:** Hours since last maker activity

### Why kanban check matters (codified 2026-06-30)

qa-agent's 6-check protocol is structurally blind to kanban tasks. The H28 scope discipline says qa-agent verifies "outputs awaiting verification" via file system, not via kanban task queue. This means a kanban task that completed (run finished, summary in run log) but lost its artifact — or one that blocked mid-run and was never retried — will sit silently in the kanban indefinitely, invisible to qa-agent.

**Operations-manager audit catches what qa-agent misses.** Add this check to every routing audit. The cost is one `hermes kanban list` + one `hermes kanban stats` call (low token cost), the benefit is surfacing zombie tasks that have been silently blocked for weeks.

## Ground-Truth Sources (priority order)

**1. `hermes cron list` (HIGHEST)** — H38 recipe: ground truth for cron registry health. Shows all active crons with `Last run`, `Next run`, and `ok`/`error:` status. Always sweep this FIRST before reading state.md files.

**2. qa-agent state.md H<N> verdict history** — Independent cross-validation. qa-agent runs hourly, applies 6-check protocol, and writes structured verdict rows. Use most recent H row (typically 1h old).

**3. Profile state.md files** — Read all 9 maker profiles + default in parallel batch. Look at:
   - `## Current Goal` (should be None or pure-routine-cron)
   - `## Active Tasks` / `## Pending Tasks` / `## Blocked Tasks` tables (should be empty)
   - `## Recent Verdicts` (most recent activity timestamp)
   - File mtime (informational only — see Cadence-Decay recipe)

**4. `find` scan for handoff files** — Apply H10 false-positive triage (see Recipes).

## Recipes

### H38 — `hermes cron list` Ground-Truth Sweep

```bash
hermes cron list 2>&1 | head -200
```

Look for:
- Number of active crons (typically 18)
- ALL `Last run` should end with `ok`
- ZERO `error:` annotations
- `Next run` timestamps should be in the future per cadence

If ANY cron shows `error:` or `ok` is missing → real fault. If `Last run` is way past expected cadence → cron slip but not necessarily fault (check `Next run`).

### H10 — False-Positive Handoff Triage

`find ~/.hermes/profiles -type f -name "pending*"` will match:
- `coder/skills/hermes-github-backup/references/wiki-independence-pending.md` — static ref doc, NOT a handoff (mtime >30 days, path under `skills/*/references/`)

`find ~/.hermes/profiles -type d -name "handoff*"` will match:
- `coder/skills/handoff/` — static skill bundle containing only `SKILL.md`, NOT a task queue

Triage rule: if path is under `skills/*/references/` or `skills/*/` AND file/dir is >30 days old AND content is documentation-style → FALSE POSITIVE. Otherwise → investigate.

### H44 — Cadence-Decay Option (a)

When the same recommendation has been made 5+ times without action, the signal becomes overhead. Two options:

**(a) Explicit "noted, no action needed"** — State the recommendation is logged, shift focus to other signals (e.g., cron-truth sweep which IS new value per sweep).

**(b) Escalation with new evidence** — If new evidence warrants it, escalate; otherwise default to (a).

Default: (a). Never re-state the same cadence recommendation >5 times.

### H34 — Multi-Profile Cron Fault Taxonomy

When a profile's cron is late:

| Slip ratio | Status | Action |
|---|---|---|
| 0/6h | WITHIN TOLERANCE | Log, no action |
| 1-2 ticks late (6-12h) | STALE | Note, re-derive from primary reads |
| 3+ ticks late (12-24h) | DEGRADING | Track in cron truth table |
| >24h late | CRITICAL FAULT | Investigate crontab entry, notify Orchestrator |
| recovery_acceleration >1.0 for 2+ sweeps | RECOVERED | Note recovery, track sustainability |

**Recovery trajectory example:** ops-manager went H22 (24h breach) → H34 (CRITICAL CORRECTION) → H38 (fully recovered, sustained 7+ sweeps). Recovery is sustained when slip_ratio = 0/6h for 2+ consecutive sweeps.

### H36 — Clock-Anomaly Detection

Profile state.md `updated:` frontmatter may be AHEAD of system time. This indicates clock-write anomaly. Only fires when frontmatter > system time (not when stale). Log but don't fabricate rows. Per H38 lesson: harmless cosmetic drift on operations-manager frontmatter (e.g. `2026-06-27T00:00:00+07:00` showing as 1h in future of actual 23:00) is NOT a fault signal — file mtime is the truth, frontmatter is the cron-stamp.

### H50 — Pre-Fire Window (≤60s Tolerance)

Crons "due" to fire within seconds of audit time are NOT overdue — they will fire within seconds/minutes. Triage rule: `Next run` within 60s of sweep = PRE-FIRE (log, not fault), within 60min = NORMAL cadence, past by >1min = genuine slip. Do NOT classify crons in the 60min pre-fire window as overdue. See `references/cadence-decision-windows.md`.

### H56b — Cross-Cadence Sibling-Collision (Codified 2026-06-29)

When two crons share the same `0 */6 * * *` cadence (e.g. qa-agent 6h gate + operations-manager routing audit, both fire at 00:00/06:00/12:00/18:00), the H40 sibling-collision pre-check recipe must be tightened. Default H40 assumes "6h gap between sibling writes" — when both fire within seconds of each other, the gap is ~0s and a sibling write CAN land mid-patch.

**Detection rule:**
1. Check `hermes cron list` for any OTHER cron with the same Schedule as the sweep being run
2. If found, the pre-check `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` must be run **immediately before patch** (not "6h ago" — use actual file mtime as reference)
3. The expected post-patch count = current + 1 is only valid if BOTH crons use the same H<N> numbering. If sister profile uses different numbering (e.g. operations-manager uses sweep timestamps, not H numbers), the patch anchor must be unique to the file's content, not its table row count.

**Real example (H74, 2026-06-29 06:00):** qa-agent H73 sweep landed at 06:00:28 (17s before ops-manager H74 sweep at 06:00:42). Both use 6h cadence `0 */6 * * *`. Sibling-collision pre-check via `wc -c` + targeted anchor (operations-manager tail line 185, "H73 sweep ready for next event") verified uniqueness BEFORE patch. Sister profile (qa-agent) uses H-row table format, operations-manager uses timestamp-line format — different anchor strategies, both safe.

**Pitfall:** DO NOT assume "no sibling write in 6h gap" when both profiles share cadence. Verify via file mtime + anchor uniqueness every sweep.

### H60 — Auto-Suspend Decision Window (H60→H65)

When a recommendation has been repeated 5+ times without action (H44 cadence-decay), escalate through the H55-final-warning → H60-auto-suspend-issued → H65-terminal progression. Track elapsed sweeps + token cost in the audit report so Orchestrator can decide. operations-manager audit (6h) tracks this window for Orchestrator visibility even when qa-agent (hourly) is the one running it. See `references/cadence-decision-windows.md`.

### H51 — By-Design Idle Rules

Three profiles are HEALTHY despite stale mtime by design: **coder** (no cron registered, event-driven only), **memory-curator** (cron writes to Obsidian not state.md), **default** (state.md reflects last session-end, not active agent). Apply H51 rules BEFORE counting "idle" profiles to get the true idle count requiring Orchestrator attention. See `references/cadence-decision-windows.md`.

## Output Format

Routing audit reports should include:

1. **Header:** Audit time, cadence, on-cadence status
2. **Three primary counts:** Stuck, Pending QA, Idle
3. **Cron registry health:** N active / N healthy / N errored
4. **Per-profile snapshot table:** Profile, mtime, idle hours, cron status, notes
5. **Cross-validation:** qa-agent H<N> reference
6. **Verdict:** System healthy / faults detected / no action required
7. **🟡 Bloat marker (when applicable):** if any profile state.md >200KB, surface compaction opportunity recommendation (non-blocking, escalation-permission-only). See `references/state-md-bloat-detection.md` for full trigger language and escalation format.

**30m heartbeat variant** (lite): 1-line summary + table only. No long bullet lists, no Audit Summary block. See `references/30min-heartbeat-pattern.md`.

## Pitfalls

- **DO NOT** rely on file mtime alone for "idle" metric. File mtime ≠ cron truth. A profile may have stale mtime (10d) but fresh cron activity. Always cross-check with `hermes cron list`.
- **DO NOT** treat "no recent activity" as a fault. System may be intentionally dormant (no tasks pending = healthy idle).
- **DO NOT** re-state the same cadence recommendation >5 times. Apply H44 cadence-decay.
- **DO NOT** fabricate state.md rows to fill gaps. If history was overwritten by a sibling cron (H6 lesson: daily backup cron ran `git checkout` mid-sweep), treat file-as-truth per H25 NO-OP principle.
- **DO NOT** full-read qa-agent/state.md on 30m cadence — it's 50KB-200KB+, will hit 100K char limit. Use `offset = total_lines - 100, limit = 100` to get only the latest H rows. **If file size is already >100K bytes, `read_file` will refuse** — fall back to `terminal: tail -120` to extract the latest H rows. **Detect bloat early** with `wc -c ~/.hermes/profiles/*/state.md` and surface a 🟡 BLOAT marker when any file >100K. When qa-agent/state.md >200K, bloat has reached compounding territory — escalate to user for compaction (see `references/state-md-bloat-detection.md` for full recipe and thresholds).
- **DO NOT** write to ANY state.md file from the heartbeat cron — read-only by design, sibling-collision-safe with qa-agent's write-only hourly gate.
- **DO** run `hermes cron list` FIRST before reading profile state.md. Ground truth before structural signals.
- **DO** cross-validate with qa-agent H<N> most recent verdict. Independent verification per H38 lesson.
- **DO** keep heartbeat output to 1-line + table format — user explicitly requested this.

## Related

- `~/.hermes/profiles/operations-manager/state.md` — Full audit history (H1-H57+)
- `~/.hermes/profiles/qa-agent/state.md` — Independent cross-validation source
- Hermes docs: https://hermes-agent.nousresearch.com/docs/user-guide/profiles

## Support Files

- `references/cron-fault-taxonomy.md` — Detailed H34 codification with examples
- `references/false-positive-triage-recipes.md` — H5/H10 false-positive patterns
- `references/real-time-cron-fire-detection.md` — H56 technique: detect crons that fired within seconds of audit (strongest live-health signal)
- `references/30min-heartbeat-pattern.md` — LITE variant for Orchestrator Heartbeat cron (30m cadence, read-only, 1-line + table output). Includes **H70 CRITICAL-grep false-positive triage** (regex matches `### CRITICAL (0)` zero-count headers — always context-inspect before declaring a finding).
- `references/cadence-decision-windows.md` — H50 (pre-fire window) + H60 (auto-suspend decision window H60→H65) + H51 (by-design idle rules: coder-no-cron, memory-curator-obsidian, default-active-sessions)
- `references/state-md-bloat-detection.md` — Three-tier bloat detection (50K/100K/200K) + `read_file` 100K refusal workaround (`terminal tail` recipe) + compaction trigger thresholds + escalation message format
- `references/state-md-editing-pitfalls.md` — Anchor-uniqueness recipe for `patch()` (7-match collisions on repeated H50 PRE-FIRE lines) + multi-line context anchor pattern + patch tool's offset/limit pagination warning + frontmatter timestamp drift (H36) + sibling-collision rules for state.md writes
- `references/kanban-stuck-task-triage.md` — Procedure for triaging stuck kanban tasks (Check #2 in 7-check protocol). Three recoverability patterns (A/B/C) + CLI quick reference + t_3a73b0af real example. **Operations-manager is the ONLY sweep that catches stuck kanban tasks** — qa-agent's H28 scope discipline excludes kanban.
- `templates/audit-report-template.md` — Standard routing audit report format