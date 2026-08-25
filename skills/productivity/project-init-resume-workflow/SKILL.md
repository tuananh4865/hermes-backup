---
name: project-init-resume-workflow
title: Project Init & Resume Workflow (Telegram/Terminal)
description: 4-step workflow BẮT BUỘC khi user nói "tạo project X" / "mở project X" / "resume project X" qua Telegram/terminal. PLAN → CHECKLIST → LOG → EXECUTE. Distinguish from `project-checklist-management` (lightweight CHECKLIST file) and `default-project-hub-pattern` (3-tier setup for DEFAULT project).
created: 2026-06-18
updated: 2026-06-18
version: 1.0
type: skill
tags: [project-management, init, resume, plan, checklist, log, telegram-workflow, idempotent]
confidence: high
related_skills:
  - project-checklist-management
  - default-project-hub-pattern
  - hermes-project-workflow-system
  - multi-agent-orchestrator
---

# Project Init & Resume Workflow

> **Class-level skill** for the **lifecycle event** of starting or reopening a project — distinct from `project-checklist-management` (mid-project tracking) and `default-project-hub-pattern` (3-tier setup for one ongoing default project).
>
> **Anh's mandate (18/06):** User làm việc qua Telegram/terminal → em PHẢI tự setup project structure (PLAN → CHECKLIST → LOG → EXECUTE) TRƯỚC khi execute task đầu tiên. Anh không muốn Kanban/UI overhead — em đọc file yêu cầu trong project folder thay vì chat history.

## When to use this skill

**Trigger phrases from user (Vietnamese OR English):**

| Trigger | Action |
|---------|--------|
| "tạo project X" / "tạo dự án X" / "khởi tạo X" | → INIT |
| "init project X" / "setup project X" | → INIT |
| "mở project mới: X" | → INIT |
| "mở project X" / "mở lại project X" | → RESUME |
| "vào project X" / "resume project X" | → RESUME |
| "tiếp tục project X" / "làm tiếp project X" | → RESUME |
| "làm trong project X" / "làm việc trên project X" | → RESUME |
| "project X đang đến đâu rồi?" / "status project X" | → STATUS |

**Use when:**
- User says one of the trigger phrases above
- User wants to start fresh project or reopen old one
- User wants to track what was done / is doing / todo without Kanban overhead
- Telegram/terminal workflow (no UI)

**Do NOT use when:**
- User asks about a project mid-session without naming it (use `project-checklist-management` for ongoing tracking)
- User asks to set a project as DEFAULT for all future sessions (use `default-project-hub-pattern`)
- User asks for full Hermes infra with sub-agents + CI gates (use `hermes-project-workflow-system`)
- Single-file edit / 1-shot task → just do it, no workflow needed

## The 4-Step Workflow (BẮT BUỘC)

```
┌──────────────────────────────────────────┐
│  Step 1: PLAN                           │
│  → Init: read REQUIREMENTS.md (nếu có)  │
│  → Resume: read hub.md + tasks/ + logs/ │
├──────────────────────────────────────────┤
│  Step 2: CHECKLIST                       │
│  → Verify structure (folders + files)    │
│  → Create todo list in todo tool         │
├──────────────────────────────────────────┤
│  Step 3: LOG                             │
│  → Create logs/{date}-session-{id}.md    │
│  → BEFORE any execution                 │
├──────────────────────────────────────────┤
│  Step 4: EXECUTE                         │
│  → Run first task with loop engine       │
│  → Update log after each significant step│
└──────────────────────────────────────────┘
```

**CRITICAL: KHÔNG skip Step 1-3.** Nếu em nhảy thẳng vào EXECUTE task đầu tiên mà chưa đọc REQUIREMENTS / hub → em sẽ tự đoán và làm sai.

### Step 1: PLAN (đọc user requirements)

**Khi INIT (project mới):**
```bash
# 1. Read REQUIREMENTS.md (nếu user đã có sẵn)
cat /Volumes/Storage-1/Hermes/wiki/projects/{project-id}/REQUIREMENTS.md

# 2. Nếu chưa có → tạo từ template
bash ~/.hermes/scripts/init-project.sh {project-id} "{kpi text}"

# 3. Sau khi init → anh điền REQUIREMENTS.md (goal, KPIs, timeline, phases)
```

