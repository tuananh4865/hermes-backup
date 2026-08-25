---
title: TikTok Shop Product Research — Structured Data for Script Writing
name: tiktok-shop-product-research
created: 2026-07-16
updated: 2026-07-20
type: skill
tags: [research, ecommerce, tiktok, shopee, product, script-writing, affiliate, url-resolution, captcha, waf]
description: Research 1-N specific products for TikTok Shop / Shopee / e-commerce affiliate script writing. Returns JSON with brand, origin, specs, VN retail price, USP, competitors, user reviews, and at least 1 real citation URL per product. Also covers vt.tiktok.com short-URL batch resolution and SlardarWAF captcha pitfall.
trigger: User asks for product research with specs + price + competitors + citations for any e-commerce/TikTok Shop script OR hands a list of vt.tiktok.com share URLs to fetch metadata from
version: 0.7.0
changelog:
  - 2026-07-16 v0.1.0 Initial skill with 11-product example
  - 2026-07-16 v0.2.0 Add batch 4-subagent pattern (12 products) + brand-name assumption pitfall + reference scaling
  - 2026-07-17 v0.3.0 Add vt.tiktok.com URL-resolution path (og_info in redirect), SlardarWAF captcha pitfall + recognition + fallback ladder, scripts/resolve_vt_urls.sh, references/vt-tiktok-url-resolution-2026-07-17.md
  - 2026-07-17 v0.4.0 Add wiki-cache audit workflow. References wiki-cache-audit-pattern-2026-07-17.md
  - 2026-07-17 v0.4.0 Add image URL extraction from og_info + retailer-mirror fallback (dodoto.vn, armafvietnam.vn, ftpshop.com.vn, mho.vn, xnthoiding.vn, g00jodoqglobal.com, kentfaith.com, dji-vietnam.vn faster than Kalodata/Minea). End-to-end 14-product batch in 5 min. References vt-tiktok-batch-2026-07-17-run-report.md
  - 2026-07-20 v0.5.0 Add mix-batch dispatch pattern - NEW + VERIFY-EXISTING split when wiki has K of N URLs cached. 4 subagents in parallel, clean reports in under 10 min
  - 2026-07-20 v0.6.0 Add FastMoss mirror recipe - Step D for view/product/ID URLs that bypass SlardarWAF. 4/4 products verified via FastMoss SEO metadata + exa fetch_exa. Search snippet fallback for price + sold_count from shop.tiktok.com meta tags
  - 2026-07-20 v0.7.0 Add Verify-Existing-Wiki Pattern - 4-step recipe for verify N existing wiki files against new URLs - read existing file FIRST, classify diff as MATCH MINOR MAJOR WRONG_PRODUCT, append footer not replace frontmatter, return WAS NOW summary. Plus pitfall skip subagents for N at most 4
---

# TikTok Shop Product Research

> Research 1-N specific products for TikTok Shop / Shopee VN / e-commerce affiliate script writing. Returns structured JSON with brand, origin, specs, VN retail price, USP, competitors, user reviews, and at least 1 real citation URL per product.

## When to Use This Skill

Anh asks:
- "research sản phẩm X / Y / Z cho TikTok"
- "tìm data chính xác về [brand] [model]"
- "đối thủ của [product] là gì"
- "viết script TikTok Shop cho [category]"
- "giá VN của [product] + specs + đánh giá"

**This is NOT:**
- YouTube trending video research (use `youtube-trending-research`)
- TikTok algorithm/social trends research (use `social-media-trends`)
- Generic web research (use `deep-research-multi-pillar` for multi-domain)

## Output Schema (REQUIRED)

Every product MUST include these fields. Do NOT omit any.

```json
{
  "name": "ARMAF Odyssey Mega Body Spray 200ml",
  "brand": "ARMAF",
  "origin": "UAE (Dubai) – Sterling Parfums Industries LLC, 1999",
  "specs": {
    "volume": "200ml",
    "type": "Perfumed Body Spray",
    "longevity": "3-6h",
    // ... product-specific keys
  },
  "price_vnd": 239000,
  "price_note": "Chính hãng armafvietnam.vn: 239k-400k tuỳ mùi; classic.vn ~199k",
  "usp": "Giá rẻ 1/10 so với nước hoa chính hãng; 200ml dùng cả tháng; 19+ phiên bản unisex",
  "competitors": ["Bath & Body Works Body Mist", "Victoria's Secret Body Mist", "..."],
  "user_reviews": "Fragrantica 2026: '70% giống Tom Ford Noir Extreme, $40 cho 200ml = good value'",
  "citations": [
    "https://armafvietnam.vn/products/xit-thom-toan-than-nam-armaf-odyssey-mega-200ml",
    "https://armaf.com/products/odyssey-mega-body-spray"
  ]
}
```

