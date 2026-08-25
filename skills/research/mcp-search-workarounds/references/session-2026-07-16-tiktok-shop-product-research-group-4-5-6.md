---
title: TikTok Shop Product Research — Session 2 (Groups 4-5-6, brand-name typo pitfall)
created: 2026-07-16
session: 2 of 2 same-day TikTok Shop product research sessions
type: session-reference
tags: [mcp, search, workaround, web-extract, exa, tiktok-shop, product-research, vietnam, brand-typo, dodoto, k-f-concept, pocket-3, vacuum]
related_skills: [deep-research-multi-pillar, self-verify-after-workaround, evidence-first-delivery]
---

# Session: TikTok Shop Product Research — Groups 4-5-6 (2026-07-16, second session)

## Context

User (Tuấn Anh) requested strict-mode research for 3 more product groups destined for TikTok Shop Vietnam content. Same contract as first session (see `references/session-2026-07-16-tiktok-shop-product-research.md`):

- Each product needs: brand + origin, specs, VN retail price, USP, competitors, citations
- Output format: JSON array
- Each product MUST have ≥1 citation URL
- Vietnamese descriptions, English specs

**Task breakdown (this session):**
- **Group 4** — DJI Pocket 3 ốp bảo vệ (cases): 3 brands/plans (Kea Concept, 360° multi-brand, multi-clip)
- **Group 5** — Doroto ELUX V3 handheld vacuum: 2 models (V3 + other mini model)
- **Group 6** — K&F Concept cleaning pen/lens (lens pen + camera pen + lens wipe + macro lens for Pocket 3)

Output: `/Users/tuananh4865/.hermes/research-output/dji-pocket3-camera-accessories-research.json` (~20 KB, 11 products).

## What Worked Same-Day — Pattern Re-Verified

Same pattern from earlier session held perfectly:

1. **Skipped Tier 1 entirely** (`web_extract` — knew DDG backend fails from prior session). Did NOT probe — went straight to Exa `web_fetch_exa` and `web_search_advanced_exa`.

2. **Tier 3 enrichment with highlights** — `mcp__exa__web_search_advanced_exa` with `enableHighlights=True` + `highlightsMaxCharacters=800` worked first try for Sunnylife 754V3 dimensions (52×114×41mm, 35g), K&F Concept KF31.110 case specs, K&F Concept 10X Macro Lens (20-40mm focus distance, magnetic attach).

3. **Tier 2 selective** — `mcp__exa__web_fetch_exa` worked on dodoto.vn, kfconcept.com, kentfaith.com, jola.vn, sunnylife.net. Hit `"unknown error"` on Shopee VN product pages (same Shopee blocking behavior as session 1).

4. **Multi-MCP parallel backend** — running `mcp__MiniMax__web_search` AND `mcp__exa__web_search_exa` in the SAME tool batch returned complementary results (MiniMax for general news/blog mentions, Exa for spec-table data). 4-call batches with mixed backends consistently returned 30-40 useful results per batch.

## NEW Signal from This Session — Brand Name Verification Pitfall

### What happened

User typed **"Kea Concept ốp Pocket 3"** in Group 4. Initial searches across both backends returned ZERO results with this exact brand:

```python
mcp__MiniMax__web_search("Kea Concept DJI Pocket 3 silicone case")  # → 0 hits with this brand
mcp_exa__web_search_exa(query="Kea Concept DJI Pocket 3 silicone case")  # → bikini brand, nail salon, hotel — all unrelated
```

### Diagnosis

"Kea Concept" doesn't exist as a camera accessories brand. Two hypotheses:

1. **Typo for "K&F Concept"** — K&F Concept is the world's #1 filter brand (Euromonitor 2025), has a DJI Pocket 3 silicone case (KF31.110, $9.99), Vietnamese distributor (dji-vietnam.vn).
2. **Typo for another brand** — could be "Kaza Concept", "Klea", etc. but K&F is the most likely because of the K&F Concept + DJI Pocket 3 combo on TikTok Shop VN.

### Fix applied

Did NOT fabricate a brand. Instead:

