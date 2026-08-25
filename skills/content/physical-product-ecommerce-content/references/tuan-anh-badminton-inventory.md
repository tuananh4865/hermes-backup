# Tuấn Anh Badminton — Inventory Update Workflow

> **Reference file.** Companion to `physical-product-ecommerce-content` SKILL.md. Read this BEFORE updating `products-inventory.md` (the canonical source of truth for SKUs, prices, margins).

## File location (canonical)

```
/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/products-inventory.md
```

Single source of truth. NEVER duplicate SKU/pricing data elsewhere. Every Facebook content draft, every margin call, every "top LN" reference MUST trace back to this file.

## File structure (must follow)

```
---
title: Products Inventory — Tuấn Anh Badminton
created: YYYY-MM-DD
updated: YYYY-MM-DD         ← BUMP EVERY UPDATE
type: project
tags: [project, inventory, badminton, yonex]
confidence: high
relationships: [hub, content-calendar-30-days, phase-1-launch]
---

# Bảng Quản Lý Sản Phẩm — Tuấn Anh Badminton

> Cập nhật: YYYY-MM-DD. Nguồn: <ảnh đơn hàng NCC>.

## Bảng <N> SKU đầy đủ              ← INITIAL TABLE (preserved as-is)
| # | Sản phẩm | Tier | SL | Giá nhập (VND) | Giá bán (gạch) | LN/SP | % LN |
| ... |

## Ghi chú quan trọng                ← PRESERVED across updates
### Về giá
### Cảnh báo kho
### Top 3 biên tuyệt đối

## Đợt nhập YYYY-MM-DD — Hàng mới    ← APPEND NEW SECTION PER BATCH
| # | Sản phẩm | Tier | SL | Giá nhập | Giá bán | LN/SP | % LN |
| ... |

### Tổng hợp sau N đợt               ← CỘNG DỒN toàn kho (số SKU, tổng vốn, tổng LN dự kiến)
### Ghi chú đợt này                  ← New SKU insights, size warnings, upsell hooks
### Top LN tuyệt đối toàn kho (sau đợt N) ← Update ranking

## Tracking bán hàng (cập nhật khi có đơn)
```

**Why this structure:** Initial table is immutable history (per-batch proof). Append per-batch section so đợt 1 / đợt 2 / đợt N are independently auditable. Cộng dồn số liệu toàn kho ở ngay sau batch table.

## Update workflow (5 bước BẮT BUỘC)

### Bước 1: ĐỌC ẢNH CẨN THẬN
- Anh gửi ảnh đơn hàng nhập → parse theo format chuẩn:
  - **Giá nhập** = số đầu tiên (giá vốn NCC)
  - **Giá bán** = số bị **gạch ngang** (strikethrough) dưới giá nhập (anh đã gạch giá cũ → ghi giá bán mới)
  - **SL** = cột số lượng
- ⚠️ **Verify bằng tổng tiền hàng** ở cuối ảnh (anh hay in ra, dễ check): tổng vốn các dòng = tổng tiền hàng trong ảnh. Nếu sai → hỏi lại TRƯỚC khi ghi.

### Bước 2: ĐỌC FILE INVENTORY HIỆN TẠI
- **ĐỌC TOÀN BỘ** (`read_file` không pagination) trước khi patch.
- Note: file hiện có bao nhiêu SKU, có bao nhiêu section "Đợt nhập", comment đặc biệt nào.

### Bước 3: PATCH FRONTMATTER (updated date + dòng "Cập nhật")
```yaml
updated: YYYY-MM-DD     ← BUMP
```
```markdown
> Cập nhật: YYYY-MM-DD. Nguồn: <mô tả ngắn nguồn ảnh>.
```

### Bước 4: APPEND SECTION ĐỢT MỚI (KHÔNG sửa bảng cũ)
- Dùng `patch` với `old_string` đủ context để unique (KHÔNG match nhầm vào heading khác).
- Section gồm:
  - Bảng SKU mới (cột giống bảng gốc)
  - Row TỔNG ĐỢT (tổng SL + vốn + bán + LN + % LN)
  - Subsection "Tổng hợp sau N đợt" — số SKU cộng dồn + tổng vốn + tổng LN dự kiến
  - Subsection "Ghi chú đợt này" — insights riêng (size hiếm, sản phẩm mới cần content, warning size tồn)
  - Subsection "Top LN tuyệt đối toàn kho" — ranking cập nhật

