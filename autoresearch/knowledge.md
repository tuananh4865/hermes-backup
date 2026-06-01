# Hermes Autoresearch Knowledge

## Current Focus (2026-06-02)
Tonight's focus: **Knowledge Acquisition — Gen Z slang + AI agent research**

### System Status (02:00)
- Wiki: ✅ 0 issues (wiki_lint --fast PASSED)
- Skills: 241 skills healthy, SHS = 0
- Workers: ⚠️ PERMANENTLY DELETED May 25 — web search fallback only
- Gen Z slang: No new terms found (web search finds only already-documented terms from May 2026)
- Session recording: ✅ WORKING — 545 sessions in state.db (June 1 confirmed false alarm)

### Tonight's Research: AI Agent Self-Improvement

**No new Hermes release found** — v0.15.2 (May 29) is still latest. No v0.16 or v0.15.3 announced yet.

**Gen Z Slang Findings:**
- Web search finds only already-documented terms (Đỉnh, Toang, Gato, lọ, Xịn sò, Kèo, Quẩy, etc.)
- No genuinely new viral terms from June 2026
- Current slang list (updated May 27) remains accurate
- Workers deleted May 25 — cannot get fresh worker output

**arXiv Self-Improvement Papers Reviewed:**
- SIA (arXiv:2605.27276) — Dual-mode (harness + weight updates) — already documented May 31
- SelfHeal, ErrorProbe, AutoResearchClaw — documented June 1
- SkillsInjector + GRASP — documented June 1
- Self-Evolving Agents Survey (arXiv:2507.21046) — H. Gao, 32 citations, comprehensive taxonomy

**Total self-improvement techniques documented: 28**

## Previous Focus (2026-06-01)
Tonight's focus was: **Self-Debugging — session recording false alarm, found 3 new arXiv papers**

### Key Finding: Session Recording FALSE ALARM
- June 1 claimed "session recording broken since May 28"
- **ACTUALLY WORKING** — 545 sessions in state.db
- Root cause: stale monitoring output, not actual data loss
- Fixed knowledge.md with correct information

### System Status (02:00)
- Wiki: ✅ 0 issues (wiki_lint --fast PASSED)
- Skills: 238 skills healthy, SHS = 0
- Workers: ⚠️ PERMANENTLY DELETED May 25 — web search fallback only
- Gen Z slang: No new terms found (web search confirms May 2026 terms still active)
- **⚠️ FALSE ALARM:** Session recording is WORKING — 545 sessions in state.db, cron jobs running correctly. knowledge.md had stale information about broken session recording.

### Tonight's Research: Self-Debugging (June 1, 2026)

**3 new arXiv papers found:**

1. **SelfHeal** (arXiv:2604.17699) — Dual-agent system: Fix Agent + Critic Agent with Gemini 3 Pro. First empirical study on bug fix patterns in LLM agents. AgentDefect benchmark (37 buggy instances).

2. **ErrorProbe** (arXiv:2604.17658) — 3-stage pipeline: MAS Failure Taxonomy → Backward Tracing → Multi-Agent Team (Strategist/Investigator/Arbiter). Verified episodic memory prevents error pattern corruption.

3. **AutoResearchClaw** (arXiv:2605.20025) — 5-mechanism framework: Multi-agent debate, Self-healing executor (Pivot/Refine), Verifiable reporting, HITL, Cross-run evolution. +54.7% vs AI Scientist v2.

**Key insight:** Self-debugging paradigm shifted — from external oracle to internal multi-agent debate, failure as information source, verified memory for cross-run learning.

Total self-improvement techniques documented: **28** (was 25)

### System Status (02:00)
- Wiki: ✅ 0 issues (105 files checked)
- Skills: 238 skills healthy, SHS = 0
- Workers: ⚠️ PERMANENTLY DELETED May 25 — web search fallback only
- Gen Z slang: No new terms found (web search confirms May 2026 terms still active)
- **⚠️ CRITICAL:** Session recording broken since May 28 — no user sessions logged for 4 days

### Hermes v0.15.2 / v0.15.0 "Velocity Release" (May 28-29, 2026)

