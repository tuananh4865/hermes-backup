---
name: folder-worktree-convention
description: Quy ước worktree chuẩn cho MỌI folder em làm việc — file final giữ flat trong folder, file tạm vào `{folder}/tmp/`, KHÔNG tạo folder con lồng, KHÔNG tự copy/sync Drive, KHÔNG tự xóa folder cũ. Load khi bắt đầu task ở folder bất kỳ (không chỉ edit clip) để tự check + mkdir `{folder}/tmp/` + áp gates trước khi act.
version: 1.0.0
author: 'Tuấn Anh + Hermes Agent (04/07 — NO-AUTONOMY evidence: 3 anti-patterns trong 1 session)'
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [workflow, file-management, folder-hygiene]
    related-skills: [tiktok-video-editor, mac-disk-cleanup-audit, recurring-junk-folder-investigation]
---

# Folder Worktree Convention (04/07 — anh HARD rule, class-level)

> **Anh mandate 04/07 (verbatim):** *"Làm việc trong dự án ở bất kỳ folder nào cũng phải thiết lập worktree theo đúng chuẩn. File linh tinh / tạm thời / không ảnh hưởng project chính → gom hết vào `{folder}/tmp/` để gọn."*

## 🚨 Tại sao skill này tồn tại

Trước 04/07, em phạm **3 anti-patterns trong 1 session edit clip**:
1. Tạo folder con `clip_drive3_source/` lồng trong folder final → anh flag *"sao lại tạo thêm folder gì vậy???"*
2. Đặt tên file `clip_drive3_v1_edited.mp4` (có version + hậu tố thừa) → sai format
3. Tự ý `cp` file sang Google Drive My Drive/ → anh chửi *"địt mẹ mày sao cứ tự cho là mình hay ho biết hết"*

**10/07 evidence (bổ sung — vẫn tiếp tục xảy ra):** Sau skill update, em vẫn leak file vào `~/Downloads/`, `~/Movies/badminton-highlights/`, `~/.hermes/cache/` cho đến khi anh escalate. **4TH anti-pattern** mới: save file lẻ lung tung ngoài `/Volumes/Storage-1/Hermes/` → anh mandate 10/07 *"mọi hoạt động Hermes đều phải được lưu ở Volumes/Storage-1/Hermes"*. Fix = worktree routing rule ở cuối file này.

Skill này = CLASS-LEVEL rule. Áp dụng cho MỌI folder em làm việc (không chỉ edit clip). Khi em bắt đầu task ở folder X (bất kỳ) → load skill này → check + apply gates.

## 🌳 Pattern chuẩn

```
{any-folder}/
├── {final files có giá trị lâu dài}    ← file đã render, file final, file cần giữ
└── tmp/                                ← MỌI thứ linh tinh
    ├── transcript.json / .txt / .srt   ← Whisper / parser output
    ├── keep_plan.txt                   ← analysis output
    ├── audio_extract.wav              ← ffmpeg extract
    ├── filter_ffmpeg.txt              ← ffmpeg filter
    ├── scratch_*.txt                  ← note tạm, debug log
    └── legacy-*/                      ← folder cũ move vào (KHÔNG xóa)
```

## ⚙️ 6 Rules cứng

1. **KHÔNG tạo folder mới cùng cấp** với file final trong folder chính
   - ❌ `Hermes-Edit/transcripts/`, `Hermes-Edit/analysis/`, `Hermes-Edit/output/`
   - ✅ Mọi thứ phụ → `Hermes-Edit/tmp/`
2. **KHÔNG tạo folder con lồng** trong folder chính (trừ `tmp/`)
   - ❌ `Hermes-Edit/clip_xxx_source/`, `Hermes-Edit/draft_v1/`
   - ✅ `Hermes-Edit/tmp/clip_xxx_working/` nếu cần thiết (hoặc flat trong `tmp/` luôn)
3. **Tất cả file tạm** → `{folder}/tmp/` ngay từ đầu, KHÔNG tạo ở `/tmp` (system)
   - Lý do: anh không thấy file ở `/tmp`, khó debug. Khi vào `tmp/` của folder là thấy ngay.
