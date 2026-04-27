---
title: "Solo Dev AI Workflow"
created: 2026-04-17
type: concept
tags: [solo-dev, ai-tools, workflow, productivity]
related:
  - [[slc-methodology]]
  - [[vibe-coding]]
  - [[coding-agents]]
---

# Solo Dev AI Workflow

## Overview

Solo dev AI workflow is the practice of a single developer using AI coding agents as their entire engineering team — architect, reviewer, debugger, and deployer. The workflow replaces traditional team-based development with tightly-integrated AI assistance at every stage of the software development lifecycle.

## Core Principles

### 1. AI as Force Multiplier, Not Replacement

The solo dev AI workflow doesn't eliminate the need for engineering judgment — it amplifies the output of every decision. The human sets direction, makes architectural decisions, and validates quality; AI handles implementation boilerplate, research, and iteration.

### 2. Context is Everything

AI agents are dramatically better with:
- **Small, well-scoped tasks** (SLC methodology)
- **Rich context** — relevant files, previous decisions, business requirements
- **Clear success criteria** — how to know when it's done

### 3. Human-in-the-Loop at Decision Points

Critical decisions (architecture, security, UX direction) stay with the human. AI handles the execution. The workflow fails when humans rubber-stamp AI outputs without verification.

## Typical Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  1. IDEA → Define micro-feature using SLC                    │
│     "Build a user authentication flow with email/password"   │
└──────────────────────────┬───────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  2. CONTEXT GATHERING → AI helps research                     │
│     "What are the best practices for password auth in 2026?" │
└──────────────────────────┬───────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  3. AI IMPLEMENTATION → Claude Code / Cursor session          │
│     Generate code, handle edge cases, write tests             │
└──────────────────────────┬───────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  4. HUMAN REVIEW → Verify quality and correctness             │
│     Review AI code, catch edge cases AI missed               │
└──────────────────────────┬───────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  5. DEPLOY → AI helps with DevOps, CI/CD, monitoring         │
└──────────────────────────────────────────────────────────────┘
```

## Essential Tools (2026)

| Tool | Role | Best For |
|------|------|----------|
| **Claude Code** | Primary coding agent | Architecture, complex features |
| **Cursor** | IDE-integrated AI | Inline edits, paired programming |
| **v0/Lovable** | UI prototyping | Rapid UI iterations |
| **GitHub Copilot** | Inline completion | Boilerplate, familiar patterns |
| **Windsurf** | Code agent | Autonomous feature development |
| **Bolt** | Full-stack prototyping | MVPs in hours |

## Workflow Patterns

### Pattern 1: Quick iteration
1. Define feature in plain English
2. AI implements end-to-end
3. Human reviews + requests changes
4. AI iterates until approved
5. Ship

### Pattern 2: Architect + Implement
1. Human defines architecture and edge cases
2. AI implements based on spec
3. Human validates against spec
4. Ship

### Pattern 3: Research → Build
1. AI researches best approaches
2. Human reviews findings and decides
3. AI implements chosen approach
4. Ship

## Common Pitfalls

- **Over-reliance on AI** — AI code can be subtly wrong; always review
- **Scope creep** — AI can generate unlimited code; human must enforce scope
- **Context overflow** — too many files confuses AI; keep contexts tight
- **Skipping tests** — AI-generated tests are often incomplete; validate coverage

## Metrics for Success

Solo dev AI workflow succeeds when:
- Features ship in hours, not days
- Code quality is comparable to team-developed projects
- Developer happiness is higher (less boilerplate, more creative work)
- Maintenance burden stays manageable

## Related

- [[slc-methodology]] — SLC framework for solo devs
- [[vibe-coding]] — Broader vibe coding context
- [[coding-agents]] — Claude Code, Cursor, Copilot tools
