---
title: Autoresearch 2026-05-24 — Complete Failure Night
created: 2026-05-24
type: reference
tags: [autoresearch, worker-death, web-search-failure]
confidence: high
---

# Autoresearch 2026-05-24 — Complete Failure Night

## What Happened

Tonight's autoresearch (2AM) was a complete write-off due to dual failures:
1. **Workers completely dead** — output directories EMPTY, not just stale
2. **Web search completely down** — mcp_exa (5 consecutive failures), web_search (400 errors)

## Worker Death Status — ESCALATED

**Previous (2026-05-22):** Workers stale 10+ days, directories had old files
**Tonight (2026-05-24):** Directories EMPTY — no files at all, not even old ones

This means cron jobs themselves have STOPPED FIRING entirely, not just producing stale output.

```
# Before (stale — old files exist):
$ ls -la /Users/tuananh4865/hermes/workers/content-creator/outputs/
-rw-r--r--  1 tuananh4865  staff  7009 May 11 08:XX 2026-05-11-morning-brief.md

# After (dead — no files at all):
$ ls -la /Users/tuananh4865/hermes/workers/content-creator/outputs/
# (empty — no output)
```

**This is beyond "stale" — this is TOTAL WORKER DEATH.**

## Web Search Failure Pattern

Both web search providers failed:
- `mcp_exa_web_search_exa`: "MCP server 'exa' is unreachable after 5 consecutive failures"
- `web_search`: HTTP 400 errors after 3 attempts
- `mcp_MiniMax_web_search`: Returns 400 errors

**Fallback options exhausted:** No web search possible for Gen Z slang, AI agent research, or anything else.

## Impact

- Gen Z slang sync: CANNOT sync (workers dead, no web fallback)
- AI agents research: CANNOT research (web search down)
- Session log analysis: Sessions directory empty (no sessions to analyze)
- All three research focuses blocked

## Git Commit

```
988c9b5be autoresearch 2026-05-24: Wiki clean (1829 files, 0 issues), 238 skills healthy, Workers DEAD (output dirs empty), web search down all night (mcp_exa, web_search failing)
```

## Recommendation

Anh needs to:
1. **Restart worker cron jobs** — content-creator, research-agent, orchestrator crons all dead
2. **Check web search providers** — both mcp_exa and web_search failing
3. Manual intervention required — autoresearch cannot self-recover from this state

## Key Lesson

The escalation path for worker death:
1. **Stale** (May 11-14): Old files exist, workers producing but not fresh
2. **Dead** (May 22): Old files gone, directories empty, cron jobs stopped firing
3. **Tonight confirmed**: No recovery possible without manual restart

This is now documented as "complete worker death" in the skill.