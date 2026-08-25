# Tuấn Anh Review TikTok — Inventory + Enumeration Workflow

> **Reference file.** Companion to `physical-product-ecommerce-content` SKILL.md. Read this BEFORE enumerating "what products does anh have" for the Tuấn Anh Review TikTok project. Companion to `tuan-anh-badminton-inventory.md` (which covers the OTHER project — Yonex racket shop).

## Two projects — don't conflate (L38 + L43 separation rule)

Tuấn Anh runs **2 separate projects**:

| Project | Hub path | Output | Products |
|---|---|---|---|
| **Tuấn Anh Badminton** (Yonex racket shop) | `wiki/projects/tuan-anh-badminton/hub.md` | Facebook content + inventory file | 14+6 = 20 SKU Yonex (vợt + giày + phụ kiện) |
| **Tuấn Anh Review TikTok** (lifestyle/tech review) | `wiki/projects/tuan-anh-review-tiktok/hub.md` | TikTok clips + product scripts | 12+ nhóm sản phẩm (body mist, tripod, ốp Pocket 3, lens, sạc dự phòng, v.v.) |

**Tuấn Anh verbatim feedback (16/07):** *"Tuấn anh review tiktok có nhiều sản phẩm hơn vậy mà"* — when user asks about products in Review TikTok, do NOT limit to `tuan-anh-review-tiktok/products/` folder (which only tracks 2 products with scripts).

## Pitfall #41 (NEW 2026-07-16) — Multi-source enumeration required

**Root cause of 16/07 miss:** Em chỉ đọc `tuan-anh-review-tiktok/hub.md` → thấy "📊 Sản phẩm đã review" table có 1 row (ARMAF) + em liệt kê thêm 1 (Ulanzi MA66) = 2 sp. Sai hoàn toàn — anh có 12 nhóm sản phẩm DISTINCT đã edit.

**Lesson:** Tuấn Anh Review TikTok là content-output project, không phải inventory project. Sản phẩm "có" = sản phẩm đã từng được edit TikTok clip, không phải sản phẩm có file research trong wiki.

## Multi-source enumeration recipe (BẮC BUỘC khi user hỏi "có bao nhiêu sản phẩm?")

**Phải check ≥4 nguồn trước khi trả lời:**

### Source 1: Wiki hub + products/ folder
```bash
ls /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/
ls /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/scripts/
```
- Ưu điểm: Có spec + script chuẩn
- Nhược điểm: KHÔNG đầy đủ — chỉ track sản phẩm đã qua Phase 0 research + viết script

### Source 2: Hermes-Edit output folder (CRITICAL — nguồn chính xác nhất)
```bash
ls /Volumes/Storage-1/Pocket3/Hermes-Edit/*.mp4
```
- Ưu điểm: ĐẦY ĐỦ NHẤT — mỗi clip render = 1 sản phẩm đã edit
- Nhược điểm: Tên file dài, cần parse

### Source 3: Session search (catches products mentioned in conversation)
```bash
session_search(query="clip TikTok edit ARMAF body mist review sản phẩm", sort="newest")
```
- Ưu điểm: Bắt được product mentioned trong Telegram chat nhưng chưa có file wiki
- Nhược điểm: Có thể miss nếu session không match query

### Source 4: worktree output (intermediate state)
```bash
ls /Volumes/Storage-1/Pocket3/Hermes-Edit/tmp/*/
```
- Ưu điểm: Bắt được sản phẩm đang edit dở (chưa ship final)
- Nhược điểm: Tạm thời, có thể đã xóa sau cleanup

## Parse Hermes-Edit filenames — group by category (Python recipe)

```python
import os, re
from collections import defaultdict

he_dir = "/Volumes/Storage-1/Pocket3/Hermes-Edit"

def categorize(name):
    name = name.lower()
    if "body-mist" in name or "amap" in name or "amf" in name or "lemony" in name or "armaf" in name:
        return "🧴 Body Mist (ARMAF/AMAP/AMF/Lemony)"
    if "sac du phong" in name or "sac-du-phong" in name:
        return "🔋 Sạc dự phòng mini gắn iPhone"
    if "but ipad" in name or "goldjordock" in name:
        return "✏️ Bút cảm ứng iPad (Gojodot/Goldjordock)"
    if "but ve sinh" in name or "but lau lens" in name:
        return "🖊️ Bút vệ sinh lens/máy ảnh (K&F)"
    if "lens macro" in name:
        return "🔍 Lens macro K&F (Pocket 3)"
    if "may hut bui doroto" in name or "may hut bui cam tay" in name:
        return "🌀 Máy hút bụi cầm tay Doroto"
    if "op bao ve pocket3" in name or "op pocket3" in name or "kea concept" in name:
        return "🛡️ Ốp bảo vệ Pocket 3"
    if "tripod" in name and ("ulanzi" in name or "1m6" in name or "1m7" in name):
        return "📐 Tripod Ulanzi"
    if "gia do dien thoai" in name:
        return "📱 Giá đỡ điện thoại"
    if "bo ve sinh ong kinh" in name:
        return "🧹 Bộ vệ sinh ống kính"
    if "ngam thao tac" in name or "quick release" in name:
        return "⚙️ Ngàm thao tác nhanh / Quick-release"
    if "den led" in name:
        return "💡 Đèn LED dán tường mini"
    return f"❓ Khác: {name}"

products = defaultdict(list)
for f in sorted(os.listdir(he_dir)):
    if f.endswith(".mp4"):
        products[categorize(f)].append(f)

for cat, files in sorted(products.items(), key=lambda x: -len(x[1])):
    print(f"{len(files):<3} {cat}")
```

