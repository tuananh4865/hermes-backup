---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 wiki-self-evolution (extracted)
  - 🔗 wiki-self-heal (extracted)
  - 🔗 wiki-watchdog (extracted)
relationship_count: 3
---

# Wiki Self-Evolution Skill

> Agent behavior for running self-evolution cycles on the wiki.

## Trigger Conditions

- User asks to "self-evolve", "improve wiki", "fill gaps"
- Gap analysis finds missing topics
- Quality score drops below threshold
- New domain knowledge added that needs integration

## Behavior

### Step 1: Assess Current State
```
Run: wiki_gap_analyzer.py
Run: wiki_self_critique.py --all
Run: freshness_score.py --stale-only
```

### Step 2: Plan Improvements
- List gaps sorted by priority
- Identify low-quality pages
- Find stale content needing refresh
- Look for duplicate/merge candidates

### Step 3: Execute Improvements
```
For each gap:
  1. wiki_auto_improve.py --topic [topic]
  2. wiki_self_critique.py --page [new-page]
  3. Update index.md if new page
  4. Log action in log.md
```

### Step 4: Verify & Report
- Run wiki_lint.py to verify health
- Report changes to user
- Commit + push changes

## Output Format

```
## Self-Evolution Report

### Gaps Found
- [topic]: [reason]

### Improvements Made
- [page]: [change]

### Quality Impact
- Before: X/Y
- After: X/Y

### Wiki Health
- Stale: X → Y
- Quality avg: X → Y
```

## Integration

- Uses [[wiki-self-evolution]] concept page for background
- Coordinates with [[wiki-self-heal]] for broken links
- Triggered by [[wiki-watchdog]] on file changes
- Uses [[multi-agent-wiki]] for parallel gap analysis and content generation

> **Auto-improvement:** *Trigger conditions are vague** - "gap analysis finds missing topics" doesn't specify who runs what analysis. There's no clear entry point or mechanism for detection.

> **Auto-improvement:** Evolution" - a process for running self-improvement cycles on a wiki.

> **Auto-improvement:** *Trigger Conditions are vague**: The "gap analysis finds missing topics" doesn't specify who runs what analysis or when. There's no clear mechanism for detection.

> **Auto-improvement:** evolution - a process for a wiki agent to improve itself. Looking at the content and the auto-improvement notes at the bottom, I can identify a few key issues: