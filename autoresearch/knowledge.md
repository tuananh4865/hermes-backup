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

### Tonight's Findings (2026-05-17)

### System Status (02:00)
- Wiki: ⚠️ 1 issue — missing frontmatter on hermes-x-research-2026-05-16.md (FIXED)
- Skills: 142 skills healthy, SHS = 0
- Workers: content-creator outputs/ LAST OUTPUT May 14 morning (7009 bytes) — 3 days stale
- Gen Z slang: May 14 content has "lọ", "SÍT RỊT" — already in wiki entity, no new terms to sync
- Session logs: ~/Library/Application Support/hermes-agent/sessions/ not accessible (empty)

### AI Agent Research — Self-Debugging (May 17, 2026)

Research focus tonight: **Self-Debugging** capability — latest arXiv techniques.

**7 new techniques documented in self-debugging-techniques-may-2026.md:**

1. **ReflexiCoder** (arxiv:2603.05863) — RL-zero trains reflection-correction trajectory into model weights. No external oracles needed at inference.

2. **Polaris** (arxiv:2603.23129) — Gödel agents: inspect policy → trace → modify → test loop. Experience abstraction distills failures into reusable strategies. 7B model consistent gains.

3. **DebugRepair** (arxiv:2604.19305) — LLM-based APR with simulated instrumentation. Test semantic purification + LLM-inserted breakpoints + hierarchical patch refinement.

4. **SelfHeal** (arxiv:2604.17699) — Multi-agent bug fix for LLM agents. Fix agent + critic agent. Internal fix rules + external web search. Gemini 3 Pro outperforms all baselines.

5. **ErrorProbe** (arxiv:2604.17658) — Self-improving error diagnosis in multi-agent systems. 3-stage: MAST taxonomy → backward tracing → multi-agent diagnosis. Verified episodic memory prevents corruption.

6. **DeepVerifier** (arxiv:2601.15808) — Test-time rubric-guided verification. DRA Failure Taxonomy (5 categories, 13 subcats). +8-11% on GAIA/XBench-DeepResearch.

7. **ERL** (arxiv:2603.24639) — Experiential Reflective Learning. Heuristics from trajectories. +7.8% on Gaia2. Selective retrieval essential.

**Key insight:** Self-debugging paradigm shift — from external feedback → self-generated verification, from response-level → policy-level changes, from single agent → multi-agent diagnosis teams.

### Wiki Fix Applied
- Added missing frontmatter to queries/hermes-x-research-2026-05-16.md

### Gen Z Slang Status
- Worker output May 14: "lọ" (HOT), "SÍT RỊT" (135M+ posts) — both already in wiki entity
- No new slang terms to sync tonight
- Workers stale since May 14 (3 days) — content-creator still producing but not firing

---

## Previous Night (2026-05-14)

### System Status (02:00)
- Wiki: ✅ 3638 files, 0 issues (wiki_lint --fast PASSED)
- Skills: 139 skills listed (SHS = 0)
- Workers: content-creator/outputs/ May 14 morning (7009 bytes) confirmed fresh
- Content Creator May 14 morning: 3 scripts (Kem Chống Nắng SPF50+, Body Mist LACOON, Neck Fan InnoYO)

### AI Agent Research — Self-Evolving + RL-based Memory (May 2026)

**New techniques documented:**

1. **SAGE (Skill Augmented GRPO for Self-Evolution)** — RL framework enabling agents to learn skills across task chains and reuse them. 2x success rates when utilizing learned skills from skill library. Sequential Rollout mechanism.

2. **Self-Evolving Software Agents (arXiv:2604.27264)** — BDI-LLM architecture combining Belief-Desire-Intention reasoning with LLMs. Automated evolution module operates alongside reasoning loop, enabling autonomous evolution of goals, reasoning, and executable code.

3. **Memory-R1** — RL framework equipping LLMs with ability to actively manage external memory. Agents trained when to store, retrieve, update, summarize, discard. 5 memory ops as callable tools.

4. **SISL (Self-Improving Skill Learning)** — Skill-based meta-RL framework for robust skill learning from noisy/suboptimal offline data. Addresses imperfect demonstration learning.

5. **Real-Time Procedural Learning** — State-indexed procedural memory letting agents learn from past experiences, improving accuracy and reliability over time.

6. **SAGE (Multi-Agent Self-Evolution, arXiv:2603.15255)** — Closed-loop framework with 4 agents: Challenger, Planner, Executor, Reflector for generalized reasoning evolution.

**Key insight:** Self-improvement paradigm shifting from heuristic-based to RL-trained policies. Memory operations (store/retrieve/update/summarize/discard) becoming standard callable tools trained via GRPO/PPO. BDI reasoning + LLM = autonomous goal/reasoning evolution.

---

## Previous Night (2026-05-10) — CORRECTED