### Bước 5: VERIFY (BẮT BUỘC trước khi báo xong)
```bash
wc -l products-inventory.md                          # dòng tăng đúng ~25-30
grep -c "^|" products-inventory.md                  # số rows tăng đúng ~7 (6 SKU + 1 TỔNG)
grep "^##" products-inventory.md                     # section headers đầy đủ
```
- Nếu `### Về giá` heading bị mất → **RESTORE NGAY** (Pitfall #1 dưới đây).
- Báo cáo cho anh dạng bảng 6 cột ngắn gọn (anh đọc trên điện thoại).

## PITFALLS (đã fail thật)

### Pitfall #1: Patch xóa nhầm heading `### Về giá`
- **Symptom:** Dùng `old_string` match quá ngắn → `patch` xóa luôn heading subsection.
- **Reproduce:** Session 2026-07-12, em patch từ "## Ghi chú quan trọng\n\n### Về giá\n..." → match 2 chỗ → xóa nhầm heading.
- **Fix:** Restore ngay bằng patch lại. Lesson: luôn `read_file` toàn bộ file trước khi patch để biết chính xác context cần match.
- **Prevention:** Dùng `replace_all=False` (mặc định) + đủ 3-4 dòng context trong `old_string` để chỉ match 1 chỗ duy nhất.

### Pitfall #2: Patch fail "Found 2 matches" — old_string không unique
- **Symptom:** `patch` báo "Found 2 matches" khi section đã có 1 lần rồi + em cố patch thêm 1 lần nữa.
- **Fix:** Đọc file xem đã patch trước đó chưa. Nếu rồi → chỉ patch 1 lần duy nhất. Nếu chưa → thêm context để `old_string` unique.

### Pitfall #3: Quên bump `updated` trong frontmatter
- **Symptom:** Nội dung thay đổi nhưng `updated` vẫn date cũ → downstream tooling (nightly curator, content calendar) pick up sai mtime.
- **Fix:** Luôn bump `updated: YYYY-MM-DD` ở Bước 3, song song với dòng "Cập nhật:" trong body.

### Pitfall #4: Quên ghi "Ghi chú đợt này"
- **Symptom:** Append bảng xong → ship → 1 tuần sau anh hỏi "size 37 này từ đợt nào?" → mò không ra.
- **Fix:** Bước 4 PHẢI có subsection "Ghi chú đợt này" với: SKU mới đáng chú ý, size hiếm, biên cao/thấp, insight để lên content kế tiếp.

### Pitfall #5: Tổng tiền hàng trong ảnh ≠ tổng parse thủ công
- **Symptom:** Em parse 6 dòng → tính tổng X. Nhưng ảnh in tổng = Y ≠ X.
- **Fix:** Bước 1 PHẢI đối chiếu tổng tiền hàng ảnh với tổng tính thủ công. Sai → hỏi anh TRƯỚC khi ghi file (đừng assume sai số).

### Pitfall #6: Ghi Tier cho giày/phụ kiện = sai
- **Symptom:** Tier Play/Tour/Pro chỉ dành cho vợt. Ghi tier cho giày / tất / phụ kiện = confusing.
- **Fix:** Tier cho giày, tất = "—" (em-dash). Hoặc tạo tier riêng "Phụ kiện" nếu shop phát triển.

### Pitfall #7: Tất/phụ kiện nhỏ — KHÔNG chia unit thành "chiếc"
- **Symptom:** Em tự ý chia `49,000đ/đôi` thành `24,500đ/chiếc` rồi tính LN "1 chiếc bán 60K → LN 59%". Sai hoàn toàn — anh bán CẢ ĐÔI/CẢ BỘ, không bán lẻ 1 chiếc.
- **Tuấn Anh verbatim feedback (12/07):** *"Tất thì bán cả đôi chứ ai bán 1 chiếc đâu má"*
- **Reproduce:** Session 12/07, em tự ý ghi "Tất MP9 = 1 chiếc giá 60K → LN/SP 35,500 (59.2%)". Anh flag ngay. Em phải fix lại thành "1 đôi giá 60K → LN/SP 11,000 (18.5%)".
- **Fix:** Mọi phụ kiện nhỏ (tất, quấn cán, grip, dây cước) anh bán theo ĐÔI/BỘ. KHÔNG chia unit. Nếu NCC ghi "49,000đ" mà không rõ "/đôi" hay "/chiếc" → HỎI ANH trước khi ghi.
- **Verification:** Trước khi ship bất kỳ row tracking nào có "tất/quấn cán/grip/band", grep `1 chiếc` trong section tracking. Nếu có → fix.

### Pitfall #8: Khôi phục SL tracking = KHÔNG chỉ trừ 1, mà ghi rõ "đã bán"
- **Symptom:** Cập nhật SL trong bảng SKU = 0 nhưng KHÔNG ghi rõ lý do → sau này không biết tại sao SL=0 (bán hết? NCC giao thiếu? lỗi ghi?).
- **Fix:** Format chuẩn khi cập nhật SL: `0 (đã bán 12/07)` hoặc `19 (đã bán 1 đôi 12/07)`. Đính kèm date để trace.
- **Verify:** Sau khi update, mỗi SKU có SL < giá trị ban đầu PHẢI có ghi chú (date + lý do).

### Pitfall #9: Quên update "Tổng hợp sau N đợt" sau khi bán
- **Symptom:** Append tracking row, fix SL trong bảng SKU, nhưng KHÔNG cập nhật lại "Tổng hợp sau 2 đợt" (vốn còn lại, LN đợt bán, LN dự kiến toàn kho). Số liệu bị stale.
- **Fix:** Sau khi append tracking row → tính lại ngay:
  - Vốn còn lại = Vốn cũ - vốn hàng đã bán
  - Doanh thu đợt = Σ giá bán thật các row mới
  - LN đợt = Doanh thu - Σ vốn hàng đã bán
  - LN dự kiến toàn kho (chưa bán) = Σ (LN/SP × SL còn) của tất cả SKU
- **Verify:** `grep "Vốn còn lại\|Doanh thu đợt bán\|LN đợt bán\|LN dự kiến toàn kho" products-inventory.md` → 4 dòng, đồng bộ với tracking rows.

## Tracking bán hàng workflow (Bước 4b — khi anh báo "note vào sổ thu chi")

### Trigger
Khi anh nói "vừa bán X", "note vào sổ", "update tracking", "ghi bán hàng" → vào thẳng workflow tracking (không qua lại bước 1-3 batch update).

### Steps

1. **Đọc file inventory hiện tại** (`read_file` toàn bộ, không pagination).
2. **Tìm section "## Tracking bán hàng"** → biết format row hiện tại.
3. **Patch 4 chỗ ĐỒNG THỜI** (Pitfall #9 — đừng quên 1):
   - **a)** Bảng SKU: giảm SL của SKU bán, ghi `SL (đã bán DD/MM)` (Pitfall #8)
   - **b)** Update "Tổng hợp sau N đợt": số SKU còn lại, vốn còn, doanh thu đợt, LN đợt, LN dự kiến
   - **c)** Update "Top LN tuyệt đối toàn kho" — loại SKU đã hết khỏi ranking
   - **d)** Append row mới vào tracking table (format xem dưới)
