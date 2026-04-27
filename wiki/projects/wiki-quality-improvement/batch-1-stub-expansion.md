---
title: "Batch 1: Stub Expansion Plan"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [auto-filled, wiki, quality-improvement]
related:
  - [[self-healing-wiki]]
  - [[wiki-quality-improvement]]
---

# Batch 1: Stub Expansion Plan

## Pages to Expand (10 pages)

---

## 1. coding-agents.md

### Current State
- Stub page, minimal content
- Score: ~3.6/10

### Target
- 500+ words
- 5+ wikilinks
- Code examples
- Real use cases

### Content Outline
```markdown
# AI Coding Agents

## Overview
What are AI coding agents, why they matter.

## Top Coding Assistants

### Claude Code (Anthropic)
- Strengths: Code editing, debugging, explanation
- Use cases: General coding, refactoring, code review
- Installation: `npm install -g @anthropic-ai/claude-code`

### Cursor
- Strengths: IDE integration, autocomplete
- Use cases: Daily coding, pair programming

### GitHub Copilot
- Strengths: Contextual suggestions
- Use cases: Boilerplate, tests

### OpenAI Codex
- Strengths: API access, automation
- Use cases: Scripting, batch operations

## Comparison Table
| Assistant | Strength | Best For |
|-----------|----------|----------|
| Claude Code | Reasoning | Complex refactoring |
| Cursor | IDE-native | Daily coding |
| Copilot | Speed | Boilerplate |

## Related Concepts
- [[autonomous-wiki-agent]] - How to build agents
- [[agent-frameworks]] - Frameworks for building agents
- [[vibe-coding]] - Using AI for coding
```

---

## 2. open-source-ai-agents.md

### Content Outline
```markdown
# Open-Source AI Agents

## Landscape Overview
Major open-source AI agents in 2024-2025.

## AutoGPT Family
- AutoGPT: Pioneering autonomous agents
- BabyAGI: Simplified task-driven agents
- AgentGPT: Web interface

## LangChain-based Agents
- LangChain Agents: Tool-use agents
- LlamaIndex Agents: RAG-powered agents

## Other Notable Agents
- Superagent: Simple agent framework
- ShortGPT: Video/content agents

## Installation Examples
```bash
pip install autogpt
pip install langchain
```

## Related
- [[agent-frameworks]]
- [[multi-agent-systems]]
```

---

## 3. agent-frameworks.md

### Content Outline
```markdown
# AI Agent Frameworks

## Why Use Frameworks
Abstraction, tool use, memory, orchestration.

## LangGraph
- Graph-based workflow
- State management
- Use case: Complex multi-step agents

```python
from langgraph.graph import StateGraph
```

## CrewAI
- Role-based agents
- Collaborative tasks
- Use case: Multi-agent collaboration

## AutoGen (Microsoft)
- Conversational agents
- Code execution
- Use case: Software development teams

## LlamaIndex Agents
- RAG-native
- Knowledge retrieval
- Use case: Research assistants

## Comparison
| Framework | Strength | Best For |
|-----------|----------|----------|
| LangGraph | Flexibility | Complex workflows |
| CrewAI | Simplicity | Team tasks |
| AutoGen | Code | Dev teams |

## Related
- [[coding-agents]]
- [[multi-agent-systems]]
```

---

## 4. ai-code-assistants.md

### Content Outline
```markdown
# AI Code Assistants Comparison

## Categories
1. IDE Plugins (Cursor, Copilot)
2. CLI Tools (Claude Code, Codex)
3. Web-based (AgentGPT, ChatGPT)

## When to Use What

### Daily Coding → IDE Plugin
- Cursor, Copilot
- Real-time suggestions

### Complex Refactoring → CLI
- Claude Code
- Deep reasoning, full context

### Quick Tasks → Web
- ChatGPT, Claude.ai
- One-off scripts

## Code Examples
```bash
# Claude Code
claude "Write a Python script to..."
```

## Related
- [[coding-agents]]
- [[vibe-coding]]
```

---

## 5. autonomous-wiki-agent.md (EXPAND EXISTING)

### Content Outline
```markdown
# Autonomous Wiki Agent

## Overview
How Hermes Agent manages the wiki brain.

## Core Capabilities

### Self-Healing
- Broken link detection
- Missing frontmatter repair
- Stale content refresh

### Self-Improvement
- Gap analysis
- Content generation
- Quality scoring

### Task Execution
- Priority-based task queue
- Sub-agent delegation
- Progress tracking

## Implementation Details

### Scripts
- `wiki_lint.py`: Health checks
- `wiki_self_heal.py`: Auto-fix issues
- `wiki_self_critique.py`: Quality scoring

### Cron Jobs
- Daily: Self-heal at 3 AM
- Weekly: Health check Monday 2 AM
- Morning: Research + planning 7:30 AM

## Related
- [[self-healing-wiki]]
- [[karpathy-llm-wiki]]
- [[multi-agent-systems]]
```

---

## 6. multi-agent-systems.md (EXPAND EXISTING)

