# Canonical DEFAULT CONFIG Pattern (added 2026-07-18)

> **Status:** Reusable methodology for promoting a per-clip-verified value (e.g. V22 verified 0.15 opacity) to a skill-class DEFAULT (e.g. 0.18 opacity).
> **First-class example:** DEFAULT opacity = 0.18 added 18/07/2026. See SKILL.md section `## 🔴 PIP CROPPING PATTERN FOR TIKTOK VERTICAL (added 2026-07-18, FIRST-CLASS)` → `### 8 DEFAULT VALUES` table.

## Why this pattern exists

When anh says "đặt default opacity thành 0.18", em đừng chỉ đổi một số trong recipe. Em phải đặt nó thành **canonical** cho toàn bộ skill class — có nghĩa là 6 thứ sau phải có MỘT CÁCH NHẤT QUÁN:

1. DEFAULT VALUES table (công thức copy-paste)
2. Canonical Recipe block (code mẫu dùng default values)
3. Lịch sử thay đổi (giữ old value làm reference, KHÔNG xóa)
4. Khi nào dùng override (guidance for per-clip override)
5. Anti-pattern table updated (cả "quá trong" và "quá đục" đều correct back to default)
6. Cross-reference pointers (từ references/ về SKILL.md và ngược lại)

Không có đủ 6 phần → default KHÔNG thực sự canonical, future sessions sẽ confused.

## 8-step pattern (copy-paste cho mọi lần default-promotion)

### Bước 1 — Cite anh's explicit request verbatim

Ở đầu section trong SKILL.md, ghi rõ câu verbatim của anh:

```markdown
**Anh yêu cầu:** "Đặt độ trong mặc định thành 0.18"
```

KHÔNG paraphrase. Future session cần search "độ trong mặc định 0.18" thì phải tìm thấy đúng câu của anh.

### Bước 2 — State the rule

```markdown
**Rule:** Mọi clip dọc TikTok dùng DEFAULT CONFIG này trừ khi anh override rõ ràng.
```

Scope rõ ràng: "mọi clip dọc TikTok" = which clips are bound by this default.

### Bước 3 — 8 DEFAULT VALUES table

```markdown
### 8 DEFAULT VALUES (liquid glass + typography):

| Property | Default V7.2 (18/07/2026) | Override allowed |
|---|---|---|
| **opacity** | **0.18** (dày hơn 0.15, mờ nhám rõ) | ✅ Override nếu anh muốn 0.15 (V22 verified) hoặc 0.20 |
| padding | 40px 36px | ✅ Override |
| ... |
```

Rules:
- First row = property being changed (bold + "Default" cell bold)
- "Override allowed" column explicit = ✅ Override with concrete alternatives
- 8 rows = full scope of DEFAULT (anh đã chọn 8 = same as 8 HARD RULES V7.1)

### Bước 4 — Canonical Recipe block (copy-paste ready)

```markdown
### Canonical Recipe (copy-paste cho mọi clip):

```css
.phase-glass {
  ...
  background: rgba(255, 255, 255, 0.18);     /* DEFAULT 0.18 */
  ...
}
```
```

Block phải dùng default values, không hardcode. Comment inline đánh dấu `/* DEFAULT 0.18 */` để future readers thấy ngay.

### Bước 5 — Lịch sử thay đổi (preserve old values)

```markdown
### Lịch sử thay đổi opacity (cho reference):

| Version | Opacity | Trạng thái |
|---|---|---|
| V22 (case study verified) | 0.15 | Verified PASS bằng mắt thật — giữ làm reference |
| V7 (motion upgrade) | 0.18 | Nâng lên vì anh feedback "trong suốt quá" |
| **V7.2 (current default)** | **0.18** | **DEFAULT cho mọi clip mới** |
```

CRITICAL: KHÔNG xóa V22 row dù 0.15 không còn là default. Lý do:
- Old clips đã verify với 0.15 — rollback reference
- Override decisions ("khi nào dùng 0.15") cần historical context
- Anh có thể A/B test giữa 0.15 và 0.18

### Bước 6 — Khi nào dùng override guidance

```markdown
### Khi nào dùng 0.15 thay vì 0.18:

- Anh explicit nói "dùng 0.15 như V22"
- Clip có background quá phức tạp cần glass trong hơn để không che
- Khi A/B test nếu 0.18 chưa work, test 0.15 hoặc 0.20
```

Concrete triggers cho override. Tránh "use judgment" — list specific cases.

### Bước 7 — Update anti-pattern table (cả 2 directions)

Trong `references/v7-liquid-glass-css-standards.md` Section 10 "Lỗi thường gặp":

```markdown
| Lỗi | Nguyên nhân | Fix |
|---|---|---|
| Glass card quá đục (mờ tịt, che talking head) | Opacity > 0.22 (override quá đà) | Hạ xuống **0.18** (DEFAULT 18/07/2026) |
| Glass card quá trong suốt (mất chữ) | Opacity < 0.15 | Tăng lên **0.18** (DEFAULT) — không bao giờ < 0.15 |
```

