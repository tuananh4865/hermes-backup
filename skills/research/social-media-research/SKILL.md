---
title: Social Media Research — Platform-Native with last30days + Agent-Reach
name: social-media-research
version: "1.2.0"
description: Research topics across YouTube, X/Twitter, Reddit, TikTok, and other social platforms using last30days + Agent-Reach. Platform-native data, not web-search articles about platforms.
argument-hint: YouTube trends this week | OpenClaw vs Hermes comparison | Reddit AI tools discussion | trending TikTok sounds this month
trigger: research YouTube | research X/Twitter | research Reddit | research social media | trending content | platform-native research | nghiên cứu kênh youtube | phân tích kênh
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
user-invocable: true
metadata:
  requires:
    bins:
      - python3.13
      - yt-dlp
    env: []
    optionalEnv:
      - XAI_API_KEY
      - BRAVE_API_KEY
      - SCRAPECREATORS_API_KEY
      - RDT_TOKEN
---

# Social Media Research — Platform-Native

## Core Principle

**Use platform-native tools BEFORE web search.**

When Anh asks to "research YouTube" or "search X" or "find Reddit discussions":
→ Use `last30days` + `Agent-Reach` first
→ Web search is ONLY the fallback

**Why:** Web search finds ARTICLES ABOUT platforms — not platform data. The difference is critical for content decisions.

---

## Setup (CRITICAL — Python 3.13 Required)

### last30days
```bash
# Location
~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py

# IMPORTANT: Requires Python 3.12+, NOT python3.11
# Use: /opt/homebrew/bin/python3.13

# Test:
/opt/homebrew/bin/python3.13 ~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py --help

# YouTube transcripts (yt-dlp):
brew install yt-dlp
```

### Agent-Reach (supplementary, for specific platforms)
```bash
# Status check
cd ~/.hermes/skills/agent-reach && python3 -m agent_reach.cli doctor

# YouTube/Bilibili subtitle:
yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "URL"
```

---

## Usage Patterns

### Basic research (last30days)
```bash
/opt/homebrew/bin/python3.13 ~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py "TOPIC" --emit=compact --search=reddit,youtube --days=7
```

### With web backend override
```bash
/opt/homebrew/bin/python3.13 ~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py "TOPIC" --search=reddit,youtube,twitter --days=30 --web-backend=brave
```

### Agent-Reach YouTube transcript
```bash
yt-dlp --write-auto-sub --skip-download -o "/tmp/%(id)s" "VIDEO_URL"
# Then read the .vtt or .json file
```

### Agent-Reach Reddit
```bash
rdt search "TOPIC" --limit=10
rdt read POST_ID
```

---

## Platforms & Tools Matrix

| Platform | Primary Tool | Secondary Tool |
|----------|-------------|----------------|
| YouTube | last30days (transcripts) | Agent-Reach (yt-dlp) |
| Reddit | last30days (via rdt-cli) | Agent-Reach (rdt) |
| X/Twitter | last30days (needs XAI_API_KEY) | - |
| TikTok | last30days (needs SCRAPECREATORS_API_KEY) | - |
| Bilibili | Agent-Reach (yt-dlp) | - |
| Hacker News | last30days (free, no key) | - |
| Polymarket | last30days (free, no key) | - |
| GitHub | last30days (free, no key) | Agent-Reach (gh cli) |

---

## Output Format for Anh

When delivering research, use Vietnamese with:
- Key findings as bold lead-ins
- Engagement numbers (views, upvotes, likes)
- Platform-specific insights
- Actionable for TikTok affiliate content

No trailing `Sources:` block — emoji-tree footer from last30days is the citation.

---

## YouTube Channel Deep-Dive Workflow (verified 2026-07-11, @VuiVe case)

When user sends a YouTube channel URL + "nghiên cứu sâu" / "phân tích kênh này" / "research kênh X", follow this 2-prong parallel pattern:

### Step 1: Verify + capture metadata (orchestrator, <1 min)
```bash
# Load channel page (don't try to extract — YouTube blocks web_extract)
browser_navigate "https://www.youtube.com/@{HANDLE}"

# Capture in 1 snapshot:
# - Name, Verified badge, subscriber count, video count
# - Slogan (channel description line)
# - Contact email (for monetization signal)
```

