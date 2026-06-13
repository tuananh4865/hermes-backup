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
