---
title: Social Media Trend Research — Last 30 Days
name: social-media-trends
created: 2026-06-01
updated: 2026-06-01
type: skill
tags: [research, social-media, youtube, x-twitter, trending, content-research]
description: Research trending topics, viral content, and emerging patterns on YouTube and major social platforms within a 30-day window. Use platform-native tools before web search.
trigger: Research trending content on YouTube, X (Twitter), or other social platforms within the last 30 days
---

> Researches trending topics, viral content, and emerging patterns on YouTube and major social platforms within a 30-day window.

## When to Use This Skill

Anh asks for:
- "YouTube trends" / "xu hướng YouTube"
- "content trending trên X" / "X trending topics"
- "video viral tuần này"
- "research YouTube" or "research social media"
- Anything involving YouTube, X/Twitter, TikTok performance data

**Always use this BEFORE generic web search when the query involves YouTube or social platforms.**

---

## Research Flow

### Step 1: Identify Target Platform(s)

| Platform | Primary Tool | Notes |
|----------|-------------|-------|
| YouTube | YouTube Studio Analytics, YouTube Trending, vidIQ | Trending tab, search within last 30 days |
| X/Twitter | X search, X trending API | Use `since:` filter for 30-day window |
| TikTok | TikTok Creative Center, trending sounds | Country-specific |
| General social | web_search with site: operators | Fallback only |

### Step 2: Platform-Specific Search

**YouTube (use these sources, NOT just web search):**
```
# YouTube search with date filter
site:youtube.com "topic" after:2026-05-01

# YouTube Trending pages by category
https://www.youtube.com/feed/trending

# vidIQ for competitor research + trends
https://vidiq.com/youtube-trends/
```

**X/Twitter:**
```
site:x.com OR site:twitter.com "topic" since:2026-05-01

# X advanced search
https://twitter.com/search?q=topic%20since%3A2026-05-01
```

### Step 3: Synthesize Findings

Structure findings by:
- **Topics:** What themes are trending
- **Formats:** What content formats perform best
- **Timing:** When posts/videos perform best
- **Engagement signals:** Likes, comments, shares, watch time

### Step 4: Deliver in Anh's Format

Use Vietnamese. Focus on actionable content for TikTok affiliate.

---

## ⚠️ CRITICAL: Don't Just Web Search

Anh specifically corrected this: **web search alone is insufficient for YouTube/social research.**

Web search finds ARTICLES ABOUT YouTube — not YouTube's actual data.

**Required approach:**
1. Navigate to YouTube directly (youtube.com/trending, youtube.com/feed/subscriptions)
2. Use YouTube Studio Analytics if available
3. Use vidIQ/TubeBuddy for keyword/trend data
4. Use platform-native search (X advanced search, YouTube filters)
5. THEN supplement with web search for analysis/opinion

**Why this matters:** 
- Web search gives you "content about trending content" (filtered, delayed)
- Platform-native gives you "actual trending data" (fresh, direct)
- The difference is significant for timely content decisions

**Reference:** `references/youtube-research-platform-native.md` — detailed platform-native research approach

---

## Related

- [[agent-reach]] — Analyze engagement/reach metrics on social platforms
- [[tiktok-viral-script]] — TikTok content creation (complements this research)
- [[youtube-deep-dive-2026]] — YouTube strategy knowledge base

---

## Sources

- YouTube Trending: https://www.youtube.com/feed/trending
- vidIQ YouTube Trends: https://vidiq.com/youtube-trends/
- X Advanced Search: https://twitter.com/search-advanced
- TikTok Creative Center: https://ads.tiktok.com/business/creativecenter