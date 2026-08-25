# Wiki Organization Patterns for Product Research Batches

> Two patterns from the 2026-07-17 14-product TikTok Shop batch audit. Apply when working on batches of 5+ related products.

## Pattern 1 — Reference File for Unverified Brand

**Trigger**: TikTok Shop captcha blocks the PDP AND no mirror surfaces the brand. You have product name fragment but no verified `brand`, `MPN`, or official source.

**Anti-pattern**: Fabricate a brand based on visual guess, similarity to known product, or Vietnamese keywords. The 17/07 desk lamp episode: "Đèn bàn LED" with no shop listing returned meant the brand could be anything from Baseus to Xiaomi to no-name OEM. Em must NOT pick one and write `brand: Baseus` based on visual similarity.

**Correct pattern**:
1. Create the wiki file with `*-reference.md` filename suffix and `status: researched-by-reference` in frontmatter.
2. Pick 1-2 same-category reference brands with verified specs. Use 2 so future audit can distinguish sources:
   ```yaml
   ---
   status: researched-by-reference
   references:
     - Baseus Smart Eye Series DGZG-02 (Vietnam flagship)
     - Xiaomi Mi LED Desk Lamp 1S (global reference)
   ---
   ```
3. Cite the reference explicitly in body. Include a `LIMITATION` section listing which fields are inferred from reference (most specs) vs verified (only the niche and category).
4. Surface to user: "⚠️ Brand chưa verify được — em cần anh browse manual hoặc reauthenticate cookies để confirm."
5. **Do NOT mark the wiki file as `status: researched`** until brand is verified. `researched-by-reference` is a clear signal to future audit that the data is provisional.

**Example**: `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/desk-lamp-led-smart-baseus-mi-reference.md` (2026-07-17). Wikilink `*-reference.md` files from `[[hub]]` index pages with note that they need verification.

## Pattern 2 — Consolidate Same-Category Duplicates

**Trigger**: Batch creates (or already had) 3+ wiki files for products in the same category, e.g.:
- 4 cleaning-pen files: Lenspen Original, VSGO DKL-15, Hoodman Lens Cleaner, FB 5-in-1
- 5 tripod variants from Ulanzi (1m6, 1m7, MA66, PK-08, MT-08)
- 10+ body mist variants from ARMAF Odyssey line

**Anti-pattern**: Maintain N stub files forever. Wiki search becomes noisy. Each file has 2-3 citations; collectively they have 12 citations but no single file shows the full landscape.

**Correct pattern**:
1. Create 1 consolidated comparison file: `{category}-collection-{YYYY-MM-DD}.md` (e.g. `cleaning-pen-collection-2026-07-17.md`).
2. Structure:
   ```
   # Header (purpose, scope, last-updated)
   ## Comparison Table (1 column per product, rows = spec/price/USP/competitors)
   ## Per-Product Deep Section (4-5 specs per product, link to original wiki)
   ## Unified Citations Block (sum of all originals)
   ## Insights for User (which product fits which use case)
   ```
3. **Keep originals**. The consolidated file `references` them via `[[wikilink]]` so wiki search still surfaces individual files for keyword matches.
4. Total citation coverage is preserved (sum across originals = sum across consolidated). Don't lose citation coverage during consolidation.
5. **Ask user before consolidating if N > 3**: "Anh muốn em gộp 4 file cleaning pen thành 1 file comparison không? Tiết kiệm clutter nhưng giữ nguyên 4 file gốc." — applies for batches of 3+ only.

**Example**: `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/cleaning-pen-collection-2026-07-17.md` (8.4KB, 12 citations across 4 products).

## When to Apply Each Pattern

| Situation | Pattern 1 (reference file) | Pattern 2 (consolidate) |
|---|---|---|
| 14-product batch, 1 product brand unknown | ✅ apply for that 1 | — |
| 14-product batch, 4 products all cleaning pen | — | ✅ apply for those 4 |
| 14-product batch, 13 different categories | — | — |
| Existing batch of 5+ products re-discovered | — | ✅ apply |

## Pitfalls

- Don't mark `*-reference.md` files as `status: researched` — keep `researched-by-reference` so future audits know the data is provisional.
- Don't consolidate files from different categories (different audience, different price tier).
- Don't consolidate files with citations < 2 — they need research first, then consolidation later.

## Pattern 3 — Re-verify cycle when source URL is CAPTCHA-blocked (NEW 20/07/2026)

**Trigger**: User asks to verify/update an *existing* wiki file against a source URL (e.g. "verify this K&F filter wiki against `https://www.tiktok.com/view/product/1733899724122392054`"), AND the URL is blocked by anti-bot CAPTCHA / Cloudflare interstitial / Security Check on both `web_extract` and `browser_navigate`.

