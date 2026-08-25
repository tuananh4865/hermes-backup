# Batch Product Research Workflow (NEW v0.7.0, 2026-07-16)

When the user asks for research on a BATCH of products (e.g. "lên mạng tìm thông tin chính xác của 12 sản phẩm và import vào wiki"), don't research one-by-one. Use this parallel-subagent pattern.

## When to use

Trigger phrases:
- "research tất cả sản phẩm rồi viết script"
- "lên thông tin chính xác của N sản phẩm"
- "em cần có thông tin chính xác của toàn bộ N sản phẩm trước khi có thể viết script"
- "import data vào wiki" (when 5+ products involved)

The signal is: user wants **research BEFORE any script writing**, for a **batch** of products. If user wants 1 product, just run Phase 0 inline.

## 5-step procedure

1. **Group products by category** — read `Hermes-Edit/` filename list, extract distinct product slugs, group into 3-4 thematic clusters (body mist + tripod + bút iPad / ốp + máy hút bụi + bút K&F / etc.). Reason: subagents work better with a focused niche than 12 mixed products.

2. **Dispatch parallel subagents** via `delegate_task`:
   - 4 subagents for 12 products = 3 products/subagent is the sweet spot
   - Each subagent gets: (a) the 3 product names to research, (b) the JSON output schema, (c) explicit "MỖI SẢN PHẨM PHẢI CÓ ≥1 CITATION URL" requirement, (d) tools available (`web_search`, `web_extract`, `mcp__exa__*`)
   - Tell subagent to write output to `/Users/tuananh4865/research_<scope>.json` (NOT return inline — JSON is too large to embed in delegation result)

3. **Wait for fan-out completion** — Hermes re-enters the conversation with the consolidated results. Subagents run in background; don't poll.

4. **Batch import to wiki** — read JSON, for each product:
   - Build slug: `name.lower() → ASCII → kebab-case`
   - Build frontmatter (title, brand, origin, price_vnd, status: researched, sources: N)
   - Build body: metadata table + specs + USP + competitors + citations list + insights
   - Write to `wiki/projects/<project>/products/<slug>-<brand>.md`
   - **One file per product**, not one file per category. Wiki structure stays searchable.

5. **Embed summary in Telegram reply** — don't just save files and report. Show:
   - Table of all imported products (name, brand, price_vnd, citation count)
   - Group breakdown (which group, how many products)
   - Status of remaining subagents (3 still running, 1 done)

## Output JSON schema (required for subagents)

```json
{
  "groups": [
    {
      "group_id": 7,
      "group_name_vi": "Ngàm thao tác nhanh / Quick-release plate",
      "products": [
        {
          "name": "Ulanzi UKA01 Quick-release Plate (C007)",
          "brand": "Ulanzi",
          "origin": "China (Shenzhen Ulanzi Technology)",
          "specs": {"material": "...", "weight_g": 52, ...},
          "price_vnd": 420000,
          "usp_vi": "...",
          "competitors": ["Falcam F38", "Peak Design Capture"],
          "citations": ["https://...", "https://..."]
        }
      ]
    }
  ],
  "total_citations": 28
}
```

## Pitfalls

- **Don't write files inline from subagent result.** Subagents have isolated context, returning 12 products × 5 fields = ~30KB JSON inline. Read the JSON file from disk after fan-out completes.
- **Vietnamese diacritics in filenames.** `safe_slug()` function MUST convert: à→a, ư→u, đ→d, etc., and replace any non-ASCII with `-`. Otherwise `os.open` raises FileNotFoundError on macOS (case-insensitive APFS but strict UTF-8).
- **Slug collisions.** If 2 products in the same group have similar names (e.g. ARMAF + AMAP), append brand slug: `<name-slug>-<brand-slug>.md`.
- **Citation count is signal, not decoration.** Each product MUST have ≥1 URL. No URL = reject the entry, re-dispatch that product to a new subagent.
- **web_extract may fail (DuckDuckGo backend).** Subagent should fallback to `mcp__exa__web_fetch_exa`. Document the fallback in the JSON if it happens.
- **Don't write scripts before research.** User explicit: "cần có thông tin chính xác của toàn bộ N sản phẩm trước khi có thể viết script". If you catch yourself writing a script while research is still pending, STOP.

