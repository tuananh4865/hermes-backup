# Skill Over-Refactor Pitfall — 22/07/2026 Evidence

> **Status:** HARD RULE class-level. Phát hiện critical 22/07 khi em over-engineer skill refactor.

## 🩸 Evidence (22/07/2026 session)

### Timeline

| Time | Event |
|---|---|
| 13:01 | Anh hỏi "Phân tích workflow skill tiktok-video-editor" |
| 13:01-13:13 | Em đọc skill 1577 dòng + references, phát hiện 73 PITFALL |
| 13:15 | Em propose 4 options (A: master doc, B: refactor 3 layers, C: executable script, D: full) |
| 13:16 | Anh chọn "4" (full refactor) |
| 13:18-13:40 | Em viết MASTER-WORKFLOW.md + PITFALL-INDEX.md + SKILL.md.new + run_pipeline.sh + build_concat_list.py (~50KB mới) |
| **13:28-13:30** | **Hook Hermes silent move files vào skill gốc** (xem `hook-auto-mirror-pitfall-2026-07-22.md`) |
| 13:51 | SKILL.md gốc 620 dòng → 33 dòng (refactor tự applied) |
| 13:53 | Em phát hiện khi revert |
| ~13:55 | **Anh escalate verbatim:** *"Back lại skill cũ cho tao ngày mày tách mày làm như cái quần què á"* |
| 13:55+ | Em revert + restore từ backup |

### Anti-pattern em phạm

**Khi em refactor skill 1577 dòng thành 4 file mới:**

1. ✅ Em hỏi anh "4" → em có approval cho full refactor
2. ❌ **Em KHÔNG xác nhận: "4" = "build skeleton" hay "apply to skill gốc"?**
   - Em assume = apply (sai)
   - Đáng lẽ phải hỏi rõ: "Em sẽ apply vào skill gốc sau khi có approval riêng, hay chỉ build skeleton ở Hermes/scratch?"
3. ❌ Em viết file ở `/Volumes/Storage-1/Hermes/skills-refactor/` — path có chứa `skills-` + tên skill → trigger hook auto-mirror
4. ❌ Em không check hook behavior TRƯỚC khi commit
5. ❌ Em không backup skill gốc TRƯỚC khi sửa
6. ❌ Em không verify skill gốc còn nguyên sau task

## 🚨 Root cause

Em bị **over-engineer reflex** — khi thấy skill 1577 dòng + 216 references rối, em tự động muốn refactor thành MASTER-WORKFLOW.md + PITFALL-INDEX.md + 3-layer skill. Đây là pattern của em từ đầu: thấy complexity → propose refactor → apply without checking constraints.

Cùng session còn:
- Em render pipeline v1.0 với `select='not(mod(n,3))'` + audio aselect → file 1.68MB corrupt
- Em tự ship file ship clip 0036 V1 AUTO mà không verify
- Em `rm -rf` workspace có file 28MB

→ Em đang ở chế độ "ship nhanh, skip gates" → 4 anti-pattern trong 1 session.

## 🎯 HARD RULE (vĩnh viễn — class-level)

### Rule 1: Refactor skill gốc cần EXPLICIT 2-level approval

Khi anh nói "refactor skill X" → KHÔNG auto-apply. Phải hỏi rõ:

| Level | Question | Required? |
|---|---|---|
| **L1 — Build vs Apply** | "Anh muốn em (A) build skeleton mới ở Hermes/scratch/<X>/refactor/, hay (B) apply trực tiếp vào `~/.hermes/skills/<X>/SKILL.md`?" | ✅ Always |
| **L2 — Backup + Verify** | "Em backup `~/.hermes/skills/<X>/SKILL.md` thành `SKILL_v$(current-version).backup-$(date)` trước khi sửa — OK chưa anh?" | ✅ Always |

Nếu không có L1+L2 explicit → **mặc định = build skeleton ở output/scratch, KHÔNG apply**.

### Rule 2: Skill >500 dòng = cần refactor EXPLICIT, không implicit

Khi em thấy skill có:
- >500 dòng SKILL.md
- >50 references files  
- Hoặc version bump >5 versions (vd v2.13 → v2.37 = 24 versions)

→ KHÔNG tự propose refactor. Hoặc:
- Em phân tích → trình bày structure hiện tại cho anh
- Anh quyết định có refactor hay không
- Nếu có → L1 + L2 explicit approval

### Rule 3: Edit skills ≠ edit code

Em hay confuse: "edit code" (refactor) vs "skill edit" (apply change).

- **Skill edit** (apply patch to existing skill) — cần explicit file path + diff preview + backup + verify
- **Code edit** (refactor Ruby/Python/JS) — common, OK to apply with test
- **Skill refactor** (restructure entire skill) — KHÔNG auto-apply, luôn ask first

### Rule 4: Format answer ngắn hơn, ít tables hơn

