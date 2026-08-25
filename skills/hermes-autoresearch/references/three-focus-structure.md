# Three-Focus Autoresearch Structure

## Overview
Hermes Autoresearch uses a 3-focus structure:
1. Skills Improvement (primary, every night)
2. AI Agents Research
3. Hermes Agentic Features (em tự chọn)

## Why 3 Focuses?

### Focus 1: Skills Improvement
- Direct impact on Hermes performance
- Measurable (SHS metric)
- Quick wins possible each night
- Foundation for everything else

### Focus 2: AI Agents Research
- Keep Hermes current with landscape
- Discover new techniques
- Feed into Focus 3 improvements

### Focus 3: Hermes Agentic Features
- Long-term autonomy
- 16 capabilities to choose from
- Em tự quyết định based on context
- Creative, high-impact work

## Decision Framework (for Focus 3)

Each night, evaluate:
1. **What's blocking productivity?** — capability that would remove biggest obstacle
2. **What's feasible tonight?** — something achievable in 1 night
3. **What's foundational?** — capability that enables others

Then choose ONE and work on it until:
- Progress made (commit)
- Stuck (try different angle or switch)
- Time's up (report and continue next night)

## Git Workflow
```
~/.hermes/autoresearch/
├── program.md          ← What to do (human edits)
├── knowledge.md       ← What's been learned (agent updates)
├── DISCARDED.md       ← What failed (agent logs)
└── RESULTS.tsv        ← Metrics log
```

Branch per session: `autoresearch/YYYY-MM-DD`

## Report Cadence
- Every 30 min: progress to Telegram
- Format: brief, scannable, action-oriented
- Include: current focus, progress, blockers, next action
