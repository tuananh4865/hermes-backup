# Hermes Autoresearch Knowledge

## Current Focus (2026-05-05)
Tonight's focus: **Skill Creation #8** — improving existing skills
- Added pitfalls sections to 4 skills
- Adding examples to engineering-diagnose

## Skills Improved Tonight
| Skill | Improvements |
|-------|-------------|
| hermes-autoresearch | Added 10-item pitfalls section |
| engineering-diagnose | Added 2 examples + 5 common pitfalls |
| dogfood | Added 10-item pitfalls section |
| engineering-tdd | Added 10-item pitfalls section |

## Research Baselines
| Area | Baseline | Target |
|------|----------|--------|
| TikTok | 0 slang tracked this session | 10+ new slang |
| AI Agents | 0 techniques this session | 5+ new techniques |
| Hermes | 0 features proposed | 5+ proposed, 2+ implemented |

## What Works
- Web search for latest trends (2026 only)
- Reading GitHub repos for frameworks
- Experimenting with prototype features
- Updating wiki with findings

## What Doesn't Work
[Fill from DISCARDED.md]

## Active Experiments
| Date | Experiment | Score Before | Score After | Status |
|------|------------|--------------|-------------|--------|
| - | - | - | - | - |

## Key Insights
[Agent fills this during research]

## Important Paths
- Wiki: /Volumes/Storage-1/Hermes/wiki
- Skills: ~/.hermes/skills
- Scripts: /Volumes/Storage-1/Hermes/wiki/scripts
- Hermes code: ~/.hermes/hermes-agent/

## Research Sources
- TikTok: web search for "TikTok trends 2026", "Gen Z slang 2026"
- AI Agents: arxiv.org, github.com/trending, Hacker News
- Hermes: ~/.hermes/hermes-agent/gateway/, ~/.hermes/skills/



## Tonight's Findings (2026-05-09)

### Skill Improvement: tiktok-viral-script
- Added 3 complete example scripts (product discovery, warning hook, transformation)
- Added pitfalls section (6 categories of mistakes)
- Fixed broken relationship: xitter → xurl, added gen-z-slang-2026-04
- Skill now: 289 lines (was 213)

### AI Agent Research — Self-Improving Agents (2026-05-09) — NEW ARXIV PAPERS

**New techniques documented:**

1. **Experiential Reflective Learning (ERL)** — reflects on task trajectories + outcomes to generate transferable heuristics. Gaia2 benchmark: +7.8% over ReAct baseline. Key: selective retrieval essential.

2. **In-Context Policy Optimization (ICPO)** — test-time scaling via multi-round self-reflection. ME-ICPO uses minimum-entropy selection for robust self-assessed rewards.

3. **Trajectory-Informed Memory Generation** — 4-component pipeline: Trajectory Intelligence Extractor + Decision Attribution Analyzer + Contextual Learning Generator + Adaptive Memory Retrieval. AppWorld: +14.3pp goal completion, +28.5pp on complex tasks.

4. **Hyperagents (Meta, Mar 2026)** — integrates task agent + meta agent (both editable). Metacognitive self-modification enables open-ended improvement. DGM-H outperforms DGM across coding, paper review, robotics, math grading.

5. **MARS (Metacognitive Agent Reflective Self-improvement)** — principle-based (normative rules) + procedural (step-by-step strategies) reflection in SINGLE recurrence cycle. 6 benchmarks, outperforms SOTA with reduced compute.

6. **RetroAgent** — hindsight self-reflection with dual intrinsic feedback: (1) intrinsic numerical feedback tracks subtask completion, (2) intrinsic language feedback distills reusable lessons. GRPO-trained agent comparisons: +18.3% ALFWorld, +15.4% WebShop, +27.1% Sokoban, +8.9% MineSweeper.

7. **Group-Evolving Agents (GEA)** — group-centric evolution (not individual). Experience sharing within group → sustained progress. SWE-bench: 71.0% vs 56.7% baseline. Fixes framework-level bugs in 1.4 iterations avg (vs 5 for tree-based).

