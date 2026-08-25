# Shopee Vietnam — Web Scraping Blocked (2026-06-19)

**Session:** 2026-06-19 Shopee Affiliate Research Cron — Friday rotation: tripod/mount/accessory

## Finding

**Shopee.vn blocks automated content extraction.**

When running `mcp_exa_web_fetch_exa` on Shopee URLs:
```
Error fetching URL(s): https://shopee.vn/ulanzivietnam: unknown error
https://shopee.vn/search?keyword=tripod: CRAWL_LIVECRAWL_TIMEOUT
```

Both direct product pages AND search result pages are blocked.

## Impact on Research Workflow

| Tool | Shopee Target | Result |
|------|---------------|--------|
| `mcp_MiniMax_web_search` | ✅ Works | Returns snippets with product names, prices, ratings |
| `mcp_exa_web_fetch_exa` | ❌ BLOCKED | CRAWL_LIVECRAWL_TIMEOUT |
| `web_extract` | ❌ Likely blocked | Same anti-bot detection |

## Workaround Used (This Session)

1. Used web search snippets — returns product names, prices, ratings from Shopee search results
2. Extracted data from:
   - Vietnamese review YouTube videos (YouTube descriptions contain Shopee links)
   - Shopee Mall brand pages indexed in search results
   - Vietnamese Facebook/Instagram posts mentioning Shopee products
3. Commission rates sourced from **third-party affiliate sites** (BitBrowser, Cuelinks, Indoleads) not Shopee itself

## Data Quality Achieved

| Data Type | Source | Quality |
|-----------|--------|---------|
| Product names/prices | Web search snippets | ✅ Adequate |
| Ratings/sales volume | Web search snippets | ✅ Adequate |
| Commission rate ranges | Third-party affiliate sites | ✅ Adequate |
| Exact commission per product | ❌ Not available | Requires Seller Center login |
| EPC, cookie window | ❌ Not available | Requires Seller Center login |

## Anti-Pattern: Trying to Extract Shopee Pages Directly

**DO NOT:**
```python
# WRONG — will timeout:
web_extract(["https://shopee.vn/product/..."])
mcp_exa_web_fetch_exa(["https://shopee.vn/search?keyword=tripod"])

# WRONG — Shopee blocks cua-driver/headless browser:
computer_use → navigate to Shopee
```

**INSTEAD — Use web search as the primary Shopee data source:**
```bash
# Web search for Shopee products — returns rich snippets:
mcp_MiniMax_web_search query="Ulanzi MT80 Shopee Vietnam tripod price"

# Vietnamese keywords work well:
mcp_MiniMax_web_search query="chân tripod ulanzi Shopee 2026 giá"

# Combine with YouTube for product links:
mcp_MiniMax_web_search query="tripod review Shopee Vietnam TikTok 2026"
```

## Session Outcome

Research completed for tripod/mount/accessory niche:
- 5 products identified (Ulanzi MT80, F360T, TSS PLUS, SmallRig, JJC)
- Commission rate ranges documented (6-8% for Cameras & Drones category)
- **⚠️ Critical limitation flagged:** Exact commission per product requires Seller Center login
- Research file saved to: `~/Workspace/Claude/Projects/Content Creator/Research/2026-06-19/shopee-deal-tripod-mount-accessory.md`
- Wiki saved to: `wiki/queries/shopee-affiliate-tripod-accessory-june-2026.md`

## Related

- Skill section: `## ⚠️ CRITICAL LIMITATION: Shopee Affiliate Dashboard Data (2026-06-17)`
- This session: Shopee 6.6 sale confirmed still running (1-7/6/2026)
