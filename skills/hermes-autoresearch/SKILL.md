---
title: Hermes Autoresearch — Agentic Research Loop
name: hermes-autoresearch
created: 2026-04-27
updated: 2026-05-04
type: skill
tags: [autoresearch, self-improvement, karpathy-pattern, agentic]
description: Karpathy-style autonomous research loop — 3 focuses (TikTok + AI Agents + Hermes Agentic), infinite repeat, NEVER STOP
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

### 1. TikTok Content Research
- Monitor TikTok trends (2026 only)
- Find new Gen Z slang (Vietnamese + English)
- Research viral hooks, CTAs, script structures
- Update wiki: `gen-z-slang-2026-04.md`, `tiktok-trends-*.md`

### 2. AI Agents Research
- Monitor AI agent landscape (LangChain, Mastra, Flowise, n8n)
- Research agentic patterns (REPLOM, self-improvement, multi-agent)
- Track MCP, A2A protocols, emerging frameworks
- Update wiki: `ai-agent-trends-*.md`

### 3. Hermes Agentic Features (PRIMARY)
Develop NEW capabilities to make Hermes more autonomous:
- Better memory/recall systems
- Self-debugging capabilities
- Multi-agent coordination
- Proactive task execution
- Autonomous decision making
- Self-improvement loops

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

- `Hermes_Score >= 50` (proposed 5+ features, implemented 2+)
- Found **10+** new Gen Z slang terms
- Documented **5+** new AI agent techniques
- Implemented **1+** working Hermes prototype

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

## Known Issues

- Cron job runs from arbitrary directory — use absolute paths
- Telegram reports every 30 min can be noisy — human can interrupt if too much

---

## References

- `references/karpathy-autoresearch.md` — Karpathy's AutoResearch pattern research
