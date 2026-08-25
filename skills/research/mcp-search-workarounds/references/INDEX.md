# mcp-search-workarounds — Reference Index

Quick pointer map for the references/ directory.

| File | Captured | What it documents |
|------|----------|-------------------|
| `ml-model-research-tier5-curl-github.md` | 2026-07-09 | Tier 5 (curl raw GitHub) — full recipe + YAMNet transcript. Use when researching any ML model: class IDs, hyperparameters, inference code, architecture. |
| `session-2026-06-17-fable5-search.md` | 2026-06-17 | 4 MCP queries, 2 hit `1027-output new_sensitive`. Origin of the 3-step fallback chain. |
| `session-2026-06-28-trend-scan.md` | 2026-06-28 | Tier 1 (web_extract) + Tier 2 (exa) failures → Tier 3 (phrase search) recovery. EF slang definitions, 4-source cross-validation. |
| `session-2026-07-07-tru1-sales-psychology-1027.md` | 2026-07-07 | First verified case of **operator-less 1027 trigger** (Bencivenga "Bullseye", Brunson HSO). Paraphrased fallback discipline + Appendix A transparency rule. |
| `session-2026-07-16-tiktok-shop-product-research.md` | 2026-07-16 | **NEW.** Parallel-batch `web_extract` waste (4 URLs × DuckDuckGo fail); Shopee/amzn `"unknown error"` from Tier 2; `mcp__exa__web_search_advanced_exa` + `enableHighlights=True` for numeric product specs; cross-source VN price triangulation (540K vs 763K same SKU). Use when researching physical products with specs/prices. |

**Rule of thumb for picking a reference:**
- ML model research (architecture, class IDs, exact code/CSV) → `ml-model-research-tier5-curl-github.md`
- Operator 1027 errors with `site:` → `session-2026-06-17-fable5-search.md`
- Tier 1+2 extraction cascade fails → `session-2026-06-28-trend-scan.md`
- Operator-less keyword 1027 (creator + concept + salesy) → `session-2026-07-07-tru1-sales-psychology-1027.md`
- Physical product research (specs/prices/VN channels) → `session-2026-07-16-tiktok-shop-product-research.md`