**Group wrapper**:
```json
{
  "research_date": "YYYY-MM-DD",
  "groups": [
    { "group": "Body Mist", "products": [...] }
  ],
  "summary_insights": ["..."],
  "limitations": ["..."]
}
```

## Research Flow

### Step 1: Identify OEM vs Branded Status FIRST

Before searching, classify each product by likelihood:
- **Known brand with website** (Armaf, Ulanzi, GOOJODOQ, Apple): search brand.com first → then VN distributor
- **OEM/private label** (AMAP, AMF, Goldjordock): NO brand website exists. Use Alibaba/1688 wholesale + Shopee listings. Note explicitly in `limitations`.
- **Descriptor not brand** ("Lemony", "body mist cho nữ"): search by descriptor across known brands (Lush, Naturalium, BodyX, Puresense).

**Pitfall**: Don't fabricate a brand origin for OEM products. State "OEM Trung Quốc, dropship Shopee VN" and link the listing.

### Step 2: Batch Parallel Searches (5-8 per turn)

Run ALL these in ONE assistant turn per group:

```
Set A — Brand official site:
- "{brand}" official site
- "{brand}" "{model}" specifications

Set B — Vietnamese retailer (price):
- "{brand}" "{model}" giá shopee.vn
- "{brand}" "{model}" armafvietnam.vn OR classic.vn OR dienmayxanh.com

Set C — Reviews & comparisons:
- "{brand}" "{model}" review fragrantica OR rtings OR tomsguide
- "{brand}" vs "{competitor}" 2026

Set D — OEM detection (for unknown brands):
- "{brand}" Alibaba OEM
- "{brand}" 1688 wholesale

Set E — User-generated reviews:
- "{brand}" "{model}" reddit review 2026
- TikTok "{brand}" "{model}" review
```

### Step 3: Targeted Fetch for Specs

After search, use `mcp__exa__web_fetch_exa` on the BEST URLs to extract:
- Brand official product page → exact specs, weight, dimensions
- VN retailer (armafvietnam.vn, classic.vn, annguy.vn, huylinh.net, kingcom.com.vn) → VN price
- Review sites (fragrantica.com, rtings.com, amazon.com) → user reviews

**Critical**: `web_extract` defaults to DuckDuckGo which is search-only. USE `mcp__exa__web_fetch_exa` for extraction.

### Step 4: Specs in English, Description in Vietnamese

- `specs` object: English keys + English values (universal)
- `usp`, `competitors`, `user_reviews`, `price_note`: Vietnamese for Anh's audience
- `citations`: URLs unchanged (English URLs fine)

### Step 5: Minimum Citation Standard

- Each product: ≥1 citation URL, ideally 2-3
- Prefer: brand.com > VN authorized retailer > Shopee/Lazada listing > review site > Reddit/TikTok
- For OEM products: cite the Alibaba/Shopee listing that establishes price + origin

### Step 6: Document Limitations

In `limitations` array, explicitly state:
- OEM products without brand website
- Models with multiple OEM variants (Gojodot 0700 = GOOJODOQ CD3293)
- Price volatility on TikTok Shop (±20-30%)
- Failed searches or unavailable sources

## Tool Priority

1. **mcp__exa__web_search_exa** (PRIMARY): batch parallel searches, returns rich snippets with prices/specs inline
2. **mcp__exa__web_fetch_exa** (PRIMARY for extraction): clean markdown from known URLs
3. **mcp__exa__web_search_advanced_exa** (when needing filters): domain filter, date range, category filter
4. **mcp__MiniMax__web_search**: fallback if Exa fails
5. **web_search** (DDG): LAST RESORT, often returns irrelevant data
6. **web_extract**: NEVER (search-only backend error)

**Pitfall**: `web_extract` via default DuckDuckGo backend returns `{"success": false, "error": "DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content. Set web.extract_backend to firecrawl, tavily, exa, or parallel."}`. Always use Exa MCP for both search AND fetch.

## Niche-Specific Knowledge

