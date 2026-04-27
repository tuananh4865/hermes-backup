---
title: Topic Workflow Discussion
created: 2026-04-09
updated: 2026-04-12
type: concept
tags: [project-management, wiki, vibe-coding, agent-context, topic-workflow]
relationships:
  - 🔗 karpathy-llm-knowledge-base (extracted)
  - 🔗 user-profile (extracted)
relationship_count: 2
---

# Topic Workflow Discussion

## Overview

Critical workflow rule: **Never save to wiki on first/surface read.** Always research thoroughly first.

## Step-by-Step Process

### Step 1: Raw Capture (Immediate)
When Anh sends a topic:
1. Save raw to `raw/transcripts/conversations/[date]-[topic].md`
2. Done immediately, no analysis yet

### Step 2: Research (Before Wiki Save)
**MANDATORY** — Do thorough research:
- Read full sources, multiple sources, primary sources first
- Search for additional context
- Analyze: key insights, implications, connections, what was missed
- Evaluate: truth vs opinion vs speculation

### Step 3: Wiki Save (After Research)
Only after thorough analysis:
- Save refined synthesis + AI perspective to wiki concept page
- Include source citations
- Add related concept links
- Write in Vietnamese with English technical terms

### Step 4: Commit
Git add → commit → auto-push to GitHub

## Schema Requirements

Every concept page must have:
- `title`: Concept name
- `created`: YYYY-MM-DD
- `updated`: YYYY-MM-DD
- `type`: concept | personal | reference
- `tags`: [relevant, tags]

## Vietnamese Pronouns

- **Anh** = addressing the user (Tuấn Anh)
- **Em** = referring to self (the AI)

Never use "bạn" or "tôi".

## Related
- [[karpathy-llm-knowledge-base]] — Inspiration for this workflow
- [[user-profile]] — User preferences and context
