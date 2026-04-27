---
title: "Hermes Self-Learning: P3.1 Config-driven Complexity Weights"
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [hermes-agent, self-learning, complexity-analysis, config-driven]
---

# Hermes Self-Learning: P3.1 Config-driven Complexity Weights

> Implementation of user-configurable complexity weights for task classification.

## Executive Summary

P3.1 enables users to override or extend default complexity keyword detection via `config.yaml`. The system now accepts custom keywords for HIGH/MEDIUM complexity classification, which are appended to (not replacing) the default keywords. All 22 tests pass.

## Implementation Details

### Config Schema

```yaml
self_learning:
  complexity_weights:
    high: [kubernetes, terraform, aws-ecs]
    medium: [docker-compose]
```

### Behavior
- **Append mode**: Custom keywords append to defaults, not replace
- **Default keywords preserved**: Keywords like "entire", "multiple" still work
- **Priority**: Config keywords take precedence for user-specific domains

### Complexity Levels

| Level | Detection | Override Support |
|-------|-----------|-----------------|
| LOW | Default simple task patterns | Via config |
| MEDIUM | Intermediate patterns + keywords | Via `medium:` |
| HIGH | Complex patterns + keywords | Via `high:` |

## System Components

### Agent Files

| File | Function |
|------|----------|
| `failure_classifier.py` | Extract failure reason (11 types) |
| `trajectory_index.py` | SQLite persistent storage + similarity search |
| `outcome_evaluator.py` | Close the learning loop |
| `pattern_matcher.py` | Match new task → past failures → warnings |
| `complexity_analyzer.py` | LOW/MEDIUM/HIGH detection |
| `proactive_planner.py` | Planning component |

### Key Interfaces

- `ProactivePlanResult` fields: `should_proceed, complexity, injected_context, planned_actions, recommendations, adjusted_iteration_budget, abort_reason`
- `injected_context` — prepends recommended_actions as context for agent
- `lifecycle:pre_execution` — status callback before task execution

## Related Topics

- [[Hermes Self-Learning System]]
- [[Complexity Analysis]]
- [[Hermes Agent]]

## References

- Git commit: `feat(self-learning): P3.1 config-driven complexity weights`
- Repo: https://github.com/tuananh4865/hermes-agent-self-learning
- Pending: P3.2 (User-facing feedback về learned lessons)