### Body Mist / Perfume
- ARMAF Odyssey = 19+ scents, 200ml body spray (Mega, Aqua, Homme, Mandarin Sky, Limoni, Spectra, Candee, Tyrant, Aoud, Marshmallow, Soda Pop, Toffee Coffee, Go Mango, Eau de Montagne, Black Forest, Revolution, Wild One, Artisto)
- ARMAF VN official: armafvietnam.vn (Sterling Parfums UAE, 1999 by Hassan Naeem)
- AMAP/AMF = OEM private label, $0.40-1.50 wholesale, 89-150k VN retail
- "Lemony" is NOT a brand — descriptor for Lush Flutter, Naturalium, BodyX, Puresense
- VN price reference: armafvietnam.vn / classic.vn / annguy.vn

### Tripod / Ulanzi
- Brand: Shenzhen Ulanzi Technology, China
- Uka Quick Release ecosystem + Arca-Swiss compatibility
- Flagship: MA66 (75g, $24.99 US) for DJI Pocket 3/4
- VN reference: huylinh.net, kingcom.com.vn, nhatnguyencamera.com, icamera.vn, newlite.vn, thietbiquayphim.com
- DJI Pocket 3 accessories: PM-01 (magnetic), PK-06 (expansion), PK-08 (auto fold), MA66 (tripod), LM18 (LED), CK01 (clip)

### iPad Stylus
- **GOOJODOQ = Gojodot** (Vietnamese transliteration) = OEM Trung Quốc lớn nhất
- Model code: CD32xx = base series, GD12/GD13 = premium, GD13 Pro = wireless charging gen mới nhất
- Apple Pencil dupe phổ biến nhất: 199k base, 400-549k wireless
- KenKE, Zspeed, Ankace là đối thủ cùng phân khúc
- "Goldjordock" = OEM không có website, dropship Shopee, 99-199k

## Output File Convention

Save to: `~/tiktok_product_research_{YYYY-MM-DD}.json` (root home, simple)

Format: pretty-printed JSON, bilingual (English specs, Vietnamese descriptions), valid JSON (parseable).

## Common Pitfalls

- **Don't confuse AMAP/AMF with ARMAF** — different brands, both UAE/Middle East but ARMAF = Sterling Parfums (founded 1999, premium), AMAP/AMF = OEM/private label, no official brand site
- **Don't fabricate specs** for OEM products without listing — state "OEM, specs tương đương GOOJODOQ CD3293"
- **Don't trust single source** for VN price — cross-check 2-3 retailers (armafvietnam.vn + classic.vn + Shopee)
- **Don't forget the limitations array** — be honest about OEM/unknown sources
- **Don't write 19+ scent names from memory** — fetch the actual armaf.com/armaf.uk product listing
- **Don't miss the "không phải brand" cases** — Lemony, Goldjordock, "Gojodot 0700" all need disambiguation upfront

## URL-Resolution + Captcha Pitfalls (NEW v0.3.0, from 2026-07-17 vt.tiktok.com batch)

User sometimes hands you a list of `vt.tiktok.com/XXXXX/` short URLs (TikTok app share links, copy-pasted from chat). Do NOT try to fetch them directly — follow this path:

### Step A — Resolve short URL → product ID + title from redirect (FREE, no captcha)

```bash
curl -sL -o /dev/null -w '%{url_effective}' \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  --max-redirs 5 "https://vt.tiktok.com/XXXXX/"
```

The 301-redirect URL itself contains **three free data points** embedded by TikTok's share-link server:

1. **`/view/product/{product_id}`** path → the canonical product ID (digits, 19 chars typically)
2. **`og_info` query param** → URL-encoded JSON with `title` and `image`. Decode with `urllib.parse.unquote_plus`.
3. **`image` URL inside `og_info`** → the product thumbnail hosted on TikTok's CDN (`p16-oec-sg.ibyteimg.com`, `tos-alisg-i-aphluv4xwc-sg.ibyteimg.com`, or `tos-maliva-i-o3syd03w52-us.ibyteimg.com`). Useful for visual reference / downstream scripts that want to embed thumbnails.

This gets you product name + thumbnail URL + product ID without ever hitting the WAF. **This is the single highest-leverage step in the whole skill — always run it first**, even for "name only" lookups.

### Step B — Recognize the captcha block FAST

