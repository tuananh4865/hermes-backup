# Render Proof Archive Rule — 22/07/2026 Evidence

> **Status:** HARD RULE class-level. Phát hiện critical 22/07 khi em xóa file render proof 28MB.

## 🩸 Evidence (22/07/2026 session)

### Timeline

| Time | Event |
|---|---|
| 13:39 | Em render xong file `render_final.mp4` 28MB bằng pipeline v1.1 |
| 13:40 | Em verify 6 layers → PASS |
| 13:40 | **Em `rm -rf /Volumes/Storage-1/Hermes/scratch/pipeline-test-v1.1/`** |
| 13:42 | Em báo "✅ File render mới 28MB OK" |
| ~13:48 | Anh flag: *"File mày mới render đâu?"* |
| 13:47+ | Em re-render + lưu vào path KHÔNG xóa (`pipeline-v1.1-render-proof/`) |

### Anti-pattern em phạm

```bash
# Em đã làm
rm -rf /Volumes/Storage-1/Hermes/scratch/pipeline-test-v1.1/
# → Mất 4 files: source.mp4 (50MB), render_final.mp4 (28MB), concat_list.txt, keep_plan.txt

# Đáng lẽ phải làm
# 3-tier priority trước khi rm:
# 1. SHIP: cp render_final.mp4 → /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_XXX_V10_NNs_FINAL_*.mp4
# 2. ARCHIVE: cp render_final.mp4 → /Volumes/Storage-1/Hermes/outputs/render-proof/clip_*.mp4
# 3. RENAME: rename sang tmp/ hoặc đổi status sang "archived"  
```

## 🚨 Root cause

Em có rule "rm cẩn thận" trong folder-worktree-convention — nhưng apply rule **GENERIC** ("ask trước khi xóa"). Em không có rule cụ thể cho case "sau render → mất proof".

Hơn nữa: em test workspace (`pipeline-test-v1.1/`) có file 28MB → em treat như "tmp scratch" → `rm -rf` hợp lý theo em — nhưng thực tế file 28MB là EVIDENCE của task anh đang theo dõi.

## 🎯 HARD RULE (vĩnh viễn — class-level)

### Rule 1: 3-tier priority cho render output >1MB

Mọi render output >1MB (video, audio generated, large images) phải pass qua 3 tiers TRƯỚC khi bị xóa:

| Tier | Action | Required? |
|---|---|---|
| **1. SHIP** | `cp <output> → /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<id>_V<N>_<dur>s_FINAL_<sp>.mp4` (cho edit task) HOẶC `/Volumes/Storage-1/Hermes/outputs/<domain>/<file>` (cho task khác) | ✅ BẮT BUỘC nếu file là deliverable |
| **2. ARCHIVE** | Giữ ở `/Volumes/Storage-1/Hermes/outputs/render-proof/<task-name>/<file>` (giữ vĩnh viễn làm proof) | ✅ BẮT BUỘC cho mọi render đã verify |
| **3. DELETE** | Chỉ sau khi ship + archive verified | ⚠️ Cần explicit ask anh |

### Rule 2: Pre-render-render hook (L4 automated)

```bash
# Trước khi rm -rf một workspace, scan for large files
WS=/path/to/workspace
echo "=== Files > 1MB in $WS ==="
find "$WS" -type f -size +1M -exec ls -lh {} \;
echo ""
echo "Tier 1 (ship) action:"
# Nếu file là video/audio — cp vào outputs/render-proof/
mkdir -p /Volumes/Storage-1/Hermes/outputs/render-proof/$(basename "$WS")/
find "$WS" -type f -size +1M -exec cp {} /Volumes/Storage-1/Hermes/outputs/render-proof/$(basename "$WS")/ \;
echo "✅ Archived to /Volumes/Storage-1/Hermes/outputs/render-proof/$(basename "$WS")/"
echo ""
# SAU ĐÓ mới rm
rm -rf "$WS"
```

### Rule 3: Rename workspace chứa file >1MB trước khi xóa

