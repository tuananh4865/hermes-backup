# Memory Optimization for AI Agents — May 2026 Research

> Captured from arXiv research May 10, 2026. Part of Hermes Autoresearch knowledge base.
> Related: `references/self-improving-agents-may-2026.md` (reflective/self-improvement techniques)

## 8 New Techniques (arXiv, Jan-Apr 2026)

### 1. DeltaMem
- **Paper:** arXiv:2604.01560 (Apr 2026)
- **What it does:** RL-trained agentic memory management. Formulates memory updating as end-to-end task.
- **Key innovation:** Novel "Memory-based Levenshtein Distance" reward — measures edit distance between memory states
- **Note:** Training-free version already outperforms baselines
- **Benchmark:** LoCoMo, HaluMem, PersonaMem

### 2. Unified Memory Agent (UMA)
- **Paper:** arXiv:2602.18493 (Feb 2026)
- **What it does:** End-to-end RL framework unifying memory operations + QA
- **Architecture:** Dual memory — compact core summary (global) + Memory Bank (explicit CRUD over key-value entries)
- **Benchmark:** Ledger-QA (continuous state tracking), 13 datasets
- **Key insight:** Joint optimization outperforms decoupled 2-stage (66.29% → 76.46%)
- **Note:** Proactive consolidation during streaming, not passive retrieval

### 3. Knowledge Access > Model Size
- **Paper:** arXiv:2603.23013 (Mar 2026)
- **What it does:** Memory-augmented inference for persistent agents
- **Key finding:** 8B model + memory = 69% of 235B model performance at 4% cost
- **Statistics:** Up to 47% of user queries are semantically similar to prior interactions
- **Routing:** Memory augments routing, not replaces it. Hybrid retrieval (BM25 + cosine) +7.7 F1
- **Implication:** For Hermes — memory optimization > model scale

### 4. LatentMem
- **Paper:** arXiv:2602.03036 (Feb 2026)
- **What it does:** Learnable multi-agent memory framework with role-aware customization
- **Architecture:**
  - Experience bank — stores raw interaction trajectories (lightweight)
  - Memory composer — synthesizes compact latent memories conditioned on agent context
- **Training:** Latent Memory Policy Optimization (LMPO) — propagates task-level signals through latent memories
- **Results:** 50% fewer tokens, 2x inference speed, up to +19.36% over vanilla
- **Solves:** Memory homogenization (all agents same memory) + information overload

### 5. AtomMem
- **Paper:** arXiv:2601.08323 (Jan 2026)
- **What it does:** Reframes memory management as CRUD decision-making problem
- **Training:** SFT + RL (not heuristics)
- **Key insight:** Learned policy INCREASES Create/Update/Delete, DECREASES Read over time
- **Benchmark:** HotpotQA, 2WikiMultihopQA, Musique — 8B outperforms static memory workflows
- **Implication:** For QA tasks, proactive revision > passive retrieval

### 6. MemReader
- **Paper:** arXiv:2604.07877 (Apr 2026)
- **What it does:** Active memory extraction with ReAct paradigm
- **Variants:**
  - MemReader-0.6B — distilled passive extractor (cost-efficient)
  - MemReader-4B — active extractor with GRPO
- **Process:** Think → Act (write/retrieve/buffer/discard) → Observe
- **Benchmark:** LOCOMO, LongMemEval, HaluMem — state-of-the-art
- **Key:** Explicit reasoning about information value BEFORE writing

### 7. Agentic Memory / AgeMem
- **Paper:** arXiv:2601.01885 (Jan 2026)
- **What it does:** Unified LTM + STM management as tool-based actions
- **5 memory ops:** store, retrieve, update, summarize, discard — all callable tools
- **Training:** 3-stage progressive GRPO (warmup → LTM → STM coordination)
- **Benchmark:** 5 long-horizon benchmarks — outperforms all baselines
- **Key behaviors discovered by learned policy:**
  - Proactively summarize BEFORE context fills (not after)
  - Selectively discard semantically similar entries that add no new info

### 8. OCR-Agent
- **Paper:** arXiv:2602.21053 (Feb 2026)
- **What it does:** Capability Reflection + Memory Reflection for VLM self-correction
- **Mechanisms:**
  - Capability Reflection — diagnose errors, generate correction plan, filter capability hallucinations
  - Memory Reflection — avoid repetitive attempts, leverage historical reasoning traces
- **Result:** +2.0 on InternVL3-8B English, +1.2 Chinese subsets
- **Key insight:** Memory Reflection prevents "refinement stagnation" and "ineffective looping"

---

## Key Insights Summary

| Theme | Insight |
|-------|---------|
| **Heuristics → Learned** | Memory optimization shifting from rules to RL/SFT |
| **CRUD as interface** | CRUD operations becoming standard memory API |
| **Unified > Separate** | Joint LTM+STM optimization outperforms separate systems |
| **Active > Passive** | Proactive consolidation beats reactive retrieval |
| **Memory > Model** | 8B+memory beats 235B for repetitive queries at 4% cost |

## Hermes Relevance

- **AtomMem CRUD pattern** — could implement memory as explicit CRUD decisions in WikiMemoryProvider
- **AgeMem 3-stage GRPO** — relevant for training memory management policy for Hermes
- **DeltaMem Levenshtein reward** — could measure memory state transitions for Hermes session continuity
- **MemReader active extraction** — could improve what gets written to MEMORY.md vs discarded
- **UMA proactive consolidation** — could replace Hermes reactive context compression

## Sources
- arXiv:2604.01560 — DeltaMem (Apr 2026)
- arXiv:2602.18493 — UMA (Feb 2026)
- arXiv:2603.23013 — Knowledge Access (Mar 2026)
- arXiv:2602.03036 — LatentMem (Feb 2026)
- arXiv:2601.08323 — AtomMem (Jan 2026)
- arXiv:2604.07877 — MemReader (Apr 2026)
- arXiv:2601.01885 — AgeMem (Jan 2026)
- arXiv:2602.21053 — OCR-Agent (Feb 2026)
