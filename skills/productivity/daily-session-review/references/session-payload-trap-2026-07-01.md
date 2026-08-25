---
title: session_search Payload Trap — 2026-07-01
date: 2026-07-01
type: reference
tags: [session-search, payload-trap, daily-session-review]
confidence: high
relationships: [daily-session-review/SKILL.md]
---

# session_search Payload Trap — 2026-07-01

## Problem

Keyword queries via `session_search` return 200-600KB payloads persisted to temp files. When read via `read_file`, these files show 0 lines because the actual content is wrapped in a `<persisted-output>` JSON block, not plain text.

**Symptoms:**
- `session_search(query="...")` returns 200KB+ of JSON
- `read_file` on the persisted temp path shows `0 lines`
- Tool preview snippets only show ~1500 chars
- Keyword content appears as `>>>` highlighted terms in the preview but the full session content is inaccessible

## Root Cause

Cron job sessions (especially heartbeats) contain the full system prompt (~1000 lines each for `hermes-agent` skill + `quality-checker` skill). Even targeted keyword searches match these prompts, inflating payloads.

## Solution

**Read previous day's `daily-session-review.md` first** — it gives yesterday's sessions, gaps, and action items in clean ~4KB. No payload parsing needed.

```bash
# Step 0: Always do this first
cat ~/Workspace/Claude/Projects/Content\ Creator/Research/{YYYY-MM-DD-1}/daily-session-review.md
ls ~/Workspace/Claude/Projects/Content\ Creator/Research/{YYYY-MM-DD-1}/
```

Then check research output files directly on disk (`youtube-trending-*.md`, `tiktok-shop-*.md`) — these are more useful than session transcripts for Content Creator context.

Only use `session_search` as a fallback:
1. `session_search(limit=5, sort="newest")` — browse recent sessions (small payload, preview snippets only)
2. Identify Content Creator session IDs from the list
3. `session_search(session_id="ID", around_message_id=X, window=5)` — targeted reads only

## When Previous Day's Review Is Missing

If `{YYYY-MM-DD-1}/daily-session-review.md` doesn't exist (e.g., first run), fall back to:
1. `session_search(limit=5, sort="newest")` — get session IDs
2. `session_search(session_id="ID", window=3)` — targeted reads, never full payloads
3. Check disk for research files: `ls ~/Workspace/Claude/Projects/Content\ Creator/Research/`

## Related

- [[daily-session-review]]
- [[session-sources-2026-06-25]] — earlier discovery of session_search payload issues