**Output verified 16/07/2026:** 12 nhóm sản phẩm DISTINCT, 28 file clips, 55 file .mp4 tổng (bao gồm versions).

## Top products by version count (insight from 16/07)

| Sản phẩm | Versions | Insight |
|---|---:|---|
| Sạc dự phòng mini iPhone | 9 (V1→V9) | Anh iterate nhiều nhất — chốt V9 final |
| Tripod Ulanzi Pocket 3 (deep-dive) | 17 | Khó nhất — clip dài nhiều take |
| Body Mist AMAP line-up | 4 | Multi-variant (thơm mát, tinh tế, Dubai) |
| Tripod Ulanzi (general) | 6 | Across 1m6/1m7/xoay360 |

## Workflow khi anh hỏi "có những sản phẩm gì?"

1. **Đọc wiki hub.md** — get context 2 project
2. **Chạy Python recipe ở trên** — get 12 nhóm DISTINCT
3. **Cross-check session_search** — confirm có sản phẩm nào mentioned nhưng chưa edit clip không
4. **Trả lời với 2 bảng**:
   - Bảng 1: Sản phẩm có wiki track (2 — ARMAF + Ulanzi Tripod Pocket 3)
   - Bảng 2: Sản phẩm đã edit clip (12 nhóm DISTINCT)
5. **Ghi rõ nguồn** — để anh check

## Workflow khi anh muốn enumerate "đã edit xong những clip nào"

```bash
# Đếm tổng clip
ls /Volumes/Storage-1/Pocket3/Hermes-Edit/*.mp4 | wc -l

# Đếm theo tuần (chia đợt)
ls -la /Volumes/Storage-1/Pocket3/Hermes-Edit/*.mp4 | awk '{print $6, $7, $8, $9}' | sort -k1M -k2n -k3
```

## Cleanup binary rule (L34) — khi nào xóa V_old

Theo L34, sau khi V_n ship final → xóa V_old ngay. KHÔNG archive. Cleanup rule:
- Giữ lại file FINAL (tên có "V1" suffix theo convention mới — V1 = FINAL, không phải version 1)
- Xóa các V2/V3/V4/V5 nếu V1 final đã đè lên
- KHÔNG xóa file cùng tên khác version trừ khi V_n accepted as "final"

Verified 14/07: rename V5 → V1 final trong cleanup pass.

## Stub-creation workflow (Pitfall #42 follow-up — NEW 2026-07-16)

Khi anh hỏi option "1" (tạo stub cho sản phẩm chưa track) sau khi enumeration phát hiện 12+ nhóm DISTINCT:

**Input:** danh sách product_meta từ Source 2 (Hermes-Edit) ở trên.
**Output:** N file `.md` stub trong `wiki/projects/tuan-anh-review-tiktok/products/`.

**Stub template xem SKILL.md § "PITFALL #42".** Mỗi stub có:
- Frontmatter với brand + category + edit-count + latest-version
- Bảng metadata từ Hermes-Edit (8 field)
- Bảng files đã render (clip_id + version + size + date)
- Next actions checklist cho Phase 0 research
- Related links tới 2 sp đã có script (reference format)

**Auto-generation bằng Python** (xem code recipe trong SKILL.md § PITFALL #42):
- Parse filenames → extract product slug + version + clip_id + mtime + size
- Map slug → human name + brand + category qua master dict
- Skip nếu đã có trong `wiki/products/`
- Build content từ template, ghi file

**Verified 16/07/2026:** 30 stub files được tạo trong 1 turn (~5 phút Python). Tổng `wiki/products/` = 32 files (2 có script + 30 stub).

**Anti-pattern:** KHÔNG tạo từng file bằng tay. 30 sp × 5 phút = 2.5 giờ thủ công vs 5 phút auto.

## Cross-references

- `physical-product-ecommerce-content/SKILL.md` — Class-level umbrella cho product content
- `references/tuan-anh-badminton-inventory.md` — Companion cho Tuấn Anh Badminton project
- Wiki source: `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/`
- Output: `/Volumes/Storage-1/Pocket3/Hermes-Edit/` (rendered clips)
- L38 (project separation) + L43 (pronoun rule) trong `learned-about-tuananh`

---

*Created 2026-07-16 từ session "Phân tích các nội dung tiktok + lên danh sách sản phẩm". Pattern tái sử dụng: bất cứ khi nào user hỏi "có những sản phẩm gì?" / "đã làm gì rồi?" / "có bao nhiêu version?" — đây là enumeration task, BẮC BUỘC cross-check ≥4 nguồn.*