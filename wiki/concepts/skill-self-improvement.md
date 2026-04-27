---
created: 2026-04-15
tags: [self-improvement, skill-retrieval, autonomous, garry-tan]
related:
  - skill-recommend
  - skill-indexer
  - autonomous-wiki-agent
---

# Skill Self-Improvement System

Garry Tan's insight: *"The bottleneck is never the model's intelligence — it's whether the right skill is loaded at the right time."* and *"The system will improve itself as skills compound."*

## Architecture

```
Task arrives
    ↓
skill_recommend(task)
    ↓  [logs to _usage_log.jsonl]
Every recommendation is recorded
    ↓
skill_insight_analyzer (daily cron, 7AM)
    ↓
auto_skill_patch (dry-run, reports)
    ↓
Trigger conditions sharpened
    ↓
Next day: better recommendations
    ↓
Usage compounds → system improves itself
```

## Components

### 1. skill_recommend — Usage Logger
- **Location**: `~/.hermes/hermes-agent/tools/skill_recommend.py`
- **Auto-logs**: task, recommended skills (top-5), selected skill, outcome, session_id
- **Log file**: `~/.hermes/skills/_usage_log.jsonl`

### 2. skill_insight_analyzer — Insight Engine
- **Location**: `/Volumes/Storage-1/Hermes/scripts/skill_insight_analyzer.py`
- **Run**: `python3 ~/.hermes/scripts/skill_insight_analyzer.py`
- **Finds**:
  - Missing skills (tasks with no good match)
  - Weak trigger_conditions (recommended >3x, selected <15%)
  - Low-success skills (selected but <40% success rate)
  - Over-recommended skills (too broad)
  - Workflow patterns (repeated tasks)
  - Trigger gap suggestions

### 3. auto_skill_patch — Safe Auto-Tuner
- **Location**: `/Volumes/Storage-1/Hermes/scripts/auto_skill_patch.py`
- **Safe auto-patches** (no approval): trigger_conditions additions
- **Asks first**: new skills, deletion, body rewrites
- **Dry-run**: `python3 ~/.hermes/scripts/auto_skill_patch.py --dry-run`
- **Apply**: `python3 ~/.hermes/scripts/auto_skill_patch.py --apply`

### 4. Cron Job — Morning Health Check
- **Schedule**: Daily 7:00 AM
- **Job ID**: `e2491f94fdf4`
- **Delivers**: Telegram summary of skill health metrics

## Self-Improvement Loop

The loop is **autonomous** — it runs every morning and continuously improves:

1. **Log** — Every `skill_recommend()` call is recorded
2. **Analyze** — Daily cron runs `skill_insight_analyzer`
3. **Detect** — Weak triggers identified automatically
4. **Patch** — `auto_skill_patch` sharpens trigger_conditions
5. **Compound** — Next day's recommendations are more accurate

Over time, the skill retrieval system learns which skills work for which tasks.

## Key Metrics

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Match rate | > 80% | 50-80% | < 50% |
| Unique skills used | > 10 | 5-10 | < 5 |
| Missing skill tasks | < 10% | 10-30% | > 30% |

## Example

```
Day 1: "build CI/CD pipeline for iOS" → no good match
  → logged as missing_skill

Day 2: "setup iOS CI/CD" → still no match
  → pattern detected: "ci", "cd", "ios", "pipeline"

Day 7: analyzer finds 3 similar missing tasks
  → suggests: "ci/cd", "pipeline", "ios deployment" as triggers
  → auto_skill_patch adds to relevant skills

Day 8: "iOS CI/CD setup" → matches iOS dev skill correctly
```

## Philosophy

**Thin harness, fat skills.** The core retrieval code stays minimal. All the knowledge lives in skill metadata (trigger_conditions, use_case_keywords, tags). As skills compound, the system gets smarter without changing the core.

This is how a wiki becomes an "intelligent agent" — not through smarter models, but through accumulated procedural knowledge that auto-tunes itself.
