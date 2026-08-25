# Cron Audit Patterns

For cron jobs whose mission is **inspection / health-check** rather than research or automation. Examples: "operations-manager 6h routing audit", "qa-agent backlog check", "worker idle detector".

## Core problem

Audit runs have no shared state. Each run lands in a fresh session with zero chat history. The prompt must self-contain all paths, expected artifacts, and decision rules — OR the run will guess and fabricate.

## 4-step template

### 1. Inventory phase (parallel greps)

```bash
# State files the audit expects
find <wiki_root> -name "state.md" -not -path "*/.git/*"

# Role-named env stubs (live vs backup)
ls <secrets_root>/.env.<role>      # live
ls <secrets_root>/.env.<role>.backup  # backup only

# Worker directories (heartbeat tracking)
ls <workers_root>/<role>/
cat <workers_root>/<role>/HEARTBEAT.md

# Crontab self-check
cat <wiki_root>/.crontab | grep <job-name>
```

**Run all of these in one tool-call batch** — they're independent reads.

### 2. Classify each artifact

| Class | Meaning | Audit action |
|-------|---------|--------------|
| (a) live + has data | Real state to inspect | Count and report |
| (b) live + empty | State file exists but no activity | Report 0 + note "no activity since creation" |
| (c) backup-only | `.env.<role>.backup` exists, no live `.env` | Report 0 + flag "system not deployed" |
| (d) absent | No file, no backup | Report 0 + flag "never set up" |

**NEVER upgrade a class-(c) or (d) to a synthetic number.** If you find 0 worker state files, the report is "0 idle workers", not "3 idle workers (estimated from folder count)".

### 3. Honest report structure

```markdown
# <Role> — <Frequency> Audit

**Run:** YYYY-MM-DD HH:MM:SS TZ
**Audit window:** <window>

## Report

| Metric | Count |
|--------|-------|
| Stuck tasks (>Xh) | N |
| Pending QA (>Xh) | N |
| Idle agents (>Xh) | N |

## Detail
<one paragraph per metric explaining what was searched and why the count is what it is>

## Root cause
<why the system is in this state — missing infra, env stubs only, etc.>

## Recommendation
<what needs to be set up for the audit to produce real numbers>
```

### 4. Save routing log even on zero-data runs

Path: `wiki/cron/<role>-<frequency>-audit-<YYYY-MM-DD>.md`

This preserves the audit trail. Next run can grep for prior runs and detect "this has been broken for N days, escalating".

## Anti-patterns to refuse

- ❌ "3 workers found, all marked idle" — counting empty folders as workers
- ❌ "Estimated N stuck tasks based on git log age" — git log ≠ task queue
- ❌ Skipping the report because "nothing to report" — the absence IS the report
- ❌ Inventing recommendations that imply the system works ("restart the gateway") when the system was never deployed

## Decision rules when target system is ambiguous

If the cron prompt says "audit the X system" and X is ambiguous (could mean env stubs, worker folders, or a real process):

1. Search ALL candidate locations in one batch
2. If NONE have live data → report 0 + flag "X is referenced by name only, no live infrastructure"
3. If SOME have live data → audit ONLY the live parts, document the gaps
4. NEVER assume X is "the worker folders" or "the env stubs" without verification

## Provenance

Pattern derived from `operations-manager-6h-routing-audit` run on 2026-06-26. Multi-agent infrastructure was referenced via `.env.operations-manager.backup` and `.env.qa-agent.backup` only — no live state files, no workers with heartbeat tracking, no crontab entry for the audit itself. Honest zero-report with root-cause + recommendation was the correct deliverable. Adding this to the skill so future audits of unbuilt systems don't fabricate.