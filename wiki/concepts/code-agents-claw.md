---
title: Code Agents (CLAW)
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [agent, llm, code-agents, automation]
confidence: high
sources: [raw/articles/karpathy-no-priors-code-agents-claw.md]
relationships: [[karpathy]], [[skill-graph], [hermes-agent]]
---

# Code Agents (CLAW)

**CLAW** = Computer Launched Agentic Worker. Persistent AI agent that loops autonomously, manages tasks, and acts on behalf of the user.

## Key Concept from Andre Karpathy

### The December Flip

Karpathy went from **80/20** (human/agent coding) to **20/80** in December:
- Hasn't typed a line of code since December
- Spends 16 hours/day "expressing will to agents"
- Not typing code — **manifesting** through agents

### Peter Steinberg's Setup

Multiple agents working in parallel:
- 10+ Codex agents checked out on different repos
- Each task takes ~20 minutes
- He reviews their work between agents
- **Macro actions**: "here's a new functionality, delegate to agent 1"

### Token Throughput as Bottleneck

> "If you don't feel bounded by your ability to spend on tokens, then you are the bottleneck."

- Max your subscription
- Run multiple agents in parallel
- You're the constraint, not compute

## CLAW Characteristics

1. **Persistent** — Keeps looping, doesn't require interactive session
2. **Memory** — Sophisticated beyond context compaction
3. **Personality** — Feels like a teammate, can praise you
4. **Multi-agent** — Teams of agents collaborating
5. **WhatsApp/chat interface** — Natural language control

## Dobby — Home Automation CLAW

Karpathy's home agent:
- Controls lights, HVAC, shades, pool, spa, security
- Natural language: "Dobby, sleepy time" = lights off
- Security camera + AI detection
- Sends WhatsApp alerts with images
- Replaced 6 different apps

## Implications for Software

### The Unbundling

- **Old**: Apps as UX layer for every device/service
- **New**: APIs + Agents as the UX
- "Agents crumble up bespoke apps"

### The Rebundling

- Single natural language interface (WhatsApp)
- Agents orchestrate all underlying APIs
- No need for custom app per device

## Related

- [[karpathy]] — Andre Karpathy
- [[skill-graph]] — Skill graph pattern for agent instruction
- [[hermes-agent]] — Hermes agent system
