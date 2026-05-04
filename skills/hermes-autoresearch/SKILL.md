---
title: Hermes Autoresearch — Agentic Research Loop
name: hermes-autoresearch
created: 2026-04-27
updated: 2026-05-04
type: skill
tags: [autoresearch, self-improvement, karpathy-pattern, agentic]
description: Karpathy-style autonomous research loop — Skills Improvement + AI Agents + Hermes Agentic (16 capabilities, em TỰ CHỌN mỗi đêm), infinite repeat, NEVER STOP
trigger: Cron job 2AM hàng đêm, run forever until goal achieved
---

# Hermes Autoresearch — Agentic Research Loop

> Lấy cảm hứng từ [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
> Core philosophy: **give an agent narrow scope + git memory + never stop = autonomous improvement**

## Core Principles

- **program.md is the skill** — human programs the agent via markdown
- **Git is memory** — rollback on failure, commit on success
- **NEVER STOP** — run until goal achieved or human interrupts
- **Multi-dimensional research** — 3 focus areas simultaneously

---

## Repository Structure

```
~/.hermes/autoresearch/
├── program.md          ← Agent instructions (human edits)
├── knowledge.md        ← Persistent memory (insights, what worked/failed)
├── DISCARDED.md        ← Failed experiments (avoid repeating)
├── RESULTS.tsv         ← Log: commit, scores, status, description
└── research.py         ← Optional: benchmark script (not always needed)
```

---

## Three Research Focuses

### 1. Skills Improvement (PRIMARY — every night)
Improve skills in `~/.hermes/skills/`

Metrics:
```
SHS = stale_skills × 10 + missing_examples × 5 + broken_links × 3 + low_confidence × 2
Target: SHS = 0
```

What to improve:
- Add missing examples to skills
- Fix broken `[[wikilinks]]`
- Add pitfalls section
- Verify commands still work
- Raise confidence scores

### 2. AI Agents Research
Research self-improvement patterns and agent frameworks.

Target: Document 5+ new techniques

Focus areas:
- Self-debugging patterns
- Agent skill creation
- Memory optimization
- Multi-agent coordination
- Self-improvement loops
- MCP, A2A protocols

### 3. Hermes Agentic Features (em TỰ CHỌN mỗi đêm)
**Em TỰ QUYẾT ĐỊNH** capability nào để improve, dựa trên:
1. Highest impact cho công việc với anh
2. Quickest improvement (feasible trong 1 night)
3. Foundational (giúp cải thiện capabilities khác)

**16 Agentic Capabilities:**

| Category | Capability |
|----------|------------|
| Core | Self-Debugging, Self-Correction, Learning from Failures, Proactive Work |
| Knowledge | Memory Optimization, Knowledge Acquisition, Context Management |
| Skill/Tool | Skill Creation, Tool Use, Tool Creation |
| Planning | Goal Decomposition, Planning, Priority Setting, Reasoning |
| Collaboration | Multi-Agent Coordination, Delegation |

Metrics:
```
Hermes_Score = self_debug_fixed × 10 + skills_created × 20 + mistakes_prevented × 5
```

---

## Metrics (Multi-dimensional)

```
TikTok_Score = trends_found × 10 + slang_added × 5 + patterns_found × 3
Agents_Score = frameworks_found × 10 + patterns_found × 5 + techniques_added × 3
Hermes_Score = features_proposed × 10 + features_implemented × 20 + wiki_pages_updated × 2
```

**Note:** These are tracked qualitatively, not via script. Agent self-reports progress.

---

## Success Criteria (STOP when ANY met)

- `SHS = 0` (all skills healthy)
- `Hermes_Score >= 50`
- Documented **5+** new AI agent techniques
- Created **3+** new skills autonomously
- Error resolution rate > 80%

---

## Experiment Loop

```
LOOP FOREVER (until success criteria met OR human interrupts):

1. Read program.md, knowledge.md, DISCARDED.md
2. Pick ONE focus area
3. Research (web search, docs, experimentation)
4. Implement or document findings
5. Measure score improvement
6. If improved → git commit
7. If no progress → try different angle, git reset
8. Update knowledge.md
9. Every 30 min → send progress to telegram
10. STOP ONLY when success criteria met OR human interrupts
```

---

## Cron Job Configuration

```bash
# Job ID: a4b8e528983f
# Schedule: 0 2 * * * (2AM daily)
# Repeat: forever (vô hạn)
# Deliver: telegram:1132914873:3764041476

cronjob update --job_id a4b8e528983f --repeat 0  # 0 = infinite
```

---

## Progress Reports (every 30 min to Telegram)

```
# Autoresearch Progress — HH:MM

## TikTok Research
- Slang found: N
- Patterns documented: N

## AI Agents Research  
- Frameworks found: N
- Techniques documented: N

## Hermes Features
- Proposed: N
- Implemented: N

## Current focus
[What you're working on right now]

## Blockers
[Any issues]
```

---

## Key Differences from Karpathy

| Aspect | Karpathy AutoResearch | Hermes Autoresearch |
|--------|----------------------|---------------------|
| Domain | LLM training | 3 research focuses |
| Metric | val_bpb (single) | Multi-dimensional scores |
| Time | 5 min fixed | 5 min per experiment |
| Stop | Never | Goal achieved or human |
| Reports | None | Every 30 min to Telegram |

---

## Important Paths

| Path | Purpose |
|------|---------|
| `~/.hermes/autoresearch/` | Autoresearch repo |
| `~/.hermes/skills/` | Hermes skills |
| `/Volumes/Storage-1/Hermes/wiki/` | Wiki knowledge base |
| `~/.hermes/hermes-agent/` | Hermes gateway code |

---

## Critical: Goal Specificity Rule

**"Make X more agentic" = TOO VAGUE = WILL FAIL**

Karpathy-style autonomy requires TREMENDOUS specificity:

| ❌ Vague | ✅ Specific |
|----------|------------|
| "Make Hermes more agentic" | "Self-debugging: resolve 80% errors autonomously" |
| "Improve skills" | "SHS = 0 (stale×10 + missing_examples×5 + broken_links×3 + low_conf×2)" |
| "Research AI agents" | "Document 5 new techniques from arxiv/github" |

**Rule:** Every goal MUST have:
1. Metric formula (even if simplified)
2. Concrete stop condition (exact number)
3. Measurable output (wiki page, skill, prototype)

If goal is vague → user WILL push back → wasted session

---

## Known Issues

- SHS = 0 có thể không đạt được nếu some skills truly need low confidence
- Script path phải là absolute vì cron job chạy từ directory khác

---

## References

- `references/karpathy-autoresearch.md` — Karpathy's AutoResearch pattern research
