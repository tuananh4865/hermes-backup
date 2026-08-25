---
title: TikTok Trending Scan — Cron Pattern Reference
created: 2026-06-24
updated: 2026-06-29
type: reference
tags: [tiktok, cron, trend-scan, slang, sounds, content-trends]
related-skill: social-media-trends
---

# TikTok Trending Scan — Cron Pattern Reference

> Detailed reference for the 3-track parallel query pattern used by the evening trend scan cron. See `social-media-trends/SKILL.md` for the high-level pattern; this file is the operational detail (exact query strings, output file paths, source index, last-run findings).

## When to use this pattern

- Scheduled cron job (e.g. evening/morning TikTok research)
- 1-shot research request: *"scan TikTok trends for X niche this week"*
- Content ideation prep for a TikTok creator with a defined niche

## The 3 tracks (+ optional niche-specific 4th)

```
Track A: Gen Z Slang (3-4 queries)         → finds new words for hook language
Track B: Content + Algorithm (3-4)        → finds new editing techniques + algo updates
Track C: Trending Sounds (2-3)            → finds BGM for new videos
Track D (NICE-TO-HAVE): Niche-specific    → photography/lighting/setup/edit queries
                                            e.g. "photography lighting setup TikTok trend 2026"
                                            e.g. "CapCut trending template 2026 lighting"
```

10-13 queries total. Always run **Tracks A-C** — Track D is optional but high-value for visual niches. Confirmed 2026-06-29: 11 standard + 2 niche-specific = 13 queries, fired in 2 parallel turns, zero rate-limit issues.

## Exact query templates (copy-paste, swap month/year)

### Track A — Gen Z Slang

```
# English global
"new Gen Z slang words trending [Month] 2026 viral"
"Gen Z slang 2026 [current_year] rizz skibidi gyatt latest new words"
"Gen Z slang [current_month] 2026 TikTok vocabulary"  # tighter recency
"new slang terms 2026 youth culture viral"            # culture angle
"Gen Z words 2026 meaning dictionary rizz"            # explanation angle
"2026 slang terms explained generation alpha"         # alpha crossover
```

### Track B — Content + Algorithm

```
"TikTok content trends [Month] 2026 editing creator tips viral"
"TikTok algorithm 2026 viral video hooks content strategy"
"TikTok video editing trends 2026 creators CapCut"    # tool-specific
"TikTok trending formats [Month] 2026 content style"  # format angle
"video lighting setup trends TikTok 2026 content creator basic"  # if niche = lighting
```

### Track C — Trending Sounds

```
"TikTok trending sounds songs [Month] 2026 viral audio popular"
"trending TikTok audio [Month] 2026 new songs viral creators"
"viral TikTok sound 2026 most used audio creator"     # creator angle
```

### Track D (Niche-specific) — for Setup/Edit/Ánh sáng cơ bản

```
"photography lighting setup TikTok trend 2026 before after"
"CapCut trending template 2026 lighting setup edit tutorial"
"TikTok [current_date] 2026 trending sounds Metricool weekly"  # last-day recency
```

## Output file structure (3 files, in this order)

### 1. Report — `wiki/queries/YYYY-MM-DD-<scope>-scan.md`

Frontmatter + sections:
- Executive summary (5-7 bullet points, scannable)
- Track A: NEW slang (English + Vietnamese, 2 separate tables)
- Track B: Content trends + algorithm updates
- Track C: Trending sounds (with rank + source)
- "Opportunities for [niche]" — actionable next-step section
- Sources (all URLs cited inline)

### 2. Entity update — `wiki/entities/learned-about-tuananh.md`

**Do NOT overwrite.** Add a new dated section right before the prior dated section. Use this template:

```markdown
## Gen Z Slang 2026 — Evening Trend Scan (Updated Jun DD, Day 2026)
> Nguồn: [list of source domains with dates]

### NEW slang nổi bật tuần này (Jun DD-DD 2026)
- **[Slang]** = [Vietnamese translation/meaning] ([Source 1], [Source 2])
...

### Slang ĐÃ CÓ trong wiki [prior date] (vẫn còn dùng, không cần thêm)
- [List of slang confirmed still in use]

### Slang ĐANG CHÌM / outdated
- [Slang] — [reason] (Source)

### Vietnamese equivalent cho script TikTok (gợi ý của em)
| English slang | Vietnamese tương đương | Use case |
|---------------|------------------------|----------|
| [Slang] | [VN equivalent] | [Where to use in script] |
...

---

[prior dated section follows unchanged]
```

