---
title: TikTok Shop Product Research — Tier Escalation Patterns (2026-07-16)
created: 2026-07-16
type: session-reference
tags: [mcp, search, workaround, web-extract, exa, tiktok-shop, product-research, vietnam, pricing, mag-safe, quick-release, tripod]
related_skills: [deep-research-multi-pillar, self-verify-after-workaround, evidence-first-delivery, multi-agent-orchestrator]
---

# Session: TikTok Shop Product Research — 3 groups × 11 products × 28 citations

## Context

User (Tuấn Anh) requested strict-mode research for 3 product groups destined for TikTok Shop Vietnam content. Each product needed: brand + origin, specs, VN retail price, USP, competitors, citations. Output format = JSON array. Each product MUST have ≥1 citation URL.

**Task breakdown:**
- **Group 7** — Quick-release plate (camera/Pocket 3): 2 products (generic + Ulanzi)
- **Group 8** — Mini MagSafe power bank for iPhone (V1→V9 = 9 versions of the same product category, need 7-9 candidates)
- **Group 9** — Mini phone tripod (1 edited clip): 1-3 products

Output: `/Users/tuananh4865/research_tiktok_groups_7_8_9.json` (20 KB).

## Where I Hit the Wall

### Failure 1: parallel-batch `web_extract` Tier 1 (DuckDuckGo)

**What happened:** I started with the most aggressive Tier 1 call — 4 URLs in one parallel batch.

```python
web_extract(urls=[
  "https://www.aliexpress.com/item/1005007254052652.html",
  "https://shopee.vn/Ulanzi-PK16-...",
  "https://www.amazon.com/ULANZI-Release-Adapter-Gimbals-Arca-Swiss/dp/B0F999Y3W8",
  "https://www.ulanzi.com/collections/quick-release-system",
])
```

**Result:** ALL 4 URLs returned the same error in one shot:
```
{"success": false, "error": "DuckDuckGo (ddgs) is a search-only backend
 and cannot extract URL content. Set web.extract_backend to firecrawl, tavily, exa, or parallel."}
```

**Why this burned me:** I wasted 1 round-trip (4 URLs × same broken backend) thinking parallel = efficient. It IS efficient when the backend works; it's wasteful when the backend is broken. The error rate is 100%, not 50%.

**Fix for next time:** Run 1 single-URL `web_extract` first as a backend-detect probe. If it returns the DuckDuckGo error → escalate immediately to Tier 2 in the SAME turn.

### Failure 2: Tier 2 exa fetch_exa "unknown error" on Shopee + Amazon

```python
mcp_exa_web_fetch_exa(urls=[
  "https://shopee.vn/TRIPOD-MINI-...",
  "https://shopee.vn/Tripod-mini-...",
  "https://shopee.vn/Tripod-Máy-Ảnh-...",
])
# Result: 3/3 returned "Error fetching URL(s): ...: unknown error"
```

**Diagnosis:** Shopee VN blocks crawler user agents aggressively. Same issue with Amazon product URLs. Exa's `web_fetch_exa` can't bypass because Shopee serves a captcha or JavaScript-only page.

**Fix:** Skip Shopee + Amazon product URLs in Tier 2 entirely. Use:
- `mcp__exa__web_search_advanced_exa` with the product name + specs keywords (Tier 3 enriched)
- OR `sosanhgia.vn` / `didongaz.com` / aggregator sites that mirror Shopee listings but have crawler-friendly HTML

## What Worked — Tier 3 Enriched with Highlights

Once I knew the chain, the winning pattern for product research was:

```python
mcp__exa__web_search_advanced_exa(
  query="Ulanzi UKA01 quick release plate specs weight dimensions 20kg",
  numResults=5,
  enableHighlights=True,
  highlightsMaxCharacters=800,
)
# Returned:
# Title: "Bộ kit tháo lắp nhanh Ulanzi Uka01 C007 tải trọng 20kg"
# URL:   https://shopnhiepanh.vn/bo-kit-tháo-lắp-nhanh-ulanzi-uka01-c007-tải-trọng-20kg.html
# Highlights: "420.000", "20kg", "52g", "54.3 x 41.3 x 19.6mm", "hợp kim nhôm"
```

