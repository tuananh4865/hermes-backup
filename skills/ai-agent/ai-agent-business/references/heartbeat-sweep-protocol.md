---
title: Orchestrator Heartbeat Sweep Protocol
created: 2026-06-24
updated: 2026-06-24
type: reference
tags: [heartbeat, sweep, orchestrator, multi-agent, ops, monitoring, security, drift]
status: battle-tested
session_origin: 2026-06-24 08:31 orchestrator 30m heartbeat (H11 sweep)
---

# Orchestrator Heartbeat Sweep Protocol

> **This file is the operational playbook for the periodic "heartbeat" cron that runs while the user is away.** When SOUL.md or the cron job says "run a 30m heartbeat check", follow these 6 steps. The umbrella `ai-agent-business` skill gives the *what* (heartbeat = agent works while you sleep); this file gives the *how* (the actual sweep procedure + the 3 pitfall classes that quietly eat correctness).

## When to use

- Cron job fires with prompt like "30m heartbeat", "30-minute check", "periodic sweep", "agent health check"
- User says "check on the agents", "sweep status", "orchestrator heartbeat"
- `HEARTBEAT.md` schedule lists a sweep at this cadence (typically 30m, 2h, or 6h)

## The 6-step sweep procedure

Run in order. Each step is a single parallel batch of tool calls where possible.

### Step 1 — Read state.md of all active profiles (parallel)

Read N `~/.hermes/profiles/<name>/state.md` files in a single batched tool call. Active profiles are the ones listed in the heartbeat prompt (for this user: `qa-agent`, `engineering-lead`, `operations-manager`, `code-reviewer`, `security-engineer`).

**Why batch:** N reads are independent → one tool round-trip.

**What to extract from each:**
- `## Current Goal` (should be `None` for idle)
- `## Active Tasks` / `## Pending Tasks` / `## Blocked Tasks` tables (rows + last update mtime)
- `## Handoff History` (rows where mtime > 2h = needs nudge)
- Most recent verdict in the verdict table

**Output:** A mental model of "who is doing what" before you touch anything.

### Step 2 — Find tasks pending >2h, nudge the agent

For each task in any profile's `## Pending Tasks` or `## Handoff History` table where `mtime > 2h`:

