# Session Notes — May 9, 2026 Evening Orchestrator Cron

## Key Finding: Documentation ≠ Execution

The orchestrator briefing doc has detailed TRÁHN QA enforcement and 600-char format limit documented. Yet the orchestrator STILL delivered a verbose ~800-char report.

### Root Cause
1. Cron job runs with frozen system prompt — cannot call skill_view
2. Reading docs ≠ executing checks
3. Bash gates exist as text, not invoked shell commands

### Pattern (seen across multiple sessions)
| Session | Rule | Executed |
|---------|------|----------|
| 2026-05-08 am | 3-bullet | ❌ |
| 2026-05-08 pm | TRÁHN gate | ❌ |
| 2026-05-09 | 600-char limit | ❌ |

**Documentation alone has NOT prevented failures.**

## Files Modified This Session
- `references/orchestrator-briefing.md` — PITFALL 16+17+18
- `SKILL.md` — path resolution fix (tilde → full path in cron)

## Source Locations (Check ALL Three)
1. `/Users/tuananh4865/hermes/workers/*/outputs/`
2. `/Volumes/Storage-1/Hermes/workers/*/outputs/`
3. `~/.hermes/cron/output/{job_id}/`
