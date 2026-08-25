# YouTube Trending Research Job — Content Creator Workflow

**Date:** 2026-06-20
**Updated:** 2026-06-28
**Source:** Daily 8AM cron job — Content Creator YouTube Search Trends
**Purpose:** Track YouTube trending for gear review niche (mic/đèn/gimbal for new content creators)

---

## Job Overview

Each morning 8AM, track YouTube Search trending for content creator gear keywords.
- Top videos trending 24-72h
- Search volume changes
- Channel push patterns
- Content formats viewers prefer (so sánh, hướng dẫn, unbox)

---

## Keyword Rotation (by day of week)

| Day | Keyword (Vietnamese) | English equivalent |
|-----|---------------------|-------------------|
| Monday | "review mic thu âm cho người mới" | mic review for beginners |
| Tuesday | "đèn LED quay video giá rẻ" | budget LED video lights |
| Wednesday | "gimbal điện thoại nào tốt" | best smartphone gimbal |
| Thursday | "flycam cho người mới bắt đầu" | beginner flycam |
| Friday | "action cam nào đáng mua" | worth buying action cam |
| Saturday | "lens cho máy quay vlog" | lens for vlog cameras |
| Sunday | "best gear cho content creator 2026" | best gear 2026 |

---

## Tool Selection

**YouTube Trending Research = `mcp_MiniMax_web_search`**
NOT `last30days` — last30days gets transcripts/content, NOT trending lists, view counts, or subscriber data.

| Task | Tool |
|------|------|
| YouTube trending research (this job) | `mcp_MiniMax_web_search` |
| YouTube transcript extraction | `youtube-content` skill + yt-dlp |
| YouTube content repurposing | `youtube-content` skill |

---

## 5-Source Rule — Practically Achievable Subset

**Strict interpretation** requires ≥5 sources per video, but the `mcp_MiniMax_web_search` API returns only:
- ✅ URL, snippet text, upload date
- ✅ Related search queries (proxy for trend direction)
- ❌ View count, subscriber count, like/comment ratio, retention

**Pragmatic minimum (3 sources, 2026-06-26 verified):**
1. YouTube search result URL + snippet + date ← `mcp_MiniMax_web_search`
2. VN gear site cross-reference (vjshop.vn, tokyocamera.vn) ← separate search
3. TikTok/Instagram social signal (same product, even if different language) ← separate search
4. Shopee price proxy (site:shopee.vn snippet) ← separate search
5. International review (PCMag, DPReview, RTINGS) ← separate search

**What to do when full data is unavailable:**
- Mark missing fields "CHƯA ĐỦ DỮ LIỆU" — do NOT fabricate view counts or subscriber numbers
- When channel subs are unknown: note "~50K-500K est." from context clues in snippet
- When engagement is unknown: note "engagement tạm tính từ comment density trong snippet"
- Confidence drops to **medium** when ≥2 of 5 fields are "CHƯA ĐỦ DỮ LIỆU"

**Hard lesson (2026-06-26):** Even well-resourced searches via MiniMax API do NOT surface view counts, subscriber numbers, or engagement ratios. Budget time accordingly — 30-minute cron jobs cannot achieve true 5-source depth for every video. Target top 5 videos at medium confidence, skip the rest.

---

## Output Path

```
~/Workspace/Claude/Projects/Content Creator/Research/{YYYY-MM-DD}/youtube-trending-{niche}.md
```

Telegram summary delivered separately (O-Lab topic 604).

---

## Data Confidence Rules

| Condition | Confidence |
|-----------|------------|
| ≥10K subs + >3% engagement + ≥5 sources | high |
| Mixed data quality or <5 sources | medium |
| Channel <10K subs OR no engagement data | low |
| International sources only (no VN data) | low |

---

## Vietnamese Data Sources (verified 2026-06-28)