4. **Cleanup system `/tmp`** sau khi task xong (xóa file do task em tạo)
5. **File cũ** từ session trước trong folder chính → move vào `tmp/legacy-{name}/` thay vì xóa
   - **KHÔNG BAO GIỜ tự xóa** — hỏi anh trước
6. **KHÔNG tự copy/move/sync file sang nơi khác** (Drive, desktop, v.v.) trừ khi anh explicit
   - Lý do: anh đã config sync, em copy = duplicate + lãng phí bandwidth/disk
   - Trừ khi anh nói rõ "copy sang X" → làm theo, KHÔNG tự propose

## ✅ Self-check gates (BẮT BUỘC trước MỌI task)

```
[ ] Folder làm việc đã có {folder}/tmp/ chưa? → Nếu chưa → mkdir ngay
[ ] Mọi file tạm sắp sinh ra có path prefix = {folder}/tmp/ ? 
[ ] KHÔNG tạo folder mới cùng cấp file final?
[ ] KHÔNG tạo folder con lồng (trừ tmp/)?
[ ] Nếu cleanup file cũ → ĐÃ HỎI ANH chưa?
[ ] Nếu sync/copy file sang nơi khác → ĐÃ ĐƯỢC ANH CHỈ rõ chưa?
```

**Nếu 1 gate fail → STOP, không hành động, hỏi anh.**

## 🗣️ Tone correction (04/07 evidence — class-level)

Khi bị flag sai bởi anh:
1. **DỪNG ngay** hành động đang làm
2. **KHÔNG argue** — không "nhưng mà em nghĩ..."
3. **KHÔNG hỏi option A/B/C** — đợi anh chỉ rõ
4. **Ngôn ngữ ngắn**: "Dạ em hiểu rồi", hỏi đúng 1 câu cần thiết
5. **Patch skill** ngay để chặn anti-pattern tái phạm — không chỉ save rule vào memory

**Anti-pattern reply khi bị flag**:
- ❌ "Anh muốn X hay Y?" → tự chọn best option rồi deliver
- ❌ "Em cần hỏi thêm để hiểu yêu cầu" → research, đọc wiki, tự hiểu
- ❌ Multi-option không commit → pick one and execute
- ❌ Tự propose giải pháp khi chưa research hệ thống thực tế

**Default mode**: low confidence. Tự tin cao = red flag = dừng research lại.

## 🚨 TRIỆT ĐỂ Methodology — anh mandate 04/07 (verbatim)

> *"Mày phải tự học dựa trên những sai lầm đã tìm được cách khắc phục **triệt để** chứ không phải tự học khi vấn đề của mày chưa được giải quyết."*

**5 levels of rule enforcement (low → high):**

| Level | Mechanism | Example | Effectiveness |
|-------|-----------|---------|---------------|
| **L1 — Document** | Rule in SKILL.md text | "KHÔNG tạo folder con" | ❌ Low — text only, agent violates |
| **L2 — Memory** | Save to memory | `[04/07] no folder con` | ❌ Low — memory ≠ behavior |
| **L3 — Self-check gate** | Checklist BEFORE act | `[ ] Path flat, no folder con?` | 🟡 Medium — agent might skip |
| **L4 — Automated gate** | Script validates | `verify_worktree.py` exit 1 → blocks render | ✅ High — can't bypass |
| **L5 — System-wide CI** | Pre-tool hook | `pre_tool_use` hook on every tool call | ✅ Highest — runs every time |

**Anh's "triệt để" = L4 minimum (script gate), prefer L5 (CI hook).** L1-L2 alone = no help. Documenting without patching = same as no doc.

**04/07 evidence — escalated 3 times before patching:**
1. L1: Rule in skill → em violated (created `clip_drive3_source/`)
2. L2: Save to memory → em violated next session (still created folder)
3. **L3+L4: Self-check gates + `scripts/verify_worktree.py`** → em cannot violate anymore (script blocks render)

