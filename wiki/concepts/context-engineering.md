---
title: "Context Engineering"
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [ai, vibe-coding, prompts, context, engineering]
related:
  - [[vibe-coding]]
  - [[coding-agents]]
  - [[prompts]]
---

# Context Engineering

## Overview

Context engineering = the practice of structuring project context so AI coding tools generate relevant, accurate code. Unlike simple prompt writing, context engineering focuses on how information is organized, presented, and maintained across an entire project.

Core insight: AI tools fail not because they're dumb, but because they lack sufficient context. Context engineering fills that gap.

## Why It Matters for Vibe Coding

When vibe coding, you have a conversation with an AI. The AI can only "see" what you show it. Context engineering ensures:

1. **AI understands your project structure** — How files relate, what the architecture looks like
2. **AI knows your coding standards** — Naming conventions, preferred patterns, style preferences
3. **AI understands the domain** — Business logic, user flows, technical constraints
4. **AI maintains consistency** — Across files, features, and conversation turns

## Key Techniques

### 1. Project Memory Files

Create a `CONTEXT.md` or `.cursorrules` file in your project root:

```
# Project Overview
- Type: React Native mobile app
- Purpose: Habit tracker with social features
- Core users: 18-35 fitness enthusiasts

# Architecture
- Frontend: React Native + Expo
- State: Zustand
- API: REST + WebSocket

# Coding Standards
- File naming: kebab-case
- Component pattern: Container/Presentational
- Error handling: try/catch with user-friendly messages
```

### 2. Hierarchical Context Presentation

When asking AI to make changes, provide context in layers:

1. **Project level** — Overall architecture and goals
2. **Feature level** — What the specific feature does
3. **File level** — Relevant code snippets
4. **Task level** — Specific change needed

### 3. Semantic File Organization

Organize files so AI can navigate naturally:
- `features/auth/login.tsx` — Authentication feature
- `features/auth/register.tsx`
- `features/auth/components/` — Auth-related components

### 4. Inline Context Comments

Add brief comments explaining non-obvious decisions:

```typescript
// Using setTimeout workaround here because 
// React Native's Animated API has a bug on iOS 17
// Related issue: https://github.com/...
```

## Resources

- [Context Ark — Context Engineering for Vibe Coders](https://contextark.com/blog/context-engineering-for-vibe-coders)
- [Cursor Rules](https://cursor.sh) — Project-specific AI rules
- [Vibe Coding](https://en.wikipedia.org/wiki/Vibe_coding) — Wikipedia overview

## Related Concepts

- [[vibe-coding]] — The broader practice AI-assisted development
- [[coding-agents]] — Claude Code, Cursor, and other AI coding tools
- [[prompts]] — Prompt writing techniques