### System Status (02:00)
- Wiki: ✅ 3637 files, 0 issues
- Skills: 136 skills healthy, SHS = 0
- Workers: content-creator ✅, research-agent ✅ (cron outputs confirmed)
- Autoresearch repo: main branch, clean

### AI Agent Research — Memory Optimization (2026-05-10)

**8 new techniques documented:** DeltaMem, UMA, Knowledge Access Beats Model Size, LatentMem, AtomMem, MemReader, AgeMem, OCR-Agent.

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
---

## Git
- Autoresearch repo: ~/.hermes/autoresearch
- Backup remote: git@github.com:tuananh4865/hermes-backup.git

## Tonight's Findings (2026-05-15)

### System Status (02:00)
- Wiki: ✅ clean
- Skills: 139 skills, SHS = 0
- Workers: STALE since May 11 (4 days) — content-creator/outputs/ last May 11
- Gen Z slang: wiki entity May 11, found "lỏ/lọ" new variants from May 5 web search

### Hermes X Research — May 15, 2026
- Hermes Agent: **150,290 stars** (up from 131.8K on May 10), global rank #47
- v2026.5.7 "The Tenacity Release" (May 7): Kanban multi-agent, /goal persistent, checkpoints v2, 8 P0 security fixes
- v2026.4.30 "The Curator Release": Autonomous skill library maintenance, 57% TUI cold start reduction

### AI Agent Frameworks Comparison (2026)

| Framework | Score | Stars | Latency | Best For |
|-----------|-------|-------|---------|----------|
| LangGraph | 44/50 | 130K | ~1.2s | Complex workflows, enterprise |
| CrewAI | 38/50 | 46K | ~1.8s | Rapid prototyping |
| AutoGen | 35/50 | 55K | ~2.1s | Research (WARNING: 6 months silent) |

### Self-Improving Agent Tools Found

1. **Cognify** — Auto-tunes LangChain/DSPy. 2.8x quality, 10x cost reduction
2. **autoresearch-agents** (hwchase17) — LangSmith-powered autonomous agent optimization
3. **self-evolving-codegen** — 5-agent pipeline with evaluator→analyzer→evolver→tracker. Gen 0→1: 0.506→0.921
4. **Autogenesis** — RSPL+SEPL protocol layers for versioned agent evolution

### Gen Z Slang Update
- "lỏ vãi", "lọ" (HOT, May 5, 2026) — already in wiki entity
- "toang" — already in wiki entity

---

## Previous Night (2026-05-13)

### System Status (02:00)
- Wiki: ✅ 3638 files, 0 issues (wiki_lint --fast PASSED)
- Skills: 138 skills, SHS = 0
- Workers: last ran May 10 (orchestrator not firing properly)
- Gen Z slang: verified fresh in learned-about-tuananh.md (updated 2026-05-11)

### AI Agent Research — Self-Improving Agents (May 2026)

**12 new techniques documented:**

1. **ERL (Experiential Reflective Learning)** — Reflects on trajectories to generate reusable heuristics. +7.8% on Gaia2. Selective retrieval critical.
2. **Polaris (Gödel Agent)** — Policy-level self-repair for small LMs via experience abstraction. 7B achieves consistent gains.
3. **Self-Consolidation** — Contrastive reflection + self-consolidation distills textual experience into latent space.
4. **ReflexiCoder** — RL-zero internalizes self-debugging into model weights. No external oracles needed.
5. **RetroAgent** — Dual intrinsic feedback (numerical + language). SimUtil-UCB retrieval. +18.3% ALFWorld.
6. **MARS** — Single recurrence cycle self-improvement. Principle-based + procedural reflection.
7. **AEL** — Two-timescale bandit + LLM reflection. Key: self-diagnosis is bottleneck (58% memory+reflection gain).
8. **DeepVerifier** — Test-time verification scaling. DRA Failure Taxonomy (5 categories, 13 subcats). +8-11% GAIA.
9. **ICPO** — In-context policy optimization. ME-ICPO with minimum-entropy response selection.
10. **MemPO** — Self-memory policy optimization. 25.98% F1 gain, 67.58% token reduction.
11. **EMPO²** — Hybrid on/off-policy RL. 128.6% improvement over GRPO on ScienceWorld.
12. **MCMA** — Meta-cognitive memory abstraction. Memory Copilot via DPO. +25.07% ALFWorld.

**Key insight:** Self-improvement shifting from heuristic → RL-trained policies. Self-diagnosis is the bottleneck, not experience accumulation. Memory operations as callable tools trained via GRPO.

## Tonight's Findings (2026-05-14)

### System Status (02:00)
- Wiki: ✅ 0 issues — fixed missing frontmatter on references/self-improving-agents-may-2026.md
- Skills: 138 skills, SHS = 0
- Workers: Content Creator last ran May 13 18:02, Research Agent last ran May 12 14:08 (both stale)
- Gen Z slang: May 13 content has "thơm vãi", "sống nổi", "pin trâu" — already in wiki entity

### AI Agent Research — Multi-Agent Coordination (May 2026)