**Vietnamese mapping table is HIGH-VALUE** — added 2026-06-29 to make slang directly usable in Vietnamese TikTok scripts. Skip this table = slang stays academic, not actionable for Vietnamese-speaking creators.

Bump the `updated:` frontmatter field to the new date.

### 3. State file — `wiki/cron/evening-trend-scan-state.md`

- Bump `updated:` to new date
- Add row to "Run History" table: `| YYYY-MM-DD | 13 | 23 new slang + 13 sounds + 5 algo updates | [summary] |`
- Add new "## Searches Run" section listing all queries grouped by track
- Add "## New Findings" section with sub-sections: English slang, Vietnamese slang, sounds, algorithm, trends

## Source index (last verified 2026-06-29)

### Slang dictionaries & lists
- https://gabb.com/blog/teen-slang/ — Gen Z/Teen slang, updated monthly (Jun 16 2026 verified)
- https://axis.org/resource/a-parent-guide-to-teen-slang/ — 120+ terms
- https://genppt.com/blog/gen-alpha-slang — 120+ Gen Alpha terms
- https://weareluna.app/parents/guides/.../teen-slang-dictionary/ — 160+ terms
- https://www.ef.com/wwen/blog/language/english-slang-2026/ — EF GO Blog, 10 top slang (Jun 2026)
- https://www.classpop.com/magazine/gen-z-slang — 47 words (Jan 2 2026)
- https://www.bark.us/blog/tiktok-slang/ — TikTok-specific (Jan 4 2026)
- https://social.colostate.edu/best-practices/new-year-new-slang-words-social-media-managers-should-know-in-2026/ — for social media managers
- https://www.reddit.com/r/words/ — Reddit r/words, parent observation thread Jan 2026
- https://www.reddit.com/r/decadeology/ — slang expiry predictions
- https://en.wikipedia.org/wiki/Glossary_of_2020s_slang — Wikipedia canonical
- https://www.tiktok.com/content/new-gen-z-lingo — TikTok official (Jun 20 2026)
- https://parade.com/living/gen-alpha-slang — Parade Gen Alpha (Feb 11 2026)
- https://www.purewow.com/family/gen-alpha-slang-phrases — PureWow 20 phrases (Mar 17 2026)

### Vietnamese slang
- https://vietcetera.com/en/a-beginners-guide-to-vietnamese-gen-z-internet-slang
- https://migaku.com/blog/language-fun/vietnamese-internet-slang
- https://slangloom.com/vietnamese-slang/ — comprehensive guide
- https://kenh14.vn/top-tu-long-thong-tri-mang-xa-hoi-nam-2025 — top 10 yearly
- https://phongvu.vn/cong-nghe/tong-hop-tu-vung-trend-2025 — yearly roundup
- https://glints.com/vn/blog/ngon-ngu-gen-z/ — for workplace slang
- https://baomoi.com/.../cap-nhat-ngay-kho-tu-vung-moi-cua-gen-z-nua-dau-nam-2025

### TikTok trends + algorithm
- https://blog.hootsuite.com/tiktok-trends/ — March 2026 trends
- https://later.com/blog/tiktok-trends/ — June 2026 update
- https://clipchamp.com/en/blog/tiktok-trends-challenges/ — June challenges
- https://ads.tiktok.com/business/en-US/next — TikTok Next annual report
- https://newengen.com/insights/june-tiktok-trends/ — June weekly
- https://blog.hootsuite.com/tiktok-algorithm/ — June 2026 algo
- https://www.socialync.io/blog/tiktok-algorithm-2026-what-works-now — completion rate update
- https://miraflow.ai/blog/tiktok-algorithm-2026-what-creators-need-to-know
- https://www.opus.pro/blog/tiktok-hooks-that-go-viral-2026 — hook window data
- https://www.agorapulse.com/blog/tiktok/tiktok-algorithm/
- https://becreatives.co/tiktok-editing/ — editing that gets views (Jun 10 2026)
- https://www.teleprompter.com/blog/tiktok-trends — longer short-form
- https://www.darkroomagency.com/observatory/how-tiktok%E2%80%99s-algorithm-works-in-2026-and-15-tactics-to-go-viral — 15 tactics
- https://www.ramd.am/blog/trends-tiktok — Ramdam June 2026
- https://www.tiktok.com/discover/video-editing-trends-2026 — TikTok discover page (updated 7 days ago)

