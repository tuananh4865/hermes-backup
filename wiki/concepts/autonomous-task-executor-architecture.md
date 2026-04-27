---
title: Autonomous Task Executor Architecture
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [automation, agent, cron, task-management]
sources: [raw/transcripts/2026-04-11/2026-04-11-7h30-sng-hng.md]
confidence: high
---

# Autonomous Task Executor Architecture

## Executive Summary

The wiki's autonomous task system failed because `task_checker.py` only **listed** tasks without executing them. A new `autonomous_task_executor.py` was built that spawns Claude Code subagents to actually execute tasks, achieving real autonomous operation.

## The Problem

```
task_checker.py --autonomous
```

This command was assumed to execute tasks autonomously. In reality, it only:
1. Loaded task state
2. Got task list
3. Built proposal (displayed)
4. Saved last check
5. Logged

**Zero execution happened.** Cron ran this, saw no tasks completed, moved on.

## The Solution

`autonomous_task_executor.py` — spawns Claude Code print-mode subagent to execute tasks:

```python
cmd = [
    'claude', '-p', prompt,
    '--output-format', 'json',
    '--max-turns', '5',
    '--dangerously-skip-permissions'
]
```

For system tasks (like wiki lint), direct commands work better:
```python
if task_type == 'system':
    prompt = f"Run this exact command in ~/wiki directory:\ncd ~/wiki && python3 scripts/wiki_lint.py --auto-fix 2>&1"
```

## Execution Flow

```
Cron job triggers
    ↓
task_checker.py (lists + filters)
    ↓
autonomous_task_executor.py (spawns subagent)
    ↓
Claude Code subagent executes task
    ↓
Result logged → git commit if changed
    ↓
deep_research.py (if no tasks left)
```

## Task Filtering

35 of 51 tasks were user-dependent (required account creation, credentials, etc.):
- "Configure Turso database" — needs user Turso account
- "Set up Vercel env vars" — needs user credentials
- etc.

Only 16 tasks were truly autonomous-executable.

## Test Results

| Task | Result | Time |
|------|--------|------|
| Fix 89 wiki lint issues | ✅ SUCCESS | 13s |
| Restart watchdog daemon | ✅ SUCCESS | ~5s |

## Key Insights

1. **Documentation ≠ Execution** — A skill/script that describes workflow is not the same as one that executes it
2. **Subagent pattern** — Spawning Claude Code with `--dangerously-skip-permissions` enables true autonomous execution
3. **Task classification** — Must separate user-dependent vs autonomous-executable tasks
4. **Timeout handling** — 180s timeout for Claude Code subagent (5 min was too long, 60s too short)

## Related

- [[autonomous-wiki-agent]] — The skill that triggered this discovery
- [[wiki-self-heal]] — Wiki health maintenance