### Step 2: Dispatch 2 subagents in parallel (NEVER sequential)
- **Subagent A: Channel deep-analysis** — analyze 30-50 latest videos (hook pattern, title formulas, thumbnail style, monetization signals, upload frequency, engagement rate). Output 2000-4000 word markdown.
- **Subagent B: Market benchmark** — research competitor channels in same niche + adjacent niches (top 10 channels, gap analysis, transferable formulas). Output 2500-5000 word markdown with comparison tables.

Both subagents get full tool access (`mcp__exa__*`, `mcp__MiniMax__*`, `browser_navigate`, `web_extract` with Firecrawl/Tavily backend). Dispatch via `delegate_task(tasks=[A, B])` — they run in background.

### Step 3: While subagents run, browse Videos/Shorts/Playlists tabs
Quick-scan 20-30 video titles from the Videos tab → extract pattern signals:
- Title formula repetition (e.g., "Tất cả [X] trong Y phút")
- Average view count
- Post cadence (timestamps: 1d, 4d, 7d, 10d...)
- Long-form vs Shorts ratio

This data gets added to the synthesized report as ground-truth verification.

### Step 4: Synthesize + deliver
- Wait for both subagents (background mode auto-notifies)
- Synthesize into 1 unified report with: (1) Channel profile, (2) Pattern analysis, (3) Market context, (4) Gap analysis for user's purpose, (5) Roadmap 30/60/90 days
- **Embed inline in Telegram** (Telegram embed rule) — save file only if >4000 chars or user explicit request
- Cite subagent outputs as source (not as the report itself)

### Anti-patterns
- ❌ Single subagent for both analysis + benchmark — wastes time, results shallow
- ❌ `web_extract` on `youtube.com/@handle` directly — returns "DuckDuckGo is search-only" error. **Always use `browser_navigate` for YouTube**
- ❌ Sequential subagent dispatch — doubles wall time. Parallel is 2x faster
- ❌ Skipping channel page metadata — subagents will re-discover what browser_snapshot already captured

### Why this works
- Subagent A goes deep on content/format/hook signals
- Subagent B goes wide on market/competitor context
- Orchestrator adds ground-truth from browser snapshot (no fabrication)
- Synthesized output gives user BOTH the channel profile AND how to apply it to their niche

---

## Visual / Branding Deep-Dive Sub-Trigger (added 2026-07-11, @VuiVe case)

When user follows up the channel research request with: *"làm báo cáo chi tiết về phong cách hình ảnh, nội dung, thumbnail, title, description, mô tả kênh và hệ thống kênh"* — this is NOT a generic re-request. It's a **depth bias signal toward visual + branding identity**. The user already accepted the basic research and now wants:

1. **Phong cách hình ảnh** (visual style: animation, color palette, illustration vs photo)
2. **Phong cách nội dung** (content style: tone, pacing, narrative structure)
3. **Thumbnail style** (composite layout: text overlay, faces, color, props)
4. **Title formulas** (pattern recognition from 30+ titles with frequency %)
5. **Description structure** (template breakdown: affiliate, contact, CTA, etc.)
6. **Mô tả kênh** (channel slogan, About section, branding statement)
7. **Hệ thống kênh** (channel ecosystem: main + sub-channels, social media, contact info)

**When this trigger fires:**
- Dispatch a NEW subagent C focused on VISUAL/BRANDING ONLY (don't try to retrofit Subagent A's general analysis)
- Use `references/youtube-channel-visual-branding-template.md` (NEW) as output scaffold
- Browse to 5-10 actual video pages to capture **verbatim description text** + **thumbnail visual description** (no fabrication — describe what you see)
- Verify all video IDs from `web_search` snippets by `browser_navigate` (snippets can attribute videos to wrong channels — verified @VuiVe case 2026-07-11)

### Updated 4-prong pattern (Subagent A + B + C + orchestrator verify)

The original workflow uses 2 subagents (A: channel analysis, B: market benchmark). The visual/branding follow-up adds a third subagent C for depth-on-visual. Updated pattern:

