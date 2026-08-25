---
title: Social Media Trend Research — Last 30 Days
name: social-media-trends
created: 2026-06-01
updated: 2026-07-10
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
- **"Tìm N video {topic} hot nhất tuần X → Y"** — ad-hoc weekly content-niche deep-dive (e.g. "Tìm 15-20 video YouTube Shorts cầu lông hot nhất tuần 03/07 → 10/07/2026") — see `references/weekly-content-niche-shorts-research.md`
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

## Scheduled Cron Trend Scan (research-lead profile)

When running as a scheduled cron job (e.g. evening trend scan, profile = `research-lead`), use this 7-step output contract. Runs autonomously — no user clarification possible.

### The 7-step contract
1. **Search Gen Z slang** (3-5 queries, parallel) via `mcp_MiniMax_web_search`
2. **Search TikTok content trends** (3-5 queries, parallel) — editing techniques, formats, algorithm
3. **Search trending sounds** (2-3 queries, parallel) — current week/month
4. **Compile findings with sources** — cite all URLs, date-stamp each finding
5. **Update `wiki/entities/learned-about-tuananh.md`** — APPEND a new dated section (never overwrite). **DEDUP CHECK FIRST** — `grep -nE "\*\*<slang>\*\*"` against the file before writing. If a term already appears in any prior dated section, either: (a) skip and note in the report as "still hot, no change", (b) add only the new meaning/usage if sourced from a different provider. This prevents the file from accumulating duplicate entries across runs (confirmed pattern: Chopped, Pop off, Based, Serve appeared in 2 consecutive runs as duplicate bullets).
6. **Telegram summary** — final response is auto-delivered to cron destination; embed the full report, do NOT call `send_message`
7. **Update state.md** — the actual path is `/Volumes/Storage-1/Hermes/wiki/cron/evening-trend-scan-state.md` (NOT `~/.hermes/profiles/research-lead/state.md` — that path is wrong; the cron state lives in the wiki/cron directory). Bump `updated:` frontmatter, add a row to Run History table, add a "Searches Run" subsection listing the queries fired, add a "New Findings" subsection with the day's slang/trends/sounds, add a "Next Run Schedule" line.

### Entity file insertion pitfall (patch tool partial-read warning)

When patching `learned-about-tuananh.md` (currently 92KB+ and growing), `patch()` will fire this warning on every call after a paginated `read_file`:
```
_warning: ... was last read with offset/limit pagination (partial view).
Re-read the whole file before overwriting it.
```

**This warning is INFORMATIONAL, not blocking** — the patch still succeeds as long as your `old_string` anchor is unique in the file. Verified clean across 5+ runs (June 23, 24, 27, 28, 30, 2026).

**But there is a real risk it surfaces:** if your anchor string appears near content you haven't seen (e.g., a previous run's orphan list of slang terms that lost their section header), the patch may insert your new section in the WRONG place — between a prior section's HEADER and its body. Result: the prior section's body becomes an "orphan list" floating below your new section.

**Recipe to avoid:**
1. Before patching, run `grep -n "^## " <file>` to see all section headers and confirm the structure
2. Pick an anchor that includes the LAST line of the prior section (a section-closing line, not just a header)
3. After patching, run `grep -n "^## " <file>` again to verify the section order is still correct
4. If an orphan list appears (header is gone, body is still there), don't try to fix with another patch — re-read the full file with no offset/limit and patch it back into place

**For very large entity files (>50KB):** consider `terminal(command="tail -30 <file>")` to confirm the last section's closing line before anchoring. The `read_file` tool refuses files >100K chars, so tail/grep is the only safe inspection path.

### Tool-call discipline for cron
- **Batch independent queries in ONE assistant turn** — `mcp_MiniMax_web_search` is parallelizable, serializing wastes tokens
- **All 3 tracks should fire in one turn** if possible (e.g. 5+3+3 = 11 queries in a single block)
- **Add 1-2 niche-specific queries** beyond the 3 standard tracks when the niche is photography/lighting/setup/edit — e.g. `"photography lighting setup TikTok trend 2026 before after"` and `"TikTok June 29 2026 trending sounds Metricool weekly"`. These surface trend signals the standard 3-track pattern misses (e.g. Raw/Dreamy/Atmospheric photography trends, niche-specific trending formats). Confirmed 2026-06-29 run added 2 such queries = 13 total, all in 2 parallel blocks.
- **MCP-first** — `mcp_MiniMax_web_search` > `mcp_exa_web_search_exa` > `web_search` (faster, better recall, no rate-limit issues in cron)
- **`web_extract` is the FAILURE PATH, not the search path** — default backend is `ddgs` (search-only) and errors with: *"DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content. Set web.extract_backend to firecrawl, tavily, exa, or parallel."* When you need to actually READ a page (not just snippet), use `mcp_exa_web_fetch_exa(urls=[...], maxCharacters=3000)` instead. Confirmed working 2026-06-27 cron (New Engen June trends + Tokchart live + Slangloom + Buffer 13-songs all fetched cleanly via exa).
- **Accept snippets as data** — when `web_extract` is unavailable AND exa is rate-limited, fall back to working with search-result snippets (titles + dates + descriptions). Still citeable. 2026-06-29 cron worked clean with snippets only (no fetches needed) because query phrasing was tight enough.
- **Cross-validate slang via ≥3 sources** — different sources use different naming (EF GO calls it "Pop off", Reddit r/words spells it "21", Bark calls it "cheugy"). When ≥2 sources independently list the same term, confidence is high. When only 1 source has it, mark as "emerging, single source" and verify next run.