`https://www.tiktok.com/view/product/{id}` and `https://shop.tiktok.com/vn/pdp/{id}` are both **protected by SlardarWAF** (Arkose Labs / `slardar-sdk-web`) which presents an interactive **puzzle-piece captcha** ("Drag the puzzle piece into place"). Hallmarks:

- HTML response ≈ 5-6 KB with `<title>Security Check</title>`
- Empty `<body>` until JS solves it
- `captcha/index.js` + `client-api.arkoselabs.com` in CSP
- Page `<head>` contains `<script id="slardar-config" type="application/json">` block

**What does NOT bypass it** (verified 2026-07-17):
- Changing `User-Agent` (mobile, desktop, TikTok app signature) — same WAF hit
- `web_extract` (DDG backend — also blocked)
- `mcp__exa__web_fetch_exa` — same payload, captcha
- `browser_navigate` from a non-residential IP — captcha puzzle renders, cannot be solved by subagent

**Recognize the block in 1 curl probe, then STOP** trying server-side variants. Pivoting to redirect metadata (Step A) gets you more data in 30s than 30 minutes of UA gymnastics.

### Step C — Captcha fallback ladder

If Step A doesn't give enough (you still need price / sold_count / rating / description), try in order:

1. **VN retailer mirror search** (RECOMMENDED before aggregators) — `mcp__exa__web_search_exa` with `"\"{brand}\" \"{model}\" site:{mirror}"` against the mirrors below. These are **faster and more accurate than aggregators** for Vietnam retail price because they're the actual store-front pages — no scraping delay.
   - **Brand official VN store** (best if exists): `armafvietnam.vn`, `goojodoqglobal.com` (vn subdomain), `dji-vietnam.vn`, `dodoto.vn`
   - **Authorized VN retailer**: `ftpshop.com.vn`, `mho.vn`, `xn--inthoiding-ukbi4949gcpa5i.vn` (điện thoại di động mirror), `imax.com.vn`, `huylinh.net`, `kingcom.com.vn`, `nhatnguyencamera.com`
   - **Shopee/Lazada listings surfaced via meta-search** — Shopee VN `shopee.vn`, Lazada VN `lazada.vn`, Tiki `tiki.vn`. Often show `Kho: X` (inventory count = proxy for sale volume), `d: XXXX` (a popularity/sold score), and historical price from product description.
   - **Brand-direct (non-VN)**: `kentfaith.com` (K&F Concept), `kfconcept.com`, `amazon.{ca,com}` (rating + sold), `bhphotovideo.com`, `adorama.com` (price reference for premium imported)
   - **Single brand-search pattern** that worked 13/14 times in the 2026-07-17 batch: `"{brand in og_info title}" "giá shopee.vn"` or `"\"{product name fragment}\" \"{price unit}"` — returns the matching VN listing at the top of results.
2. **Search aggregator** — `mcp__exa__web_search_exa` with `"tiktok shop {product_id}"` or `"tiktok shop \"{title}\""` → often surfaces cached Kalodata / Minea / FastMoss / Shoplus pages that already extracted the data. Use only when retailer mirrors don't surface — adds 1-2 days of latency vs the live store.
3. **Seller-affiliate storefront** — some products have a public seller storefront at `shop.tiktok.com/@seller` that's less aggressive.
4. **User-supplied cookies** — if user has a logged-in TikTok Shop session, capture cookies via `computer_use` and pass via curl `-b`. WAF treats logged-in users differently.
5. **Headful + manual solve** — `computer_use` can drive cua-driver; user solves the puzzle in the real browser, then provide the resulting `tt_chain_token` cookie.
6. **For price data: ask user** — paste the page, type in price, screenshot. Slower than automation but always works.

### Output when captcha blocks TikTok Shop but retailer mirror is found

In practice (verified 2026-07-17, 13/14 products succeeded), Step A + Step C step 1 gets you a populated `name`, `brand`, `price`, `specs` — even though the TikTok Shop PDP itself was never rendered. Return JSON shaped like:

```json
{
  "url": "https://vt.tiktok.com/XXXX/",
  "short_code": "XXXX",
  "product_id": "1731219286255831683",
  "product_name": "<decoded og_info title>",
  "brand": "<inferred>",
  "price_sale": "49000 VND",
  "specs": "<from mirror listing>",
  "image_thumbnail": "<og_info image url>",
  "sold_count": null,                // TikTok-only — unobtainable
  "rating": null,                    // TikTok-only — unobtainable
  "fetched_ok": true,                // mirrors fetched successfully
  "source": ["vt.tiktok.com redirect", "https://ftpshop.com.vn/.../hulako-..."],
  "limitations": ["TikTok Shop SlardarWAF captcha blocks direct PDP fetch; price + specs sourced from VN retailer mirror (ftp/mho/xnthoiding); sold_count and rating unavailable"]
}
```

