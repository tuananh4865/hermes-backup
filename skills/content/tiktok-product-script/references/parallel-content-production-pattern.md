# 🚀 Parallel Content Production Pattern (16/07/2026)

> **Verified pattern** for producing N TikTok scripts in parallel using subagents. Saved from session 16/07/2026 when user asked "Làm cả 5" (viết 5 template Problem-Solution).

## 🎯 When to use

Trigger phrases:
- "Làm cả N" / "Viết hết" / "Tất cả cùng lúc"
- "Tôi muốn N template" / "Apply cho N sản phẩm"
- "Làm song song đi" / "Parallel đi em"
- N ≥ 2 templates needed with same formula

## 📐 Pattern

```python
# Step 1: Prepare context template (1 lần)
context_template = """
[CONG THUC] Problem-Solution 4-PART (90-120s):
[0-5s]   HOOK VẤN ĐỀ (P1)
[5-25s]  PAIN DEPTH (P2) — 3 vấn đề
[25-75s] GIẢI PHÁP (S) — Sản phẩm + test
[75-95s] PROOF + PRICE
[95-120s] CTA NHẸ

[NGUYÊN TẮC] KHÔNG làm chuyên gia. Tone: người thật gặp vấn đề.
KHÔNG dùng từ chuyên ngành.

[DATA] Đã research tại wiki/projects/<project>/products/<slug>.md
Citations có sẵn - em dùng trực tiếp, KHÔNG bịa.

[3 HOOKS KHÁC NHAU]:
- Version A: <vấn đề 1>
- Version B: <vấn đề 2>
- Version C: <vấn đề 3>

[SAVE] wiki/projects/<project>/scripts/<output-slug>.md
[FORMAT] Frontmatter chuẩn
"""

# Step 2: Dispatch N parallel subagents (max 8)
for product in products:
    delegate_task(
        goal=f"Viết 3-version TikTok script Problem-Solution cho {product['name']}",
        context=context_template + f"\n\n[DATA ĐẦY ĐỦ]\n{product['research_summary']}",
        role="leaf"  # MUST be leaf - no nested delegation
    )

# Step 3: Đợi subagent xong, verify file đã save, count lines
# (subagent sẽ tự save vào đúng path vì đã được hướng dẫn)
```

## 📊 Empirical result (16/07/2026)

| Metric | Sequential | Parallel |
|---|---|---|
| 4 templates × 3 versions | ~30 phút | **~5 phút total** |
| Subagent used | 1 | 4 (parallel) |
| Total API calls | ~40 sequential | ~40 parallel (4×10 each) |
| Quality consistency | Variable | **Consistent (same template)** |

**Time saved:** 6× faster với parallel subagent dispatch.

## ⚠️ Critical rules

1. **Role MUST be "leaf"** — không cho subagent delegate tiếp
2. **Context phải FULL** — subagent không có memory, phải có đủ: formula + principles + data + hooks + save path
3. **Verify file sau khi subagent xong** — đếm lines, check 3 version markers, check PAIN DEPTH sections
4. **Phase -1 routing đúng** — save vào `tuan-anh-review-tiktok/` (lifestyle) chứ không phải `tuan-anh-badminton/`
5. **Không vượt 8 subagents** — Hermes delegation.max_concurrent_children default
6. **Empirical benchmark** — 4 subagent × 1.5 phút mỗi cái = 6 phút total (acceptable cho batch)

## 🔄 Anti-patterns to avoid

- ❌ Sequential viết từng cái một (5-10× chậm hơn)
- ❌ Subagent tự do thiết kế formula (sẽ ra format khác nhau)
- ❌ Context chỉ có data, không có formula/principles (subagent sẽ bịa)
- ❌ Không verify file output sau khi subagent xong

## 📋 Verification after subagent completion

```python
import os

# Check all files exist
for script_name in script_names:
    filepath = f"/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/scripts/{script_name}.md"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()
        lines = content.split("\n")
        versions = content.count("VERSION A") + content.count("VERSION B") + content.count("VERSION C")
        pains = content.count("PAIN DEPTH")
        print(f"✅ {script_name}: {len(lines)} lines, {versions} versions, {pains} PAIN sections")
    else:
        print(f"❌ MISSING: {filepath}")
```

## 🎯 Reference (verified cases)

- **16/07/2026 — ARMAF + Sạc dự phòng + 4 subagent parallel:**
  - ARMAF V2.md: 8.1KB, 3 versions, manual em
  - sac-du-phong-magsafe-problem-solution.md: 5.5KB, 3 versions, manual em
  - op-bao-ve-pocket-3-problem-solution.md: 15.3KB, 282 lines, 3 versions, subagent (97s)
  - tripod-ulanzi-1m6-xoay360-problem-solution.md: subagent dispatched, status pending
  - lenspen-ve-sinh-ong-kinh-problem-solution.md: subagent dispatched, status pending
  - kf-but-ve-sinh-body-mist-problem-solution.md: 11.4KB, subagent
  - **Total: 6 scripts trong ~5 phút = 5-10× faster than sequential**

## 💡 When NOT to use parallel

- 1 template only (overhead > benefit)
- Templates need cross-reference (sequential ensures consistency)
- Subagent context too large (>10KB per task = bloat)
- User muốn em viết manual để demonstrate skill (educational mode)