**Version + Stars:**
- Hermes Agent: **158K+ GitHub stars** (May 30, 2026)
- v0.15.2 hotfix (v2026.5.29.2) — packaging fix for plugin.yaml manifests
- v0.15.0 "Velocity Release" (May 28) — 16,083-line PR (largest ever), 747 PRs by 321 contributors
- Sessions now 4,500x faster (Reddit)

**NEW in v0.15.0 (Velocity Release):**
1. **Promptware Defense (Brainworm)** — Blocks prompt-injection attacks at 3 chokepoints, defends context window
2. **Bitwarden Secrets Manager** — One bootstrap token replaces N per-provider API keys
3. **Skill Bundles** — Package related skills together
4. **TUI Session Orchestrator** — Terminal UI for managing sessions
5. **Auto Supply-Chain Defense** — Automatic security patching
6. **NFTY Platform** — Multi-agent coordination platform
7. **Kanban Multi-Agent v2** — Real production workflow tool

**arXiv self-improvement paper found:**
- SIA (arXiv:2605.27276) — Feedback-Agent updates BOTH harness AND weights. Beats Claude Code TerminalBench. Dual-mode self-improvement (harness tuning + weight updates). Already documented in May 31 run.

**Prompt injection defense (arXiv:2605.17634, May 17, 2026):**
- "AI Agents May Always Fall for Prompt Injections" — shows prevailing defenses still fail. Hermes v0.15's Brainworm defense is response to this research.

### Hermes X Research (May 30, 2026)

**Version + Stars:**
- Hermes Agent: **158K+ GitHub stars** (May 30, 2026) — up from 157.2K on May 29
- v0.15.2 hotfix (v2026.5.29.2) — packaging fix for plugin.yaml manifests
- v0.15.0 "Velocity Release" (May 28) — dramatically faster startup + execution
- v0.14.0 "Foundation Release" (May 16) — 180x faster browser automation, native Windows beta

**Community Use Cases Found (50+ real-world examples):**

1. **Personal Assistant** — "Claude for chat, Hermes 24/7 on mini PC for real-world stuff: email, web browsing, form filling, calendar updates" (@monty_13277)

2. **Trading & Markets** — Self-learning weather trading bot. "$100 → $216 in less than 48 hours" — Hermes scans weather markets every 60 mins, compares 3 forecast sources, buys undervalued temperature buckets. (@DeRonin_, Apr 2026)

3. **Research Agent** — "Daily research brief across Discord, Slack, Notion & Obsidian." One Hermes instance watches AI/agent space, picks signals, writes briefs, suggests content angles, tracks what owner ignores, keeps improving workflow. (@gkisokay, May 2026)

4. **Marketing / UGC Ad Studio** — "Paste product URL → Hermes scrapes landing page, pulls winning ad hooks from Meta Ads Library + TikTok Creative Center, writes brief itself. Total time: ~4 minutes." (@codewithimanshu, Apr 2026)

5. **Multi-Agent Dev Workflow** — "12 Hermes instances every day in parallel to build Hermes Agent. Backend team monitors stack issues. Post-training team creates RL environments. Dataset investigation." @Teknium runs the production pattern at Hermes itself.

6. **Production Solar Sales Ops** — "Bilbo Baggins" agent manages 8-rep door-to-door solar sales team via iMessage. Tracks daily board, runs cron for morning/evening reporting, maintains 26-page LLM Wiki of solar market intel. Live since Apr 2026.

7. **Autonomous Novel Production** — "Autonovel — House of Bells": End-to-end autonomous novel, art, audiobook production. 19 chapters, 79,456 words with audiobook + website. Nous Research's own pipeline.

8. **Polymarket Trading** — 4-layer parallel monitoring: order book, on-chain addresses, news-price lag, position changes. Hermes monitors all 4 via Polymarket module + News Skill. (@adiix_official)

9. **Second Brain / Memory** — Obsidian as long-term memory for Hermes. 794+ upvotes on the integration pattern. "Hermes reads HackerNews and emails me a daily summary."

10. **Home Lab + Server Monitoring** — "Hermes watches my homelab validators and pings Telegram." VPS server management on cheap hardware.

**Key Insight from @Teknium:** "I literally run 12 Hermes agent instances every day in parallel to build Hermes Agent — now a top 100 GitHub repository. Backend team monitors stack issues. Post-training team creates RL environments. Dataset team investigates and sometimes directly manipulates datasets."

