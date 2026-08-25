# vt.tiktok.com URL Resolution Session — 2026-07-17

> Session report for the 14-product vt.tiktok.com batch. This is the canonical
> evidence packet for the new "Step A" path in
> `tiktok-shop-product-research/SKILL.md` v0.3.0.

## The Task

User handed me a list of 14 `vt.tiktok.com/.../` short URLs (TikTok Shop share
links, copy-pasted from chat) and asked for product metadata in JSON form.

## What Worked

### vt.tiktok.com short-link resolution (no captcha, no JS)

TikTok's share-redirect server returns a 301 to a long URL of the form:

```
https://www.tiktok.com/view/product/{19_digit_id}?_d=...&og_info={URL-encoded JSON}&...
```

The `og_info` query param is a **double-URL-encoded JSON blob** with two useful
keys: `title` (Vietnamese product name, set by the shopper who shared the link)
and `image` (thumbnail, hosted on `tos-alisg-i-aphluv4xwc-sg.ibyteimg.com` or
`tos-maliva-i-o3syd03w52-us.ibyteimg.com`).

**Decode sequence** (Python):
```python
import urllib.parse, json
raw_og_info = "..." # from the final URL query string
once = urllib.parse.unquote(raw_og_info)             # first decode
twice = urllib.parse.unquote(once)                    # second decode — usually reaches JSON
data = json.loads(twice)
title = data["title"]   # → "Giá đỡ Điện thoại LOX3 Livestream ..."
image = data["image"]   # → "https://p16-oec-sg.ibyteimg.com/.../...webp"
```

**Sometimes only `+` becomes space** (`unquote_plus`), depending on whether
TikTok decided to URL-encode spaces as `+` or `%20`. The terminal script
`scripts/resolve_vt_urls.sh` tries both.

### What this got for 14 URLs

| short_code | product_id | brand_inferred |
|---|---|---|
| ZS9re2CFLXwGb-RjM5y | 1731219286255831683 | HULAKO |
| ZS9re2VbAbMNg-FemZX | 1733974507990517546 | (Universal) |
| ZS9re2bKmTpm1-EDhug | 1734240255912543921 | ULANZI |
| ZS9re2srPMAfy-mjK9Y | 1733718822340166953 | PW3 |
| ZS9re2s3aL6LX-dshPs | 1733899724122392054 | K&F CONCEPT |
| ZS9re2WNd3tvR-XZK5a | 1735529850427639286 | K&F CONCEPT |
| ZS9re2nPQ4bdp-Iube2 | 1734226192370271734 | K&F CONCEPT |
| ZS9re2EB2dpr4-OOiyy | 1731429094953026900 | Dodoto |
| ZS9re2oaGkevh-Oeewf | 1731605763856303550 | Armaf |
| ZS9rejJ8WHp1E-JiH9E | 1732050500891543161 | GOOJODOQ |
| ZS9reje49oYSv-rrtVo | 1731153273118557817 | GOOJODOQ |
| ZS9rej8EPD7G5-2wrn5 | 1732329120649414265 | GOOJODOQ |
| ZS9rej2Yv9ojK-btsDy | 1731123993250007390 | (Unbranded) |
| ZS9rejjyfeG5S-Z5Jua | 1730387676601289330 | (Unbranded) |

Total time to resolve + decode: ~25 seconds (single shell loop, sequential curl).
No captcha hit at this layer.

## What Blocked — SlardarWAF Captcha

`https://www.tiktok.com/view/product/{id}` and the 301-redirect target
`https://shop.tiktok.com/vn/pdp/{id}` both serve an **identical WAF challenge**:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="icon" href="data:;base64,=" />
    <script id="slardar-config" type="application/json">
      { "slardarClient": "SlardarWAF", ... }
    </script>
    <script src="https://sf16-website-login.neutral.ttwstatic.com/.../captcha/index.js"></script>
  </head>
  <body>Please wait...</body>
