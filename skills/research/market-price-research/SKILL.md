---
name: market-price-research
version: 0.1.0
author: Hermes
description: Research market price for a SKU or product family, with explicit comparison against the user's inventory/stock price. Returns a structured table with 🟢/🔴/🟡 flags showing where the user's stock is cheaper, costlier, or aligned with market. Use when user asks "giá thị trường", "giá bao nhiêu", "có nên nhập/bán", "compare với giá em đang bán", "kho em giá bao nhiêu vs thị trường", or any request that needs cross-reference between user inventory and live market price.
metadata:
  hermes:
    tags: [research, ecommerce, price, inventory, comparison, market]
---

# market-price-research

Research **market price** for a SKU or product family, then **compare against the user's inventory/stock price** to flag where the user is cheaper, costlier, or aligned. The output is a table with pricing tiers + raw citations, designed so the user can make 4 decisions in 30 seconds: *mua/bán bao nhiêu là hợp lý? · cây nào trong kho đang lời/lỗ? · cây nào cần giảm giá? · nên nhập/bán gì?*

## When to Use

- User asks "giá thị trường X bao nhiêu" / "giá cả thị trường" / "giá bán" → price research for a SKU or model
- User asks "giá kho anh so với thị trường" / "cây này có nên bán" / "có nên nhập" → comparison + inventory cross-check
- User asks "tìm giá mấy cây vợt khác" / "giá các dòng Yonex" → multi-SKU batch research
- User asks "so sánh giá" với bất kỳ category nào (vợt cầu lông, body mist, máy ảnh, accessory) — class này KHÔNG chỉ giới hạn ở 1 category
- Trigger phrases: "giá thị trường", "kho em", "có nên nhập", "có nên bán", "giá bao nhiêu", "compare giá", "đối chiếu giá", "so sánh với thị trường", "market price"

## When NOT to Use

- **Pure product research for a script** (specs + USP + competitors) → use `tiktok-product-script` instead
- **TikTok Shop shop-scraping** → use `research/tiktok-shop-product-research`
- **Resale pricing for a single second-hand item** → use chat 1-1, no skill needed
- **Sales-script content** ("viết script bán)") → use `content-creator-script-style` or `tiktok-product-script`

## Core Concepts

### 1. User-name ≠ Product catalog name

User thường nhắc tên sản phẩm NGẮN, không chính xác, dễ gây ambiguity:

| User nói | Có thể là | Cách disambiguate |
|---|---|---|
| "vợt 77 Pro" | Yonex Astrox 77 Pro / 77 Pro cũ / 77 Pro 2024 | Search "vợt 77 Pro" → confirm series + brand |
| "body mist Lemony" | Lush Flutter Lemony / Naturalium Lemony / BODYMISS Lemony / Descriptor (không phải brand) | Scan wiki + Hermes-Edit filenames trước khi search |
| "ốp Pocket 3" | K&F PT61 / Sunnylife 754v2 / BRDRC / OEM ốp | Match tên user vừa nói vs inventory scan |
| "MA66" | Ulanzi MA66 (Pocket 3 tripod) | Mặc định = brand đã có trong wiki |

**Decision rule:** KHÔNG search với tên user đưa ra verbatim. LUÔN augment tên với brand hints từ wiki context — hoặc hỏi user ONCE nếu không có wiki context.

### 2. Inventory lives in 3 places — scan TRƯỚC khi hỏi

Khi user nói "kho của em", "inventory", "cây em đang có", scan 3 nơi theo thứ tự ưu tiên:

```
1. Wiki specs reference file (FASTEST):
   search_files pattern="*yonex*" OR pattern="*vot*" path="/Volumes/Storage-1/Hermes/wiki/projects"
   → file "/Volumes/Storage-1/Hermes/wiki/projects/<project>/products/<brand>-specs-reference.md"
   → chứa bảng specs + giá kho + số lượng SKU

2. Hermes-Edit filenames (cho SP đã edit):
   search_files pattern="FINAL_" path="/Volumes/Storage-1/Pocket3/Hermes-Edit"
   → parse regex `clip_NNNN_V\d+_\d+s?_(.+)\.mp4` → extract SP name
   → nếu filename có tên SP → user đã edit → likely có trong kho

3. Wiki products folder (cho SP đã research):
   search_files pattern="*.md" path="/Volumes/Storage-1/Hermes/wiki/projects/<project>/products"
   → mỗi file = 1 SP đã có research cache
```

**Anti-pattern (FAIL case 26/07):** user hỏi "thêm cột so sánh với giá thị trường" → em scan 4 chỗ (Hermes-Edit/, Footages/, QuyNhon2026/, wiki/products/) → TẤT CẢ đều không có vợt. Cuối cùng mới tìm thấy inventory trong `wiki/projects/tuan-anh-badminton/products/yonex-specs-reference.md` (nằm trong project badminton, không phải review-tiktok). 

**Fix:** LUÔN scan `/Volumes/Storage-1/Hermes/wiki/projects/` (TẤT CẢ projects, không chỉ project đang active) trước khi conclude "không có inventory".

