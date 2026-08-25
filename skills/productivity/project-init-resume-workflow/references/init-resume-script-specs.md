---
title: Init/Resume Script Specs — Project Init Workflow
created: 2026-06-18
type: reference
tags: [script-specs, init-project, resume-project, idempotent]
---

# Script Specs — Project Init Workflow (3 scripts + 1 injector)

> **Created:** 2026-06-18 (Tuấn Anh mandate — 4-step workflow khi tạo/mở project qua Telegram/terminal)
> **Location:** `~/.hermes/scripts/`
> **Idempotent:** Tất cả scripts chạy nhiều lần OK, không lỗi

---

## 1. `init-project.sh` — Khởi tạo project mới

**Usage:**
```bash
bash ~/.hermes/scripts/init-project.sh <project-id> [kpi]
bash ~/.hermes/scripts/init-project.sh <project-id> --kpi="<kpi text>"
```

**Behavior:**

### Step 1: PLAN — Tạo folder structure
```bash
mkdir -p "$PROJECT_DIR"/{phases,tasks,research,actions,decisions,logs}
```

**Tạo 6 folders:** `phases/`, `tasks/`, `research/`, `actions/`, `decisions/`, `logs/`

### Step 2: CHECKLIST — Copy templates

**hub.md:**
- Nếu CHƯA có: copy từ `_template/hub.md`, replace `project_id: <project-id>` bằng project_id thật
- Nếu CÓ rồi: skip

**REQUIREMENTS.md:** (BẮT BUỘC — file anh điền requirements)
- Nếu CHƯA có: tạo với YAML frontmatter + template có 6 sections:
  - Mục tiêu chính
  - KPIs / Success metrics
  - Timeline
  - Phases (high-level)
  - Constraints / Hard rules
  - Voice / Style (nếu là content)
  - Tools / Skills liên quan
  - Notes từ user
- Nếu CÓ rồi: skip

**tasks/task-01-example.md:**
- Copy từ `_template/task.md`
- Replace `task_id: TEMPLATE` → `task_id: T-01`

### Step 3: LOG — Tạo session log init
```bash
LOG_FILE="$PROJECT_DIR/logs/$(date +%Y-%m-%d)-session-init.md"
```

**Template có 6 sections:**
- Input từ user
- Goal
- Plan (4 steps)
- Actions (timestamp + description)
- Result
- Next (cho session sau)

### Step 4: EXECUTE — Run CI gate
```bash
bash ~/.hermes/scripts/check-project-compliance.sh "$PROJECT_ID"
```

**Expected output:**
- ✅ hub.md exists
- ✅ phases/ has files
- ✅ tasks/ has status field
- ✅ All tasks have owner_role field
- ✅ All active tasks have research_refs field
- ⚠️  Có thể FAIL vì project mới chưa có phase/task — đó là OK

**Final summary:**
```
📌 BƯỚC TIẾP THEO (anh Tuấn Anh cần làm):
  1. Điền REQUIREMENTS.md với goals/KPIs/timeline
  2. Tạo phases/phase-01-{name}.md + tasks/task-{N}-{name}.md
  3. Chạy: bash ~/.hermes/scripts/check-project-compliance.sh {project-id}
```

---

## 2. `resume-project.sh` — Mở lại project cũ

**Usage:**
```bash
bash ~/.hermes/scripts/resume-project.sh <project-id>
```

**Behavior:**

### Step 1: PROJECT OVERVIEW
```bash
TITLE=$(grep -m1 "^title:" hub.md | sed 's/title: //')
STATUS=$(grep -m1 "^status:" hub.md | sed 's/status: //')
UPDATED=$(grep -m1 "^updated:" hub.md | sed 's/updated: //')
# Print + first 30 lines of body
```

### Step 2: REQUIREMENTS
```bash
# Read REQUIREMENTS.md → first 40 lines
```

### Step 3: TASKS STATUS
Count tasks by status:
- ⏳ TODO
- 🔄 IN_PROGRESS
- ⏸️  AWAITING_VERIFY
- ✅ DONE
- ❌ FAILED
- 🚨 BLOCKED

**List active tasks** (status != DONE) với format:
```
• [STATUS] basename — title (owner: owner_role)
```

### Step 4: RECENT LOGS (3 mới nhất)
```bash
RECENT_LOGS=$(ls -1t "$PROJECT_DIR/logs"/*.md | head -3)
# Print first 20 lines of each
```

### Step 5: COMPLIANCE CHECK
```bash
bash ~/.hermes/scripts/check-project-compliance.sh "$PROJECT_ID"
```

### Final summary
**Next action suggestion:**
- Nếu có IN_PROGRESS task → "Em nên tiếp tục task này"
- Nếu có AWAITING_VERIFY task → "Em nên chạy verify cho task này"
- Nếu không có → "User cần tạo task mới hoặc chọn task TODO"

---

## 3. `check-init-compliance.sh` — CI gate

**Usage:**
```bash
bash ~/.hermes/scripts/check-init-compliance.sh
```

**Checks (8/8 để PASS):**

