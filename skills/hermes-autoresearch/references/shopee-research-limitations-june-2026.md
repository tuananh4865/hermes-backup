# Shopee Vietnam Research Limitations — June 2026

**Created:** 2026-06-29  
**Status:** Documented limitation pattern

---

## Problem Summary

When researching Shopee Vietnam affiliate deals, multiple automation barriers prevent real-time data collection:

| Barrier | Date Identified | Impact |
|---------|-----------------|--------|
| Shopee.vn blocks automation (403/timeout) | 2026-06-19 | Cannot scrape product pages |
| Shopee Affiliate Seller Center requires login | 2026-06-19 | Cannot get commission rates, EPC, cookie window |
| MiniMax 1027 on brand queries (Shopee, DJI, etc.) | 2026-06-26 | Web search fails on Shopee-related queries |
| Exa MCP unreachable (6 consecutive failures) | 2026-06-29 | Web search fallback also fails |

## What IS Accessible

- **Web search snippets** — fragments from aggregator sites, KOL posts, news articles
- **Public commission rate ranges** — 2-12% base rate (general category data)
- **KOL reviews on TikTok/YouTube** — view counts, engagement
- **Affiliate aggregator sites** — BitBrowser, Cuelinks (commission ranges only)
- **TikTok Shop public data** — campaign names, voucher amounts (from TikTok's public posts)

## What Is NOT Accessible

- Exact commission rate per product
- EPC (Earnings Per Click)
- Cookie window duration
- CommissionsXtra offers (seller-set bonuses)
- Real-time product prices, ratings, sales volume
- Shopee affiliate link performance metrics

## Research Approach When All Tools Fail

1. Mark output confidence as **LOW** regardless of effort
2. Document all limitations explicitly in output file
3. Flag every deal: "⚠️ Commission rate phải verify trên Seller Center trước khi push"
4. Include general commission rate ranges from BitBrowser/Scribd sources
5. Note upcoming sale events (TikTok Shop 7.7, etc.) as timing opportunities
6. Recommend Anh manually check Seller Center for final affiliate decisions

## Example Output Header

```yaml
---
confidence: low
limitations:
  - Shopee.vn product pages blocked by automation (403 timeout)
  - Shopee Affiliate Seller Center requires login — cannot scrape
  - Exa MCP unreachable — web search only
---
```

## Key Dates

- **2026-06-19:** First documented — Shopee.vn + Seller Center blocked
- **2026-06-26:** MiniMax 1027 confirmed on Shopee queries
- **2026-06-29:** Exa also unreachable — both search backends down

## Related Reference

- `references/shopee-vietnam-scraping-blocked-2026-06-19.md` — Initial Shopee blocking documentation
