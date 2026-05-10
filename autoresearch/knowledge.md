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



## Tonight's Findings (2026-05-11)

### System Status (02:00)
- Wiki: ✅ 3638 files, 0 issues (wiki_lint --fast PASSED)
- Skills: 138 skills listed (SHS = 0)
- Workers: content-creator/outputs/ EMPTY - workers not writing to shared dir
- Cron outputs from yesterday confirmed at ~/.hermes/cron/output/
- Daily review for May 10 confirmed: 58 sessions, Gen Z slang updated

### AI Agent Research — Self-Optimizing + Multi-Agent RL (May 2026)

**New techniques documented:**

1. **Self-Optimizing Multi-Agent (arXiv:2604.02988)** — Self-play + prompt optimization for deep research. Agents explore different prompt combinations to match/exceed expert-crafted prompts.

2. **MAS2 (arXiv ICLR 2026)** — Self-Generative, Self-Configuring, Self-Rectifying Multi-Agent. Tri-agent: generator-implementer-rectifier. CTO (Collaborative Tree Optimization) trains meta-agents.

3. **MARTI-MARS² (arXiv:2602.07848)** — Multi-Agent Reinforced Training and Inference. Self-play scaling via RL. Novel scaling law: single → homogeneous multi-role → heterogeneous multi-agent = higher RL ceiling.

4. **TPGO (arXiv:2604.20714)** — Textual Parameter Graph Optimization. Self-improving MAS using "textual gradients" + GRAO (Group Relative Agent Optimization). Learn from historical optimization experiences.

5. **MARFT (ICLR 2026)** — Multi-Agent Reinforcement Fine-Tuning. Extends MARL to LaMAS (LLM-based Agent MAS). Flex-MG formalization + Action-level/Token-level MARFT.

6. **SCMA (arXiv:2601.21919)** — Self-Compression via MARL for Chain-of-Thought. Segmentation Agent + Scoring Agent collaborate to penalize redundant reasoning.

7. **HyEvo (arXiv:2603.19639)** — Self-Evolving Hybrid Agentic Workflows. LLM nodes + deterministic code nodes. Multi-island evolutionary strategy with reflect-then-generate.

8. **AWO (arXiv:2601.22037)** — Agent Workflow Optimization. Meta-tools bundle redundant tool sequences into single invocations. 11.9% fewer LLM calls, 4.2pp higher success.

9. **TOOLSELF (arXiv:2602.07883)** — Tool-driven self-reconfiguration. Unified task execution + self-adjustment into single action space. 24.1% average gain.

10. **Combee (arXiv:2604.04247)** — Scalable parallel prompt learning. Map-Shuffle-Reduce paradigm for self-improving agents. 17× speedup.

**Key insight:** Self-improvement in multi-agent systems is moving toward: (1) RL-based optimization of agent configurations, (2) self-referential/meta-cognitive modification, (3) learned memory policies replacing heuristics.

---

## Previous Night (2026-05-10)

### System Status (02:00)
- Wiki: ✅ 3637 files, 0 issues (wiki_lint --fast PASSED)
- Skills: 136 skills healthy, SHS = 0
- Workers: content-creator ✅, research-agent ✅ (cron outputs confirmed)
- Autoresearch repo: main branch, clean

### AI Agent Research — Memory Optimization (2026-05-10) — NEW ARXIV PAPERS

**New techniques documented:**

1. **DeltaMem (arXiv:2604.01560)** — RL-trained agentic memory management. Formulates memory updating as end-to-end task. Novel "Memory-based Levenshtein Distance" reward. Training-free version already outperforms baselines.

2. **Unified Memory Agent / UMA (arXiv:2602.18493)** — End-to-end RL framework unifying memory operations + QA. Dual memory: compact core summary + Memory Bank (explicit CRUD). Ledger-QA benchmark for continuous state tracking. Joint optimization outperforms decoupled 2-stage.

3. **Knowledge Access Beats Model Size (arXiv:2603.23013)** — 8B model + memory = 69% of 235B model performance at 4% cost. Up to 47% of user queries are semantically similar to prior interactions. Memory augments routing, not replaces it.

4. **LatentMem (arXiv:2602.03036)** — Learnable multi-agent memory framework. Experience bank (raw trajectories) + memory composer (role-aware latent memories). LMPO (Latent Memory Policy Optimization). 50% fewer tokens, 2x speed. Solves memory homogenization + information overload.

5. **AtomMem (arXiv:2601.08323)** — Reframes memory as CRUD decision-making problem. Learned via SFT + RL. 8B outperforms static memory workflows. Key insight: learned policy increases Create/Update/Delete, decreases Read over time.

6. **MemReader (arXiv:2604.07877)** — Active memory extraction. MemReader-0.6B (distilled passive), MemReader-4B (ReAct active with GRPO). Explicit "think-act-observe" for memory writing decisions. State-of-the-art on LOCOMO, LongMemEval, HaluMem.

7. **Agentic Memory / AgeMem (arXiv:2601.01885)** — Unified LTM + STM management. 5 memory ops as tool-based actions. 3-stage progressive RL (GRPO). 5 benchmarks: outperforms all baselines. Key: proactive summarization before context fills.

8. **OCR-Agent (arXiv:2602.21053)** — Capability Reflection + Memory Reflection for VLM self-correction. Capability constraint filters capability hallucinations. Memory Reflection avoids repetitive attempts. +2.0 on InternVL3-8B English, +1.2 Chinese.

**Key insight:** Memory optimization is moving toward LEARNED policies (RL/SFT) rather than heuristics. CRUD operations becoming standard memory interface. Unified STM/LTM management outperforms separate systems.

**Sources:**
- arXiv:2604.01560 — DeltaMem (Apr 2026)
- arXiv:2602.18493 — UMA (Feb 2026)
- arXiv:2603.23013 — Knowledge Access (Mar 2026)
- arXiv:2602.03036 — LatentMem (Feb 2026)
- arXiv:2601.08323 — AtomMem (Jan 2026)
- arXiv:2604.07877 — MemReader (Apr 2026)
- arXiv:2601.01885 — AgeMem (Jan 2026)
- arXiv:2602.21053 — OCR-Agent (Feb 2026)

---

## Previous Night (2026-05-09)

### Skill Improvement: tiktok-viral-script
- Added 3 complete example scripts (product discovery, warning hook, transformation)
- Added pitfalls section (6 categories of mistakes)
- Fixed broken relationship: xitter → xurl, added gen-z-slang-2026-04
- Skill now: 289 lines (was 213)

### AI Agent Research — Self-Improving Agents (2026-05-09)

**10 new techniques documented:**
1. ERL (Experiential Reflective Learning)
2. ICPO (In-Context Policy Optimization)
3. Trajectory-Informed Memory Generation
4. Hyperagents
5. MARS
6. RetroAgent
7. GEA (Group-Evolving Agents)
8. POLARIS
9. Self-Optimizing Multi-Agent
10. Hierarchical Self-Evolving Multi-Agent

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
