# Profile Routing Audit (6h cron pattern)

**Verified:** 2026-06-23 00:00 — operations-manager 6h audit cron.

## Purpose

Periodic health check of all Hermes profiles to detect stuck tasks, pending QA, and idle agents. Runs as a cron-driven audit (operations-manager role).

## Workflow

### 1. Discover profiles
```bash
ls -d ~/.hermes/profiles/*/state.md
```

### 2. Read all state.md in parallel
Use `read_file` in a single batched tool block (10 files = 1 round-trip). Each profile's state.md contains:
- `updated` timestamp (frontmatter)
- `Active Tasks` table
- `Pending Tasks` table
- `Blocked Tasks` table
- Run history / verdict history

### 3. Classify profiles by 3 thresholds

| State | Criterion | Action |
|-------|-----------|--------|
| **Stuck task** | Task in `Active Tasks` with `Started` > 2h ago and no recent status update | Flag for escalation |
| **Pending QA > 1h** | Item handed off to `qa-agent` (or other verifier) with no verdict after 1h | Flag for follow-up |
| **Idle agent** | `updated` timestamp > 4h ago with no `Current Goal` and empty `Active Tasks` | Note as idle (NOT a failure if no tasks exist) |
| **Active** | `updated` within last 4h OR has active goal | Healthy |

### 4. Produce structured report (3-section format)

```
# 🔍 6H ROUTING AUDIT — YYYY-MM-DD HH:MM (cron)

| Metric | Count |
|--------|-------|
| 🟥 Stuck tasks (>2h pending) | N |
| 🟨 Pending QA verification (>1h) | N |
| 🟦 Idle agents (>4h) | N |
| 🟩 Active | N |

## Profile Activity Matrix
| Profile | Last Update | Idle | Status |
|---------|-------------|------|--------|

## Verdict
[One sentence interpretation + next action if any]
```

### 5. Update `operations-manager/state.md`
- Update frontmatter `updated` + `goal` fields
- Append audit entry to `## Routing Log`
- Add new `## Audit Summary` section with counts + verdict
- Add/refresh `## Profile Activity Matrix` table

## Idle ≠ Failure (KEY INSIGHT)

If no tasks have been routed to a profile, "idle" is expected — not a routing problem. Distinguish:
- **Idle + no current goal** = System dormant, not broken
- **Idle + had goal but stopped updating** = Possible failure, investigate
- **Stuck task** = Real problem regardless of profile activity

## Pitfalls

### 1. Don't confuse "no active tasks" with "routing broken"
After multi-agent experiments end (e.g., 2026-06-17 here), all profiles correctly report idle. Audit should NOT escalate — just note dormant state.

### 2. The default profile state.md is large (400+ lines of run history)
Read with `offset=1 limit=50` only — the frontmatter `updated` timestamp is enough for the activity matrix. Don't waste tokens on full history.

### 3. Read in parallel, not sequentially
Use a single batched `read_file` call for all profile state.md files. 10 files = 1 round-trip instead of 10.

### 4. Cron context: use absolute paths
Inside cron, `~/.hermes/profiles/*/state.md` may fail due to tilde expansion. Use `/Users/tuananh4865/.hermes/profiles/*/state.md` or `search_files(pattern='**/state.md', path='...')`.

### 5. self-update the audit log
The operations-manager profile audits ITSELF. The `Idle (self)` row in the matrix is normal — don't flag it as a problem.

## When to escalate vs when to stay silent

| Condition | Action |
|-----------|--------|
| Stuck task found | Flag to user with task ID + agent + duration |
| Pending QA > 1h | Flag to user with subject + handoff time |
| All idle, no recent goals | Report as "dormant system" — no escalation needed |
| Mixed: some active, some idle | Normal — just report activity matrix |

## Sample output (2026-06-23)

```
# 🔍 6H ROUTING AUDIT — 2026-06-23 00:00 (cron)
| Metric | Count |
| 🟥 Stuck tasks | 0 |
| 🟨 Pending QA | 0 |
| 🔵 Idle (>4h) | 8 |
| 🟢 Active | 1 (default) |
Verdict: System idle since 2026-06-17. No routing failures.
```