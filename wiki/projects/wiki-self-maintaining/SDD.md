---
title: "SDD: Wiki Proactive Self-Maintaining System"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [auto-filled]
---

# SDD: Wiki Proactive Self-Maintaining System

**Confidence**: 8.5/10
**Date**: 2026-04-12
**Author**: Hermes Agent (based on deep research + analysis)

---

## Executive Summary

Nâng cấp wiki từ passive knowledge storage thành **proactive, self-maintaining memory system** cho LLM agent. Mô hình: wiki = external memory harness (theo Harrison Chase), kết hợp Karpathy's LLM Wiki 4-phase cycle + self-improvement loop.

---

## Research Findings

### What Harrison Chase's "Your Harness, Your Memory" Validates

1. **Wiki = Harness = Memory** — Our wiki IS the agent's harness. Memory = form of context. Short-term (conversation) + Long-term (wiki).
2. **Memory Ownership Matters** — Proprietary memory = competitive moat. We own our wiki, not third-party.
3. **Closed System = Lock-in** — Using Claude Agent SDK = memory lives on Anthropic's servers. We avoid this.

### What Karpathy's Model Is Missing

Karpathy describes 4-phase cycle (Ingest → Compile → Lint → Query) nhưng **chưa có self-triggered loop**. Wiki vẫn passive — chờ human feed sources.

### Key Gap: Proactive Loop

Current: Human feeds → LLM compiles → done
Target: LLM **主动** reads sources, identifies gaps, compiles pages, maintains relationships, self-critiques, improves.

---

## Solution Architecture

### 1. Formal 4-Phase Cycle (Karpathy)

```
┌─────────────────────────────────────────────────────┐
│                  AUTONOMOUS LOOP                     │
│                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  INGEST  │ →  │ COMPILE  │ →  │  LINT    │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│       ↑                                   │          │
│       └────────────── QUERY ◄────────────┘          │
│                                                      │
│  Continuous cycle: Gap Detection → Action → Review   │
└─────────────────────────────────────────────────────┘
```

### Phase 1: INGEST
- **Sources**: RSS feeds, emails, transcripts, web articles
- **Trigger**: Cron (9PM daily) + watchdog on new raw files
- **Scripts**: `ingest_rss.py`, `email_ingest.py`, `transcript_handler.py`

### Phase 2: COMPILE
- **Raw → Synthesized**: Transform sources into concept/entity pages
- **Gap Detection**: `wiki_gap_analyzer.py` finds topics mentioned but not documented
- **Script**: `wiki_auto_improve.py` generates new content

### Phase 3: LINT (Self-Healing)
- **Broken links**: `wiki_lint.py --fix`
- **Missing frontmatter**: `wiki_self_heal.py --frontmatter`
- **Quality scoring**: `wiki_self_critique.py --all`
- **Freshness**: `freshness_score.py --stale-only`

### Phase 4: QUERY
- **Passive**: LLM reads wiki as context for tasks
- **Active**: `semantic_search.py` + `ask_wiki.py` for explicit queries

---

## Implementation Plan

### Phase A: Fix & Verify Existing Scripts

**Verify functional:**
- [ ] `wiki_lint.py` — test on current wiki
- [ ] `wiki_self_heal.py` — verify auto-fix works
- [ ] `wiki_self_critique.py` — verify scoring
- [ ] `wiki_gap_analyzer.py` — verify gap detection
- [ ] `semantic_search.py` — verify search works

**Missing scripts to create:**
- [ ] `topic_workflow.py` — orchestrates raw → concept pipeline (CRITICAL GAP)
- [ ] `cron_watchdog.py` — monitors raw/ and triggers processing

### Phase B: Cron Schedule Setup

| Time | Task | Script |
|------|------|--------|
| 7:30 AM | Morning research + plan | `autonomous_deep_research.py` |
| 9:00 PM | Daily ingest | `cron_daily_ingest.py` |
| 3:00 AM | Wiki self-heal | `wiki_self_heal.py --fix --all` |
| Mon 2 AM | Weekly health | `wiki_lint.py` + `wiki_self_critique.py` |

