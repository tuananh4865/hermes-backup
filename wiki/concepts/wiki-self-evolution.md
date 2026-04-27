---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 self-healing-wiki (extracted)
  - 🔗 skills/wiki-watchdog (extracted)
  - 🔗 skills/multi-agent-wiki (extracted)
relationship_count: 3
---

# Wiki Self-Evolution

> Autonomous agent that continuously improves the wiki by identifying gaps, generating content, and self-critiquing quality.

## Overview

Self-evolution is the wiki's ability to **identify what it doesn't know** and **主动 fill those gaps** without human prompting.

## Pipeline

```
OBSERVE → PLAN → ACT → LEARN → REFLECT
```

## Components

### Gap Analyzer (`wiki_gap_analyzer.py`)
Finds missing topics by:
- Analyzing existing page clusters
- Identifying adjacent concepts that should exist
- Comparing to external knowledge sources

### Auto-Improve (`wiki_auto_improve.py`)
Generates new content for gaps:
- Creates new concept pages
- Expands existing thin pages
- Fills missing cross-references

### Self-Critique (`wiki_self_critique.py`)
Scores page quality 1-10:
- Comprehensiveness
- Accuracy
- Structure
- Wikilinks
- Freshness

### Freshness Score (`freshness_score.py`)
Detects stale content:
- No updates > 30 days = stale
- No wikilinks = orphan candidate
- Template placeholder = incomplete

### Duplicate Detector (`duplicate_detector.py`)
Finds merge candidates:
- Similar titles
- Circular links
- Overlapping content

## Usage

```bash
# Full self-evolution cycle
python3 scripts/wiki_self_evolution_agent.py --full-cycle

# Individual components
python3 scripts/wiki_gap_analyzer.py
python3 scripts/wiki_auto_improve.py
python3 scripts/wiki_self_critique.py --all
python3 scripts/freshness_score.py --stale-only
```

## Integration

Self-evolution runs:
1. **On-demand**: When agent detects gaps during conversation
2. **Scheduled**: Via watchdog trigger on file changes
3. **Manual**: User requests self-evolution cycle

## Related

- [[self-healing-wiki]] — Broken link and quality fixes
- [[wiki-watchdog]] — Event-driven triggers
- [[multi-agent-wiki]] — Cross-agent coordination
