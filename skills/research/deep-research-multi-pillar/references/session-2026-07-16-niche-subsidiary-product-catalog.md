# Session 2026-07-16 — Niche Subsidiary Product Catalog (3-group TikTok Shop)

## Source session

User brief (verbatim):
> Research CHÍNH XÁC thông tin 3 nhóm sản phẩm TikTok shop dưới đây.
> **Nhóm 10** — Bộ vệ sinh ống kính (Pocket 3): Bộ vệ sinh ống kính cho DJI Pocket 3 (brand PocketBar Trung Quốc?)
> **Nhóm 11** — Đèn LED dán tường mini (remote): Đèn LED dán tường mini có remote điều khiển
> **Nhóm 12** — Body Mist Lemony + các brand phụ: Lemony Body Mist (brand nào?) — Các body mist niche khác nếu tìm được
>
> Yêu cầu:
> 1. Dùng web_search + web_extract
> 2. Mỗi sản phẩm PHẢI có ít nhất 1 citation URL
> 3. Output format JSON array giống các subagent khác
> 4. Đặc biệt chú ý: 2 nhóm này là sản phẩm phụ, có thể ít data — cần search sáng tạo hơn

## Outcome

- **13 products** total across 3 groups (5 + 3 + 5)
- **60+ citations** verified (1-7 per product)
- **19.9 KB JSON** at `/Users/tuananh4865/tiktok_shop_groups_10_11_12.json`
- All 3 groups delivered, no fabrication, both brand-name mismatches documented upfront

## Critical pattern: brand-name category-mismatch trap (Pitfall #19)

Two of three brand hints in the brief did not exist in the named category. The session demonstrated the right response:

### "PocketBar" (Group 10)
- Brief expected: brand Trung Quốc, bộ vệ sinh ống kính DJI Pocket 3
- Search returned: Solea Stockholm (Sweden) PocketBar™ = mini crowbar (kofot), 229 kr
- Action: Documented mismatch in `note_pocketbar_brand`, expanded search to "DJI Pocket 3 lens cleaning kit" parent category
- Result: 5 alternatives delivered (Lenspen, VSGO DKL-15, FB generic kit, Hoodman, Zeiss)

### "Lemony" (Group 12)
- Brief expected: standalone body mist brand called "Lemony"
- Search returned: "Lemony" is a variant name used across multiple brands (Sapital citrus line, BODYMISS Funky Fresh with chanh vàng, Sol de Janeiro Limonada Gelada, Lush Lemony Flutter LE)
- Action: Documented mismatch in `note_lemony_brand`, searched retailers (Sapital.vn → product line catalog → citrus variants), checked Limited Edition / LE / seasonal labels
- Result: 6 alternatives delivered covering brand spectrum from VN local (BODYMISS 49k-140k) to UK LE (Lush 650k-1.2tr)

## What worked

1. **Parallel backend mix** in single round-trips — `mcp__MiniMax__web_search` + `mcp__exa__web_search_exa` returned complementary results (social mentions + structured specs).
2. **Avoided `web_extract`** — Tier 1 (DuckDuckGo) failed consistently for Shopee VN URLs. Skipped directly to MCP backends.
3. **In-line batched calls** — 3 groups fit comfortably in 15-20 calls per group; no need for `delegate_task`. Subagent overhead would have exceeded research work.
4. **Top-of-file `note_*` fields** — explicit mismatch documentation at JSON root kept the deliverable honest.
5. **JSON schema enforcement** — verified every product had ≥1 citation before final output.

## What failed / required retry

- 2 `mcp__MiniMax__web_search` queries hit API 1027 (operator-less keyword combinations). Retried with simplified queries. Cross-reference [[mcp-search-workarounds]] Pitfall #2 (operator-less 1027).
- `web_extract` consistently returned "DuckDuckGo (ddgs) is a search-only backend" for Shopee URLs — same failure mode as the parallel-batch pitfall #13 documented in the same skill set.

## Cross-references

- [[mcp-search-workarounds]] — Pitfalls #13 (parallel-batch web_extract), #16 (brand typo), #19 (brand category-mismatch — origin session)
- Output file: `/Users/tuananh4865/tiktok_shop_groups_10_11_12.json` (13 products × ≥1 citation each)
- Session task completed in ~15-20 search calls, no subagent dispatched