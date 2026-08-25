---
title: YouTube Trending Research — Content Creator Niche
name: youtube-trending-research
created: 2026-06-29
updated: 2026-06-29
type: skill
tags: [research, youtube, content-creator, trending, affiliate, tiktok]
description: Research YouTube trending videos for content creator gear niches (mic, light, gimbal, flycam, action-cam, lens) on a daily rotating keyword schedule. Produce structured reports for TikTok/Shopee affiliate.
trigger: Research YouTube trending content for content creator gear niches
---

# YouTube Trending Research

> Researches YouTube trending videos for content creator gear niches (mic, light, gimbal, flycam, action-cam, lens) on a daily rotating keyword schedule. Produces structured reports for TikTok/Shopee affiliate decisions.

## When to Use This Skill

Anh asks for:
- YouTube trending research for gear niches
- Daily cron job for content creator gear trends
- Top YouTube videos about mic/light/gimbal/flycam/action-cam/lens

**This is NOT the same as the TikTok trend scan** (which covers Gen Z slang, sounds, and algorithm updates). That job is `social-media-trends`. This skill is specifically about YouTube video research for product niches.

---

## Daily Keyword Rotation

| Ngày | Niche keyword |
|------|--------------|
| Thứ 2 (Monday) | review mic thu âm cho người mới |
| Thứ 3 (Tuesday) | đèn LED quay video giá rẻ |
| Thứ 4 (Wednesday) | gimbal điện thoại nào tốt |
| Thứ 5 (Thursday) | flycam cho người mới bắt đầu |
| Thứ 6 (Friday) | action cam nào đáng mua |
| Thứ 7 (Saturday) | lens cho máy quay vlog |
| Chủ nhật (Sunday) | best gear cho content creator 2026 |

---

## Research Flow

### Step 0: Ensure Wiki Directory Exists (Fable-5 Persistent Storage)
Before running searches, ensure the wiki queries directory exists:
```
mkdir -p /Volumes/Storage-1/Hermes/wiki/queries
```
This is mandatory for persistent storage per Fable-5 Pattern P2.

### Step 1: Identify Niche + Date

- Determine today's niche from the rotation table above
- Today's date: use actual current date for the report filename and dated sections
- Output path: `~/Workspace/Claude/Projects/Content Creator/Research/{YYYY-MM-DD}/youtube-trending-{niche}.md`

### Step 2: Run Parallel Search Queries

Run these queries in ONE assistant turn (batch all):

```
Query set A (YouTube search - Vietnamese):
- "review mic thu âm cho người mới" site:youtube.com
- "mic thu âm" review 2026 Vietnamese channel

Query set B (YouTube search - English/global):
- YouTube "review mic" "beginner" 2026 views likes
- YouTube trending mic review 2026 Vietnamese channel
- site:youtube.com "DJI Mic" "Rode Wireless" review June 2026

Query set C (TikTok comparison):
- TikTok "review mic" "người mới" 2026 Vietnam trending

Query set D (Google Trends):
- Google Trends "mic thu âm" Vietnam search volume June 2026

Query set E (Product-specific):
- YouTube "mic thu âm" "so sánh" 2026
- YouTube "Hollyland Lark" "DJI Mic Mini" review 2026
```

Minimum: 5-6 queries in parallel. More if time allows.

### Step 3: Apply 5-Source Rule Per Video

For each trending video found, ALL of these must be present:
1. YouTube search result — URL, view count, date posted
2. YouTube channel info — subscriber count, niche
3. Engagement metrics — like count, comment count (from snippet or description)
4. TikTok comparison — same product reviewed by any TikTok KOL?
5. Search trend data — Google Trends or YouTube trending list signal

If less than 5 sources found for a video → mark: CHƯA ĐỦ DỮ LIỆU

### Step 4: Quality Filters

- Video age: max 7 days old for true trending; 30 days acceptable for evergreen
- Channel credibility: 10K+ subs + engagement >3% (or mark: CHƯA ĐỦ DỮ LIỆU)
- View count context: High views alone is not enough — check channel credibility

### Step 5: Compile Report

Follow the exact output template below. Do NOT deviate.

---

## Output Template

