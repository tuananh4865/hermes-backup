---
title: Hermes Autoresearch — Agentic Research Loop
name: hermes-autoresearch
created: 2026-04-27
updated: 2026-05-05
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

## Metrics

```
Skills_Score = skills_improved × 10
Agents_Score = frameworks × 10 + techniques × 5 + patterns × 3
Hermes_Score = capabilities_improved × 20 + wiki_updated × 2
```

**Note:** These are tracked qualitatively. Agent self-reports progress via telegram.

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

Tonight's focus: [Capability em chọn]
Why chosen: [Reason based on Anh's needs]

## Skills Improvement
- Skills improved: N

## AI Agents Research
- Techniques documented: N

## Hermes Agentic
- Capabilities worked on: N
- Score so far: X

## Next action
[What I'm doing next]
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
| `~/.hermes/autoresearch/AGENTIC_COMPANY_PLAN.md` | Vision for agentic company |
| `~/.hermes/autoresearch/program.md` | Full 16 capabilities + decision framework |
| `~/.hermes/skills/` | Hermes skills |
| `/Volumes/Storage-1/Hermes/wiki/` | Wiki knowledge base |
| `~/.hermes/hermes-agent/` | Hermes gateway code |

## Cron Jobs

| Job ID | Name | Schedule | Purpose |
|--------|------|----------|---------|
| a4b8e528983f | Autoresearch Nightly | 0 2 * * * (2AM) | Self-improvement loop, forever |
| a5c02f2f0d87 | Hermes X Research | 0 7 * * * (7AM) | Daily X research, 50+ results |

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

- SHS metric may need refinement — not all low-confidence skills are bad
- Script path must be absolute when invoked from cron (directory context differs)
- Some 16 capabilities may overlap or have dependencies
- Telegram polling conflict (multiple Hermes instances) — requires manual kill
- TikTok headless browser CAPTCHA — real Chrome workaround confirmed

## Pitfalls (AVOID THESE)

1. **Vague goals** — "make X more agentic" will fail. Always use metric + stop condition.
2. **Over-researching before acting** — 5 min max per experiment. If no clear action after 5 min, try different angle.
3. **Git not used as memory** — Always `git commit` on success, `git reset` on failure. Without this, you lose progress tracking.
4. **Skipping telegram reports** — Progress not visible to Anh = session appears unproductive.
5. **Confusing "skills improvement" with "creating new skills"** — SHS measures existing skill health first.
6. **Ignoring DISCARDED.md** — Failed experiments contain lessons. Re-reading prevents repeated mistakes.
7. **Picking too many capabilities** — ONE capability per night. Spreading effort = no measurable progress.
8. **Not checkpointing** — Long sessions risk context loss. Update TASK_STATE.md every 10 tool calls.
9. **Conflicting cron jobs** — 2AM autoresearch and 7AM X research can overlap if autorseach runs long.
10. **Wiki self-heal is NOT all-purpose** — `wiki_self_heal.py --fix --all` cannot repair:
    - Stale Telegram transcript references (files deleted/moved)
    - Orphaned pages (legitimate wiki pages with no inbound links)
    - Broken wikilinks in `projects/` directory
    - Run `wiki_lint.py --fast` first to get a quick health read, then full lint only if fast passes.

**Revised Wiki Health Workflow (verified 2026-05-05):**
```
# Quick health check (2 min)
python3 scripts/wiki_lint.py --fast

# If fast passes (0 issues) → done
# If fast shows issues → try self-heal
python3 scripts/wiki_self_heal.py --fix --all

# Full lint only for detailed report (not for blocking action)
python3 scripts/wiki_lint.py
```

**Note:** 461 broken wikilinks persisting after self-heal is NORMAL for a wiki with many Telegram transcripts. The broken links are stale transcript references, not active content. Prioritize fixing broken links in `concepts/` and `entities/` over `projects/`.

11. **Skills directory architecture** — `~/.hermes/skills/` has TWO types of directories:
    - **Leaf skills** (e.g., `browser-harness`, `multi-agent-orchestrator`): Have `SKILL.md`, counted in SHS
    - **Category directories** (e.g., `apple/`, `mlops/`, `creative/`): Group related skills, NO `SKILL.md` — this is intentional, NOT a gap. Example: `apple/` contains `apple-notes/`, `apple-reminders/`, `findmy/`, `imessage/` as separate skill subdirectories.
    - When counting skills for SHS, count only leaf skills with `SKILL.md`.
    - To list skills: use `skills_list()` tool, NOT `find ~/.hermes/skills -name SKILL.md` (returns 0 on some shells due to globbing issues).

## References
## Key Lessons Learned (2026-05-04)

1. **Goal specificity is critical** — "make X more agentic" is TOO VAGUE. Must have metric + stop condition.
2. **Em TỰ CHỌN** — User wants agent to autonomously decide capability priority based on impact to his work
3. **16 capabilities scope** — Full list gives agent flexibility to choose what to improve
4. **3 focuses**: Skills improvement (always), AI agents research, Hermes agentic (rotate)
5. **Cron repeat=0** means infinite — run until goal achieved

## Known Issues

- SHS metric may need refinement — not all low-confidence skills are bad
- Script path must be absolute when invoked from cron (directory context differs)
- Some 16 capabilities may overlap or have dependencies
