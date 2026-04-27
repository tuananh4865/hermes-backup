---
title: Reflection
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [reflection, ai-agents, reasoning, self-improvement]
---

## Overview

Self-reflection in AI agents refers to the ability of an agent to observe, evaluate, and critique its own reasoning processes and outputs. Unlike traditional language models that generate responses in a single pass, reflective agents engage in iterative reasoning—pausing to assess whether their current approach is working, identifying potential errors or gaps, and adjusting their strategy accordingly. This metacognitive capability moves agents beyond pattern matching toward genuine problem-solving.

In practice, self-reflection means an agent generates internal commentary about its own decisions. When reasoning step-by-step, an agent might stop to ask: "Is this conclusion valid? What evidence supports or contradicts it? Am I missing something?" This self-questioning creates a feedback loop that improves output quality without external correction.

## Why It Matters

Self-reflection directly impacts agent quality across several dimensions. First, it enables error detection before outputs reach users—an agent that reflects on its reasoning catches logical fallacies, factual inconsistencies, and malformed tool calls early, preventing cascades of failure in multi-step tasks.

Second, reflection improves adaptivity. Agents operating in unfamiliar contexts can recognize uncertainty and pivot strategies rather than continuing down unproductive paths. This flexibility separates capable agents from brittle ones.

Third, reflection enhances transparency. When agents articulate their reasoning, users can follow the logic, identify potential issues, and make informed decisions. This interpretability matters in production environments where accountability is essential.

Finally, reflection is foundational to [[self-improvement-loops]]—without self-assessment, agents cannot identify what to improve or whether their modifications actually help.

## Techniques

Chain-of-Thought (CoT) prompting was one of the earliest reflection techniques. By instructing models to "think step by step," researchers discovered that explicit reasoning steps dramatically improved performance on complex tasks. CoT creates intermediate checkpoints where models can notice inconsistencies they might miss in shorthand reasoning. Variants include zero-shot CoT (adding "let's think step by step" to prompts) and self-consistency (generating multiple reasoning paths and selecting the most common conclusion).

ReAct (Reasoning + Acting) extended CoT by integrating tool use into the reasoning loop. Agents alternate between reasoning about their current situation and taking actions that gather information or progress toward the goal. This creates a tight feedback cycle where reasoning informs actions and action results update reasoning. ReAct excels in scenarios requiring information retrieval or environment interaction.

Other techniques include self-ask (posing follow-up questions to oneself before answering), tree of thoughts (exploring multiple reasoning branches), and reflection agents (dedicated internal agents that critique a primary agent's outputs). These methods often stack—a modern agentic system might use CoT for basic reasoning, ReAct for tool orchestration, and a separate reflection layer for quality control.

## Related

- [[self-evolving-agents]] — How reflection drives autonomous improvement
- [[agent-evaluation]] — Measuring whether reflection improves outcomes
- [[chain-of-thought]] — Foundational reasoning technique
- [[self-improvement-loops]] — Feedback mechanisms for continuous learning
- [[multi-agent-systems]] — Reflection in coordinated agent teams
- [[planning]] — Using reflection to refine agentic planning