8. **POLARIS** — recursive self-improvement for SMALL models via experience abstraction: failures → analysis → strategy synthesis → patch generation → patch integration. Bounded retries + conservative checks. Traceable memory.

9. **Self-Optimizing Multi-Agent for Deep Research** — agents self-play different prompt combinations to optimize Deep Research systems. Matches/exceeds expert-crafted prompts.

10. **Hierarchical Self-Evolving Multi-Agent** — Base LLM + SLM agent + Code-Gen LLM + Teacher-LLM. Escalation: reasoning → tool synthesis → evolution (CL/RL/GA). TaskCraft dataset: CL=fast recovery, RL=high difficulty, GA=diversity.

**Key insight:** Self-improvement is moving from single-agent reflection to multi-agent collaboration + group evolution + hierarchical metacognition.

**Sources:**
- arXiv:2603.24639 — ERL (Mar 2026)
- arXiv:2603.01335 — ICPO (Mar 2026)
- arXiv:2603.10600 — Trajectory Memory (Mar 2026)
- arXiv:2603.19461 — Hyperagents (Mar 2026)
- arXiv:2601.11974 — MARS (Jan 2026)
- arXiv:2603.08561 — RetroAgent (Mar 2026)
- arXiv:2602.04837 — GEA (Feb 2026)
- arXiv:2603.23129 — POLARIS (Mar 2026)
- arXiv:2604.02988 — Self-Optimizing Multi-Agent (Apr 2026)
- arXiv:2601.11658 — Hierarchical Self-Evolving (Jan 2026)

### Session Log Analysis Status (2026-05-08)
- Sessions directory: `~/Library/Application Support/hermes-agent/sessions/` — accessible (0 bytes, empty)
- Worker outputs: content-creator + research-agent outputs/ still EMPTY (workers running but not writing to shared outputs/)
- Daily log: ~/.hermes/workers/memory/daily/ — empty
- MEMORY.md: last updated May 5

### System Status (2026-05-08 02:00)
- Wiki: ✅ 3630 files, 0 issues (wiki_lint --fast PASSED)
- Cron jobs: All 7 worker crons verified with correct SOUL.md prompts
- Autoresearch repo: Clean, on branch autoresearch/2026-05-08
- Skills: SHS = 0 (134 skills healthy)

### Critical Gap: Workers Not Writing to Shared Outputs/
- Workers (content-creator, research-agent) cron jobs running and producing output
- BUT outputs go to cron output directory (~/.hermes/cron/output/{job_id}/)
- Workers NOT writing to shared outputs/ directories (content-creator/outputs/, research-agent/outputs/)
- This means orchestrator can't find worker products to aggregate
- Root cause: Workers write response to cron delivery, NOT to shared file system

**Fix needed:** Workers need to write output files explicitly to ~/hermes/workers/{worker}/outputs/ in addition to responding.

---

## Previous Night (2026-05-07)

### Critical Fix: Worker Cron Jobs
- All 7 worker cron jobs were running `hermes-autoresearch` skill instead of SOUL.md
- Root cause: `cron edit --prompt "$(cat SOUL.md)"` shell expansion fails
- Fix: Use Python subprocess with explicit prompt string, --clear-skills flag
- Verification: Check cron output directory for most recent run, should show correct SOUL.md not skill content

### Cron Edit Pattern (VERIFIED 2026-05-07)
```python
result = subprocess.run(
    [sys.executable, '-m', 'hermes_cli.main', 'cron', 'edit', 
     job_id, '--prompt', soul_md_content, '--clear-skills'],
    cwd='/path/to/hermes-agent'
)
```

### Orchestrator Status
- Orchestrator cron running correctly: SOUL.md content visible in 02:01:32 run
- Worker output directories still empty: workers haven't been assigned tasks yet
- Next step: Orchestrator needs to learn to create worker tasks AND write to output files

### Session Log Analysis
- Sessions directory not found at expected path
- Daily log directory exists but empty (no entries)
- MEMORY.md last updated May 5


## Git
- Autoresearch repo: ~/.hermes/autoresearch
- Backup remote: git@github.com:tuananh4865/hermes-backup.git