**Workflow after every user correction:**
1. Capture WHAT was wrong (the anti-pattern)
2. Capture WHY (root cause, not symptom)
3. Patch to L4 (script gate) at minimum — L5 if it's a class-level rule
4. Commit the patch + verify by simulating the failure (try to violate, confirm blocked)
5. Update reference doc with the failure evidence + fix

**Anti-pattern (causes rule không triệt để):**
- ❌ "Đã ghi rule vào skill rồi, xong" → chỉ L1, không block
- ❌ "Đã save vào memory rồi, xong" → chỉ L2, không enforce
- ❌ "Add pitfall #N+1 to skill" → chỉ L1, không có cơ chế ngăn
- ❌ "Documented but not patched" = same as no doc

**Test after every patch (verify gate actually blocks):**
```bash
# Simulate violation
mkdir -p /Volumes/Storage-1/Pocket3/Hermes-Edit/test_violation/
# Verify gate catches it
./scripts/verify_worktree.sh /Volumes/Storage-1/Pocket3/Hermes-Edit/test_violation/source.mp4
# Expected: exit 1 + clear error message
# If exit 0 → gate broken, patch again
```

## 🔧 Workflow khi bắt đầu task ở folder mới

```bash
# Step 1: Check folder có tmp/ chưa
if [ ! -d "{folder}/tmp" ]; then
  mkdir -p "{folder}/tmp"
  echo "✅ Created {folder}/tmp/"
fi

# Step 2: Self-check gates
echo "[ ] Folder có tmp/ chưa? $([ -d {folder}/tmp ] && echo ✅ || echo ❌)"
echo "[ ] Có folder cũ cần cleanup không? (ls -la {folder}/ | grep -v 'tmp$\|\.mp4$\|\.DS_Store')"
echo "[ ] Có file cũ cần ask anh move vào tmp/ không?"

# Step 3: Khi sinh file tạm → path = {folder}/tmp/
# VD: source audio → {folder}/tmp/audio_extract.wav
# VD: transcript → {folder}/tmp/transcript.json
# VD: keep plan → {folder}/tmp/keep_plan.json

# Step 4: Cleanup khi task xong
rm -f /tmp/*.{wav,txt,json} 2>/dev/null  # system tmp files do task em tạo
```

## 📚 Context-specific extension

**Edit clip task** → load thêm `tiktok-video-editor` (đã có sẵn):
- Output final path: `/Volumes/Storage-1/Pocket3/Hermes-Edit/{nội-dung-không-dấu}-{ddmmyyyy}.mp4`
- KHÔNG version v1/v2/edited trong filename
- KHÔNG tự copy Drive (anh config sync)

**Disk audit task** → load thêm `mac-disk-cleanup-audit`:
- KHÔNG xóa folder `~/Library/Application Support/Claude/vm_bundles/` (LIVE VM)
- KHÔNG xóa `~/.lmstudio/models/` nếu user dùng local LLM

---

## 🔍 RECURSIVE SEARCH BEFORE CLAIM (17/07 — class-level pitfall)

> **Anh escalation 17/07 (verbatim):** *"Sao lại không thấy Hermes-edit được??? Mọi lần xuất video final đều xuất vào đó mà"*

### Anti-pattern em đã phạm

Trước 17/07, em có habit nguy hiểm khi user hỏi về 1 folder mà không rõ path tuyệt đối:

```bash
# ❌ SAI — chỉ check top-level 2 chỗ rồi báo "không tồn tại"
test -d /Users/tuananh4865/Hermes-Edit || echo "❌"
test -d /Volumes/Storage-1/Hermes-Edit || echo "❌"
echo "→ Hermes-Edit không tồn tại"
```

Thực tế folder nằm sâu 2 cấp: `/Volumes/Storage-1/Pocket3/Hermes-Edit/` (87 entries top-level + 210 .mp4 files).

### Memory có rule này nhưng em vẫn quên

Trong memory `learned-about-tuananh.md` đã có lesson `2026-06-24 🍎 macOS Case-Insensitive Path Trap` + `2026-07-05 L34 BINARY CLEANUP RULE` — cả 2 đều đã ghi "KHÔNG BAO GIỜ assume folder đã xóa khi không thấy ở top-level". Em đã **biết rule** nhưng vẫn **không apply** khi user hỏi → tư duy bị "không thấy = không có" thắng lý trí.