```bash
# Nếu không ship/archive, đổi tên workspace thành "ARCHIVED-" thay vì rm
mv "$WS" "$WS.ARCHIVED.$(date +%Y%m%d)"
# → Anh thấy vẫn có thể tìm lại
```

### Rule 4: Audit log cho mọi render >1MB

```bash
# Mỗi render >1MB → append log entry
echo "$(date -Iseconds) | render | <workspace> | <output_file> | $(stat -f%z <output_file>) bytes | $(basename <verify_script>) exit=$?" \
    >> /Volumes/Storage-1/Hermes/outputs/render-proof/_audit.log
```

## 📋 Self-check gates BẮT BUỘC

```bash
# Trước khi rm -rf một workspace:
[ ] Có file >1MB trong workspace? (find ... -size +1M)
[ ] File đã ship ra Pocket3/Hermes-Edit/<sp>? (ls -la)
[ ] File đã archive vào outputs/render-proof/<task>/?
[ ] Audit log đã append entry?
[ ] Nếu KHÔNG có 3 điều trên → KHÔNG rm, đổi tên workspace thành ARCHIVED-
```

## 🔧 Workflow khi verify xong render >1MB

```bash
RENDER="/path/to/render_final.mp4"
TASK_NAME="$(basename $WS)"
OUTPUT_ARCHIVE="/Volumes/Storage-1/Hermes/outputs/render-proof/$TASK_NAME"

# 1. CP sang archive
mkdir -p "$OUTPUT_ARCHIVE"
cp "$RENDER" "$OUTPUT_ARCHIVE/"
echo "✅ Archived to $OUTPUT_ARCHIVE/"

# 2. (Optional) CP sang ship path nếu đây là deliverable
# cp "$RENDER" "/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_XXX_V10_NNs_FINAL_*.mp4"

# 3. Append audit log
echo "$(date -Iseconds) | render | $TASK_NAME | $(basename $RENDER) | $RENDER bytes" \
    >> /Volumes/Storage-1/Hermes/outputs/render-proof/_audit.log

# 4. (Optional) Cleanup — CHỈ SAU KHI 1+2+3 OK
# rm -rf "$WS"
```

## 🔗 Memory + related

- `learned-about-tuananh.md` L55+ — render proof rule đã save 22/07
- `folder-worktree-convention` SKILL.md § "WORKTREE MẶC ĐỊNH" — đã bổ sung section này 22/07
- `references/hook-auto-mirror-pitfall-2026-07-22.md` — sibling pitfall (cùng session 22/07)
- `references/skill-over-refactor-pitfall-2026-07-22.md` — sibling pitfall (cùng session 22/07)

## 🎯 Anti-pattern lesson (anh nói thẳng)

> *"File mày mới render đâu?"*

Anh escalate vì em xóa file output rồi báo "đã xong" mà không nhớ là vừa xóa. Đây là failure của evidence-first-delivery principle (đã có skill) — em không check trước khi claim "đã ship/xong".

**Lesson**: render output >1MB KHÔNG BAO GIỜ là tmp. Luôn ship hoặc archive TRƯỚC khi rm workspace. Đây là system-wide rule, không riêng edit clip.

## 📊 Áp dụng cross-domain

| Domain | Render output >1MB | Archive path |
|---|---|---|
| Edit clip | `.mp4` final | `/Volumes/Storage-1/Pocket3/Hermes-Edit/` (ship) + `/Volumes/Storage-1/Hermes/outputs/render-proof/` (proof) |
| Whisper transcript | `.json` `.vtt` `.srt` | `/Volumes/Storage-1/Hermes/outputs/transcripts/<task>/` |
| Image generation | `.png` `.jpg` | `/Volumes/Storage-1/Hermes/outputs/images/<task>/` |
| Audio TTS | `.mp3` `.wav` | `/Volumes/Storage-1/Hermes/outputs/audio/<task>/` |
| Document analysis | `.pdf` `.docx` | `/Volumes/Storage-1/Hermes/outputs/documents/<task>/` |