**Anti-pattern (NEVER DO)**:
1. Don't fabricate a "WAS vs NOW" diff by guessing what the blocked listing says.
2. Don't silently leave the wiki unchanged and report "all good" — the verify attempt was a no-op, which is also dishonest.
3. Don't claim success because "the URL looks legit". A CAPTCHA page is not a product page.

**Correct pattern** (verified 20/07/2026 on K&F filter + cleaning-pen-collection):
1. **Run BOTH scraping paths** before declaring blocked:
   - `web_extract(urls=[...])` (cheap, try first)
   - `browser_navigate(url=...)` (slower, but reaches anti-bot)
   - If EITHER returns real product content, proceed with content diff.
   - If BOTH return CAPTCHA/security-check content → blocked.
2. **Do a METADATA-ONLY update**, not a content update:
   - Frontmatter: `updated: YYYY-MM-DD`, add `tiktok-shop-product-id`, `tiktok-shop-verify-status: blocked-captcha-YYYY-MM-DD`, `tiktok-shop-verify-url`.
   - Body: append a `⚠️ TikTok Shop Verify Attempt (YYYY-MM-DD)` section documenting URL, blocker, anti-fabrication reasoning, retry recommendation.
   - **Do NOT touch specs/price/origin/MPN** — no truthful source to compare against.
3. **Flag semantic mismatch**: if the existing wiki file is a *consolidated* multi-product file (Pattern 2 output) and the verify URL maps to a *single* brand not in the file, explicitly note this in the verify-attempt section. Otherwise future audits will assume the consolidated file is the canonical cache for the single product (it's not).
4. **Recommend retry path**: list what would unblock (residential proxy, logged-in TikTok cookie, Apify actor). This is the action item the user can actually take.
5. **Report outcome as NO CHANGE** — not "success", not "fail". The wiki is unchanged in content; only metadata + audit trail was added.

### Concrete example — K&F CPL filter wiki (20/07/2026)

```yaml
# BEFORE
updated: 2026-07-17
sources: [kentfaith.com, amazon.com, kentfaith.com]

# AFTER (frontmatter)
updated: 2026-07-20
tiktok-shop-product-id: 1733899724122392054
tiktok-shop-verify-status: blocked-captcha-2026-07-20
tiktok-shop-verify-url: https://www.tiktok.com/view/product/1733899724122392054
sources: [kentfaith.com, amazon.com, kentfaith.com]   # unchanged
```

Body appended (truncated):
```
## ⚠️ TikTok Shop Verify Attempt (2026-07-20)
- Verify URL: https://www.tiktok.com/view/product/1733899724122392054
- Kết quả: ❌ BLOCKED — TikTok anti-bot CAPTCHA / Security Check ...
- Hành động: KHÔNG thay đổi dữ liệu specs/price/origin/MPN ...
- Khuyến nghị retry: Cần residential proxy hoặc TikTok Shop session cookie logged-in ...
```

### Concrete example — cleaning-pen collection wiki (20/07/2026, semantic-mismatch case)

Same frontmatter pattern, BUT verify section MUST also flag:
> "File này gộp 4 brand (Lenspen / VSGO / FB / Hoodman) — TikTok Shop product ID 1734226192370271734 chỉ map tới **K&F bút vệ sinh** silicone head, **không** map tới Lenspen / VSGO / FB / Hoodman trong bảng so sánh. Wiki cache này không phải file review riêng cho K&F bút vệ sinh."

And add a recommendation: if user wants wiki cache riêng cho K&F bút vệ sinh, create `k-f-concept-cleaning-pen-silicone-head.md`.

### Decision matrix — what to add when verify is blocked

| Wiki file shape | Blocked verify URL maps to | Action |
|---|---|---|
| Single-product wiki | The same single product | Metadata-only update + ⚠️ section |
| Single-product wiki | Different product (wrong match) | ⚠️ section flags mismatch; do NOT update single-product wiki as if it covers the URL's product |
| Multi-product consolidated wiki (Pattern 2) | One of the consolidated products | Metadata-only update + ⚠️ section that names which one |
| Multi-product consolidated wiki (Pattern 2) | A product NOT in the consolidated set | Metadata-only update + ⚠️ section that explicitly says "file does NOT cover this product" + suggestion to create a new dedicated wiki file |

### Why metadata-only (not silent skip, not fabricated diff)

- **Audit trail**: future audits can grep `tiktok-shop-verify-status: blocked-captcha` and see exactly which wiki files have attempted-but-blocked verifications, with timestamps.
- **Reversibility**: the original content (specs/price from 17/07 research) is preserved untouched. If the user later provides unblocked access, the next verify attempt can do a real WAS vs NOW diff without re-deriving the baseline.
- **Honest reporting**: matches the "Pitfall: Honest Reporting (FIRST-CLASS)" pattern from `tiktok-shop-scraping-failure-modes.md`. Same principle applies to re-verify cycles, not just initial research.