- **Subagent A: Channel deep-analysis** (general content + format + hook) — same as before
- **Subagent B: Market benchmark** (competitor channels + gap analysis) — same as before
- **Subagent C: Visual/branding identity** (NEW — only when follow-up trigger fires)
  - Browse 10+ actual video pages
  - Capture: thumbnail visual description (color palette, faces, text overlay, composition), verbatim description text (4 sections: affiliate, membership, cross-platform, contact), title formula breakdown with frequency %
  - Map channel ecosystem: main + sub-channels + social media + contact info
  - Output 3500-5000 word markdown using `references/youtube-channel-visual-branding-template.md`
- **Orchestrator**: synthesize A + B + C + ground-truth from browser_snapshot into 1 unified report

## Common Traps

0. **web_search video ID attribution is UNRELIABLE (added 2026-07-11, @VuiVe case)** — when `mcp_MiniMax_web_search` returns a YouTube URL with video ID, the SNIPPET may be from a completely different channel than expected. Real case 2026-07-11: searching "VuiVe cầu lông" returned `https://www.youtube.com/watch?v=1xCvwNWNU-w` — but that video was actually from "Cộng đồng cầu lông Việt Nam - VN Badminton", NOT @VuiVe. **Always verify with `browser_navigate` before treating a video ID as belonging to the target channel.** Cheap pre-check: read the snippet's channel attribution. If missing → navigate to verify. Also: some video IDs returned by search may be already-deleted (`{"StaticText": "This video isn't available anymore"}`) — handle gracefully, pick next candidate.

0a. **Rotating sponsor pattern in description (added 2026-07-11, @VuiVe case)** — high-performing Vietnamese YouTube channels often use **rotating sponsors per video** instead of one fixed sponsor. Each video's first line of description is a DIFFERENT affiliate link: video N = CellphoneS, video N+1 = Thế Giới Di Động (Xiaomi), video N+2 = Odoo ERP, video N+3 = Prep Edu VSTEP. When documenting a channel's monetization model, **scan 5-10 video descriptions** and note the rotation pattern. Don't assume single-sponsor model. Common pattern: 4-part description structure = (1) Affiliate link of the day, (2) Membership/Join link, (3) Cross-platform links (sub-channels, Fanpage), (4) Business contact (Email + Zalo + CN email for cross-border). For @VuiVe: business contact email is `partners.98smedia@gmail.com`, Zalo `0349585580` (named person: Thủy Trần), CN email `contactvuive@163.com` — having a dedicated CN email signals cross-border monetization ambition.

0b. **Sub-channel discovery via raw channel ID (added 2026-07-11, @VuiVe case)** — when a main channel has a sub-channel like "Vui Vẻ Uncut", the URL in description may be in raw channel-ID form (e.g., `@UCxxd6_BshqmOGaJfNnDsTYQ`) instead of a custom handle. Navigating to that raw-ID URL may return **404 Not Found** ("This page isn't available"). Workaround: search the main channel's videos for cross-references to the sub-channel name, OR search YouTube for "Vui Vẻ Uncut" with `browser_navigate` to YouTube search results page. Don't trust the description URL as ground truth — verify with a navigation first. Also note: custom URLs with Vietnamese diacritics (e.g., `c/VuiVẻ`) can URL-encode differently — prefer the `@handle` form.

1. **Python version** — last30days v3.3.1 requires 3.12+. Using python3.11 gets "requires Python 3.12+" error. Always use `/opt/homebrew/bin/python3.13`.

2. **Reddit 403** — Public Reddit search API returns 403. last30days falls back to RSS tier (22 posts, score-only). Works fine for research.

3. **YouTube transcript failure** — yt-dlp fails for ~1/6 videos. last30days has direct HTTP fallback. 5/6 success rate is normal.

4. **No X/Twitter auth** — Without XAI_API_KEY, last30days uses Digg (1000 AI accounts, no auth required). Good enough for most research.

