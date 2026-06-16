---
name: ai-agent-frameworks
description: "Research, analyze, and apply AI coding agent frameworks — Loop Engineering, harness engineering, sub-agent patterns. When Anh shares an X/Substack article about coding agents (Claude Code, Codex, OpenAI tools, MCP), or asks to compare agent architectures, or wants to implement a 5-block loop pattern (automations, worktrees, skills, MCP, sub-agents)."
title: AI Agent Frameworks — Research & Application
created: 2026-06-01
updated: 2026-06-01
type: skill
tags: [ai, agents, engineering, research, framework, loop-engineering]
confidence: high
relationships: [xurl, hermes-autoresearch]
trigger: |
  - Anh shares an article/tweet about Claude Code, Codex, MCP, sub-agents, or AI agent patterns
  - Anh asks "phân tích bài này" + URL of an X post or Substack about coding agents
  - Anh asks about applying agent patterns to his own workflows
  - Anh wants to implement automations, worktrees, skills, MCP, or sub-agents
---

# AI Agent Frameworks — Research & Application

## Trigger Conditions

Load this skill when Anh:
- Shares a tweet/Substack URL about Claude Code, Codex, MCP, sub-agents, or AI agent frameworks
- Asks to analyze a recent article by Addy Osmani, Boris Cherny, Peter Steinberger, or other AI agent thought leaders
- Wants to implement 5-block loop pattern (automations, worktrees, skills, MCP, sub-agents) in his own systems
- Asks "what's new in AI agent development" or "latest coding agent trends"

## Core Frameworks Covered

### 1. Loop Engineering (Addy Osmani, June 2026)

**Definition:** Replacing the human-as-prompter with a system that recursively prompts the agent. A loop = a recursive goal where you define purpose and AI iterates until complete.

**5 Building Blocks + 1:**
| # | Block | Codex | Claude Code |
|---|-------|-------|-------------|
| 1 | Automations (heartbeat) | Automations tab | `/loop`, `/goal`, hooks, GitHub Actions |
| 2 | Worktrees (isolation) | Built-in worktrees | `git worktree`, `--worktree`, `isolation: worktree` |
| 3 | Skills (project knowledge) | `$skill` or `/skills` | `SKILL.md` folders |
| 4 | Plugins/Connectors (MCP) | MCP support | MCP support |
| 5 | Sub-agents (maker vs checker) | `.codex/agents/` TOML | `.claude/agents/` + teams |
| +1 | Memory (state file) | Markdown / Linear | External files |

**3 Pitfalls (KEEP these in mind):**
1. **Verification is still on you** — loop running unattended is loop making mistakes unattended
2. **Comprehension debt** — faster loop = bigger gap between what exists and what you understand
3. **Cognitive surrender** — easy to stop having an opinion and just take whatever the loop gives back

### 2. Agent Harness Engineering (cousin of Loop Engineering)

**Definition:** The environment a single agent runs inside + the factory model = the system that builds the software. Loop engineering sits ONE FLOOR ABOVE the harness.

**Components:**
- Skills (project context, conventions)
- Tools/MCP (real-world action)
- Memory (state between runs)
- Sub-agents (specialization)

### 3. Multi-Agent Orchestration Patterns

**Key insight from 0xCodez (Claude Managed Agents):**
- Up to 20 agents in a roster
- Each agent has own model + prompt + scoped toolset
- Coordinator agent delegates to specialists in parallel
- `agent_toolset_20260401` enables delegation
- Common split: 1 explores, 1 implements, 1 verifies

## Research Methodology (When Anh Shares URL)

### Step 1: Fetch Content
```python
# Try in order
mcp_exa_web_fetch_exa(urls=[URL], maxCharacters=10000)
# If fails, fall back to:
mcp_exa_web_search_exa(query="<author> <topic> <date>", numResults=5)
```

### Step 2: Identify the Author's Original Sources
For AI agent articles, the original insight usually traces back to:
- Anthropic engineering docs
- OpenAI cookbook
- Boris Cherny (head of Claude Code)
- Peter Steinberger (coding agent practitioner)
- Addy Osmani (engineering leadership perspective)