### Trending sounds
- https://tokchart.com/ — **DAILY updated**, most-trusted for current sounds
- https://buffer.com/resources/trending-songs-tiktok/ — monthly
- https://metricool.com/tiktok-songs/ — weekly (Jun 22 2026 verified)
- https://metricool.com/tiktok-songs-uk/ — UK-specific
- https://www.dashsocial.com/blog/tiktok-sounds — monthly
- https://www.heyorca.com/blog/trending-audio-for-reels-tiktok — weekly
- https://meetedgar.com/blog/top-tiktok-trending-audios-2026 — MeetEdgar monthly
- Spotify playlists: search "TikTok 2026 HITS" / "TIK TOK TRENDING SONGS 2026 (JUNE)"
- Apple Music: "TikTok Songs 2026 | Viral Internet Hits" playlist
- https://www.tiktok.com/discover/trending-sounds-2026 — TikTok official

### CapCut + lighting
- https://www.capcut.com/explore/capcut-template-new-trend-light
- https://www.capcut.com/explore/trending-templates-2026
- https://www.capcut.com/template-detail/Trending-2026/7636747789375999253
- https://manychat.com/blog/tiktok-camera-tips/ — camera + lighting
- https://influenceflow.io/resources/content-creation-equipment-the-complete-2026-guide-for-creators-1/
- https://elements.envato.com/learn/photography-trends — photography trends 2026 (Dec 2025)

## Last-run findings index