5. **TikTok Shop + Shopee Vietnam affiliate data — web search is INSUFFICIENT (2026-06-20 UPDATED)**
   - `last30days` with SCRAPECREATORS_API_KEY returns TikTok content metadata (trending sounds, hashtags, viral videos) — NOT TikTok Shop e-commerce data (prices, sales volume, commission rates, seller rankings)
   - Web search finds ARTICLES ABOUT platforms — not platform's actual real-time data
   - **Shopee Vietnam specifically:** `mcp_exa_web_fetch_exa` times out on shopee.vn URLs (blocked). Use web search snippets + Vietnamese gear review sites as proxies.
   - **For affiliate research on either platform**: Use web search to find KOL reviews, Vietnamese tech stores (DJI Store VN, Shopee VN stores), and price comparisons — then note in the report that data is indirect/estimated

   **What's ACCESSIBLE (indirect sources, verified 2026-06-20):**
   - Shopee Mall prices via search snippets: `site:shopee.vn {product}` ✅
   - Vietnamese KOL TikTok/YouTube posts (view counts, engagement signals) ✅
   - Vietnamese review sites: vjshop.vn, tokyocamera.vn, djivietnam.com.vn, djistore.com.vn, thegioididong.com (gear guides reflect real market) ✅
   - Facebook groups (DJI VN, action cam communities) — seller posts with prices ✅
   - International comparison reviews (YouTube, DPReview) ✅
   - Shopee commission rate RANGES from published fee structures: 2.5-12% base + up to 40% CommissionsXtra

   **What's NOT ACCESSIBLE (requires login/Seller Center):**
   - Exact commission rate per product (Shopee Affiliate / TikTok Shop Seller Center only) ❌
   - EPC (Earnings Per Click) per product ❌
   - Cookie window duration ❌
   - CommissionsXtra offers (seller-set bonuses) ❌
   - Sales volume per product (seller dashboard only) ❌
   - Seller ratings/review counts on Shopee/TikTok Shop (requires product page crawl, CAPTCHA) ❌

   **Confidence rule:** Always flag `confidence: medium` when using indirect sources. `confidence: low` when only international sources (no VN data). `confidence: high` only when Seller Center data verified. For commission rates, note "est." and cite the published base rate range.

6. **YouTube trending research uses mcp_MiniMax_web_search — NOT last30days (CRITICAL, updated 2026-06-28)**
   - last30days + yt-dlp get **transcripts/content**, NOT trending lists, view counts, or subscriber data
   - For the **daily 8AM YouTube trending job** (Job 3, Content Creator gear): use `mcp_MiniMax_web_search` exclusively
   - last30days is the **wrong tool** for this job — will return zero relevant results
   - `mcp_MiniMax_web_search` returns: URL, snippet, upload date, related queries (proxy for trend direction)
   - What it does NOT return: view count, subscriber count, engagement ratios
   - See: `references/youtube-trending-job-workflow.md` (full tool selection table + keyword rotation)

7. **web_extract DuckDuckGo backend** — `web_extract` tool fails with "DuckDuckGo (ddgs) is a search-only backend" when the extract_backend is not set. The intended fix was `mcp_exa_web_fetch_exa`, but that also fails when the exa MCP is not connected (verified 2026-06-18: returned "MCP server 'exa' is not connected"). Current fallback for URL content extraction: use `mcp_MiniMax_web_search` snippets only, or `web_extract` with direct URLs if content is short. If exa MCP is needed, run `~/.hermes/scripts/setup-exa-mcp.sh` first.

8. **Vietnamese keyword 1027-output new_sensitive** — `mcp_MiniMax_web_search` returns `{"status_code": 1027, "status_msg": "output new_sensitive"}` for certain Vietnamese-language queries (especially compound queries like `"lens cho máy quay vlog"`). Workaround: switch to English/product-name variants immediately (e.g., `"Canon PowerShot V1 lens review 2026 Vietnam"`). Do NOT retry the same query — change approach.

9. **Vietnamese YouTube data** — YouTube trending for VN niche uses Vietnamese-language search queries ("gimbal điện thoại nào tốt" not "best smartphone gimbal"). Key Vietnamese data sources: vjshop.vn, tokyocamera.vn, djistore.com.vn, thegioididong.com — these publish gear guides that reflect real Vietnamese market trends.

