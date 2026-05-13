# Worker Dual-Path Discovery (2026-05-13)

## The Problem
During orchestrator session (May 13, 2026), agent checked for worker outputs:
- Looked at `/Users/tuananh4865/.hermes/workers/content-creator/outputs/` — EMPTY
- Looked at `/Users/tuananh4865/hermes/workers/content-creator/outputs/` — HAS FILES

The content creator had produced output but agent reported "no new content" because it only checked one path.

## Root Cause
Workers write to `/Users/tuananh4865/hermes/workers/*/outputs/` (primary path from worker SOUL.md).
But the orchestrator and skill docs referenced `/Users/tuananh4865/.hermes/workers/*/outputs/` (secondary path from cron context).

These may be:
1. The SAME directory (if `.hermes` is a symlink to `hermes`)
2. DIFFERENT directories (two separate directories)
3. Neither — the actual canonical path differs from what cron context suggests

## Verification Pattern
```bash
# ALWAYS check BOTH paths when looking for worker outputs
ls -la /Users/tuananh4865/hermes/workers/{worker}/outputs/ 2>/dev/null | head -5
ls -la /Users/tuananh4865/.hermes/workers/{worker}/outputs/ 2>/dev/null | head -5

# If outputs appear in ONLY one path, document which is canonical
# If outputs appear in BOTH, they may be symlinked
ls -la /Users/tuananh4865/.hermes/workers/ | grep hermes
```

## Status (2026-05-13)
- Content Creator outputs confirmed at: `/Users/tuananh4865/hermes/workers/content-creator/outputs/`
- Last file: `2026-05-13-morning-content.md` (7029 bytes, created 08:02)
- Research Agent outputs at: `/Users/tuananh4865/hermes/workers/research-agent/outputs/`
- Last file: `2026-05-12-evening-brief.md` (10753 bytes, created May 12 14:08)

## Action Required
Update all worker-checking logic to use the correct canonical path:
`/Users/tuananh4865/hermes/workers/{worker}/outputs/`