Split row thành 2 directions:
- Quá cao (>0.22) → về 0.18
- Quá thấp (<0.15) → về 0.18

Old row `Glass card quá trong suốt | Opacity 0.15 | Tăng lên 0.18` STALE vì 0.18 là default rồi — replace.

### Bước 8 — Cross-reference pointers (2 chiều)

**SKILL.md → references/v7-liquid-glass-css-standards.md:**

```markdown
> **Lưu ý (18/07/2026):** DEFAULT opacity = **0.18** (supersedes V22 verified 0.15). Override allowed per-clip nếu context yêu cầu (chart phase đục hơn 0.22, CTA mỏng hơn 0.15). Xem SKILL.md section `## 🔴 PIP CROPPING PATTERN FOR TIKTOK VERTICAL (added 2026-07-18, FIRST-CLASS)` → `### 8 DEFAULT VALUES` table.
```

**Từ references/ khác (e.g. clip-0003-v71-nate-herk-alignment.md, v7-liquid-glass-css-standards.md) → SKILL.md section:**

Trong file đó, thêm pointer ở chỗ relevant để readers biết default = 0.18:

```markdown
> **Note (18/07/2026):** Opacity 0.18 = canonical DEFAULT trong SKILL.md. V22 verified 0.15 vẫn valid cho override downward (xem "Khi nào dùng 0.15 thay vì 0.18").
```

### Bước 9 (bonus) — Frontmatter tags

Add tag cho discoverability:

```yaml
tags:
  - ...
  - v71-default-opacity-018
  - canonical-default-config
```

Hai tags:
- Specific value tag (`v71-default-opacity-018`) — tìm chính xác lần default-promotion này
- Pattern tag (`canonical-default-config`) — tìm TẤT CẢ default promotions trong skill history

## Anti-patterns khi promote default

- ❌ Chỉ đổi 1 số trong recipe — không canonical, future sessions confused
- ❌ Xóa V22 verified 0.15 row khỏi lịch sử — mất rollback reference
- ❌ "Override if needed" không có concrete triggers — agents sẽ không biết khi nào override
- ❌ Anti-pattern table chỉ fix 1 direction (chỉ "quá thấp" mà không "quá cao") — mất cân bằng
- ❌ Không cross-reference giữa SKILL.md và references/ — readers không tìm thấy
- ❌ Đặt section dưới heading không liên quan (vd dưới "PIP CROPPING") — readers skip vì tưởng unrelated

## Khi nào apply pattern này

Apply khi:
- Anh nói "đặt default X thành Y" (X = existing value đã verified per-clip, Y = new value to promote)
- Một per-clip value được verified ở ≥1 case study mà giờ muốn dùng cho TẤT CẢ future clips
- Cần rollback reference (giữ old value như historical option)

KHÔNG apply khi:
- Value chỉ used trong 1 case study, chưa verified cross-clip
- Anh muốn experimental override per-clip (không phải default)
- Anh muốn A/B test hai values (giữ cả hai trong recipe, không promote một)

## Cross-reference

- SKILL.md section `## 🔴 PIP CROPPING PATTERN FOR TIKTOK VERTICAL (added 2026-07-18, FIRST-CLASS)` → `### 8 DEFAULT VALUES (liquid glass + typography)` table — canonical example
- `references/v7-liquid-glass-css-standards.md` Section 10 — anti-pattern table updated both directions
- `references/clip-0003-v71-nate-herk-alignment-2026-07-18.md` — V7.1 case study that originally verified 0.18
- `references/v19-v22-patches-from-v18-approved.md` — V21 history (opacity 0.18 → 0.15 → rolled back to 0.18) — explains why this default-promotion happened NOW vs later

## Verified case (18/07/2026)

Triggered by anh explicit: "PATCH skill tiktok-product-motion-graphics set default opacity = 0.18"

Process:
1. Initial patch attempted — created duplicate section (under wrong H2 due to parallel-edit)
2. Detected duplicate by re-reading full file (12k → 50k bytes mid-task)
3. Removed redundant section, kept the parallel-edit's better-organized version
4. Added pointer note from V7.1 ALIGNMENT section to canonical DEFAULT CONFIG
5. Updated anti-pattern table in v7-liquid-glass-css-standards.md to reflect 0.18 as default
6. Added frontmatter tags v71-default-opacity-018 + canonical-default-config

Result: canonical DEFAULT CONFIG section in SKILL.md, references/ cross-linked both directions, anti-pattern table consistent, history preserved.

**Lesson for future default-promotions:** Always re-read FULL current file state before patching — parallel edits in multi-session environments can land your patch in wrong location. Detect duplicates by searching for new section headers BEFORE adding content.
