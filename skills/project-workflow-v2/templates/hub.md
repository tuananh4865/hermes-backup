---
title: <PROJECT_NAME> Project — Hub
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: project-hub
tags: [project, <TAG1>, <TAG2>]
confidence: high
status: active
owner: Tuấn Anh
orchestrator: Hermes (default profile)
project_id: <project-slug>
relationships: [<related-1>, <related-2>]
---

# <PROJECT_NAME> Project

> **Hub file** — Single entry point cho mọi thứ liên quan project này.
> Mọi phase, task, action phải reference về đây.

## 🎯 NORTH STAR

- **Mục tiêu cuối:** <KPIs>
- **Timeline:** <N tuần/ngày>
- **Owner:** Tuấn Anh
- **Orchestrator:** Hermes (default profile)

## 👥 TEAM (Profile-based)

| Role | Profile | Responsibility |
|------|---------|----------------|
| **Orchestrator** (Em) | `default` | Coordinate, QA, report |
| **Content Director** | `content-director` | Content strategy, voice, scripts |
| **Research Lead** | `research-lead` | Research, data collection |
| **Coder** | `coder` | Automation, tooling |
| **Memory Curator** | `memory-curator` | Wiki updates, log, archive |
| **QA Agent** | `qa-agent` | Verify, score, gate-keep |

## 📁 STRUCTURE

```
projects/<project-slug>/
├── hub.md                          # File này
├── phases/
│   └── phase-01-<name>.md
├── tasks/
│   └── task-<phase>-<id>-<name>.md
├── actions/
│   └── <YYYY-MM-DD>-<task-id>-<action>.md
├── decisions/
│   └── decision-<id>.md
└── logs/
    └── <YYYY-MM-DD>-sessions.md
```

## 🔄 WORKFLOW LOOP

```
1. PLAN   → Tạo Task trong phase/, define deliverables
2. DELEGATE → Orchestrator giao cho role phù hợp
3. EXECUTE → Role làm → mỗi action tạo file actions/<date>-<id>.md
4. VERIFY  → QA Agent check pass/fail
5. LOG     → session-auto-log auto-append logs/<date>.md
6. NEXT    → Nếu pass → next task. Nếu fail → fix
```

## 🔗 DEPENDENCIES (high-level)

- **phase-01** depends on: nothing
- **phase-02** depends on: phase-01
- **phase-03** depends on: phase-02

## 📊 CURRENT STATUS (YYYY-MM-DD)

- **Active phase:** [phase-01-...](./phases/phase-01-...)
- **Tasks in progress:** 0
- **Tasks completed:** 0
- **Last session:** <session-id>
- **Next action:** <next task id>

## 🛡️ GOVERNANCE

- **Workflow rules:** `~/.hermes/docs/project-workflow-v2.md`
- **Loop engine:** `~/.hermes/profiles/_shared/project-loop-engine.md`
- **Auto-log hook:** `~/.hermes/hooks/session-auto-log/` (v2 with project tracking)
- **CI gate:** `bash ~/.hermes/scripts/check-project-compliance.sh <project-slug>`

## 🔗 RELATED

- [[tiktok-viral-script]] — (delete if not applicable)
- [[learned-about-tuananh]] — User preferences
- [[fable5-patterns]] — System-wide mandate (must apply)

---

*Last updated: YYYY-MM-DD HH:MM ICT by Hermes (orchestrator)*