1. Searched for the actual top-selling ốp DJI Pocket 3 brands on TikTok Shop VN + Shopee VN → found K&F Concept, Sunnylife, BRDRC, Ulanzi, PULUZ, MOBANINA.
2. **Wrote an explicit `note_on_kea_concept` field** at top of output JSON flagging this:
   ```json
   {
     "note_on_kea_concept": "Không tìm thấy brand tên chính xác 'Kea Concept' trong bất kỳ nguồn nào (shopee, tiktok shop, amazon, brand chính hãng). Rất có thể là typo/nhầm lẫn với 'K&F Concept'..."
   }
   ```
3. Recommended K&F Concept as the most likely candidate + listed alternatives Sunnylife/BRDRC/Ulanzi so user can pick.

### Why this matters as a reusable lesson

**Anti-pattern (DO NOT):**
- ❌ Invent specs for "Kea Concept ốp Pocket 3" and write fake citations
- ❌ Skip the brand and silently substitute K&F Concept without flagging
- ❌ Assume the user made no mistake, blame user

**Correct pattern:**
- ✅ Try 2-3 search backends with the EXACT user-provided name verbatim — confirm if brand exists
- ✅ If zero hits, generate candidate list of likely typos/similar brands by topic (k&f concept for camera accessories, kea gear for surf bikinis, etc.)
- ✅ Surface the discrepancy EXPLICITLY in the output (top-of-file note + recommendations)
- ✅ Provide best-guess substitute product data so user can course-correct

**Verification recipe (run before fabricating anything):**
```bash
# Probe 1: exact name across both backends
mcp_MiniMax__web_search('"Kea Concept" "[product category]"')
mcp_exa__web_search_advanced_exa(query='"Kea Concept" camera accessory')

# Probe 2: domain only (if user mentioned a category, search brands in that category)
mcp_MiniMax__web_search('DJI Pocket 3 silicone case top brands Vietnam 2026')
# Returns: K&F Concept, Sunnylife, BRDRC, Ulanzi → hint toward typo
```

**Cost when this fires:**
- 2 extra `web_search` calls upfront
- Saves: fabricating 4-6 fake products (each with 1-2 fake citations) that user would later spot and call out
- Output now has transparency field — user can decide whether to confirm typo or clarify intent

## NEW Signal from This Session — Multi-Backend Parallel Batch

In session 1, I ran batches of 4 Exa searches sequentially and batches of 4 MiniMax sequentially. In this session 2, **I mixed backends in the same parallel batch**:

```python
# Parallel batch with 4 MiniMax + 4 Exa = 8 calls in 1 round-trip
mcp__MiniMax__web_search(["Kea Concept...", "Doroto ELUX V3...", "K&F Concept cleaning pen...", "DJI Pocket 3 case 360..."])
mcp_exa__web_search_exa(["Doroto Lux Air V3 specifications...", "K&F Concept Macro Lens specs...", "Sunnylife 754V3 silicone case dimensions...", "K&F Concept cleaning pen shopee..."])
```

**Result:** Both backends returned complementary result sets in the same round-trip. Exa gave richer spec-table highlights for technical specs; MiniMax gave broader blog/news/PR coverage.

**Lesson:** When researching physical products, mix backend types in one parallel batch:
- **MiniMax**: blog mentions, news articles, social media, Vietnamese sources
- **Exa (`web_search_advanced_exa` + highlights)**: spec tables, official product pages, structured numeric data
- **Exa (`web_fetch_exa`)**: full-page markdown when you need more than snippet

## NEW Signal from This Session — Dodoto Brand Origin Pattern (Vietnamese OEM)

Discovered that **Dodoto** (sometimes typed "Doroto" by users) is a Vietnamese brand:

- Hộ kinh doanh Phạm Đình Hiên — Vietnamese sole proprietorship registered under dodoto.vn
- Products OEM-manufactured in China (Lux Air V3 = 140W, 25.000Pa, ABS shell)
- Sells direct via dodoto.vn + shopee franchise store + Facebook Page dodotoshop

**Implication for research:** When user lists a brand name and you find a Vietnamese .vn domain + Vietnamese sole proprietorship info, suspect Vietnamese brand OEM from China. This affects how you price-compare (Dodoto direct price = retail, no distributor markup).

