---
name: project-setup-ritual
title: Pre-flight Project Setup Ritual
description: Mandatory onboarding ritual BEFORE any project work — read existing context, setup log/plan/checklist system, then execute. For long-running multi-week/multi-month projects where the user (Tuấn Anh) wants per-action audit trail, dependency tracking, and the agent must always know "task nào ở đâu, when, who, related to what". Load when user says "làm project X", "mở lại project X", "task T-X.Y trong project X", or "em phải tự đọc file yêu cầu trong project trước".
version: 1.0
type: skill
tags: [project-management, onboarding-ritual, pre-flight-checklist, project-setup, workflow]
related_skills:
  - hermes-project-workflow-system
  - project-checklist-management
  - project-workflow-loop-engine
  - multi-agent-orchestrator
  - self-verify-after-workaround
confidence: high
created: 2026-06-18
---

# Pre-flight Project Setup Ritual

> **Class-level skill:** Mandatory 3-phase ritual for ANY project work (new or existing). Setup log system + plan + checklist TRƯỚC khi execute. Distinct from `hermes-project-workflow-system` (ongoing workflow) and `project-checklist-management` (lightweight checklist maintenance).
>
> **Why this exists:** Tuấn Anh explicitly clarified 18/06 — he wants the agent to SELF-READ project requirements files BEFORE working, and to setup log/plan/checklist system as a PRE-FLIGHT step, not as an afterthought.

## When to use this skill

**Trigger phrases from user:**
- "làm project X" / "tạo project X" / "set up project X"
- "mở lại project X" / "tiếp tục project X"
- "task T-X.Y trong project X"
- "research về Z trong project X"
- "em phải tự đọc file yêu cầu trong project"
- "thiết lập để em tạo được plan + checklist cho mọi project"
- "mỗi project mới tạo đều phải tuân thủ workflow"

**Use when:**
- User starts ANY new project (Content Creator, app build, course, research, business)
- User reopens an existing project after a break
- User assigns a task within a known project
- Agent joins a project mid-flight (sub-agent delegation)

**Do NOT use when:**
- 1-shot quick Q&A → just answer
- Pure conversation / clarification → no project context
- User explicitly says "skip planning" or "just do X quickly"

## The 3-Phase Ritual

### Phase 0 — Đọc Project (existing project)

**When:** User says "mở lại project X" / "tiếp tục project X" / "làm task trong project X"

```
□ ls wiki/projects/{project_id}/ — verify structure exists
□ read hub.md → north star, team, scope
□ read dashboard.md → current status, blockers (if exists)
□ read dependency-graph.md → task dependencies (if exists)
□ ls tasks/ → list current tasks + statuses
□ ls research/ → list prior research outputs
□ ls actions/ → check recent activity log
□ Identify gaps: what's TODO? what's BLOCKED? what depends on what?
```

**Output:** Em phải biết trước khi làm gì:
- Project này đang ở phase nào?
- Task nào đang chờ?
- Task em sắp làm phụ thuộc vào task nào khác?

### Phase 1 — Setup Project (new project)

**When:** User says "làm project X" / "tạo project X"

```
□ Run bootstrap script (idempotent):
  bash ~/.hermes/scripts/bootstrap-project.sh {project_id} "{Project Name}" {owner}

  Creates:
  - wiki/projects/{project_id}/ folder
  - 5 subfolders: phases/, tasks/, research/, actions/, logs/
  - hub.md from _template/hub.md (auto-fill placeholders)

□ Edit hub.md → fill NORTH STAR, TEAM, KPI, dependencies
□ Create phase-01-{name}.md in phases/
□ Create first task-{T-01.1}-{name}.md in tasks/ (from _template/task.md)
□ Run compliance check:
  bash ~/.hermes/scripts/check-project-compliance.sh {project_id}
□ Document setup in log: actions/{YYYY-MM-DD}-setup-{project_id}.md
```

**Why this phase matters:** Without hub.md + structure, sub-agents + future sessions have NO context. The user explicitly said "mỗi một project mới tạo đều phải tuân thủ workflow này chặt chẽ" 17/06.

### Phase 2 — Pre-task Checklist (mỗi task)

**When:** Before executing ANY task (after Phase 0 or 1)