**Truthful `fetched_ok` semantics**: set `true` when ANY reliable source returned data, even if TikTok Shop itself wasn't reachable. The flag means "structured fields populated from citations" — not "TikTok Shop PDP rendered". Mark the actual source under `source` and the gap under `limitations`.

**Do NOT silently fabricate price/sold_count.** Honesty here is a first-class feature — see brand-name assumption pitfall below.

### Pitfall — Don't confuse vt.tiktok.com share metadata with truth

The share-link `og_info` title is set by the **shopper who shared the link** at share time, not by the merchant. It can be:
- Truncated (especially in `+` URL-encoded form, decoded titles may end mid-phrase)
- Stale (product may have been renamed)
- Spammy ("chính hãng giá rẻ ..." patterns injected by affiliate tools)

Treat it as `name_hint`, verify against the live PDP when reachable. Mark inferred brands as `inferred_from_title: true` in `specs` so downstream scripts know not to trust it absolutely.

### Step D — FastMoss as canonical TikTok Shop mirror (NEW v0.6.0, from 2026-07-20 wiki-verify session)

When user provides a direct TikTok Shop URL like `https://www.tiktok.com/view/product/{id}` (NOT a vt.tiktok.com share link, but a `view/product/...` URL), Step A doesn't apply — there's no redirect to mine. BUT the same SlardarWAF captcha blocks direct fetch. The trick is to surface the same data via FastMoss analytics, which mirrors TikTok Shop product metadata.

**Pattern (verified 2026-07-20, 4/4 products verified end-to-end):**

1. Search for the product ID as text. **Both backends can surface FastMoss analytics pages** when you put the 19-digit product ID in the query:
   ```python
   mcp_MiniMax_web_search('"1731429094953026900" Dodoto Lux Air')
   # → top result: fastmoss.com/id/e-commerce/detail/1731429094953026900
   mcp_MiniMax_web_search('"1732329120649414265" GOOJODOQ')
   # → fastmoss.com/vi/e-commerce/detail/1732329120649414265
   ```

2. Fetch the FastMoss page with `mcp__exa__web_fetch_exa`. It returns the TikTok Shop title verbatim in the page H1/SEO fields. Example:
   ```
   https://www.fastmoss.com/vi/e-commerce/detail/1732329120649414265
   → H1 = "【GOOJODOQ*KOL/KOC】Đế điện thoại có thể gập, có thể xoay 360° và nghiêng 180°, chất liệu bằng thép carbon, nhỏ gọn & nhẹ"
   ```
   Note: FastMoss page body is mostly analytics widgets (skeleton loaders), but the SEO metadata + H1 is rendered server-side and survives exa's text extraction.

3. Cross-reference the title against the user-provided URL's expected product. If the title doesn't match (different brand, different specs), flag explicitly — the user may have mis-shared the URL.

4. For price + sold_count, FastMoss analytics pages don't expose these in the rendered HTML. Fall back to `shop.tiktok.com/vn/pdp/{slug-title-encoded}/{id}` SEO snippets from search results — TikTok surfaces price + sold in meta tags even when direct fetch is captcha'd:
   ```python
   mcp_MiniMax_web_search('site:shop.tiktok.com "1731153273118557817"')
   # → meta description contains: "Pin 4000mAh & 5000mAh ... ₫96.029 ₫199.000 (giảm 52%)"
   ```

**Why this matters:** It is the only end-to-end path that verifies TikTok Shop title + price without user-supplied cookies or manual captcha solve. 4/4 products verified in the 2026-07-20 session. Pre-requisite: you have the 19-digit product ID (which `vt.tiktok.com` redirects expose, or user gives you directly).

### Step E — CLI script for batch resolution

See `scripts/resolve_vt_urls.sh` for a one-liner that takes a file of `vt.tiktok.com` URLs (one per line) and outputs `short_code|product_id|decoded_title` tuples. Use this when user hands you N>3 URLs — saves manual piping.

## Batch Pattern for 12+ Products (NEW v0.2.0, from 2026-07-16 12-batch)

