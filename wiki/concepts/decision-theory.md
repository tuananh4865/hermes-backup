---
title: Decision Theory
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [decision-theory, reasoning, ai, probability, game-theory, rational-agent]
---

# Decision Theory

## Overview

Decision theory is the formal study of how rational agents make choices under uncertainty. It provides mathematical frameworks for representing decision problems, evaluating outcomes, and determining optimal actions. As a discipline, it bridges economics, philosophy, statistics, and computer science—offering the theoretical foundation for AI agent planning, reinforcement learning, and autonomous systems.

The core insight of decision theory is that choices should be made by comparing the expected values of outcomes, weighted by their probabilities and the agent's preferences (utility). This framework allows precise reasoning about trade-offs, risk, and information value.

## Key Concepts

**Rational Agent**: An entity that systematically chooses actions maximizing its expected utility given its beliefs about the world. Rationality doesn't imply perfection—it acknowledges uncertainty and resource limitations.

**Utility Function**: A mathematical mapping from outcomes to real numbers representing preferences. A rational agent's utility function captures what it values and in what proportions.

**Expected Utility**: The weighted average of utility across possible outcomes, where weights are outcome probabilities. The foundational principle: choose the action with highest expected utility.

```python
# Decision-theoretic action selection
from dataclasses import dataclass
from typing import Callable

@dataclass
class Action:
    name: str
    outcomes: dict[str, float]  # probability distribution over outcomes
    utility: Callable[[str], float]

def expected_utility(action: Action) -> float:
    """Calculate expected utility of an action"""
    return sum(
        prob * action.utility(outcome)
        for outcome, prob in action.outcomes.items()
    )

def select_best_action(actions: list[Action]) -> Action:
    """Choose action with highest expected utility"""
    return max(actions, key=expected_utility)

# Example usage
buy_stock = Action(
    name="Buy Stock",
    outcomes={"rise": 0.6, "fall": 0.4},
    utility=lambda o: 1000 if o == "rise" else -500
)

hold = Action(
    name="Hold",
    outcomes={"rise": 0.6, "fall": 0.4},
    utility=lambda o: 0
)

best = select_best_action([buy_stock, hold])
print(f"Optimal action: {best.name}")  # Output: Optimal action: Buy Stock
```

**Risk and Uncertainty**: Decisions under risk have known probability distributions; decisions under uncertainty have unknown distributions. Distinguishing these matters for appropriate reasoning methods.

**Information Value**: The value of perfect information is the difference between expected utility with the information versus without. This quantifies how much acquiring more information is worth.

## How It Works

Decision theory provides several frameworks:

1. **Normative Theory**: How rational agents *should* decide (prescriptive)
2. **Descriptive Theory**: How humans *actually* decide (often deviates from rationality)
3. **Prescriptive Theory**: Practical tools for improving decision-making

**Decision Trees**: Graphical representations showing decision points, chance events, and outcomes:
```
        [Invest?]
           |
    +-----+-----+
    |           |
  Yes          No
    |           |
 [Market]    [Safe]
  60%/40%    100%
 +/-20%     +5%
```

**Bayesian Updating**: Combining prior beliefs with new evidence to form updated beliefs, essential for sequential decision-making under uncertainty.

## Practical Applications

- **AI Agent Planning**: Decision theory underpins reinforcement learning and Markov Decision Processes (MDPs)
- **Autonomous Vehicles**: Reasoning about navigation decisions under uncertainty
- **Medical Diagnosis**: Choosing treatments based on probability-weighted outcomes
- **Financial Portfolio**: Optimizing asset allocation under risk
- **Game Theory**: Strategic decision-making in multi-agent scenarios

## Examples

**Multi-Armed Bandit Problem**:
```python
import random

class BanditSolver:
    """Thompson sampling for multi-armed bandit"""
    def __init__(self, arms: int):
        self.successes = [1] * arms  # Beta prior alpha
        self.failures = [1] * arms   # Beta prior beta
    
    def select_arm(self) -> int:
        """Sample from posterior and select best"""
        samples = [
            random.betavariate(self.successes[i], self.failures[i])
            for i in range(len(self.successes))
        ]
        return samples.index(max(samples))
    
    def update(self, arm: int, reward: int):
        """Update posterior with observed reward"""
        if reward:
            self.successes[arm] += 1
        else:
            self.failures[arm] += 1
```

## Related Concepts

- [[reasoning]] — AI reasoning systems
- [[cognitive-biases]] — Systematic human reasoning deviations
- [[game-theory]] — Strategic decision-making in multi-agent settings
- [[reinforcement-learning]] — Learning from reward signals
- [[probability]] — Mathematical framework for uncertainty
- [[bayesian-inference]] — Updating beliefs with evidence

## Further Reading

- Pearl "Probabilistic Reasoning in Intelligent Systems"
- Russell & Norvig "Artificial Intelligence: A Modern Approach" (Decision Theory chapters)

## Personal Notes

Decision theory reveals how much of "common sense" can be formalized. Yet humans systematically violate its predictions—we overweight small probabilities, anchor on irrelevant information, and let emotions distort utility assessments. AI systems designed with decision theory can avoid these biases, but translating real-world preferences into utility functions remains challenging.
