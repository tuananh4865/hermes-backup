---
confidence: high
last_verified: 2026-04-16
type: concept
tags: [reasoning, llm, patterns, chain-of-thought]
related:
  - [[agent-planning-reasoning]]
  - [[agentic-ai]]
  - [[agent-memory-architecture]]
sources:
  - arXiv 2310.00194v4: Modular Agentic Planner (MAP)
  - Nature 2026: Brain-inspired agentic architecture
  - arXiv 2602.22769v1: AMA-Bench memory evaluation
---

# Reasoning Patterns

## Overview

Reasoning patterns are structured approaches that enable LLMs to solve complex problems by breaking them down into logical steps. In 2026, these patterns became fundamental to agentic AI systems.

## Core Patterns

### Chain-of-Thought (CoT)
Encourages step-by-step reasoning before answering.

**Example:**
```
Problem: If all roses are flowers and some flowers fade quickly, what can we conclude?
Reasoning: 
1. All roses = flowers (subset)
2. Some flowers fade quickly
3. Roses could be among those that fade quickly
Conclusion: Some roses may fade quickly (not certain, but possible)
```

**When to use:** Math problems, logical deduction, multi-step calculations.

### Self-Consistency
Generate multiple reasoning paths, take majority vote.

**Approach:**
1. Generate N different reasoning paths
2. Each path produces an answer
3. Select most common answer

**When to use:** Complex reasoning where multiple valid approaches exist.

### Tree of Thoughts (ToT)
Explore multiple reasoning branches simultaneously.

**Structure:**
```
                    Problem
                   /   |   \
              Branch A Branch B Branch C
                 |       |       |
            Expand    Expand    Prune
                 \       |       /
                  \      |      /
                 Best Path Selected
```

**When to use:** Creative tasks, strategic planning, scenarios with multiple valid solutions.

### ReAct (Reasoning + Acting)
Combines reasoning traces with action execution.

**Loop:**
1. Think: Reason about current state
2. Act: Take an action
3. Observe: Note the result
4. Repeat until goal achieved

**When to use:** Agent tasks requiring tool use, web browsing, multi-step workflows.

### Plan-then-Execute
Decompose task into plan, then execute steps.

**Sequence:**
1. **Plan:** Break down into subtasks
2. **Execute:** Complete each subtask
3. **Monitor:** Check for plan deviations
4. **Adapt:** Modify plan if needed

**When to use:** Long-horizon tasks, project management, complex builds.

## Advanced Patterns

### Reflexion
Self-reflection after task completion to improve future performance.

**Process:**
1. Attempt task
2. Evaluate outcome
3. Reflect on what went wrong
4. Update strategy

### Modular Agentic Planner (MAP)
Published in Nature 2026: Brain-inspired architecture for planning.

**Key insight:** Planning via recurrent interaction between specialized modules (inspired by prefrontal cortex).

**Components:**
- Working memory module
- Planning module
- Execution module
- Reflection module

### Continuous Memory Architecture (CMA)
Formalized in arXiv 2601.09913v1 for persistent memory in LLM agents.

**Properties:**
- Long-term context retention
- Selective memory retrieval
- Temporal grounding

## Implementation Patterns

### Prompt Engineering
```markdown
Let's think step by step about this problem.
1. First, I need to understand...
2. Next, I should consider...
3. Therefore, the best approach is...
```

### Code Implementation
```python
class ReActAgent:
    def think(self, state):
        # Reasoning about current state
        return reasoning
        
    def act(self, reasoning):
        # Take action based on reasoning
        return action_result
        
    def observe(self, result):
        # Update state with observation
        pass
```

## Choosing a Pattern

| Task Type | Best Pattern |
|-----------|-------------|
| Math/Logic | Chain-of-Thought |
| Creative | Tree of Thoughts |
| Agent Tasks | ReAct |
| Long-horizon | Plan-then-Execute |
| Self-improvement | Reflexion |
| Complex Planning | MAP (Modular Agentic Planner) |

## Related Concepts

- [[agent-planning-reasoning]]
- [[agentic-ai]]
- [[agent-memory-architecture]]
- [[multi-agent-systems]]