When user asks for 12+ products across 4+ categories, dispatch **4 subagents in parallel via `delegate_task`** (3 products/subagent = sweet spot). Each subagent writes to `/Users/tuananh4865/research_<scope>.json` (NOT return inline — JSON too large).

**Pattern** (verified 12 products / 4 subagents / 6 min / 170+ citations):
1. Read `os.listdir('/Volumes/Storage-1/Pocket3/Hermes-Edit/')` → extract distinct product slugs from filenames
2. Group by category (4 groups: body mist + tripod / sạc + giá đỡ / ốp + K&F / niche items)
3. Dispatch 4 subagents parallel, each with: 3 product names + JSON schema + "≥1 citation URL mandatory" + tools list
4. Wait for fan-out (each subagent ~5-7 min)
5. Read JSON files from disk, import each product as 1 file (not 1 file per category) into `wiki/projects/<project>/products/`
6. Embed summary table in Telegram reply (name + brand + price + citation count per group)

## Brand-Name Assumption Pitfall (NEW v0.2.0, from 2026-07-16)

**4 cases caught in 1 batch** where user's mental brand name was wrong:
- **"Kea Concept" ốp Pocket 3** → typo/nhầm với **K&F Concept** (Top 1 filter brand TG)
- **"Lemony" body mist** → KHÔNG phải brand, là descriptor (Lush Flutter / Naturalium / BodyX / Puresense)
- **"PocketBar" bộ vệ sinh** → KHÔNG phải brand Trung Quốc, thật ra là mini crowbar Solea Stockholm (Thụy Điển)
- **"AMAP" / "AMF" body mist** → OEM private label, không phải ARMAF

**Rule**: When subagent returns "brand X not found", DON'T silently invent a replacement. **Report the discrepancy to user** with evidence (searches tried, no official site found). User may have typo'd or mis-remembered. Honest reporting preserves trust — fake brand data breaks scripts.

## Pitfalls

- **Don't confuse AMAP/AMF with ARMAF** — different brands, both UAE/Middle East but ARMAF = Sterling Parfums (founded 1999, premium), AMAP/AMF = OEM/private label, no official brand site
- **Don't fabricate specs** for OEM products without listing — state "OEM, specs tương đương GOOJODOQ CD3293"
- **Don't trust single source** for VN price — cross-check 2-3 retailers (armafvietnam.vn + classic.vn + Shopee)
- **Don't forget the limitations array** — be honest about OEM/unknown sources
- **Don't write 19+ scent names from memory** — fetch the actual armaf.com/armaf.uk product listing
- **Don't miss the "không phải brand" cases** — Lemony, Goldjordock, "Gojodot 0700" all need disambiguation upfront

## Wiki-Cache Audit + Mix-Batch Pattern (NEW v0.5.0, from 2026-07-20 audit session)

When user hands you N URLs but wiki already has K of them cached (K < N), do NOT dispatch N parallel subagents. Split into 2 branches in a single `delegate_task(tasks=[...])`:

1. **NEW branch** (N-K products) — full research + write new wiki file. Dispatch 1 subagent per product or 1 subagent per 2-3 small products.
2. **VERIFY-EXISTING branch** (K products) — read existing wiki file + compare against new URL data + flag only diffs (no overwrite). Dispatch 1 subagent per 2-4 files (more efficient than 1-per-file because context is shared).

**Why split:**
- NEW tasks need independent research context (web search + fetch)
- VERIFY tasks need ACCESS to existing wiki frontmatter + body — give them the existing file paths
- Mixing → each subagent's context includes BOTH irrelevant research paths AND irrelevant wiki paths → context bloat → reads slower + more chance of hallucinating mismatches

**Dispatch template:**
```python
delegate_task(tasks=[
    {"goal": "NEW: write 4 files for PID 1731xxx/1733xxx/1734xxx", "context": "All PIDs + URLs + format template path"},
    {"goal": "VERIFY existing 3 files vs PID 1734xxx/1735xxx/1735xxx", "context": "Existing wiki paths + URLs + report format"},
    {"goal": "VERIFY existing 4 files vs PID 1731xxx/1732xxx/1732xxx/1731xxx", "context": "Existing wiki paths + URLs + report format"},
])
```

**Max 3 concurrent subagents per group** (Hermes `max_concurrent_children=3`). If N > 9 with mixed branches, batch sequentially (3 NEW, wait, 3 VERIFY, wait, ...).