## Verified case (2026-07-16)

- **12 products across 4 subagents** (3 products/subagent) → all completed in ~5 min
- **28 citations across 12 products** = 2.3 citations/product average (above ≥1 floor)
- **3 subagents still pending** when first one returned — handled by reporting status, NOT blocking on completion
- **Vietnamese-safe slug function** was needed to avoid FileNotFoundError on filenames like `floveme-tripod-tf-3120-gậy-3-chân-kẹp-điện-thoại-floveme.md`
- **Final result**: 12 product files imported to `wiki/projects/tuan-anh-review-tiktok/products/`, all with `status: researched`, price_vnd, 4-7 citations each

## TikTok Shop short-link resolution (NEW 2026-07-20)

When user pastes `vt.tiktok.com/ZS9r...` short links instead of full URLs, resolve them BEFORE dispatching subagents. The short link redirects to `https://www.tiktok.com/view/product/<numeric_pid>` with the product title + image embedded in the `og_info` query param.

**Bash recipe (no web_search needed):**
```bash
curl -sIL --max-redirs 5 --max-time 10 "https://vt.tiktok.com/ZS9re2CFLXwGb-RjM5y/" \
  | grep -oE 'og_info=[^&\s]+|/view/product/[0-9]+'
```

**Python extractor pattern:**
```python
import re, subprocess
from urllib.parse import unquote

def resolve_tiktok_shortlink(url):
    r = subprocess.run(["curl", "-sIL", "--max-redirs", "5", "--max-time", "10", url],
                       capture_output=True, text=True)
    h = r.stdout
    pid = (re.search(r'/view/product/(\d+)', h) or [None, "unknown"])[1]
    m = re.search(r'og_info=([^&\s]+)', h)
    if m:
        decoded = unquote(m.group(1))
        title = re.search(r'"title":"([^"]+)"', decoded)
        image = re.search(r'"image":"([^"]+)"', decoded)
        return pid, (title.group(1).replace("+"," ") if title else "?"), (image.group(1).replace("\\/","/") if image else "")
    return pid, "?", ""
```

**Resolved URL pattern:** `https://www.tiktok.com/view/product/{pid}` — share this canonical URL with subagents instead of the short link.

**Tip:** The resolved title reads like SEO keyword spam ("Giá đỡ Điện thoại LOX3 Livestream Chụp Hình Sản Phẩm Xoay 360 Độ..."). Use it as a hint of what the seller emphasizes, NOT as authoritative specs. Specs come from Phase 0 web_search + exa.

## TikTok Shop anti-bot CAPTCHA workaround (NEW 2026-07-20)

**The hard problem:** `https://www.tiktok.com/view/product/<pid>` BLOCKS both `web_extract` and `browser_navigate` with anti-bot CAPTCHA as of July 2026. Browserbase warns "Running WITHOUT residential proxies. Bot detection may be more aggressive." Direct fetch returns CAPTCHA wall; no workaround via MCP browser tools.

**DO NOT waste time retrying direct fetches. Route around TikTok entirely.**

**3-tier fallback chain (use in order):**

| Tier | Tool | When it works | When it fails |
|------|------|---------------|---------------|
| 1 | `web_search` with `"<product name>" TikTok Shop giá` query | Most common — search engines index product pages even if direct fetch blocks | Sometimes returns only SEO summaries |
| 2 | `mcp__exa__web_fetch_exa` on `tiktok.com/view/product/...` URL | Works on simpler TikTok Shop pages | Still blocked for high-traffic SKUs |
| 3 | `mcp__exa__web_fetch_exa` on **third-party indexing sites** (FastMoss, Shopee VN, CellphoneS, brand official site, Amazon) | Almost always works | None — this tier is the most reliable |

**Verified source patterns (from 2026-07-20 real cases):**

| Product | Sources used | Why they work |
|---------|--------------|---------------|
| ULANZI MA66 Tripod | Ulanzi.com official + N4 MY + AliExpress + Huy Linh VN | Brand official has full specs; regional resellers confirm pricing |
| K&F PT61 Case | K&F official (kfconcept.com KF20.0024) + Amazon US + Kentfaith | Brand site has exact SKU; Amazon has social proof + price consistency |
| ARMAF Odyssey | armafvietnam.vn (TCR Distributing) + Fragrantica + YouTube reviews | VN official distributor has exact VN variant list; Fragrantica has fragrance notes |
| GOOJODOQ pen (fixed MAJOR brand error) | TikTok Shop listing (`og_info.title`) + GOOJODOQ global site | Title says "[GOOJODOQ*KOL/KOC]"; we corrected `goldjordock → goojodoq` |

