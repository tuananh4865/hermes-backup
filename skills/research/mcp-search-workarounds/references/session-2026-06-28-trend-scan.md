---
title: Evening Trend Scan — MCP Page Extraction Failures (2026-06-28)
created: 2026-06-28
type: session-reference
tags: [mcp, search, workaround, page-extraction, web-extract, exa, trend-scan, tiktok, slang]
related_skills: [tiktok-viral-script, self-verify-after-workaround]
---

# Session: Cron Trend Scan — MCP Page Extraction Tier 1 & 2 Failures

## Context

Cron job: research-lead running evening trend scan for Tuấn Anh's TikTok content niche (Setup/Edit/Ánh sáng). Goal: surface new Gen Z slang, content trends, and trending sounds for today's content ideation.

**Task breakdown (7 deliverables):**
1. Search Gen Z slang 2026 (3-5 queries) — done via mcp_MiniMax_web_search
2. Search TikTok content trends 2026 (3-5 queries) — done
3. Search Gen Z trending sounds (2-3 queries) — done
4. Compile findings with sources — done
5. Update entities/learned-about-tuananh.md — done
6. Send summary to Telegram — done (final response IS the deliverable)
7. Update state.md — done

## Where I Hit the Wall

After 5 successful `mcp_MiniMax_web_search` queries (got 40+ search results across slang, trends, sounds), I tried to **deep-extract** 3 specific pages to confirm slang definitions:

### Tier 1 failure: `web_extract`

```python
web_extract(urls=[
  "https://www.ef.com/wwen/blog/language/english-slang-2026/",
  "https://social.colostate.edu/best-practices/new-year-new-slang-words-social-media-managers-should-know-in-2026/",
  "https://metricool.com/tiktok-songs/"
])
# Response: {"success": false, "error": "DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content. Set web.extract_backend to firecrawl, tavily, exa, or parallel."}
```

**Why it failed:** The default Hermes `web_extract` backend is DuckDuckGo (ddgs), which is **search-only**. The error message even tells you to switch backends, but that requires config changes I shouldn't make mid-task.

### Tier 2 failure: `mcp_exa_web_fetch_exa`

```python
mcp_exa_web_fetch_exa(urls=[
  "https://www.ef.com/wwen/blog/language/english-slang-2026/",
  "https://social.colostate.edu/best-practices/new-year-new-slang-words-social-media-managers-should-know-in-2026/",
  "https://metricool.com/tiktok-songs/"
], maxCharacters=3000)
# Response: {"error": "MCP server 'exa' is not connected"}
```

**Why it failed:** The Exa MCP server isn't configured/connected in this profile/session. Unlike a 429 (which means try again later), "not connected" is a hard blocker.

## Tier 3: The Workaround That Worked

Instead of insisting on full page extraction, I ran **2 query-specific searches** that surfaced the exact facts I needed:

```python
mcp_MiniMax_web_search('"aura farming" "canon event" "crashing out" meaning slang')
# Got 3 results: EF GO Blog confirming the 10 terms, Instagram @pubity list, 
# Instagram @ingredient reel showing Gen Z Việt using these terms

mcp_MiniMax_web_search('"jestermaxxing" "mogging" "rizz" meaning slang 2026')
# Got 2 results: Reddit r/The10thDentist and Business Insider confirming 
# jestermaxxing = intentionally being funny, frame mogging = dominating
```

**Result:** Confirmed 8+ new slang definitions in 2 searches, no full page needed. Each search snippet had 2-3 sentences defining the term.

## Key Insight: Snippets > Full Pages for Fact-Lookup

The reflex when you have a URL is to fetch the full page. But for **definition confirmation** (slang, song name, hashtag trend), search snippets usually contain the answer. Full page extraction is for:
- Reading full articles for content
- Extracting datasets or long-form quotes
- When the snippet doesn't have enough context

For **cron-style research tasks** (gather facts, compile report), snippets + cross-validation is faster and more reliable than 1-2 full page fetches that might fail.

## What I Did Instead

1. **Accepted Tier 1/2 failures** as hard stops — didn't retry the same broken tools
2. **Pivoted to Tier 3** (query-specific searches) — 2 queries got me the definitions
3. **Cross-validated** each slang term across 2-3 sources from the snippet pool:
   - "Aura farming" → EF GO Blog + YouTube slang guide + Instagram @pubity
   - "Jestermaxxing" → Business Insider + YouTube + Reddit
   - "Crashing out" → EF GO Blog + Reddit + Instagram
4. **Compiled with confidence** — terms confirmed by 3+ sources = high confidence

## Final Output Quality

- **18 new Gen Z slang terms** added to wiki with definitions + sources
- **14 trending TikTok sounds** surfaced (cross-validated Metricool + tokchart + Buffer + Spotify)
- **13 format/algorithm trends** (velocity speed ramp, multi-panel beat sync, etc.)
- **6 photography/lighting niche trends** (Raw, Dreamy, Atmospheric; window light preferred)
- **5 niche-specific hook ideas** combining slang + setup/lighting niche

## Pinned Takeaways (2026-06-28)

1. **`web_extract` default backend is search-only** — DuckDuckGo (ddgs) cannot fetch pages. Don't retry, escalate.
2. **Exa MCP can be hard-disconnected** — "not connected" is not a transient error, treat as unavailable.
3. **The 4-tier fallback chain works** — Tier 1 (web_extract) → Tier 2 (exa) → Tier 3 (query-specific search) → Tier 4 (accept snippets). For fact-lookup, Tier 3 is usually the fastest.
4. **Cross-validate in snippets, not just trust 1 source** — 3 sources confirming the same slang definition = high confidence.
5. **Cron trend scans don't need full pages** — 5 parallel searches + snippet cross-validation is faster than 1-2 deep extracts.

## Update to Parent Skill

Added "Page Extraction Failures — The 4-Tier Fallback Chain" section to `mcp-search-workarounds/SKILL.md`. Bumped pinned lessons from 5 to 8. This pattern will save the next research-lead cron job 5-10 minutes of stuck-on-extract time.