10. **TikTok viral-clips research WITHOUT SCRAPECREATORS_API_KEY (verified 2026-07-10)**
    - This is the **most common production case** — the key is rarely set in `default` profile, and `last30days` Python 3.13 binary is often not installed at `/opt/homebrew/bin/python3.13` (verified: only 3.11 + 3.14 on a fresh Mac; `uv` will auto-download 3.13 on first run but adds ~30s overhead).
    - **Working fallback chain** (used successfully, returned 20+ clips for "badminton viral 03/07–10/07/2026"):
      1. **Skip last30days** entirely for TikTok metadata when key missing — go straight to `mcp__MiniMax__search`.
      2. **Fan out ~10–15 parallel queries** across these axes (do NOT do 2–3 queries then stop):
         - English product/topic: `"viral TikTok {topic} video July 2026"`
         - English creator/player's handle: `"@{creator} viral July 2026"`
         - English tournament hook: `"{topic} {tournament} 2026 viral TikTok"`
         - Vietnamese language (if VN relevance needed): `"cầu lông viral TikTok tháng 7 2026"`
         - Funny/fail/relatable variants: `"{topic} fail funny TikTok this week"`
         - Product review axis: `"{topic} {brand} racket unboxing review viral 2026"`
         - Tutorial axis: `"{topic} tutorial beginner how to {skill} viral 2026"`
         - Creator-by-creator (famous creators in niche): `"@bwf.official viral"`, `"@aapopuhakkabadminton trick shot"`
      3. **Mark view counts as `TBD`** in deliverable — Google snippets show `Likes` and `Comments` but rarely `Views` for TikTok. **NEVER fabricate view numbers.**
      4. **Flag `confidence: medium`** at the top of the report with the exact env limitations (no key, no Python 3.13 binary, etc.) — user/parent agent needs to know what to verify manually.
    - **Output structure that works** (see `references/tiktok-viral-clips-report-template.md` for the full template):
      - Per-clip: Creator (@handle) + URL + likes visible + chủ đề + 1-2 sentence tóm tắt + "Vì sao viral" + **"Adapt cho kênh {channel}? Yes/No + lý do"** + ngày đăng
      - Topic breakdown table at end (counts per category)
      - "Recommended adaptations" section split by channel (for multi-channel reports)
      - Bonus picks (3 extra) beyond the requested N
      - Caveats block at top: tool used, view-count limitation, confidence level
    - **Total runtime**: ~15 parallel web_search calls + 1 markdown write. ~2 min wall time. Beats waiting for last30days to fail on missing key.
    - **Don't do mid-session**: don't try to "fix" the env (install py3.13, request API key from user) — the fallback path above is faster. Note the env gap in caveats and move on.

11. **YouTube channel page = ALWAYS browser_navigate, NEVER web_extract (verified 2026-07-11)** — `web_extract` on `youtube.com/@handle` returns "DuckDuckGo is search-only backend and cannot extract URL content". `mcp_exa_web_fetch_exa` may also fail on YouTube URLs. The reliable path is `browser_navigate` → `browser_snapshot` → extract data manually from the snapshot text. The snapshot includes channel name, subscribers, video count, slogan, and the first ~20 latest video titles/views/timestamps.

## Related Skills

- `tiktok-viral-script` — Content creation (uses research output)
- `hermes-autoresearch` — Nightly skill improvement (uses last30days for AI agent landscape research)
- `youtube-content` — YouTube transcript extraction and content repurposing
- `youtube-trending-research` — Daily rotating keyword schedule for gear niches

## Reference

Full setup notes: `references/last30days-agent-reach-setup.md`
- **`references/youtube-trending-job-workflow.md`** — Daily 8AM YouTube trending job for Content Creator niche (mic/đèn/gimbal/lens). Documents keyword rotation, 5-source rule, output paths, and VN data source proxies. NEW 2026-06-20.
- **`references/tiktok-viral-clips-report-template.md`** — Markdown template for the "N hottest viral TikTok clips for week X" deliverable. Use when parent agent asks for a list of viral clips to plan content. NEW 2026-07-10.
- **`references/youtube-channel-deep-dive-template.md`** — Output template for "research kênh YouTube X sâu" requests. Includes channel profile schema, pattern analysis table, market benchmark table, gap analysis structure, and 30/60/90 day roadmap. NEW 2026-07-11.
- **`references/youtube-channel-visual-branding-template.md`** — Output template for the second-pass visual/branding deep-dive request ("phong cách hình ảnh, thumbnail, title, description, hệ thống kênh"). Includes 7-section breakdown (visual style, content style, thumbnail composite, title formulas with frequency %, 4-part description template with rotating sponsor pattern, channel ecosystem). NEW 2026-07-11.