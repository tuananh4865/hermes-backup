# Self-Improving AI Agents — May 2026 Research

> Captured from arXiv research May 9, 2026. Part of Hermes Autoresearch knowledge base.
> Previous: `references/self-improving-agents-2026.md` (older techniques)

## 10 New Techniques (arXiv, Mar-Apr 2026)

### 1. Experiential Reflective Learning (ERL)
- **Paper:** arXiv:2603.24639 (Mar 2026)
- **What it does:** Reflects on task trajectories + outcomes to generate transferable heuristics
- **Key insight:** Selective retrieval is essential — not all past experiences are useful
- **Benchmark:** Gaia2 — +7.8% over ReAct baseline
- **Heuristics > few-shot prompting** for transfer across tasks

### 2. In-Context Policy Optimization (ICPO)
- **Paper:** arXiv:2603.01335 (Mar 2026)
- **What it does:** Test-time scaling via multi-round self-reflection
- **ME-ICPO:** Minimum-entropy selection for robust self-assessed rewards
- **Key insight:** Single-layer linear self-attention can provably imitate policy optimization
- **Use case:** Mathematical reasoning tasks, inference-time improvement

### 3. Trajectory-Informed Memory Generation
- **Paper:** arXiv:2603.10600 (Mar 2026)
- **4-component pipeline:**
  1. Trajectory Intelligence Extractor — semantic analysis of reasoning patterns
  2. Decision Attribution Analyzer — which decisions led to failures/recoveries
  3. Contextual Learning Generator — strategy tips, recovery tips, optimization tips
  4. Adaptive Memory Retrieval — injects relevant learnings based on multi-dimensional similarity
- **Benchmark:** AppWorld — +14.3pp goal completion, +28.5pp on complex tasks (149% relative increase)
- **Key insight:** Unlike generic memory, this captures execution patterns, not just conversational facts

### 4. Hyperagents (Meta)
- **Paper:** arXiv:2603.19461 (Mar 2026)
- **What it does:** Integrates task agent + meta agent (both editable in same program)
- **Key innovation:** Metacognitive self-modification — the improvement procedure itself can evolve
- **DGM-H** outperforms DGM across coding, paper review, robotics reward design, math grading
- **Key insight:** Meta-level modification procedure is itself editable → self-accelerating progress
- **Safety:** Sandboxing + human oversight; transfer hyperagents acquire persistent memory + performance tracking

### 5. MARS (Metacognitive Agent Reflective Self-improvement)
- **Paper:** arXiv:2601.11974 (Jan 2026)
- **What it does:** Principle-based (normative rules) + procedural (step-by-step strategies) reflection in SINGLE recurrence cycle
- **Key insight:** Mimics human learning — abstract principles + procedural strategies
- **Benchmark:** 6 benchmarks, outperforms SOTA with reduced compute
- **Efficiency:** Single cycle vs multi-turn recursive loops (other methods)

### 6. RetroAgent
- **Paper:** arXiv:2603.08561 (Mar 2026)
- **What it does:** Hindsight self-reflection with dual intrinsic feedback:
  1. Intrinsic numerical feedback — tracks subtask completion relative to prior attempts
  2. Intrinsic language feedback — distills reusable lessons into memory buffer
- **Retrieval:** SimUtil-UCB strategy balancing relevance, utility, exploration
- **Benchmark comparisons vs GRPO-trained agents:**
  - +18.3% ALFWorld
  - +15.4% WebShop
  - +27.1% Sokoban
  - +8.9% MineSweeper

### 7. Group-Evolving Agents (GEA)
- **Paper:** arXiv:2602.04837 (Feb 2026)
- **What it does:** Group-centric evolution (not individual agents)
- **Key innovation:** Experience sharing within group → sustained cumulative progress
- **vs tree-based evolution:** Individual isolation prevents effective information sharing
- **Benchmark:** SWE-bench 71.0% vs 56.7% baseline; Polyglot 88.3% vs 68.3%
- **Bug fixing:** Framework-level bugs fixed in 1.4 iterations avg (vs 5 for tree-based)
- **Key insight:** Diversity from exploration → transient variations → long-term useful experience

### 8. POLARIS
- **Paper:** arXiv:2603.23129 (Mar 2026)
- **What it does:** Recursive self-improvement for SMALL models via experience abstraction
- **Cycle:** Failures → analysis → strategy synthesis → patch generation → patch integration
- **Key features:**
  - Bounded retries + conservative checks
  - Traceable memory (limited context growth)
  - Compact reusable repair strategies as minimal code patches
- **Key insight:** Works on smaller models (unlike DGM which needs large capacity)

### 9. Self-Optimizing Multi-Agent for Deep Research
- **Paper:** arXiv:2604.02988 (Apr 2026)
- **What it does:** Multi-agent Deep Research system self-plays different prompt combinations
- **Key insight:** Enables agents to optimize prompts autonomously — matches/exceeds expert-crafted prompts
- **Architecture:** Orchestrator + parallel worker agents for planning, retrieval, synthesis
- **Current limitation:** Relies on hand-engineered prompts and static architectures

### 10. Hierarchical Self-Evolving Multi-Agent
- **Paper:** arXiv:2601.11658 (Jan 2026)
- **Architecture:** Base LLM + SLM agent + Code-Gen LLM + Teacher-LLM
- **Escalation path:** Reasoning → tool synthesis → evolution (CL/RL/GA)
- **Evolution methods:**
  - CL (Curriculum Learning) = fast recovery, strong generalization
  - RL (Reward-Based) = excels on high-difficulty tasks
  - GA (Genetic Algorithm) = high behavioral diversity
- **Dataset:** TaskCraft (hierarchical tasks, tool-use traces, difficulty scaling)

---

## Key Insight: Evolution of Self-Improvement

| Generation | Approach | Limitation |
|------------|---------|------------|
| Gen 1 | Single-agent reflection | No experience transfer |
| Gen 2 | Multi-agent reflexion | Still isolated learning |
| Gen 3 | Group evolution | Shared experience, sustained progress |
| Gen 4 | Hierarchical metacognition | Different components for different tasks |
| Gen 5 | Hyperagents | Meta-level itself mutable |

**Trend:** Self-improvement is moving from single-agent reflection → multi-agent collaboration + group evolution + hierarchical metacognition + self-referential modification.

## Hermes Relevance

- **Trajectory Memory pattern** could improve Hermes session continuity (on_session_end)
- **Group Evolution** pattern could apply to Felix Model workers sharing learnings
- **MARS single-cycle reflection** could make Hermes self-correction faster
- **POLARIS** approach (small-model self-improvement) fits Hermes local-first architecture

## Sources
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
