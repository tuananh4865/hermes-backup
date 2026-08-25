# Dual-Output-Path Discovery (2026-05-14)

> Session: Autoresearch 2026-05-14 | Workers: Content Creator last fired May 13 18:02

## The Problem

Worker outputs appear in TWO locations:
1. **Cron output dir**: `/Users/tuananh4865/.hermes/cron/output/{job_id}/YYYY-MM-DD-*.md`
2. **Worker outputs/**: `/Users/tuananh4865/hermes/workers/{worker}/outputs/YYYY-MM-DD-*.md`

The slang sync loop in SKILL.md only checked `workers/*/outputs/`. But content may exist ONLY in cron output dir, making the sync loop silently pass (no new slang found) even when workers actually fired.

## Verified Paths (2026-05-14)

```bash
# CRON OUTPUT — where workers actually write first
ls -la /Users/tuananh4865/.hermes/cron/output/ce3701b4dcdd/2026-05-13*.md  # Content Creator
ls -la /Users/tuananh4865/.hermes/cron/output/e4fb0c36e9f7/2026-05-13*.md  # Research Agent

# WORKER OUTPUTS — confirmation copy (may be empty even when workers fired)
ls -la /Users/tuananh4865/hermes/workers/content-creator/outputs/
ls -la /Users/tuananh4865/hermes/workers/research-agent/outputs/
```

## Corrected Slang Sync Loop

```bash
# Check BOTH paths for fresh worker content
CRON_OUTPUT=$(ls -t /Users/tuananh4865/.hermes/cron/output/{job_id}/*.md 2>/dev/null | head -1)
WORKER_OUTPUT=$(ls -t /Users/tuananh4865/hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)

# Use whichever is newer
LATEST=""
for f in "$CRON_OUTPUT" "$WORKER_OUTPUT"; do
    [ -n "$f" ] && [ "$f" -nt "$LATEST" ] && LATEST="$f"
done

if [ -n "$LATEST" ]; then
    # Check for slang terms
    grep -iE "(Ối dồi ôi|Ra dại|Nam thư|lọ.*HOT|Các mom ơi|meoxink|thơm vãi|sống nổi|pin trâu)" "$LATEST"
fi
```

## Key Insight

**"Workers configured" ≠ "Workers fired"** — Having SOUL.md files ≠ workers producing output.
**"Cron output exists" ≠ "Worker outputs/ populated"** — Workers may write to cron dir but NOT to shared outputs/.

Always check cron output dir as primary source for slang sync.