4. **Tính LN từng row bằng Python** (KHÔNG tính tay):
   ```bash
   python3 -c "
   gia_ban = 3050000
   gia_von = 2780000
   ln = gia_ban - gia_von
   print(f'LN = {ln:,} đ (margin {ln/gia_ban*100:.1f}%)')"
   ```
   HARD RULE — mọi row tracking PHẢI có LN tính bằng script, không estimate.
5. **Verify** bằng `grep` + đếm row tracking.

### Format row tracking (BẮC BUỘC)

```
| Ngày bán | Sản phẩm | SL | Giá bán thật | Khách | LN/SP | Tổng LN | Ghi chú |
| YYYY-MM-DD | <Tên đầy đủ SKU> | <Đơn vị rõ ràng> | <Giá bán thật> | <Mô tả> | <LN/SP> | <SL × LN/SP> | <Context: giá gạch, lý do giảm giá, bundle, etc.> |
```

**Đơn vị SL phải rõ:** "1", "1 đôi", "1 chiếc", "2 đôi", etc. KHÔNG chỉ ghi số trần.

**Ghi chú bắt buộc cho mỗi row:**
- Giá bán thật vs giá gạch (nếu anh giảm giá để chốt nhanh)
- Bundle (khách mua kèm cái gì)
- Lý do giảm giá (nếu có)
- Tier khách (nữ, nam, người mới, người chơi lâu năm)