1. Check the assigned profile's last activity mtime.
2. If the profile is idle but the task is unowned, **route it** to the right maker via `kanban` (use `multi-agent-orchestrator` skill for the routing decision).
3. If the profile is busy on something else, **flag it** in your report — do not preempt.
4. If the task has been pending >24h, **escalate** to the user (don't silently let it rot).

**Anti-pattern:** Do not nudge the maker directly via `send_message` — the heartbeat should produce a *report*, not a chat. The next cron tick will pick up the report and act. Nudging in real time steals the user's attention budget.

### Step 3 — Find outputs waiting qa-agent verification, route to qa-agent

Look for files in `~/.hermes/profiles/*/outputs/`, `~/hermes/workers/*/outputs/`, or any `*/deliverables/` dir that are:
- Newer than qa-agent's last sweep (mtime comparison)
- Not yet in qa-agent's `## Verdict History` table

For each:
1. Run `kanban` (or your routing layer) to create a verification task assigned to qa-agent with the file path.
2. Log the route in your report.

**Anti-pattern:** Do NOT read the output file and self-verify. The point of the heartbeat is *routing*, not redoing qa-agent's job. Independent verification is the whole point.

### Step 4 — Check for security CRITICAL findings, auto-fix per owner authority

Run the security-engineer 7-category checklist (perms, secrets, dangerous patterns, deserialization, etc.) but **only the cheap, idempotent subset** — full scan is a separate cron at 03:00.

**Perm-drift regression check (NEW — discovered 2026-06-24):**

Security files that were hardened to 600/700 can silently regress to 644 if any code path rewrites them (config.yaml is the most common offender). Check:

```bash
# One command, lists the 6 files security-engineer monitors
ls -la /Users/tuananh4865/.hermes/config.yaml \
       /Users/tuananh4865/.hermes/auth.json \
       /Users/tuananh4865/.hermes/state.db* \
       /Users/tuananh4865/.hermes/.env 2>/dev/null | awk '{print $1, $NF}'
```

Compare to security-engineer's last sweep findings (read `~/.hermes/profiles/security-engineer/state.md` § Daily Scan Findings). Any file that was 600/700 and is now 644 = **drift regression**.

**Auto-fix protocol (per owner authority):**
- Severity LOW (perm tightening only) → `chmod 600 <file>` immediately, log in report
- Severity MEDIUM (e.g. dangerous `shell=True` in active code) → log + escalate, do NOT auto-fix
- Severity HIGH/CRITICAL → log + halt heartbeat, escalate to user before any fix

**Why perm tightening is safe to auto-fix:** `chmod 600` is reversible, idempotent, and only tightens. It cannot delete data or expose secrets further. The opposite (`chmod 644`) IS the dangerous direction.

### Step 5 — Check for agent conflicts (2 agents on same file), auto-resolve

Look for:
- Lock files: `find ~/.hermes/profiles -name "*.lock"` — but **only count lock files held by live processes** (check `lsof | grep <lockfile>`). Stale lock files are noise.
- Concurrent edits: 2+ profile `state.md` modified in the same minute by different profiles
- Both engineering-lead AND coder writing to same file in last 5 min

**Resolution priority matrix (in order):**
1. **Severity** — security fix beats feature work beats cleanup
2. **Reversibility** — non-reversible beats reversible (the irreversible one wins because it must land first)
3. **Cost** — cheaper (in tokens / time) beats expensive
4. **Deadline** — closer deadline wins

**For the heartbeat, you almost never need to actually resolve anything** — the live lock holders usually sort themselves out within seconds. The check is for the rare case where two heartbeat-tier crons are scheduled at the same minute and race on `state.md` patching.

**Real failure (2026-06-24, H6 row in qa-agent state.md):** Daily backup cron ran `git checkout` mid-sweep, overwriting H6-H34 verdict history. The collision was visible in the file mtime delta after the fact. Preflight check (next pitfall) catches it before write.

### Step 6 — Report: N active, N stuck, N verified, N escalated

Output format the user expects:

```
**Heartbeat 30m — <ISO timestamp> | N active, N stuck, N verified, N escalated**

| Profile | Last Update | Idle | Status | Action |
|---------|-------------|------|--------|--------|
| <name>  | <mtime>    | <Xh> | <icon> | <1-line> |

**Security:** <PASS/FAIL> — <1-line summary, with auto-fix note if applied>
**Routing queue:** <N pending> → <N needs verification>
**Conflicts:** <None / list>
**Escalations:** <N> — <1-line each, with cron name if it's a cron fault>
```

Then **log the sweep** to qa-agent's `state.md` per the established H-row pattern (preflight check first — see Pitfall #3 below).

## 3 pitfall classes that quietly eat correctness

### Pitfall #1 — "I can't verify this" → silence (DON'T skip the sweep)

If you can't read a profile's state.md (file missing, permission error, lock), say so explicitly in the report. **Do not silently mark the profile as "active"** because you couldn't verify it was idle. The point of the heartbeat is to catch the missing case, not paper over it.

**Reporting pattern:**
> `<profile>` — UNVERIFIED: state.md read failed (`<error>`). Defaulting to idle but flagging for next sweep.

### Pitfall #2 — Cadence trigger: 7+ consecutive idle sweeps = reduce cron frequency

If you record 7+ consecutive idle sweeps (no stuck, no escalations, no security regressions), recommend reducing the cron frequency (e.g. hourly → 6h). The user has explicitly asked for this in 2026-05-06 sessions.

**Pattern:** After H7, H8, H9, ... include in your report:

> **CADENCE TRIGGER FIRED AGAIN: N consecutive idle sweeps (H1-H<N>)** — recommendation to reduce `<profile>` cron from `<X>` to `<Y>` persists.

Do NOT actually change the cron yourself — the user owns that decision. Just surface the count.

### Pitfall #3 — state.md preflight check before appending (the H35-class collision)

**Symptom of a collision:** You `patch` your row into `state.md`, then 5 minutes later another sweep (or worse, a daily backup cron doing `git checkout`) reverts the file. Your row vanishes. The next sweep thinks the count is H<N>-1 and writes a duplicate.

**Real failure (2026-06-24, qa-agent H6 row):** Daily backup cron ran `git checkout 05ed1c9a9` over 22h of accumulated H6-H34 verdict history. The agent's patch attempt hit a merge conflict with the checkout, and the backup process kept the committed version. The H6 row existed in git commit 05ed1c9a9 but not in the working file. Result: subsequent sweeps couldn't detect the collision and re-wrote a "new" H6.

**Preflight check (run before every state.md patch):**

```bash
# 1. Check file size stability
SIZE_BEFORE=$(stat -f "%z" ~/.hermes/profiles/<profile>/state.md)
# 2. Check frontmatter `updated:` hasn't been reset by a backup
grep "^updated:" ~/.hermes/profiles/<profile>/state.md
# 3. Check the verdict table is well-formed (no orphan rows)
grep -c "^| H[0-9]" ~/.hermes/profiles/<profile>/state.md
```

If `size` jumped by >10KB without you expecting it, or `updated:` is older than your last sweep, **read the file in full first** before patching. Do not assume the file looks like the cached version in your context.

**After-append verification (catches it after the fact):**

```bash
# 4. Confirm your row made it
grep -F "<your unique marker>" ~/.hermes/profiles/<profile>/state.md
# 5. Confirm file is still parseable (no truncated row)
tail -1 ~/.hermes/profiles/<profile>/state.md
```

If step 4 misses, your write collided. Re-read, re-write, log the collision in your report so the user knows.

## Outputs the heartbeat should produce

1. **A 1-line summary + table** delivered to the user (Telegram, terminal, or wherever the cron is wired). Format above.
2. **A new row in the qa-agent (or designated) state.md** with verdict N/A, score N/A, issues 0, subject = "(heartbeat — no pending)" and a Notes column with the full sweep summary.
3. **A new row in the operations-manager state.md** if you're running as ops-manager (the "6h audit" pattern). Same shape.
4. **Optional: append to loop-engineering/CHANGELOG.md** if any auto-fix was applied (so the audit trail picks it up).

## Anti-patterns

- ❌ **Silently fixing all perm drift without logging it.** The user wants to know if the heartbeat applied ANY side effect. Always include a security section in the report.
- ❌ **Nudging agents in real time** ("Hey engineering-lead, your task is 2h old"). The heartbeat reports, the next cron acts.
- ❌ **Reading output files to "preview" verification.** Trust qa-agent's job. Your job is routing, not pre-verification.
- ❌ **Skipping the sweep because the system looks idle.** Idle is the most common state, and the heartbeat's value is precisely the regression check (Pitfall #3, security drift). Skipping when idle defeats the purpose.
- ❌ **Reporting "0 stuck, 0 escalated" without evidence.** The user wants to see the per-profile mtime table. "All clear" without numbers = unverified claim.

## Connection to other skills

- `ai-agent-business` (umbrella) — the *what* and *why* of heartbeat
- `multi-agent-orchestrator` — when the heartbeat finds work to route
- `self-verify-after-workaround` — applies for the auto-fix step (verify chmod actually applied via `stat`)
- `hermes-agent-decision-guard` — when a borderline call (auto-fix vs escalate) needs a rule
- `kanban-orchestrator` — when the heartbeat creates kanban tasks for routing

## Session reference

- `references/session-2026-06-24-orchestrator-heartbeat-h11.md` — the H11 sweep that produced this file. Includes the exact `chmod 600` call, the table format, the state.md preflight result, and the cadence-trigger wording.