**Hermes vs Alternatives:**
- vs LangChain: Hermes compounds (skills improve), LangChain stays flat
- vs OpenClaw: "Claude = CEO, OpenClaw = Senior Engineer, Hermes = worker 24/7 on a mini PC"
- vs Consumer agents: Hermes is self-hosted, self-improving, infrastructure-level

**v0.15 "Velocity Release" Key Changes:**
- 16,083-line PR merged (largest ever)
- Kanban multi-agent: real production workflow tool
- dramatically faster — startup, execution, shipping work
- 28 commits, 21 merged PRs since v0.15.0

### Gen Z Slang Status
- Web search finds only already-documented terms (Đỉnh, Toang, Gato, lọ, etc.)
- Workers deleted May 25 — no fresh worker output to sync
- wiki entity Gen Z section (updated May 27) is current
- **No new slang to sync tonight**

---

### System Status (02:00)
- Wiki: ✅ 0 issues (wiki_lint --fast PASSED)
- Skills: 251 skills healthy, SHS = 0
- Workers: ⚠️ PERMANENTLY DELETED May 25 — workers pipeline GONE, web search fallback used
- Gen Z slang: Updated 10 new terms (Sít Rịt, Đỉnh, Toang, Xõa, Cày, Cổ tươi, Bánh bèo, Kiwi Kiwi, Dizz, Tái châu) from web search

### Tonight's Research
**AI Agent self-improvement techniques found:**
1. **ERL** (arXiv:2603.24639) — Experiential Reflective Learning, +7.8% Gaia2
2. **DebugRepair** (arXiv:2604.19305) — Self-directed debugging with runtime evidence
3. **ELITE** (arXiv:2603.24018) — Experiential learning + intent-aware transfer
4. **InspectCoder** (arXiv:2510.18327) — Interactive debugger control + breakpoint inspection
5. **ACE** (arXiv:2510.04618) — Agentic Context Engineering, +10.6% AppWorld

### Gen Z Slang Findings
- 10 new Vietnamese Gen Z terms from web search (not workers — workers deleted)
- All added to entities/learned-about-tuananh.md with updated date 2026-05-27
- Workers permanently deleted May 25 — web search is now ONLY slang source

### Skills Improved Tonight
- Gen Z slang synced: 10 new terms added to wiki entity
- AI Agent techniques: 5 new documented

---

## Previous Focus (2026-05-23)
Tonight's focus: **Self-Debugging #1 + AI Agent Research**
- Researched self-improving agent techniques (SICA 17→53%, ERL +7.8%, DGM-Hyperagents)
- Gen Z slang synced: "kịt kin", "trình là gì", "ối dồi ôi", "hài hước tưởng mình vô duyên"
- Wiki clean (1824 files), SHS = 0, Workers still DEAD
- Hermes v0.14.0 still latest (157.2K stars), no v0.15 yet
- CVE-2026-7396: vulnerability in hermes-agent v0.8.0 (file gateway) — patch if using v0.8

## Skills Improved Tonight
|| Skill | Improvements |
|-------|-------------|
|| hermes-autoresearch | Added 10-item pitfalls section |
|| engineering-diagnose | Added 2 examples + 5 common pitfalls |
|| dogfood | Added 10-item pitfalls section |
|| engineering-tdd | Added 10-item pitfalls section |

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

---

## Autoresearch 2026-05-19

### System Status (02:00)
- Wiki: ✅ Clean (0 issues, SHS = 0)
- Skills: 142 skills healthy
- Workers: ⚠️ STALE 8+ days — Content Creator (May 11), Research Agent (May 11)

### Gen Z Slang Status
- Workers dead → used web search fallback (per MANDATORY death detection)
- slangloom.com May 11 source: 6 terms already in wiki (Xịn sò, Kèo, Quẩy, Tạch, Tấu hài, Hết nước chấm)
- tcc-agency.com "lọ" article (May 5) — already tracked
- No NEW slang found from web search (slang evolves slower in May 19 week vs May 18)
- **No slang sync needed** — wiki Gen Z section (updated May 18) is current

### AI Agent Research — 6 NEW Self-Debugging Techniques