**Why this beats `mcp__MiniMax__web_search` for product specs:**
- `enableHighlights` returns the EXACT numeric strings (weights, dimensions, capacities, wattages) verbatim, not paraphrased
- `highlightsMaxCharacters=600-1000` gives ~5-8 quote-style snippets per result
- Multi-source triangulation is easier: do 2-3 queries targeting different angles of same product

**Confirmed worked for:**
- Baseus Magnetic Mini → returned weight 137.6g, capacity 5000mAh / 19.25Wh, USB-C PD 20W, conversion 75%, wireless 5/7.5/10/15W — all from baseus.vn + smartones.com.vn snippets
- Ulanzi UKA01 → 52g, 54.3×41.3×19.6mm, 20kg load, aluminum+silicone — from shopnhiepanh.vn + dof.zone + sonyalpha.vn
- Wiwu Snap Cube → Lightning 5V-3A + Type-C 5V-3A input, 20W Type-C out, 15W wireless — smartones.com.vn
- SANTH CW12 → 169.000 VND exact price from Genk.vn article

## Cross-Source VN Price Triangulation

VN retail prices vary wildly. Real bands from this session:

| Product | Channel A (official) | Channel B (reseller) | Channel C (Shopee) |
|---|---|---|---|
| Baseus Magnetic Mini | 540K (baseus.vn) | 550K (smartones.com.vn) | 763K (mobilekishop.net) |
| Ulanzi UKA01 | 420K (shopnhiepanh.vn) | 490K (dof.zone) | 619K (sonyalpha.vn) |
| SANTH CW12 | 169K (Genk.vn direct) | n/a | 169K (Shopee) |

**Pattern for handling:** Pick the median of the channel spectrum OR report a banded range. Don't pretend there's one universal price.

## Final Output

`research_tiktok_groups_7_8_9.json`:
- **11 products** total (Group 7: 2, Group 8: 7 = SANTH/Baseus/Wiwu/InnoMag/Xiaomi UltraThin/Vention FHN/Cuktech CP12, Group 9: 3 = Floveme TF-3120 / OEM 3120 / Ulanzi MT-08)
- **28 citations** across all SKUs
- 4 rounds of tool calls (instead of 7+ rounds I would have used naively)

Plus the "insights_summary_vi" field which gives Tuấn Anh the strategic angles for content scripting (e.g. "V1-V9 of sạc dự phòng = compare 9 SP từ 169K → 1.59tr", "PK16 gắn Pocket 3 vào xe máy/tủ lạnh").

## Key Insights (Pinned Lessons)

1. **Probe Tier 1 with 1 URL before parallel-batch** — failing 4 in parallel costs the same round-trip as failing 1, but you don't know if the failure is transient until you probe.

2. **Tier 2 selectively** — Shopee VN + Amazon product pages return `"unknown error"` from `web_fetch_exa`. Skip them. Use brand sites, AliExpress, aggregator sites (sosanhgia.vn, didongaz.com, thegioimayanh.com, shopnhiepanh.vn, cellphones.com.vn) — they have crawler-friendly HTML.

3. **For numeric specs, `mcp__exa__web_search_advanced_exa` with `enableHighlights=True` is the canonical answer** — richer than MiniMax snippets, returns exact numbers verbatim.

4. **VN prices need multi-source band reporting** — never claim "giá X VND" without checking 2-3 channels.

5. **Always include "insights_summary" field in research output** — Tuấn Anh (and any consumer of research output) wants strategic angles, not just data. The 30s spent writing insights saves 5 min of user re-reading the raw JSON.

## Update to Parent Skill

Added new section "Pitfall — Don't parallel-batch web_extract" + "Tier 3 enrichment for numeric product specs" + "Cross-source triangulation for VN prices" to `mcp-search-workarounds/SKILL.md`. Bumped pinned lessons from 11 to 15 (added #12-15). Pattern Source list now shows 5 session-origin events. References list now includes this file as the 2026-07-16 entry.