**Khi RESUME (project cũ):**
```bash
# Auto-load context
bash ~/.hermes/scripts/resume-project.sh {project-id}

# Output:
# - Project overview (từ hub.md)
# - Requirements (từ REQUIREMENTS.md)
# - Tasks status breakdown (TODO/IN_PROGRESS/DONE/FAILED/BLOCKED)
# - 3 most recent session logs
# - Suggested next action
```

**Em phải có mental model rõ ràng về:**
- Project là gì (goal từ REQUIREMENTS)
- Đang ở phase nào (từ hub.md hoặc phases/)
- Task nào chưa xong (status != DONE)
- Có blocker gì không (status FAILED/BLOCKED > 24h)

### Step 2: CHECKLIST (verify + plan)

**Auto-verify structure:**
```bash
bash ~/.hermes/scripts/check-init-compliance.sh
# Checks 5/5: scripts exist + executable, shared ref exists, SOUL.md references, templates exist

bash ~/.hermes/scripts/check-project-compliance.sh {project-id}
# Checks: hub.md exists, phases/tasks structure, YAML fields, no stuck > 24h
```

**Tạo todo list cho task hiện tại (dùng `todo` tool):**
```python
todo(action="write", todos=[
    {"id": "1", "content": "Đọc REQUIREMENTS.md / hub.md", "status": "in_progress"},
    {"id": "2", "content": "Đọc tasks/*.md → list active tasks", "status": "pending"},
    {"id": "3", "content": "Load skill liên quan (nếu task yêu cầu)", "status": "pending"},
    {"id": "4", "content": "Execute task đầu tiên", "status": "pending"},
    {"id": "5", "content": "Log action sau mỗi step quan trọng", "status": "pending"},
    {"id": "6", "content": "Verify trước khi report DONE", "status": "pending"},
])
```

### Step 3: LOG (ghi session log TRƯỚC khi làm)

**Template: `logs/{YYYY-MM-DD}-session-{short-id}.md`**

```markdown
---
title: Session log {date}
created: YYYY-MM-DD
type: session-log
project_id: {project-id}
phase_id: {phase-id (nếu có)}
task_id: {task-id (nếu có)}
---

# Session YYYY-MM-DD — {Project name}

## 📥 Input từ user
> {user message nguyên văn}

## 🎯 Goal của session
{1 câu tóm tắt}

## 📋 Plan
{Copy từ Step 2 CHECKLIST}

## ⚙️ Actions (update trong session)
- [HH:MM] {action description}

## 🏁 Result (update cuối session)
{output summary}

## 📌 Next (cho session sau)
{1-3 bullet}
```

### Step 4: EXECUTE

- Apply `hermes-project-workflow-system` Loop Engine 6 steps (nếu project > 2 tuần)
- Hoặc apply simpler loop nếu < 2 tuần
- Update session log sau mỗi action quan trọng
- Verify trước khi report DONE

## Scripts (3 scripts đã setup sẵn 18/06)

### `bash ~/.hermes/scripts/init-project.sh <project-id> [kpi]`
- Tạo folder structure 4-layer (`phases/`, `tasks/`, `research/`, `actions/`, `decisions/`, `logs/`)
- Copy template `hub.md` + `task.md` từ `_template/`
- Tạo `REQUIREMENTS.md` rỗng cho anh điền
- Tạo session log init
- Auto RUN `check-project-compliance.sh`

**Idempotent:** chạy nhiều lần OK, chỉ tạo file/folder còn thiếu.

### `bash ~/.hermes/scripts/resume-project.sh <project-id>`
- Đọc `hub.md` + REQUIREMENTS + tasks status + 3 logs mới nhất
- Generate context summary cho session mới
- Read-only (không modify gì)
- Suggest next action

