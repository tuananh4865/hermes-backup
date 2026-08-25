# Phase Templates — Copy-Ready

## Hub Template (`wiki/projects/_template/hub.md`)

```markdown
---
title: Project Hub Template — {PROJECT_NAME}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
type: project-hub
tags: [project, {project_id}, template]
confidence: high
status: active
owner: {OWNER_NAME}
orchestrator: Hermes (default profile)
project_id: {project_id}
relationships: [{related-project-1}, {related-project-2}]
---

# {PROJECT_NAME} Project — Hub

> **Hub file** — Single entry point cho mọi thứ liên quan project này.
> Mọi phase, task, action phải reference về đây.
>
> **Setup date:** {YYYY-MM-DD}
> **Setup by:** {orchestrator/sub-agent name}
> **Pre-flight Ritual:** Phase 1 ✅

## 🎯 NORTH STAR

- **Mục tiêu:** {1-2 câu mô tả mục tiêu cuối cùng}
- **Deadline:** {YYYY-MM-DD hoặc duration}
- **Success metric:** {KPI chính để đo success}
- **Scope:** {in-scope} / **Out of scope:** {không làm gì}

## 👥 TEAM

| Role | Profile | Responsibility |
|------|---------|----------------|
| **Orchestrator** | `default` (MiniMax-M3) | Coordinate, QA, report cho owner |
| **{Role 1}** | `{profile-name}` | {mô tả trách nhiệm} |
| **{Role 2}** | `{profile-name}` | {mô tả trách nhiệm} |
| **{Role 3}** | `{profile-name}` | {mô tả trách nhiệm} |

## 📁 STRUCTURE (Pre-flight Ritual compliant)

```
{project_id}/
├── hub.md                  ← File này
├── dashboard.md            ← Live status (update sau mỗi task)
├── dependency-graph.md     ← Task → task mapping
├── phases/
│   └── phase-01-{name}.md
├── tasks/
│   └── task-{T-NN.M}-{name}.md
├── research/               ← Research outputs (YAML frontmatter BẮT BUỘC)
├── actions/                ← Action log per task (granular, ≥50 từ/file)
└── logs/                   ← Per-project session logs (auto-fill by hook)
```

## 📋 PHASES OVERVIEW

### Phase 01: {Phase name}
- **Duration:** {N ngày}
- **Goal:** {1 câu}
- **Tasks:** [List task IDs]

## 🎯 KEY DELIVERABLES

- [ ] {Deliverable 1}
- [ ] {Deliverable 2}
- [ ] {Deliverable 3}
```

## Task Template (`wiki/projects/_template/task.md`)

```markdown
---
title: Task {T-NN.M} — {Task Name}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
type: task
tags: [task, {T-NN.M}, {project_id}]
project_id: {project_id}
phase_id: {phase_id}
task_id: {T-NN.M}
status: ⏳ TODO
priority: {high/medium/low}
owner_role: {role-name}
orchestrator: Hermes (default profile)
research_refs: []       # ← v2.1: research inputs (MANDATORY)
verify_attempts: 0       # ← v2.2: retry counter (max 3)
last_failure_reason: ""  # ← v2.2: lý do fail gần nhất
escalated_at: null       # ← v2.2: timestamp when escalated
---

# Task {T-NN.M} — {Task Name}

> **Copy from _template/task.md** when creating new tasks. Fill all `<placeholder>` fields.

## 🎯 Objective

{1-2 câu mục tiêu task. Tại sao cần thiết?}

## 📚 Research (Step 0)

- Research files: [[T-01.1-research-1]], [[T-01.2-research-2]]
- Skills to load: `{skill-name}` (if any)

## 📦 Deliverables

1. **{Deliverable 1}** với:
   - {Detail cụ thể}
   - {Acceptance criteria}

2. **{Deliverable 2}** với:
   - {Detail}
   - {Acceptance criteria}

## 🔄 LOOP ENGINE v2.3 (6 bước)

### Step 0: RESEARCH (đã làm)
- ✅ Research files loaded

### Step 1: PLAN (đã làm)
- ✅ Task created with deliverables
- ✅ Dependencies declared
- ✅ Owner assigned

### Step 1.5: RESEARCH (conditional)
- {RUN / SKIP} (lý do)

### Step 2: EXECUTE ({owner_role})
- Load skill `{skill-name}` TRƯỚC
- Use `mcp_MiniMax_*` for external data
- Save findings to `research/`
- Log every action to `actions/{date}-{T-NN.M}-{action}.md`

### Step 3: VERIFY (qa-agent)
- [ ] Deliverable count đạt yêu cầu
- [ ] YAML frontmatter đầy đủ
- [ ] ≥2 wikilinks
- [ ] Voice compliance
- [ ] CI gate passes

### Step 4: NEXT
- PASS → mark DONE + unblock downstream
- FAIL → loop from Step 2 (max 3 attempts) → escalate

## 🔗 Dependencies

- **Depends on:** [{T-XX.Y}, ...]
- **Blocks:** [{T-XX.Z}, ...]

## 📝 Action Log

(Mỗi action sẽ tạo file `actions/{date}-{T-NN.M}-{action-id}.md`)
```

## Action Log Template (`actions/{date}-{T-NN.M}-{action-id}.md`)

```markdown
---
title: {Action description} ({T-NN.M})
created: {YYYY-MM-DD}
type: action-log
tags: [action-log, {T-NN.M}, {project_id}]
project_id: {project_id}
phase_id: {phase_id}
task_id: {T-NN.M}
agent_role: {your-role}
---

# {YYYY-MM-DD}-{T-NN.M}-{action-id}

## Context
Tại sao làm action này? Reference đến task nào?

## Action
Mô tả cụ thể hành động đã làm (≥50 từ).

## Result
Output / finding / decision.

## Next
Bước tiếp theo (nếu có).
```

## Setup Log Template (`actions/{date}-setup-{project_id}.md`)

```markdown
---
title: Project Setup — {project_id}
created: {YYYY-MM-DD}
type: ritual-log
tags: [ritual, pre-flight, setup, {project_id}]
project_id: {project_id}
---

# Project Setup — {project_id}

## Phase 1 Steps Executed
- [x] Created folder structure (phases/tasks/research/actions/logs)
- [x] Created hub.md from template (filled NORTH STAR)
- [x] Created phase-01-{name}.md
- [x] Created first task T-01.1
- [x] Ran check-project-compliance.sh

## Plan for First Task
- Sub-action 1: ...
- Sub-action 2: ...
- Sub-action 3: ...

## Blockers
- (none / list)

## Ready to Execute?
- [x] YES
- [ ] NO — blocked by ...
```