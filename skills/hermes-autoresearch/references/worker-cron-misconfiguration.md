# Worker Cron Misconfiguration — Discovery, Fix & Verification (2026-05-06)

## Status: FIXED ✅

All 7 cron jobs corrected on 2026-05-06 20:01. This reference documents the pattern for future use.

## The Problem

**All 7 worker/orchestrator cron jobs ran `hermes-autoresearch` instead of worker-specific prompts.**

This was discovered on 2026-05-06 morning scan — workers had empty outputs/ directories despite having run multiple times.

## Cron Jobs Affected

| Job ID | Worker | Should Run | Was Running | Status |
|--------|--------|------------|-------------|--------|
| ce3701b4dcdd | Content Creator (8AM) | TikTok scripts, Gen Z trends | hermes-autoresearch | ✅ FIXED |
| 50bc2c2dfbb3 | Content Creator (6PM) | Script report | hermes-autoresearch | ✅ FIXED |
| e4fb0c36e9f7 | Research Analyst (8:30AM) | Product research | hermes-autoresearch | ✅ FIXED |
| 1c425ba42980 | Research Analyst (6PM) | Research report | hermes-autoresearch | ✅ FIXED |
| 045a44210a59 | Orchestrator (9AM) | Morning briefing | hermes-autoresearch | ✅ FIXED |
| f1584a9a1d86 | Orchestrator (every 2h) | Worker monitoring | hermes-autoresearch | ✅ FIXED |
| fc2191d508a3 | Orchestrator (9PM) | Nightly consolidation | hermes-autoresearch | ✅ FIXED |

## Root Cause

When workers were set up (SOUL.md + HEARTBEAT.md created), the cron jobs were NOT updated with worker-specific prompts. The cron jobs still pointed to `hermes-autoresearch` skill.

**"Workers configured" ≠ "Workers running"**

## How to Diagnose

```bash
# Check if cron output shows skill content (wrong) vs worker content (correct)
cat ~/.hermes/cron/output/{job_id}/*.md | head -30

# If output starts with skill frontmatter like "title: Hermes Autoresearch" → WRONG PROMPT
# If output starts with worker-specific briefing format → CORRECT

# Check worker outputs/ directory
ls -la ~/.hermes/workers/content-creator/outputs/
ls -la ~/.hermes/workers/research-agent/outputs/

# If empty despite cron running → likely wrong prompt
```

## How to Fix (VERIFIED 2026-05-06)

**CRITICAL: The command is `cron edit`, NOT `cron update`.** `cron update` does not exist.

```bash
# Full path required in cron/shell context:
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit {job_id} --prompt "$(cat ~/.hermes/workers/{worker}/SOUL.md)" --clear-skills
```

**For each worker cron:**

```bash
# Content Creator crons (2 jobs)
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit ce3701b4dcdd --prompt "$(cat ~/.hermes/workers/content-creator/SOUL.md)" --clear-skills
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit 50bc2c2dfbb3 --prompt "$(cat ~/.hermes/workers/content-creator/SOUL.md)" --clear-skills

# Research Analyst crons (2 jobs)
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit e4fb0c36e9f7 --prompt "$(cat ~/.hermes/workers/research-agent/SOUL.md)" --clear-skills
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit 1c425ba42980 --prompt "$(cat ~/.hermes/workers/research-agent/SOUL.md)" --clear-skills

# Orchestrator crons (3 jobs)
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit 045a44210a59 --prompt "$(cat ~/.hermes/workers/orchestrator/SOUL.md)" --clear-skills
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit f1584a9a1d86 --prompt "$(cat ~/.hermes/workers/orchestrator/SOUL.md)" --clear-skills
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit fc2191d508a3 --prompt "$(cat ~/.hermes/workers/orchestrator/SOUL.md)" --clear-skills
```

**Verify after fix:**
```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list
# All 7 jobs should show: Skills: none (not hermes-autoresearch)
```

## The Correct Pattern

Worker cron prompt should be:
1. Worker role definition (from SOUL.md)
2. Worker task specifics (from HEARTBEAT.md)
3. Output format instructions
4. Where to write results (outputs/)

NOT `hermes-autoresearch` which is for self-improvement research.

## Lesson Learned

Creating SOUL.md + HEARTBEAT.md files is NOT sufficient to make workers autonomous.

**Every new worker cron job must:**
1. Have a worker-specific prompt (not a skill)
2. Write to the worker's outputs/ directory
3. Be verified to produce output after running