### 3. Market price = 3 tiers, mỗi tier 1 flag

Giá thị trường VN thường có 3 tiers:

| Tier | Định nghĩa | Use case |
|---|---|---|
| **Giá bán lẻ chính hãng** | Shop lớn (ShopVNB, XB Sports, Thế Giới Cầu Lông, Đại Hưng) | Khi user so sánh giá bán online |
| **Giá sale tốt** | Shop sale, không phải lúc nào cũng có | Khi user muốn mua giá tốt |
| **Giá cũ** | 30-40% thấp hơn giá mới, tùy tình trạng | Khi user muốn bán/mua second-hand |

**Cross-check tối thiểu 3 sources** trước khi put number vào table. Nếu 1 source độc lập → KHÔNG đưa ra — KHÔNG đoán.

### 4. Output table format (FIRST-CLASS)

Mỗi khi xong research, output BẮT BUỘC có table với format:

```
| SP | Giá kho | Giá thị trường | Chênh lệch | Flag |
|---|---:|---:|---:|:---:|
| SP-1 | 4.500.000 | 4.300.000 - 4.700.000 | Ngang | 🟡 |
| SP-2 | 3.950.000 | 4.350.000 - 4.550.000 | Rẻ hơn 400-600k | 🟢 |
| SP-3 | 3.611.000 | 2.700.000 - 3.200.000 | Cao hơn 400-700k | 🔴 |
```

**Flag rules:**
- 🟢 **Lời/Deal** — giá kho RẺ hơn thị trường ≥ 5% → user có lợi thế bán
- 🟡 **Ngang** — giá kho nằm trong range thị trường → fair
- 🔴 **Lỗ/Caution** — giá kho CAO hơn thị trường ≥ 5% → khó bán, cần giảm giá

**Sau table, BẮT BUỘC có 3 sections:**
1. **Recommended actions** — 1 dòng/flag (vd: "đẩy mạnh TikTok/FB", "cần giảm giá", "bundle")
2. **Tiêu chí mua/bán** — đoạn ngắn dựa trên table (vd: "mua mới dưới 4.2tr = tốt; bán cũ đẹp = ~2tr")
3. **Caveats** — giá kho có thể cũ (file 08/07), cần verify với sổ hiện tại

## How to Run

### Step 1 — Capture user's request + initial scan

```bash
# 1a. Extract product name from user message
# VD: "vợt cầu lông 77 pro" → "77 Pro" (likely Yonex Astrox 77 Pro theo context)

# 1b. Scan inventory FIRST (3 paths trên)
search_files pattern="*yonex*" path="/Volumes/Storage-1/Hermes/wiki/projects"
search_files pattern="77" path="/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/products"
search_files pattern="FINAL_77" path="/Volumes/Storage-1/Pocket3/Hermes-Edit"
```

### Step 2 — Search market price (3 sources minimum)

```python
# Primary: mcp__exa__web_search_exa (VN retailer mirror)
results = web_search(
  query='"Yonex Astrox 77 Pro" giá Việt Nam',
  numResults=8
)

# Cross-check sources
candidates = [
  "shopvnb.com", "xbsports.vn", "thegioicaulong.com.vn",
  "daihungsport.vn", "hvshop.vn", "nicsports.vn"
]
```

### Step 3 — Fetch retail pages for exact price

```python
# Sử dụng mcp__exa__web_fetch_exa, KHÔNG dùng web_extract (search-only)
for url in [validated_shop_urls]:
  page = mcp__exa__web_fetch_exa(urls=[url], maxCharacters=3000)
  # Extract: price_vnd, in_stock, bảo hành, options (3U/4U)
```

### Step 4 — Build comparison table

```python
# Inventory price (từ wiki specs file hoặc user confirm)
inventory = {
  "Astrox 77 PRO": 3_950_000,  # giá kho hiện tại
  "Astrox 99 PRO": 4_500_000,
  # ...
}

# Market price (từ 3+ sources)
market = {
  "Astrox 77 PRO": (4_349_000, 4_550_000),  # (min, max)
  "Astrox 99 PRO": (4_500_000, 4_800_000),
  # ...
}

# Compute flag
def flag(inv, market_min, market_max):
  if inv < market_min * 0.95: return "🟢"
  if inv > market_max * 1.05: return "🔴"
  return "🟡"
```

### Step 5 — Deliver

```
Output:
1. Table comparison (giá kho vs thị trường + flag)
2. Recommended actions (theo flag)
3. Caveats (giá kho có thể cũ, giá thị trường có thể sale/regular)
4. Sources (URL list, tối thiểu 3 cho mỗi SKU)
```

## Pitfalls