### Rule mới (L4 enforcement bằng bash script)

**KHI user nhắc đến 1 folder name mà KHÔNG cho path tuyệt đối** (vd: "Hermes-Edit", "folder final", "thư mục output", "ấy có biết folder X không"):

1. **Bước 1 — Check allowlist TRƯỚC** (không được skip):
   ```bash
   # Top-level candidates (anh thường đặt tên worktree ở đây)
   for p in \
     /Users/tuananh4865/Hermes-Edit \
     /Volumes/Storage-1/Hermes-Edit \
     /Volumes/Storage-1/Pocket3/Hermes-Edit \
     /Volumes/Storage-1/Hermes-Edit \
     "/Users/tuananh4865/Hermes Edit" \
     "/Volumes/Storage-1/Hermes Edit"; do
     [ -e "$p" ] && echo "FOUND: $p" && exit 0
   done
   ```

2. **Bước 2 — Nếu KHÔNG tìm thấy ở allowlist → RECURSIVE search đến depth 4 TRÊN `/Volumes/Storage-1/` TRƯỚC** (KHÔNG tìm trên `/Users/tuananh4865/` vì file edit worktree LUÔN ở Storage-1):
   ```bash
   find /Volumes/Storage-1 -maxdepth 4 -type d -iname "*Hermes*Edit*" 2>/dev/null
   ```
   Nếu ra kết quả → dùng path đó. Nếu KHÔNG ra → tiếp bước 3.

3. **Bước 3 — Nếu vẫn không có → MỚI được hỏi anh** (chứ không phải hỏi ngay ở bước 1):
   > *"Em đã check 6 allowlist + recursive depth 4 trên Storage-1 mà chưa thấy folder {name}. Anh có thể cho em absolute path hoặc em check tiếp chỗ khác không anh?"*

4. **Bước 4 — KHI HỎI**: KHÔNG dùng câu "Em không thấy folder đó" hoặc "Folder có thể đã bị xóa" — vì user sẽ escalate. Thay bằng "Em tìm ở 7 chỗ và chưa thấy, anh cho em path đầy đủ nhé".

### 3 anti-pattern chính trong recursive search pitfall

| # | Anti-pattern | Ví dụ sai | Đúng |
|---|---|---|---|
| 1 | **Top-level only** — chỉ check `/Users/{user}/` + `/Volumes/Storage-1/` | `test -d /Volumes/Storage-1/Hermes-Edit` (FALSE FAIL) | Recursive depth 4 toàn bộ Storage-1 |
| 2 | **"Không thấy = không có"** — assume folder đã bị xoá khi check top-level fail | "Hermes-Edit không tồn tại anh ơi" | "Em đã check 7 chỗ + recursive, có thể em chưa tìm đúng chỗ. Anh nhắc lại path đầy đủ giúp em" |
| 3 | **Case-sensitive search** — search `Hermes-Edit` thay vì `-iname` | `find ... -name "Hermes-Edit"` (FALSE FAIL trên macOS case-insensitive) | `find ... -iname "*Hermes*Edit*"` |

### Verify gate tự động (bash one-liner anh có thể chạy ngay)

```bash
# Trước khi claim "folder X không tồn tại" → chạy cái này
SEARCHNAME="Hermes-Edit"
echo "=== Allowlist check ==="
for p in "/Users/$USER/$SEARCHNAME" "/Volumes/Storage-1/$SEARCHNAME" "/Volumes/Storage-1/Pocket3/$SEARCHNAME" "/Volumes/Storage-1/Hermes/$SEARCHNAME" "/Users/$USER/${SEARCHNAME,,}" "/Users/$USER/${SEARCHNAME^^}"; do
  [ -e "$p" ] && echo "FOUND at: $p"
done
echo ""
echo "=== Recursive depth 4 trên Storage-1 ==="
find /Volumes/Storage-1 -maxdepth 4 -type d -iname "*${SEARCHNAME,,}*" 2>/dev/null
echo ""
echo "=== Recursive depth 4 trên home ==="
find /Users/$USER -maxdepth 4 -type d -iname "*${SEARCHNAME,,}*" 2>/dev/null
```