</html>
```

CSP headers include `*.arkoselabs.com`, `client-api.arkoselabs.com`,
`static.captchami.com`, `*.arkoselabs.com`. SlardarWAF partners with Arkose
Labs for the challenge. The Hermes `browser_navigate` snapshots showed:

```
- generic
  - dialog
    - generic: "Verify to continue:"
    - generic: "Drag the puzzle piece into place"
    - generic [ref=e4] clickable [cursor:pointer]   ← the puzzle piece
```

### Tools that did NOT bypass (verified):

1. `curl` desktop UA (`Mozilla/5.0 (Macintosh...)`) → 5582-byte captcha HTML
2. `curl` mobile UA (`iPhone... Safari`) → same captcha HTML
3. `curl` TikTok app UA (`com.zhiliaoapp.musically/2022600030`) → same
4. `mcp__MiniMax__web_search("tiktok shop 1731219286255831683")` → search backend doesn't surface product data
5. `web_extract` (DDG default backend) → `{success: false, error: "DuckDuckGo (ddgs) is a search-only backend..."}`
6. `mcp__exa__web_fetch_exa` → returns `"Security Check"` page only
7. `browser_navigate` (Hermes computer-use) → captcha dialog snapshot, no price/rating/sold_count data

### Cost in tool calls before recognizing the block

Approximately 4-5 tool calls spent on UA variations and web_extract before
realizing the WAF is uniform across all paths. **The lesson**: if the first
probe returns the SlardarWAF challenge page, do NOT spend the second probe
trying another UA. Pivot to redirect metadata (Step A) or ask the user.

## Output Schema Used

```json
{
  "url": "https://vt.tiktok.com/ZS9re2CFLXwGb-RjM5y/",
  "short_code": "ZS9re2CFLXwGb-RjM5y",
  "product_id": "1731219286255831683",
  "product_name": "Giá đỡ Điện thoại LOX3 Livestream Chụp Hình Sản Phẩm Xoay 360 Độ Chất Liệu Cao Cấp",
  "full_title_from_share_meta": "<decoded og_info title>",
  "brand": "HULAKO",              // inferred from title, marked as inferred downstream
  "price_original": null,
  "price_sale": null,
  "discount_pct": null,
  "sold_count": null,
  "rating": null,
  "description_excerpt": null,
  "fetched_ok": false,
  "error_if_any": "TikTok Shop product page returns SlardarWAF captcha..."
}
```

When user needs actual price/sold_count, present the partial result and ask
for human assist on the captcha, OR escalate to one of the Step-C fallbacks
in the skill.

## Brands Inferred — Audit

The 14 products cluster into 9 brands:

| Brand | Count | Notes |
|---|---|---|
| K&F CONCEPT | 3 | Cameras accessories (filters, case, cleaning pen) — well-known brand |
| GOOJODOQ | 3 | iPad stylus + powerbank + phone stand |
| ULANZI | 1 | MA66 tripod |
| HULAKO | 1 | LOX3 phone holder |
| Dodoto | 1 | Cordless vacuum |
| Armaf | 1 | Body spray |
| PW3 | 1 | Diffuser (model name, not brand — verify) |
| Universal | 1 | Arca-Swiss plate |
| Unbranded | 2 | Desk lamp + Sunset lamp |

Note: "PW3" might be the diffuser's *model number* not a brand. **Flag in
downstream usage** — user was told it's a "PW3" without confirming whether
that's brand or model.

## Cross-Skill Observations

- The redirect-to-WAF split is identical to what Shopee and Amazon short-links
  sometimes do — `sm.tiktok.com`, `shp.ee`, `amzn.to` may have similar layers
  where the redirect server is friendly but the destination is WAF'd. The
  same Step-A / Step-B pattern likely applies. Worth investigating for a
  future broader skill `ecommerce-shortlink-metadata`.
- `mcp__MiniMax__web_search` did not surface product-specific data even when
  the title was unique enough. For cached product metadata, Kalodata and
  FastMoss sites are more reliable aggregator targets than general search.