**8 NEW techniques found:**

1. **SECP (Self-Evolving Coordination Protocol)** — arxiv:2602.02170
   - Bounded self-modification of coordination protocols while preserving formal invariants
   - Coverage increased from 2→3 accepted proposals after 1 recursive modification
   - Byzantine fault tolerance, O(n²) message complexity

2. **TPGO (Textual Parameter Graph Optimization)** — arxiv:2604.20714
   - Multi-agent system optimization as graph evolution problem
   - Textual gradients (structured NL feedback from execution traces)
   - GRAO (Group Relative Agent Optimization) — learns from historical optimization experiences

3. **CORAL (Autonomous Multi-Agent Evolution)** — arxiv:2604.01658
   - Shared persistent memory + asynchronous multi-agent execution + heartbeat-based interventions
   - 10× fewer evaluations than fixed evolutionary search baselines
   - Kernel engineering: 1363→1103 cycles (20% gain)

4. **REDEREF (Training-Free Agentic Coordination)** — arxiv:2603.13256
   - Thompson sampling for belief-guided delegation
   - Reflection-driven re-routing via calibrated LLM judge
   - 28% token reduction, 17% fewer agent calls, 19% faster time-to-success

5. **Pressure-Field Coordination** — arxiv:2601.08129
   - O(1) coordination overhead via shared artifact state
   - Agents operate locally, coordination emerges from quality signals
   - Temporal decay prevents premature convergence (96.7% vs 86.7%)

6. **Symphony-Coord** — arxiv:2602.00966
   - Decentralized multi-agent via online contextual bandit (LinUCB)
   - Two-stage dynamic beacon protocol (screening + adaptive routing)
   - Sublinear regret bounds, self-healing under distribution shifts

7. **EvoMaster (Foundational Evolving Agent Framework)** — arxiv:2604.17406
   - Iterative self-critique + hypothesis refinement across experimental cycles
   - Multi-agent collaborative evolution (solver/critic/rewriter roles)
   - 41.1% on Humanity's Last Exam, 75.8% MLE-Bench Lite

8. **Self-Optimizing MAS for Deep Research** — arxiv:2604.02988
   - Multi-agent Deep Research systems self-play prompt combinations
   - Matches/exceeds expert-crafted prompts via exploration
   - Orchestrator + parallel worker agents architecture

### Hermes Agentic Focus Tonight
- Capability: Multi-Agent Coordination (highest impact for current workflow)
- Found 8 new techniques to add to orchestrator skill
- Workers stalled since May 12-13 — orchestrator can detect but not recover autonomously

### Priority Actions
1. Add 8 new multi-agent coordination techniques to multi-agent-orchestrator skill
2. Build worker-stall-recovery.sh for autonomous worker restart
3. Gen Z slang already current — no sync needed tonight

---

## Tonight's Findings (2026-05-18)

### System Status (02:00)
- Wiki: ✅ 0 issues (3701 files, wiki_lint --fast PASSED)
- Skills: 141 skills healthy, SHS = 0
- Workers: STALE — last output May 13 evening (9301 bytes), 5+ days old
- Gen Z slang: Updated with 6 new terms from slangloom.com May 2026

### Gen Z Slang Sync (May 18, 2026)
**Source:** slangloom.com (published May 11, 2026) — "Vietnamese Slang: The Ultimate 2K26 Guide"

**New terms added:**
- **Xịn sò** — high quality, impressive, stylish
- **Kèo** — deal, plan, arrangement
- **Quẩy** — party hard, energetic dancing
- **Tạch** — fail, didn't work out
- **Tấu hài** — acting like a comedian unintentionally
- **Hết nước chấm** — extremely good, unbelievably amazing

**Worker status:** Workers stale since May 13 (5+ days). Used web search fallback per MANDATORY death detection rule.

### AI Agent Research — Self-Improving Agents (May 18, 2026)
**Focus:** Self-Improving Agents ecosystem survey

**Key findings from o-mega.ai 2026 guide:**

1. **HyperAgents (Meta, UBC, Oxford, NYU — arxiv:2603.19461)**
   - Transfers self-improvement strategies across DOMAINS (robotics → math grading)
   - imp@50 = 0.630 on novel domain
   - Self-improving improvement loop: agents learn to improve improving

2. **SWE-RL** — Software engineering RL for autonomous code improvement

3. **AlphaEvolve** — Google's evolutionary algorithm for discovering algorithms

4. **ACE (Agentic Context Engineering — arxiv:2510.04618)**
   - Treats contexts as evolving playbooks
   - Accumulates, refines, organizes context over time

**Paradigm shift confirmed:** Self-improving agents moving from single-task to cross-domain strategy transfer. HyperAgents demonstrates that "learning to improve" can generalize.

### Reference Document Updated
- `references/self-improving-agents-2026.md` — Updated with HyperAgents, ACE, SWE-RL, AlphaEvolve
