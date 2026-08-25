---
title: HARD CUT Default + CLEAN DELETE Protocol — PITFALL #90 (FLIP of #38)
created: 2026-07-26
updated: 2026-07-26
type: reference
tags: [pitfall-90, hard-cut, no-fade, clean-delete, user-removal-protocol, tiktok-video-editor]
confidence: high
relationships: [tiktok-video-editor-v0.05, audio-fade-check-pitfall-38-DEPRECATED, tiktok-product-script-v0.9.1]
---

# HARD CUT Default + CLEAN DELETE Protocol — PITFALL #90

> **Status:** PITFALL #38 (audio fade 30ms BẮT BUỘC) đã **DEPRECATED** 26/07/2026 theo user feedback. HARD CUT là default concat behavior. File `audio-fade-check-pitfall-38-2026-07-18.md` hiện chỉ mang tính historical record — KHÔNG dùng `afade=t=in/out` ở concat segments.

## 🚨 User Feedback (verbatim 26/07/2026)

**Tuấn Anh sau khi xem 7 clip batch 25/07:**
> *"Anh thấy có fade in fade out hình ảnh khi chuyển từ cảnh này sang cảnh khác! Em bỏ cái đó đi"*

**Tuấn Anh sau khi em patch lần 1 (vẫn để comment "REMOVED"):**
> *"Nói bỏ thì bỏ hẳn ra khỏi skill luôn chứ để comment lại làm gì?"*

→ **2 HARD RULEs mới** vĩnh viễn (cross-skill, cross-project):

### Rule A — HARD CUT is DEFAULT (PITFALL #90)

Khi concat segments trong `build_pre_speed.sh` (tiktok-video-editor), KHÔNG dùng `fade=t=in/out` (video) hoặc `afade=t=in/out` (audio). Mỗi segment CHỈ có:

```bash
[0:v]trim=start=${start}:end=${end},setpts=PTS-STARTPTS,
     scale=1080:1920:force_original_aspect_ratio=increase,
     crop=1080:1920[v${i}]
[0:a]atrim=start=${start}:end=${end},asetpts=PTS-STARTPTS,
     aresample=44100[a${i}]
```

`concat=n=${N}:v=1:a=1[outv][outa]` nối segments hard cut, không apply audio filter mỗi segment.

### Rule B — CLEAN DELETE PROTOCOL (khi user nói "bỏ X")

**Trigger phrasings:**
- "bỏ X đi" / "làm gì X" / "remove X" / "xóa X"
- Bất kỳ user explicit request nào muốn REMOVE một feature/practice/setting.

**Protocol (BẮT BUỘC theo 4 bước đồng bộ):**

| Step | Action | Verify |
|---|---|---|
| 1 | REMOVE code/filter/feature khỏi script | `grep -n "X" <script>` = 0 matches |
| 2 | REMOVE tất cả SKILL.md sections/tables/notes tham chiếu X | `grep -n "X" SKILL.md` = chỉ doc ref (changelog nếu có), không còn active pattern |
| 3 | REMOVE helper file thừa (nếu có, vd `/tmp/build_clip_no_fade.py`) | `ls <file>` = No such file |
| 4 | REMOVE memory entry stale + replace với 1 entry mới nói về LESSON (KHÔNG nói "deprecated") | `grep "X" memory` = 0 mention active |

**Anti-pattern:**
- ❌ "thêm comment nói đã bỏ" = noise, user đọc lại sẽ thấy confusion
- ❌ "để comment tham chiếu REMOVED/deprecated" = signal nhiễu
- ❌ "giữ lại PITFALL row chỉ để ghi DEPRECATED" = clutter

**ĐÚNG:** Code clean, SKILL.md ngắn, memory entry mới focus vào LESSON (vd: "khi user nói bỏ X → remove hẳn").

## 📁 Files affected 26/07/2026 cleanup

| File | Action | Verify |
|---|---|---|
| `tiktok-video-editor/scripts/build_pre_speed.sh` | Xóa `afade=t=in/out` filter khỏi filter_complex | `grep -c "afade" build_pre_speed.sh` = 0 active matches |
| `tiktok-video-editor/SKILL.md` | Xóa section "AUDIO FADE 30ms" + "6.5b", đánh dấu PITFALL #81/#86 deprecated | grep = 0 active pattern |
| `/tmp/build_clip_no_fade.py` | Xóa | file not found |
| `~/.hermes/skills/.../scripts/build_clip_no_fade.py` | Xóa | file not found |
| `build_pre_speed.sh<` heredoc leftover dir | Xóa | dir not found |
| `/Volumes/Storage-1/Hermes/Edit/clip_0095/` test fixture | Xóa (0B broken symlinks) | dir not found |

## 🎓 Cross-skill Lesson vĩnh viễn

**Khi user complaint về HOW-TO (style/tone/format/workflow):**
- Code pattern ← xóa hẳn
- SKILL.md doc ← xóa section/table row
- Helper scripts ← xóa file
- Memory ← REPLACE (không append) — focus LESSON thay vì X cũ

**Apply cho MỌI skill có HARD CUT/fade/audio filter code:** grep, verify, xóa đồng bộ.

## 📚 Related

- `tiktok-video-editor/SKILL.md` v0.05 (26/07 update) — bỏ PITFALL #81 + #86, HARD CUT is default
- `tiktok-product-script/SKILL.md` v0.9.1+ — TONE "văn nói đời thường" preference (cùng class clean-delete)
- Real case 26/07: 7 clip batch V1 (afade) → V2 (hard cut) — `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_*_V2_*.mp4`
- Whisper re-segmentation noise (case 0088): "bỏ vô bất cứ cái túi nào mà mình muốn" → split 2 segs → merge range keep_plan để fix (xem tiktok-video-editor PITFALL #90 § "Whisper re-segmentation noise")

---

*Created 2026-07-26 - flip PITFALL #38 → #90 khi user đổi preference từ fade sang hard cut.*