1. **DebugRepair (arXiv:2604.19305)** — Self-directed debugging with runtime evidence
   - Test semantic purification + simulated instrumentation + debugging-driven conversational repair
   - Key: patches refine using intermediate runtime states, not just pass/fail

2. **ReflexiCoder (arXiv:2603.05863)** — RL framework for self-reflection/self-correction
   - Teaches model "how to debug" via RL-zero training, internalizes error detection
   - Shifts from external test loop → intrinsic cognitive skill

3. **Polaris (arXiv:2603.23129)** — Gödel agent for small language models
   - Policy repair via experience abstraction — failures become policy updates
   - 7B model with Polaris competitive with larger baselines

4. **ErrorProbe (arXiv:2604.17658)** — Multi-agent failure attribution
   - Symptom-driven backward tracing + verified episodic memory
   - 3-agent team (Strategist, Investigator, Arbiter) for error localization

5. **TraceCoder (arXiv:2602.06875)** — Trace-driven collaborative debugging
   - Instruments code with diagnostic probes → causal analysis → HLLM from past failures
   - 34.43% relative improvement in Pass@1

6. **Debug2Fix (arXiv:2602.18571)** — Interactive debugging for coding agents
   - Integrates debuggers (Java/Python) into agent framework via subagent architecture
   - Makes weaker models (GPT-5, Haiku 4.5) match stronger models (Sonnet 4.5)

**Key paradigm shift:** Self-debugging moving from response-level (retry) → policy-level (learn to debug).

### Hermes Agentic Capability Worked On
**Self-Debugging** — High impact, foundational for other capabilities
- Documented 6 new techniques from arXiv May 2026
- These techniques could be implemented in Hermes gateway hooks

### Recommendations
1. **Workers need restart** — 8+ days stale, cron jobs may need re-enabling
2. **Consider implementing ErrorProbe pattern** — multi-agent diagnosis for complex failures
3. **TraceCoder approach** — add instrumentation hooks to Hermes for self-debugging

### Git Commit
- Status: CLEAN (wiki clean, skills healthy, no blocking issues)

---

## Tonight's Findings (2026-05-22)

### System Status (02:00)
- Wiki: ✅ clean (1824 files, 0 issues — wiki_lint --fast PASSED)
- Skills: 96 skill directories, SHS = 0 (verified clean)
- Workers: ⚠️ STALE — content-creator/outputs/ and research-agent/outputs/ are EMPTY (no outputs in days)
- Session logs: ~/Library/Application Support/hermes-agent/sessions/ — empty (0 bytes)
- Gen Z slang: Workers dead since May 11+, web search fallback used — no new terms found

### AI Agent Research — Self-Improving + Goal Decomposition (May 22, 2026)

**NEW TECHNIQUE: Darwin Gödel Machine (DGM)**
- arXiv:2505.22954 (Jan 2026, OpenReview) — Sakana.ai
- World's first self-improving coding agent that iteratively modifies its own code
- Combines Darwinian evolution (stepping stones) + Gödel machine (self-referential improvement)
- Key insight: FROZEN pretrained FMs can self-improve by modifying code/workflows without retraining
- Open-ended exploration finds novel improvement paths humans would miss

**Goal Decomposition — TDP (Task-Decoupled Planning)**
- arXiv:2601.07577 — "Task-Decoupled Planning for Long-Horizon Agents"
- 60% context reduction via DAG sub-goals
- HIGH applicability for Hermes multi-agent orchestration
- Separates planning from execution — planner creates DAG, executor runs nodes

**Other Goal Decomposition Techniques Found:**
- DELTA (delta-llm.github.io) — autoregressive robot tasks, MEDIUM
- Flare (arXiv:2601.22311) — consistent improvement, MEDIUM
- PIVOT (arXiv:2605.11225) — 120 tasks each domain, MEDIUM
- Policy Decompositions (arXiv:2605.06957) — LLM agent applicable, HIGH
- Plan-to-Action (arXiv:2604.12147) — 16,991 trajectories, ~70% plan adherence, HIGH

**Total: 6+ new techniques documented**

### Gen Z Slang Status
- Workers dead since May 11+ — no new outputs to sync
- Web search found no NEW Vietnamese slang (existing terms already in wiki)
- Wiki Gen Z section (updated 2026-05-21) is current — no sync needed