### Content Outline
```markdown
# Multi-Agent Systems

## Overview
Multiple AI agents working together.

## Agent Roles
- Orchestrator: Coordinates other agents
- Specialist: Handles specific domains
- Critic: Reviews and validates

## Communication Patterns
1. **Hierarchical**: Orchestrator → Specialists
2. **Peer-to-peer**: Agents share information
3. **Debate**: Agents argue different perspectives

## Framework Examples

### CrewAI
```python
from crewai import Agent, Task, Crew
```

### LangGraph
```python
# Multi-agent with state
```

## Use Cases
- Research: One agent searches, one synthesizes
- Coding: One writes, one reviews
- Planning: One generates, one critiques

## Related
- [[agent-frameworks]]
- [[agentic-ai]]
```

---

## 7. self-healing-wiki.md (EXPAND EXISTING)

### Content Outline
```markdown
# Self-Healing Wiki

## Overview
Wiki that detects and fixes its own problems.

## Healing Mechanisms

### 1. Broken Link Detection
- Run: `python3 scripts/wiki_lint.py`
- Auto-fix: Create stub pages or remove link

### 2. Missing Frontmatter
- Auto-add required fields:
  - `created:`
  - `updated:`
  - `tags:`

### 3. Stale Content Detection
- Pages not updated in 30+ days
- Auto-refresh trigger

### 4. Orphan Detection
- Pages with no inbound links
- Auto-link to index

## Scripts
- `wiki_lint.py --auto-fix`: Fix issues
- `wiki_self_heal.py --fix --all`: Comprehensive heal
- `wiki_self_critique.py`: Quality scoring

## Related
- [[autonomous-wiki-agent]]
- [[wiki-enhancement-roadmap]]
```

---

## 8. karpathy-llm-wiki.md (EXPAND EXISTING)

### Content Outline
```markdown
# Karpathy LLM Wiki Pattern

## Overview
Andrej Karpathy's approach to knowledge management with LLMs.

## Key Principles

### 1. Raw → Wiki Pipeline
- Raw: Unmodified source material
- Wiki: LLM-synthesized knowledge
- Never modify raw sources

### 2. Incremental Building
- Add sources gradually
- Update as understanding grows
- Cross-reference continuously

### 3. LLM as Writer
- Let LLM synthesize
- Human reviews and refines
- Quality over quantity

## Directory Structure
```
raw/           # Sources (never edit)
wiki/          # LLM-generated
  concepts/    # Knowledge
  entities/    # People, tools
  sources/     # Source summaries
```

## Implementations
- [[mduongvandinh/llm-wiki]]
- [[graphify]]

## Related
- [[rag]]
- [[knowledge-graphs]]
```

---

## 9. local-llm-agents.md (CREATE NEW)

### Content Outline
```markdown
# Local LLM Agents

## Overview
Running AI agents on local hardware.

## Why Local?

### Privacy
- Data stays on machine
- No API calls

### Cost
- Free after hardware investment
- Unlimited usage

### Customization
- Fine-tune on your data
- Custom prompts

## Tools

### LM Studio
- GUI for model management
- OpenAI-compatible API
- Download models from library

### Ollama
- CLI-first
- Model library
- Run anywhere

### MLX (Apple Silicon)
- Optimized for M1/M2/M3
- Fast inference
- llama.cpp alternative

## Setup Example
```bash
# Ollama
ollama pull llama3
ollama run llama3

# LM Studio
# Download, install, load model
```

## Agent Integration
- Connect via OpenAI-compatible API
- Use [[agent-frameworks]] with local endpoint

## Related
- [[local-llm-agents]]
- [[lm-studio]]
- [[agent-frameworks]]
```

---

## 10. agentic-ai.md (CREATE NEW)

### Content Outline
```markdown
# Agentic AI

## Definition
AI that can:
1. Perceive environment
2. Plan actions
3. Execute autonomously
4. Learn from results

## vs Traditional AI

| Aspect | Traditional AI | Agentic AI |
|--------|---------------|------------|
| Input | Fixed dataset | Dynamic environment |
| Output | Single prediction | Multi-step actions |
| Memory | None | Persistent |
| Autonomy | None | High |

## Key Capabilities

### 1. Tool Use
- Call APIs
- Read/write files
- Execute code

### 2. Planning
- Break down goals
- Sequence actions
- Handle failures

### 3. Memory
- Short-term: Current context
- Long-term: Past experiences

### 4. Self-Correction
- Error detection
- Recovery strategies
- Learning

## Examples
- [[autonomous-wiki-agent]]
- [[coding-agents]]
- [[multi-agent-systems]]

## Related
- [[agent-frameworks]]
- [[self-improvement-loops]]
```

---

## Execution Order
1. coding-agents.md
2. open-source-ai-agents.md
3. agent-frameworks.md
4. ai-code-assistants.md
5. autonomous-wiki-agent.md (expand)
6. multi-agent-systems.md (expand)
7. self-healing-wiki.md (expand)
8. karpathy-llm-wiki.md (expand)
9. local-llm-agents.md (create)
10. agentic-ai.md (create)

---

## Metadata
_plan_created: 2026-04-11
_batch: 1
_pages: 10
