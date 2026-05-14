# Self-Improving AI Agents — May 2026 Research

> Autoresearch 2026-05-13 | Focus: Self-Improving Agents + RL-based Memory

## 12 NEW Techniques Documented

### 1. ERL (Experiential Reflective Learning)
- Reflects on task trajectories to generate reusable heuristics
- Selective retrieval critical for performance
- +7.8% on Gaia2 vs ReAct baseline
- Source: arXiv:2603.24639

### 2. Polaris (Gödel Agent for Small LMs)
- Policy-level self-repair via experience abstraction
- 7B model achieves consistent gains via auditable patches
- MGSM, DROP, GPQA, LitBench benchmarks
- Source: arXiv:2603.23129

### 3. Self-Consolidation for Self-Evolving Agents
- Contrastive reflection to summarize error-prone patterns
- Self-consolidation distills textual experience into latent space
- Addresses failure learning + context window exhaustion
- Source: arXiv:2602.01966

### 4. ReflexiCoder (Self-Debugging via RL)
- Internalizes self-reflection + self-correction into model weights
- RL-zero training paradigm, no external oracles needed
- Optimizes entire reflection-correction trajectory
- Source: arXiv:2603.05863

### 5. RetroAgent (Retrospective Dual Intrinsic Feedback)
- Hindsight self-reflection with dual feedback: numerical + language
- SimUtil-UCB retrieval strategy balancing relevance/utility/exploration
- +18.3% ALFWorld, +15.4% WebShop, +27.1% Sokoban vs GRPO
- Source: arXiv:2603.08561

### 6. MARS (Metacognitive Agent Reflective Self-improvement)
- Single recurrence cycle self-improvement
- Principle-based (what to avoid) + procedural (how to succeed)
- 6 benchmarks, reduced computational overhead
- Source: arXiv:2601.11974

### 7. AEL (Agent Evolving Learning)
- Two-timescale: Thompson Sampling bandit (fast) + LLM reflection (slow)
- Memory + reflection = 58% improvement over stateless
- Key insight: self-diagnosis is bottleneck, not experience accumulation
- Sharpe 2.13 on portfolio benchmark
- Source: arXiv:2604.21725

### 8. DeepVerifier (Test-Time Verification Scaling)
- Self-evolving via rubric-guided verification
- 5 failure categories, 13 sub-categories in DRA Failure Taxonomy
- +8-11% on GAIA, +3-6% on XBench-DeepResearch
- Source: arXiv:2601.15808

### 9. ICPO (In-Context Policy Optimization)
- Test-time scaling via multi-round self-reflection
- ME-ICPO: minimum-entropy response selection for robust self-assessment
- Source: arXiv:2603.01335

### 10. MemPO (Self-Memory Policy Optimization)
- Agent autonomously summarizes + manages own memory
- 25.98% F1 gain, 67.58% token reduction
- Long-horizon agents with 3 actions: reason, invoke tool, memorize
- Source: arXiv:2603.00680

### 11. EMPO² (Exploratory Memory-Augmented On-/Off-Policy)
- Hybrid RL combining on- and off-policy updates
- 128.6% improvement over GRPO on ScienceWorld
- Superior OOD adaptation
- Source: arXiv:2602.23008

### 12. MCMA (Meta-Cognitive Memory Abstraction)
- Memory abstraction as learnable cognitive skill
- Memory Copilot trained via DPO
- +25.07% ALFWorld, +7.92% ScienceWorld
- Source: arXiv:2601.07470

### 13. LSE (Learning to Self-Evolve)
- RL framework trains LLMs to improve their own contexts at test time
- Tree-guided evolution loop for multi-round refinement
- 4B model outperforms GPT-5/Claude Sonnet 4.5 on Text-to-SQL (BIRD) + MMLU-Redux
- Source: arXiv:2603.18620

### 14. HyperAgents / DGM-H (Darwin Gödel Machine — Hyperagents)
- Metacognitive self-modification: meta agent modifies BOTH task agent AND itself
- Eliminates domain-specific alignment assumption of original DGM
- Improves across: coding, paper review, robotics reward design, Olympiad math grading
- Key: meta-level modification procedure is itself editable → can improve how it generates improvements
- Source: arXiv:2603.19461

### 15. Self-Guide (Co-Evolving Internal Reward + Policy)
- Agent generates self-guidance signal at inference → converts to step-level reward for training
- Co-evolving loop: better policy → better guidance → better reward → better policy
- GRPO co-evolution: +8% over environment reward-only baselines
- Stage-wise trust schedule stabilizes co-evolution
- Source: arXiv:2604.03098

## Key Insights

1. **Self-improvement paradigm shift**: From heuristic-based → RL-trained policies
2. **Self-diagnosis bottleneck**: Memory + reflection together produce 58% improvement; every additional mechanism degrades (AEL finding)
3. **Failure learning**: Contrastive reflection captures error-prone patterns (Self-Consolidation)
4. **Single-cycle improvement**: MARS achieves in 1 cycle what others need multi-turn loops
5. **Memory operations as tools**: CRUD operations becoming standard callable actions trained via GRPO/PPO
6. **Metacognitive self-modification**: HyperAgents shows meta-level procedure is itself editable — can improve how it generates future improvements (not just task performance)
7. **Co-evolving rewards**: Self-Guide demonstrates policy + internal reward can co-evolve — better policy → better guidance → stronger reward → better policy

## Sources
- arXiv:2603.24639 — ERL (Mar 2026)
- arXiv:2603.23129 — Polaris (Mar 2026)
- arXiv:2602.01966 — Self-Consolidation (Feb 2026)
- arXiv:2603.05863 — ReflexiCoder (Mar 2026)
- arXiv:2603.08561 — RetroAgent (Mar 2026)
- arXiv:2601.11974 — MARS (Jan 2026)
- arXiv:2604.21725 — AEL (Apr 2026)
- arXiv:2601.15808 — DeepVerifier (Jan 2026)
- arXiv:2603.01335 — ICPO (Mar 2026)
- arXiv:2603.00680 — MemPO (Mar 2026)
- arXiv:2602.23008 — EMPO² (Feb 2026)
- arXiv:2601.07470 — MCMA (Jan 2026)
