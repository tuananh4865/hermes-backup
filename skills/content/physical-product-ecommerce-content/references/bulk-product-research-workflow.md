# Bulk Product Research Workflow — Parallel Subagent Dispatch + JSON Aggregation + Wiki Import

> **Reference file.** Companion to `physical-product-ecommerce-content` SKILL.md § PITFALL #43. Load khi user yêu cầu "lên mạng tìm thông tin N sản phẩm + import vào wiki".

## When to use this workflow

Trigger phrases:
- *"Lên mạng tìm thông tin chính xác của N sản phẩm + import vào wiki"*
- *"Research N sản phẩm TikTok shop để viết script"*
- *"Cần thông tin chính xác toàn bộ N sp"*

Anti-trigger (use single-product Phase 0 from `tiktok-product-script` instead):
- User chỉ cần data cho 1 sản phẩm
- User không cần research từ web (đã có data)
- Sản phẩm quá niche (<10 search results)

## Verified case study (session 16/07/2026)

**Input:**
- 12 nhóm sản phẩm Tuấn Anh Review TikTok (đã enumerate từ Hermes-Edit)
- Anh yêu cầu: *"Em cần có thông tin chính xác của toàn bộ 12 sản phẩm trước khi có thể viết script nên hãy lên mạng tìm thông tin chính xác của 12 sản phẩm và import vào wiki đi"*

**Output:**
- 29 markdown product files imported vào `wiki/projects/tuan-anh-review-tiktok/products/`
- 100+ citations (URLs from shopee.vn, tiktok.com, brand official sites, genk.vn, tinhte.vn, etc.)
- Tổng thời gian: ~10 phút (4 parallel subagents × 5-7 phút + aggregate 1 phút)

## 4-step workflow

### Step 1: Chunk N products into M groups

**Sweet spot: 3 products per subagent** (verified session 16/07). Group by category/brand để research chuyên sâu hơn.

```python
# Example: 12 products → 4 groups of 3
groups = [
    {"id": 1, "name": "Body Mist + Tripod Ulanzi + Bút iPad", "products": [...]},
    {"id": 2, "name": "Ốp Pocket 3 + Máy hút bụi + Bút K&F", "products": [...]},
    {"id": 3, "name": "Ngàm quick-release + Sạc dự phòng + Giá đỡ", "products": [...]},
    {"id": 4, "name": "Bộ vệ sinh ống kính + Đèn LED + Lemony", "products": [...]},
]
```

### Step 2: Dispatch parallel subagents

```python
from hermes_tools import delegate_task

for group in groups:
    goal = f"""
Research CHÍNH XÁC thông tin {len(group['products'])} sản phẩm:
{chr(10).join(f'- {p}' for p in group['products'])}

Yêu cầu:
1. Dùng web_search + web_extract (ưu tiên mcp__exa__web_fetch_exa vì DuckDuckGo backend hay fail)
2. Mỗi sản phẩm PHẢI có ≥1 citation URL nguồn thật (shopee.vn, tiktok.com, brand official, retailer uy tín)
3. Output format JSON array, mỗi object có:
   - name, brand, origin, specs (object), price_vnd, usp_vi, competitors (list), citations (list URL)
4. Trả về tiếng Việt cho description, tiếng Anh cho specs
5. Lưu output vào /Users/tuananh4865/research_tiktok_group_{group['id']}.json
"""
    delegate_task(goal=goal, role="leaf", context="AUDIENCE: Tuấn Anh cần data CHÍNH XÁC để viết script TikTok + bán hàng. KHÔNG bịa data — phải có citation URL.")
```

**Key settings:**
- `role="leaf"` (không cho subagent dispatch tiếp)
- Mỗi subagent chạy isolated context (max 4 concurrent theo Hermes config)

### Step 3: Aggregate JSON files

```python
import json
import os

results = []
for filepath in [
    "/Users/tuananh4865/research_tiktok_groups_1_2_3.json",
    "/Users/tuananh4865/research_tiktok_groups_4_5_6.json",
    "/Users/tuananh4865/research_tiktok_groups_7_8_9.json",
    "/Users/tuananh4865/research_tiktok_groups_10_11_12.json",
]:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for group in data.get("groups", []):
            results.extend(group.get("products", []))

print(f"Total products: {len(results)}")
total_citations = sum(len(p.get("citations", [])) for p in results)
print(f"Total citations: {total_citations}")
```

### Step 4: Bulk write markdown files

