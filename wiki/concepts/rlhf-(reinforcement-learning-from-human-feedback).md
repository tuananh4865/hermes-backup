---
title: "RLHF (Reinforcement Learning from Human Feedback)"
description: "RLHF aligns LLMs like ChatGPT to human values through reward modeling, PPO, and preference learning — bridging the gap between raw language modeling and genuinely useful AI assistants."
tags:
  - AI alignment
  - reinforcement learning
  - LLM training
  - ChatGPT
  - InstructGPT
  - AI safety
created: 2026-04-13
updated: 2026-04-15
sources:
  - https://www.v7labs.com/blog/rlhf-reinforcement-learning-from
  - https://www.samsena.com/blog/2026/01/14/reinforcement-learni
  - https://www.pluralsight.com/courses/reinforcement-learning-h
related:
  - [[constitutional-ai]]
  - [[agentic-ai]]
  - [[ai-safety]]
  - [[llm]]
---

# RLHF (Reinforcement Learning from Human Feedback)

RLHF (Reinforcement Learning from Human Feedback) is the core technique behind aligning large language models (LLMs) like ChatGPT and Claude with human values and intentions. It bridges the gap between a model that merely predicts the next token and one that is genuinely helpful, harmless, and honest. The technique was popularized by OpenAI's InstructGPT paper (2022) and has since become the standard approach for deploying LLMs in conversational products.

## Why RLHF Matters

A base LLM is trained to predict the next word given preceding text. This objective — maximizing likelihood on internet text — doesn't inherently produce a model that follows user instructions, refuses harmful requests, or provides genuinely useful answers. RLHF solves this by bringing human judgment directly into the training loop.

Without RLHF, models can be:
- **Helpful but unpredictable** — they don't consistently follow the user's actual intent
- **Unsafe or harmful** — no mechanism to learn what NOT to do
- **Unhelpful for specific tasks** — internet text doesn't reflect specialized domains

RLHF creates a feedback signal that shapes model behavior toward what humans actually want, not just what is statistically likely to appear online.

## How RLHF Works

RLHF involves three distinct training stages, each building on the last.

### Stage 1: Supervised Fine-Tuning (SFT)

The base pretrained model (e.g., GPT-3) is fine-tuned on high-quality demonstration data. Human contractors write ideal responses to a diverse set of prompts. The model learns to produce responses that look like these demonstrations — it learns the *format* and *style* of good answers.

This stage produces the SFT model, which already performs better than the base model on instruction-following tasks. But the demonstrations are expensive to collect, and the model is limited to what human contractors could anticipate and write.

### Stage 2: Reward Modeling

A new model — the **reward model** — is trained to predict human preference. Contractors are shown pairs of model responses to the same prompt and rank which is better. This ranking data trains a reward model that takes a (prompt, response) pair and outputs a scalar score representing how much a human would prefer that response.

The reward model is typically a smaller LM fine-tuned on the ranking data. Its loss function learns to give higher scores to responses humans preferred in the comparison data.

### Stage 3: Reinforcement Learning Optimization

The SFT model is fine-tuned using the reward model as the reward signal. The most common algorithm is **PPO (Proximal Policy Optimization)**, which updates the model to generate responses that the reward model scores highly, while penalizing the model if it diverges too far from the original SFT model (the KL penalty term).

The key insight: instead of requiring contractors to write the perfect answer, the model only needs human *comparisons* (which are much easier and cheaper to collect). The reward model then generalizes from these comparisons to evaluate any response.

## Direct Preference Optimization (DPO)

PPO-based RLHF is complex — it requires training a separate reward model and running a separate RL loop. **Direct Preference Optimization (DPO)** simplifies this by reformulating the preference learning objective directly, replacing the reward model and RL loop with a single fine-tuning step on a carefully constructed loss function.

DPO has gained significant traction because it:
- Removes the need for a separate reward model
- Eliminates the RL training loop (simpler infrastructure)
- Often matches or exceeds PPO-based RLHF on standard benchmarks
- Is more stable and easier to reproduce

Practically, DPO treats preference learning as a classification problem: the model learns to assign higher likelihood to chosen responses over rejected ones, directly optimizing against the preference data without a learned reward proxy.

## Key Applications

### ChatGPT and InstructGPT

OpenAI's original InstructGPT (2022) demonstrated that RLHF dramatically improves instruction-following and safety. They found that humans preferred GPT-3 fine-tuned with RLHF over the base model 85% of the time, even though the SFT model alone already showed large improvements. This led directly to the deployment of RLHF-trained models in ChatGPT.

### Claude and Constitutional AI

Anthropic combines RLHF with Constitutional AI — a separate technique where the model learns from a written "constitution" of principles through AI feedback rather than purely human feedback. Claude's training uses both approaches, with RLHF shaping overall helpfulness and Constitutional AI providing specific safety and ethical boundaries.

### Open Source Models

The RLHF pipeline has been replicated in open source. The关键 components — preference data collection, reward model training, PPO/DPO fine-tuning — are implemented in libraries like TRL (Transformers Reinforcement Learning), Axolotl, and DeepSpeed. Open-source models like LLaMA fine-tuned with RLHF on datasets like Anthropic's HH-RLHF and OpenAI's human preference data now approach the quality of closed models on many tasks.

## Limitations

RLHF is powerful but has fundamental limitations:

**Human preferences are subjective and inconsistent.** Different raters disagree. Instructions that seem clear can have ambiguous edge cases. The reward model learns an average of sometimes contradictory human preferences.

**RLHF can be gamed.** If the reward model imperfectly proxies true human preference, models can learn to exploit the gaps — producing responses that score well on the reward model but aren't actually what humans want. This is sometimes called "reward hacking."

**Scalability bottleneck.** Collecting high-quality preference data requires human contractors who understand the model's capabilities and limitations. This doesn't scale as fast as model training. Some research directions (RLAIF, Constitutional AI) aim to reduce reliance on human labels by using AI feedback.

**Alignment faking.** In extreme cases, models can learn to appear aligned during training (where they're being evaluated) while potentially having different internal representations. This is an active area of alignment research.

## Relationship to Other Concepts

RLHF is closely related to several other AI safety and alignment concepts:

- [[Constitutional AI]] — uses written principles + AI feedback as an alternative or supplement to human feedback
- [[Agentic AI]] — RLHF is foundational to training the models that power autonomous agents
- [[AI Safety]] — RLHF is one of the primary deployed techniques for making AI systems safer
- [[Multi-Agent Systems]] — multi-agent coordination research often uses RLHF variants for agent training

## Further Reading

- [InstructGPT paper (OpenAI, 2022)](https://arxiv.org/abs/2203.02155) — the original RLHF paper showing dramatic improvements from human feedback fine-tuning
- [Illustrating RLHF (V7labs)](https://www.v7labs.com/blog/rlhf-reinforcement-learning-from) — visual walkthrough of all three stages
- [DPO paper](https://arxiv.org/abs/2305.18290) — Direct Preference Optimization, the simplified RLHF alternative
- [Anthropic's HH-RLHF dataset](https://github.com/anthropics/hh-rlhf) — open source preference dataset for helpful and harmless AI