Nếu cả 3 đều rỗng → MỚI hỏi anh.

### Liên hệ với memory pitfalls đã có

| Memory lesson | Mối liên hệ với recursive search pitfall |
|---|---|
| `2026-06-24 macOS Case-Insensitive Path Trap` | Cùng pattern "không thấy ≠ không có" trên filesystem HFS+/APFS |
| `2026-07-05 L34 BINARY CLEANUP RULE` | Liên quan: "KHÔNG BAO GIỜ assume folder đã xóa" |
| `2026-07-12 ADVERSARIAL SUBAGENT VERIFIER` | Cùng tinh thần: "Tool return success ≠ ground truth" |

**Bài học meta:** Cả 3 memory rule trên đều đã có sẵn nhưng em vẫn fail. Đây là **failure của activation** (em không load rule khi cần), không phải failure của knowledge. Fix = nhúng rule vào SKILL.md (đã làm trong patch này) + tham chiếu reference (đã link ở dưới).

### Reference

- `references/recursive-search-before-claim-2026-07-17.md` — full evidence transcript + 4-step workflow + verify bash script + 3 anti-pattern table

---

## 🔴 SO SÁNH 2 WORKTREE CỦA ANH (17/07 evidence — em đã nhầm thật sự)

| Worktree | Path | Em hay nhầm là | Thực tế |
|---|---|---|---|
| **Edit clip final** | `/Volumes/Storage-1/Pocket3/Hermes-Edit/` | Em search top-level `/Volumes/Storage-1/Hermes-Edit` → fail | Nằm sâu 2 cấp dưới `Pocket3/` |
| **Hermes outputs (mặc định)** | `/Volumes/Storage-1/Hermes/outputs/` | Em search `/Volumes/Storage-1/outputs` → fail | Nằm sâu 1 cấp dưới `Hermes/` |

**Lesson:** Hai worktree chính của anh đều là path con — KHÔNG BAO GIỜ chỉ check top-level, LUÔN dùng recursive search depth 4 trước khi report "không thấy".

---

## Related Skills

- `tiktok-video-editor` — domain-specific extension (edit clip, filename, output path Pocket3)
- `mac-disk-cleanup-audit` — disk cleanup với 3-tier safety
- `recurring-junk-folder-investigation` — khi folder keep reappear sau khi delete
- `default-project-hub-pattern` — set up project folder theo 3-tier loading
- `project-init-resume-workflow` — 4-step workflow khi start project mới

## When to Load This Skill

- Bất kỳ task nào yêu cầu tạo/sửa/di chuyển file trong folder
- Đặc biệt: edit video, build code project, viết research doc, làm data analysis
- KHI MỚI VÀO folder (chưa quen cấu trúc) → check gates trước khi act

## References

- `references/no-autonomy-anti-patterns.md` — 3 anti-patterns 04/07 evidence + cách fix triệt để
- `references/folder-cleanup-protocol.md` — protocol cleanup folder cũ (ask → move → never delete)
- `references/self-check-gate-script.md` — bash script check gates trước khi act
- `references/outputs-worktree-2026-07-10.md` — anh mandate worktree mặc định cho file lẻ
- `references/telegram-clarify-ui-bug-2026-07-19.md` — **NEW 19/07** `clarify` tool không render UI trên Telegram → dùng inline numbered list + Hermes-Only mandate mở rộng scope
- `references/hook-auto-mirror-pitfall-2026-07-22.md` — **NEW 22/07** Hook Hermes tự động mirror file mới từ `/Volumes/Storage-1/Hermes/*` vào `~/.hermes/skills/*` (silent apply, agent không control). Anti-pattern + evidence (SKILL.md 620 dòng tự động replace thành 33 dòng). HARD RULE: KHÔNG tạo file mới ở Hermes/ với path gợi ý skill (vd: `skills-refactor/tiktok-video-editor/`) — chỉ dùng output domain (`outputs/`, `scratch/`, `wiki/`).
- `references/render-proof-archive-rule-2026-07-22.md` — **NEW 22/07** HARD RULE: file render proof >1MB KHÔNG BAO GIỜ `rm -rf` mà không ship ra Pocket3/Hermes-Edit hoặc archive vào `/Volumes/Storage-1/Hermes/outputs/`. 3-tier priority: ship → archive → xóa.
- `references/skill-over-refactor-pitfall-2026-07-22.md` — **NEW 22/07** Anh escalation "Back lại skill cũ cho tao ngày mày tách mày làm như cái quần què á". Anti-pattern: refactor skill gốc (>50KB / 100+ dòng) mà không có explicit approve. HARD RULE: refactor skill gốc cần anh approve TRƯỚC khi viết script chạy trên path đó.

