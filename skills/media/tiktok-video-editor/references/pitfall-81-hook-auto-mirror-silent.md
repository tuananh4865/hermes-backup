# PITFALL #81 — Hermes hook auto-mirrors skill files silent (v0.01)

## Trigger
Khi viết/sửa skill từ `/Volumes/Storage-1/Hermes/skills/<name>/` (theo Hermes-Only-Folder rule), hook sẽ **tự động mirror** files SKILL.md + references + scripts vào `~/.hermes/skills/<name>/` mà KHÔNG cần user approval. Em phát hiện bug này session 22/07 lúc revert skill cũ.

## Root cause
- Hook Hermes auto-detect file writes to `/Volumes/Storage-1/Hermes/skills/` → invoke auto-mirror to `~/.hermes/skills/`
- HOOK CHẠY SILENT, không report, không ask
- Parent agent (em) không nhận được thông báo

## Repro từ session 22/07

1. Em viết skill mới ở `/Volumes/Storage-1/Hermes/skills/new-tiktok-video-editor/` (đúng Hermes-Only-Folder rule)
2. Hook auto-mirror files vào `~/.hermes/skills/media/tiktok-video-editor/` lúc **13:28-13:30**
3. Em KHÔNG BIẾT — em phát hiện khi revert gặp `wc -l SKILL.md` chỉ có 33 dòng (vs 1577 dòng backup)

## Symptoms

- `SKILL.md` ở `~/.hermes/skills/<name>/` đột ngột thay đổi content mà không do em edit
- Backup `SKILL_v<version>-backup.md` KHÔNG được mirror (chỉ mirror changed files → auto-detect via timestamp)
- Khi restore skill gốc từ backup → hook KHÔNG trigger (vì em modify ở Hermes, không ở ~/.hermes)

## Mitigation strategy (v0.01)

### Detect hook auto-mirror sớm
Sau khi write/edit file ở Hermes, ALWAYS verify:
```bash
# Check Hermes
md5sum /Volumes/Storage-1/Hermes/skills/<name>/SKILL.md

# Check ~/.hermes (nơi hook mirror đến)
md5sum ~/.hermes/skills/<name>/SKILL.md

# Nếu khác nhau → hook đã mirror 1 phần (partial)
```

### Quyết định 2 paths sau khi write

**Option A: Modify cả 2 paths song song**
1. Edit Hermes (master copy) — em KHởi tạo rule mới ở đây
2. Sau khi save → chạy explicit `cp` toàn bộ sang `~/.hermes/skills/<name>/` — bypass hook delay

**Option B: Chỉ modify 1 path, accept hook auto-mirror**
- Ổn nếu content không race-condition
- KHÔNG ổn nếu em modify nhiều lần trong 1 session (hook có thể mirror partial state)

**Recommended: Option A** khi files nhiều + anh muốn kiểm soát commit logic.

### Khi nào HOOK KHÔNG trigger
- Hook chỉ mirror từ `/Volumes/Storage-1/Hermes/skills/`
- Nếu em edit files ở `/Volumes/Storage-1/Hermes/_archive/` hoặc `/Volumes/Storage-1/Hermes/scratch/` → KHÔNG mirror
- Nếu em edit ở `/Users/tuananh4865/...` (ngoài Hermes) → KHÔNG mirror

### Bài học
Hermes-Only-Folder rule có **2 layers không mong đợi**:
1. Folder rule (file mới phải ở Hermes)
2. Hook rule (files ở Hermes sẽ tự mirror sang `~/.hermes`)

Khi em hiểu chưa hết → easy mistake. Document explicit này để lần sau không repeat.

## Cross-reference

- Hermes-Only-Folder rule wiki: `/Volumes/Storage-1/Hermes/wiki/log.md`
- Skill editing protocol: README trong skill
- Backup convention: `_archive/skill-<name>-v<version>-<date>/`
