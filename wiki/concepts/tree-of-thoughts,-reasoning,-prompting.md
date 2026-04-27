---
title: "Tree of Thoughts (ToT)"
description: "Tree of Thoughts prompting enables LLMs to explore multiple reasoning paths as a branching tree, evaluating intermediate steps and backtracking when needed — dramatically outperforming chain-of-thought on complex problem-solving tasks."
tags:
  - prompting
  - reasoning
  - LLM
  - problem-solving
  - chain-of-thought
  - inference
created: 2026-04-13
updated: 2026-04-15
sources:
  - https://arxiv.org/abs/2305.10601
  - https://www.v7labs.com/blog/tree-of-thoughts-prompting
  - https://www.geeksforgeeks.org/tree-of-thought-reasoning
related:
  - [[chain-of-thought-prompting]]
  - [[self-improving-ai]]
  - [[llm-reasoning]]
  - [[prompting-techniques]]
---

# Tree of Thoughts (ToT)

Tree of Thoughts (ToT) is a prompting framework that extends Chain of Thought by allowing LLMs to explore multiple reasoning paths as a branching tree rather than a single linear chain. Rather than committing to the first plausible answer, a ToT-enabled model generates several intermediate thought steps, evaluates their promise, and selectively pursues the most promising branches — backtracking when necessary. This mirrors how humans solve complex problems: we consider alternatives, reject dead ends, and pursue multiple lines of reasoning simultaneously.

## Why Chain of Thought Falls Short

Chain of Thought (CoT) prompting was a breakthrough — by instructing models to "think step by step," we got dramatic improvements on reasoning tasks. But CoT has a fundamental limitation: it commits to a single reasoning path. If the first chain of reasoning goes down the wrong track, the model has no mechanism to recognize and correct course.

Complex problems often require exploration:
- A proof might require trying multiple lemmas before finding the right approach
- A creative task might need to evaluate several directions before settling on the best
- Strategic decisions require considering multiple options and their consequences

CoT's linear nature makes it brittle on exactly these kinds of problems.

## The ToT Framework

ToT generalizes CoT by framing problem-solving as tree search over a space of possible reasoning paths. The framework has four stages:

### 1. Thought Decomposition

The problem is broken into discrete thought steps. Each thought should be:
- **Self-contained** — a coherent intermediate conclusion
- **Evaluable** — possible to assess whether it brings progress toward the solution
- **Not too large** — manageable enough to generate reliably

For example, in a creative writing task, thoughts might be plot directions. In a math problem, they might be intermediate equations or lemmas.

### 2. Thought Generation

The model generates candidate thoughts at each state. Two strategies:
- **Sampling** — generate multiple independent thoughts by prompting the model multiple times with the same state (works well when variety is valuable)
- **Sequential** — prompt the model to propose thoughts one after another (works when the model benefits from building on its own ideas)

### 3. State Evaluation

Each candidate thought/state is evaluated by the model. The evaluation asks: "Does this thought bring me closer to solving the problem?" The model assigns a score or classification (e.g., "promising / neutral / hopeless").

This evaluation step is what enables the tree structure — instead of just following one path, the model can compare alternatives.

### 4. Search Algorithm

The evaluated tree is traversed using a search algorithm. Common choices:
- **BFS (Breadth-First Search)** — explore all nodes level by level, maintaining a frontier of the most promising states
- **DFS (Depth-First Search)** — pursue a single promising branch deeply before backtracking
- **Beam search** — maintain the top-k most promising states at each step

The choice depends on the problem structure and computational budget.

## Key Results

The original ToT paper (Yao et al., 2023, NeurIPS) showed dramatic improvements over CoT on tasks requiring strategic reasoning:

- **Game of 24**: Given four numbers, use arithmetic to reach 24. ToT solved 49% vs 7% for CoT.
- **Creative writing**: Given partial constraints, produce coherent text. Human evaluators strongly preferred ToT outputs.
- **Mini crossword puzzles**: ToT solved 78% of puzzles vs 16% for CoT.

The key insight: tasks where "getting stuck" on a wrong path is costly benefit most from ToT's exploration and backtracking.

## ToT vs Other Prompting Approaches

| Approach | Exploration | Backtracking | Best For |
|----------|-----------|--------------|----------|
| Standard prompting | None | No | Simple factual tasks |
| Chain of Thought | Linear | No | Multi-step reasoning |
| Self-Consistency | Multiple (post-hoc) | No | Math/decision aggregation |
| Tree of Thoughts | Branching | Yes | Complex problem-solving |
| Graph of Thoughts | Graph structure | Yes | Multi-domain problems |

ToT sits at a sweet spot: it introduces genuine branching exploration and backtracking without the complexity of full graph-based approaches.

## Implementing ToT in Practice

### Simple ToT with Beam Search

```python
def tot_beam_search(model, prompt, k=5, max_depth=4):
    """Simple beam search implementation for ToT."""
    # Start with the initial problem as the root
    frontier = [{"thought": "", "state": prompt, "value": 0.0}]

    for depth in range(max_depth):
        candidates = []

        # Generate k candidates from each frontier state
        for node in frontier:
            thoughts = generate_thoughts(model, node["state"], n=k)

            for thought in thoughts:
                new_state = node["state"] + "\n" + thought
                value = evaluate_state(model, new_state)
                candidates.append({
                    "thought": thought,
                    "state": new_state,
                    "value": value,
                    "parent": node
                })

        # Select top k by value
        candidates.sort(key=lambda x: x["value"], reverse=True)
        frontier = candidates[:k]

    # Return the best final state
    return max(frontier, key=lambda x: x["value"])
```

### Prompt Template for ToT

A typical ToT prompt structure:

```
You are solving a problem using tree search over reasoning steps.

Current state: {state description}

Generate 3 different approaches to continue from this state.
For each approach, evaluate whether it seems promising.

Approach 1: {description}
Evaluation: {promise score 1-10}

Approach 2: {description}
Evaluation: {promise score 1-10}

...
```

## Limitations

ToT is computationally expensive — generating and evaluating multiple branches per step means many more model calls than CoT. It's also more complex to implement correctly. The approach is most valuable when:

- The problem genuinely has multiple viable approaches
- Wrong paths are costly (you can't just try all of them linearly)
- Evaluation of intermediate states is tractable and reliable

For simple multi-step reasoning where any correct path works, CoT is faster and often sufficient.

## Relationship to Other Concepts

- [[Chain of Thought Prompting]] — ToT generalizes CoT from linear chains to branching trees
- [[LLM Reasoning]] — ToT is one of the most effective reasoning techniques for complex tasks
- [[Self-Improving AI]] — the self-evaluation step in ToT has parallels to self-improvement
- [[Prompting Techniques]] — ToT is a high-level prompting strategy combining several primitive techniques

## Further Reading

- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) — original paper by Yao et al. (2023)
- [ToT Prompt Engineering Guide (V7labs)](https://www.v7labs.com/blog/tree-of-thoughts-prompting) — practical implementation guide
- [Graph of Thoughts (GOT)](https://arxiv.org/abs/2308.09687) — extends ToT to arbitrary graph structures