- **Don't trust user verbatim name** — user may say "vợt 77 Pro" without brand. ALWAYS scan wiki specs first to find the brand+series combo. Verified case 26/07: "77 Pro" = Yonex Astrox 77 Pro (confirm từ `wiki/projects/tuan-anh-badminton/products/yonex-specs-reference.md`).
- **Don't trust single-source price** — Always cross-check ≥3 sources. If only 1 source → state "1 source", not 3.
- **Don't use web_extract** — DDG backend is search-only, will fail. Use `mcp__exa__web_fetch_exa` for retail pages.
- **Don't cite TikTok Shop price** — SlardarWAF blocks. Use VN retailer mirrors (ShopVNB, XB Sports, etc.) instead. Listed in `references/tiktok-shop-product-research` skill § Step C.
- **Don't ignore inventory staleness** — `yonex-specs-reference.md` was last updated 2026-07-08. If user asks "giá kho em hiện tại" cho SP đó, MUST flag "giá kho 08/07 — verify với sổ trước khi dùng".
- **Don't fabricate specs/prices** — Same rule as `tiktok-product-script` PITFALL "Skip Phase 0 = bịa data". If search returns 0 → say "Không tìm thấy" hoặc "Cần user browse thủ công".
- **Don't deliver without table** — BẮT BUỘC output table so anh đọc được 30s. Không table → fail.
- **Don't follow user verbatim khi user typo** — VD: "thêm một cốt so sánh" → "cốt" = "cột" (typo). Em hiểu intent = "thêm 1 cột so sánh" → không hỏi lại. Self-check: scan user message cho common typos (cốt/cột, scrip/kịch bản, v.v.) trước khi ask.
- **Don't scan 1 place for inventory** — User's inventory có thể ở:
  1. `wiki/projects/<project>/products/<brand>-specs-reference.md` (single source of truth)
  2. `wiki/projects/<project>/products/<sku>.md` (per-SKU)
  3. `/Volumes/Storage-1/Pocket3/Hermes-Edit/` filenames (đã edit/used)
  4. `/Volumes/Storage-1/Pocket3/badminton/` HOẶC `/Footages/` (raw footage, có thể có sản phẩm trong frame)
  5. `/Volumes/Storage-1/Pocket3/QuyNhon2026/` (raw footage khác)
  → Scan TẤT CẢ 5 paths trước khi conclude "không có inventory".
- **Mỗi cây flag KHÔNG overlap** — 1 cây = 1 flag. Nếu 1 cây vừa 🟢 vừa 🔴 → split thành 2 dòng (vd: giá bán thấp 🟢, giá cũ cao 🔴).
- **Date trong citation** — Nếu source published date > 6 tháng → flag "Giá có thể đã thay đổi". Verified case 26/07: source mediavietnam.org dated 2025-07 → 1 năm cũ → chỉ dùng làm reference, không dùng làm primary.

## Verification

After delivering, confirm via `terminal`:

```bash
# Check file inventory was scanned
ls /Volumes/Storage-1/Hermes/wiki/projects/*/products/*specs*.md 2>/dev/null

# Verify table format in response
echo "PASS criteria:"
echo "  - Table có ≥ 3 cột (SP, giá kho, giá thị trường)"
echo "  - Có flag 🟢/🔴/🟡 cho mỗi hàng"
echo "  - Có ≥ 3 sources độc lập cho mỗi SKU"
echo "  - Có Recommended actions + Caveats sections"
```

## Companion Skills

- `tiktok-product-script` — Main phase 0 research cho TikTok Shop affiliate script (different goal: writing content, not price comparison)
- `research/tiktok-shop-product-research` — SlardarWAF bypass + VN retailer mirror list (share same fallback ladder)
- `wiki-product-ground-truth` — Use wiki spec refs as source of truth, KHÔNG fabricate
- `naming-inference` (TODO if needed) — Disambiguate short product names

## Lessons Applied (from 2026-07-26 session)

1. **Inventory in unexpected project** — Em scan 4 chỗ, KHÔNG thấy inventory của vợt. Cuối cùng tìm thấy ở `wiki/projects/tuan-anh-badminton/` (không phải `tuan-anh-review-tiktok/` đang active). Fix: scan `wiki/projects/*/` (wildcard) trước.
2. **Price comparison table** — Output table với flag 🟢/🔴/🟡 giúp anh đọc 30s và ra 4 decisions (mua/bán/nhập/xả). BẮT BUỘC format này.
3. **Short-name inference** — "77 Pro" = Yonex Astrox 77 Pro (Yonex là brand mặc định cho category cầu lông). Không cần ask user vì Yonex + 77 Pro = unambiguous trong badminton market.
4. **Don't follow user verbatim typo** — "cốt" = "cột" → infer intent không hỏi.
5. **Cite-after-the-fact** — Mỗi row cần ≥ 1 source URL ở cuối response. Verified case 26/07: 4 sources cho Astrox 77 Pro (ShopVNB, XB Sports, Thế Giới Cầu Lông, Media Vietnam).

---

*Skill created 2026-07-26 from session "vợt cầu lông 77 Pro" → "tìm giá các dòng vợt khác trong inventory + cột so sánh". Verified end-to-end: 12 SKUs Yonex cross-checked vs 4 sources, output table with 3 flags. ~10 min total session.*