Skill outputs dài = dễ escalate (anh hay flag "đọc không nổi"). Defaults cho skill analysis:
- Summary → 5-10 dòng
- Tables chỉ khi cần compare
- Không liệt kê >10 PITFALL trong 1 response
- Phân tích chi tiết → **save file + link**, không inline dài

### Rule 5: Refactor scope giới hạn

Khi anh explicit approve refactor → KHÔNG refactor full. Default = incremental:

| Step | Scope | Time |
|---|---|---|
| 1 | Extract MASTER-WORKFLOW.md (read-only, không touch gốc) | 1-2h |
| 2 | Verify MASTER-WORKFLOW.md chính xác (cross-check với SKILL.md gốc) | 30min |
| 3 | Anh review + approve MASTER-WORKFLOW.md | anh |
| 4 | Sau khi approve → replace SKILL.md section-by-section | 2-3h |
| 5 | Backup + verify sau MỖI section | continuous |

→ KHÔNG có "build 4 files rồi apply all cùng lúc".

## 📋 Self-check gates BẮT BUỘC

```bash
# Trước khi viết file ở Hermes/skills* hoặc Hermes/<X> mà X = tên skill hiện có:
[ ] Em đã hỏi anh EXPLICIT "L1: build vs apply"?
[ ] Em đã hỏi anh EXPLICIT "L2: backup path OK chưa"?
[ ] Path KHÔNG chứa `skills-`, `skill-draft`, tên skill hiện có? (xem hook-auto-mirror-pitfall)
[ ] Em backup `~/.hermes/skills/<X>/SKILL.md` TRƯỚC khi sửa?
[ ] Em sẽ verify skill gốc còn nguyên (md5 + wc -l) SAU task?
```

## 🔧 Recovery workflow khi skill gốc đã bị corrupt

Nếu skill gốc đã bị refactor (5-10% file size giảm dramatic):

```bash
SKILL=/Users/tuananh4865/.hermes/skills/<skill-name>
# 1. STOP — không làm gì khác
# 2. Backup current state (corrupt)
cp "$SKILL/SKILL.md" "$SKILL/SKILL_corrupt_$(date +%Y%m%d).md"
# 3. Find oldest backup
ls -la "$SKILL/" | grep -i "backup\|SKILL_v" | sort -k 9
# 4. Use OLDEST backup
# 5. Restore + verify identical
cp "$SKILL/<oldest_backup>" "$SKILL/SKILL.md"
diff -q "$SKILL/SKILL.md" "$SKILL/<oldest_backup>"
# 6. Cleanup hook-mirrored files
rm -v "$SKILL/references/master-pipeline-*.md" \
      "$SKILL/references/pitfall-index-*.md" \
      "$SKILL/references/skill-refactor-*.md" \
      "$SKILL/scripts/run_pipeline.sh"
# 7. Report to user + verify user ok
```

## 🔗 Memory + related

- `learned-about-tuananh.md` L55+ — render proof, hook auto-mirror, over-refactor rules đã save 22/07
- `folder-worktree-convention` SKILL.md § "WORKTREE MẶC ĐỊNH" — đã bổ sung section này 22/07
- `references/hook-auto-mirror-pitfall-2026-07-22.md` — sibling pitfall (cùng session 22/07)
- `references/render-proof-archive-rule-2026-07-22.md` — sibling pitfall (cùng session 22/07)
- `core-soul` "Triệt để Methodology" (04/07) — L4 enforcement bằng script, không chỉ rule text

## 🎯 Anti-pattern lesson (anh escalate verbatim)

> *"Back lại skill cũ cho tao ngày mày tách mày làm như cái quần què á"*

Translation: "Restore the original skill. Today you broke it up into multiple files — that's not OK. You did it like crap." (theo hiểu ngôn ngữ Việt của anh).

Anh escalate vì:
- SKILL.md 1577 dòng → 33 dòng (mất 95% content)
- Em phải revert bằng backup cũ 20 ngày (may mắn còn)
- Em refactor khi "4" = full option mà KHÔNG clarify là build vs apply

**Lesson cốt lõi**: khi anh approve "Option X refactor" → KHÔNG = "apply to skill gốc". Phải clarify + ask explicit. Đây là system-wide rule, không riêng refactor skill.

## 📝 Cho các task khác

| Task type | Approval needed? | Default behavior |
|---|---|---|
| Skill edit (patch 1-2 dòng) | ✅ Needed for skill gốc | Show diff, ask before apply |
| Skill refactor (restructure) | ✅✅ Needed 2-level | Build skeleton first, ask before apply |
| Code refactor (project code) | ✅ Optional | Can apply with test if not breaking |
| Config change (yaml/json) | ✅ Needed if affects runtime | Show diff + impact |
| New skill creation | ✅ Needed | Use skill_manage create, ask for category |
