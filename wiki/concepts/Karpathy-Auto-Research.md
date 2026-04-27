---
title: Karpathy Auto Research
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [karpathy, auto-research, self-improving-ai, ai-optimization, llm-ops]
description: Karpathy's self-improving AI framework that autonomously optimizes AI agents and skills against real-world data.
source: https://youtu.be/bc4NrE0cOE0
---

## Overview

Auto Research is a framework introduced by Andrej Karpathy that enables AI agents to become self-improving. The core concept: define measurable criteria for what you want to optimize, then let the AI autonomously run an optimization loop — testing hypotheses, evaluating outcomes, and iteratively improving — without constant human feedback.

When applied well, it lets AI agents and skills autonomously optimize against real-world data: cold email campaigns, landing page conversions, content engagement, or anything measurable.

## Core Loop

The Auto Research framework runs a continuous optimization loop:

```
1. Define criteria → What exact conditions must be true/false?
2. Establish baseline → Run tests with current version, score it
3. Generate hypothesis → Propose a specific change that might improve the score
4. Run iteration → Test the updated version with a separate sub-agent
5. Evaluate outcome → Judge passes/fails (script-based for deterministic, LLM judge for subjective)
6. Decide → Keep the change if it improved score, discard if not
7. Repeat → Until goal is reached or max iterations hit
```

## Key Concepts

### Criteria Definition (The Most Important Part)

The framework only becomes as good as the criteria you define. Rules for good criteria:

- **Binary outcomes** — The result must be true or false, not subjective
- **Exact conditions** — Not "make hooks short" but "first line must be under 136 characters"
- **One variable per criteria** — If you need "and" to describe it, split into two separate criteria

### Two Evaluation Modes

| Mode | Use Case | Example |
|------|----------|---------|
| Script/Deterministic | Clear-cut rules with code-checkable outcomes | Character count, format compliance |
| LLM Judge | Subjective or pattern-matching tasks | Tone matching, writing framework adherence |

### Three-Layer Framework for Subjective Skills

Even creative/subjective tasks like LinkedIn copywriting can be optimized:

1. **Hard rules** — Clear-cut best practices (hook < 136 chars, sentence length 5-12 words)
2. **Pattern matching** — Your unique writing patterns (bold claims need nuance words like "I think", "I believe")
3. **Creative layer** — Some subjectivity remains that can't be optimized

## Applications

### Optimize AI Skills
- LinkedIn writer skill: hook length, bullet format, writing framework compliance
- Newsletter subject lines: improve open rates
- Landing page copy: improve CTR
- Email sequences: improve open rates

### Optimize Processes
- Second brain / knowledge management (wiki link creation, knowledge retrieval)
- Accounting/invoicing workflows
- Customer support responses

### Autonomous Weekly Optimization
Set up scheduled tasks to run optimization loops on a cadence:

1. Pull last week's performance data
2. Define new hypothesis based on results
3. Make changes (e.g., new H1 copy)
4. Next week: scrape data, keep change if metrics improved, revert if not
5. Generate next hypothesis

Example target: "Run until average likes reaches 250" or "Run 10 iterations max"

## Architecture

```
Main Agent (you interact with)
├── Auto Research Skill
│   ├── Test Runner sub-agent (runs tests with new version)
│   ├── LLM Judge sub-agent (evaluates subjective outcomes)
│   └── Eval script (evaluates deterministic outcomes)
└── Dashboard → shows all iterations, what was kept/discarded, improvement %
```

The separation between Test Runner and Judge ensures unbiased evaluation — the judge doesn't know which version it's evaluating.

## Real-World Data Optimization

The most powerful use case: feed real-world performance data into the loop.

**Example workflow:**
1. Pull top-performing and worst-performing LinkedIn posts + engagement data
2. Ask Claude to identify patterns (hook type vs. metrics, CTA analysis vs. metrics, writing framework vs. metrics)
3. Generate hypotheses based on patterns found
4. Run autonomous optimization loop against those hypotheses
5. Schedule to run weekly, iterating on the best-performing combinations

## Caveats

- **Token cost** — Running 10+ iterations can get expensive. Optimize skills you use frequently.
- **Diminishing returns** — In testing, performance often degrades after 10-15 iterations. Cap iterations.
- **Start with well-defined skills** — Get skills working well with manual evals before going autonomous.
- **Human in the loop available** — Can set up guardrails if you're not comfortable with full autonomy.

## Related

- [[AI Agents]] — The broader concept of autonomous AI systems
- [[LLM Operations]] — Operational practices for running LLMs in production
- [[Prompt Engineering]] — Crafting effective prompts for AI systems
- [[Skills 2.0]] — Claude's skill creation and evaluation system
