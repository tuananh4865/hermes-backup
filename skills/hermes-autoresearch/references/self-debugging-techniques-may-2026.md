# Self-Debugging Techniques — May 2026

**Research date:** 2026-05-19
**Source:** arXiv papers + Exa search
**Status:** 6 new techniques documented

## Paradigm Shift

Self-debugging moving from:
- **Response-level** (retry, regenerate) → **Policy-level** (learn to debug itself)
- **External feedback** (human/tool critique) → **Self-generated verification** (self-critique)
- **Single agent** → **Multi-agent diagnosis teams**

---

## 6 NEW Self-Debugging Techniques

### 1. DebugRepair (arXiv:2604.19305)

**Key innovation:** Runtime evidence + simulated instrumentation → patch refinement

**Components:**
- Test semantic purification — cleaner test signals
- Simulated instrumentation — trace without real execution
- Debugging-driven conversational repair — patch via dialogue

**For Hermes:** Could implement a self-repair loop that uses execution traces to refine its own fixes.

---

### 2. ReflexiCoder (arXiv:2603.05863)

**Key innovation:** RL-zero trains model to internalize "how to debug"

**Approach:**
- Reinforcement learning from zero — no labeled debugging data
- Policy learns debugging as a skill, not just task completion
- Internalizes error patterns

**For Hermes:** Would need RL training pipeline to teach debugging policy.

---

### 3. Polaris (arXiv:2603.23129)

**Key innovation:** Gödel agent — policy-level changes persist across sessions

**Key findings:**
- 7B model competitive with larger models when usingPolaris approach
- Self-correction at policy level beats response-level retry
- Persistent fix memory — fixes carry forward

**For Hermes:** `on_pre_compress()` checkpoint should save debugging fixes to a persistent memory layer.

---

### 4. ErrorProbe (arXiv:2604.17658)

**Key innovation:** 3-agent team for failure attribution

**Architecture:**
- **Strategist** — plans diagnostic approach
- **Investigator** — executes probes, gathers evidence
- **Arbiter** — evaluates evidence, attributes failure cause

**For Hermes:** When self-correction fails 3x, spawn ErrorProbe team to diagnose.

---

### 5. TraceCoder (arXiv:2602.06875)

**Key innovation:** Diagnostic probes + causal analysis + learn from past failures

**Approach:**
- Insert instrumentation hooks to trace execution
- Causal analysis of failure propagation
- Learn from historical debug sessions

**For Hermes:** Add tracing to Hermes gateway for autonomous debugging.

---

### 6. Debug2Fix (arXiv:2602.18571)

**Key innovation:** Integrates debuggers into agent subagent architecture

**Approach:**
- Debugger as first-class subagent
- Can inspect memory, call stack, variables
- Fix generation with debugger context

**For Hermes:** Could integrate Python debugger as a tool for self-debugging.

---

## Summary Table

| Technique | arXiv | Key Innovation | Hermes Applicability |
|-----------|-------|---------------|---------------------|
| DebugRepair | 2604.19305 | Runtime evidence + simulated instrumentation | Self-repair loop |
| ReflexiCoder | 2603.05863 | RL-zero for debugging policy | RL training pipeline |
| Polaris | 2603.23129 | Policy-level persistence | Persistent debug memory |
| ErrorProbe | 2604.17658 | 3-agent diagnosis team | Multi-agent failure diagnosis |
| TraceCoder | 2602.06875 | Diagnostic probes + causal analysis | Gateway instrumentation |
| Debug2Fix | 2602.18571 | Debugger as subagent | Debugger tool integration |

---

## Next Steps

1. **ErrorProbe pattern** — implement 3-agent diagnosis for complex failures
2. **TraceCoder approach** — add instrumentation to Hermes gateway
3. **Polaris approach** — persistent debugging memory layer