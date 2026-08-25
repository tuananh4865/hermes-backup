# Cron Job Model Parameter Bug — FIXED 2026-05-05

## Problem

Creating cron jobs with `model` parameter causes error:
```
'<' not supported between instances of 'str' and 'int'
```

## Root Cause

When `model` is passed as a dict like `{"model": "MiniMax-M2.7", "provider": "minimax"}`, the cron job system tries to compare it as a number.

## Solution

**Omit `model` parameter entirely** from `cronjob create`. Let the skill's default model be used.

```python
# WRONG — causes error:
cronjob create(
    model={"model": "MiniMax-M2.7", "provider": "minimax"},
    ...
)

# CORRECT — omit model:
cronjob create(
    name="Job Name",
    prompt="...",
    schedule="0 8 * * *",
    skills=["hermes-autoresearch"],
    ...
)
```

## Verified Working Pattern

All cron jobs created 2026-05-05 without `model` parameter:
- `ce3701b4dcdd` — Content Creator Morning Brief
- `50bc2c2dfbb3` — Content Creator Evening Report
- `e4fb0c36e9f7` — Research Analyst Morning Brief
- `1c425ba42980` — Research Analyst Evening Report
- `fc2191d508a3` — Orchestrator Nightly Consolidation
- `045a44210a59` — Orchestrator Morning Briefing
- `f1584a9a1d86` — Orchestrator Agent Monitor

All run successfully with MiniMax-M2.7 (skill default).

## If Non-Default Model Needed

If a specific job needs a non-default model, use the cron job's own configuration after creation, not the create call.