```markdown
---
title: YouTube Trending — {Niche} — {YYYY-MM-DD}
date: {YYYY-MM-DD}
job: youtube-trending
niche: {mic|light|gimbal|flycam|action-cam|lens|weekly}
sources_count: {N}
confidence: high | medium | low
---

# YouTube Trending — {Niche} — {YYYY-MM-DD}

## TL;DR
- Video trending nhất: "{title}" bởi {channel} — {views} views
- Format đang hot: {so sánh|hướng dẫn|unbox|review}
- Search keyword tăng mạnh: "{keyword}" +{X}%
- Cơ hội cho anh: {gợi ý video nên làm}

## Top 10 YouTube videos trending

| # | Title | Channel | Subs | Views | Posted | Format | Affiliate? | Nguồn |
|---|-------|---------|------|-------|--------|--------|------------|--------|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... |

## Phân tích chi tiết
### #1. "{Title}"
- **Channel:** {name + subs + verification}
- **Engagement:** {likes/comments + retention nếu có}
- **Content format:** {so sánh 2 sản phẩm / hướng dẫn sử dụng / unbox / review chi tiết}
- **Hook pattern:** {cách mở đầu video}
- **Sản phẩm chính:** {list sản phẩm được review}
- **Có affiliate link không:** {có/không, nếu có thì dẫn tới đâu}
- **Bài học cho anh:** {rút ra điều gì cho content của mình}

### #2-#10: ...
(Tóm tắt ngắn gọn)

## Search Trend Analysis
- **Keyword tăng mạnh:** "{keyword}" tăng {X}% trong 7 ngày
- **Keyword đang giảm:** "{keyword}" giảm {X}%
- **Keyword mới nổi:** "{keyword}"

## So sánh với TikTok
- Cùng sản phẩm, KOL TikTok nào đã review?
- Format nào trending trên TikTok nhưng chưa có trên YouTube?
- Cơ hội cross-post?

## Nguồn
- [1] [YouTube search results](URL) — truy cập {YYYY-MM-DD}
- [2] [YouTube channel page](URL) — truy cập {YYYY-MM-DD}
- [3] [YouTube Studio analytics](URL) — truy cập {YYYY-MM-DD}
- [4] [Google Trends data](URL) — truy cập {YYYY-MM-DD}
- [5] [TikTok comparison search](URL) — truy cập {YYYY-MM-DD}

## Khuyến nghị cho anh Tuấn Anh
- Video nên làm hôm nay: "{topic gợi ý}"
- Hook nên dùng: "{hook pattern}"
- Cross-post sang TikTok không? {có/không, format cần chỉnh gì}
```

---

## Telegram Summary Format

For O-Lab topic 604 delivery:

```
📺 YouTube Trending — {Niche} — {YYYY-MM-DD}

Hot: "{video title}" ({views} views, {channel})
Trend ↑: "{keyword}" +{X}%

📁 ~/Workspace/Claude/Projects/Content Creator/Research/{date}/youtube-trending-{niche}.md

Sources: {N} | Confidence: {high/medium/low}
```

---

## Confidence Scoring

| Score | Criteria |
|-------|----------|
| HIGH | ≥5 sources per video, verified channels 10K+ subs, fresh data <7 days |
| MEDIUM | 3-4 sources per video, mixed channel quality |
| LOW | <3 sources, or most videos >30 days old, or channel credibility unclear |

---

## Tool Priority

1. MCP-first: mcp_MiniMax_web_search (fast, parallelizable) → use for all queries
2. mcp_exa_web_search_exa → fallback if exa is connected (not always available)
3. web_search → last resort
4. No browser/YouTube navigation → web search snippets are sufficient for this job

---

## Timing and Budget

- Max time: 30 minutes
- Max tool calls: 50
- If over budget: Deliver top 5 videos + note BUDGET EXCEEDED

---

## Common Pitfalls

- Don't skip the TikTok comparison — this is a core part of identifying cross-post opportunities
- Don't rely on view count alone — check channel credibility (10K+ subs + engagement >3%)
- Don't mark videos as trending if >7 days old — call them popular instead
- Don't copy exact formats — only learn hook patterns and structure
- Don't suggest videos that require expensive equipment — audience is budget-conscious beginners
- Don't forget the daily rotation — wrong niche keyword = wrong trending data
- **YouTube search API data gaps:** mcp_MiniMax_web_search returns limited view/subscriber data for small Vietnamese channels. Many videos show "No data" or 0 views. When this happens: (a) mark the video as CHƯA ĐỦ DỮ LIỆU, (b) reduce overall confidence to MEDIUM, (c) recommend using vidIQ or TubeBuddy for accurate data in the report's "Ghi chú về dữ liệu" section

---

## Related Skills

- social-media-trends — TikTok Gen Z slang + sounds + algorithm trends (evening cron scan, DIFFERENT job)
- tiktok-viral-script — TikTok content creation (complements this research)
- content-creator-project-workflow — Project-level workflow for content creator channel

---

## Sources

- YouTube Search: https://www.youtube.com/results?search_query=
- Google Trends Vietnam: https://trends.google.com/trends/explore?date=today-7d&geo=VN&q=
- vidIQ YouTube Trends: https://vidiq.com/youtube-trends/
- TikTok Search: https://www.tiktok.com/search?q=
