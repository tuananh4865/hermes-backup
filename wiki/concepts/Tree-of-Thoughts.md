---
title: "Tree of Thoughts (ToT)"
description: "Tree of Thoughts prompting enables LLMs to explore multiple reasoning paths as a branching tree, evaluating intermediate steps and backtracking when needed — dramatically outperforming chain-of-thought on complex problem-solving tasks."
tags: [prompting, reasoning, LLM, problem-solving, chain-of-thought, inference]
created: 2026-04-12
updated: 2026-04-20
type: concept
sources:
  - https://arxiv.org/abs/2305.10601
  - https://www.v7labs.com/blog/tree-of-thoughts-prompting
  - https://www.geeksforgeeks.org/tree-of-thought-reasoning
related:
  - [[chain-of-thought-prompting]]
  - [[llm-reasoning]]
  - [[self-improving-ai]]
  - [[reasoning-patterns]]
  - [[agent-planning]]
---

# Tree of Thoughts (ToT)

Tree of Thoughts (ToT) is a prompting framework that treats LLM reasoning as **deliberate search over a tree of possibilities**, rather than a single linear chain. Unlike [[chain-of-thought-prompting]] which produces one reasoning path, ToT generates multiple branching paths, evaluates each as it goes, and backtracks when a branch appears unproductive.

## The Core Idea

Standard chain-of-thought:
```
Input → Step 1 → Step 2 → Step 3 → Answer
```

Tree of Thoughts:
```
         Input
       /      \
   Branch A   Branch B
   /    \     /    \
 A1     A2   B1     B2
  \     /     \     /
   \   /       \   /
   Evaluate    Evaluate
      \         /
       \       /
      Best Path → Answer
```

The LLM acts as both **generator** (proposing next steps) and **evaluator** (judging whether a partial solution looks promising), enabling genuine search rather than just sequential inference.

## Why It Outperforms Chain-of-Thought

Chain-of-thought works well for problems where the correct path is obvious. But for problems requiring **non-trivial planning**, **creative decomposition**, or **trial-and-error**, the first path chosen is often wrong, and CoT has no mechanism to recover.

ToT solves this by:

1. **Parallel exploration** — multiple paths explored simultaneously
2. **Mid-course correction** — evaluate at intermediate steps, not just the final answer
3. **Pruning** — abandon low-value branches early
4. **Lookahead** — evaluate not just current state but potential future states

## The Algorithm

For any problem, ToT follows this pattern:

```
1. DECOMPOSE — Break the problem into discrete "thought steps"
2. GENERATE — For the current state, generate k candidate next steps
3. EVALUATE — For each candidate, use the LLM to assess:
   "Does this partial solution look promising? Rate 1-10 and explain."
4. PRUNE — Discard candidates below a threshold
5. CHECK — If a candidate solves the problem, return it
6. RECURSE — Continue with remaining candidates
```

## When to Use ToT vs. CoT

| Scenario | Best Approach |
|----------|---------------|
| Math word problems with one clear path | Chain-of-thought |
| Strategic planning (24-game, creative writing) | Tree of Thoughts |
| Code debugging with multiple possible fixes | Tree of Thoughts |
| Fact extraction from text | Direct prompting |
| Any problem where your first guess is often wrong | Tree of Thoughts |

## Research Findings

The original paper (Yao et al., 2023, arXiv:2305.10601) showed ToT dramatically outperforms CoT on:
- **Game of 24**: 74% vs 4% success rate
- **Creative writing**: significantly higher quality outputs
- **Mini crossword puzzles**: substantial improvement over CoT

The key insight: for problems requiring **non-monotonic reasoning** (where you might need to backtrack), tree search over thought space is essential.

## Related Concepts

- [[chain-of-thought-prompting]] — single-chain reasoning (ToT's simpler alternative)
- [[llm-reasoning]] — broader category of how LLMs reason
- [[self-improving-ai]] — agents that evaluate and improve their own outputs
- [[reasoning-patterns]] — patterns like ToT, ReAct, Reflexion
- [[agent-planning]] — how agents plan multi-step tasks