- **Gear review sites:** vjshop.vn, tokyocamera.vn, djivietnam.com.vn, bhasia.com.vn
- **VN YouTube channels:** VJShop (~30K+ subs), BNCamera, Phukienflytech
- **TikTok VN:** Canon RF 16mm, Sigma 10-18mm trending (May-Jun 2026)
- **International:** DPReview, Amateur Photographer, RTINGS, Fstoppers — good for specs, NOT VN pricing

**VN gear site giá + tình trạng bán (Shopee snippet proxy):**
- DJI Osmo Mobile 8: 3.200.000₫ (-18%), 1K+ đã bán (Shopee Mall DJI Official)
- DJI Mic Mini: 2.300.000₫ (giảm từ 4.900.000₫ — clearance sau Mic Mini 2)
- DJI Mic 3: 5.244.530₫ (Shopee)

---

## Shopee/TikTok Shop Limitation

These platforms block direct crawling. For affiliate data:
- ✅ Prices: search snippets (site:shopee.vn)
- ✅ KOL reviews: Vietnamese YouTube/TikTok posts
- ✅ Commission ranges: published fee structures (2.5-12% base)
- ❌ Exact EPC, sales volume, seller ratings: requires Seller Center login

Always flag `confidence: medium` when using indirect sources.

---

## Key Findings (2026-06-20 — Lens niche)

- **Top trending format:** "Still Worth It in 2026?" review
- **Hot keyword:** Canon PowerShot V1 (ra Apr 2025, still trending mid-2026)
- **New opportunity:** Lens/phụ kiện cho DJI Osmo Pocket 3 — niche trống trên YouTube VN
- **TikTok → YouTube:** Canon RF 16mm, Sigma 10-18mm đang hot TikTok, chưa có YouTube VN review kỹ

## Key Findings (2026-06-28 — Weekly Gear niche)

**Sunday keyword: "best gear cho content creator 2026"**
- **NAB 2026 is the dominant topic** — multiple gear review videos from May-Jun 2026 getting 200K+ views
  - "The BEST New Creator Gear at NAB 2026" (May 25, 2026) — 283K+ views
  - "We Found the BEST Creator Tech at NAB 2026" (Apr 29, 2026) — 200K+ views
  - NAB 2026 reveals: Zhiyun Smooth Q5 Ultra, Insta360 Pocket 4 teased (chưa công bố), GoPro cinema cameras, RODE RODECaster Studio
- **DJI Osmo Mobile 8** is the #1 trending gimbal in June 2026 (3.2M ₫, 1K+ sold Shopee VN)
- **DJI Mic Mini 2** just launched Jun 2026 — "Mic 3 phiên bản giá hạt dẻ"
- **DJI Mic Mini** clearance price drop: 2.3M ₫ (từ 4.9M) — prime affiliate opportunity
- **Insta360 Flow 2 Pro** — fresh review June 2026 (5 days ago), still best AI-tracking gimbal
- **Canon PowerShot V1** — Fstoppers review 4 days ago, still "hidden gem" positioning works

**Best query strategy for this job (updated 2026-06-28):**
- English queries ("NAB 2026 creator gear", "best gimbal smartphone 2026 review") return better results than Vietnamese for this niche — use English product names + "2026 review"
- VN gear sites (vjshop.vn, tokyocamera.vn, djivietnam.com.vn) critical for price + VN market signals
- Shopee snippets give price + sales volume proxy: `site:shopee.vn {product}`
- NAB 2026 recap for Vietnamese creators — fully empty on YouTube VN, high-opportunity ranking term

**Format patterns confirmed working June 2026:**
- "Best [X] for 2026" roundup
- "Still worth it in 2026?" retrospective
- "NAB [year] recap" — completely empty on YouTube VN
- "3 tháng dùng [sản phẩm]" — long-term review, high trust signal
- "Hidden gem" positioning (Canon PowerShot V1)

---

## Related

- Skill: `social-media-research` (this file belongs here)
- Skill: `youtube-content` (transcript extraction — different task)
- Content Creator project: `~/Workspace/Claude/Projects/Content Creator/`
