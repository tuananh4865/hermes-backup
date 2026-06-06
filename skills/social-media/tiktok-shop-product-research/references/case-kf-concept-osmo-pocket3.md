# Case Study: K&F Concept Filter Set for DJI Osmo Pocket 3

**Date:** 2026-06-06
**Source session:** User sent Shopee link, then asked "Check top những video review sản phẩm này được nhiều view nhất!"

## Product snapshot
- **Name:** K&F Concept 3 Bộ lọc từ tính CPL + Black Mist 1/4 + ND2-ND32
- **Compatible:** DJI Osmo Pocket 3 / 4
- **Key feature:** Magnetic mount, multi-coated HD optical glass
- **Shopee URL slug:** `i.822371109.25979426475`

## What worked in this session
1. **Decoded product from URL** — Shopee link slug contains brand + product type + device.
2. **Shopee block was accepted gracefully** — web_extract 400'd, browser showed "Page Unavailable" (anti-bot). Didn't burn cycles trying to bypass — moved to YouTube.
3. **YouTube view count extraction from search results** — `browser_navigate` to YouTube search, snapshot includes view counts under titles. No need to click through.
4. **Two-query triangulation** — searched "K&F Concept magnetic filter DJI Osmo Pocket 3 review" and "K&F Concept Osmo Pocket 3 filter magnetic best" — second query caught additional listicle videos.
5. **Pattern extraction** — identified that top 3 videos all used "Worth It?", "Fixed vs Variable", and demo patterns. The 46s official video got 8.4K only — proving long-form works better for this niche.
6. **Content gap identification** — found 5 angles no competitor had done (durability test, K&F vs DJI official, reverse psychology, Vietnam vlog, TikToker POV).

## Top videos captured
| # | Video | Channel | Views |
|---|-------|---------|-------|
| 1 | K&F Fixed vs Variable ND Filters on the Osmo Pocket 3 | Capture Guide | 51K |
| 2 | Osmo Pocket 3 ND FILTERS – Worth It? | Joey Vela | 50K |
| 3 | DJI Osmo Pocket 3 Variable ND Filters K&F Concept Review | AbbyBReviewing | 18K |
| 4 | Almost Perfect DJI Osmo Pocket 3 Mounts // K&F Concept | ROAM it RALPH | 10K |
| 5 | K&F CONCEPT Filter Kit For DJI Osmo Pocket 3 | K&F CONCEPT (official) | 8.4K |

## Verdict given to user
- **Market:** Niche, top view ~51K, not explosive but viable
- **Risk:** Saturated by Chinese brand official + a few KOLs
- **Recommendation:** Could test with 3 scripts in 7 days, but warned user that this is a niche market, not a hot trend
- **Final CTA:** Offered A/B/C/D options, recommended B (research other product) as more likely to be explosive

## Lessons for next time
- When Shopee blocks, **move to YouTube search in 1 tool call** — don't keep retrying web_extract
- For camera/gear niches, view counts top out around 50K-100K — this is normal, not a failure of the product
- Always check the **official brand channel** video (K&F CONCEPT had 8.4K only with 46s clip) — this proves short-form doesn't work for technical reviews
- "Worth It?" question format in title = proven hook pattern, copy this structure for new products
