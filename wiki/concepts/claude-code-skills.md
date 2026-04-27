---
title: Claude Code Skills
description: 220+ production-ready skills for Claude Code and other AI coding agents — git workflows, testing, deployment, refactoring.
tags:
  - Claude Code
  - skills
  - AI coding
  - agent skills
  - automation
created: 2026-04-14
related:
  - vibe-coding
  - agentic-ai
  - claude-code
---

# Claude Code Skills

A growing ecosystem of **220+ production-ready skills** for Claude Code and other AI coding agents. Skills are modular, reusable prompt templates that automate specific developer workflows.

## What Are Skills?

Skills are structured prompts with:
- **Description**: What the skill does
- **Triggers**: When to invoke the skill
- **Actions**: Step-by-step instructions for the agent
- **Examples**: Input/output examples

## Top Skill Categories

### Git & Version Control
- `/commit` — Smart commit with conventional commits format
- `/pr` — Create pull requests with description
- `git-worktree` — Manage multiple git worktrees

### Testing
- Comprehensive test suite generation
- Unit test writing
- Integration test patterns

### Deployment
- Vercel, Railway, Fly.io deployment
- Docker containerization
- CI/CD pipeline setup

### Refactoring
- Extract to function/component
- Rename and move refactors
- Technical debt reduction

### Documentation
- API documentation generation
- README creation
- Changelog management

## Notable Community Skills

| Skill | Author | Uses | GitHub Stars |
|-------|--------|------|-------------|
| claude-skills | alirezarezvani | 233 skills, 11 tools | Growing |
| remotion-skill | Various | Video generation in code | Popular |
| git-worktree | Community | Branch management | Standard |

## Using Skills

In Claude Code:
```
/skill-name  # Invoke a skill
/skill-list  # See available skills
/skill-add   # Add a new skill
```

## Creating Custom Skills

```markdown
# Skill Name

## Description
What this skill does.

## Triggers
- When the user asks for X
- When project contains Y

## Actions
1. First step
2. Second step
3. Verification

## Examples
Input: "..."
Output: "..."
```

## See Also

- [[vibe-coding]] — Using skills in your solo dev workflow
- [[agentic-ai]] — Agentic systems these skills power
- [[claude-code]] — The primary AI coding agent