### `bash ~/.hermes/scripts/check-init-compliance.sh`
- CI gate verify workflow 100% applied
- Checks: 3 scripts exist + executable + shared ref exists + SOUL.md references + templates exist
- Should be 8/8 PASS at any time

## Project Structure (BẮT BUỘC mọi project)

```
/Volumes/Storage-1/Hermes/wiki/projects/{project-id}/
├── hub.md                  # Project overview, KPIs, current state
├── REQUIREMENTS.md         # User requirements (em đọc file này thay vì chat history)
├── phases/                 # Layer 1: Giai đoạn lớn (2-4 tuần)
├── tasks/                  # Layer 2: Task trong phase (1-3 ngày)
├── research/               # Layer 2.5: Research outputs
├── actions/                # Layer 3: Action log (1-8h)
├── decisions/              # Quyết định quan trọng
└── logs/                   # Session logs (auto-generated)
```

## How this skill differs from sibling skills

| Skill | Scope | Trigger | Output |
|-------|-------|---------|--------|
| **project-init-resume-workflow** (this) | Lifecycle event: init OR resume | "tạo/mở/resume project X" | Setup structure + load context |
| `project-checklist-management` | Mid-project tracking | "log/checklist/tracking" | CHECKLIST file với 4 sections |
| `default-project-hub-pattern` | Set project as DEFAULT | "set this as default" | 3-tier (hub + wiki entity + memory) |
| `hermes-project-workflow-system` | Heavy infra for system projects | System-level + multi-agent | 6-step Loop Engine + CI gates |

**Decision rule:** Nếu user nói "tạo/mở/resume" → THIS skill. Nếu "log/checklist" → project-checklist-management. Nếu "default" → default-project-hub-pattern. Nếu > 2 tuần + multi-agent → hermes-project-workflow-system.

## Common pitfalls

### 0. (NEW 23/06) Fable-5 mandate violation — skip workflow script for "quick" project setup

**Trap:** User says "làm project X" / "tạo game đơn giản" / "build prototype". Agent thinks it's a "quick" task, skips running `init-project.sh` / `bootstrap-project.sh`, creates just a single `wiki/projects/{project_id}.md` file with all the content inline. The "quick" project then becomes the long-term home for the work, but the project structure is wrong from session 1.

**Real session 2026-06-23:** Anh caught em skipping Fable-5 + Loop Engineering when setting up `mini-rpg-games` (1 file `.md` instead of folder). Message: *"Có vẻ em quên mất không áp dụng fable 5 system và loop engineering vào rồi đúng không? Vì chưa thấy em verify plan"*

**Fix:**
1. **EVERY project — no exceptions.** Even "small" projects. Especially "prototype" projects that turn into long-running ones.
2. Before creating ANY project file, run:
   ```bash
   bash ~/.hermes/scripts/check-init-compliance.sh
   ```
