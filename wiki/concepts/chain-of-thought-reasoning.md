---
title: "Chain Of Thought Reasoning"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags:
  - reasoning
  - llm
  - prompt-engineering
  - cognition
---

## Overview

Chain of Thought (CoT) reasoning is a prompting technique that enhances large language model performance by encouraging explicit intermediate reasoning steps before arriving at a final answer. Rather than demanding immediate responses, CoT prompting guides models to articulate their logical progression, breaking complex problems into manageable sequential steps. This approach emerged from research showing that standard prompting often underperformed on tasks requiring multi-step deduction, arithmetic, or commonsense reasoning. By making the reasoning process visible and structured, CoT enables models to handle significantly more complex tasks than their raw capabilities would suggest, effectively unlocking latent problem-solving abilities that remain dormant under direct answer formats.

## Key Concepts

The foundation of Chain of Thought reasoning rests on several interconnected principles. **Intermediate steps** serve as cognitive scaffolding, allowing models to store partial results and maintain context across lengthy derivations. **Explicit reasoning** forces the model to externalize its internal logic, which paradoxically improves accuracy because the act of articulating reasoning often reveals errors or inconsistencies that would otherwise remain hidden. **Step-by-step decomposition** transforms intractable problems into sequences of simpler sub-problems, each of which the model can reliably solve. The technique also leverages what researchers call "reasoning as computation"—treating the forward pass of the model as a form of dynamic problem-solving rather than simple pattern matching.

The effectiveness of CoT scales with model size, with larger models benefiting more dramatically from the technique. This observation suggests that smaller models may lack the representational capacity to benefit from extended reasoning chains, possibly because they cannot reliably maintain coherent logical states across multiple inference steps. Additionally, CoT works best when the reasoning steps are natural language descriptions of actual logical operations, not just decorative commentary. The technique is closely related to program synthesis, as good chain-of-thought prompts effectively teach the model to "program itself" through language.

## How It Works

In practice, CoT prompting typically involves providing a few examples that demonstrate the reasoning format, where each example shows the problem, the step-by-step solution, and the final answer. This few-shot approach establishes a template that the model applies to new problems. For example, a CoT prompt for a math problem would show: "First, I need to find the total number of items. The problem states there are 5 boxes with 12 items each, so 5 × 12 = 60 items. Then I subtract the 8 items removed, giving 60 - 8 = 52 items remaining."

More advanced implementations include **self-consistency sampling**, where multiple reasoning chains are generated and the most common final answer is selected. Another variant, **Tree of Thoughts**, explores branching reasoning paths and evaluates their promise before committing to a direction. Some systems incorporate **planning prompts** that ask the model to first outline its approach before executing each step, creating a two-level reasoning hierarchy.

The computational mechanism underlying CoT involves the model's attention mechanism maintaining activation patterns across tokens that represent logical state. Each reasoning step modifies this state, and the final answer emerges from the accumulated reasoning rather than being retrieved directly from training data.

## Practical Applications

Chain of Thought reasoning has become essential in several domains where precision matters. **Mathematical problem solving** was the original motivation—models that cannot reliably carry digits when performing long multiplication can still succeed with CoT by breaking the operation into single-digit multiplications and careful addition. **Code debugging and generation** benefits from CoT because explaining why code fails requires tracking state across execution steps. **Complex QA tasks** that involve multi-hop reasoning—connecting disparate facts to reach a conclusion—show dramatic improvements with CoT prompting.

In **autonomous agents**, CoT serves as an internal monologue mechanism, allowing agents to plan actions before executing them. This is particularly valuable when agents operate in environments where mistakes are costly or irreversible. The technique also enables better human oversight, as observing an agent's reasoning chain makes it easier to identify where it went wrong or to correct its approach before it commits to a bad plan.

**Scientific reasoning** applications use CoT to work through hypotheses, experimental design, and data interpretation. Models guided through step-by-step analysis of experimental results can draw more nuanced conclusions than those asked to summarize findings directly.

## Examples

A classic example involves solving a word problem:

```
Problem: If a train leaves station A at 9:00 AM traveling 60 mph, and another
train leaves station B (200 miles away) at 9:30 AM traveling 80 mph, when
will they meet?

Chain of Thought:
1. Train A has a 30-minute head start (0.5 hours)
2. Distance covered by Train A in that time: 60 × 0.5 = 30 miles
3. Remaining distance between trains: 200 - 30 = 170 miles
4. Combined closing speed: 60 + 80 = 140 mph
5. Time to meet after Train B starts: 170 / 140 ≈ 1.21 hours
6. Time from Train B start: 1.21 hours ≈ 1 hour 13 minutes
7. Meeting time: 9:30 AM + 1:13 = 10:43 AM

Answer: They will meet at approximately 10:43 AM.
```

Another example from debugging:

```
Problem: This function should return the index of the first even number,
but it returns -1 even when even numbers exist.

Chain of Thought:
1. The function iterates through the array correctly
2. The condition checks `num % 2 == 0` which should identify even numbers
3. The return statement is inside the loop, so it should return immediately
4. Wait—checking the indentation, the return is INSIDE an inner if block
5. The outer if checks `num > 0`, which filters out negative even numbers
6. But the test case has [-2, -1, 3] and -2 is even but also negative
7. The bug is the `num > 0` condition filtering valid candidates
```

## Related Concepts

- [[Tree of Thoughts]] - An extension that explores branching reasoning paths
- [[Prompt Engineering]] - The broader discipline of crafting effective prompts
- [[Large Language Models]] - The underlying technology that CoT enhances
- [[Self-Consistency]] - A technique sampling multiple CoT paths for robust answers
- [[ReAct Reasoning]] - Combining reasoning with action-taking in agents

## Further Reading

- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022) - The seminal paper introducing CoT
- "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" - Extension to branched reasoning
- "Self-Consistency Improves Chain of Thought Reasoning in Language Models" - Enhanced CoT through sampling
- Anthropic's research on reasoning with language models

## Personal Notes

CoT represents a fundamental shift in how we think about LLM capabilities—the same model can appear dramatically more or less capable depending on how we prompt it. I've found CoT especially valuable when building agents that need to justify their decisions to users. The technique does have costs: longer outputs mean higher token usage and slower response times. For simple factual queries, standard prompting is more efficient. But for complex reasoning tasks, the investment in CoT almost always pays off in accuracy.
