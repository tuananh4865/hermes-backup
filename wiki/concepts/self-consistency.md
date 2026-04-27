---
title: "Self Consistency"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [llm-prompting, reasoning, machine-learning, chain-of-thought]
---

# Self Consistency

## Overview

Self-consistency is a prompting technique developed to improve the reliability and accuracy of reasoning outputs from large language models. The method, introduced by Wang et al. in 2022, works by generating multiple reasoning paths for a single problem and then selecting the most consistent answer among them. Rather than relying on a single chain-of-thought reasoning trace, self-consistency encourages the model to explore diverse reasoning strategies and then aggregates the results through a majority-vote mechanism.

The core insight behind self-consistency is that complex reasoning problems often admit multiple valid approaches, and answers that emerge from several independent reasoning paths are more likely to be correct than those derived from a single chain of logic. This is particularly important because LLMs are probabilistic systems—a single generation can be sensitive to subtle prompt variations or sampling randomness. By sampling multiple times and taking the mode of the answers, self-consistency hedges against individual reasoning errors and hallucinations.

## Key Concepts

**Chain-of-Thought (CoT) Prompting** is a prerequisite for self-consistency. CoT encourages the model to explicitly lay out intermediate reasoning steps rather than jumping directly to the final answer. This produces a more interpretable reasoning trace and often leads to better results, especially for multi-step problems in arithmetic, logic, and commonsense reasoning.

**Majority Voting** is the aggregation method used in self-consistency. After generating N reasoning paths and their corresponding answers, the system tallies votes for each unique answer and returns the most frequently generated response. This simple ensemble approach is remarkably effective and requires no additional training or fine-tuning.

**Temperature Sampling** controls the randomness of LLM outputs. Higher temperature values produce more diverse reasoning paths, which is desirable for self-consistency since the goal is to explore multiple independent approaches. Typical values for self-consistency range from 0.7 to 1.0, though the optimal setting depends on the model and task.

**Path Diversity** is crucial to the technique's effectiveness. If all generated reasoning paths follow the same strategy, the majority vote provides little additional assurance. Effective self-consistency prompting uses high temperature and sometimes combinatorial variation (e.g., reordering few-shot examples) to maximize the diversity of reasoning approaches.

## How It Works

The self-consistency pipeline operates in three stages:

1. **Reasoning Generation**: The LLM is prompted with a problem and asked to produce a reasoning trace. This is done N times (often 20-40 times) with a temperature > 0, producing N distinct reasoning paths and candidate answers.

2. **Answer Extraction**: Each reasoning trace is parsed to extract the final answer. For multiple-choice problems, this is straightforward. For free-response or arithmetic problems, answer extraction may require regex patterns or careful prompting to isolate the final result.

3. **Majority Vote Aggregation**: The extracted answers are tallied, and the answer receiving the most votes is selected as the final output.

```python
def self_consistency(prompt, model, n_paths=20, temperature=0.8):
    answers = []
    for _ in range(n_paths):
        response = model.generate(prompt, temperature=temperature)
        answer = extract_answer(response)
        answers.append(answer)
    return Counter(answers).most_common(1)[0][0]
```

This method has been shown to significantly improve performance on benchmarks including GSM8K (math word problems), ARC (science questions), and SVAMP (arithmetic reasoning).

## Practical Applications

Self-consistency is particularly valuable in domains where accuracy is critical and reasoning errors can be costly. In **legal and compliance analysis**, a law firm might use self-consistency to verify that an LLM's interpretation of a regulation is robust across multiple reasoning approaches. Different reasoning paths may reference different sections of the law or apply different precedent analogies, and the majority answer is more trustworthy.

In **medical information synthesis**, self-consistency helps verify that diagnostic suggestions or treatment summaries are consistent regardless of how the model frames its reasoning. Since medical errors can have serious consequences, running multiple reasoning paths and checking for consensus adds an important layer of validation.

For **software code generation**, self-consistency can verify that a generated implementation is correct across multiple explanations of the same requirements. If the model produces the same functional code from different requirement interpretations, confidence in its correctness increases.

**Mathematical problem solving** is one of the strongest application areas. On GSM8K, self-consistency with a 40-path sample improved accuracy from around 34% (with chain-of-thought alone) to over 74% with the PaLM model. The technique essentially treats the LLM as an ensemble of reasoners.

## Examples

Consider a word problem: "A store has 15 apples. They sell 7 apples in the morning and 3 more in the afternoon. How many apples do they have left?"

A naive single-pass chain-of-thought might produce: "15 - 7 = 8, then 8 - 3 = 5, so they have 5 apples left."

With self-consistency, the model might generate multiple paths:
- Path 1: "15 - 7 = 8, 8 - 3 = 5" → 5
- Path 2: "Total sold: 7 + 3 = 10, 15 - 10 = 5" → 5
- Path 3: "Morning: 15 - 7 = 8, Afternoon: 8 - 3 = 5" → 5
- Path 4: "15 apples, sold 10 total, left = 5" → 5

All paths agree on 5, providing strong confidence. If one path had incorrectly computed 15 - 7 = 6, it would be outvoted.

## Related Concepts

- [[Chain-of-Thought Prompting]] - The foundational technique of generating step-by-step reasoning traces
- [[Large Language Models]] - The underlying technology to which self-consistency is applied
- [[Prompt Engineering]] - The broader discipline of crafting inputs to maximize LLM output quality
- [[Ensemble Methods]] - Traditional ML concept of combining multiple models, analogous to self-consistency within a single model
- [[Reasoning Augmentation]] - Techniques for enhancing LLM reasoning capabilities beyond prompting

## Further Reading

- Wang et al., "Self-Consistency Improves Chain of Thought Reasoning in Language Models" (2022) — the original paper introducing the technique
- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022) — foundational work on CoT prompting
- "The Prompt Report" by Anthropic — comprehensive survey of prompting techniques including self-consistency

## Personal Notes

Self-consistency is one of the most practical and low-cost improvements to LLM reliability. It requires no fine-tuning and can be layered on top of existing applications. The main trade-offs are increased inference cost (N times slower) and latency. For high-stakes applications where a single wrong answer is costly, this trade-off is often worth it. Consider using a lower N (e.g., 5-10) for faster iteration and increasing to 20-40 for production or high-stakes queries.