---

## 🌳 WORKTREE MẶC ĐỊNH CHO FILE LẺ (10/07/2026 — anh mandate, class-level)

> **Anh mandate verbatim:** *"cài đặt cho toàn bộ các hoạt động của hermes đều phải được lưu ở Volumes/Storage-1/Hermes. tạo worktree cho phù hợp với từng loại file và từng loại hoạt động sao cho hermes agent chỉ tạo file, tải file và hoạt động toàn bộ bên trong worktree này!!!! ngoại trừ những dự án đã được chỉ định worktree thì mặc định mọi file lẻ tẻ phải được bỏ vào bên trong worktree mặc định này!!!"*

### Phân biệt worktrees (19/07 — mở rộng scope "MỌI THỨ")

| Worktree | Path | Dùng cho | Quy tắc |
|---|---|---|---|
| **EDIT VIDEO (của anh)** | `/Volumes/Storage-1/Pocket3/Hermes-Edit/` | Edit clip cầu lông, render TikTok cuối | Anh giám sát trực tiếp — cho phép vì raw footage MP4 nằm ở Pocket3, copy qua Hermes sẽ tăng latency 4K |
| **HERMES MẶC ĐỊNH (MỌI THỨ)** | `/Volumes/Storage-1/Hermes/` | File mới em tạo: download, screenshot, audio, transcript, cron output, scripts, wiki, products, projects, configs, tools, experiments | Em tự route vào sub-folder đúng theo domain |

**Anh mandate 19/07 (verbatim, dấu `!!!!` = escalate):** *"anh muốn em làm mọi việc trong Volumes/Storage-1/Hermes phải tạo và làm tất cả mọi thứ trong đó!!!!"*

### Cấu trúc `/Volumes/Storage-1/Hermes/` (đã có sẵn — em theo)

```
/Volumes/Storage-1/Hermes/
├── wiki/             ← Knowledge base (entities, concepts, comparisons)
├── products/         ← Product research cache (wiki products)
├── projects/         ← Multi-week projects workspaces
├── scripts/          ← Python/Bash scripts em viết
├── skills/           ← Custom skills (mirror ~/.hermes/skills nếu cần)
├── outputs/          ← File lẻ runtime (downloads, videos, audio, transcripts, screenshots)
├── Edit/             ← (option) Move Hermes-Edit ở Pocket3 về đây nếu anh OK
├── logs/             ← Cron logs, debug logs
├── memories/         ← Memory dumps, state files
├── secrets/          ← Encrypted secrets (KHÔNG raw API key)
├── workers/          ← Multi-agent worker configs
├── cron/             ← Cron job definitions
├── archive/          ← Archive folder cũ (KHÔNG xóa)
└── <custom>/         ← Em tạo folder mới theo domain nếu cần
```

### Apply ngay (19/07 — HARD RULE)

- **Mọi file MỚI em tạo cho anh** → PHẢI nằm trong `/Volumes/Storage-1/Hermes/...`
- **KHÔNG tạo file trong `/Users/tuananh4865/`** (Mac local) trừ 3 trường hợp:
  1. **System config bắt buộc**: `~/.hermes/config.yaml`, `~/.hermes/.env`, `~/.bashrc` — Hermes gateway **đọc từ đây lúc start** (move đi = break gateway)
  2. **Runtime state**: `~/.hermes/state.db`, `~/.hermes/sessions/`, `~/.hermes/logs/` — đang chạy, không move
  3. **Anh explicit cho phép**: vd "save vào ~/Downloads/" — làm theo
