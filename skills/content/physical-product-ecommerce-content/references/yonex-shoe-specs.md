# Yonex Shoe Spec Research — Reference Data & Methodology

> Verified 2026-07-08 from us.yonex.com (official US), badmintonwarehouse.com (retailer), ckyew.com (Gen-3 reviewer), bonbonbadminton.com (spec dump). Use as the canonical data source for Yonex shoe specs in `tuan-anh-badminton` project.

## Why this file exists

Tuấn Anh Badminton sells Yonex shoes alongside rackets. Pitfall #36 (in SKILL.md) requires verifying specs from ≥2 official sources before writing any content. This file is the **first cached spec bank for the shoe segment** — mirror of the racket `products/<model>.md` rule.

## ⚠️ Pitfall #37 — "Subaxia" without "GT" does NOT exist as a Wide

When user (or yourself) says "Yonex Subaxia Wide", they almost always mean the **Subaxia GT Wide** (SHBSG1W, launched Dec 2025 / Jan 2026). The Subaxia line has:

- `Subaxia GT` (Men's, standard width) — colorway "Dark Gray"
- `Subaxia GT Wide` — colorway "**Gray**" (different from Men's colorway)
- `Subaxia GT1 Wide` — alternate SKU (same tech, different number)

There is **no plain "Subaxia Wide"** without the GT suffix. If a search returns "Subaxia" alone, it's usually referring to the GT series. Verify SKU on Yonex USA before writing content.

## ⚠️ Pitfall #38 — Yonex does NOT publish exact gram weights

Unlike rackets (which always have a published weight in 3U/4U notation), Yonex shoes have **no official gram-per-shoe spec** on the product page. Retailers give qualitative descriptors ("relatively light for a high-cushion shoe"). For weight, you must:

1. Use the standard-width version's commonly cited figure as a baseline (e.g. 65 Z4 ~300g, Subaxia GT Men's ~305g)
2. Add ~10-15g for the Wide last (extra material)
3. Label as **estimate, not official** in any spec table

Do NOT publish a gram weight as fact. Either omit the field or label as `~300g (estimated)`.

## EUR 42 = US M 9 = 27.0 cm (shoe size conversion for Yonex)

This is the most-asked size in Tuấn Anh Badminton orders. Memorize:

| EUR | US Men | US Women | cm |
|-----|--------|----------|----|
| 40  | 7.5    | 9        | 25.5 |
| 40.5| 8      | 9.5      | 26.0 |
| 41  | 8.5    | 10       | 26.5 |
| **42**  | **9**  | **10.5**  | **27.0** |
| 43  | 9.5    | 11       | 27.5 |
| 44  | 10     | 11.5     | 28.0 |

Both 65 Z4 Wide and Subaxia GT Wide run EUR 37.5-47 (23.5-31.0 cm) — same size grid. Wide version is unisex in sizing but Yonex still labels "M 9 / W 10.5".

## Verified spec records (canonical JSON, copy as base for wiki)

### 1. Yonex Power Cushion 65 Z4 Wide (SHB65Z4W)

```json
{
  "model": "Yonex Power Cushion 65 Z4 Wide (SHB65Z4W)",
  "upper": "Synthetic Leather (seamless) + Double Raschel Mesh panels",
  "midsole": "Synthetic Resin with Power Cushion+ + Feather Bounce Foam + Power Graphite Sheet (midfoot plate)",
  "outsole": "Rubber (gum rubber) with Radial Blade Sole pattern",
  "width": "Wide (unisex, wider forefoot)",
  "weight_g": 300,
  "weight_note": "Approx 300g for size 26.0cm. Yonex does not publish exact gram weight; size 42 EUR (27.0cm) estimated ~310-315g",
  "size_range": "EUR 37.5-46 (22.0-30.0cm, +31.0/32.0cm); US M 5.5-12 / W 7-12. Size 42 EUR = M 9 / 27.0cm",
  "key_tech": [
    "Power Cushion+ (shock absorption + repulsion)",
    "Feather Bounce Foam",
    "Power Graphite Sheet",
    "Double Raschel Mesh",
    "Seamless Upper",
    "Radial Blade Sole (+3% traction)",
    "Inner Bootie",
    "Toe Assist Shape",
    "Lateral Shell"
  ],
  "target": "Club to competition — wide-footed performance players",
  "price_usd": 135,
  "price_jpy_msrp": 19000,
  "price_note": "$135 Yonex USA; ~$125 street (Badminton Warehouse). JPY MSRP ~19,000",
  "color": "White (primary)",
  "release": "January 2025 (12th generation)",
  "official_url": "https://us.yonex.com/products/power-cushion-65-z4-wide",
  "sku": "SHB65Z4W"
}
```

### 2. Yonex Subaxia GT Wide (SHBSG1W) — Gray

```json
{
  "model": "Yonex Subaxia GT Wide (SHBSG1W) — Gray",
  "note": "The only 'Subaxia Wide' is the Subaxia GT Wide (2026). Men's standard width = Dark Gray; Wide version colorway = Gray.",
  "upper": "Synthetic Resin (Durable Skin Light) + Double Raschel Mesh + Inner Bootie + Lateral Shell",
  "midsole": "Synthetic Resin — GRPHT THRTTL (Power Graphite plate + Power Cushion Rev) + Split Midsole (firmer forefoot / softer heel) + Feather Bounce Foam",
  "outsole": "Rubber (indoor court) with Radial Blade Sole + Round Sole",
  "width": "Wide (unisex, roomier forefoot)",
  "weight_g": 320,
  "weight_note": "Yonex does not publish gram weight. Retailers describe 'relatively light for high-cushion shoe'. Estimated ~315-325g for size 27.0cm",
  "size_range": "EUR 37.5-47 (23.5-31.0cm); US M 5.5-13 / W 7-12. Size 42 EUR = M 9 / 27.0cm",
  "key_tech": [
    "GRPHT THRTTL (+37% impact absorption, +42% repulsion vs Hyper msLite)",
    "3D Heel Cushioning",
    "Split Midsole with Optimized Hardness",
    "Feather Bounce Foam",
    "Double Raschel Mesh",
    "Durable Skin Light",
    "Radial Blade Sole",
    "Round Sole",
    "Lateral Shell",
    "Toe Assist Shape",
    "Synchro-Fit Insole",
    "Inner Bootie"
  ],
  "target": "Intermediate to advanced / competition — aggressive movers, wide-footed",
  "price_usd": 155,
  "price_jpy_msrp": 22000,
  "price_note": "$155 Yonex USA; JPY MSRP ~22,000",
  "color": "Gray (primary Wide colorway; also Dark Green)",
  "release": "2026 (launched Dec 2025/Jan 2026)",
  "official_url": "https://us.yonex.com/products/subaxia-gt-wide",
  "sku": "SHBSG1W"
}
```

## Spec research methodology (reusable for any new Yonex shoe)

### Sources (in priority order)

1. **us.yonex.com** or **yonex.com/japan** — official product page. Has SKU, color, tech list, size grid, official URL. Lacks: exact gram weight, JPY MSRP.
2. **badmintonwarehouse.com** — best retailer for spec dumps + verified size grid in EUR/US/cm. Has user reviews.
3. **ckyew.com** — best for Gen-3 (latest) reviews with deep tech explanation. Useful for understanding what each tech DOES.
4. **bonbonbadminton.com / joybadminton.com / badmintonhq.co.uk** — alternative retailers, useful for colorway comparison + JPY MSRP conversion.
5. **Amazon product listings** — sometimes include detailed tech specs copy-pasted from manufacturer.

### Tool fallback pattern

- `web_search` returns 5 results — good for SKU/color confirmation
- `web_extract` may fail with "DuckDuckGo search-only backend" — fall back to `mcp__exa__web_fetch_exa` for actual page content
- `browser_navigate` is overkill for spec lookup — only use if Exa fails AND page has JS-rendered specs

### Fields to always capture for a Yonex shoe

```json
{
  "model": "Full marketing name + SKU in parens",
  "upper": "Material composition",
  "midsole": "Material + tech names (Feather Bounce, Power Cushion+, GRPHT THRTTL, etc.)",
  "outsole": "Rubber type + pattern name",
  "width": "Standard / Wide / Extra-Wide (note unisex if applies)",
  "weight_g": 0,
  "weight_note": "estimate basis if not official",
  "size_range": "EUR range + US + cm",
  "key_tech": ["array of tech names — exactly as Yonex capitalizes"],
  "target": "Player level + use case",
  "price_usd": 0,
  "price_jpy_msrp": 0,
  "price_note": "USD retail + JPY retail street price",
  "color": "Primary colorway name",
  "release": "Month + year + generation note",
  "official_url": "us.yonex.com or yonex.com/japan product page",
  "sku": "parent SKU from official page"
}
```

### Output file convention

For each new shoe, save to `wiki/projects/tuan-anh-badminton/products/shoes/<model-slug>.json` with the same schema. Mirror to `wiki/products-inventory.md` if SKU is in shop inventory.

## Known gaps in this data

- **Gram weights**: estimated only (Pitfall #38)
- **2026 Subaxia GT Men's standard-width color**: described as "Dark Gray" but Yonex USA sometimes labels "Dark Gray" and "Dark Green" interchangeably — verify per SKU before publishing
- **JPY MSRP**: ~19,000 and ~22,000 estimated based on USD:JPY ~140 conversion + Yonex's typical 1.1-1.3x markup vs USD; NOT verified from yonex.co.jp directly