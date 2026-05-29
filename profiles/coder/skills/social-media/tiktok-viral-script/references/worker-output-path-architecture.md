# Worker Output Path Architecture (2026-05-10)

## The Problem

`tiktok-viral-script` skill documents:
```
~/hermes/workers/content-creator/outputs/YYYY-MM-DD-[morning/evening]-brief.md
```

**Reality**: Workers write to cron output directories, NOT to `~/hermes/workers/*/outputs/`.

## Two Output Locations

| Location | Purpose | Status |
|----------|---------|--------|
| `/Users/tuananh4865/.hermes/cron/output/{job_id}/YYYY-MM-DD_*.md` | **PRIMARY** — where workers actually write | ✅ Working |
| `/Users/tuananh4865/hermes/workers/*/outputs/` | **SECONDARY** — often EMPTY even when workers ran | ❌ Gap |

## Known Cron Job IDs

| Job ID | Worker | Schedule | Actual Output Path |
|--------|--------|----------|-------------------|
| `ce3701b4dcdd` | Content Creator Morning | 8AM | `/Users/tuananh4865/.hermes/cron/output/ce3701b4dcdd/` |
| `50bc2c2dfbb3` | Content Creator Evening | 6PM | `/Users/tuananh4865/.hermes/cron/output/50bc2c2dfbb3/` |
| `e4fb0c36e9f7` | Research Analyst Morning | 8:30AM | `/Users/tuananh4865/.hermes/cron/output/e4fb0c36e9f7/` |
| `1c425ba42980` | Research Analyst Evening | 6:30PM | `/Users/tuananh4865/.hermes/cron/output/1c425ba42980/` |

## Correct Path Usage

```bash
# WRONG — tilde doesn't expand in cron, AND it's the wrong directory
~/hermes/workers/content-creator/outputs/

# CORRECT — absolute path, correct directory
/Users/tuananh4865/.hermes/cron/output/ce3701b4dcdd/

# Check what's actually there
ls -lt /Users/tuananh4865/.hermes/cron/output/ce3701b4dcdd/*.md 2>/dev/null | head -5
```

## Root Cause

Workers are triggered by cron jobs. When cron fires, the worker runs and writes its output to the cron job's output directory (`~/.hermes/cron/output/{job_id}/`), NOT to the shared `~/hermes/workers/*/outputs/` directory.

The shared outputs/ directories were meant to be written by workers for the orchestrator to read, but the worker SOUL.md prompts never explicitly write to those paths — they just output content which gets captured by the cron system.

## Orchestrator Reading Pattern

The orchestrator reads from BOTH locations:
1. Cron output dirs (primary — always check first)
2. Shared outputs/ (secondary — often empty)

## Implication for Skill

When the skill says "write to `~/hermes/workers/content-creator/outputs/`", in practice this means:
- In cron context: output goes to cron output dir
- The orchestrator knows to read from cron dirs

For human-readable checks, look in cron output dirs:
```bash
ls -lt /Users/tuananh4865/.hermes/cron/output/*/2026-05-10*.md
```
