---
confidence: low
last_verified: 2026-04-10
relationships:
  - ❓ phase-2-build (ambiguous)
  - ❓ phase-1-init (ambiguous)
  - ❓ phase-2-build (ambiguous)
  - ❓ phase-3-launch (ambiguous)
  - ❓ github-link (ambiguous)
  - ❓ deployed-url (ambiguous)
  - ❓ 001-why-react (ambiguous)
  - ❓ 002-db-schema (ambiguous)
  - ❓ 001-why-react (ambiguous)
  - ❓ projects/my-wiki-redesign/hub (ambiguous)
  - ❓ projects/my-wiki-redesign/phase-1-init (ambiguous)
  - ❓ projects/my-wiki-redesign/decisions/001-why-react (ambiguous)
  - ❓ project-management (ambiguous)
  - ❓ project-management (ambiguous)
  - ❓ knowledge-base (ambiguous)
  - ❓ self-healing-wiki (ambiguous)
relationship_count: 16
---
# Project Management Wiki Integration — Research Synthesis

> **Status**: Research complete — Ready for implementation
> **Date**: 2026-04-09

## Tổng quan giải pháp

Wiki hiện tại + Project Management = **"Intelligent Project Hub"**

Mục tiêu: Agent retain full project context across sessions, không bị drift khi context window fill up.

---

## 1. Concept: Multi-Layer Project Context Architecture

### Layer 1: Project Hub (central nervous system)
- 1 file duy nhất chứa full overview của project
- Link tới tất cả phases, milestones, decisions
- Agent đọc file này để hiểu project state

### Layer 2: Phase Notes (module)
- Each phase = 1 note
- Chứa goals, tasks, blockers, decisions của phase đó
- Tự động link tới next phase

### Layer 3: Task granular (atomic)
- Tasks được track trong phase note
- Hoặc dùng daily notes cho cross-project tasks

### Layer 4: Decisions Log
- Mỗi major decision = 1 note
- Link từ phase vào decision để traceability

---

## 2. Directory Structure

```
wiki/
├── projects/                    # NEW: All projects here
│   ├── _templates/              # Project templates
│   │   ├── project-hub.md      # Hub template
│   │   ├── phase.md            # Phase template
│   │   └── task.md             # Task template
│   ├── project-name/           # Each project = folder
│   │   ├── hub.md              # Project overview (MANDATORY)
│   │   ├── phase-1-init.md     # Phase 1
│   │   ├── phase-2-build.md    # Phase 2
│   │   ├── decisions/          # Decision logs
│   │   │   ├── 001-why-react.md
│   │   │   └── 002-db-schema.md
│   │   └── assets/             # Project files
│   └── another-project/
│       └── ...
├── concepts/
│   └── project-management.md   # NEW: PM methodology docs
├── scripts/
│   └── project-tools.py        # NEW: Automation scripts
└── ...
```

---

## 3. Frontmatter Schema cho Projects

### Project Hub Frontmatter
```yaml
---
title: Project Name
created: 2026-04-09
updated: 2026-04-09
type: project
status: active | paused | completed | archived
phase: current phase name
tags: [project, active]
start-date: 2026-04-01
target-date: 2026-06-30
github: github.com/user/repo
---

# Project Name

## Overview
(Mission, goals, success criteria)

## Current Phase
[[phase-2-build]] ← wikilink

## Phases
1. [[phase-1-init]] — Completed ✓
2. [[phase-2-build]] — In Progress
3. [[phase-3-launch]] — Planned

## Milestones
- [x] MVP complete
- [ ] Beta testing
- [ ] Production launch

## Team
- Owner: Tuấn Anh
- Contributors: [link to any contributors]

## Resources
- [[github-link|GitHub]]
- [[deployed-url|Live Site]]

## Decisions
- [[001-why-react|Chose React over Vue]]
- [[002-db-schema|DB Schema v2]]

## Notes
(Random context, links, ideas)
```

### Phase Frontmatter
```yaml
---
title: Phase 2 — Build
created: 2026-04-10
updated: 2026-04-15
type: phase
status: in-progress | completed | planned
phase-number: 2
parent-project: project-name
tags: [phase, in-progress]
---

# Phase 2: Build

## Goals
- [ ] Implement auth
- [ ] Build dashboard
- [ ] API integration

## Tasks
<!-- Tasks tracked inline with checkboxes -->

## Blockers
- Waiting on API docs from vendor

## Decisions Made
- [[001-why-react|Chose React over Vue]]

## Next Action
@review PR #23

## Artifacts
- Screenshot of dashboard mockup
- Link to staging env
```