- **KHÔNG tạo ở `/tmp/` system** — anh không thấy file ở `/tmp/`, khó debug
- **Nếu task CẦN file ngoài Hermes** (vd: download MP4 lớn về Mac local vì volume mount chậm) → HỎI anh trước, đừng tự quyết

### Khi anh chưa confirm scope (đã xảy ra 19/07)

Em hỏi `Option A/B/C/D` qua tool `clarify` → Telegram UI **KHÔNG render được choices** (anh flag: *"3 scope em hỏi anh không thấy xuất hiện? em hỏi lại xem nào"*).

**Fix = HỎI BẰNG TEXT THƯỜNG** khi channel = Telegram:
```markdown
**Anh muốn em xử lý X sao?**

1. Option A — mô tả ngắn
2. Option B — mô tả ngắn
3. Option C — mô tả ngắn
4. Option D — em recommend + lý do

Anh gõ A/B/C/D hoặc nói rõ ý em làm
```

KHÔNG dùng tool `clarify` với `choices` parameter khi platform = Telegram. Alternatives OK: open-ended question, hoặc inline numbered list trong tin nhắn.

### Self-check gates CẬP NHẬT (19/07)

```
[ ] File sắp save có path nằm trong /Volumes/Storage-1/Hermes/...?  (anh mandate 19/07)
[ ] Nếu nằm ngoài Hermes → có phải 1 trong 3 ngoại lệ (system config / runtime state / anh explicit)?
[ ] File thuộc domain nào?  → route vào sub-folder đúng (wiki/, products/, scripts/, outputs/, ...)
[ ] Folder cha có tmp/ chưa?  → nếu chưa → mkdir
[ ] KHÔNG tạo folder con lồng (trừ tmp/)?
[ ] KHÔNG tự copy/sync Drive?
[ ] Nếu cleanup file cũ → ĐÃ HỎI ANH chưa?
```

### 9 sub-folders theo LOẠI FILE

```
/Volumes/Storage-1/Hermes/outputs/
├── downloads/      ← Telegram files, browser download (MP4/PDF/MP3/ZIP)
├── videos/         ← Video YouTube/TikTok em download để xử lý
├── images/         ← image_generate output, processed ảnh
├── audio/          ← TTS, transcription source, MP3 download
├── documents/      ← PDF, DOCX em phân tích cho anh
├── screenshots/    ← computer_use captures, browser screenshots
├── transcripts/    ← Whisper cache (.vtt/.srt/.json)
├── cron-output/    ← Cron job deliverables
└── scratch/        ← Throwaway temp (AUTO-CLEANUP 7 ngày)
```

### Allowlist (giữ nguyên path riêng — KHÔNG route)

