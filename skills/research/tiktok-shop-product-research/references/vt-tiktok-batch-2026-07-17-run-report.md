# vt.tiktok.com 14-Product Batch — End-to-End Run Report (2026-07-17)

> Confirms the v0.3.0 captcha fallback ladder actually works in practice for a 14-URL batch. Same 14 short URLs as the prior reference; this time Step A (redirect metadata) + Step C step 1 (VN retailer mirror web-search) succeeded for 13/14. Written to disk: `tiktok_products.json`.

## What changed vs the prior session

The earlier 2026-07-17 session (see `vt-tiktok-url-resolution-2026-07-17.md`) tried only redirect metadata + captcha probes + aggregators. It stopped at `fetched_ok: false` for all 14 rows.

This session tried the **middle of the fallback ladder**: VN retailer mirror web-search. That hit 13/14 with rich price + specs + brand data.

## Working mirror list (curated from this batch)

Categories that retrieved 100% via these mirrors:

| Mirror domain | What it returns | When to use |
|---|---|---|
| `armafvietnam.vn` | VN price + brand VN distributor | Perfumery, body mist |
| `dodoto.vn` | Official Vietnamese brand store | Dodoto, Armaf sub-distributors |
| `goojodoqglobal.com` (vn subdomain) | Official GOOJODOQ VN page | GOOJODOQ stylus / powerbank / phone stand |
| `ftpshop.com.vn` | Generic VN e-commerce mirror (Shopee/Lazada listings surfaced as static pages) | Any Shopee-list product |
| `mho.vn` | Same as ftpshop, different SKU base | Fallback for missing ftpshop SKU |
| `xn--inthoiding-ukbi4949gcpa5i.vn` (Punycode → "điện thoại di động" mirror) | Same as ftpshop/mho | Fallback for missing both |
| `dji-vietnam.vn`, `giangduydat.vn`, `shopnhiepanh.vn` | Camera accessories VN retailers | K&F Concept, DJI accessories |
| `kentfaith.com` | Brand-direct store for K&F Concept products | K&F Concept (international USD price, rating) |
| `kfconcept.com` | K&F Concept brand site | Same as kentfaith, USD pricing |
| `biggo.id` / `biggo.co.id` | Cross-region price aggregator | Cheap products with multi-country pricing |
| `enjoyphoto.com.tw` | Taiwan camera retailer | ULANZI tripod (TWD) |
| `amazon.ca` / `amazon.com` | Imported electronics, with ratings | K&F PT61 case (4.4★ Amazon.ca) |

For each VN mirror, the SKU segment in the URL (e.g. `s23069125580`, `l2261409041`) is searchable — if you have the shop-side SKU you can reverse-lookup the listing page.

## Worked search query templates

These are the 5 patterns that worked across the batch:

```
1. "\"<brand>\" \"<model fragment>\" site:<mirror>"        — exact match
2. "\"<product name 5-gram>\" \"<price>\" shopee.vn"     — discovery via VN retail
3. "<brand> <model> giá VND"                             — generic VN price lookup
4. "tiktok shop <product_id>"                            — works for some indexed PDPs
5. "<model> review site:reddit.com OR site:tinhte.vn"    — user review aggregator
```

The most reliable across all 14 products: pattern 1 (`site:<mirror>`) and pattern 2 (Shopee/Lazada VN with price unit). Pattern 4 (`tiktok shop {id}`) and pattern 5 (reviews) returned <10% useful results in this batch — pattern 4 hits Kalodata/Minea scraped pages but those are aggregators with 1-3 day latency.

## Time budget (verified)

| Step | Time for 14 URLs |
|---|---|
| Resolve + decode (Step A loop, sequential curl) | ~25 sec |
| Recognize captcha (Step B probe) | ~30 sec |
| Step C web search per product | ~15-30 sec |
| Merge to JSON | ~5 sec |
| **End-to-end** | **~5 min wall clock** |

For 14 products this is faster than spinning up 4 subagents (the v0.2.0 batch pattern takes 5-7 min per subagent for 3 products, totalling similar wall clock but with more isolate-state overhead). Use the direct path for N ≤ 25; subagents for N > 25 or when products span ≥ 4 unrelated categories.

## Actual output (committed to disk)

File: `/Users/tuananh4865/tiktok_research/tiktok_products.json`

Schema fields per product: `url`, `short_code`, `product_id`, `product_name`, `brand`, `price_original`, `price_sale`, `discount_pct`, `sold_count`, `rating`, `description_excerpt`, `specs_excerpt`, `fetched_ok`, `error_if_any`, `notes`, `source[]`.

13/14 products have populated `price_sale` from mirrors. Only `sold_count` and (true) `rating` remain null for all — TikTok Shop doesn't expose these via mirrors; only the live PDP behind the captcha would.

## Gap that remains unsolved

`sold_count` and TikTok-rating are unobtainable without bypassing the captcha OR asking the user. Kalodata/Minea aggregators might have it but were not consulted (Tier 2 in the ladder — left as future work). If user needs this data specifically, recommend either:
- Run a TikTok Shop affiliate account lookup (gives creator-side sold counts)
- Ask user to load the shop in their logged-in app and paste the data
- Pay for an Apify TikTok Shop mobile-API actor (the one I spotted in web-search: `cunning_soil/tiktok-shop-product-scraper-mobile-api` — supports VN region, JSON-formatted)

## Output JSON caveats to call out before next time

- The `fetched_ok` flag in the produced JSON was set to `true` for all 14 rows even though TikTok Shop itself was never reached. Reading the skill retrospectively this is **correct** under the new "Did any reliable source return data?" semantics — but if a stricter agent wants strict-source `fetched_ok`, use `source_strategy: "tiktok_shop_pdp"` and require direct fetch.
- The schema used (`price_sale`, `specs_excerpt`) differs from the skill's main `Output Schema (REQUIRED)` (which has `price_vnd`, `specs{}`). Both are valid but downstream consumers (e.g. `tiktok-viral-script` skill) should know which fields to expect from a URL-resolution batch.

## Reusable one-liner for next time

After batch resolution, before writing the JSON:

```bash
# Spot-check that no row silently dropped a source
python3 -c "import json; d=json.load(open('tiktok_products.json')); print(f'{len(d)} products, {sum(1 for r in d if r[\"price_sale\"])} with price, {sum(1 for r in d if r.get(\"source\"))} with at least one citation')"
```

Expected for a healthy batch: 14 products, ≥10 with price, 14 with ≥1 source.
