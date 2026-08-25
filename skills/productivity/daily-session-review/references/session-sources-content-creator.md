---
title: Session Title Patterns for Content Creator Review
date: 2026-06-29
type: reference
tags: [session-filter, content-creator, cron-jobs]
---

# Session Title Patterns — Content Creator Context

## Sessions to SKIP (non-Content Creator, pollute keyword matches)

These cron job types generate too much noise and are never relevant for Content Creator research:

| Pattern | Reason |
|---------|--------|
| `%Heartbeat%` | Orchestrator ping-pong, 30-min intervals, no content decisions |
| `%Routing Audit%` | Operations Manager routing check |
| `%Quality Gate%` | QA Agent verification |
| `%Vuln Scan%` | Security Engineer scan |
| `%Cleanup%` | Orchestrator weekly cleanup |
| `%Backup%` | Hermes Daily Backup |
| `%Consolidation%` | Memory Curator nightly |

## Sessions to CHECK (Content Creator relevant)

These sessions are the primary sources for Content Creator daily review:

| Session title pattern | Source | What it contains |
|---------------------|--------|------------------|
| `%TikTok 5-Channel%` | cron | TikTok Shop trending + YouTube search trends |
| `%YouTube Search Trends%` | cron | Gear review research per day-of-week keyword |
| `%TikTok Shop%` | cron | TikTok Shop product trending |
| `%Nightly Monitor%` | cron | Multi-channel monitoring including TikTok |
| `%Autoresearch%` | cron | May contain Content Creator research from previous night |
| `%Nightly Reflection%` | cron | Orchestrator review of previous day |
| `%Daily Briefing%` | cron | Orchestrator daily briefing — may reference Content Creator |
| `%Trend Scan%` | cron | Research Lead trend scanning |
| (null title) | cron | May be ad-hoc sessions — check content for keywords |

## How to identify Content Creator sessions

1. First filter by title patterns (pre-filter above)
2. Then search message content for Content Creator keywords
3. Key indicators in content:
   - File paths containing `Content Creator/Research/`
   - Keywords: `mic`, `đèn`, `gimbal`, `TikTok Shop`, `Shopee Affiliate`, `review`, `test`
   - Cron job instructions referencing Content Creator context

## Related
- [[daily-session-review]]
- [[session-db-schema]]
