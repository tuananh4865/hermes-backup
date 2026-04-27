---
title: "SLC Methodology (Solo Dev AI Workflow)"
created: 2026-04-17
type: concept
tags: [solo-dev, vibe-coding, workflow, productivity]
related:
  - [[vibe-coding]]
  - [[coding-agents]]
  - [[agentic-ai]]
---

# SLC Methodology — Solo Dev AI Workflow

## Overview

**SLC = Simple, Lovable, Complete.** It's a product development methodology designed specifically for solo developers working with AI coding agents. The core insight: **AI agents are most effective when given tightly scoped, well-defined tasks** — and SLC enforces this discipline.

The SLC mindset is credited with "supercharging" solo developer workflows when combined with AI coding tools like Claude Code, Cursor, and Lovable.

## The Three Pillars

### Simple
**Small enough to ship in one session.** The task should be achievable without the context growing beyond what the AI agent can handle effectively.

- Break large features into micro-features (< 4 hour tasks)
- One clear deliverable per session
- Avoid scope creep — if it takes > 1 day, split it

### Lovable
**Something users actually want.** Not just functional — it needs emotional resonance. The bar for "lovable" forces you to think about UX, edge cases, and the details that make software feel premium.

- UX details that AI agents often skip (loading states, error handling, empty states)
- Performance that doesn't frustrate
- Polish that makes users feel "this was made for me"

### Complete
**Actually done-done.** No "it works on my machine." No leaving TODOs. No 80% features that ship but feel half-baked.

- Tests that prove it works
- Edge cases handled
- README that explains how to use it
- Error messages that help

## Why SLC Works with AI Agents

AI coding agents struggle with:
1. **Large contexts** — more code = more confusion
2. **Unclear requirements** — "make it better" is ambiguous
3. **Half-baked features** — they default to "good enough"

SLC addresses all three:
- Small scope keeps context tight
- Clear requirements come from the "lovable" standard
- "Complete" forces quality gates

## Workflow in Practice

```
┌─────────────────────────────────────────────────────────┐
│  Feature Idea                                            │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Apply SLC Test:                                        │
│  • Simple enough for one session? ❌ → Scope down       │
│  • Lovable — will users care? ❌ → Rethink              │
│  • Complete — can you test it fully? ❌ → Scope out    │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Single Claude Code / Cursor Session                    │
│  "Build [specific feature] that does [specific thing]" │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Ship → Get feedback → Iterate                         │
└─────────────────────────────────────────────────────────┘
```

## Solo Dev AI Stack (2026)

| Tool | Use Case | SLC Fit |
|------|----------|---------|
| **Claude Code** | Primary coding agent | Best for complex tasks |
| **Cursor** | IDE integration | Good for paired editing |
| **v0/Lovable/Bolt** | UI-first prototyping | Fast SLC iterations |
| **Replit** | Quick experiments | Good for throwaway ideas |

## Key Principle: One Session = One Feature

The fundamental discipline of SLC with AI:

- **Before AI session:** Define the micro-feature clearly
- **During session:** Let AI do the implementation, stay available for clarification
- **After session:** Review, test, ship — don't start a second feature in the same context

## Related

- [[vibe-coding]] — Broader vibe coding context
- [[coding-agents]] — Claude Code, Cursor, Copilot
- [[solo-dev-ai-workflow]] — Related solo developer patterns
