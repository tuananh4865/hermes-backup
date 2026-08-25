---
title: Task T-<PHASE_NUM>.<ID> — <TASK_NAME>
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: task
tags: [task, <TAG1>]
project_id: <project-slug>
phase_id: phase-<PHASE_NUM>-<name>
task_id: T-<PHASE_NUM>.<ID>
status: ⏳ TODO
priority: <high | medium | low>
owner_role: <profile-name>
orchestrator: Hermes (default)
relationships: [<related-1>]
depends_on: [<task-id-prev>]
blocks: [<task-id-next>]
estimated_hours: <N>
actual_hours: null
---

# Task T-<PHASE_NUM>.<ID> — <TASK_NAME>

## 🎯 Objective

<Mô tả 1-2 câu: làm gì, output gì, ai dùng>

## 📦 Deliverables (MUST HAVE)

1. **<Deliverable 1>** với:
   - <requirement 1>
   - <requirement 2>

2. **<Deliverable 2>** với:
   - <requirement>

3. **Saved to wiki:**
   - `wiki/<path>/<file1>.md`
   - `wiki/<path>/<file2>.md`

## 🔄 LOOP ENGINE (plan → execute → verify → next)

### Step 1: PLAN (Orchestrator)
- ✅ Task created with clear deliverables
- ✅ Dependencies declared
- ✅ Owner assigned: <profile>
- ✅ Verify criteria defined below

### Step 2: EXECUTE (<owner>)
- Load relevant skill TRƯỚC
- Use MCP tools for external data
- Save findings to wiki immediately
- Log every action to `actions/YYYY-MM-DD-T-<PHASE>.<ID>-<action>.md`

### Step 3: VERIFY (qa-agent) — **MUST PASS**
- [ ] <Criterion 1>
- [ ] <Criterion 2>
- [ ] <Criterion 3>
- [ ] <Criterion 4>
- [ ] YAML frontmatter valid
- [ ] ≥2 wikilinks per wiki file
- [ ] Voice compliance
- [ ] TRÁHN: 0 violations
- [ ] Citations format: title + URL + date

### Step 4: NEXT (Orchestrator)
- If PASS → mark task DONE → start next task
- If FAIL → return to Step 2 with specific issues
- If BLOCKED > 24h → Telegram Tuấn Anh

## 📊 Verify Script (qa-agent runs)

```bash
# Check deliverable 1: file exists
test -f /Volumes/Storage-1/Hermes/wiki/<path>/<file1>.md

# Check deliverable 2: count ≥N
grep -c "^### " <file> | awk '{ if ($1 >= N) exit 0; else exit 1 }'

# Check YAML frontmatter present
head -1 <file> | grep -q "^---"
```

## 🚦 Status Flow

```
⏳ TODO → 🔄 IN_PROGRESS → ⏸️ AWAITING_VERIFY → ✅ DONE / ❌ FAILED → 🔁 RETRY
```

## 🔗 Dependencies

- **Depends on:** <task-id-prev or "nothing">
- **Blocks:** <task-id-next or "nothing">
- **Related:** <other-task-id>

## 📝 Action Log

(Mỗi action nhỏ sẽ tạo file `actions/YYYY-MM-DD-T-<PHASE>.<ID>-<action>.md`)

- `YYYY-MM-DD-T-<PHASE>.<ID>-load-skill.md` — Loaded <skill-name>
- `YYYY-MM-DD-T-<PHASE>.<ID>-<action>.md` — <description>
- `YYYY-MM-DD-T-<PHASE>.<ID>-save.md` — Saved to wiki
- `YYYY-MM-DD-T-<PHASE>.<ID>-verify.md` — QA agent verification

---

*Task created: YYYY-MM-DD HH:MM ICT by Hermes (orchestrator)*