**Always cite which source an article builds on** — most AI agent articles in 2026 are derivative summaries.

### Step 3: Classify the Article
| Type | Signal | Response |
|------|--------|----------|
| Original essay | Long-form, new framework, multiple examples | Deep analysis, extract framework |
| TL;DR / Roadmap | "X-step roadmap" + bullet points | Quick comparison with original |
| Tutorial / How-to | Step-by-step, code examples | Extract reusable patterns |
| Opinion / Take | Hot take on existing framework | Note the opinion, compare to other takes |

### Step 4: Distill Actionable Patterns
For each framework, extract:
- **What it is** (1-sentence definition)
- **When to use it** (trigger conditions)
- **How to apply it** (concrete steps)
- **Pitfalls** (what goes wrong)

## Application Workflow (For Anh's Systems)

When Anh wants to apply a framework to his Felix model / Hermes / worker system:

### Step 1: Gap Analysis
Compare the framework's components to Anh's current setup:
| Framework Component | Hermes Equivalent | Match? |
|---------------------|-------------------|--------|
| Automations | Heartbeat worker + cron jobs | ✅ 80% |
| Worktrees | Sub-agents in different contexts | ⚠️ Need explicit isolation |
| Skills | Skills (gskill files) | ✅ 100% |
| Plugins/MCP | MCP servers (browser, exa, v.v.) | ✅ 100% |
| Sub-agents | Single agent per task | ❌ **Missing maker vs checker split** |
| Memory | Wiki + memory system | ✅ 100% |

### Step 2: Recommend Top 3 Actions
Always recommend in priority order with concrete first-step:

1. **Sub-agent checker pattern** (biggest gap)
   - Worker (maker) → Worker (checker) → Hermes review → Anh approve
   - Use case: research, script writing, code generation
   - First step: Add a verification step in current workflow

2. **Implement `/goal` primitive** (loop until verified)
   - Worker agent runs loop until PASS verified condition
   - Use case: content posting, data gathering, batch processing
   - First step: Define a verifiable condition for one workflow

3. **State file for long-running workflows**
   - Loop records: tried, passed, failed, next
   - Use case: multi-day research, content production pipeline
   - First step: Add `state.md` to one ongoing project

### Step 3: Anti-Patterns to Avoid

❌ **Looping without verification** — agent says "done" but isn't
❌ **Skipping human review** — even with checker, you still need to ship code you understand
❌ **Too many automations at once** — start with 1, scale later
❌ **Ignoring token cost** — loop's token burn can dwarf prompt-engineering cost
❌ **Cognitive surrender** — taking loop output without thinking

## Response Style for AI Agent Analysis

When Anh shares an article URL:

### Format
1. **Quick classification** (1 line): "This is a TL;DR of Addy Osmani's essay"
2. **Summary** (2-3 sentences): Core thesis
3. **Framework extraction**: Tables, comparison to other frameworks
4. **Application to Anh's systems**: 3 specific recommendations
5. **Source attribution**: Where the original insight came from

### Tone
- Vietnamese casual ("anh" + "em" for non-TikTok context)
- Direct, no fluff
- 3 actionable next steps, not "let me know what you want"

### Avoid
- Re-explaining the article in full
- Listing options without committing
- Asking "có muốn em đi sâu vào cái nào?"
- Inventing facts not in the source

## Sources to Track

| Source | Frequency | Best For |
|--------|-----------|----------|
| Addy Osmani Substack | ~2x/month | Engineering management + AI agents |
| Boris Cherny (Claude Code head) | ~1x/month | Claude Code roadmap, primitives |
| Peter Steinberger | ~1x/month | Practitioner insights |
| 0xCodez | ~5x/week | TL;DR summaries, X-specific trends |
| Anthropic Engineering Blog | ~2x/month | Official Claude Code updates |
| OpenAI Cookbook | ~3x/month | Codex patterns, multi-agent |

## Related
- [[xurl]] — X/Twitter research tool
- [[hermes-autoresearch]] — Nightly research loop (already implements automations pattern)
- `references/loop-engineering-summary.md` — Full summary of Addy Osmani's essay (created 2026-06-01)
- `references/ai-agent-articles-log.md` — Log of articles researched this skill