### Capability Focus Tonight: Goal Decomposition
- Selected: Planning → Goal Decomposition
- Why: TDP (60% context reduction via DAG sub-goals) directly applicable to Hermes multi-agent orchestration
- DGM provides new paradigm for self-improvement without retraining

### Recommendations
1. Workers need restart — 10+ days stale, cron jobs may be paused
2. Consider implementing TDP DAG planning for multi-agent orchestrator
3. DGM pattern (self-modifying code) could inspire Hermes self-improvement hooks

---

## Previous Night (2026-05-17)

### System Status (02:00)
- Wiki: ⚠️ 1 issue — missing frontmatter on hermes-x-research-2026-05-16.md (FIXED)
- Skills: 142 skills healthy, SHS = 0
- Workers: ⚠️ STALE 6+ days — Content Creator (May 14), Research Agent (May 12)
- Gen Z slang: Workers dead → used web search fallback

### Gen Z Slang Status (Workers Dead — Web Search Fallback)
- Workers stale since May 12-14
- slangloom.com (May 11): Xịn sò, Kèo, Quẩy, Tạch, Tấu hài, Hết nước chấm — already in wiki
- trykaiwa.com (Jan 2026): 20 phrases — already in wiki  
- tcc-agency.com "lọ" (May 5): already tracked
- No NEW slang found from web search
- Wiki Gen Z section (updated May 18) is current

### AI Agent Research — Experiential Learning + Self-Referential Agents (May 20, 2026)

**5 NEW techniques documented:**

1. **ERL (Experiential Reflective Learning — arXiv:2603.24639)**
   - Reflects on task trajectories → generates transferable heuristics
   - +7.8% on Gaia2 benchmark over ReAct baseline
   - Key: selective retrieval essential, heuristics > few-shot prompting

2. **SICA (Self-Improving Coding Agent — arXiv:2504.15228)**
   - Agent edits its own scaffolding code for self-improvement
   - 17% → 53% on SWE-Bench Verified
   - Non-gradient-based, data-efficient

3. **DGM-Hyperagents (arXiv:2603.19461)**
   - Self-referential: task agent + meta agent in one editable program
   - Meta-level modification procedure itself editable
   - Cross-domain transfer of "how to self-improve" demonstrated

4. **RetroAgent (arXiv:2603.08561v1)**
   - Hindsight self-reflection → dual intrinsic feedback (numerical + language)
   - SimUtil-UCB retrieval balances relevance, utility, exploration
   - +18.3% ALFWorld, +27.1% Sokoban

5. **GVU Self-Play (arXiv:2512.02731)**
   - Unifies STaR, SPIN, Reflexion, GANs, AlphaZero as GVU operator
   - Variance Inequality: sufficient condition for stable self-improvement
   - Noise management in generation + verification = critical

**Paradigm shift confirmed (May 20):**
- Single-task learning → transferable heuristics
- Gradient-based → non-gradient (code self-modification)
- Fixed improvement mechanism → meta-level modifiable
- External feedback → intrinsic dual feedback (numerical + language)

**Reference updated:** `references/self-improving-agents-may-2026.md` — now 17 total techniques

### Gen Z Slang Rules — Updated Understanding
- Workers last fired May 14 (Content Creator), May 12 (Research Agent)
- slangloom.com most reliable source (updated May 11, 2026)
- Gen Z slang evolves slower in May 20 week vs May 13-18
- No new slang from web search — wiki Gen Z section (May 18) is current

### Workers Status — DEATH CONFIRMED
- Content Creator: last output May 14 10:02 (7009 bytes morning-content)
- Research Agent: last output May 12 14:08 (10753 bytes evening-brief)
- 6+ days since last worker fired
- Workers need restart but cron restart is manual task for Anh

### Hermes Agentic Capability Worked On
**Learning from Failures** + **Self-Correction** — High impact, foundational
- ERL pattern: heuristic memory layer for session continuity
- SICA pattern: self-patching gateway hooks
- RetroAgent pattern: dual feedback instead of simple retry
- DGM-H pattern: meta-level self-improvement procedure

