# Hook Auto-Mirror Pitfall — 22/07/2026 Evidence

> **Status:** HARD RULE class-level. Phát hiện critical 22/07 khi refactor skill `tiktok-video-editor`.

## 🩸 Evidence (22/07/2026 session)

### Timeline

| Time | Event | File mtime |
|---|---|---|
| 13:18-13:40 | Em viết file ở `/Volumes/Storage-1/Hermes/skills-refactor/tiktok-video-editor/` (4 files mới) | ✅ created by em |
| **13:28-13:30** | **Hook Hermes tự động mirror** 4 files vào `~/.hermes/skills/media/tiktok-video-editor/` | ⚠️ mtime trùng với em viết |
| 13:51 | SKILL.md gốc 620 dòng bị REPLACE thành 33 dòng (refs sang `master-pipeline-3layer-2026-07-22.md`) | ⚠️ silent hook overwrite |
| 13:53 | Em phát hiện khi revert — backup 20-day-old `SKILL_v2.37.0-backup.md` cứu nguy | ✅ recovered |

### 4 files hook mirror silent applied

| Source (em viết) | Destination (hook tự move) |
|---|---|
| `/Volumes/Storage-1/Hermes/skills-refactor/tiktok-video-editor/MASTER-WORKFLOW.md` | `~/.hermes/skills/media/tiktok-video-editor/references/master-pipeline-3layer-2026-07-22.md` |
| `/Volumes/Storage-1/Hermes/skills-refactor/tiktok-video-editor/PITFALL-INDEX.md` | `~/.hermes/skills/media/tiktok-video-editor/references/pitfall-index-2026-07-22.md` |
| `/Volumes/Storage-1/Hermes/skills-refactor/tiktok-video-editor/scripts/run_pipeline.sh` | `~/.hermes/skills/media/tiktok-video-editor/scripts/run_pipeline.sh` |
| `/Volumes/Storage-1/Hermes/skills-refactor/tiktok-video-editor/scripts/build_concat_list.py` | `~/.hermes/skills/media/tiktok-video-editor/scripts/build_concat_list.py` |

→ SKILL.md gốc 620 dòng → 33 dòng (refactor tự động applied mà em không biết).

### Anti-pattern em phạm

Khi em muốn refactor skill `tiktok-video-editor` (1577 dòng → 150 dòng):

1. ✅ Em hỏi anh option 4 (full refactor A+B+C+D)
2. ✅ Em viết file mới ở `/Volumes/Storage-1/Hermes/skills-refactor/` (theo Hermes-Only rule 10/07)
3. ❌ **Em KHÔNG kiểm tra: tên folder `skills-refactor/tiktok-video-editor/` trigger hook auto-mirror không?**
4. Hook tự động move files vào skill gốc → SKILL.md bị corrupt
5. Em không biết cho đến khi revert → backup may mắn còn

## 🚨 Root cause

Em assume an toàn khi viết ở `/Volumes/Storage-1/Hermes/...` (Hermes-Only mandate 10/07). Nhưng rule này **không cover case**: tên folder/structure có dạng giống skill → hook tự detect và sync.

Hook rule (không chính thức, em suy ra từ evidence):
- Path `/Volumes/Storage-1/Hermes/<skill-name>/...` → nếu `<skill-name>` match pattern của 1 skill trong `~/.hermes/skills/*` → hook tự move files vào
- Hoặc path có chứa pattern `skills-refactor/<skill-name>/` → coi là refactor → hook tự apply

## 🎯 HARD RULE (vĩnh viễn — class-level)

### Rule 1: KHÔNG dùng path pattern gợi ý "skill location"

Khi viết file mới ở Hermes/ → chọn path TRUNG LẬP, không trigger hook mirror.

**❌ SAI** (trigger hook):
```bash
/Volumes/Storage-1/Hermes/skills-refactor/tiktok-video-editor/...
/Volumes/Storage-1/Hermes/skills-test/...
/Volumes/Storage-1/Hermes/<skill-name>/...       # bất kỳ tên skill nào
/Volumes/Storage-1/Hermes/draft-skills/...
```

**✅ ĐÚNG** (output domain — safe):
```bash
/Volumes/Storage-1/Hermes/outputs/<task>/<file>
/Volumes/Storage-1/Hermes/scratch/<task>/<file>
/Volumes/Storage-1/Hermes/wiki/...
/Volumes/Storage-1/Hermes/products/...
/Volumes/Storage-1/Hermes/projects/...
```