## Cross-Reference: Search Backends Hit-and-Miss for This Session

| Backend | Worked for | Failed for |
|---|---|---|
| `mcp__MiniMax__web_search` | dodoto.vn (snippets), Facebook DJI Osmo Pocket VN group, shopee.vn listings, jola.vn product page | brand sites with JS-heavy pages (kfconcept.com), TikTok Shop internal pages |
| `mcp__exa__web_search_advanced_exa` (+ highlights) | shopnhiepanh.vn, giangduydat.vn, diemdo.vn, mayanh24h.com, imax.com.vn, dodoto.vn (with highlights) | Reddit (no highlights match needed), Shopee VN (same crawl block) |
| `mcp__exa__web_fetch_exa` | dodoto.vn, kfconcept.com (clean markdown), kentfaith.com, jola.vn, sunnylife.net, goodio.be, distrinode.co.za, smartizz.com | Shopee VN product URLs, Amazon product URLs |
| `web_extract` | SKIPPED ENTIRELY (known DDG fail) | n/a |

## Final Output Notes

JSON file at `/Users/tuananh4865/.hermes/research-output/dji-pocket3-camera-accessories-research.json` includes:

- 11 products across 3 groups
- ~40 citation URLs (across shopee, dodoto.vn, kentfaith, kfconcept.com, amazon, Reddit, jola, sunnylife, Facebook, etc.)
- `note_on_kea_concept` field flagging the typo
- `insights_summary` field with strategic angles (K&F vs BRDRC pricing tier, Dodoto Lux Air V3 vs Xiaomi Deerma comparison, K&F Macro Lens viral on Reddit r/osmopocket)
- Vietnamese descriptions, English specs (matching user's bilingual contract)

## Update to Parent Skill

This reference is **session 2 of 2 same-day TikTok Shop product research sessions**. Skill already has session 1 reference at `references/session-2026-07-16-tiktok-shop-product-research.md`. This adds:

- **Lesson #16 (NEW):** Brand-name verification protocol — when user-provided brand returns 0 results, probe with exact name verbatim, generate likely-typo candidates, surface discrepancy explicitly in output (do NOT fabricate).
- **Lesson #17 (NEW):** Mix web-search backends (MiniMax + Exa `web_search_advanced_exa`) within one parallel batch for complementary coverage.
- **Lesson #18 (NEW):** Vietnamese OEM brand pattern — when .vn domain + Vietnamese sole proprietorship → flag as Vietnamese brand with China OEM, affects price triangulation.

## Conversation transcript: the user's prompt verbatim

```
Research CHÍNH XÁC thông tin 3 nhóm sản phẩm TikTok shop dưới đây. Mỗi sản phẩm cần tìm: brand name + origin, specs kỹ thuật, giá bán lẻ thị trường VN, USP chính, đối thủ cạnh tranh, đánh giá.

Nhóm 4 — Ốp bảo vệ DJI Pocket 3:
- Kea Concept ốp Pocket 3
- Ốp bảo vệ 360° cho Pocket 3 (multiple brands)
- Ốp Pocket 3 nhiều loại (đã edit 4 clip)

[...]

Yêu cầu:
1. Dùng web_search + web_extract để lấy data thật từ shopee.vn, tiktok.vn, amazon
2. Mỗi sản phẩm PHẢI có ít nhất 1 citation URL nguồn thật
3. Output format JSON array [...]
```

**Notable:** User wrote "web_extract" but Tool's actual backend is broken (DDG search-only). I had to interpret as "use web search / web extraction tools" and pivot to Tier 2 exa `web_fetch_exa` + advanced search with highlights. Same pattern as session 1 — this is now the canonical workflow.

## Related

- `references/session-2026-07-16-tiktok-shop-product-research.md` — Session 1 (Groups 7-8-9: quick-release plate, MagSafe power bank, mini tripod) — establishes the working pattern
- `references/session-2026-07-07-tru1-sales-psychology-1027.md` — different lesson (operator-less 1027 trigger); references companion
- `references/ml-model-research-tier5-curl-github.md` — Tier 5 for ML models, not e-commerce
- `../SKILL.md` pinned lessons #1-15 — existing workarounds, this ref adds #16-18
