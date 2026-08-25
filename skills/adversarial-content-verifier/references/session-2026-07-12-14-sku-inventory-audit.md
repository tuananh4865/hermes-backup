# Worked Example — 14-SKU Yonex Inventory Audit (2026-07-12)

## Task Frame

User assigned role: **INDEPENDENT ADVERSARIAL VERIFIER**.

**Author's claim under audit:**
> "Đã lập bảng quản lý 14 SKU Yonex với giá nhập + giá bán đầy đủ. Tổng tiền hàng 37,108,000 VND. Tất cả 14 sản phẩm đều có margin đúng (Play/Tour = 30%, Pro = 12-20%, Giày = 25%). Sẵn sàng cho Tuấn Anh dùng để quản lý kho và content bán hàng."

**Author's evidence:**
- File hint: `products/yonex-specs-reference.md` or `hub.md` (author wasn't sure)
- Note: "đã verify bảng 14 SKU 100% chính xác"

## Step 0 — Apply Pitfall F4 (don't trust author's file path)

```bash
ls -la /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/
# → contains products-inventory.md, hub.md, phase-1-launch.md, content-calendar-30-days.md, astrox-77-facebook-content.md
ls -la /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/products/
# → contains yonex-specs-reference.md, facebook-content-ax77-series.md, facebook-content-templates.md
```

**Finding:** Author suggested `products/yonex-specs-reference.md` or `hub.md`, but the actual 14-SKU table is in **`products-inventory.md`** (root of project, not under `products/`). Lesson: always `ls` and `grep` to locate the real file.

## Step 1 — Layer 1 STRUCTURAL

```bash
wc -l products-inventory.md
# → 58 lines
grep -c "^| [0-9]" products-inventory.md
# → 14 rows (numbered 1-14)
```

**L1 STRUCTURAL: PASS** — File exists, 14 SKU rows present.

## Step 2 — Layer 2 SEMANTIC (4 sub-claims)

### Sub-claim A — Tổng giá nhập = 37,108,000 VND

Re-derived by reading the table and summing the "Giá nhập (VND)" column:

```
1,245,000 + 3,611,000 + 804,000 + 2,057,000 + 2,169,000
+ 1,035,000 + 944,000 + 2,344,000 + 2,319,000 + 2,780,000
+ 4,500,000 + 4,750,000 + 3,950,000 + 4,600,000
= 37,108,000 ✓
```

**Sub-claim A: PASS** — Total cost matches claim exactly (0% deviation).

### Sub-claim B — Đúng 14 SKU, mỗi SKU SL=1

Counted independently via `grep -c "^| [0-9]"`. All 14 rows have `| 1 |` in the SL column.

**Sub-claim B: PASS**.

### Sub-claim C — Margin rule (Play/Tour = 30%, Pro = 12-20%, Giày = 25%)

**This is where Pitfall F1 fired.** For each SKU, computed BOTH formulas:

| # | Tier | Cost | Price | LN | MARGIN (LN/price) | MARKUP (LN/cost) | File's %LN | Formula file used | Rule (strict margin)? |
|---|------|-----:|------:|---:|------------------:|-----------------:|-----------:|-------------------|-----------------------|
| 1 | Play | 1,245,000 | 1,779,000 | 534,000 | 30.02% | 42.89% | 30.0% | MARGIN | YES |
| 2 | Tour | 3,611,000 | 5,159,000 | 1,548,000 | 30.01% | 42.87% | 30.0% | MARGIN | YES |
| 3 | Play | 804,000 | 1,149,000 | 345,000 | 30.03% | 42.91% | 30.0% | MARGIN | YES |
| 4 | Tour | 2,057,000 | 2,939,000 | 882,000 | 30.01% | 42.88% | 30.0% | MARGIN | YES |
| 5 | Tour | 2,169,000 | 3,099,000 | 930,000 | 30.01% | 42.88% | 30.0% | MARGIN | YES |
| 6 | Play | 1,035,000 | 1,479,000 | 444,000 | 30.02% | 42.90% | 30.0% | MARGIN | YES |
| 7 | Play | 944,000 | 1,349,000 | 405,000 | 30.02% | 42.90% | 30.0% | MARGIN | YES |
| 8 | Tour | 2,344,000 | 3,349,000 | 1,005,000 | 30.01% | 42.88% | 30.0% | MARGIN | YES |
| **9** | **Giày** | 2,319,000 | 2,899,000 | 580,000 | **20.01%** | **25.01%** | **25.0%** | **MARKUP** | **NO — FAIL** |
| **10** | **Giày** | 2,780,000 | 3,479,000 | 699,000 | **20.09%** | **25.14%** | **25.1%** | **MARKUP** | **NO — FAIL** |
| 11 | Pro | 4,500,000 | 5,599,000 | 1,099,000 | 19.63% | 24.42% | 19.6% | MARGIN | YES (within 12-20%) |
| 12 | Pro | 4,750,000 | 5,399,000 | 649,000 | 12.02% | 13.66% | 12.0% | MARGIN | YES |
| 13 | Pro | 3,950,000 | 4,549,000 | 599,000 | 13.17% | 15.16% | 13.2% | MARGIN | YES |
| 14 | Pro | 4,600,000 | 5,239,000 | 639,000 | 12.20% | 13.89% | 12.2% | MARGIN | YES |

**Discovery (Pitfall F2 — MIXED FORMULA):** 12 SKU vợt (Play/Tour/Pro) dùng **MARGIN** formula; 2 SKU giày (#9, #10) dùng **MARKUP** formula. Cùng 1 bảng, 2 công thức khác nhau, không có disclosure trong header.

**Strict margin interpretation:** 2 SKU giày fail rule 25% (margin thực chỉ 20%). 2/14 = không đủ ngưỡng ≥3 để auto-FAIL, nhưng vẫn PARTIAL_PASS.

**Sub-claim C: PARTIAL** — Vợt pass; Giày pass NẾU author dùng "margin" theo nghĩa markup nội bộ; FAIL nếu strict interpretation. Công thức không nhất quán trong cùng 1 bảng.

### Sub-claim D — Cross-reference label check (Pitfall F3)

So sánh `products-inventory.md` (cột "Giá nhập") với `products/yonex-specs-reference.md` (cột "Giá bán shop"):

| Model | Inventory "Giá nhập" | Yonex-specs "Giá bán shop" | Same number? |
|-------|----------------------|----------------------------|--------------|
| 99 PLAY | 1,245,000 | 1,245,000 | YES |
| 99 TOUR | 3,611,000 | 3,611,000 | YES |
| ... (all 14) | ... | ... | YES (all 14 identical) |

**Finding:** Cả 14 SKU có CÙNG số liệu trong 2 file nhưng với LABEL khác nhau. Hai khả năng:
- A) inventory's "giá nhập" = cost; yonex-specs's "giá bán shop" bị label SAI (đang hiển thị cost)
- B) ngược lại — yonex-specs là giá bán thật, inventory's "giá nhập" bị label sai

