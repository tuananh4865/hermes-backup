---
title: HyperAgents
description: Self-referential AI agents that can modify their own code and prompts
tags: [ai, agents, self-improvement, autonomous-ai]
---

# HyperAgents

HyperAgents are a class of self-improving AI agents that can modify their own code, prompts, and behavior through self-referential loops — essentially improving their own architecture based on performance feedback.

## Overview

HyperAgents extend Constitutional AI principles to the realm of autonomous code modification. Rather than relying on external human feedback, HyperAgents continuously evaluate their own performance and implement improvements.

## How They Work

1. **Self-Critique**: Agent evaluates its own outputs against defined objectives
2. **Modification Planning**: Identifies specific aspects to improve
3. **Self-Modification**: Updates prompts, code, or internal state
4. **Verification**: Tests modifications don't degrade performance
5. **Loop**: Repeats continuously

## Safety Considerations

The self-modification capability raises significant safety questions. HyperAgents implementations typically include:

- Constitutional constraints on what can be modified
- Sandboxed execution environments
- Human oversight checkpoints
- Rollback capabilities if modifications cause degradation

## Related

- [[self-improving-ai]]
- [[autonomous-agents]]
- [[ai-safety]]
- [[constitutional-ai]]
