---
title: "Anthropic"
created: 2026-04-15
updated: 2026-04-19
type: entity
tags: [ai-company, safety, llm, anthropic, claude]
related:
  - [[claude]]
  - [[claude-code]]
  - [[ai-safety]]
  - [[openai]]
  - [[google-gemini]]
sources:
  - https://www.anthropic.com/
  - https://www.anthropic.com/research
  - https://www.anthropic.com/transparency
  - https://www.anthropic.com/responsible-scaling-policy/roadmap
  - https://www.scientificamerican.com/article/anthropics-safety-first-ai-collides-with-the-pentagon-as-claude-expands-into/
  - https://thehill.com/policy/technology/5824219-anthropic-new-ai-dangerous-public/
---

# Anthropic

> AI safety and research company behind Claude. Founded in 2021 by Dario Amodei, Daniela Amodei, and other former OpenAI researchers.

## Overview

**Anthropic** is an AI safety and research company based in San Francisco, working to build reliable, interpretable, and steerable AI systems. The company is best known for [[Claude]], its flagship AI assistant, and for its constitutional AI approach to alignment.

**Founded:** 2021 by Dario Amodei (CEO), Daniela Amodei (President), and others
**Headquarters:** San Francisco, California
**Funding:** $7.3B+ raised (as of 2025), investors include Google, Salesforce, Spark Capital

## Mission & Safety Focus

Anthropic's core differentiator is its **safety-first philosophy**. The company has explicitly drawn red lines:

- **No mass surveillance of Americans** — Claude will not be used for mass surveillance applications
- **No fully autonomous weapons** — Anthropic will not provide AI for fully autonomous weapons systems

CEO Dario Amodei has stated Anthropic will refuse contracts that violate these principles, even at significant revenue cost.

## Key Products

### Claude

Claude is Anthropic's flagship AI assistant, available in three main tiers:

| Model | Position | Best For |
|-------|----------|----------|
| **Claude Opus 4** | Most capable | Complex research, coding, analysis |
| **Claude Sonnet 4** | Mid-range | Balanced performance and speed |
| **Claude Haiku 3** | Fast, affordable | High-volume, low-latency tasks |

All three models support the Claude Code agentic coding tool.

### Claude Code

Command-line coding agent that runs locally. Ships as a CLI tool (`npm install -g @anthropic-ai/claude-code`) and as integrations for VS Code and JetBrains IDEs.

### Claude Team Plan

Anthropic's Team plan offers higher usage limits and faster inference for organizations, positioning Claude as an enterprise alternative to consumer ChatGPT.

## Research

Anthropic publishes research on:

- **Constitutional AI (CAI)** — Training AI systems to be helpful, harmless, and honest using a set of guiding principles
- **Interpretability** — Understanding what happens inside neural networks
- **Responsible Scaling Policy** — Framework for safely deploying increasingly capable AI models
- **AI Safety** — Measurable evaluations of model capabilities and risks

### The Mythos Model Controversy (April 2026)

In April 2026, Anthropic announced it would hold back the full release of a new model (codenamed "Mythos") because it believes the model poses unprecedented cybersecurity risks. The company published a detailed report on the model's capabilities, including:

- Ability to discover novel zero-day vulnerabilities
- Autonomous exploit development potential
- Capabilities that exceed what the company believes should be publicly released

This marked a significant escalation in Anthropic's "responsible disclosure" approach to frontier AI safety.

### Claude Sonnet 4.6 Release (February 2026)

Released under the same safety standard (ASL-3), Claude Sonnet 4.6 continues improvements in cybersecurity evaluations. The model demonstrates meaningful progress in AI's ability to assist defenders — Anthropic positioned Claude Code Security as a "force multiplier" for security teams, reportedly having prevented over $15B in potential cyber losses.

## Business & Partnerships

### Google Partnership

Anthropic has a significant partnership with Google Cloud, making Claude available via Google Cloud's Vertex AI. This positions Anthropic as a competitor to OpenAI's Azure integration while leveraging Google's cloud infrastructure.

### Enterprise Focus

Anthropic has been more conservative than OpenAI in enterprise dealmaking, prioritizing safety partnerships over rapid commercialization. Notable enterprise customers include:

- Salesforce (via Slack integration)
- Samsung (mobile device AI)
- Multiple Fortune 500 companies (confidential)

## Financials & Valuation

Anthropic was valued at approximately **$18.4B** in its 2025 funding round, making it one of the most valuable AI startups alongside OpenAI ($157B) and xAI ($50B).

## Related Concepts

- [[claude]] — Anthropic's flagship AI assistant
- [[claude-code]] — Anthropic's CLI coding agent
- [[ai-safety]] — AI safety as a field and Anthropic's approach
- [[openai]] — Primary competitor
- [[google-gemini]] — Another major AI competitor
