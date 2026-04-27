---
title: "Reinforcement Learning"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, reinforcement-learning, sequential-decision-making, ai, deep-learning]
---

# Reinforcement Learning

## Overview

Reinforcement learning (RL) is a paradigm of machine learning where an agent learns to make decisions by interacting with an environment. The agent takes actions, receives scalar reward signals, and updates its decision-making policy based on the cumulative feedback it receives. Unlike supervised learning, where explicit label pairs (input, correct output) are provided, RL relies on a reward signal that may be sparse, delayed, and confounded by the agent's own past actions. This creates fundamental challenges around credit assignment—determining which past actions were responsible for current rewards.

RL is the approach behind many of the most impressive AI achievements of the last decade, including game-playing systems like AlphaGo and Atari-playing agents, robotics control policies, and increasingly, large language model alignment via techniques like RLHF (Reinforcement Learning from Human Feedback).

## Key Concepts

**The Agent-Environment Loop**: At each timestep, the agent observes a state $s_t$, takes an action $a_t$, receives a reward $r_t$, and transitions to a new state $s_{t+1}$. This interaction continues until a terminal state is reached or the episode ends. The agent's goal is to learn a policy $\pi(a|s)$ that maximizes expected cumulative return.

**Rewards vs Returns**: The reward is a immediate scalar signal, but the return is the cumulative sum of rewards, typically discounted: $G_t = r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + \dots$ where $\gamma \in [0,1]$ is the discount factor. The discount factor controls how far-sighted the agent is.

**Value Functions** estimate how good a state (or state-action pair) is in terms of expected future return. The state-value function $V^\pi(s) = \mathbb{E}_\pi[G_t | s_t = s]$ estimates expected return from state $s$ following policy $\pi$. The action-value function $Q^\pi(s,a) = \mathbb{E}_\pi[G_t | s_t=s, a_t=a]$ estimates expected return after taking action $a$ from state $s$.

**The Bellman Equations** express the recursive nature of value functions: $V^\pi(s) = \sum_a \pi(a|s) \sum_{s',r} p(s',r|s,a)[r + \gamma V^\pi(s')]$. These equations are the foundation of most RL algorithms.

## How It Works

RL algorithms can be broadly categorized by how they approach learning:

**Value-Based Methods** learn approximate value functions and derive policies from them. Q-Learning learns the optimal action-value function $Q^*$ directly. Deep Q-Networks (DQN) scale this to high-dimensional state spaces by using neural networks to approximate $Q(s,a)$. DQN introduces experience replay (storing transitions and sampling randomly for updates) and target networks (stabilizing training by using a slowly-updated network for targets).

**Policy Gradient Methods** directly optimize the policy parameters by computing estimates of the policy gradient. REINFORCE provides an unbiased Monte Carlo estimate. Proximal Policy Optimization (PPO) constrains policy updates to improve sample efficiency and training stability. Actor-Critic methods combine value function approximation (the critic) with policy optimization (the actor).

**Model-Based RL** learns a model of the environment dynamics $p(s'|s,a)$ and plans using the learned model. This can dramatically improve sample efficiency but requires the model to be sufficiently accurate.

## Practical Applications

- **Game Playing**: AlphaGo, AlphaZero, and Atari game-playing agents have achieved superhuman performance
- **Robotics**: Training manipulation policies, locomotion controllers, and autonomous navigation
- **Recommendation Systems**: Optimizing user engagement over sequences of recommendations
- **Large Language Model Alignment**: RLHF and GRPO techniques align language models with human preferences
- **Autonomous Driving**: Decision-making and control in dynamic traffic environments
- **Drug Discovery**: Optimizing molecular properties through experimental feedback loops

## Examples

```python
# Q-Learning table-based example
import numpy as np

# Simple FrozenLake environment (4x4 grid)
n_states = 16
n_actions = 4  # up, down, left, right
q_table = np.zeros((n_states, n_actions))

# Hyperparameters
alpha = 0.1      # learning rate
gamma = 0.99     # discount factor
epsilon = 0.1    # exploration rate

# Epsilon-greedy action selection
def choose_action(state):
    if np.random.random() < epsilon:
        return np.random.randint(n_actions)
    return np.argmax(q_table[state])

# Update rule (simplified Q-learning)
def update(state, action, reward, next_state):
    best_next = np.max(q_table[next_state])
    q_table[state, action] += alpha * (reward + gamma * best_next - q_table[state, action])

# Training loop would iterate over episodes
print("Q-table after initialization:")
print(q_table)
```

## Related Concepts

- [[Machine Learning]] — the broader discipline
- [[Deep Learning]] — neural network approaches that power modern RL
- [[Supervised Learning]] — often used to pre-train components of RL systems
- [[Self-Supervised Learning]] — techniques used in model-based RL
- [[RLHF (Reinforcement Learning from Human Feedback)]] — applying RL to LLM alignment

## Further Reading

- "Reinforcement Learning: An Introduction" by Sutton and Barto — the definitive textbook
- OpenAI Spinning Up — accessible tutorials on RL algorithms
- "Deep Reinforcement Learning Hands-On" by Maxim Lapan

## Personal Notes

The exploration-exploitation trade-off is one of the most fundamental tensions in RL. Epsilon-greedy is simple but naive; more sophisticated methods like UCB or curiosity-driven exploration perform better in complex environments. The credit assignment problem becomes especially severe in long-horizon tasks, which is why reward shaping and hierarchical RL are active research areas.