### Entity file rules (CRITICAL)
- **APPEND, never overwrite** — preserve prior slang entries as agent context
- **Match the existing section structure** (file already has "Gen Z Slang" + "TikTok Content Trends" + "Trending Sounds" sections; add a dated sub-section like "Gen Z Slang 2026 — Evening Trend Scan (Updated Jun 26)")
- **Bump `updated:` frontmatter** if present
- **Cite sources inline** — every claim should have a URL

### State file rules
- **Cron state path** (research-lead profile) = `/Volumes/Storage-1/Hermes/wiki/cron/evening-trend-scan-state.md` — NOT the default `~/.hermes/profiles/research-lead/state.md`. The cron job writes to the wiki/cron directory for visibility.
- **For other profiles**, state path = `~/.hermes/profiles/<profile-name>/state.md`
- **Bump `updated:` timestamp** to current run
- **Update "Current Goal"** if a goal is set
- **Append a row to Run History** with: time, goal, worker, runs count, PASS/FAIL/WARN, score, notes
- **Update Recent Verdicts table** if scoring was performed

### Telegram delivery
- The system auto-delivers your final response — **do NOT call `send_message`** yourself
- Format: emoji section headers, tables, code blocks fine
- Vietnamese for user-facing content (per SOUL.md)
- Cite all sources in the report
- If system prompt says `[SILENT]`, respect it; otherwise always emit a real (even if thin) report

**Reference:** `references/tiktok-trending-scan-cron-pattern.md` — exact query templates, source index, 3-track breakdown, pitfalls, last-run findings table.

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

## 🧭 Multi-Platform Parallel Dispatch (Verified 10/07/2026, badminton case)

When anh asks for **multi-platform niche content research simultaneously** (e.g. "TikTok + YouTube Shorts for topic X"), do NOT try to scrape both platforms in one subagent context.

**Pattern that worked:**
1. Dispatch **one subagent per platform** in parallel via `delegate_task` (mode: `tasks` batch with N parallel goals).
2. Each subagent gets a tight scope: 1 platform + 1 niche + 1 date range + 1 output file path.
3. Each subagent returns a structured markdown file with: ranked top 15-20 clips × per-clip metadata (URL, creator, view count, topic tag, viral rationale, copyright flag, adapt verdict).
4. Main agent reads both files with `read_file`, synthesizes ONE unified ranking for anh.
5. Main agent embeds the unified top-list + content calendar DIRECTLY in the Telegram reply (per SOUL.md § Artifact Decision: anh reads Telegram on phone, doesn't open Mac for long files).

**Verified result (10/07/2026, weekly badminton shorts 03-10/07):**
- Subagent 1 (TikTok): 23 clips → 20 KB file
- Subagent 2 (YouTube Shorts): 18 clips → 18.5 KB file
- Wall-clock: 3.5 min for both via single batch dispatch
- Main synthesis: 41 clips unified, top 5 Tier-1 picks for 2 channels (Tuấn Anh Badminton shop + Tuấn Anh Review TikTok), 7-day content calendar

**Caveat to flag in EVERY such deliverable:**
- Subagent view counts are MEDIUM confidence by default (web search snippets, not platform APIs).
- View counts marked `TBD` need anh to verify on the app before content production.
- TikTok exact views would need `SCRAPECREATORS_API_KEY` — NOT in default profile (per 10/07/2026 audit). State this honestly so anh doesn't expect TikTok API-grade numbers.

## Related

## Related

- [[agent-reach]] — Analyze engagement/reach metrics on social platforms
- [[tiktok-viral-script]] — TikTok content creation (complements this research)
- [[youtube-deep-dive-2026]] — YouTube strategy knowledge base
- **[[references/weekly-content-niche-shorts-research.md]]** — Ad-hoc weekly content-niche deep-dive pattern (e.g. "Tìm 15-20 video {topic} shorts hot nhất tuần X → Y"). Worked example: badminton 03-10/07/2026.

---

## Sources

- YouTube Trending: https://www.youtube.com/feed/trending
- vidIQ YouTube Trends: https://vidiq.com/youtube-trends/
- X Advanced Search: https://twitter.com/search-advanced
- TikTok Creative Center: https://ads.tiktok.com/business/creativecenter