---
title: "Hermes Self-Learning"
created: 2026-04-18
updated: 2026-04-18
type: project
status: active
phase: core-complete
tags: [hermes-agent, self-learning, trajectory, complexity]
confidence: high
relationships:
  - hermes-dojo
  - agentic-self-evolving-system
---

# Hermes Self-Learning

**Status**: Active (Core Loop Complete)
**Started**: 2026-04-18
**Phase**: Core complete, ongoing improvements

## Mission

Self-learning system for Hermes Agent — learns from task outcomes, adjusts complexity dynamically, surfaces proactive suggestions.

## Core Features (All Implemented)

- ✅ `save_trajectories=True` — TrajectoryIndex + OutcomeEvaluator + ComplexityAnalyzer + PatternMatcher + ProactivePlanner
- ✅ Shared TrajectoryIndex instance across all components
- ✅ `OutcomeEvaluator.evaluate()` hook after task completion
- ✅ `ProactivePlanner.plan_ahead()` hook before task start
- ✅ Config-driven complexity weights
- ✅ User-facing lesson feedback via `get_recent_lessons()`
- ✅ Integration tests — 27 tests, all passing

## Current Issues

See `hermes-self-learning/limitations-2026-04-18.md` for current limitations being addressed.

## Next Action

Review limitations doc for P4+ priorities.