**Tool preference note:** The default `web_extract` uses DuckDuckGo backend (search-only, unreliable page fetch). For TikTok Shop data, **`mcp__exa__web_fetch_exa` is the working tool**. Always have subagents try exa first for TikTok Shop research; fall back to `web_search` snippets if exa also blocks.

## Cross-source citation discipline (NEW 2026-07-20)

**Rule:** Every spec/number/brand claim in the resulting wiki file must trace to **≥2 independent sources**. If only 1 source confirms a claim, mark it with ⚠️ (acceptable but flag).

**Anti-pattern (fabrication):**
- ❌ Cite only the brand's own website (self-claim, marketing copy)
- ❌ Cite only the seller's TikTok Shop listing (no third-party confirmation)
- ❌ Carry forward old claims from previous wiki files without re-verification

**Verification ladder (most → least authoritative):**

1. **Brand official site** (`ulanzi.com/products/Ma66`) — canonical specs
2. **Regional distributor / official VN site** (`armafvietnam.vn`) — VN-specific variants + prices
3. **Independent industry databases** (Fragrantica, GSMArena, DPReview) — compositional specs
4. **Major retailers** (Shopee VN, Lazada, Amazon) — actual price + variant availability
5. **Creator reviews** (YouTube, Reddit) — real-world usage, longevity
6. **TikTok Shop listing title** (`og_info`) — keyword hints only, NOT specs

**Conflict resolution:** When sources disagree (e.g., Ulanzi 500g load vs Huy Linh 250g), **follow official-brand-site priority** and document the conflict in the wiki file with the rationale.

**Drop unverifiable claims.** Verified case: K&F PT61 had an old "70g weight" claim with no source. Subagent **dropped the claim entirely** rather than keep an unverified number — added "Not officially specified" instead. Safer than guessing.

**Append to file footer when verified:**
```markdown
---
*Updated: 2026-07-20 — verified against 4 independent sources (Ulanzi official + N4 + AliExpress + Huy Linh VN)*
```

## Verified multi-batch case (NEW 2026-07-20)

**Scenario:** User sent 14 `vt.tiktok.com/...` short links for products he's currently selling as TikTok Shop affiliate.

**Final distribution after dispatch:**
- ✅ 4 brand-new products researched from scratch (LOX3, Arca Swiss, PW3, Đèn LED) — wiki files created
- ✅ 7 existing files verified + updated (ULANZI MA66, K&F PT61, ARMAF Odyssey, Dodoto, GOOJODOQ ×3) with new citations
- ⚠️ 2 files CAPTCHA-blocked — kept original content with `verify-status: blocked-captcha` metadata
- ⏳ 1 file pending research (sunset lamp)

**Major data correction caught:** A bút cảm ứng iPad product filed under `goldjordock` (assumed OEM) was actually **GOOJODOQ chính hãng** with a 38% discount (₫799k → ₫498,820). 3.3x price difference caught by cross-checking TikTok Shop listing title with GOOJODOQ global site.

**Subagent batch results:**
- Subagent 1 (4 new products): completed 293s, 4 files 1.3-1.4KB each
- Subagent 2 (3 verify): TIMEOUT 600s on `web_extract` → re-dispatched with `web_search` instead → completed 344s on retry
- Subagent 3 (4 verify GOOJODOQ+Dodoto): completed 376s, 49 API calls
- Subagent 4 (2 K&F verify): completed 68s but BOTH returned NO CHANGE due to CAPTCHA (honest anti-fabrication discipline)

**Total wall time:** ~10 min from link resolution to all wiki files written + hub.md updated + bảng tổng hợp embed trong Telegram reply.

**Key takeaway for the workflow:** When verifying EXISTING wiki files against TikTok Shop, the subagent task is "compare file content to TikTok Shop listing + 2+ independent sources, update if different". The TikTok Shop listing provides the price/origin truth signal; the independent sources (brand official, retailers) provide the specs authority. Don't conflate them.