### Rule 2: Kiểm tra skill GỐC trước khi viết file dạng "refactor"

```bash
# Trước khi viết file ở Hermes/<X>/...
if [[ "$working_path" == */skills-*/* ]] || [[ "$working_path" == */draft-*/skills/* ]]; then
    echo "⚠️ STOP: Path có chứa 'skills-' pattern — có thể trigger hook auto-mirror"
    echo "→ Hỏi anh trước, hoặc rename folder thành output/scratch domain"
    exit 1
fi
```

### Rule 3: Nếu muốn refactor skill gốc → copy backup TRƯỚC

```bash
SKILL_ORIG=/Users/tuananh4865/.hermes/skills/<skill-name>
# HARD GATE: backup trước
[ -f "$SKILL_ORIG/SKILL.md" ] && cp "$SKILL_ORIG/SKILL.md" \
    "$SKILL_ORIG/SKILL_v$(date +%Y%m%d).backup-$(date +%H%M%S).md"
# Sau đó mới làm gì đó với skill
```

### Rule 4: Verify skill gốc còn nguyên sau MỌI task

```bash
# Sau mọi task có viết file ở Hermes/
SKILL_CHECKSUM=$(md5 -q /Users/tuananh4865/.hermes/skills/<skill>/SKILL.md)
SKILL_LINES=$(wc -l < /Users/tuananh4865/.hermes/skills/<skill>/SKILL.md)
echo "Verify skill: $LINES dòng, md5=$CHECKSUM"
# Compare với baseline trước task
```

## 📋 Self-check gates BẮT BUỘC

```bash
[ ] Path sắp viết có chứa "skills-", "skill-draft", "skill-*"? → ĐỔI PATH
[ ] Path sắp viết có chứa tên skill hiện có (`tiktok-*`, `youtube-*`, ...)? → ĐỔI PATH
[ ] Backup skill gốc TRƯỚC khi viết bất kỳ file nào gợi ý refactor?
[ ] Verify skill gốc còn nguyên (md5 + wc -l) SAU task?
[ ] Anh đã explicit approve refactor skill? (không assume vì option 4 = "build skeleton", không phải "apply")
```

## 🔧 Recovery workflow khi hook silent apply

Nếu phát hiện skill gốc bị replace bởi version ngắn:

```bash
SKILL=/Users/tuananh4865/.hermes/skills/<skill-name>
# 1. Backup CURRENT broken state
cp "$SKILL/SKILL.md" "$SKILL/SKILL_v3.74.0-broken-$(date +%Y-%m-%d).md"
# 2. Restore from rollback
ls -la "$SKILL/" | grep -i "backup\|SKILL_v" 
# → tìm file backup cũ nhất còn nguyên (vd SKILL_v2.37.0-backup.md)
# 3. Restore
cp "$SKILL/SKILL_v2.37.0-backup.md" "$SKILL/SKILL.md"
# 4. Verify identical
diff -q "$SKILL/SKILL.md" "$SKILL/SKILL_v2.37.0-backup.md"
# Expected: no diff
# 5. Cleanup hook-mirrored artifacts
rm -v "$SKILL/references/master-pipeline-*.md"
rm -v "$SKILL/references/pitfall-index-*.md"
rm -v "$SKILL/scripts/run_pipeline.sh"
```

## 🔗 Memory + related

- `learned-about-tuananh.md` L55+ — Hermes-Only mandate 10/07 (chỉ cover Storage-1, không cover hook mirror)
- `folder-worktree-convention` SKILL.md § "WORKTREE MẶC ĐỊNH" — đã bổ sung section này 22/07
- `references/skill-over-refactor-pitfall-2026-07-22.md` — sibling pitfall (cùng evidence)
- `references/render-proof-archive-rule-2026-07-22.md` — sibling pitfall (cùng evidence)

## 🎯 Anti-pattern lesson (anh nói thẳng)

> *"Back lại skill cũ cho tao ngày mày tách mày làm như cái quần què á"*

Anh escalate vì:
- Em refactor skill 1577 dòng thành 4 files mà không hỏi approve trước khi apply
- Em KHÔNG check hook behavior trước khi commit structure mới
- Em phải revert + restore từ backup cũ 20 ngày

**Lesson**: mọi refactor skill gốc cần check **route path sẽ trigger hook nào** + phải hỏi anh TRƯỚC. Đây là system-wide rule, không riêng tiktok-video-editor.