```
Bước 1 — RESEARCH (≥2 sources, ≥5 phút)
  □ Đọc task spec: wiki/projects/{id}/tasks/task-{T-NN.M}-{name}.md
  □ Đọc related research files (research_refs field)
  □ Đọc related tasks (related_tasks, depends_on fields)
  □ Load skill nếu task spec yêu cầu (skill_view trước)
  □ Self-check: deliverables rõ chưa? Verify criteria có chưa?

Bước 2 — PLAN (3-7 sub-actions, ≥5 phút)
  □ Break task thành 3-7 sub-actions cụ thể
  □ Mỗi sub-action có: mô tả + expected output + est. time
  □ Identify blockers: cần gì từ upstream? cần tools nào?
  □ Identify risks: có thể fail ở đâu? rollback plan?

Bước 3 — SETUP LOG (1 file log đầu tiên)
  □ Tạo actions/{YYYY-MM-DD}-{T-NN.M}-setup.md
  □ File này chứa: plan từ Bước 2 + checklist đầy đủ
  □ Em commit "em bắt đầu task T-NN.M, plan: [...]"

Bước 4 — EXECUTE
  □ Mỗi sub-action → log file actions/{date}-{T-NN.M}-{action-id}.md
  □ Mỗi output → save research/ với YAML frontmatter
  □ Update task status nếu cần

Bước 5 — VERIFY
  □ Self-check: deliverables đủ chưa? Quality đạt chưa?
  □ Run: bash ~/.hermes/scripts/check-project-compliance.sh {project_id}
  □ Update verify_attempts + last_failure_reason nếu fail
  □ Update dashboard.md (status counters)

Bước 6 — NEXT
  □ Update task status → DONE (nếu pass)
  □ Update dependency-graph.md (nếu task complete mở unlock task khác)
  □ Notify user với evidence (file paths, command output)
```

**Why each step matters:**
- Step 1-2: Research trước + plan trước → work-style preference 17/06 ("em phải research trước khi làm")
- Step 3: Setup log trước khi execute → "log mọi action nhỏ để dễ quản lý" (anh 17/06)
- Step 5: Verify với evidence → work-style preference 17/06 ("em phải verify trước khi done")
- Step 6: Update dashboard → "biết chính xác task nào đang làm" (anh 17/06)

## Decision Tree (auto-trigger cho agent)

```
User message
    │
    ├─ "làm project X" or "tạo project X"     → Phase 1 (setup) + Phase 2 (per task)
    ├─ "mở lại project X" or "tiếp tục X"     → Phase 0 (đọc) → Phase 2 (per task)
    ├─ "task T-X.Y" or "làm task X.Y"          → Phase 0 (quick) + Phase 2
    ├─ "research về Z"                          → Phase 1 mini + Phase 2 (research task)
    └─ "quick question"                         → KHÔNG cần Ritual (1-shot task)
```

## 🚨 Hard Rules (KHÔNG BAO GIỜ VI PHẠM)

1. **KHÔNG execute task** khi chưa chạy Phase 2 (Research + Plan + Setup Log)
2. **KHÔNG skip action logging** — mỗi sub-action = 1 file trong actions/ (≥50 từ)
3. **KHÔNG tạo project mới** mà không có hub.md + template structure
4. **KHÔNG announce done** khi chưa pass Phase 2 Step 5 (Verify) với evidence
5. **KHÔNG modify task spec** của người khác — tạo task mới nếu cần
6. **KHÔNG đoán content task spec** — nếu thiếu info, hỏi orchestrator

## Tool selection matrix (theo workflow class)

| Project class | Use this skill | Then layer with |
|--------------|----------------|------------------|
| User content (TikTok, YouTube, blog) | ✅ Phase 0+2 only (lightweight) | `project-checklist-management` for daily tracking |
| Personal app build (5-30 tasks) | ✅ Full 3-phase | `hermes-project-workflow-system` for heavy infra |
| Multi-month course/business | ✅ Full 3-phase | Both `hermes-project-workflow-system` + `project-checklist-management` |
| Hermes system infrastructure | ✅ Phase 1 only | `hermes-project-workflow-system` for ongoing |

## Files involved (canonical)

```
~/.hermes/profiles/_shared/project-setup-ritual.md    # This skill's source-of-truth
~/.hermes/scripts/bootstrap-project.sh                # Phase 1 idempotent script
~/.hermes/scripts/check-project-compliance.sh        # Phase 2 Step 5 CI gate
~/.hermes/scripts/check-all-compliance.sh            # Unified gate

wiki/projects/_template/hub.md                       # Phase 1 hub template
wiki/projects/_template/task.md                      # Phase 2 task template
wiki/projects/{project_id}/hub.md                    # Read in Phase 0
wiki/projects/{project_id}/actions/                  # Write in Phase 2 Step 3+4
```