| # | Check | Pass criteria |
|---|-------|---------------|
| 1 | init-project.sh exists + executable | `-f && -x` |
| 2 | resume-project.sh exists + executable | `-f && -x` |
| 3 | check-init-compliance.sh exists + executable | `-f && -x` |
| 4 | profiles/_shared/project-init-workflow.md exists | `-f` |
| 5 | SOUL.md references project-init-workflow | `grep -q "project-init-workflow"` |
| 6 | _template/hub.md exists | `-f` |
| 7 | _template/task.md exists | `-f` |

**Note:** Hiện tại check 7 items (không phải 8) nhưng spec note "8/8 PASS" — fix trong tương lai nếu cần.

**Add SOUL.md check nếu thiếu:**
```bash
# Inject idempotent
bash ~/.hermes/scripts/add-project-init-to-soul.sh
```

---

## 4. `add-project-init-to-soul.sh` — Idempotent injector

**Usage:**
```bash
bash ~/.hermes/scripts/add-project-init-to-soul.sh
```

**Inject vào 6 SOUL.md files:**
- `~/.hermes/SOUL.md` (default profile)
- `~/.hermes/profiles/coder/SOUL.md`
- `~/.hermes/profiles/content-director/SOUL.md`
- `~/.hermes/profiles/research-lead/SOUL.md`
- `~/.hermes/profiles/qa-agent/SOUL.md`
- `~/.hermes/profiles/memory-curator/SOUL.md`

**Marker check:**
```bash
MARKER="PROJECT-INIT-WORKFLOW MANDATE"
grep -q "$MARKER" "$soul_file"
```

**Idempotent:** Nếu đã có marker → skip. Nếu chưa → append block.

**Injected block content:**
```markdown
## 🆕 PROJECT-INIT-WORKFLOW (MANDATORY)

> **Tuấn Anh mandate (18/06):** Mọi lần tạo project mới hoặc mở lại project cũ, em **BẮT BUỘC** chạy workflow 4-step TRƯỚC khi execute task đầu tiên:
>
> **PLAN → CHECKLIST → LOG → EXECUTE**
>
> Lý do: anh làm việc qua Telegram/terminal → em không có context dồi dào → phải tự setup project structure để khi quay lại session sau, đọc file và tiếp tục được ngay.

### Trigger detection
- "tạo project X" / "mở project mới: X" / "init project X" → chạy `init-project.sh`
- "mở project X" / "resume project X" / "tiếp tục project X" → chạy `resume-project.sh`

### 4-Step Workflow
1. **PLAN**: Đọc `REQUIREMENTS.md` (nếu init) hoặc `hub.md` + `tasks/` (nếu resume)
2. **CHECKLIST**: Verify structure + tạo todo list trong todo tool
3. **LOG**: Tạo `logs/{date}-session-{id}.md` TRƯỚC khi làm
4. **EXECUTE**: Chạy task đầu tiên với loop engine 6 bước (nếu project > 2 tuần)

### Scripts
- `bash ~/.hermes/scripts/init-project.sh <project-id> [kpi]`
- `bash ~/.hermes/scripts/resume-project.sh <project-id>`
- `bash ~/.hermes/scripts/check-init-compliance.sh` (CI gate)

### Full reference
- `~/.hermes/profiles/_shared/project-init-workflow.md` — Shared ref (full spec)

### Hard rule
**KHÔNG ĐƯỢC nhảy vào EXECUTE task khi chưa setup project structure.**
**PHẢI đọc REQUIREMENTS.md hoặc hub.md trước.**
```

---

## Idempotency rules (BẮT BUỘC)

Tất cả scripts PHẢI đảm bảo:

1. **Folder creation:** `mkdir -p` (idempotent)
2. **File copy:**
   ```bash
   if [ ! -f "$target" ]; then
       cp "$source" "$target"
       echo "✅ Created"
   else
       echo "⏭️  Exists, skip"
   fi
   ```
3. **YAML placeholder replace:**
   ```bash
   sed -i.bak "s/<placeholder>/actual_value/g" "$file"
   rm -f "$file.bak"
   ```
4. **CI gate:** `bash check.sh` → exit code KHÔNG fail script init (dùng `|| true`)

---

## Edge cases đã biết

1. **`check-project-compliance.sh` line 121 bug:** `[: 0\n0: integer expression expected` khi actions/ empty.
   - Đây là bug có sẵn trước khi init workflow tạo
   - KHÔNG fix trong scope này (out of scope)

2. **`sed -i.bak` trên macOS:** cần `.bak` để work (Linux khác, không cần `.bak`).
   - Đã dùng `.bak` để compatible cả macOS và Linux.

3. **Project folder đã tồn tại:** script KHÔNG error, chỉ skip existing files/folders.

4. **Resume project không tồn tại:** exit 1 với error message "Run init-project.sh first".

5. **CI gate fail vì project mới:** expected behavior, không crash script.

---

## Khi nào cần update scripts này

- Khi `hermes-project-workflow-system` thêm field mới (verify_attempts, escalated_at, etc.) → update init-project.sh + CI gate
- Khi có project class mới cần structure khác (vd: project KHÔNG dùng loop engine) → tạo variant script
- Khi SOUL.md đổi format → update add-project-init-to-soul.sh

---

*Spec created: 2026-06-18 by Hermes per Tuấn Anh mandate 18/06*
*Pattern: 3-piece enforcement (shared ref + idempotent scripts + CI gate)*
