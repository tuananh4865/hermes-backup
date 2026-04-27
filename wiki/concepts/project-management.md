---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 projects/personal-finance-tracker/hub (extracted)
  - 🔗 projects/personal-finance-tracker/phase-1-init (extracted)
  - 🔗 projects/personal-finance-tracker/decisions/001-tech-stack (extracted)
  - 🔗 wiki (extracted)
relationship_count: 4
---

# Project Management

## Overview
Tích hợp project management vào wiki để:
- **Full context preservation** — Agent không bị mất context giữa các sessions
- **Phase-based tracking** — Mỗi project có phases rõ ràng
- **Task granularity** — Tasks được track inline trong phase notes
- **Decision traceability** — Mọi major decision đều có log

## Core Principle
> **Context footprint = only what's relevant now**
> Đừng nhồi nhét mọi thứ vào context. Chỉ inject project context khi cần.

## Architecture

## Related
- [[001-topic]]

### 4-Layer Model
```
Project Hub (1 file)
    ↓ links to
Phase Notes (per phase)
    ↓ links to
Tasks (inline checkboxes)
    ↓ linked from
Decision Logs (1 file per decision)
```

### Project Hub
- Central nervous system của project
- Chứa: mission, current phase, milestones, team, links
- Agent đọc hub để hiểu full project state

### Phase Notes
- Goals, tasks, blockers cho từng phase
- Progress notes cập nhật sau mỗi session
- Next action luôn visible

### Decision Logs
- Context → Options → Decision → Rationale → Consequences
- Link từ phase vào để traceability

## Task Syntax

```markdown
- [ ] TODO item
- [>] In progress
- [x] Done
- [!] Blocked
```

## Status Values

| Object | Statuses |
|--------|----------|
| Project | `active`, `paused`, `completed`, `archived` |
| Phase | `planned`, `in-progress`, `completed`, `cancelled` |

## Directory Structure

```
wiki/projects/
├── _templates/
│   ├── project-hub.md
│   ├── phase.md
│   └── decision.md
└── {project-name}/
    ├── hub.md
    ├── phase-1-name.md
    ├── phase-2-name.md
    └── decisions/
        ├── 001-decision-name.md
        └── 002-decision-name.md
```

## Agent Workflow

### Session Start
1. Read SCHEMA.md
2. Read index.md
3. Read log.md (last 20 lines)
4. **NEW**: Check for active projects → inject context if needed
5. Proceed with request

### During Session
- When user mentions project: load hub + current phase
- After significant work: offer to update phase notes
- On major decision: create decision log

### Session End
- Sync any project updates back to wiki
- Update phase progress notes
- Commit + push

## Wikilinks

```markdown
[[projects/personal-finance-tracker/hub]]
[[projects/personal-finance-tracker/phase-1-init]]
[[projects/personal-finance-tracker/decisions/001-tech-stack]]
```

## Context Freshness Rules

1. **Project hub**: Updated date = trust indicator. Stale > 7 days = prompt review
2. **Phase notes**: Update after each significant work session
3. **Decision logs**: Immutable sau khi decided

## Best Practices

1. **Hub nhỏ gọn**: Chỉ essential info, link tới details
2. **Phase rõ ràng**: Mỗi phase có clear goal và deliverables
3. **Task visible**: Next action luôn ở prominent position
4. **Decision linked**: Từ phase link tới decision để trace

## Comparison: Wiki PM vs CLAUDE.md

| Aspect | CLAUDE.md (Claude Code) | Wiki PM (ours) |
|--------|------------------------|----------------|
| Scope | Per-project, single file | Multi-file, hierarchical |
| Navigation | Search within file | Wikilinks |
| Tasks | Manual | Inline checkboxes |
| Phases | Implicit | Explicit phase notes |
| Decisions | buried | Separate decision log |
| Agent access | Read on start | Load on demand |
| Maintenance | Manual | Script-assisted |

**Wiki approach**: Richer structure, better long-term retention, requires discipline

## Related
- [[wiki]] — Wiki overview
- `projects/_templates/project-hub` — Hub template (copy, don't link)
- `projects/_templates/phase` — Phase template (copy, don't link)