---

## 4. Agent Session Workflow

### At Session Start (modified):
```
1. Read SCHEMA.md
2. Read index.md
3. Read log.md (last 20 lines)
4. NEW: Check for active projects → inject project context if needed
5. Proceed with user's request
```

### When User mentions a project:
```
1. Check if project exists in projects/
2. If yes: load project hub + current phase
3. Inject into session context for this turn
4. Offer to update project state if changed
```

### Context Injection Pattern:
- Agent keeps "active project context" small (1-2 pages max)
- Use `/compact` metaphor: periodically compress project state
- Key principle: **context footprint = only what's relevant now**

---

## 5. Wikilink Convention

```markdown
# Projects
[[projects/my-wiki-redesign/hub]] — Full project hub

# Phases
[[projects/my-wiki-redesign/phase-1-init]]

# Decisions  
[[projects/my-wiki-redesign/decisions/001-why-react]]

# Tasks (inline in phase)
- [ ] Review API docs
- [x] Setup dev environment
```

---

## 6. Phase/Task Status Tracking

Status values:
- **project**: `active | paused | completed | archived`
- **phase**: `planned | in-progress | completed | cancelled`
- **task**: `[ ] TODO | [>] in-progress | [x] done | [!] blocked`

Inline task format (compatible với Obsidian/Todoist):
```markdown
- [ ] This is a task
- [>] This task is in progress
- [x] This task is done
- [!] This task is blocked
```

---

## 7. Key Features cho Agent Memory

### Auto-inject Project Context
When user works on a project, agent should:
1. Note current phase/task in working memory
2. Check if context has drifted from project hub
3. Offer to sync updates back to wiki

### Context Freshness
- Project hub updated date = indicator of freshness
- If outdated > 7 days: prompt user to review
- Phase note should be updated after each significant work session

### Multi-project Awareness
- Multiple active projects supported
- User can specify "which project are we talking about"
- If ambiguous: ask

---

## 8. Comparison: Vibe Coding Context Files vs Wiki PM

| Aspect | CLAUDE.md (Claude Code) | Wiki PM (ours) |
|--------|------------------------|----------------|
| Scope | Per-project, single file | Multi-file, hierarchical |
| Navigation | Search within file | Wikilinks |
| Tasks | Manual | Inline checkboxes |
| Phases | Implicit | Explicit phase notes |
| Decisions |buried in comments | Separate decision log |
| Agent access | Read on start | Load on demand |
| Maintenance | Manual | Script-assisted |

**Kết luận**: Wiki approach cho phép richer structure và better long-term retention, nhưng cần discipline để update.

---

## 9. Implementation Steps

### Phase 1: Schema Extension (done in this session)
- [ ] Update SCHEMA.md to include `projects/` directory
- [ ] Add `project` and `phase` frontmatter types
- [ ] Create project templates

### Phase 2: Templates
- [ ] Create `projects/_templates/project-hub.md`
- [ ] Create `projects/_templates/phase.md`
- [ ] Document task syntax

### Phase 3: Scripts
- [ ] Create `scripts/project-tools.py`:
  - `new-project <name>` — scaffold new project
  - `new-phase <project> <phase-name>` — create phase
  - `list-projects` — show all projects
  - `project-status <project>` — show status summary
  - `sync-context` — refresh active project context

### Phase 4: Workflow Integration
- [ ] Modify startup sequence to check active projects
- [ ] Add "project context" to memory injection
- [ ] Create wiki page: [[project-management]]

### Phase 5: Automation
- [ ] Cron job: project health check (stale updates)
- [ ] Auto-compact project context when too large

---

## 10. Điểm quan trọng nhất

### Prevention of Context Loss
1. **Small footprint**: Project hub chỉ chứa essential info
2. **Frequent sync**: Sau mỗi session, update phase note
3. **Decision traceability**: Link decisions vào code/context
4. **Freshness signal**: Updated date là trust indicator

### Agent Never Gets Lost
- Luôn biết đang ở project nào, phase nào
- Có audit trail của decisions
- Có clear "next action" visible

---

## Related

- [[project-management]] — Detailed methodology
- [[knowledge-base]] — General KB patterns
- [[self-healing-wiki]] — Auto-maintenance approach
