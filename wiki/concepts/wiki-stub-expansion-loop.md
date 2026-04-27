---
title: "Wiki Stub Expansion Loop"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: [wiki, autonomous, self-heal, stubs]
---

# Wiki Stub Expansion Loop — Operational Pattern

## The Problem

Self-heal creates MORE stubs from the new wikilinks in expanded pages:

```
expand 4 stubs → self-heal detects new broken links → creates 4 more stubs
→ expand those → self-heal creates 4 more → repeat...
```

**Stub ratio stays flat (~51-52%)** despite expansion work. Self-heal spawns stubs faster than expansion clears them.

## Observed (2026-04-21)

1. Expanded 2 pages from research (`apple-silicon-mlx-local-llm`, `vibe-coding-solo-developer`)
2. Self-heal created 4 new stubs: `bolt-new.md`, `v0-dev.md`, `privacy-first-ai.md`, `agents.md.md`, `memory.md.md`
3. Expanded those 3 substantive stubs (deleted `.md.md` artifacts)
4. Self-heal ran again → "No broken links found ✅"
5. But `git status` showed self-heal ALREADY created more stubs before the final heal
6. Stub count: **1538 → 1541** despite 6 pages expanded

## Root Cause

New concept pages contain wikilinks to other non-existent pages. Self-heal auto-creates stubs for every broken wikilink target. Expanding page A → creates stubs for B, C, D → those stubs have wikilinks too → self-heal creates more stubs...

## Effective Strategies

### Strategy A: Bulk Expand Then Heal (BEST)

1. Expand all target pages BEFORE any self-heal
2. Run ONE self-heal at the END
3. Commit everything together

This breaks the loop by creating all stubs in one batch, then healing once.

### Strategy B: Accept Slow Progress

- Focus on highest-value stubs (product/company names ≥500 words)
- Self-heal will always create stubs — expected behavior
- Net = expanded pages minus new stubs created
- ~6 expansions per cycle, ~5 stubs created → net ~1 page per cycle
- Slow but real progress over time

### Strategy C: Control Wikilinks First

- Before expanding, remove wikilinks to non-existent pages
- Only link to pages that already exist
- Prevents stub cascade at source

## Detection

```bash
# Stub ratio
python3 -c "
import os
stubs = sum(1 for root, dirs, files in os.walk('concepts')
    for f in files if f.endswith('.md')
    if '[TODO:' in open(os.path.join(root, f)).read())
total = sum(1 for root, dirs, files in os.walk('concepts')
    for f in files if f.endswith('.md'))
print(f'Stub ratio: {stubs/total*100:.1f}% | {stubs}/{total}')
"

# Check for new uncommitted stubs
cd ~/wiki && git status -s concepts/*.md
```

## Key Insight

**Stub ratio target (50%) is nearly impossible in active expansion mode** because self-heal is reactive — creates stubs FOR pages you create. Two ways to actually reduce ratio:
1. Bulk expand many pages (10+) in one pass, then heal once
2. Accept minimal net progress per cycle, play the long game

## Related

- [[wiki-self-heal]] — self-heal convergence behavior
- [[wiki-enhancement-roadmap]] — improvement priorities
