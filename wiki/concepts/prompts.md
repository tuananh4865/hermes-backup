---
title: "Prompts"
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [prompt-engineering, llm, context-engineering]
related:
  - [[context-engineering]]
  - [[vibe-coding]]
  - [[agentic-ai]]
---

# Prompts

A **prompt** is the primary interface between humans and LLMs — the input text that guides a model to produce a desired output. In AI agent systems, prompts (or **prompt templates**) are carefully structured to enable consistent, high-quality responses across different tasks and contexts.

## Prompt Engineering Core Principles

### 1. Be Specific and Direct
- State exactly what you want the model to do
- Include format requirements (JSON, markdown, bullet points)
- Define the scope: what IS included, what IS NOT included

### 2. Provide Context
- Background information the model needs
- Relevant domain knowledge
- User/audience description
- Historical information about the task

### 3. Chain of Thought / Reasoning
- Ask the model to "think step by step" for complex推理 tasks
- Use ReAct pattern: Thought → Action → Observation → Response
- Enable the model to self-correct mid-reasoning

### 4. Output Formatting
- Specify exact output schema
- Use examples (few-shot prompting)
- Include guardsrails for safety

## Prompt Patterns in Agent Systems

### System Prompts
The base instruction defining the agent's role, behavior, and constraints:

```
You are a [ROLE] that specializes in [DOMAIN].
You ALWAYS [BEHAVIOR 1].
You NEVER [BEHAVIOR 2].
When given [TRIGGER], you [RESPONSE].
```

### Tool-Calling Prompts
Structured prompts that invoke external functions:

```
When the user asks about [TOPIC], call the function search_web(query="...").
When the user asks to [ACTION], call the function execute_code(code="...").
```

### Memory-Augmented Prompts
Prompts that include retrieved context:

```
Relevant context from your knowledge base:
---
[RETRIEVED CONTENT HERE]
---

Based on this context, answer the following question:
[USER QUESTION]
```

### Multi-Agent Prompts
Each agent in a multi-agent system has a specialized prompt defining its role:

**Example — Supervisor Agent**:
```
You are the coordinator of a research team.
You delegate questions to the appropriate specialist agent:
- Code questions → Software Engineer
- Research questions → Research Analyst
- Design questions → Product Designer

Analyze the user's request and delegate to the right agent.
```

**Example — Researcher Agent**:
```
You are a Research Analyst specializing in [DOMAIN].
Your job is to gather, synthesize, and summarize information.
Always cite your sources.
Output in structured format: Summary, Key Points, Sources.
```

## Context Window Management

With modern LLMs (GPT-4o 128K, Claude 3.5 200K, Gemini 1.5 1M), prompt composition matters more than ever:

- **Position matters**: Information at the start and end of context is remembered best
- **Compression**: Use summarized/aggressive context before raw content
- **Retrieval prioritization**: Only include the most relevant context

## Prompt Templates vs. Hardcoded Prompts

| Approach | Pros | Cons |
|----------|------|------|
| **Hardcoded** | Simple, predictable | Inflexible, hard to maintain |
| **Template-based** | Flexible, dynamic | More complex, needs testing |
| **Learned/Evolved** | Optimized for task | Requires training infrastructure |

## Self-Evolving Prompts (2026 Frontier)

Per Andrej Karpathy (March 2026): Agents that **modify their own prompts** based on failure cases and success patterns. The agent generates candidate prompts, tests them against evaluation criteria, and converges on better instructions over time.

This closes the loop between deployment and improvement — instead of humans hand-crafting prompts, the agent continuously refines its own instruction set.

## Related Concepts

- [[context-engineering]] — The broader discipline of maximizing LLM performance through context management
- [[vibe-coding]] — Natural language prompting for code generation
- [[agentic-ai]] — Agents that go beyond prompts to act autonomously
