# Clean-Delete Policy (26/07/2026)

## User verbatim rule

**Tuấn Anh (26/07):** *"Nói bỏ thì bỏ hẳn ra khỏi skill luôn chứ để comment lại làm gì?"*

## Anti-pattern (lần 1 em mắc 26/07)

Khi anh yêu cầu bỏ afade 30ms:
1. Em patch `build_pre_speed.sh` thành HARD CUT
2. **NHƯNG vẫn để comment:**
   - File: `# v0.04 (26/07/2026): REMOVED afade 30ms theo Tuấn Anh feedback`
   - SKILL.md: section "HARD RULE v0.04 — NO FADE IN/OUT (HARD CUT mandatory)"
   - Memory: entry tham chiếu `/tmp/build_clip_no_fade.py` (file helper thừa)
3. Anh flag → em mới thực sự clean

## Fix: REMOVE HẲN — không để signal nhiễu

Khi user nói "bỏ X đi" / "làm gì X" / "remove X" / "xóa X":

### 1. REMOVE HẲN khỏi code

- Xóa hẳn dòng có `fade=t=in` / `afade=t=in:out`, KHÔNG thay bằng `// REMOVED fade`
- Xóa hẳn function, không `function_remove_soon()` empty

### 2. REMOVE section khỏi SKILL.md

- Xóa hẳn section title + body, KHÔNG thêm "Section X đã được thay bằng Y"
- Xóa comment chú thích "v0.04 changed this"
- Nếu cần note cho posterity → 1 dòng ngắn trong changelog, KHÔNG tạo section riêng

### 3. DELETE helper files thừa

- Helper script: `rm -f /tmp/build_clip_X.py`
- Backup files: `rm -f original_backup.py`
- Reference files cũ: `rm -f references/old-approach.md`
- Heredoc leftover: `rm -rf "script.sh<"` (sau redirect fail)

### 4. CLEAN entry memory

- KHÔNG append entry mới chỉ nói "deprecated X"
- GỘP entry cũ + entry mới thành 1 entry focus vào LESSON (clean-delete policy)
- Xóa entry chỉ note "deprecated X"

### 5. VERIFY bằng grep

```bash
# 0 matches = clean
grep -nE "X|REMOVED|deprecated" <file>
# Allows: 1 dòng comment giải thích CURRENT behavior (e.g. "KHÔNG dùng fade")
# Allows: 1 dòng changelog ngắn
# Disallows: any code referencing X
# Disallows: section explaining "X was removed"
```

## Allowed exceptions

| Type | Allowed? | Example |
|---|---|---|
| Code referencing X | ❌ Không | `filter_complex: fade=...` |
| Comment giải thích CURRENT behavior | ✅ Có | `# KHÔNG dùng fade — HARD CUT default` |
| Section SKILL.md mô tả CURRENT rule | ✅ Có | `## Step 6.5 — SMART PAD (no fade)` |
| Section SKILL.md nói "X đã bỏ" | ❌ Không | ~~`## HARD RULE v0.04 — NO FADE`~~ |
| Helper script thừa | ❌ Không | ~~`/tmp/build_clip_no_fade.py`~~ |
| Memory entry gộp lesson | ✅ Có | `[26/07 NO-FADE-CLEAN-DELETE importance:1.0]` |

## Real case 26/07 verification

After clean-delete applied:
- `build_pre_speed.sh` (active + working): `grep -nE "fade|afade"` = 1 match (line 6 comment giải thích HARD CUT default)
- SKILL.md v0.05: 4 doc references (author note, step 6.5 note, smart pad bullet, changelog) — no code, no leading "removed" section
- `/tmp/build_clip_no_fade.py`: ❌ removed
- `~/.hermes/skills/.../build_clip_no_fade.py`: ❌ removed
- `build_pre_speed.sh<` heredoc leftover dir: ❌ removed
- Memory: 2 entry gộp thành 1 entry `[26/07 NO-FADE-CLEAN-DELETE importance:1.0]`

## Tại sao strict?

- "Comment nói REMOVED" = noise, user đọc lại = confusion (anh feedback 26/07)
- Helper file thừa = risk bị reuse nhầm lúc khẩn cấp
- Section "X đã bỏ" = signal clutter, khó scan SKILL.md
- Memory entry trùng entry cũ = recount limit press

## Self-check trước khi SHIP một "bỏ X"

```bash
# 1. grep code của X trong source files
grep -rnE "X_to_remove" /path/to/code/

# 2. grep "REMOVED|deprecated" trong source files (should be 0 active code)
grep -rnE "REMOVED|deprecated" /path/to/code/

# 3. check helper/backup files
ls /tmp/*X* /path/to/backup*X* 2>/dev/null

# 4. grep X trong SKILL.md + docs
grep -nE "X_to_remove" /path/to/SKILL.md

# 5. Memory entry recount
hermes memory --list | grep "X_to_remove"
```

If all 5 PASS (1 match in doc OK as current behavior), ship clean-delete.
