---
name: default-project-hub-pattern
title: Default Project + hub.md Pattern
description: Wire up a project as the agent's persistent default across all future sessions. Use when user explicitly says "set this as my default project", "thiết lập đây là project mặc định", or names a project they want to keep working on. Creates a three-tier loading structure (project hub.md + wiki entity + persistent memory) so every new session auto-discovers the project, its voice, voice rules, and workflow without re-onboarding.
created: 2026-06-13
updated: 2026-06-13
type: skill
tags: [project-management, context-engineering, memory, wiki, onboarding]
confidence: high
---

# Default Project + hub.md Pattern

When a user designates a project as their **persistent default** ("từ nay đây là project mặc định của em", "set this as the default project"), wire it up in three tiers so future sessions pick it up automatically — without re-explaining the project from scratch.

## When to use

Trigger when the user says any of:
- "đây là project mặc định" / "set this as the default project"
- "từ session sau làm việc trong project X"
- "review project X và thiết lập làm default"
- "em cứ assume project X là của anh"

Do NOT use when:
- User is just exploring a folder (one-off read)
- User asks to set up a new project from scratch (use `gsd-new-project` or `prototype` instead)
- User just wants to remember a path (use `memory` only)

## The Three-Tier Pattern

```
┌────────────────────────────────────────────────────────┐
│  Tier 1: PROJECT HUB (project root: hub.md)           │
│  → Project's authoritative file index + voice + rules  │
├────────────────────────────────────────────────────────┤
│  Tier 2: WIKI ENTITY (wiki/entities/<name>.md)         │
│  → Cross-session discoverability from the agent's KB   │
├────────────────────────────────────────────────────────┤
│  Tier 3: PERSISTENT MEMORY (memory tool)                │
│  → Injected every turn; tells agent the project name   │
└────────────────────────────────────────────────────────┘
```

All three tiers MUST be created in the same turn. None alone is enough.

## Tier 1: hub.md (in the project root)

Create `<PROJECT_PATH>/hub.md` with this structure:

```markdown
# <Project Name> — Hub

> **Project mặc định của em (User's Hermes Agent)**
> Set as default: YYYY-MM-DD
> Path: `/absolute/path/to/project/`

## 🎯 Project Goal
<one paragraph — what the project is building>

## 📁 Cấu trúc Project

### 1. Guidelines (Kim chỉ nam — ĐỌC TRƯỚC)
- `guideline-1.md` — <one-line description>
- `guideline-2.md` — <one-line description>

### 2. Roadmap & Chiến lược
- `roadmap.md` — <one-line description>

### 3. Phân tích / Case studies
- `analysis-1.md` — <one-line description>

### 4. Kịch bản / Content
- `script-pack-1.md` — <one-line description>

### 5. Trend / Input feeds
- `Trend_Updates/` — <what lives here>

## 🎬 <Nội dung / Voice / Niche>
<3-5 bullets covering the project's content pillars>

## 🧠 Niche & Voice
- Niche: <one sentence>
- Voice: <pronouns + tone — cố định>

> **⚠️ Voice capture is the #1 priority for hub.md.** If user changes voice preferences mid-project (e.g. loại bỏ "anh + mấy con vợ" → trung tính), update hub.md, wiki entity, AND memory entry in the SAME turn. Embed a dated note in each.

## 📐 Quy tắc BẮT BUỘC
<3-7 hard rules the agent must enforce>

## 📊 Mục tiêu
<concrete 30/60/90 day targets if applicable>

## 🔄 Khi bắt đầu session mới
1. Đọc `hub.md` này trước
2. Check `<input feeds>/` mới nhất
3. Load guidelines tương ứng với task
4. Áp dụng voice "<pronouns>" cố định
5. Nhắc user chạy series theo tỷ lệ <X>/<Y>

## 📝 Log
- **YYYY-MM-DD** — Set làm project mặc định. Tạo hub.md. <one-line summary of contents>.
```

## Tier 2: Wiki entity (in the user's wiki)

Create `<WIKI>/entities/<project-slug>.md`:

```markdown
---
title: <Project Name>
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: project
tags: [project, <domain1>, <domain2>]
confidence: high
relationships: [<linked-concept-1>, <linked-concept-2>, <user-profile>]
---

# <Project Name>

> **ĐÂY LÀ PROJECT MẶC ĐỊNH CỦA EM (<User>'s Hermes Agent)**
> Set as default: YYYY-MM-DD

## Path
`<absolute/project/path>`

## Goal
<one paragraph>

## 3 Trụ / Pillars / Sections
<3-5 bullet points of the project's main axes>

## Files Trong Project
- `hub.md` — Project overview, file index
- `<guideline>.md` — <description>
- <...>

## Voice & Pronouns
- Xưng hô: "<xưng hô>" (CỐ ĐỊNH)
- Tone: <tone description>

## Mục tiêu <timeframe>
- <target 1>
- <target 2>

## Quy tắc BẮT BUỘC
- <rule 1>
- <rule 2>

## Workflow khi bắt đầu session mới
1. Đọc `hub.md` trước
2. Check `<input feeds>/` mới nhất
3. Load guidelines tương ứng task
4. Áp dụng voice "<xưng hô>" cố định
5. Nhắc user chạy series theo tỷ lệ <X>/<Y>

## Related
- [[<linked-concept-1>]] — <description>
- [[<linked-concept-2>]] — <description>
- [[<user-profile>]] — User profile + voice
```

Then:
- Add a row to `<WIKI>/index.md` under the "Projects" or auto-ingest section
- Add a dated log entry to `<WIKI>/log.md`: `## [YYYY-MM-DD] project-default | <one-line summary>`

## Tier 3: Persistent memory entry

```python
memory(action="add", target="memory",
  content="Default project = <Project Name> (set YYYY-MM-DD). Path: <absolute/path>. Hub: hub.md. Niche: <one-line>. Voice cố định: '<pronouns>'. Tỷ lệ: <X> : <Y>. Mỗi session mới tự load hub.md + <input feeds>/ trước.")
```

**Memory hygiene:** If memory is at the cap, REMOVE old one-off task entries first (they have no value past 7 days) before adding this durable fact. Don't replace durable facts (e.g. user preferences, voice rules, environment quirks).

## Pitfalls

### 0.5. (NEW 2026-06-17) Multi-Phase Project ≠ Single-Phase — Use `project-workflow-v2` Instead

**The trap:** This skill is optimized for SINGLE-PHASE projects (one hub, current state, voice + rules). For MULTI-PHASE projects (3+ phases, 5+ agents, multi-month timeline), use `project-workflow-v2` skill instead.

**Decision matrix:**
| Project shape | Skill to use |
|---------------|--------------|
| Single-phase, ongoing (Content Creator 1-trụ days, daily ops) | `default-project-hub-pattern` (this skill) |
| Multi-phase, multi-month (Content Creator 3 trụ over 45 days, multi-agent) | `project-workflow-v2` |
| Multi-month + 5+ agents + verify-before-next | `project-workflow-v2` |
| One-off experiment / prototype | `prototype` skill |

**When to switch from this skill to project-workflow-v2:**
- User says "phases", "milestones", "multiple steps", "nhiều tháng"
- User says "track tasks", "log mỗi action", "verify trước khi next"
- Project has > 5 agents participating
- Timeline > 2 weeks

**Migration path:** If you started with `default-project-hub-pattern` and project grew:
1. Create `wiki/projects/{project-id}/phases/`, `tasks/`, `actions/`, `logs/` folders
2. Move the hub.md content INTO `wiki/projects/{project-id}/hub.md` (project-specific)
3. Keep `wiki/entities/{project}.md` for cross-session discoverability
4. Use `project-workflow-v2` for new phases/tasks going forward

**Real session (2026-06-17):** Content Creator project was set up with `default-project-hub-pattern` on 13/06. On 17/06, user said "dự án lớn nhiều ngày nhiều tháng" → migrated to project-workflow-v2. Hub.md content reused, but added phases/tasks/actions/logs structure.

### 0. (NEW 2026-06-13) Hard Rule: QUALITY BAR — research must have evidence, never guess

When working on Content Creator (or any project with a "đọc file → đề xuất" workflow), user has set a **HARD RULE** that overrides the default "just be helpful" agent behavior:

1. **KHÔNG trả lời chung chung.** Every claim must be specific.
2. **KHÔNG tự đoán.** If the user's request has ambiguity (which timeline? which day? which file?), ASK before recommending — use `clarify` with 3-4 concrete options.
3. **KHÔNG bịa đặt thông tin.** If you cite a number, a stat, a guideline rule, or a date, it must trace back to a file you actually read.
4. **Mọi research phải có bằng chứng:** URL nguồn chính thức + ngày truy cập + đối chiếu ≥2 nguồn độc lập (for external research beyond the project's own files).
5. **Không chắc → PHẢI đặt câu hỏi khai thác trước khi trả lời.** Max 1-3 focused questions, not 6 generic ones.

**Anti-pattern (DO NOT REPEAT — session 2026-06-13):**
- User: "vào project content creator, đọc file, gợi ý kịch bản cho hôm nay là ngày thứ 2"
- BAD: I read 3 timeline files, picked "ngày thứ 2" by counting from 13/06/2026 (assumed), and built a recommendation WITHOUT asking which timeline (Series 0 đồng vs Pocket 3 vs Lớp vỡ lòng).
- GOOD: I used `clarify` with 4 timeline options. User picked "tự chọn tối ưu nhất" → then I read the files, analyzed by 4 verifiable criteria (setup, momentum, viral potential, CTA strength), and recommended E2 with the file path + section + reasoning all cited.

**Embed in hub.md** (under "Quy tắc BẮT BUỘC") for any project where this rule applies:
```markdown
## 📐 Quy tắc BẮT BUỘC
- [Quality Bar] KHÔNG trả lời chung chung / KHÔNG tự đoán / KHÔNG bịa đặt
- [Quality Bar] Mọi research phải có bằng chứng (URL + ngày truy cập + ≥2 nguồn)
- [Quality Bar] Không chắc → đặt câu hỏi khai thác trước khi hành động
```

**Embed in memory** (as QUALITY BAR entry, marked BẮT BUỘC MỌI RESPONSE) so it survives across sessions and overrides any "be helpful, just guess" default.

**Lesson (the user's frustration, captured 2026-06-13):** "Em không trả lời chung chung hoặc tự đoán hoặc bịa đặt thông tin mà mọi thông tin em cung cấp cho anh cần phải qua kiểm tra kĩ lường cũng như có bằng chứng research rõ ràng!" — this was a real correction after I made a bad assumption about "ngày thứ 2" in the Content Creator project. The fix is NOT to ask 6 questions (user finds that annoying too), it's to ask 1-3 sharp questions when ambiguity is high.

### 1. Treating it as a one-off
If you only create hub.md without the wiki entity + memory entry, the next session won't know the project exists. Always wire all three tiers.

### 2. Forgetting voice/tone in hub.md
The single most important thing hub.md captures is the voice ("anh" + "mấy con vợ", NOT "anh" + "các bạn"). Without it, every future session reverts to default pronouns.

**Voice changes are common — embed a dated update protocol.** When user says "loại bỏ voice X" or "đổi sang voice Y" mid-project, you must:
1. Update hub.md (project)
2. Update wiki entity
3. Update memory entry (replace old voice fact)
4. Update any skill docs that reference the old voice (e.g. `tiktok-viral-script` for Content Creator project)
5. All in the SAME turn — don't leave stale voice rules around

**Anti-pattern:** Update only memory, leave wiki + hub.md with old voice → next session loads wiki, sees old voice, applies it incorrectly.

### 3. Memory write rejected due to cap
If the memory tool returns "exceeds limit", you need to:
1. List current entries
2. Remove the oldest one-off task entries (these have no lasting value)
3. Re-add the durable default-project fact

Don't just give up — clean up the noise first.

### 4. Hub.md becomes a stale dump
After creation, hub.md will drift from reality. Each time you create a new major file in the project, update hub.md's file index. Add a "📝 Log" section at the bottom and append a dated entry.

### 5. Wiki entity exists but isn't linked
A wiki page that no other page links to is invisible. Make sure to:
- Add at least 2 wikilinks in the body (relationships field in frontmatter)
- Add a row in `<WIKI>/index.md`

### 6. Don't recreate what's in user's CLAUDE.md / AGENTS.md
If the project already has a CLAUDE.md or AGENTS.md, treat THAT as Tier 1 instead of inventing a new hub.md. Only create hub.md if no rules file exists.

### 7. The "User added new files" refresh pattern (added 2026-06-13)
When user comes back and says "anh mới thêm file mới, hãy review lại project" — do NOT rebuild hub.md from scratch. Instead:

1. `ls -la` + sort by mtime → find files newer than hub.md
2. `read_file` the 3-5 most recent new files (titles + first 50 lines each — don't read the whole thing)
3. Detect if they form a new SYSTEM (numbered 00-03, or pattern like "X phần 1/2/3")
4. Rewrite ONLY the file index + log section of hub.md
5. Update memory entry to mention the new sub-system (if it changed the project's mental model)
6. Send Telegram summary listing the new files + what they replace/supplement

**When to refresh hub.md vs leave alone:**
- 1-2 random new files → just update file index + log
- 3+ files forming a new sub-system (00/01/02/03 pattern) → rewrite file index sections, add a "🆕 Hệ thống SỐ" table at top
- File count > 20 → consider adding a "Quick reference" table at top of hub.md

**Anti-pattern:** Re-reading every file from scratch when user added 5 files → wastes tokens + risks overwriting existing structure. The file index is the only thing that needs updating; the rest of hub.md is stable.

**Files referenced in sub-system doc but not yet created (gap detection):**
When a numbered file like `00-ban-do-tong.md` references "Trạm điều hành kênh (HTML)" or "Ứng dụng thực tế theo tình huống" that don't exist yet → list them in your report as "CÒN THIẾU" so user knows what to create next. Don't pretend they exist.

### 8. Voice/voice-rule change detection from sibling subagents
When a sibling subagent patches a memory entry, the replacement string may be SHORTER than the original (compresses voice fact to fit). Always re-read the memory file after a sibling writes to it, instead of assuming your previous entry is intact.

**Signal:** `memory` tool returns `Entry replaced` or `Entry removed` from another agent. Verify with `read_file ~/.hermes/memories/MEMORY.md` before relying on memory contents in the same turn.

### 9. (NEW 2026-06-16) "User added new files, review + restructure" — extends Pattern #7

When user says "anh mới thêm file mới, hãy review lại project" AND/OR "truy cập kênh TikTok X, xem video, rút bài học, tái cấu trúc" — this is a 2-part compound task:

**Part A: Re-review project** (follow Pattern #7)
1. `ls -la` + sort by mtime → find files newer than hub.md
2. `read_file` the new files (titles + first 50 lines)
3. Detect sub-system pattern (numbered 00-03, or pattern like "X phần 1/2/3")
4. Rewrite ONLY the file index + log section of hub.md
5. Update memory if sub-system changed the project's mental model

**Part B: Competitor analysis + restructure** (NEW pattern from 2026-06-16 session)

Trigger: User shares a TikTok/YouTube channel URL + "xem tất cả video + rút bài học + tái cấu trúc project"

Workflow:
```
1. yt-dlp --flat-playlist → get metadata for ALL videos (URL, title, view_count)
2. Sort by view_count → pick top 3-5 viral + 1-2 recent
3. For each video:
   - yt-dlp -F → list formats
   - **Use `h264_540p_*-0` format** (TikTok không có audio-only standalone)
   - ffmpeg -ar 16000 -ac 1 → extract audio for Whisper
   - mlx_whisper --model mlx-community/whisper-large-v3-mlx --output-format srt → transcript (cached local)
   - ffmpeg -vf "fps=1/15,scale=320:-1" -vframes 4 → 4 frames
   - mcp_MiniMax_understand_image → visual analysis (NOT vision_analyze)
4. Tổng hợp: 5 bài học lõi + so sánh project + đề xuất tái cấu trúc
5. ASK USER FIRST: "Anh muốn em sửa trực tiếp hay tạo file mới chứa đề xuất?"
6. After user choice: patch 1 file phân tích mới + update 1-2 file guideline có bài học liên quan
7. Update wiki log + memory nếu cần
```

**Real failure (2026-06-16) to avoid:** Em assumed "anh muốn em sửa trực tiếp" mà không hỏi trước. User đã chọn option "sửa trực tiếp" (option 2) khi em clarify, nhưng lesson là: ALWAYS clarify before structural changes to existing files. Ngay cả khi có vẻ obvious.

**Step 5 MUST USE `clarify` tool** with options:
- A) Tạo file mới chứa bài học, KHÔNG sửa file cũ
- B) Sửa trực tiếp hub + 1-3 file guideline có bài học liên quan
- C) Gửi tóm tắt trước, anh quyết sau
- D) Chỉ cần phân tích, KHÔNG tái cấu trúc

**Update tiktok-viral-script skill** with reference file `competitor-u40hoc-xaykenh-analysis.md` (5 bài học + 5 hook mới #13-17 + workflow pitfalls). This skill update ensures the next session knows how to do competitor analysis without re-deriving the workflow.

**Sibling skill for DEEP analysis:** Use `tiktok-competitor-deep-analysis` skill when user explicitly asks for 50+ clip stratified sampling (not just 4 viral). Created 2026-06-16 from the 50-clip @u40hoc.xay.kenh session. See `references/50-clip-workflow-notes.md` for full workflow.

**Real failure (2026-06-16) — sample size matters:** User asked for "ít nhất 50 clip" but the first analysis only covered 4 viral clips. The 4-clip sample produced a wrong conclusion (CTA "provoke" listed as pattern #5), corrected by 50-clip analysis (CTA "specific action" 42%, provoke 4%). Pattern #5 in 04-phan-tich-khoa-hoc-u40hoc-xaykenh.md must be treated as DEPRECATED. Always cross-check viral-only analysis against a larger stratified sample before committing to conclusions.

### 10. (NEW 2026-06-16) Folder-based Restructure — distinct from Pattern #9

When user says **"cấu trúc lại file trong project"** / "tổ chức lại folder" / "move file vào folder cho gọn" — this is a **different task** from Pattern #9 (which is about updating hub after new files appear). This pattern is about **moving existing files into folder structure + fixing broken wikilinks**.

**Trigger phrases:**
- "cấu trúc lại file trong project" / "tổ chức lại folder"
- "gộp file theo mục đích" / "phân loại lại"
- "root directory có quá nhiều file, dọn lại"
- "move mấy file nghiên cứu vào folder riêng"

**When to use this pattern vs Pattern #9:**

| User intent | Pattern |
|---|---|
| "anh mới thêm file mới, review + update hub" | Pattern #9 (light touch) |
| "cấu trúc lại project, move file vào folder" | **Pattern #10** (this — heavy restructure) |
| "viết thêm file mới X" | Just write file + update hub |
| "dọn dẹp project" | Could be either — clarify |

**Workflow: 5-step folder restructure**

1. **Inventory + classify** — `ls -la` root, sort by mtime. Categorize each file by PURPOSE (not by name):
   - `Analysis/` — research, case studies, competitor analysis, roadmap research
   - `Operations/` — progress, SOP, voice profile, tiến độ tracker
   - `Trend_Updates/` — date-based trend files (already exists in most projects)
   - `Raw/` — data thô: transcripts, contact sheet, screen recordings
   - `Archive/` — workflow artifacts, old versions, deprecation
   - Root: keep only "system" files (hub + numbered system 00-03 + main guidelines + scripts + UI tools)

2. **Create folders + move files** — use `mv` in a single batch:
   ```bash
   mkdir -p Analysis Operations Raw Archive
   mv <file1> Analysis/ && mv <file2> Analysis/ && ...
   ```
   For dated workflow artifacts (e.g. `compass_artifact_wf-*.md`):
   ```bash
   mkdir -p Archive/2026-06-15-compass-artifacts
   mv compass_artifact_*.md Archive/2026-06-15-compass-artifacts/
   ```
   ⚠️ **Preserve date in archive folder name** — enables future "find old workflow by date".

3. **Fix broken wikilinks** — every `[[file]]` and `path/to/file.md` reference in the project must be updated:
   - `search_files(pattern=<moved_file>, target=content)` — find all references
   - For each match, update path: `[[old]]` → `[[Analysis/old]]` and `path/old.md` → `Analysis/old.md`
   - **HTML files** have relative paths: `./SOP_Proof_Shot_3_San_Pham.md` → `./Operations/SOP_Proof_Shot_3_San_Pham.md`
   - **Use `patch` for markdown, `execute_code` with `read_file` + `str.replace` for HTML** (the `patch` tool fails on HTML)
   - **Pitfall**: when wikilinks use just filename (`[[phan-tich-kenh-hi-imdung]]` without path), `patch` may fail repeatedly if surrounding context matches multiple places. **Fallback**: use `execute_code` with Python `str.replace` for replace_all=True cases.

4. **Rewrite hub.md** with the new folder structure:
   - Lead with a tree diagram of the new layout
   - Add a "Quy tắc vào project" section explaining when to open which folder
   - Update file index to use folder prefixes (`Analysis/04-phan-tich-...`)
   - Append a "📝 Log" entry with: date + intent + new structure summary

5. **Verify no broken references remain** — run `search_files` for each moved file. If 0 matches, references are clean. ⚠️ **Don't skip this step** — broken links silently accumulate.

**Real session example (2026-06-16, Content Creator project):**

User: "Cấu trúc lại file trong project với những cái em vừa phân tích được đi sau đó đề xuất kịch bản ngày 1 cho anh!"

**What I did (single turn):**
1. `ls -la` → 28 files + 4 folders
2. Classified into 4 new folders: `Analysis/` (7 research files), `Operations/` (4 ops files), `Raw/` (transcripts + screenshots), `Archive/2026-06-15-compass-artifacts/` (2 old workflow files)
3. Kept at root: 16 system files (hub + 00-03 + main guidelines + 3 UI tools + 3 script files)
4. Moved 11 files via batch `mv` commands
5. Fixed 4 broken wikilinks (3 in 8-dang-content-chi-dan.md, 1 in checklist-4-tru-cot.html)
6. Rewrote hub.md with new tree + "Quy tắc vào project" section
7. Used `execute_code` with Python `str.replace` for the 2 stubborn wikilinks in 8-dang-content (the `patch` tool kept failing despite unique context)
8. Wrote kịch bản "Ngày 1" → `Operations/kich-ban-ngay-1-5-cai-dat-camera.md`

**Verification step I added:** `search_files(pattern=<moved_file>, target=content)` for each moved file, ensure 0 remaining references with old path. If found → patch.

**Pitfalls specific to this pattern:**

- ⚠️ **HTML files use different patch strategy** — `patch` tool's fuzzy matching often fails on HTML minified strings. Use `execute_code` with `read_file` + `str.replace` instead.
- ⚠️ **Don't move UI tools** — `tram-dieu-hanh-kenh.html` and `checklist-4-tru-cot.html` are referenced by 3+ other files. Keep at root unless you're also updating all references in the same turn.
- ⚠️ **Don't move `Trend_Updates/` content** — it has its own organic date-based naming convention. Leave it alone.
- ⚠️ **Compass artifact files** (from `claude-code` orchestrator workflows) are session-specific — archive with date, don't keep at root.
- ⚠️ **Backup before bulk `mv`** — if project uses git, the moves will be detected as renames. If not, just trust the `mv` (it's atomic on same filesystem).

**Compound task signal:** When user says "cấu trúc lại X, sau đó [action Y]" — treat as 2-part task. The "sau đó" indicates the user wants BOTH done, not just one. In the 2026-06-16 session, "sau đó đề xuất kịch bản ngày 1" meant: restructure FIRST, then write script. Don't merge into one step.

### 11. (NEW 2026-07-24) INDEPENDENT PROJECT RULE — Topic-fit check BEFORE save

**The trap:** Em đã nhầm save VuiVe research (YouTube channel analysis @1.18M subs) vào `wiki/projects/learn-google-flow/vuive-research/` thay vì tạo project độc lập `wiki/projects/vuive-channel-research/`. User phải dừng em: *"đây là project độc lập không thuộc bất cứ project nào khác hết!"*

**Rule:** Trước khi save bất kỳ file nào vào `wiki/projects/<existing-project>/`, check topic có thực sự thuộc project đó không. Dùng checklist 3 câu:
1. Mục đích chính của project hiện tại là gì? (đọc hub.md nếu chưa rõ)
2. File em sắp save phục vụ mục đích đó không?
3. Nếu câu 2 = "không" hoặc "liên quan gián tiếp" → TẠO PROJECT MỚI, không nhét vào project hiện có.

**Examples of independent projects (theo 24/07 wiki state):**

| Project | Topic | KHÔNG thuộc về |
|---|---|---|
| `learn-google-flow/` | Học Google Flow AI studio (plan ULTRA) | ❌ VuiVe research, ❌ tiktok script, ❌ shop cầu lông |
| `vuive-channel-research/` | Research kênh YouTube @VuiVe | ❌ Google Flow tools, ❌ content calendar cầu lông |
| `tuan-anh-badminton/` | Shop vợt cầu lông | ❌ TikTok review linh tinh, ❌ YouTube research |
| `tuan-anh-review-tiktok/` | TikTok Shop affiliate review | ❌ Voice clone, ❌ VuiVe clone |

**When unsure — ask user.** Verbatim from 24/07: *"đây là project độc lập không thuộc bất cứ project nào khác hết!"*

**Recovery if missaved:** Move files using `shutil.move()` from wrong location → correct location. Update paths in moved files (relative paths often still work). Update both hub.md files. Update `wiki/log.md` if it exists.

**Anti-pattern:** Save vào project "gần giống nhất" vì lười tạo folder mới. Topic-fit > convenience.

### 12. (NEW 2026-07-24) Search filesystem BEFORE writing new research — extends Pattern #7

**The trap:** User bảo "em không thấy bất cứ file tài liệu nào về nghiên cứu kênh VuiVe". Em đã viết lại research từ đầu — nhưng thực tế có SẴN 4 file VuiVe research ở:
- `wiki/concepts/youtube-channel-vuive-content-script-analysis-2026-07-11.md`
- `wiki/concepts/youtube-channel-vuive-visual-branding-analysis-2026-07-11.md`
- `~/Workspace/Claude/Projects/YouTube Tổng Hợp/01_Phan_Tich_VuiVe_va_Ke_Hoach_Kenh_Moi.md`
- `~/Workspace/Claude/Projects/YouTube Tổng Hợp/02_UPDATE_Pivot_Format_Tong_Hop_VuiVe.md`

**Rule:** Khi user nói "em không thấy file X" / "anh không thấy tài liệu nào về Y" → **SEARCH FILESYSTEM FIRST** across multiple locations:
- `~/.hermes/wiki/concepts/` (wiki entities + concept docs)
- `~/.hermes/wiki/projects/<other-projects>/` (cross-project)
- `~/Workspace/Claude/Projects/<topic>/` (Claude Code artifacts)
- `/Volumes/Storage-1/Hermes/` (Storage 1, cross-machine)
- `~/Downloads/` (downloaded PDFs)
- `~/.hermes/autoresearch/` (research archive)

Use `search_files(pattern=<keyword>, target=files, path=<root>)` recursively. Then grep for keywords if filename search misses.

**Anti-pattern:** Assume data missing → re-research from scratch → waste tokens + risk synthesis errors vs the original analysis.

### 13. (NEW 2026-07-24) BEFORE/AFTER unique-ID diff for generation claims

**The trap:** Trong Google Flow session, em báo "thành công" sau khi thấy `images: 41` tăng từ 15. Nhưng thực tế con số đó bao gồm cả ảnh cũ trong DOM — KHÔNG có generation mới. User bắt: *"Em vẫn chưa tạo được bất cứ hình ảnh mới nào, làm lại"*.

**Rule:** Khi verify một generation action (image/video/file creation), PHẢI:
1. Snapshot unique IDs TRƯỚC khi trigger (e.g. `getMediaUrlRedirect?name=<UUID>` IDs trong DOM)
2. Save IDs to `/tmp/<feature>_before_ids.json`
3. Trigger generation action
4. Snapshot unique IDs SAU khi action
5. Compute diff: `set(after_ids) - set(before_ids)` = new items
6. ONLY claim success if diff.size() > 0

**Implementation:**

```python
js = '''
(function() {
    const urls = new Set();
    document.querySelectorAll("*").forEach(el => {
        for (const attr of el.attributes) {
            if (attr.value?.includes("getMediaUrlRedirect")) {
                const m = attr.value.match(/name=([a-f0-9-]+)/);
                if (m) urls.add(m[1]);
            }
        }
    });
    const html = document.body.innerHTML;
    const matches = html.match(/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/g) || [];
    matches.forEach(id => urls.add(id));
    return JSON.stringify([...urls]);
})()
'''
```

**Counter-example (FAIL):** "Before: 15 videos + 47 images. After: 41 images. SUCCESS!" → Wrong because the 41 count includes pre-existing media still in DOM.

**Anti-pattern:** Reporting "X items exist" without checking if X > before_count of unique IDs. Always diff.

### 14. (NEW 2026-07-24) cua-driver page tool for real Chrome session (extends browser-harness)

**The trap:** Em dùng CDP `Runtime.evaluate` qua WebSocket riêng — KHÔNG phải Chrome thật của anh. User phải dừng: *"đây là CDP proxy events ≠ user thật → Google backend reject project cũ"*. Sau đó anh nói project cũ vẫn mở được khi click tay = chứng minh CDP events ≠ user events.

**Correct method:** Dùng `cua-driver` page tool với Chrome thật của anh (đã đăng nhập sẵn). Em đã verify:

```bash
# Find Chrome PID + window
cua-driver list_windows → window 3489 (Google Flow – Studio sáng tạo AI...)
# Run JS in REAL Chrome (not CDP proxy)
echo '{"pid": 85715, "window_id": 3489, "action": "execute_javascript", "javascript": "..."}' \
  | /Users/tuananh4865/.local/bin/cua-driver call page
```

**Actions available:**
- `execute_javascript` — Run JS in real Chrome
- `get_text` — Extract visible text
- `query_dom` — Find elements by CSS selector
- `click_element` — Click element with cursor animation
- `insert_text` — Insert text (CDP Input.insertText IME-style commit — bypasses Slate state sync)
- `type_keystrokes` — Real per-character keystrokes

**Why cua-driver > raw CDP:** Browser state changes are recognized as real user actions. For React/Slate editors that track state via internal models (not DOM), JS `innerText + InputEvent` does NOT sync state — only CDP `Input.insertText` does. cua-driver wraps this correctly.

**When to use:** Any browser automation where the page has auth, stateful UI, or framework state tracking. Avoid raw CDP WebSocket for Chrome that's already running.

## Verification

After wiring, confirm in the same turn:

- [ ] `<PROJECT>/hub.md` exists and contains: Goal, File map, Voice, Rules, Workflow, Log
- [ ] `<WIKI>/entities/<project>.md` exists with frontmatter + 2+ wikilinks
- [ ] `<WIKI>/index.md` has a new row pointing to the entity
- [ ] `<WIKI>/log.md` has a dated entry
- [ ] Memory entry was added (verify by re-running memory list and seeing the new entry)

Test: Next session, say "let's continue the project" — agent should load hub.md and apply the voice without being told.

## Example: Content Creator Project (session 2026-06-13)

User: "Vào `<path>` và review project này sau đó từ nay hãy thiết lập đây là project mặc định của em"

What I did (all in one turn):
1. `ls` + `read_file` for major guideline files (14 files + 2 folders)
2. Created `<PROJECT>/hub.md` with full structure above
3. Created `<WIKI>/entities/content-creator-project.md`
4. Added row to `<WIKI>/index.md`
5. Added dated entry to `<WIKI>/log.md`
6. Added memory entry: "Default project = Content Creator..."
7. Sent Telegram summary to user

Voice embedded: "anh" + "mấy con vợ" (the user's TikTok voice) → next session auto-applies it.

**UPDATE 2026-06-13 — VOICE CHANGED:** Same day, anh said "Loại bỏ hoàn toàn voice anh + mấy con vợ đi". I updated:
- hub.md (project) — "Trung tính, chuyên nghiệp, KHÔNG dùng xưng hô thân mật"
- wiki entity — same
- memory — replaced old voice entry, added IMPORTANT note
- `tiktok-viral-script` skill — patched Voice Rules section + Example scripts header

**Lesson:** When voice changes mid-project, the update must cascade to all dependent skills, not just the project's own hub.md. A voice that was embedded in a skill (tiktok-viral-script) will keep firing that voice every time the skill is loaded — until you patch the skill itself.

## Related

- `context-engineering` (profile `coder`) — broader context-loading patterns (this skill is a specialization)
- `using-agent-skills` — how to discover and load skills
- `wiki-maintenance` — wiki cleanup and structure
- `tiktok-viral-script` — example of a project that benefits from a hub.md
- `tiktok-competitor-deep-analysis` — DEEP 50-clip stratified sampling variant (sibling skill, 2026-06-16)
- `references/sweet-spot-script-workflow.md` — 6-step workflow for writing kịch bản "Ngày 1" from competitor research data (sweet spot driven, voice-aware, shot-list detailed) — NEW 2026-06-16
