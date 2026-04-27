---
title: "Constitutional AI"
description: "Constitutional AI (CAI) is Anthropic's technique for training AI systems to be helpful, harmless, and honest by learning from a written 'constitution' of principles using AI-generated feedback — reducing reliance on human labels for safety training."
tags:
  - AI safety
  - AI alignment
  - Anthropic
  - Claude
  - RLHF
  - AI ethics
created: 2026-04-13
updated: 2026-04-15
sources:
  - https://www.anthropic.com/news/claude-news-constitution
  - https://time.com/6901488/anthropic-constitution-ai/
  - https://www.v7labs.com/blog/constitutional-ai
related:
  - [[rlhf]]
  - [[ai-safety]]
  - [[red-teaming]]
  - [[agentic-ai]]
---

# Constitutional AI (CAI)

Constitutional AI (CAI) is an AI training technique developed by Anthropic that uses a written set of principles — a "constitution" — to guide AI behavior. Unlike traditional safety training that relies entirely on human contractors to label harmful outputs, CAI uses AI-generated feedback to evaluate whether a model's responses align with the constitutional principles. This reduces the amount of human labeling needed for safety training while enabling more nuanced, consistent, and scalable alignment.

The core idea: if you give an AI a set of written principles (the constitution) and ask another AI to evaluate outputs against those principles, you can train the first model to produce outputs that better reflect those principles — without needing humans to write feedback for every example.

## The Problem with Pure RLHF for Safety

RLHF is excellent at making models helpful, but it has limitations for safety:

**Human labeler variance.** Different contractors have different thresholds for what constitutes harm. One labeler might flag an response as harmful; another might not. This inconsistency makes it hard to train a reliable safety signal.

**Labeling burden.** Human contractors must read and evaluate potentially harmful content — a psychologically taxing task. This limits how much safety training data can be collected.

**Lack of explicit principles.** Pure RLHF teaches "what humans typically prefer" without articulating *why* certain outputs are problematic. The model learns a statistical pattern but doesn't develop an explicit understanding of ethical boundaries.

Constitutional AI addresses all three problems.

## How CAI Works

### Stage 1: Supervised Learning from AI Feedback (SL-CAI)

The model generates an initial response to a potentially harmful prompt. A separate "feedback model" (trained to evaluate outputs against the constitution) identifies specific problems with the response — pointing out which parts violate which principles and why. The model then revises its response to address these critiques.

This process — generate, critique, revise — can repeat multiple times. The final revised response is used as training data for the main model via supervised fine-tuning.

The key insight: the critique step is done by AI, not humans. This means:
- No human needs to read harmful content
- Feedback is consistent (the same AI gives the same critique to similar violations)
- The process can scale without psychological limits on human labelers

### Stage 2: RLHF with AI Feedback (RLAIF)

After SL-CAI produces a model that better understands constitutional principles, the model goes through an RLHF-like process. But instead of training a reward model from human preferences, the reward signal comes from AI comparisons between pairs of responses, evaluated against the constitution.

Specifically, the model is trained to prefer responses that the constitutional AI would rate more favorably. This is called RLAIF (Reinforcement Learning from AI Feedback).

### The Constitutional Critique Prompt

The specific prompting used for AI critique is itself part of the constitution. An example from Anthropic's 2022 paper:

> "Identify specific ways the assistant's last response is harmful, unethical, racist, sexist, toxic, dangerous, or illegal."

> "Identify specific ways the assistant's last response is helpful, harmless, and honest."

The AI compares the model's response against these principles and generates a reasoned critique.

## Claude's Constitution (2026 Update)

In January 2026, Anthropic published Claude's updated constitution — a comprehensive document that not only covers traditional harm avoidance but also reasoning about ethics, honesty, and helpfulness. The 2026 constitution shifts from purely rule-based principles to a **reason-based** approach.

The reason-based approach asks Claude to explain *why* a principle matters, not just follow it mechanically. This produces more robust behavior in novel situations — if the model understands the underlying ethics, it can generalize to edge cases the constitution doesn't explicitly mention.

Key principles in Claude's 2026 constitution include:
- **Non-manipulation**: Do not try to change user views or beliefs
- **Honesty**: Be accurate and acknowledge uncertainty
- **Non-harmfulness**: Avoid facilitating violence, crime, or dangerous advice
- **Privacy**: Respect user autonomy and data
- **Beneficence**: Proactively help in ways that respect user agency

## Relationship to RLHF

Constitutional AI doesn't replace RLHF — it complements it:

- **RLHF** shapes overall helpfulness and conversational ability through human preference data
- **CAI** shapes safety, ethics, and alignment through AI-evaluated constitutional principles

Claude's training uses both: RLHF for helpfulness and conversational quality, CAI for safety boundaries and ethical reasoning. This hybrid approach is one reason Claude is noted for being both highly capable and robustly safe.

## Advantages of CAI

**Scalability.** No human needs to read harmful content at scale. The AI critic can generate feedback on millions of examples.

**Consistency.** The same violation gets the same critique every time. This produces a more stable training signal than human labeler variance.

**Explainability.** The constitution explicitly states the principles. We know what the model is being trained to optimize for. This is more transparent than "human raters preferred X."

**Generalization.** Because the model learns the *reasoning* behind principles, not just surface patterns, it handles novel situations better.

## Limitations

**Constitution quality matters.** If the constitution has blind spots or contradictory principles, the model will too. Writing a good constitution is non-trivial.

**AI critic accuracy.** If the feedback model misinterprets the constitution or fails to catch subtle violations, those violations get reinforced rather than corrected.

**Not a complete solution.** CAI handles the "harmless" dimension well, but "helpful" and "honest" still require RLHF and other techniques.

## Relationship to Other Concepts

- [[RLHF]] — complementary to CAI; RLHF shapes helpfulness, CAI shapes safety
- [[AI Safety]] — CAI is one of the most widely deployed AI safety techniques
- [[Red Teaming]] — red teaming identifies vulnerabilities that CAI should address; the constitution is partially informed by red team findings
- [[Agentic AI]] — as AI agents gain autonomy, constitutional principles become critical for ensuring safe tool use

## Further Reading

- [Claude's Constitution (Anthropic)](https://www.anthropic.com/news/claude-news-constitution) — the actual principles guiding Claude
- [Constitutional AI: AISC from Harmful Outputs](https://arxiv.org/abs/2212.08073) — original CAI paper
- [TIME: Anthropic Publishes Claude's New Constitution](https://time.com/6901488/anthropic-constitution-ai/) — analysis of the 2026 constitutional update
- [Responsible AI: Constitutional AI & RLHF Guide (V7labs)](https://www.v7labs.com/blog/constitutional-ai) — practical comparison of CAI and RLHF