3. If `wiki/projects/{project_id}.md` already exists as single file, **immediately restructure** (don't apologize — just fix):
   ```bash
   mv wiki/projects/{project_id}.md wiki/projects/{project_id}/_backup_old_hub.md
   mkdir -p wiki/projects/{project_id}/{phases,tasks,research,actions,logs,decisions}
   ```
4. Then create proper hub.md + dashboard.md + dependency-graph.md.
5. **Run `check-project-compliance.sh {project_id}` BEFORE announcing done** — must show `✅ PASS`.

**Lesson:** "Quick" projects are an excuse to skip workflow. The workflow exists to make ALL projects auditable. Even a 1-hour prototype deserves a proper hub + action log.

### 0b. (NEW 2026-07-13) Init project manually instead of running `init-project.sh`

**Trap:** User says "Tạo project mới" (e.g. "Tạo project mới, project này anh muốn em học cách sử dụng trang https://labs.google/fx/tools/flow..."). Agent reads the trigger, recognizes "create project", but instead of running `init-project.sh <project-id>` to create the canonical 6-folder structure (phases/tasks/research/actions/logs/decisions), it `mkdir -p` only the subfolders it thinks it needs (research/workflows/projects/screenshots/prompts) and writes a single `hub.md`.

**Real session 2026-07-13:** Created `learn-google-flow/` with custom folder structure (research/, workflows/, screenshots/, prompts/, projects/) instead of the canonical phases/tasks/research/actions/logs/decisions. Lost the standard automation hooks (no `check-project-compliance.sh` validation, no session log auto-creation, no task tracking).

**Fix:**
1. **ALWAYS** run `bash ~/.hermes/scripts/init-project.sh <project-id> [kpi-text]` FIRST when user says "tạo project".
2. The script creates the canonical 6-folder structure + hub.md + REQUIREMENTS.md + task template + initial session log.
3. THEN customize inside the structure (e.g. create `research/`, `workflows/`, `screenshots/` as needed inside the standard folders — NOT replace them).
4. The standard folders (`phases/`, `tasks/`, `logs/`, `actions/`, `decisions/`) are NOT optional even for "exploration" projects.

**Lesson:** Even when the project name suggests "exploration" or "learning" (like `learn-google-flow`), the WORKFLOW structure (plan → checklist → log → execute) still applies. Custom research subfolders are fine INSIDE `research/`, not as replacements for the workflow structure.

### 0c. (NEW 2026-07-13) Don't ask "what do you want me to explore" — propose concrete steps

**Trap:** User says "Tạo project mới" + vaguely defines the goal. Agent does exploration then asks "anh muốn em explore feature nào cụ thể?" with 4 options — wasted round-trip when user already gave direction.

**Real session 2026-07-13:** After exploration of Google Flow UI, agent output 4 numbered open questions and asked anh to pick. But anh already said "học cách sử dụng" — the natural follow-up is to ask "anh muốn em TEST tính năng nào trước?", not "anh muốn em làm gì tiếp?". The difference: TEST has a deliverable, "làm gì tiếp" is open-ended.

**Fix:**
1. After exploration, propose CONCRETE next step with deliverable scope (e.g. "test prompt X → render video Y → save to folder Z").
2. If multiple valid paths, propose 2-3 numbered options EACH with concrete deliverable (not abstract questions).
3. **Don't** ask open-ended "what do you want" questions when user gave direction. Direction = execute, with safe default.
4. Use `clarify` only when there is genuine trade-off (cost vs. time vs. irreversible side-effect). For "what feature first?", propose + let user pick from numbered list.

### 1. (NEW 2026-06-18) Nhảy thẳng vào EXECUTE khi nghe trigger word

**Trap:** User nói "mở project content-creator" → em tự động bắt đầu làm task mà KHÔNG chạy resume-project.sh.

**Fix:** ALWAYS run Step 1 (resume-project.sh) FIRST, đọc output, SAU ĐÓ mới execute.

**Anti-pattern (real session 2026-06-18):** Em viết 4 scripts + shared ref nhưng KHÔNG save thành skill ngay → session sau quên pattern này.

### 2. (NEW 2026-06-18) Hỏi clarifying questions khi user đã rõ ràng

**Trap:** Em dùng `clarify` tool với 4 options khi user đã rõ ràng → user frustrated.

**User preference (2026-06-18):** "Anh làm việc với em qua telegram hoặc terminal cho nhanh gọn" → em phải TỰ DECIDE, không hỏi.

**Fix:** Chỉ dùng `clarify` khi:
- Decision có trade-off lớn ($$$, irreversible)
- Multiple valid approaches với unclear best
- Cần user input về subjective preference (voice, style)

KHÔNG dùng khi:
- Đã có default obvious → execute
- User đã nói rõ → execute
- Research có thể tự quyết → execute

### 3. Không tạo REQUIREMENTS.md khi init

**Trap:** Init project mà quên tạo REQUIREMENTS.md → user phải nhắc lại requirements qua chat → dễ quên → sai.

**Fix:** init-project.sh tự động tạo REQUIREMENTS.md với YAML frontmatter + template structure. User chỉ cần điền nội dung.

### 4. Quên update log sau khi execute

**Trap:** Execute task xong nhưng KHÔNG update `logs/{date}-session-{id}.md` → session sau không biết context → re-research → waste tokens.

**Fix:** Sau MỖI step quan trọng (action > 5 phút), append log entry.

### 5. Idempotency không đảm bảo

**Trap:** Chạy `init-project.sh` 2 lần → lỗi vì folder đã tồn tại → user phải manual fix.

**Fix:** Tất cả scripts PHẢI idempotent. Pattern:
```bash
# Check if exists trước khi tạo
if [ ! -f "$path" ]; then
    cp template "$path"
else
    echo "⏭️  skip"
fi
```

### 6. CI gate flag stuck tasks nhưng không escalate

**Trap:** `check-project-compliance.sh` warn task stuck AWAITING_VERIFY > 24h → em note trong report nhưng KHÔNG escalate.

**Fix:** Khi run CI gate + thấy stuck > 24h → em phải explicit:
1. List stuck tasks với age
2. Suggest escalate hoặc pick up lại
3. KHÔNG silently continue

## When to use which project management skill (decision matrix)

| Project shape | Skill | Output |
|---------------|-------|--------|
| User muốn tạo/mở/resume project | **project-init-resume-workflow** (this) | Setup + load context |
| User muốn CHECKLIST + auto-log | `project-checklist-management` | CHECKLIST file |
| User muốn set project làm DEFAULT | `default-project-hub-pattern` | 3-tier setup |
| Hermes system infra (multi-agent, CI) | `hermes-project-workflow-system` | 6-step Loop Engine |
| 1-shot task / Q&A | (none) | Just do it |

## Verification pattern

After running this workflow, verify:

```bash
# 1. Scripts exist + executable
bash ~/.hermes/scripts/check-init-compliance.sh
# Expected: 8/8 PASS

# 2. Project structure valid
bash ~/.hermes/scripts/check-project-compliance.sh {project-id}
# Expected: 0 issues

# 3. Session log created
ls -la /Volumes/Storage-1/Hermes/wiki/projects/{project-id}/logs/
# Expected: {date}-session-{id}.md exists

# 4. Next action clear
# - If RESUME → output suggest next task from status breakdown
# - If INIT → output show "anh cần điền REQUIREMENTS.md"
```

## Reference files

- `references/init-resume-script-specs.md` — Full spec cho 3 scripts (init-project.sh, resume-project.sh, check-init-compliance.sh), arguments, output format, idempotency rules
- `references/trigger-detection-patterns.md` — Regex patterns cho trigger detection (Vietnamese + English), edge cases
- `references/shared-ref-project-init-workflow.md` — Copy of `~/.hermes/profiles/_shared/project-init-workflow.md` (shared reference file) để tham khảo

## Example: Init a new project (verified 2026-06-18)

User: *"Tạo project mới: tiktok-affiliate-q3-2026, KPI 50 triệu doanh thu"*

**Step 1 (PLAN):** Em detect trigger "tạo project", extract project_id = "tiktok-affiliate-q3-2026", KPI = "50 triệu doanh thu"

**Step 2 (CHECKLIST):**
```bash
bash ~/.hermes/scripts/check-init-compliance.sh  # → 8/8 PASS
```

**Step 3 (LOG):** Init script tự tạo session log.

**Step 4 (EXECUTE):**
```bash
bash ~/.hermes/scripts/init-project.sh tiktok-affiliate-q3-2026 "50 triệu doanh thu Q3 2026"
# → Tạo folder + REQUIREMENTS.md + hub.md + task-01-example.md + session log
```

**Output:** Báo cáo Telegram với:
- Folder location
- Bước tiếp theo: "Anh điền REQUIREMENTS.md"
- Trigger words em sẽ nhận: "mở project tiktok-affiliate-q3-2026" → resume

## Related

- `project-checklist-management` — Mid-project tracking (CHECKLIST file)
- `default-project-hub-pattern` — Set DEFAULT project (3-tier)
- `hermes-project-workflow-system` — Heavy infra (6-step Loop Engine + CI)
- `multi-agent-orchestrator` — Decomposition + delegation
- `self-verify-after-workaround` — When user demands strict QA
