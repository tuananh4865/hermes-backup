---
title: Task Checklist Template (Tuấn Anh mandate 2026-06-18)
type: template
applies_to: kanban_create body field
---

# Task Body — Checklist Template

> **MANDATORY** for every `kanban_create` call when working with Tuấn Anh.
> Use this exact structure in the `body` field so the user can audit
> "what's done vs pending" at a glance.

## Structure

```markdown
## 🎯 Objective
{1-2 sentences: what does this task accomplish? Why does it matter?}

## 📋 Checklist
- [ ] {Step 1 — concrete, verifiable}
- [ ] {Step 2}
- [ ] {Step 3}
- [ ] {Step 4}

## 📦 Deliverables
1. **{Deliverable 1}** — {acceptance criteria}
2. **{Deliverable 2}** — {acceptance criteria}

## 🔗 Dependencies
- **Depends on:** [{task_ids}]
- **Blocks:** [{task_ids}]
- **Related:** [{task_ids}]

## 📊 Verify
```bash
{command to verify deliverable 1}
{command to verify deliverable 2}
```

## 🚦 Status
- ⏳ TODO → 🔄 IN_PROGRESS → ⏸️ AWAITING_VERIFY → ✅ DONE / ❌ FAILED → 🔁 RETRY
```

## Why this structure

- **Checklist** = visual progress (Tuấn Anh can scan and see what's done)
- **Verify commands** = no ambiguity about "done" (matches his work-style mandate to VERIFY before declaring done)
- **Dependencies** = explicit graph (matches his "Mục đó liên quan liên đới đến những mục nào khác")
- **Status flow** = single source of truth (matches his "biết chính xác mục nào làm ở đâu fix cái gì vào thời điểm nào")

## Worked example

```python
kanban_create(
    title="Research Gen Z slang for Content Creator project",
    assignee="research-lead",
    body="""## 🎯 Objective
Nghiên cứu Gen Z slang Vietnam mới nhất (May-Jun 2026) để làm input cho content scripts.

## 📋 Checklist
- [ ] Load skill `tiktok-competitor-deep-analysis`
- [ ] Run 3 `mcp_MiniMax_web_search` queries (fresh slang, trending, viral)
- [ ] Compile list ≥10 terms với Vietnamese + English meaning + ≥2 sources + date
- [ ] Save to `wiki/projects/content-creator/research/T-01.1-gen-z-slang-2026-06.md`
- [ ] Log mỗi search vào `actions/2026-06-17-T-01.1-search-slang-*.md`

## 📦 Deliverables
1. **Slang list** — ≥10 terms, each with ≥2 sources ≤30 days, YAML frontmatter
2. **Action logs** — 3+ search logs + 1 save log, each ≥50 words

## 🔗 Dependencies
- **Depends on:** []
- **Blocks:** [T-01.2 voice-profile, T-01.4 scripts]

## 📊 Verify
```bash
test -f wiki/projects/content-creator/research/T-01.1-gen-z-slang-2026-06.md
grep -c "^### " wiki/projects/content-creator/research/T-01.1-gen-z-slang-2026-06.md | awk '{ if ($1 >= 10) exit 0; else exit 1 }'
```

## 🚦 Status
⏳ TODO → 🔄 IN_PROGRESS → ⏸️ AWAITING_VERIFY → ✅ DONE
""",
    priority=2,
)
```

## Anti-patterns (DON'T do this)

- ❌ Empty body or prose-only body — fails audit
- ❌ Vague checklist ("research slang", "write report") — not verifiable
- ❌ No verify commands — can't tell if task is actually done
- ❌ No dependencies declared — breaks the audit graph

## Reference

- Mandate transcript: `references/tuan-anh-workflow-mandate.md`
- Project workflow: `~/.hermes/profiles/_shared/project-loop-engine.md`
- Sub-agent ref: `~/.hermes/profiles/_shared/sub-agent-workflow.md`