Flag nhưng không block verdict — chỉ arithmetic nội tại của inventory thì đúng (37,108,000 = sum cột "Giá nhập" trong inventory).

## Step 3 — Layer 3 FUNCTIONAL

- Bảng markdown chuẩn (separator `|---|---|---|...|`, số right-aligned) — PASS
- Có cột Tier (Play/Tour/Pro/—) — PASS cho 12 SKU; 2 SKU giày có Tier = "—" (không rõ ràng)
- Cột "% LN" tồn tại nhưng **KHÔNG ghi rõ đây là margin hay markup** → Pitfall F2 firing ngay tại column header

## Step 4 — FAIL-FIRST Hypotheses

| H | Hypothesis | Test | Result |
|---|------------|------|--------|
| H1 | Tổng 37,108,000 có thể sai do copy-paste error | Sum 14 cost values | PASS (khớp 100%) |
| H2 | Số SKU có thể không đúng 14 | `grep -c "^| [0-9]"` | PASS (= 14) |
| H3 | Margin 30% có thể chỉ là target chứ không phải thực tế | Compute (LN/price) × 100 | PASS (30.01-30.03% cho tất cả Play/Tour) |
| H4 | Có SKU nào margin FAIL rule? | Compute per-row | **FIRE** — 2 SKU giày margin thực = 20% nếu strict |
| H5 | File author claim có tồn tại không? | `ls` real path | **FIRE** — file ở `products-inventory.md` chứ không phải `products/yonex-specs-reference.md` như author gợi ý |

## Final Verdict

```
VERDICT: PARTIAL_PASS
L1 STRUCTURAL: PASS — 14 SKU rows present in products-inventory.md
L2 SEMANTIC:
  A) Tổng cost: PASS (37,108,000 chính xác)
  B) Số SKU = 14: PASS
  C) Margin rule: PARTIAL
     - Vợt (12 SKU): PASS — margin thực = 30% đúng
     - Giày (2 SKU): FAIL strict (margin thực = 20% thay vì 25%)
     - INCONSISTENCY: file dùng margin cho vợt, markup cho giày (mixed formula)
L3 FUNCTIONAL: PARTIAL — table format OK, cột "% LN" không ghi rõ margin hay markup
```

**Recommendation to author:**
1. Thêm disclosure vào header: `% LN = LN/giá bán (margin)` hoặc áp dụng nhất quán 1 công thức
2. Nếu muốn strict margin 25% cho giày, tăng giá bán: giày 65z4 cần bán 3,092,000 VND (margin 25%) thay vì 2,899,000 VND
3. Verify file path trong `products-inventory.md` (root) khớp với `yonex-specs-reference.md` (subfolder) — một trong hai có label sai

## Lessons for Future Audits

1. **Always compute BOTH margin and markup formulas** when author claims a %LN — silence on which formula is a red flag, not a green light
2. **Pitfall F2 (mixed formula in same table) is automatic PARTIAL_PASS** even if all numbers internally check out — design flaw, not data flaw
3. **Pitfall F3 cross-reference check** catches mislabeling that arithmetic alone misses
4. **Author's "I verified it 100%" is the strongest signal to verify most aggressively** — overconfidence correlates with skipped checks
5. **The 2-SKU-fail threshold matters**: PARTIAL_PASS (not FAIL) when <3 SKU fail, but still flag and recommend fix — verifier's job is to surface, user decides
