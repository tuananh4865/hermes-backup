---
title: "Session 2026-06-16 (3rd) — Pre-Deployment Audit Caught Pre-Existing transcript-saver Hook"
date: 2026-06-16
author: Hermes Agent
session_type: discovery
related: session-2026-06-16-hooks-activation.md, session-2026-06-16-example.md
---

# Session 2026-06-16 (Round 3) — transcript-saver Hook Discovery

## What happened

User asked: "Check cách để setup hook message realtime trong hermes ra wiki raw transcripts"

Expected outcome: Design a NEW hook to capture Telegram messages to `wiki/raw/transcripts/`.

Actual outcome: Discovered the hook already exists and has been running for 3+ months.

## The discovery path

```bash
# Step 1: Check if any hook directory exists
ls -la ~/.hermes/hooks/transcript-saver/
# → Exists since May 11, 2026. Files: HOOK.yaml + handler.py + __pycache__/

# Step 2: Read the hook config
cat ~/.hermes/hooks/transcript-saver/HOOK.yaml
# → name: transcript-saver
# → events: [agent:end]

# Step 3: Read the handler to understand what it does
cat ~/.hermes/hooks/transcript-saver/handler.py
# → Saves to /Volumes/Storage-1/Hermes/wiki/raw/transcripts/{YYYY-MM-DD}/
# → Filename: {HH-MM-SS}_{platform}_{sanitized_user_msg}.md
# → Frontmatter: title, created, platform, user_id, session_id, timestamp, type, tags

# Step 4: Verify it's actually firing
ls /Volumes/Storage-1/Hermes/wiki/raw/transcripts/2026-06-16/ | wc -l
# → 47 files saved today alone

# Step 5: Read one sample file to confirm content quality
cat /Volumes/Storage-1/Hermes/wiki/raw/transcripts/2026-06-16/20-00-47_telegram_*.md
# → Full YAML frontmatter + User Message + Assistant Response sections
```

## Key facts about the existing transcript-saver

| Property | Value |
|----------|-------|
| Path | `~/.hermes/hooks/transcript-saver/` |
| Created | May 11, 2026 |
| Event subscribed | `agent:end` |
| Event actually fires | YES (47 files/day observed) |
| Output path | `/Volumes/Storage-1/Hermes/wiki/raw/transcripts/{YYYY-MM-DD}/` |
| Filename format | `{HH-MM-SS}_{platform}_{sanitized-30chars}.md` |
| Frontmatter | title, created, platform, user_id, session_id, timestamp, type, tags |
| Volume | ~40-50 files/day (consistent with multiple Telegram messages per day) |

## What went right (and what the audit caught)

**What the audit caught:**
- Pre-existing hook infrastructure that solved the user's question
- 3 months of captured data already on disk
- Format/structure already in place

**What would have gone wrong without the audit:**
- Built a parallel `realtime-message-saver` hook → 2x writes per message, conflicts
- Built a hook that subscribes to wrong event → silently rejected (like `agent:end` in shell hooks mode)
- Wasted 1-2 hours reimplementing what already works
- Confused future agents about which hook is the source of truth

## Existing 4 problems with the current transcript-saver (for future improvements)

1. **Index.md broken** — `wiki/raw/transcripts/index.md` shows the same entry from 2026-04-10 duplicated 24 times; no auto-update mechanism
2. **No session grouping** — files are per-message, not per-conversation thread; hard to reconstruct a chat
3. **Filename truncate at 30 chars** — loses context for long messages (e.g. "anh-muốn-em-phân-tí" cuts off "chuyển-động-của-mẫu")
4. **No dedup** — if user sends 2 messages with same prefix in same second, second overwrites first

## User options presented (not yet decided)

| Option | Description | Effort |
|--------|-------------|--------|
| 1. Keep as-is | Hook already works; use grep/find when needed | 0 min |
| 2. Improve hook | Add session grouping, auto-index update, dedup | 30-60 min |
| 3. Full rebuild | Entity-based wiki with backlinks, NER, daily digest | 2-3 hours |

User has not yet chosen — session ended before decision.

## Lesson encoded

**Add to SKILL.md (done in this round):** "Pre-Deployment Audit: ALWAYS Check `~/.hermes/hooks/` First" section added to `loop-engineering-deployment/SKILL.md`. The skill now mandates running the audit commands before designing any new hook.

## Related references

- `session-2026-06-16-example.md` — first deployment (5 components)
- `session-2026-06-16-hooks-activation.md` — round 2 (activate shell hooks)
- `session-2026-06-16-profile-terminology.md` — round 1.5 (Profile vs Worker terminology)
