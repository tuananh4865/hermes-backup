---
title: Few-Shot Learning
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [few-shot, prompting, llm, in-context-learning, machine-learning]
---

# Few-Shot Learning

## Overview

Few-shot learning is a prompting technique that provides a language model with a handful of task examples directly in the prompt, enabling it to generalize to new, unseen inputs without fine-tuning. Rather than training a model on thousands of examples, few-shot prompting exploits the model's pre-trained knowledge and ability to recognize patterns from a minimal context. This makes it one of the most practical and widely used methods for steering [[llm]] behavior in production systems.

The term originates from the broader machine learning concept where models learn from tiny datasets—sometimes just one to five examples per class. In the LLM context, few-shot learning is more precisely called **in-context learning**: the model doesn't update its weights, but uses the examples as a guide for formatting, reasoning, and styling its response.

## Key Concepts

- **N-shot categorization**: The number of examples provided (zero-shot, one-shot, few-shot). "Few" typically means 2–10 examples.
- **Example format**: Each example usually consists of an input and its expected output, separated consistently so the model learns the mapping pattern.
- **Demonstration quality**: Examples should be representative, diverse, and free of label noise. Even ordering matters—placing harder examples later can improve performance.
- **Chain-of-thought (CoT)**: Pairing few-shot examples with step-by-step reasoning traces dramatically improves accuracy on complex tasks.
- **Calibration**: Models can be biased by example distribution. Knowing this helps you design balanced, neutral demonstrations.

## How It Works

When you provide examples in a prompt, the model performs pattern matching against its internal representations learned during pretraining. It identifies structural similarities between your examples and the new query, then generates outputs consistent with those patterns.

```
System: You are a sentiment classifier. Classify as positive or negative.

Example 1:
Input: "The food was absolutely delicious."
Output: positive

Example 2:
Input: "Terrible service, never going back."
Output: negative

Example 3:
Input: "It was fine, nothing special."
Output: negative

Now classify:
Input: "Best purchase I've made in years!"
Output:
```

The model reads the pattern across examples—positive for enthusiastic praise, negative for complaints or neutrality—and applies it to the new input. No weight updates occur; everything happens in the forward pass.

## Practical Applications

- **Classification tasks**: Sentiment analysis, spam detection, intent routing, topic labeling
- **Format transformation**: JSON structuring, translation, summarization to a specific style
- **Code generation**: Generating code snippets in a particular language or following a specific API pattern
- **Data extraction**: Pulling structured entities from unstructured text using format examples
- **Persona/style transfer**: Teaching the model to respond in a specific voice by showing dialogue examples

## Examples

### Simple Classification

```python
# Few-shot prompt for entity type extraction
prompt = """
Extract the main entity and its type from each sentence.

Example 1:
Sentence: "Apple Inc. announced a new MacBook."
Entity: Apple Inc. | Type: organization

Example 2:
Sentence: "Mount Everest is 8,849 meters tall."
Entity: Mount Everest | Type: landmark

Example 3:
Sentence: "Alice and Bob went to the store."
Entity: Alice, Bob | Type: person

Now extract from:
Sentence: "Tesla delivered 1 million cars in 2023."
Entity:
"""
```

### Chain-of-Thought with Few-Shot

```python
# Few-shot with reasoning steps
cot_prompt = """
Solve each math problem by showing your reasoning.

Example 1:
Question: If a store has 24 apples and sells 7, how many are left?
Reasoning: Start with 24 apples. Subtract 7 sold. 24 - 7 = 17.
Answer: 17

Example 2:
Question: A train travels 120 miles at 60 mph. How long does it take?
Reasoning: Time = Distance / Speed. 120 / 60 = 2 hours.
Answer: 2

Now solve:
Question: A rectangle is 8cm by 5cm. What is its area?
Reasoning:
Answer:
"""
```

## Related Concepts

- [[llm]] — Large language models that enable few-shot through in-context learning
- [[prompting]] — The broader discipline of crafting effective prompts
- [[tree-of-thought]] — An extension that explores multiple reasoning paths
- [[huggingface]] — Hub for models and datasets commonly used in few-shot experiments
- [[retrieval]] — Retrieval-augmented generation (RAG) as an alternative to few-shot for knowledge-intensive tasks

## Further Reading

- Brown et al., "Language Models are Few-Shot Learners" (GPT-3 paper, 2020)
- Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (2022)
- Kojima et al., "Large Language Models are Zero-Shot Reasoners" (2022)

## Personal Notes

Few-shot is my go-to technique for any new LLM project—it's faster than fine-tuning and far more iterative. The biggest mistake I see is dumping 20+ examples when 3-5 carefully chosen ones would work better. More examples can dilute the signal, especially if they're redundant. Also watch out for position bias: models tend to weight examples in the middle of the context less heavily. If you're seeing inconsistent outputs, try shuffling your examples or moving the most important ones to the start and end.