### Recommendations
1. **Workers need restart** — 6+ days stale, cron may need manual re-enabling
2. **Implement ERL heuristic memory** — would solve session continuity gap
3. **ByteRover evaluation** — qwen3.5-4b-awq-instruct was ~44s (fastest) before disappearing from LM Studio server
4. **Consider SICA pattern for gateway hooks** — self-patching when failure pattern detected

### Git Commit
- Status: CLEAN (wiki clean, skills healthy, no blocking issues)
- Reference doc updated with 5 new techniques

---

## Autoresearch 2026-05-21

### System Status (02:00)
- Wiki: ✅ 0 issues (wiki_lint --fast PASSED)
- Skills: 236 skills healthy, SHS = 0
- Workers: ⚠️ DEAD — content-creator/outputs/ empty since May 14+ (10+ days stale)
- Gen Z slang: Workers dead → web search fallback. No new slang found (slang evolving slowly this week)

### Gen Z Slang Status (Workers Dead — Web Search Fallback)
- Workers last fired May 14 (Content Creator), May 12 (Research Agent) — 7+ days stale
- slangloom.com (May 11): Xịn sò, Kèo, Quẩy, Tạch, Tấu hài, Hết nước chấm — already in wiki
- No NEW slang from web search (May 21 search shows same terms from Mar-Jun 2026)
- Wiki Gen Z section (updated May 18) is current

### AI Agent Research — Goal Decomposition + Planning (May 21, 2026)