**Verified 2026-07-20, 14 URLs split 4-NEW + 3-VERIFY + 4-VERIFY + 2-VERIFY.** All subagents returned in <10 min with clean structured reports.

## Wiki-Cache Audit Workflow (NEW v0.4.0, from 2026-07-17 audit session)

When the user (or a parent agent) says "audit wiki products vs N URLs" or "compare the recent batch against wiki cache", the N URLs may live ONLY in the parent agent's session memory — they may not be in scope for the subagent. **Reverse-engineer** the batch by scanning the scratch JSON files at `~/`.

### Step 1 — Find the source batch on disk

```bash
ls -la /Users/tuananh4865/*.json | grep -E "tiktok|shop"
# Common filenames: tiktok_product_research_*.json, tiktok_shop_groups_*.json, research_tiktok_groups_*.json
```

When multiple JSONs exist, pick the one whose `research_date` is closest to today AND whose flattened product count matches the user's claimed N. The match is rarely exact — `groups[*].products[*].count == N` wins over `research_date` recency.

### Step 2 — Flatten the JSON into a single product list

Read the JSON, walk `groups[*].products[*]` for every group, output: `{name, brand, price_vnd, citation_count}` per item. This is the ground-truth N for the audit.

### Step 3 — Match to `wiki/projects/<project>/products/`

```bash
# Use search_files (NEVER ls) to enumerate wiki products
search_files target=files path="/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products" pattern="*.md"
```

For each JSON product, find the matching wiki file by brand slug + product descriptor in filename (e.g. `bath-body-works-*`, `ulanzi-ma66-*`, `sapital-lemony-*`, `goojodoq-0700-*`).

### Step 4 — Extract citation count from frontmatter

Every wiki product file has frontmatter `sources: N` (= total citation links at the bottom). Use `grep -E "sources:|^price_vnd|^brand|^origin" file.md` to extract quickly.

### Step 5 — Produce audit table

Columns: `# · product_name · brand · wiki_file · has_citation · citation_count · price_vnd · recommendation`.

**Recommendation rule**: products with `sources: < 3` need a top-up fetch to reach the wiki minimum standard. Cite top categories with no wiki coverage as `gap: needs new research`.

### Pitfall — Don't trust user's claimed N blindly

The 2026-07-17 audit session said "14 URLs" → found 11 in JSON-1, 11 in JSON-2, **14 in JSON-3** → JSON-3 wins (exact count match). If no JSON matches, surface the discrepancy instead of forcing a fit. The actual N is whatever's on disk, not what's claimed.

### Pitfall — Don't re-research products that already have wiki cache

If `wiki/products/{slug}.md` exists with `status: researched` and `confidence: high`, skip new research. Only patch if `sources: < 3` OR frontmatter `updated` is more than 30 days old.

## Verify-Existing-Wiki Pattern (NEW v0.7.0, from 2026-07-20 audit session)

When user gives you N URLs and says "verify these against the existing wiki files" (e.g. "Verify và update 4 file wiki cache cũ"), the workflow is DIFFERENT from full research. Do this:

### Step 1 — Read each existing wiki file FIRST

Don't blindly trust frontmatter or titles — read the full file. The brand may have been wrong, the price may be stale, the model may have changed. Especially:
- **Filename** is often the longest signal — contains slug, brand variants, OEM hypotheses
- **Frontmatter `brand:` field** is the most likely to be wrong (typos from task brief get encoded as "Goldjordock" when real brand is GOOJODOQ)
- **Body specs** may contradict the TikTok Shop title entirely (e.g. wiki says "ABS plastic, height-adjustable 26.3-36.3cm" but TikTok Shop says "thép carbon, foldable, 180° tilt")

### Step 2 — Per file, decide diff category

For each (existing file, new URL) pair, classify:

| Diff category | Action |
|---|---|
| `MATCH` — wiki specs match TikTok Shop title exactly | NO update needed (only add TikTok Shop citation if missing) |
| `MINOR_DIFF` — price off by <10%, color/edge-case specs differ | Update specific fields, append `Updated:` footer |
| `MAJOR_DIFF` — brand, material, or core spec differs | Rewrite affected sections, document the discrepancy in frontmatter `note:` field |
| `WRONG_PRODUCT` — wiki describes different SKU than TikTok Shop URL | Major rewrite + flag in frontmatter + add `tiktok_shop_id` to disambiguate from old source |

