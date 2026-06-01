# Self-Debugging Techniques — June 2026

## SelfHeal: Empirical Fix Pattern Analysis and Bug Repair in LLM Agents
**arXiv:2604.17699** | Oakland University | April 20, 2026

### Key Findings
- First empirical study on bug fix patterns in LLM agents
- Studied buggy posts from Stack Overflow, GitHub, HuggingFace Forums
- Created **AgentDefect** benchmark: 37 runtime buggy instances with fixed code + tests

### SelfHeal Architecture
- **Multi-agent system**: Fix Agent + Critic Agent (both ReAct-based)
- **Tools**: Internal knowledge (fix rules) + External knowledge (web search)
- **Backbone**: Gemini 3 Pro outperforms all baselines significantly
- **Key insight**: Two independent agents propose + validate fixes

### Bug Categories Found
1. Reasoning module errors
2. Memory mechanism errors  
3. Planning strategy errors
4. External tool interface errors
5. Component interaction errors

### Hermes Applicability: **HIGH**
- Fix agent = main debugging agent
- Critic agent = verification/QA agent
- Can be implemented as two subagents with different roles

---

## ErrorProbe: Self-Improving Error Diagnosis in Multi-Agent Systems
**arXiv:2604.17658** | King's College London + Amazon Alexa AI | April 19, 2026

### Key Innovation
Self-improving framework for **semantic failure attribution** — identifies which agent failed and where.

### Three-Stage Pipeline
1. **MAS Failure Taxonomy** → detect local anomalies
2. **Symptom-driven Backward Tracing** → prune irrelevant context
3. **Multi-Agent Team** (Strategist + Investigator + Arbiter) → validate error hypotheses

### Verified Episodic Memory
- Updates **only when** error patterns confirmed by executable evidence
- No expensive expert annotation needed
- Enables cross-domain transfer without retraining

### Results
- Significantly outperforms baselines on TracerTraj and Who&When benchmarks
- Step-level localization: major improvement over LLM-as-Judge
- Episodic memory prevents error pattern corruption

### Hermes Applicability: **HIGH**
- 3-agent diagnosis team pattern directly applicable
- Verified memory concept aligns with Hermes checkpoint system
- Backward tracing = Hermes error recovery pattern

---

## AutoResearchClaw: Self-Reinforcing Autonomous Research
**arXiv:2605.20025** | UNC-Chapel Hill + collaborators | May 22, 2026

### The Problem
Existing autonomous research systems:
- Rely on single-agent reasoning
- Stop when execution fails
- Don't carry experience across runs

### Five Mechanisms
1. **Structured Multi-Agent Debate** — hypothesis generation + result analysis
2. **Self-Healing Executor** — Pivot/Refine decision loop transforms failures into information
3. **Verifiable Result Reporting** — prevents fabricated numbers + hallucinated citations
4. **Human-in-the-Loop Collaboration** — 7 intervention modes (full autonomy → step-by-step)
5. **Cross-Run Evolution** — past mistakes → future safeguards

### Key Results
- **ARC-Bench**: 25-topic experiment-stage benchmark
- **AutoResearchClaw outperforms AI Scientist v2 by 54.7%**
- HITL ablation: precise targeted collaboration > full autonomy + exhaustive oversight

### Self-Healing Executor Pattern
```
FAILURE → PIVOT (try alternative) → if still fails → REFINE (reassess approach)
```
- Failures treated as **information**, not dead ends
- Partial results preserved and informative

### Hermes Applicability: **MEDIUM-HIGH**
- Self-healing executor = Hermes error recovery
- Cross-run evolution = Hermes memory/checkpoint system
- 5 mechanisms framework for autonomous research

---

## Summary Table

| Technique | arXiv | Key Metric | Hermes Applicability |
|-----------|-------|------------|---------------------|
| SelfHeal | 2604.17699 | Gemini 3 Pro beats all baselines | **HIGH** — dual-agent fix+critic |
| ErrorProbe | 2604.17658 | Step-level localization SOTA | **HIGH** — 3-agent diagnosis team |
| AutoResearchClaw | 2605.20025 | +54.7% vs AI Scientist v2 | **MEDIUM-HIGH** — 5-mechanism framework |

## Key Insight
Self-debugging paradigm has shifted:
- **Old**: External oracle tells agent what's wrong
- **New**: Internal multi-agent debate (fix + critic), failure as information, verified memory

Total self-improvement techniques documented: **28** (was 25, added SelfHeal, ErrorProbe, AutoResearchClaw)
