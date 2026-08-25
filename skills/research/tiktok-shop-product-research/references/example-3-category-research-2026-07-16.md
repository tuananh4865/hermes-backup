---
title: Worked Example — 3-Category Product Research (Body Mist, Tripod, Stylus)
type: reference
date: 2026-07-16
parent_skill: tiktok-shop-product-research
---

# Worked Example: 11-Product Research Across 3 Categories

This is the actual JSON output from a session that researched 3 product groups (Body Mist, Ulanzi Tripod, iPad Stylus) for TikTok Shop script writing. Future sessions should treat this as a reference for structure, depth, and citation patterns.

## What this example demonstrates

- **Mixed branded + OEM products** (ARMAF branded vs AMAP/AMF/Goldjordock OEM)
- **Descriptor-not-brand** disambiguation (Lemony ≠ brand; Gojodot 0700 = GOOJODOQ CD3293)
- **VN retailer price sourcing** from 6+ different Vietnamese retailers
- **Dual-language output** (English specs, Vietnamese descriptions)
- **Honest limitations section** (which products lack brand websites)

## Categories researched

| Group | Products | OEM products | Branded products |
|-------|----------|--------------|------------------|
| Body Mist | 5 (ARMAF Mega, ARMAF Homme, AMAP, AMF, Lemony) | 3 | 2 |
| Tripod Ulanzi | 4 (MA66, MG-002/SK-03, MT-10/PK-08/TT38, full ecosystem) | 0 | 4 |
| iPad Stylus | 2 (GOOJODOQ 0700, Goldjordock) | 1 | 1 |

## Citation pattern observed

- **ARMAF products**: 4-6 citations each (armaf.com + armaf.uk + armafvietnam.vn + classic.vn + annguy.vn + fragrantica.com)
- **Ulanzi products**: 5-6 citations each (ulanzi.com + huylinh.net + kingcom.com.vn + ulanzi.jp + cined.com + amazon.com)
- **GOOJODOQ products**: 4-6 citations (goojodoqglobal.com + manual.goojodoqglobal.com + amazon + ftpshop.com.vn + dienmayxa.com)
- **OEM products (AMAP/AMF/Goldjordock)**: 2-4 citations each (Alibaba wholesale + accio.com + shopee search URL + brand disambiguation note)

## JSON file location

The full output is at `~/tiktok_product_research_2026.json` (33KB). Schema and fields match the parent skill's output schema exactly.

## Time budget observed

- 4 parallel search batches (~12 web_search calls)
- 8 parallel Exa MCP searches
- 1 write_file call for final JSON
- Total: ~15 tool calls, ~10 minutes

## Lessons extracted into parent skill

1. Always classify OEM vs branded BEFORE searching
2. Use `mcp__exa__web_fetch_exa` not `web_extract` (DDG is search-only)
3. Batch 5-8 parallel searches per turn
4. Cite 2-3 sources per product minimum
5. Document limitations honestly (OEM status, naming variants, price volatility)
6. Disambiguate descriptors (Lemony, Gojodot 0700) upfront in the brand field

## Niche knowledge captured (reusable across future Body Mist / Tripod / Stylus research)

### Body Mist VN price reference points (2026)
- Bath & Body Works 236ml: 350-500k
- Victoria's Secret 250ml: 400-600k
- ARMAF Odyssey 200ml: 239-400k
- Body Holic (Hàn) 100ml: 160k
- AMAP/AMF/Shimang 50-100ml: 89-150k

### Ulanzi Pocket 3 ecosystem prices
- PM-01 magnetic: 579k
- PK-06 expansion: 690k
- PK-08 mini tripod auto-fold: 199k
- MA66 magnetic tripod: 590-750k
- Full bundle: $99.99 (~$2.5tr)

### iPad stylus VN price reference points (2026)
- Apple Pencil 1: 2.5-3tr
- Apple Pencil 2: 3.5-4tr
- Apple Pencil USB-C: 2.3tr
- Logitech Crayon: 1.8tr
- GOOJODOQ CD3293 base: 199k
- GOOJODOQ GD13 wireless: 400-549k
- Goldjordock OEM: 99-199k