## Pitfalls (Tuấn Anh's frustration patterns)

1. **Recommend heavy tools (Kanban GUI, dashboards) when user wants lightweight** — Tuấn Anh works via Telegram/terminal, không cần GUI. Khi propose tools, ALWAYS check user's actual channel first. (Pitfall from 18/06.)

2. **Skip Phase 1 setup, jump to Phase 2** — Agent thinks "Phase 1 không cần vì project đã có structure" — but missing hub.md template fields (team, KPIs) = blind spots for future sessions.

3. **Skip Phase 0 đọc project** — Agent claims "biết project rồi" without reading hub.md. Tuấn Anh caught this 18/06 ("em phải tự đọc file yêu cầu").

4. **Phase 2 Step 5 verify không có evidence** — Agent nói "xong rồi" mà không chạy `check-project-compliance.sh`. Tuấn Anh's #1 frustration — "em phải verify/QA/test trước khi done" (work-style 17/06).

5. **Phase 2 Step 3 setup log bị skip** — Agent bắt đầu execute mà quên tạo `-setup.md` file đầu tiên. Mất audit trail cho 3-5 sub-actions đầu.

6. **Plan trên đầu mà không ghi xuống file** — Tuấn Anh muốn plan phải là FILE (có thể đọc lại, audit), không phải chỉ trong context.

## Verification pattern (Tuấn Anh's #1 preference)

After each phase, verify with evidence:

```bash
# Phase 0 — verify đã đọc
test -f wiki/projects/{id}/hub.md && echo "✅ hub exists"
ls wiki/projects/{id}/tasks/ | wc -l   # count tasks

# Phase 1 — verify setup
test -f wiki/projects/{id}/hub.md && echo "✅ hub created"
test -d wiki/projects/{id}/phases/ && echo "✅ phases dir"
test -d wiki/projects/{id}/tasks/ && echo "✅ tasks dir"

# Phase 2 Step 5 — verify compliance
bash ~/.hermes/scripts/check-project-compliance.sh {project_id} | tail -3

# Phase 2 Step 3 — verify setup log exists
test -f wiki/projects/{id}/actions/{date}-{T-NN.M}-setup.md && echo "✅ setup log"
```

## Example: Content Creator project (verified 17-18/06)

**Tuấn Anh's exact request 17/06:**
> "Tưởng tượng em làm một dự án lớn nhiều ngày nhiều tháng thì em sẽ thiết lập hệ thống workflow như thế nào để không bị lộn xộn... mỗi một project mới tạo đều phải tuân thủ workflow này chặt chẽ. Các agent làm bất cứ một hành động nhỏ nào cũng phải log lại theo từng task nhỏ"

**Setup actions:**
1. Phase 1 → bootstrap `content-creator` → 6 folders + hub.md từ template
2. Phase 2 → mỗi task T-01.x tạo task-{id}.md + action logs
3. Wire vào default SOUL.md + 3 sub-agent SOULs (coder, research-lead, content-director)
4. CI gate `check-project-compliance.sh` enforce

**Impact (verified):**
- 21 files trong project organized rõ ràng
- Mỗi task có action log (≥50 từ/file)
- Mỗi sub-agent biết phải làm gì qua SOUL.md + shared ref
- T-01.1 chạy E2E: 11 slang + 6 sounds + 9 action logs + QA verify

## Reference files

- `references/bootstrap-script.md` — Full bootstrap-project.sh usage + idempotency notes
- `references/phase-templates.md` — Hub + task + action log templates ready to copy
- `references/phase2-ritual-e2e-walkthrough.md` — Real Phase 2 walkthrough for Content Creator T-01.4 (18/06, 15 scripts × 3 trụ, parallel fan-out, 3-layer verify caught 3 bugs). Use as template for similar multi-variant content tasks.

## See also

- `hermes-project-workflow-system` — Heavy 4-piece for ongoing multi-week infra projects
- `project-checklist-management` — Lightweight daily CHECKLIST maintenance
- `project-workflow-loop-engine` — 6-step RESEARCH→PLAN→EXECUTE→VERIFY→NEXT loop
- `multi-agent-orchestrator` — Decomposition + delegation patterns
- `self-verify-after-workaround` — Tuấn Anh's strict QA pattern with evidence