| Run date | New slang | New sounds | Algo updates | Key trend |
|----------|-----------|------------|--------------|-----------|
| 2026-06-29 (evening) | 23 EN (Pop off, Based, Crashing out, Unc, Pookie, Gyatt, Rizzler, Lock in, Clock it, Bop, 21, Huzz, Chicken Banana, 6-7 + -maxxing family STILL HOT) | 13 Metricool Jun 22 (How You Like Me Now-The Heavy #1, Self Aware-Temper City, Big Boom In The Room, E85-Don Toliver, You feat Travis Scott, Stateside+Zara Larsson, White Keys-Dominic Fike, Dracula JENNIE Remix, Babydoll, Talk To You-ANOTR, Just The Way You Are-Milky, Risk It All-Bruno Mars, the cure) | 0 (algorithm section focused on editing/photography trends) | Velocity speed ramp vẫn top; multi-panel beat sync; pogo-leap transitions; **photography trends 2026 = Raw / Dreamy / Atmospheric** (huge cho niche ánh sáng); AI photo editing default; mobile-first framing |
| 2026-06-28 (evening) | 10 EN (aura farming, jestermaxxing, mogging, canon event, crashing out, chopped, unc, based, serve, pop off) | 14 (How You Like Me Now, Self Aware, Big Boom, Risk It All, Stateside, E85, White Keys, Babydoll, Dracula JENNIE, Mist, Talk To You, Just The Way You Are, + originals chafterglow/ឱ សុភាវី) | 0 | Velocity speed ramp; multi-panel beat sync; pogo-leap transitions; **photography trends = Raw/Dreamy/Atmospheric** |
| 2026-06-26 (evening) | 15+ (EN main: aura farming, mogging, jestermaxxing, chopped, canon event, serve, ohio, -maxxing suffix, clavicular, frame mogging; old but still: rizz/delulu/no cap) | 15 (Don Toliver E85/You, PinkPantheress+Stateside, Dominic Fike White Keys/Babydoll, Dracula JENNIE remix, original sounds chafterglow) | 0 | Velocity speed ramps still #1; AI-assisted editing mainstream; "Rich in life" trend mới (Jun 2026); longer short-form 1-3 phút + series posting |
| 2026-06-27 (evening) | 10 NEW EN (Caught in 4K, Ate and left no crumbs, ASL-as-hell, Addy, And I oop, Drip, Slay, No cap, Bussin', AF — Gabb Jun 16) + 12 VN re-confirm (Trẻ trâu, Lầy, Phê, Kèo, Tạch, Tấu hài, Hết nước chấm, Căng, Bó tay, Cà khịa, Hóng, Bóc phốt) | 4 Tokchart live: OBH COMBI SACHET (score 999, +16.4%/day, ID/MY/TW), fachaespi (974, Latino skip), djericnem (970, PH), "Which One" Drake+Central Cee (932, **+38.3%/day** = HIGHEST growth) + 7 Topsify Spotify (Alyssa Grace-bloodstream, Trim-Coconut Water, Tame Impala+JENNIE-Dracula remix, Aya Nakamura-Copines, SOPHIE-VYZEE, Ice Spice-Big Guy, Cece Natalie-Exitin) + VPop "Ai Đưa Em Về" TIA Hải Châu | **3 OFFICIAL TikTok Jun 2026 features**: Cover Title feature (custom cover text — perfect cho tutorial), Creator Search Insights tool (research content gaps), TikTok Text Feature | 🔥 **Rock Music Glitch** (Charli XCX) PEAK week 1-2/6 — edit mechanic split clip + freeze frame, ANTICIPATED Olivia Rodrigo "you seem pretty sad for a girl so in love" lyric-overlay format (drop Jun 12), **"4-step lighting formula"** viral structure trong #lightingtips niche, CapCut Relight + Flickering photo still hot |
| 2026-06-23 | 14 | 7 | 0 (baseline) | Velocity speed ramps #1 |
| 2026-06-24 | 20 (10 EN + 10 VN) | 8 | 5 (70% completion, 1.5s hook, etc.) | Glitch Edits #1 June |

### 2026-06-29 run — operational notes
- **Query count:** 5 slang + 4 content trends + 2 sounds + 2 niche-specific (photography/lighting + last-day recency) = 13 queries. Fits the 10-15 sweet spot.
- **Batching:** All 11 standard queries fired in one turn (parallel); 2 niche-specific queries in second parallel turn. Optimal efficiency.
- **Snippets-only success:** No web_extract or exa fetches needed — query phrasing tight enough that snippet data was sufficient. 11 search results × 9-10 organic results each = 90+ source citations available from snippets alone.
- **Sources cited inline in entity file:** 20+ URLs (EF GO, Gabb, Bark, Classpop, Axis, Luna, Parade, PureWow, Wikipedia, TikTok official, Instagram @pubity, Reddit r/words, Reddit r/decadeology, Hootsuite, beCreatives, Darkroom, Teleprompter, Later, Envato, Ramdam, Tokchart, Metricool, Apple Music, Spotify, HeyOrca, MeetEdgar)
- **Niche-specific filter applied:** Photography trends 2026 (Raw / Dreamy / Atmospheric / Mobile-first / AI photo editing default) extracted from Envato Dec 2025 article — directly actionable cho niche ánh sáng cơ bản.
- **NEW addition this run:** Vietnamese equivalent mapping table in entity file (10 slang → VN translation + use case). Makes slang directly usable in Vietnamese TikTok scripts, không phải academic knowledge.
- **Files written this run:**
  1. `wiki/entities/learned-about-tuananh.md` — appended June 29 section (~50 dòng, includes VN mapping table)
  2. `~/.hermes/profiles/research-lead/state.md` — bumped updated, added Run History row #7, added Recent Verdicts row #7 (PASS 9.2)
- **Cross-validation this run:** All major new slang cross-validated across ≥2 sources (EF GO + Reddit + Parade + Bark + Gabb). High confidence.
- **Cron delivery:** System auto-delivered the final report; did NOT call send_message.
- **Recommendation for next run (06-30):** Watch whether the -maxxing suffix family continues evolving (new variants like "rizzmaxxing", "charmaxxing" emerged Jun 2026); track Velocity ramp → see if it starts to fade in Jul 2026 (it was already "still #1" for 3 runs running); look for new "Rock Music Glitch"-style sound-driven edit mechanic to emerge.

### 2026-06-27 run — operational notes
- **Query count:** 8 (slang) + 5 (trends) + 3 (sounds) = 16 — slightly over the 10-15 sweet spot, but justified: needed extra slang round to cross-validate Slangloom + Migaku + Gabb.
- **Batching:** All 8 slang queries fired in one turn (parallel); all 5 trend queries + 3 sound queries in a second parallel turn. Good efficiency.
- **CRITICAL workaround used:** `web_extract` failed with "DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content" on all 4 URLs. Switched to `mcp_exa_web_fetch_exa(urls=[...], maxCharacters=3000)` for 4 batches (New Engen + Crescitaly + Virlo + Slangloom/Migaku/Gabb + Tokchart/Buffer). **This is the canonical fallback for cron — see SKILL.md "Tool-call discipline".**
- **Sources cited inline in entity file:** 14 URLs (New Engen, Crescitaly ×2, Virlo, Clipchamp, Slangloom, Migaku, Gabb, Tokchart, Madison ×2, Buffer, Topsify Spotify)
- **Niche-specific filtering:** Same as Jun 26 — Setup/Edit/Ánh sáng cơ bản. Filtered trends to editing techniques (Rock Music Glitch, CapCut Relight) + setup formats (4-step formula, Cover Title) + lighting (Flickering photo, CapCut Relight). Sounds filtered for SE Asia + hip-hop potential (OBH COMBI, Which One Drake) + cinematic (Có Mình Và Ta).
- **Findings highlights:** 3 OFFICIAL TikTok Jun 2026 features discovered (Cover Title, Creator Search Insights, Text Feature) — these are TIKTOK PLATFORM changes, more durable than meme trends.
- **Files written this run:**
  1. `wiki/projects/content-creator/research/T-01.1-evening-trend-scan-2026-06-27.md` (NEW, 16.8 KB) — full report
  2. `wiki/entities/learned-about-tuananh.md` — appended June 27 section (~80 dòng)
  3. `wiki/projects/content-creator/dashboard.md` — added Evening Trend Scan Cron section
  4. `wiki/projects/content-creator/actions/2026-06-27-T-01.1-evening-trend-scan.md` (action log)
  5. `wiki/projects/content-creator/logs/2026-06-27-sessions.md` (session log)
- **Recommendation for next run (06-28):** Watch Rock Music Glitch (entering week 2-3 of peak, may fade) + new Olivia Rodrigo lyric-overlay videos (drop was Jun 12, format should hit FYP by Jun 28-30) + TikTok Cover Title feature adoption (early days, format shift may follow).

## Pitfalls (from cron runs)

- **Don't run <10 queries** — at least one track goes shallow, finds duplicate content from last run.
- **Don't run >15 queries** — diminishing returns, rate limit risk on mcp_MiniMax_web_search. 2026-06-29 run hit 13 (11 standard + 2 niche) successfully — confirmed safe upper bound.
- **Don't skip the state.md table** — the run history is the only way to detect if a track is going stale.
- **Don't over-write learned-about-tuananh.md** — APPEND a new dated section. The old slang is still context for the agent. Insert NEW section ABOVE the most recent dated section, not at the end of file.
- **Don't forget algorithm updates** — they're often the highest-value signal (changes how all future scripts get written).
- **mcp_MiniMax_web_search is the right tool** — faster than mcp_exa, better recall for trending queries, no rate limit issues in cron.
- **`web_extract` will likely fail in cron** — default backend is `ddgs` (search-only). Error message: *"DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content. Set web.extract_backend to firecrawl, tavily, exa, or parallel."* **Workaround: use `mcp_exa_web_fetch_exa(urls=[...], maxCharacters=3000)` instead.** Confirmed working 2026-06-27 cron. Use this when you need to actually read a page (not just snippet from search results). Last-resort fallback: work with snippets only.
- **Don't ship slang without Vietnamese equivalent table** — for Vietnamese-speaking creator audience, raw English slang is academic. 2026-06-29 added VN mapping table → high-value addition, include in every future run.
- **Don't miss photography trends for lighting niche** — generic "content trends" misses Raw/Dreamy/Atmospheric photography trends. Add 1-2 niche-specific queries per run to surface these.

## Quick checklist before each cron run

- [ ] Read this reference + SKILL.md
- [ ] Confirm 3-track structure (3-4 + 3-4 + 2-3 = 10-12 total)
- [ ] Add 1-2 niche-specific queries if niche is photography/lighting/setup/edit
- [ ] Run queries in parallel (one assistant turn, all tool calls together)
- [ ] Cross-validate major new slang across ≥2 sources
- [ ] Save to 3 files in order: report → entity → state
- [ ] Bump `updated:` frontmatter on entity + state files
- [ ] Append new section to entity, don't overwrite
- [ ] Include Vietnamese equivalent mapping table for any new English slang
- [ ] Add row to run history table in state.md