```python
import os
import re

def safe_slug(s):
    """Convert Vietnamese + special chars to ASCII slug."""
    s = s.lower()
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[đ]', 'd', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = '-'.join(filter(lambda x: x, s.split('-')))
    return s[:80]

def build_product_file(prod):
    """Build markdown file content."""
    name = prod.get("name", "Unknown")
    brand = prod.get("brand", "Unknown")
    origin = prod.get("origin", "Unknown")
    specs = prod.get("specs", {})
    price_vnd = prod.get("price_vnd", 0)
    usp = prod.get("usp_vi") or prod.get("usp", "")
    competitors = prod.get("competitors", [])
    citations = prod.get("citations", [])
    rating = prod.get("rating_signal", "")
    
    specs_md = "\\n".join([f"- **{k}**: `{v}`" for k, v in specs.items()])
    competitors_md = "\\n".join([f"- {c}" for c in competitors])
    citations_md = "\\n".join([f"{i+1}. <{c}>" for i, c in enumerate(citations)])
    
    content = f"""---
title: {name}
type: product
brand: {brand}
origin: {origin}
status: researched
price_vnd: {price_vnd}
confidence: high
sources: {len(citations)}
---

# {name}

> **Đã research** (16/07/2026) — thông tin chính xác từ web, có {len(citations)} citations.

## 📋 Metadata
| Field | Value |
|---|---|
| Tên | {name} |
| Brand | {brand} |
| Origin | {origin} |
| Giá VN | {price_vnd:,} VND |
| Rating | {rating} |

## 🔧 Specs
{specs_md}

## 🎯 USP
{usp}

## ⚔️ Đối thủ
{competitors_md}

## 📚 Citations
{citations_md}
"""
    
    name_slug = safe_slug(name)
    brand_slug = safe_slug(brand)
    fname = f"{name_slug}-{brand_slug}.md"
    return fname, content

# Bulk write
wiki_products = "/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products"
os.makedirs(wiki_products, exist_ok=True)

for prod in results:
    fname, content = build_product_file(prod)
    fpath = os.path.join(wiki_products, fname)
    
    # Collision handling
    if os.path.exists(fpath):
        base, ext = os.path.splitext(fname)
        counter = 2
        while os.path.exists(fpath):
            fname = f"{base}-v{counter}{ext}"
            fpath = os.path.join(wiki_products, fname)
            counter += 1
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
```

## Critical rules (BẮT BUỘC)

1. **Citation minimum:** Mỗi sản phẩm PHẢI có ≥1 URL thật. Không có citation = không import vào wiki, report lại để subagent search lại.

2. **Tool fallback chain:** `mcp__exa__web_fetch_exa` (ưu tiên) → `web_extract` (fallback) → `browser_navigate` (last resort). `web_extract` với DuckDuckGo backend hay fail với Vietnamese URLs.

3. **Subagent role:** PHẢI là `leaf` để tránh recursive delegation (exceeds `max_spawn_depth=1`).

4. **File collision:** Nếu 2 sản phẩm khác nhau cùng slug → append `-v2`, `-v3`. Verified case: 2 file cho ARMAF Odyssey vì subagent tạo 2 entry khác (mega vs homme).

5. **Category check:** Trước khi dispatch, đảm bảo product slug match category (tránh route nhầm project như L38 — `tuan-anh-review-tiktok` vs `tuan-anh-badminton`).

## Common pitfalls

### Pitfall 1: Subagent timeout / silent fail

**Symptom:** Subagent dispatch xong nhưng không có file JSON output.

**Fix:** Wait + check `process(action='list')` xem có subagent pending. Nếu timeout >10 phút → re-dispatch với context rõ hơn. Nếu subagent return "no results" → simplify query (ít product hơn, brand cụ thể hơn).

### Pitfall 2: web_extract fails silently

**Symptom:** Subagent báo "search complete" nhưng không có URL citations.

**Root cause:** DuckDuckGo backend không extract được Vietnamese e-commerce URLs.

**Fix:** Force subagent dùng `mcp__exa__web_fetch_exa` (đã verify work với shopee.vn, tiktok.com, amazon).

### Pitfall 3: Citation URL không accessible

**Symptom:** Subagent output URL nhưng khi em check thực tế → 404 / paywall.

**Fix:** Spot-check 5-10 citations bằng `web_extract` trước khi accept. Drop products có all-citations invalid.

### Pitfall 4: Product sai category / brand confusion

**Symptom:** Subagent output "ARMAF Odyssey Homme" ở cả nhóm Body Mist + nhóm Fragrance → duplicate.

**Fix:** Dedupe sau aggregate (group by product_name, keep first occurrence with more citations).

### Pitfall 5: File name collision sau bulk write

**Symptom:** 2 sản phẩm cùng slug → file 1 overwrite file 2.

**Fix:** Loop kiểm tra `os.path.exists()` + append `-v2`, `-v3`. Đã verify xảy ra với ARMAF (mega vs homme → 2 file khác brand slug).

## Performance baseline

- **Dispatch latency:** ~1 phút (4 subagents start parallel)
- **Subagent duration:** 4-7 phút mỗi cái (research 3 sp)
- **Aggregate + import:** ~1 phút
- **Tổng:** ~10 phút cho 12 nhóm sản phẩm

So với serial: 12 sp × 1-2 phút/sp = 24 phút + 12 manual imports = ~40 phút. Speedup: **4×**.

## Output verification checklist (Evidence Gate)

Sau khi bulk import, verify:
1. ✅ Số file trong `wiki/products/` tăng đúng số lượng dự kiến
2. ✅ Mỗi file có frontmatter với `status: researched` + `sources: N`
3. ✅ Mỗi file có ít nhất 1 URL citation trong section "📚 Citations"
4. ✅ File naming convention: `<slug>-<brand>.md` (ASCII only, no Vietnamese diacritics)
5. ✅ Không có file stub cũ nào bị mất (kiểm tra mtime)

```bash
# Verify count
ls /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/*.md | wc -l

# Check status distribution
grep -l "status: researched" /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/*.md | wc -l
grep -l "status: pending-phase-0-research" /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/*.md | wc -l
```

## Cross-references

- `physical-product-ecommerce-content/SKILL.md` § PITFALL #41-43 (3 pitfalls mới nhất)
- `references/tuan-anh-review-tiktok-inventory.md` (Pitfall #41 enumeration)
- Skill `tiktok-product-script` Phase 0 (single-product research workflow)
- Skill `evidence-first-delivery` (Evidence Gate 5 chứng cứ)

## Related sessions

- 2026-07-16: First bulk research (12 groups → 29 products → 100+ citations)
- Bulk pattern có thể scale cho N bất kỳ (3 sp/subagent là sweet spot)