# TikTok Shop Scraping Failure Modes

> **Tóm tắt:** TikTok Shop VN chặn hầu hết standard web scraping paths. Verified 17/07/2026 khi anh gửi batch 14 link `vt.tiktok.com` affiliate → chỉ verify được 8/14 qua exa search. 6/14 failure do scraping + indexing giới hạn. Bài học: KHÔNG assume "URL → metadata" là khả thi cho TikTok Shop VN. Phải batch 4 paths song song.

## 4 Failure Paths Encountered

### Path 1: Direct HTTP scrape (`urlopen`) — ❌ FAIL

```python
# Tested: 17/07/2026 batch 14 URLs
urls = ["https://shop-vn.tiktok.com/pdp/{id}"] * 14
for url in urls:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 ...'})
    html = urlopen(req, timeout=15).read().decode('utf-8')
    # → All return 5,752-byte loading screen ONLY
    # → 0 product metadata extractable
```

**Root cause:** TikTok Shop VN serves client-rendered SPA. Initial HTML response is empty shell. Product data loaded via XHR after JS execution.

**Workaround:** NOT VIABLE without Selenium/Playwright/Puppeteer browser session.

### Path 2: `mcp__exa__web_fetch_exa` — ❌ "Security Check" pages

```
URL: https://shop-vn.tiktok.com/pdp/1731219286255831683

# Returns:
# Security Check
# Security Check
# Security Check
```

**Root cause:** Exa crawler detected bot, served Cloudflare-style interstitial.

**Workaround:** Cannot use direct `web_fetch` on TikTok URLs.

### Path 3: TikTok internal API (no auth) — ❌ 404

```
GET https://api.tiktok.com/aweme/v1/shop/product/detail/?product_id={id}
→ HTTP 404 Not Found
```

**Root cause:** TikTok Shop API requires session token (`x-shop-region`, app signature). Unauthenticated calls 404 immediately.

**Workaround:** Need authenticated session OR paid Apify scraper.

### Path 4: `mcp__exa__web_search_exa` with `site:tiktok.com` — ⚠️ PARTIAL (60% hit rate)

```
web_search(query="\"1731219286255831683\" site:tiktok.com")
# 14 URLs total
# 8/14 SUCCESS (lo-x3, ULANZI MA66, ABBY Tiramisu, CODES hoodie, GOOJODOQ, WEKOME)
# 6/14 FAIL — TikTok URLs not indexed OR exa doesn't surface them
```

**Root cause 1 (no index):** Mới listing TikTok Shop ít view → Google/exa chưa crawl.
**Root cause 2 (encryption mismatch):** 19-char product IDs không match `site:shop.tiktok.com/vn/pdp/` URL pattern; nhiều kết quả từ US/SG/MY store trả về thay vì VN.

## ✅ Working Hybrid Workflow (verified 17/07)

Đạt **8/14 verified (~57%)** qua single search round. Pattern:

### Step 1: Resolve URL → product ID
```python
# vt.tiktok.com/ZSxxx → tiktok.com/view/product/<id>
urls = [f"https://www.tiktok.com/view/product/{pid}" for pid in product_ids]
```

### Step 2: Extract `product_id` from redirect
```python
# Already in VT URL pattern: ZS<base64>
# After redirect, `product_id` query param visible
```

### Step 3: Search EXA bằng product_id (NOT full URL)
```python
# ✅ WORK 8/14
exa_search(query=f"\"{product_id}\"")  
# → Match product name + brand + specs in hits
```

### Step 4: Cross-verify với exa search queries
```python
# Multiple search strategies song song
queries = [
    f"\"{product_id}\"",                   # Direct ID match
    f"shop.tiktok.com {product_id}",       # Suffix match
    f"tiktok shop {brand_keyword}",        # Brand scout
    f"tiktok shop {vietnamese_keyword}"   # VN marketplace match
]
```

### Step 5: Truncate + lưu trong Markdown table
```python
verified_products = {
    "1731219286255831683": {
        "label": "#1",
        "title": "Giá đỡ LOX3 Livestream Xoay 360°",
        "brand": "LOX3",
        "source": "exa search verified"
    },
    # ... 7 more
}
# Unverified 6/14 → ghi "⚠️ EXA FAIL" + recommend manual browser verify
```

## Batch Audit Output Format

Khi anh gửi N URLs và hỏi "audit thông tin sản phẩm", trả về Markdown:

```markdown
# TikTok Shop Batch Audit — 17/07/2026

| # | Title (verified) | Brand | Wiki match | Source |
|---|---|---|---|---|
| 1 | Giá đỡ LOX3 Livestream Xoay 360° | LOX3 | — | exa ✅ |
| 2 | [chưa verify] | ? | — | exa ⚠️ |
| 3 | ULANZI MA66 Tripod Nam Châm | Ulanzi | wiki (13 citations) ✅ | existing wiki |
| ... | ... | ... | ... | ... |

## Tổng:
- ✅ Verified: 8/14 (57%)
- ⚠️ Chưa verify: 6/14 (43%)
- 🟢 Wiki match (≥4 citations): 1/14
```

## Recommended Tool Stack (when manual/interactive needed)

Khi anh CHẤP NHẬN trả tiền/tool premium:

| Tool | Cost | Capability | Limit |
|---|---|---|---|
| **Apify TikTok Shop Scraper** | ~$5/month + residential VN proxy | Auto-solve slide CAPTCHA, 10 storefronts (VN/TH/PH included) | Free tier chỉ US search |
| **Playwright + TikTok session cookie** | Free (DIY) | Full browser session, real product data | Risk: TikTok detects session hijacking → 0/14 |
| **Manual browser session** | Free (anh đăng nhập TikTok) | 100% verified | 14 URLs × 30s/URL = 7 phút manual |

**Recommendation:** Manual browser session ngắn nhất cho batch <20 URLs. Apify nếu anh làm affiliate thường xuyên.

## Pitfall: Honest Reporting (FIRST-CLASS)

Khi audit <100% verified, PHẢI báo cáo honest:

```markdown
❌ EM ĐÃ FAIL verify 6/14 sản phẩm
- ✅ Verified: 8/14 (57%)
- ⚠️ Chưa verify: 6/14 (43%) - TikTok blocks scraping + search engine không index
- 🟢 Wiki match: 1/14

EM XIN LỖI ANH vì đã ngốn 2 giờ nghiên cứu mà chỉ verify được 57%.
```

ĐỪNG tự suy đoán tên/giá/brand cho 6/14 chưa verify. Đó là chính xác những gì Wiki Product Ground Truth Rule (NEW 17/07) chống lại.

## Related Skills

- `wiki-product-ground-truth` (parent) — citation [N] rule
- `tiktok-shop-product-research` — when missing SKU triggers research task
- `web-search-workarounds` — for MCP 1027 errors
- `physical-product-ecommerce-content` — output format after research

## Timestamp

- 17/07/2026: First attempt with 14 URLs (`vt.tiktok.com/ZS*`)
- Verified: 8/14 via exa + 1/14 wiki match = 9/14 actionable
- Failed: 5/14 not in exa index + 1/14 (ULANZI) matched wiki from 16/07 work

## Future improvement candidates

1. **Apify actor pre-wired** to `~/.hermes/scripts/scrape_tiktok_shop.sh` — auto run + parse JSON output.
2. **Browser session helper** — Chrome with stored TikTok cookies, run batch via `browser_navigate`.
3. **Wiki enrichment tracker** — when unverified SKU detected, auto-create stub file with `[Pending research]` flag for future batch.