Verified 2026-07-20 batch (4 files):
- Dodoto Lux Air V3: `MINOR_DIFF` (price 495k → 498,999)
- GOOJODOQ BD3035: `WRONG_PRODUCT` (wiki was for BD3035 boom-stand ABS plastic; TikTok Shop is carbon-steel foldable stand — different SKU, same brand)
- GOOJODOQ AD4031/4023 power bank: `MINOR_DIFF` + ADD (TikTok Shop price 96,029 + new "Chip AI tích hợp" spec)
- Goldjordock stylus: `MAJOR_DIFF` (brand Goldjordock → GOOJODOQ; price 150k → 498,820; charging Type-C → magnetic + USB-C; this was the user-provided brand hypothesis being wrong per Pitfall #16)

### Step 3 — Append footer, don't replace frontmatter

Standard footer pattern (DO append, don't lose original "Research auto-generated" line):
```markdown
---
*Research auto-generated by subagent với citation verification.*

Updated: 2026-07-20 — verified against TikTok Shop (product {ID}). [DIFF_CATEGORY]: [what changed].
```

This preserves the original research timestamp + adds the verification trail. If user later audits, they see both dates.

### Step 4 — Return WAS: / NOW: summary, NOT just "done"

Anh specifically requested this format on 2026-07-20:
```
1. file_path.md
   - WAS: {old_value}
   - NOW: {new_value}
2. file_path.md
   - NO CHANGE
3. ...
```

Per-file `WAS:` / `NOW:` lines (or `NO CHANGE`) make the audit visible in chat without forcing anh to open each file. Always include this summary at the END of the response, even if intermediate patches succeeded.

### Pitfall — Don't dispatch subagents for small N (≤4)

The 2026-07-20 audit was N=4 — I did it directly in the parent session because:
- 4 wiki files fit in one `read_file` × 4 + 4 × `patch` round
- Search results returned cleanly per product
- No risk of subagent context drift on a small task

Reserve subagent dispatch for N ≥ 8 OR when research requires 3+ queries per product. For N ≤ 4 verify-existing, do it inline.

## Support Files

- `references/example-3-category-research-2026-07-16.md` — Worked example: 11 products across 3 categories with citation patterns, time budget, and reusable niche knowledge (VN price reference points for body mist, Ulanzi ecosystem, iPad stylus)
- `references/vt-tiktok-url-resolution-2026-07-17.md` — Session report: how the first 14-product vt.tiktok.com batch was resolved via og_info + why the captcha blocked full fetches. Includes the exact redirect URL pattern, the recognized SlardarWAF HTML signatures, and the JSON shape used for `fetched_ok: false` rows.
- `references/vt-tiktok-batch-2026-07-17-run-report.md` — Follow-up session report: same 14 URLs, this time captcha + Step C retailer-mirror fallback worked end-to-end in ~5 min for 13/14 products. Documents the working mirror list (ftpshop/mho/xnthoiding/dodoto.vn/armafvietnam.vn/goojodoqglobal.com/kentfaith.com/dji-vietnam.vn), the actual output JSON that was committed to disk, and the gap (sold_count unobtainable from mirrors).
- `references/delivery-report-pattern-2026-07-20.md` — **NEW** Multi-file batch delivery must show concrete outputs separately (files vừa tạo mới + files đã verify cập nhật) FIRST, summary table LAST. Real case 20/07/2026: user hỏi "Chưa thấy sp này" cho PID 1733974507990517546 (file đã được subagent tạo). Rule vĩnh viễn: enumerate absolute file paths with 1-line description per file BEFORE the status table.
- `templates/product-research-template.json` — Copy-and-modify JSON skeleton with all required fields pre-populated
- `scripts/resolve_vt_urls.sh` — Batch CLI: takes a file of vt.tiktok.com URLs (one per line) and outputs `short_code|product_id|decoded_title` tuples via 301-redirect metadata extraction. 30s for 14 URLs on a residential proxy.

## Related Skills

- `youtube-trending-research` — YouTube video research for product niches (overlapping territory, different output)
- `tiktok-viral-script` — Write TikTok sales script from product info (this skill feeds into it)
- `deep-research-multi-pillar` — Multi-domain research synthesis (broader scope)
- `evidence-gate` — Enforce 5-evidence rule before claiming JSON file is saved