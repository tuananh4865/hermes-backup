---
title: Session Sources — Primary vs Fallback (2026-06-25)
created: 2026-06-25
updated: 2026-06-25
type: reference
tags: [daily-session-review, session-search, cron]
confidence: high
relationships: [daily-session-review/SKILL.md]
---

# Session Data Sources — 2026-06-25 Discovery

## Primary Source: wiki/log.md (BEST for recent activity)

**Why:** `wiki/log.md` is the most reliable source for recent session activity. Cron jobs append to it at completion. The last ~20 lines give you a fast, clean summary.

```bash
tail -20 /Volumes/Storage-1/Hermes/wiki/log.md
```

**What it contains:**
- Timestamp + job name + summary of what was done
- Failures, decisions, file outputs
- Updated field auto-incremented

**When to use:** Primary source for any daily review. Fast, clean, no payload noise.

## Secondary Source: session_search tool (SEARCH tool, not SQLite)

**sessions.db is EMPTY — DO NOT use SQLite directly:**
```
-rw------- 1 tuananh4865 staff 0 May 31 00:03 ~/.hermes/sessions/sessions.db
→ 0 bytes, no tables
```

**Correct tool: `session_search`** — searches across JSON session files in `~/.hermes/sessions/`

```python
session_search(query="mic đèn gimbal TikTok Shop", limit=5, sort="newest")
```

**Problem:** Even targeted queries return 200KB+ payloads because cron heartbeat messages contain the full system prompt (hermes-agent skill, quality-checker skill — both 1000+ lines).

**Workaround:**
1. Read the `preview` snippet field first (1500 chars max)
2. Use `session_id` + `around_message_id` + `window=5` to scroll into specific sessions
3. NEVER try to read the full persisted output file — it's a trap

**Sequential query strategy (3 queries, not 1):**
1. `mic đèn gimbal lens flycam action cam TikTok Shop Shopee Affiliate review test`
2. `gimbal mic đèn review gear content creator`
3. `TikTok shop affiliate content creator`

## Tertiary: Research files on disk

```
~/Workspace/Claude/Projects/Content Creator/Research/{YYYY-MM-DD}/
```

**Files found for 2026-06-24:**
- `daily-session-review.md` — previous day's review (carry-over gaps)
- `shopee-deal-lighting.md` — Shopee lighting trending research
- `youtube-trending-gimbal-2026-06-24.md` — YouTube gimbal trending

## Session Categories (from cron heartbeats observation)

| Source | Title pattern | Noise level |
|--------|--------------|-------------|
| `source: cron` | "Orchestrator Heartbeat", "QA Agent", "AutoResearch" | HIGH (full system prompt) |
| `source: telegram` | User sessions | LOW (actual content) |
| `source: cli` | Interactive sessions | LOW (actual content) |

**Filter for real user content:** Prefer `source:telegram` in session_search query, but Content Creator research cron jobs are also valid content (source=cron but topic=research).

## Key insight from 2026-06-25 run

The `cron_4ea08c530657_20260624_230012` "Orchestrator Nightly Reflection" session (90 messages) was NOT a Content Creator session — it was a system self-reflection. The actual Content Creator sessions from 2026-06-24 were:
1. `shopee-deal-lighting.md` research (cron job output file)
2. `youtube-trending-gimbal-2026-06-24.md` research (cron job output file)
3. `daily-session-review.md` carry-over from previous day

**Lesson:** Research output FILES are often more useful than session transcripts for Content Creator context. Check both.