### Row TỔNG (cuối tracking table)

```
| | **TỔNG ĐỢT BÁN <DATE>** | **<Tổng SL>** | **<Tổng doanh thu>** | | | **<Tổng LN>** | **<margin %>** |
```

### Subsection phân tích (khuyến nghị)

Sau row TỔNG → `### Phân tích đợt bán <DATE>` gồm:
- ✅ Điều tốt (bán được gì, tier nào hot)
- ⚠️ Cảnh báo (giảm giá bao nhiêu %, mất bao nhiêu LN kỳ vọng)
- 💡 Bài học (flexibility về giá, nhập thêm size nào)
- 🎯 Action cho lần sau (nhập thêm SKU, đẩy content tier nào)

### Insight quan trọng: "Giảm giá để chốt nhanh"

Khi anh báo "bán X giá Y" mà Y < giá gạch trong bảng → PHẢI ghi chú và so sánh LN thực vs LN kỳ vọng:
- LN kỳ vọng = (giá gạch - giá vốn)
- LN thực = (giá bán thật - giá vốn)
- Delta = LN kỳ vọng - LN thực (anh đã "mất" bao nhiêu LN để chốt nhanh)

Đây là data point quan trọng để anh quyết định pricing strategy dài hạn. Nếu thường xuyên phải giảm 10-15% giá gạch để bán → có thể cần điều chỉnh giá gạch thấp hơn ngay từ đầu (margin 25% thay vì 30%).

## Verify recipe (sau mỗi update)

```bash
# 1. File tồn tại + đúng path
ls -la /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/products-inventory.md

# 2. Số rows tăng đúng (mỗi batch +1 row cho mỗi SKU mới + 1 row TỔNG ĐỢT + 1 row trống)
grep -c "^|" products-inventory.md

# 3. Section "### Về giá" còn nguyên
grep -c "^### Về giá$" products-inventory.md    # phải = 1

# 4. Frontmatter updated date đúng hôm nay
grep "^updated:" products-inventory.md

# 5. Không có duplicate SKU ID (giả định SKU id liên tục)
# ID phải liên tục: đợt 1 = #1-14, đợt 2 = #15-20, đợt 3 = #21-...
grep -oP "^\|\| \d+ " products-inventory.md | sort -u | wc -l
```

## Output format khi báo cho anh

Sau khi update xong → báo cáo theo format bảng 6 cột ngắn (anh đọc trên Telegram điện thoại):

```
| # | Sản phẩm | SL | Nhập | Bán | LN | % |
```

Cuối báo cáo: dòng **TỔNG ĐỢT** + dòng **TỔNG KHO SAU N ĐỢT** + 1-2 insight ngắn (size hiếm, biên cao nhất, SKU cần content push).

KHÔNG dài dòng. KHÔNG lặp lại table markdown đầy đủ (anh đã thấy file). CHỈ báo cáo verify facts + insight.

## Cross-references

- `physical-product-ecommerce-content/SKILL.md` — Content writing skill cho product
- `references/yonex-shoe-specs.md` — Specs giày Yonex (subaxi GT, 65 Z4, VELO 300)
- `references/yonex-series-classification.md` — Series target mapping (88S vs 88D vs 99 vs ArcSaber 11 vs AX77)
- Wiki source: `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/products-inventory.md`

---

*Created 2026-07-12 từ session update inventory đợt 2 (VELO 300 + Subaxia Limited + tất MP9). Pattern tái sử dụng cho MỌI lần anh gửi ảnh đơn hàng nhập mới.*

*Updated 2026-07-12: Thêm Tracking bán hàng workflow (Bước 4b) + Pitfall #7-9 từ session anh báo "hôm nay bán 2 đôi subaxia + 1 tất". Verified workflow 4 chỗ patch đồng thời (SKU table SL + Tổng hợp sau N đợt + Top LN ranking + tracking row). HARD RULE mới: tính LN bằng Python script, KHÔNG estimate.*