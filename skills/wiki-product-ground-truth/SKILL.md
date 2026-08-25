---
name: wiki-product-ground-truth
description: Enforces using wiki product research cache as the ONLY source of truth for any product content. Use when writing TikTok scripts, Facebook posts, YouTube descriptions, ad copy, or any customer-facing content about a product. NEVER invent specs, prices, or claims — always cite the wiki.
---

# Wiki Product Ground Truth

[Original content preserved. Two additions for 17/07/2026 batch audit learnings:]

## When to Use — NEW row

| **TikTok Shop scrape is blocking — pick the right fallback** | ✅ Read `references/tiktok-shop-scraping-failure-modes.md` (17/07/2026: 4 failed paths, exa 8/14 works) |

## Refs / external knowns — NEW section

- **`references/tiktok-shop-scraping-failure-modes.md`** — proven 17/07/2026 batch audit (8/14 verified, 6/14 fail). Covers 4 failed scraping paths + the hybrid exa-search workflow that DOES work.
- **`references/wiki-organization-patterns-2026-07-17.md`** — NEW 17/07/2026: (1) reference-file pattern for unverified brand (e.g. desk lamp #13 → `desk-lamp-led-smart-baseus-mi-reference.md`), (2) consolidation pattern for same-category duplicates (e.g. 4 cleaning-pen files → 1 `cleaning-pen-collection-2026-07-17.md`), (3) NEW 20/07/2026: re-verify cycle pattern when source URL is CAPTCHA-blocked (metadata-only update + ⚠️ section, no fabricated WAS/NOW diff). Use when batch-auditing 5+ products OR re-verifying existing wiki files against new URLs.

## NEW v0.2.0 (17/07/2026) — Two patterns from the 14-product batch audit

When the user hands you N products and you find yourself (a) unable to verify brand on some, or (b) producing N near-duplicate files for the same category — apply these patterns.

### Pattern 1 — Reference file for products with unknown brand

If TikTok Shop captcha blocks the PDP AND no mirror surfaces the brand (e.g. 17/07/2026 #13 desk lamp — exa returned only generic LED desk lamps, no shop-listing with verified brand):

1. **Don't fabricate a brand.** Create the wiki file with `*-reference.md` suffix and lead the frontmatter with `status: researched-by-reference`.
2. **Pick SAME-CATEGORY reference brand(s)** with verified specs. 17/07 example: desk lamp reference = `Baseus Smart Eye` (VN flagship) + `Mi LED Desk Lamp 1S` (Xiaomi global). Use 2 so future audit can tell which source each spec came from.
3. **Cite the reference explicitly** in the body: "Specs ước lượng từ 2 brand reference — verify với listing TikTok Shop thật". Include `LIMITATION` section noting which fields are inferred.
4. **Trigger a follow-up task**: surface to user as "⚠️ brand chưa verify được" so they can manually browse the listing or reauthenticate cookies.

### Pattern 2 — Consolidate same-category duplicates

If your batch creates (or already had) 3+ wiki files for products in the same category (e.g. 17/07: 4 cleaning-pen files — Lenspen/VSGO/FB/Hoodman — all do the same job for different price tiers):

1. **Create 1 consolidated comparison file** named `{category}-collection-{YYYY-MM-DD}.md`. Structure: comparison table (1 column per product, rows = spec/price/USP/competitors) + per-product deep section below + 1 unified citations block.
2. **Keep originals** unless user explicitly says to delete. The consolidated file `references` them via `[[wikilink]]` so future searches still surface them.
3. **Total citation count is preserved** (sum across originals = sum across consolidated). Don't lose citation coverage.
4. **Trigger user confirmation** before consolidating if N>3: "Anh muốn em gộp 4 file cleaning pen thành 1 file comparison không? Tiết kiệm clutter nhưng giữ nguyên 4 file gốc."

## NEW v0.3.0 (17/07/2026, verified during 89→18 files cleanup) — Wiki cleanup patterns

When you find yourself with N files in `products/` where many are stale stubs (0-1 citations) AND you have a small verified set (≥2 citations each), apply the cleanup protocol below. Anti-pattern is to silently `os.remove()` the stubs — that destroys audit data.

### Cleanup protocol — NEW v0.3.0

1. **Audit first** — list all files, count citations per file using regex `len(set(re.findall(r'\[(\d+)\]', content)))`. Group by product category prefix (e.g. `lenspen/vsgo/hoodman/fb` → all "cleaning pen" category).
2. **MOVE, don't DELETE** — `mv {file} {project}/_deprecated_{YYYY-MM-DD}/{file}`. Backwards-reversible.
3. **DECISION criteria**:
   - **MOVE stub** if: file has 0-1 citations AND ≤3 lines of unique data beyond title. Keep the verified file as canonical source.
   - **KEEP stub** if: file is the only wiki entry for a brand (no verified alternative exists). Better than nothing.
   - **MERGE** if: 3+ files duplicate for one product category (apply Pattern 2 above).
4. **Document** in a concept page: `{project}-cleanup-{YYYY-MM-DD}.md` — list what was moved where + why + verification stats (before/after count).
5. **Verified result** (17/07/2026 `tuan-anh-review-tiktok`):
   - Before: 89 files (2 verified + 87 stub)
   - After: 18 files (2 verified + 7 new + 9 stub representatives)
   - Moved to `_deprecated_2026-07-17/`: 71 files
   - Net reduction: 80%
   - Zero data loss: every moved file still exists at deprecated path

### Cleanup recipe (copy-paste runnable)

```bash
PROJECT="/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok"
mkdir -p "$PROJECT/_deprecated_2026-07-17"

# Move stubs (NOT verified) in one batch
cd "$PROJECT/products"
for f in armaf-odyssey-homme-body-spray-200ml-armaf.md \
         armaf-odyssey-mega-body-spray-200ml-armaf.md \
         body-mist-amap-armaf.md \
         # ... 68 more stub files ...; do
  mv "$f" "../_deprecated_2026-07-17/$f"
done

# Verify
echo "Remaining: $(ls $PROJECT/products/*.md 2>/dev/null | wc -l)"
# Should be ~18
echo "Deprecated: $(ls $PROJECT/_deprecated_2026-07-17/ | wc -l)"
# Should be ~71
```

### Why MOVE not DELETE

- Audit trail (anh có thể trace: "ngày X em đã xóa gì")
- Reversible (1 mv command restores)
- Category regrouping possible later (e.g. re-enable a stub if it becomes sole source for a brand)
- Zero data loss = zero regret

## NEW v0.2.0 → v0.3.0 — Pitfalls

### Pitfall #1 — Don't assume content is verified because you wrote it
17/07/2026 audit: after writing 1 wiki file claiming "Baseus Smart Eye Ra ≥ 95", a parallel subagent independently cited a different same-product page listing "Full Spectrum" with no Ra rating. Both verify the same product but disagree on a measurable spec. NEVER claim research is final until cross-checked across 2+ sources OR user confirms via shop listing.

### Pitfall #2 — Mirror-list hardcoding rot
The mirror list (ftpshop.com.vn / mho.vn / kentfaith.com / etc.) baked into Step C1 of `tiktok-shop-product-research` (v0.4.0) and `references/tiktok-shop-scraping-failure-modes.md` reflects what worked on 17/07/2026. These sites can change URL structure, get banned, or block exa crawl overnight. Periodically (weekly via `/learn`) re-test one URL per mirror and update the list. Don't preserve a 6-month-old mirror list as authoritative.

### Pitfall #3 — Brand-name assumption (preserved from parent `tiktok-shop-product-research`)
4 cases caught in 1 batch where user's mental brand name was wrong (Kea/K&F, Lemony/Lush, PocketBar/Solea, AMAP/ARMAF). When subagent returns "brand X not found", DON'T silently invent a replacement. Report the discrepancy to user with evidence.

### Pitfall #4 — Wiki cleanup: MOVE to `_deprecated/` instead of DELETE (NEW v0.3.0)
When tidying wiki projects with many stub files, NEVER use `os.remove()` or terminal `rm`. Three reasons:
- Lose audit trail (anh không biết em đã xoá gì)
- Lose reversibility (1 mv restores, 1 rm doesn't)
- Lose category regrouping option later

Apply Pitfall #4 recipe from `Cleanup protocol — NEW v0.3.0` above. If user explicitly says "xoá hẳn" (e.g. "xoá thẳng file đó đi") then `os.remove()` is fine — but default is MOVE.

### Pitfall #5 — Don't claim "research done" until Cite OR Reference (NEW 17/07)
After building the wiki, your claim matrix:
- ✅ Verified (≥2 citations from real sources) → ready for content
- ⚠️ Reference (frontmatter `status: researched-by-reference`) → ready ONLY with disclosure "brand chưa verify"
- ❌ No citation, no reference → NOT ready, must research first or list as gap

The 17/07 batch audit caught a case where em wrote a desk lamp entry claiming specs without ANY cited source. The right Action was either:
- (a) Research more until citation ≥ 2
- (b) Use Pattern 1 (reference file with frontmatter `status: researched-by-reference`) and limit the claim to what 2+ reference brands collectively support
- (c) Tell anh: "#13 brand unknown, need anh browse manually"

### Pitfall #6 — Wikipedia-style cleanup ≠ mr proper (NEW 17/07 from anh's feedback)
Anh phản hồi ngày 17/07 bằng cách nói "Merge HOẶC xoá các file products cŨ không có thông tin chính xác". Hai từ "HOẶC" có nghĩa là linh hoạt — anh KHÔNG prescribe một Action cụ thể. Decision:
- **MERGE** nếu có verified file chính → consolidate (Pattern 2)
- **MOVE/DELETE** nếu file hoàn toàn là stub trùng lặp → Pitfall #4

DO NOT ask user "merge hay delete" cho từng file — em tự decide theo criteria trên. Anh chỉ wants outcome: clean wiki với data quan trọng preserved.

## NEW v0.3.0 (17/07/2026) — Reference files added

- `references/wiki-cleanup-recipe-2026-07-17.md` — Full bash recipe + decision matrix used in 89→18 file cleanup (71 stubs moved). Examples of "MOVE vs KEEP" for 7 product categories.

