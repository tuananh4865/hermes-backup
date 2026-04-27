---
title: Chain-of-Thought
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [chain-of-thought, prompting, reasoning, llm]
---

# Chain-of-Thought

## Overview

Chain-of-Thought (CoT) prompting is a technique in [[prompt engineering]] that encourages large language models to articulate their reasoning process step by step before arriving at a final answer. Rather than producing an answer directly, the model is guided to generate a intermediate chain of logical steps that connect the problem input to its solution output. This approach emerged from research demonstrating that LLMs, particularly larger models, possess latent reasoning capabilities that can be unlocked through appropriate prompting strategies.

The key insight behind Chain-of-Thought prompting is that the process of explaining one's reasoning often leads to more accurate results than jumping directly to conclusions. This mirrors the human cognitive experience where articulating thoughts helps clarify thinking and catch errors before they propagate. When applied to LLMs, CoT prompting has shown remarkable improvements across a range of reasoning-intensive tasks including arithmetic, logical deduction, commonsense reasoning, and multi-step problem solving.

CoT prompting represents a significant shift in how we interact with language models. Traditional prompting treated the model as a direct answer-generation engine, while CoT positioning the model as a collaborative reasoning partner that works through problems visibly. This transparency not only improves output quality but also makes model behavior more interpretable, as users can trace the logical steps that led to a particular answer.

## How It Works

Chain-of-Thought prompting operates by restructuring the prompt to include explicit reasoning examples or reasoning instructions. When a user presents a problem to an LLM, they supplement the query with carefully constructed examples that demonstrate the desired reasoning format. These examples show both the problem and the step-by-step reasoning process that leads to the solution, with each step building logically on the previous one.

The mechanism works because language models are trained on vast corpora containing human-written explanatory text. When presented with reasoning chains in prompts, the model recognizes the structural pattern and applies similar reasoning to new problems. The intermediate reasoning steps serve as computational scaffolding, allowing the model to break complex problems into manageable pieces that can be processed with greater accuracy. Each reasoning step effectively primes the model for the next step, creating a cascade of relevant activations that would not occur in direct answer generation.

The effectiveness of CoT prompting scales with model size. Larger models with more parameters and better pre-training exhibit stronger Chain-of-Thought reasoning abilities, likely because they have absorbed more reasoning patterns from their training data and have greater capacity to follow complex logical structures. This size dependency means CoT prompting is most reliably effective with frontier models and larger open-source models, while smaller models may struggle to follow the reasoning chain format consistently.

## Variations

Several notable variations of Chain-of-Thought prompting have been developed to address different use cases and scenarios.

**Few-shot Chain-of-Thought** provides multiple complete examples in the prompt, where each example includes the problem, the reasoning chain, and the final answer. This approach gives the model strong structural cues about how to approach reasoning problems. The quality and diversity of the examples significantly impact performance, making example selection an important consideration. Few-shot CoT typically outperforms zero-shot approaches on complex reasoning tasks but requires more prompt engineering effort.

**Zero-shot Chain-of-Thought** eliminates the need for manually crafted examples by instructing the model to "think step by step" or similar meta-instructions. This approach relies on the model's pre-trained reasoning capabilities without providing explicit examples. While generally less effective than few-shot CoT, zero-shot variants offer practical advantages including reduced prompt engineering overhead and better generalization across diverse problem types. The simple phrase "Let's think step by step" has become a widely used zero-shot CoT trigger.

**Self-Consistency with Chain-of-Thought** is an augmentation technique that generates multiple reasoning chains for the same problem and selects the most consistent final answer. This approach acknowledges that CoT prompting can sometimes lead reasoning astray on complex problems. By sampling multiple chains and aggregating results, self-consistency improves reliability without requiring multiple models or human intervention.

**Tree of Thoughts** extends CoT reasoning by exploring multiple branching reasoning paths simultaneously rather than following a single linear chain. This allows the model to consider alternative problem-solving strategies and backtrack when a particular approach proves unproductive. Tree of Thoughts is particularly valuable for complex problems where the optimal solution path is not immediately apparent.

## Related

- [[Prompt Engineering]] - The broader discipline of crafting effective prompts for language models
- [[Large Language Models]] - The AI systems that CoT prompting is applied to
- [[Reasoning]] - The cognitive process that CoT aims to elicit and structure
- [[Self-Consistency]] - An enhancement technique for improving CoT reliability
- [[Tree of Thoughts]] - An extension of CoT that explores branching reasoning paths
- [[AI Agents]] - Systems that often incorporate CoT reasoning as part of their decision-making
- [[Few-Shot Learning]] - The broader capability that enables learning from minimal examples
