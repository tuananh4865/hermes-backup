---
name: tiktok-shop-product-research
description: Validate a product (Shopee link, TikTok Shop, or product name) for TikTok Shop affiliate content viability before investing in script writing or filming. Covers competitive YouTube review analysis, market size estimation via view counts, win pattern extraction, and content gap identification. Trigger when user sends a product link, asks "should I do content on X product", or wants to know top YouTube reviews for a product.
---

# TikTok Shop Product Research

Validate a product BEFORE writing viral scripts. Don't waste hours scripting for a product with no audience or no angle.

## When to use this skill

User triggers:
- Sends a Shopee/TikTok Shop product link → "should I make content on this?"
- Asks "top review videos for product X" with view counts
- Wants to evaluate product for affiliate viability
- "Phân tích sản phẩm này có làm content được không"

## Workflow

### Step 0: Locale priority — VIETNAMESE FIRST (CRITICAL)

**This is a hard preference from Anh. Don't ask, don't wait to be corrected.**

When searching for review videos, competitors, or any audience signal for content creation:
1. **ALWAYS run Vietnamese-language searches first** (or in parallel with English).
2. Anh's actual audience is Vietnamese, the affiliate market is Vietnamese (Shopee VN, TikTok VN) — KOL nước ngoài là reference data, KHÔNG phải target.
3. After the Vietnamese scan, English results can supplement for win-pattern analysis, but report Vietnamese results prominently and first in the ranking table.
4. Phrases that worked for VIETNAM-priority searches:
   - `review [brand] [product] tiếng việt`
   - `bộ lọc [brand] [device] đánh giá`
   - `gl=VN&hl=vi` query params on YouTube (forces Vietnamese locale in results)
5. **Red flag from user:** If Anh EVER says "sao toàn kết quả nước ngoài?" / "tìm người Việt đi" / "toàn lấy kết quả nước ngoài vậy?" — it means Step 0 was skipped. Patch this into the session immediately and apologize briefly in Vietnamese.

### Step 1: Decode the product from the link/title
Extract from Shopee URL slug or full title:
- Brand + product type (e.g., "K&F Concept filter set")
- Compatible device (e.g., "DJI Osmo Pocket 3")
- Key features (magnetic, ND2-ND32, CPL, etc.)
- Bundle size (1, 3, 5 filters)

### Step 2: Try direct Shopee extraction, then fall back
**Primary**: `web_extract` with the Shopee URL
**Fallback if 400/blocked**: 
- `browser_navigate` to the URL — Shopee returns "Page Unavailable" for non-logged-in bot sessions. Still capture the `<title>` tag from the HTML, it often contains the full product name.
- Don't burn cycles trying to bypass Shopee anti-bot. Move to YouTube.

### Step 3: YouTube competition scan (the core signal)
Run **2 search queries** to triangulate view count data:
1. `[brand] [product] [device] review` (e.g., "K&F Concept magnetic filter DJI Osmo Pocket 3 review")
2. `[brand] [product] [device] best` (catches "best X" listicles)

For each, use `browser_navigate` to YouTube results. YouTube search result snapshots include `XXX views` directly under each title — no click-through needed.

**Target metrics to capture per video:**
- View count
- Channel name
- Video length
- Upload age
- Title pattern (question? comparison? "worth it"?)
- Whether it has chapters (signals watch time investment)

### Step 4: Sort and rank
Sort videos by view count. The TOP 5 are your competition's proven winning angles.

| Signal | Meaning |
|--------|---------|
| Top view < 50K | Niche market, low demand — risky for affiliate |
| Top view 50K-500K | Healthy niche, room to compete |
| Top view >1M | Saturated, big creators dominate, hard to break in |
| All videos <20K | New product, first-mover opportunity |
| All videos 1+ year old | Stale, refresh may work |

### Step 5: Extract win patterns from top 5
Look at titles + descriptions of top 5. Identify the angle(s) that worked:

Common viral review patterns to look for:
- **"Worth It?" question** — addresses purchase hesitation
- **"X vs Y" comparison** — decision-making content
- **"Before vs After" demo** — visual proof
- **"How to / Tutorial"** — educational evergreen
- **"I tried X for Y days"** — long-form trust building
- **"The truth about X"** — myth-busting

### Step 6: Identify content gaps (your opportunities)
After seeing what worked, ask: **what hasn't been done?**
- Test against time (durability, long-term review)
- Price comparison (vs OEM/competitor at 3x price)
- Reverse psychology ("X scenarios where you DON'T need it")
- POV of specific persona (TikToker, vlogger, mom, traveler)
- Vietnam market angle (price in VND, local alternatives, Shopee availability)

### Step 7: Report and recommend
Output should be:
1. **Ranked top videos table** (channel, views, length, angle)
2. **Win patterns** (3-5 bullet summary of what made top videos work)
3. **Content gaps** (5 unique angles no competitor has done)
4. **Verdict** (NICE - GO, MAYBE - test, SKIP)
5. **Next-step CTA** ("Viết script? Nghiên cứu sản phẩm khác? So sánh giá?")

## Vietnamese output style
- Casual "anh + em" register
- "Mấy con vợ" when referencing target audience
- Tables for ranked data (Telegram-friendly)
- Always end with 3-4 next-step options (A/B/C/D)
- See `references/output-template.md` for full template

## Pitfalls

- **Always Vietnamese-first** (Step 0) — user explicitly corrected this on 2026-06-06. Don't get cute with "comprehensive international scan first" — that's wrong for this user.
- **Don't spend >2 tool calls trying to scrape Shopee** — Shopee anti-bot is aggressive for anonymous sessions. Move to YouTube immediately.
- **Don't retry TikTok search on Vietnamese queries** — `tiktok.com/search?lang=vi-VN&q=...` returns "Đã xảy ra lỗi" reliably. Use hashtag pages (`/tag/[name]`) instead. They always load post count.
- **Don't trust 1 search query** — YouTube personalization biases results. Run 2-3 different phrasings.
- **Top view count ≠ market size** — a 50K-view review could mean a small market OR a market with no great content yet. Cross-check with hashtag volume on TikTok.
- **Don't recommend a product just because the user sent a link** — Anh values honest analysis. If the product is too niche or saturated, say so.
- **Avoid "perfect" recommendations** — if a product has obvious issues (high price, low demand, too competitive), flag them.
- **MCP `web_search` (MiniMax) often fails with TLS cert path error** in current env (`/Users/tuananh4865/.cache/uv/archive-v0/HLuixdJbXsPzfoYA6tO1k/lib/python3.12/site-packages/certifi/cacert.pem` is missing). Use `browser_navigate` to YouTube/TikTok directly as the primary signal source. Don't burn 2-3 tool calls on a web_search that will keep failing. (See `references/tool-fallback-notes.md` for full env notes.)
- **Hashtag ratio = strongest content-gap signal** — if `#brand+product` posts < 1% of `#device` posts, you have a first-mover opportunity. (See `references/tiktok-hashtag-ratios.md` for the 2026-06-06 case where #kfconceptfilter had 858 posts vs #osmopocket3's 115.6K → 99.3% content gap.)

## Tool fallback ladder (in order)
1. `browser_navigate` to YouTube `/results?search_query=...&gl=VN&hl=vi` (most reliable for review data)
2. `browser_navigate` to TikTok `/tag/[hashtag]` (most reliable for TikTok data — search page itself often errors)
3. `web_extract` on non-bot-protected URLs (blogs, official sites, news)
4. `mcp_MiniMax_web_search` (skip if previous calls have shown TLS errors in this session)
5. `mcp_exa_web_search_exa` (only if Exa MCP is connected — check first)

## Related skills
- `tiktok-viral-script` — write the script AFTER validating the product here
- `last30days` — for trending topic research
- `social-media-research` — broader platform research pattern

## Files
- `references/output-template.md` — full Vietnamese output template
- `references/case-kf-concept-osmo-pocket3.md` — case study from 2026-06-06 session