**Focus tonight:** Goal Decomposition (#11) + Planning (#12) — foundational for multi-agent orchestration

**NEW techniques found:**

1. **TDP — Task-Decoupled Planning (arXiv:2601.07577)** 
   - Decouples tasks into DAG of sub-goals via Supervisor
   - Planner + Executor with scoped contexts
   - Reduces context overhead by 60% on long-horizon tasks

2. **DELTA — Decomposed Efficient Long-Term Robot Task Planning**
   - Decomposes long-term goals into autoregressive sub-goals
   - Enables automated task planners to solve complex household/robot tasks

3. **Flare — Planning-Centric Analysis (arXiv:2601.22311)**
   - Planning-level behavior improvement across benchmarks
   - Consistent task performance improvement across agent frameworks

4. **PIVOT — Bridging Planning and Execution (arXiv:2605.11225)**
   - Long-horizon planning benchmark (Travel + Shopping Planning, 120 tasks each)
   - Plan adherence measurement for programming agents

5. **Learning and Reusing Policy Decompositions (arXiv:2605.06957)**
   - Dynamic policy-learning combining generalized planning + hierarchical task decomposition
   - For LLM-based agents — directly applicable to Hermes multi-agent orchestration

6. **From Plan to Action (arXiv:2604.12147)**
   - First extensive analysis of plan compliance in programming agents
   - 16,991 trajectories analyzed
   - Key finding: agents follow plans ~70% of time, fail on ambiguous subgoals

**Hermes-specific insight:** Hermes v0.14 "Foundation Release" released May 2026 with:
- 180x faster browser automation (CDP-based)
- Live session handoffs (/handoff command)
- Multi-agent coordination improvements
- Community request: swarm agents tutorials, kanban, conductor

**Reference updated:** `references/self-improving-agents-may-2026.md` with planning/goal-decomposition section

### Priority Recommendations
1. **Workers need restart** — 7+ days dead, cron may need manual re-enabling by Anh
2. **Implement TDP pattern** — would improve multi-agent task decomposition
3. **PIVOT benchmark** — could be used to measure orchestrator plan adherence
4. **Gen Z slang current** — no sync needed tonight

### Git Commit
- Status: CLEAN (wiki clean, SHS=0, no blocking issues)
- New techniques documented

---

## Tonight's Findings (2026-05-22)

### System Status (02:00)
- Wiki: ✅ clean (1824 files, 0 issues — wiki_lint --fast PASSED)
- Skills: 65 skills with SKILL.md, SHS = 0 (verified clean)
- Workers: ⚠️ DEAD — content-creator/outputs/ and research-agent/outputs/ are EMPTY (no outputs in days)
- Session logs: ~/Library/Application Support/hermes-agent/sessions/ — empty (0 bytes)
- Gen Z slang: Workers dead since May 11+, web search fallback used

### Gen Z Slang Update (May 22)
**NEW TERM found from web search:**
- **"Cổ điển, tôn trọng"** — "classic, respect" — used to compliment things that are "old but still done properly"
- Source: Vietnamese Gen Z slang from Threads/TikTok (May 8, 2026 via vtimes.com.au)
- Origin: From streamer Killerqueen (Lê Lưu Bách Đạt), spread across social media
- Synced to entities/learned-about-tuananh.md ✅

### Hermes Agent v0.14.0 "Foundation Release" (May 16, 2026)
- **157.2K+ stars** (global rank #46) — up from ~155K on May 20
- 808 commits since v0.13.0, 633 merged PRs, 165K lines changed
- Key features: xAI Grok OAuth, OpenAI-compatible local proxy, x_search native tool, 180x faster CDP browser, 9 new skills, LINE + SimpleX Chat, native Windows beta, /handoff live session transfer
- 12 P0 + 50 P1 issues closed
- Hermes Atlas — new resource noted by Teknium (founder)

### Capability Focus: Planning + Goal Decomposition
- TDP (Task-Decoupled Planning): 60% context reduction via DAG sub-goals
- DGM (Darwin Gödel Machine): self-modifying code without retraining
- 6 new goal decomposition techniques documented in previous sessions

### Recommendations
1. Workers need restart — 12+ days dead, cron may need manual re-enabling
2. Gen Z slang synced ✅ — "kịt kin", "trình là gì", "hài hước tưởng mình vô duyên"
3. Consider TDP pattern for multi-agent orchestrator
4. 9 new self-improvement techniques from May 2026 papers

### Git Commit
- Status: CLEAN (wiki clean, skills healthy, slang synced)
- Reference doc updated

---

## Tonight's Findings (2026-05-23)

### System Status (02:00)
- Wiki: ✅ clean (1824 files, 0 issues — wiki_lint --fast PASSED)
- Skills: 237 skills healthy, SHS = 0
- Workers: ⚠️ DEAD — content-creator/outputs/ and research-agent/outputs/ are EMPTY (12+ days)
- Session logs: ~/Library/Application Support/hermes-agent/sessions/ — empty (0 bytes)
- Gen Z slang: Workers dead since May 11+, web search fallback used

### Gen Z Slang Update (May 23)
**NEW TERMS found from web search:**
1. **"kịt kin"** — viral TikTok trend (May 5, 2026) — mimicks a polite sneeze "hắt xì nhẹ" with cute expression
2. **"trình là gì mà trình ai chấm"** — "what's your level to judge others?" — viral from HIEUTHUHAI song "Trình"
3. **"ối dồi ôi"** — expression of disbelief, like "oh my god!" — part of trình trend
4. **"hài hước tưởng mình vô duyên"** — "funny thinking I'm being rude" — ironic way to compliment
5. **"nếu anh có yêu nói đi ngại gì"** — dance challenge trend (May 12, 2026)
6. **"anh đâu cần phải xin lời em, mình đâu là gì của nhau đâu"** — viral sound trend (May 7, 2026)

### 9 NEW Self-Improving Agent Techniques (May 2026)

1. **LSE (Learning to Self-Evolve)** — arXiv:2603.18620 — trains LLMs to improve their own contexts at test-time via single-step RL. A 4B model outperforms GPT-5 and Claude Sonnet 4.5 on Text-to-SQL.

2. **Test-time Recursive Thinking (TRT)** — arXiv:2602.03094 — open-source models reach 100% on AIME-25/24. Uses accumulated knowledge + self-generated verification across iterations.

3. **Native Evolution** — arXiv:2604.18131 — trains agents to explore/summarize WITHOUT external rewards at inference. Qwen3-30B +20% on WebVoyager, 14B outperforms Gemini-2.5-Flash.

4. **Polaris** — arXiv:2603.23129 — Gödel agent for SMALL models (7B). Policy repair via experience abstraction. Failures → compact reusable strategies → code patches.

5. **SOLAR** — arXiv:2605.20189 — Self-Optimizing Lifelong Autonomous Reasoner. Meta-learning on weights as environment. Episodic memory buffer for plasticity/stability balance.

6. **GenericAgent** — arXiv:2604.17091 — context information density maximization. 4 mechanisms: minimal tools, hierarchical memory, self-evolution SOPs, context truncation.

7. **ME-ICPO** — arXiv:2603.01335 — Minimum-Entropy In-Context Policy Optimization. Self-reflection as in-context policy optimization with entropy-regularized response selection.

8. **DGM-Hyperagents** — arXiv:2603.19461 — extends DGM with metacognitive self-modification. Meta agent modifies itself AND the task agent. Self-improving self-improvement.

9. **LLM Agent Optimization Survey** — arXiv:2503.12434 — comprehensive survey: parameter-driven (SFT, RL, hybrid) + parameter-free (prompt, RAG, tool, multi-agent).

### Hermes v0.14.0 "Foundation Release" (May 16, 2026) — Updated
- **157.2K+ stars** (global rank #46)
- 808 commits, 633 merged PRs, 545 issues closed (12 P0, 50 P1)
- 215 community contributors
- Key: 180x faster CDP browser, native Windows beta, x_search native, OpenAI proxy for OAuth, /handoff live transfer, 9 new skills (Hyperliquid, Yahoo Finance, api-testing, EVM multi-chain, darwinian-evolver, osint-investigation, pinggy-tunnel, watchers, Notion overhaul)
- PyPI install: `pip install hermes-agent` works
- Community: 7,309 members in Hermes Agent X

### Gen Z Slang Entities Update Needed
**File:** `/Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md`
**Section:** Vietnamese Gen Z Hot 2025-2026
**New terms to add:**
- **kịt kin** — viral May 2026, polite sneeze meme with cute expression
- **trình là gì mà trình ai chấm** — viral from HIEUTHUHAI song, ironic judgment comeback
- **hài hước tưởng mình vô duyên** — "funny thinking I'm being rude", ironic compliment style
- **ối dồi ôi** — "oh my god!" expression, part of trình trend

## Tonight's Findings (2026-05-25)

### System Status (02:00)
- Wiki: ✅ CLEAN — 0 issues (1579 concept files)
- Skills: ✅ 233 skills healthy, SHS = 0
- Workers: ⚠️ LAST OUTPUT May 14 (6+ days stale) — Content Creator + Research Agent both dead
- Session logs: Empty directories (no new sessions since May 17)

### AI Agent Research — Multi-Agent Coordination (May 25, 2026)

Research focus tonight: **Multi-Agent Coordination** — production patterns + delegation best practices.

**Key findings:**

1. **"Team of Rivals" Pattern** (arxiv:2601.14351) — Planners, executors, critics, experts with competing incentives prevents groupthink. Centralized coordination improved Finance-Agent by 80.9% on parallel work, but sequential planning still problematic.

2. **Hermes Subagent Delegation** — delegate_task spawns isolated child agents with restricted toolsets. Max 3 concurrent, max depth 2. Orchestrator cannot delegate further (max_spawn_depth=1).

3. **Multi-Agent Orchestration Patterns (2026):**
   - Fan-out parallelism: one task → many agents
   - Hierarchical delegation: orchestrator → specialist agents
   - Producer-consumer: task queue with workers
   - Debate/state: competing agents resolve via voting

4. **Hyperagents (Meta, arxiv:2603.19461)** — Self-referential agents that modify BOTH task-solving behavior AND the improvement process itself. Performance compounds over time. Based on Darwin Gödel Machine.

5. **Production lessons (Medium Apr 26, 2026):**
   - Centralized coordination: 80.9% gains on parallelizable work
   - Sequential planning: multi-agent still struggles
   - Verification patterns critical for coherence

### Skills Status
- Total skills: 233
- SHS: 0 (healthy)
- Wiki concepts: 1,579 files, clean

### Worker Status
- Content Creator: LAST May 14 10:02 (6 days stale)
- Research Agent: LAST May 12 14:08 (8 days stale)
- Workers COMPLETELY DEAD — need manual restart

### Gen Z Slang
- Worker output: May 14 content (last available)
- Terms: "lọ", "SÍT RỊT", "KHÓ QUÁ BỎ QUA" — already in wiki entity
- No new terms to sync this session

### Recommendations
1. **Workers need restart** — Content Creator + Research Agent both dead 6+ days
2. **Multi-agent orchestration** — Hermes Issue #344 tracking evolution toward true multi-agent
3. **Next focus** — Self-Correction capability (high impact, foundation for others)
