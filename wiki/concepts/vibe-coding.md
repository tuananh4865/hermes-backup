---
title: Vibe Coding
description: Solo developer workflow using AI agents (Claude Code, Cursor) to write software by describing intent — 50-70% reduction in boilerplate time.
tags:
  - AI coding
  - solo developer
  - workflow
  - Claude Code
  - Cursor
  - productivity
created: 2026-04-14
related:
  - claude-code-skills
  - agentic-ai
  - apple-silicon-mlx
  - local-llm
---

# Vibe Coding

**Vibe coding** is the practice of writing software by describing what you want to an AI coding agent, then iterating based on the results. Instead of writing every line yourself, you:
1. Describe the desired outcome or feature
2. AI generates the code
3. You review, test, and refine
4. Repeat

## The Workflow

```
Spec → AI Generate → Review → Refine → Deploy
```

### Typical Stack
- **AI Coding Agent**: Claude Code (primary), Cursor, or Gemini CLI
- **Local LLM**: Ollama/MLX for privacy-sensitive or offline work
- **GitHub**: Version control and collaboration
- **Deployment**: Vercel, Railway, Fly.io, or cloud VPS

### What AI Handles Well
- Boilerplate code generation
- Test writing (unit tests, integration tests)
- Documentation
- Refactoring repetitive patterns
- Learning new libraries/APIs

### What Still Needs Human Expertise
- Complex debugging and stack traces
- Security-critical code (auth, payments)
- Novel architecture decisions
- Performance optimization
- Understanding business requirements

## Productivity Gains

Developers report:
- **50-70% reduction** in boilerplate coding time
- **3-5x faster** prototyping from spec to working prototype
- **Fewer typos** and syntax errors in generated code
- **Better documentation** since AI generates docstrings

## Best Practices

1. **Start with a clear spec**: Vague intent → vague code. Be specific about inputs, outputs, edge cases.

2. **Review every change**: AI generates plausible but incorrect code. Always read before committing.

3. **Use [[claude-code-skills]]**: The 220+ skill ecosystem automates common tasks (git commits, PR creation, deployment).

4. **Combine local + cloud**: Use [[apple-silicon-mlx|local MLX]] for privacy and cloud Claude Code for complex reasoning.

5. **Iterate rapidly**: Small, incremental prompts get better results than large feature dumps.

## Tools of the Trade

| Tool | Use Case |
|------|----------|
| [[claude-code-skills|Claude Code]] | Primary AI coding agent |
| [[apple-silicon-mlx|Ollama/MLX]] | Local LLM for privacy |
| Cursor | Alternative AI coding IDE |
| GitHub Copilot | Inline code suggestions |
| [[n8n]] | AI workflow automation |

## See Also

- [[agentic-ai]] — The broader category of autonomous AI systems
- [[claude-code-skills]] — 220+ production-ready skills
- [[apple-silicon-mlx]] — Running local LLMs on Mac
