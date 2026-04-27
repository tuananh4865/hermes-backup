---
title: "Agent Skills"
confidence: medium
last_verified: 2026-04-12
relationships:
  - 🔍 obsidian-skills (extracted)
  - 🔍 agent-frameworks (inferred)
  - 🔍 autonomous-wiki-agent (inferred)
relationship_count: 3
---

# Agent Skills

## Overview

Agent Skills define the capabilities and tools available to AI agents in a standardized format. The specification enables agents to understand what actions they can perform, how to invoke tools, and what constraints apply.

## Agent Skills Specification

**Source**: [agentskills.io/specification](https://agentskills.io/specification)

Standard skill definition format:

```yaml
---
name: skill-name
description: What this skill does
version: "1.0"
tags: [category, domain]
allowed_tools:
  - tool_name
  - another_tool
---
```

## Key Concepts

- **Skill Name**: Unique identifier for the skill
- **Description**: Human-readable explanation of capability
- **Allowed Tools**: List of tools the skill can invoke
- **Versioning**: Semantic versioning for compatibility

## Related

- [[obsidian-skills]] — Obsidian-specific skill implementations
- [[agent-frameworks]] — Frameworks that use skills
- [[autonomous-wiki-agent]] — Agent using skill system