### Phase C: Self-Improvement Loop

**Gap → Action → Review cycle:**
1. `task_checker.py` — scans for gaps, stale pages, broken links
2. `wiki_auto_improve.py` — generates content for gaps
3. `wiki_self_critique.py` — scores new content
4. If quality < threshold → regenerate or flag for human

### Phase D: Hermes Dojo Integration

`hermes_dojo.py` already exists — tracks agent improvements. Integrate with wiki self-evolution:
- Log every wiki improvement
- Track quality metrics over time
- Identify patterns in what needs fixing

---

## Scripts Status

### Existing & Functional ✓
| Script | Purpose | Status |
|--------|---------|--------|
| `wiki_lint.py` | Health check | ✓ Need verify |
| `wiki_self_heal.py` | Auto-fix | ✓ Need verify |
| `wiki_self_critique.py` | Quality scoring | ✓ Need verify |
| `wiki_gap_analyzer.py` | Find gaps | ✓ Need verify |
| `wiki_cross_ref.py` | Bidirectional links | ✓ Need verify |
| `semantic_search.py` | Search wiki | ✓ Need verify |
| `task_checker.py` | Task discovery | ✓ Functional |
| `autonomous_task_executor.py` | Execute tasks | ✓ Functional |
| `autonomous_deep_research.py` | Research | ✓ Functional |
| `wiki_self_evolution_agent.py` | Orchestrator | ✓ Need verify |

### Missing (CRITICAL) ❌
| Script | Purpose | Priority |
|--------|---------|----------|
| `topic_workflow.py` | Raw → Concept pipeline | HIGH |
| `cron_daily_ingest.py` | Daily ingest orchestrator | HIGH |
| `watchdog_processor.py` | Process new raw files | MEDIUM |

---

## Alternatives & Trade-offs

### Alternative 1: Full Multi-Agent System
- Separate Scholar (content), Librarian (links), Scientist (analysis) agents
- **Trade-off**: Complex, may be overkill for personal wiki

### Alternative 2: Pure Scheduled Cron
- No watchdog, pure time-based triggers
- **Trade-off**: Misses new raw files until next cron

### Alternative 3: External Agent (e.g., Claude Code)
- Let external agent maintain wiki
- **Trade-off**: Violates memory ownership principle (Harrison Chase's point)

**Chosen**: Hybrid — scheduled cron + watchdog + Hermes Dojo tracking

---

## Risks

1. **Script compatibility** — 47 scripts, some may be broken. Need verification phase.
2. **Quality control** — Auto-generated content may be low quality. Need human review loop.
3. **Cron reliability** — macOS cron vs launchd. May need different approach.
4. **Wiki bloat** — Too much auto-generated content dilutes quality. Need strict thresholds.

---

## Success Metrics

- Poor pages (< 4.0): 0
- Fair pages (4-6): < 20
- Good pages (6-8): > 80
- Excellent pages (8+): > 25
- Orphan pages: 0
- Broken links: 0
- Cron jobs running: 4/4

---

## Next Actions

1. **Verify scripts** — Run each script, fix broken ones
2. **Create `topic_workflow.py`** — Missing critical piece
3. **Set up cron jobs** — Ensure schedules run
4. **Create `cron_daily_ingest.py`** — Orchestrate daily processing
5. **Document run instructions** — So Anh can trigger manually

---

## Confidence Scoring

| Factor | Score | Weight |
|--------|-------|--------|
| Research Depth | 8 | 30% |
| Solution Clarity | 9 | 25% |
| Feasibility | 8 | 20% |
| Completeness | 8 | 15% |
| Risk Awareness | 8 | 10% |
| **Total** | **8.5** | **100%** |

---

*Generated: 2026-04-12*
