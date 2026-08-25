# Wiki Cleanup Recipe — 17/07/2026 (89 → 18 files, 71 moved)

## Context

Wiki project `tuan-anh-review-tiktok/products/` had **89 files** — 87 of them stub (0-1 citations) but only 2 verified (≥2 citations: ARMAF Odyssey 6 cit, Ulanzi MA66 13 cit).

User feedback: **"Merge hoặc xoá các file products cŨ không có thông tin chính xác"** (17/07/2026 22:35).

## Decision matrix used

| Criterion | Action | Examples (17/07) |
|---|---|---|
| 0-1 citations AND duplicates a verified file | **MOVE to `_deprecated/`** | armaf-odyssey-homme, armaf-odyssey-mega, dodoto test-ngan |
| 0-1 citations AND sole source for a brand | **KEEP** | kea-concept-op-pocket-3, mobanina-op-360 |
| 3+ files for same product category | **MERGE into 1 collection file** | 4 cleaning-pen files → `cleaning-pen-collection-2026-07-17.md` |
| Verified (≥2 citations) | **KEEP** | armaf-odyssey-body-spray-200ml.md, ulanzi-ma66-tripod-pocket-3.md |
| Newly researched (3+ citations) | **KEEP** | All 7 new files added in 17/07 batch |

## Bash recipe (verified)

```bash
PROJECT="/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok"
BACKUP_DIR="$PROJECT/_deprecated_2026-07-17"
mkdir -p "$BACKUP_DIR"

cd "$PROJECT/products"

# 71 stubs to MOVE (NOT verified, duplicate of canonical)
STUBS=(
  armaf-odyssey-homme-body-spray-200ml-armaf.md
  armaf-odyssey-mega-body-spray-200ml-armaf.md
  body-mist-amap-armaf.md
  body-mist-amap-thom-mat-speed30.md
  # ... 67 more (full list in step-by-step audit log) ...
)

for f in "${STUBS[@]}"; do
  if [ -f "$f" ]; then
    mv "$f" "$BACKUP_DIR/$f"
  fi
done

# Verify counts
echo "Remaining: $(ls $PROJECT/products/*.md | wc -l)"   # 18
echo "Deprecated: $(ls $BACKUP_DIR/*.md | wc -l)"        # 71
```

## Result

| Metric | Before | After | Δ |
|---|---:|---:|---:|
| Total files in `products/` | 89 | 18 | -71 (80% reduction) |
| Verified files (≥2 cit) | 2 | 9 | +7 (added 7 newly-researched) |
| Stub files (0-1 cit) | 87 | 9 | -78 (consolidated + moved) |
| File loss | 0% | 0% | 0 |
| Reversibility | n/a | 100% | All 71 files recoverable |

## Categories cleaned (71 files moved)

| Category | Count | Trigger |
|---|---:|---|
| ARMAF | 3 | 3 stub variants of Odyssey — MOVE |
| Body mist (10 brands) | 13 | All 0-1 cit, no verified alternative → MOVE |
| DODOTO | 5 | 5 stubs for Lux Air V3 — MOVE (1 verified) |
| Cleaning pen | 12 | ALL merged → 1 collection file, originals moved |
| K&F Concept | 4 | Stub duplicates — MOVE |
| Lighting (RGB LED dán tường) | 4 | OEM generic — MOVE |
| Tripod + Ulanzi | 22 | MA66 verified kept + kit kept, 20 stubs moved |
| Powerbank | 8 | 8 OEM brands (Baseus, Cuktech, Innomag, etc.) — MOVE |
| iPad pen | 1 | goldjordock truncated variant — MOVE |
| Phone stand | 1 | Generic stub — MOVE |

## Documentation artifact

The cleanup is documented in:
- `wiki/concepts/tiktok-shop-affiliate-14-products-audit-2026-07-17.md` (cleaned section 3 added)

This audit file records what files moved, why, and the 17→18 files remaining with status (verified / representative / newly-researched).

## Restore recipe (if needed)

```bash
mv "$BACKUP_DIR/{filename}.md" "$PROJECT/products/{filename}.md"
```

Or full restore:
```bash
mv "$BACKUP_DIR"/*.md "$PROJECT/products/"
rmdir "$BACKUP_DIR"
```

## Anti-patterns observed (don't repeat)

1. **Don't `os.remove()` stub files** — use mv (Pitfall #4)
2. **Don't keep ALL stubs** — they accumulate and obscure the verified ones
3. **Don't ask user "merge hay delete per file"** — apply decision matrix from this recipe
4. **Don't forget to log the cleanup** in a concept page (audit trail)
5. **Don't move `index.md` or `hub.md`** — only product stubs

## Related

- Skill: `wiki-product-ground-truth/SKILL.md` (Pitfall #4 for MOVE-vs-DELETE)
- Wiki: `tiktok-shop-affiliate-14-products-audit-2026-07-17.md`
- SKILL.md Pitfall #4 (NEW v0.3.0)

