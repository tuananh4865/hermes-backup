# YouTube Research — Platform-Native vs Web Search

> Created: 2026-06-01 | From session correction by Anh

## The Problem

When asked to research YouTube content, the agent ONLY used web search (Google/Bing results about YouTube).

**Anh's correction:** "Anh chỉ thấy em tìm kiếm trên mạng mà không tìm trong youtube hay các trang mạng xã hội lớn và nổi tiếng như X và Youtube"

This means: web search finds ARTICLES ABOUT YouTube — not YouTube's actual data.

## Correct Approach for YouTube Research

### Level 1: Platform-Native (REQUIRED first)

| Source | URL | What It Provides |
|--------|-----|-----------------|
| YouTube Trending | https://www.youtube.com/feed/trending | Real trending videos, categories |
| YouTube Studio | studio.youtube.com | YOUR channel analytics |
| vidIQ YouTube Trends | https://vidiq.com/youtube-trends/ | Trending keywords, competitor data |
| vidIQ Channel Analysis | https://vidiq.com/youtube-channels/ | Competitor benchmarking |
| YouTube Search Filters | youtube.com/results?search_query=topic | Actual videos, date filters |

**YouTube search with date filter:**
```
site:youtube.com "keyword" after:2026-05-01
```

### Level 2: Platform APIs (if available)
- YouTube Data API v3
- vidIQ API

### Level 3: Web Search (SUPPLEMENT only)
Web search for:
- Industry analysis articles
- Creator interviews/podcasts
- Expert commentary

**Never rely on web search alone for social platform research.**

## X/Twitter Research

### Platform-Native
- X Advanced Search: https://twitter.com/search-advanced
- X Analytics: twitter.com/[username]/analytics

### Search filters
```
site:x.com "topic" since:2026-05-01
site:twitter.com "topic" since:2026-05-01
```

### Tools
- Metricool (analytics)
- Social Blade (competitor)
- X API (if configured)

## Key Lesson

> **"Web search gives you content ABOUT trending — not actual trending data."**

For YouTube research: Navigate to YouTube.com directly, use vidIQ, use YouTube Studio. Then supplement with web search for analysis.

For X research: Use X advanced search, X analytics. Then supplement with web search.

---

## Related
- Skill: [[last30days]] — Trending content research
- Skill: [[agent-reach]] — Engagement/reach analysis
- Wiki: [[youtube-deep-dive-2026]] — YouTube strategy knowledge