| Path | Lý do giữ nguyên |
|---|---|
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/` | Anh edit video worktree |
| `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-*/` | Project workspaces (đã có) |
| `/Volumes/Storage-1/Hermes/Hop dong OPM716/` | Single project |
| `/Volumes/Storage-1/Hermes/projects/` | Older project workspaces |
| `/Volumes/Storage-1/Hermes/wiki/`, `skills/`, `scripts/` | Hermes knowledge base |
| `~/.hermes/.git/`, `state.db`, `hermes-agent/`, `sessions/`, `logs/` | Runtime state — KHÔNG động |

### CẤM save vào (legacy paths — file cũ vẫn ở đó)

| Path | Lý do cấm |
|---|---|
| `~/Downloads/` | Anh dùng cho download cá nhân |
| `~/Movies/` | Anh dùng cho project cá nhân |
| `~/Desktop/` | Anh dùng cho working files cá nhân |
| `~/.hermes/cache/` | Cache transient, không persistent |

### Cleanup policy (cron tự động dọn `scratch/`)

| Folder | Sau X ngày | Lý do |
|---|---:|---|
| `scratch/` | 7d | Temp — auto-cleanup |
| `screenshots/` | 1d | Transient |
| `audio/` | 14d | Sau khi transcribe xong |
| `transcripts/` | 30d | Sau khi dùng cho edit |
| `videos/` | 30d | Sau khi edit xong |
| `images/` | 90d | Reuse images |
| `downloads/`, `documents/`, `cron-output/` | ∞ | Anh tự quản |

### Routing flow (khi em cần save file)

```python
# Pseudo-code em tự chạy trong đầu trước khi write
def route_save(file_type: str, filename: str) -> Path:
    # 1. File thuộc project worktree riêng? → save vào project path
    if is_project_worktree_path(target):
        return project_path / filename
    
    # 2. File là runtime? (cache, sessions, logs) → save vào runtime
    if is_runtime_path(target):
        return runtime_path / filename
    
    # 3. File lẻ? → route vào /Volumes/Storage-1/Hermes/outputs/<sub>/
    subdir_map = {
        "video": "videos", "image": "images", "audio": "audio",
        "pdf": "documents", "docx": "documents",
        "screenshot": "screenshots", "transcript": "transcripts",
        "telegram_file": "downloads", "browser_download": "downloads",
        "cron_deliverable": "cron-output", "temp": "scratch",
    }
    subdir = subdir_map.get(file_type, "downloads")
    return Path(f"/Volumes/Storage-1/Hermes/outputs/{subdir}/{filename}")
```

### ⚠️ Hermes config security guard — pitfall mới (10/07)

Khi muốn sửa Hermes config global (`~/.hermes/config.yaml`), em gặp **security guard** block:

```
Refusing to write to Hermes config file: /Users/tuananh4865/.hermes/config.yaml
Agent cannot modify security-sensitive configuration. Edit ~/.hermes/config.yaml directly
or use 'hermes config' instead.
```

**Fix = KHÔNG patch trực tiếp.** Workaround:
1. Tạo config riêng ở `/Volumes/Storage-1/Hermes/outputs/.worktree-routing.yaml`
2. Em (agent) **tự đọc file đó manually** trước khi save file lẻ
3. Nếu cần runtime config → dùng lệnh `hermes config set ...` (CLI)
4. KHÔNG bypass guard bằng cách edit raw file — Hermes check signature/hash

### ⚠️ Subagent timeout pitfall — 10/07 evidence

Khi dispatch subagent để cleanup batch lớn (>500 files), em đụng **timeout 600s** với 17 API calls mà chưa xong.

**Fix cho sau:**
1. **Break thành batch nhỏ hơn** (≤300 files/subagent)
2. **Hoặc dùng `no_agent=true` cron** với shell script thuần (no LLM reasoning needed)
3. **Hoặc tăng `timeout` param** trong delegate_task nếu được hỗ trợ
4. **Verify trước khi dispatch** — nếu task chỉ là mechanical (replace + rewrite), viết Python script + chạy trực tiếp qua terminal, KHÔNG cần LLM subagent

### Self-check gates BẮT BUỘC (cập nhật 10/07)

```
[ ] File sắp save có path nằm trong /Volumes/Storage-1/?  (anh mandate 10/07)
[ ] Nếu nằm ngoài /Volumes/Storage-1/ → có phải project worktree riêng?  (Pocket3, wiki/projects/tuan-anh-*)
[ ] Nếu nằm trong ~/ → CÓ LÝ DO HỢP LỆ?  (KHÔNG lý do = FAIL → route vào outputs/)
[ ] Nếu nằm trong ~/.hermes/ → có phải runtime?  (state.db, sessions, logs, .git, venv = OK; cache = FAIL)
[ ] File thuộc loại nào?  → route vào outputs/<subdir>/ đúng
[ ] Folder có tmp/ chưa?  → nếu chưa → mkdir
[ ] KHÔNG tạo folder con lồng?
[ ] KHÔNG tự copy/sync Drive?
[ ] Nếu cleanup file cũ → ĐÃ HỎI ANH chưa?
```

**Nếu 1 gate fail → STOP, không hành động, hỏi anh hoặc tự route lại.**