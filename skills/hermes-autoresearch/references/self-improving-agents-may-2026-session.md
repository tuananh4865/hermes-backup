# Self-Improving Agents — May 2026 Research Summary

## Session: 2026-05-23 (Autoresearch Nightly)

## Key Techniques Documented

### 1. SICA (Self-Improving Coding Agent)
- **Source:** arXiv:2504.15228
- **What it does:** Agent edits its own scaffolding code for self-improvement
- **Metric:** 17% → 53% on SWE-Bench Verified
- **Type:** Non-gradient-based, data-efficient
- **Hermes applicability:** HIGH — self-patching gateway hooks

### 2. ERL (Experiential Reflective Learning)
- **Source:** arXiv:2603.24639
- **What it does:** Reflects on task trajectories → generates transferable heuristics
- **Metric:** +7.8% on Gaia2 benchmark over ReAct baseline
- **Key insight:** Selective retrieval essential, heuristics > few-shot prompting
- **Hermes applicability:** HIGH — heuristic memory for session continuity

### 3. DGM-Hyperagents
- **Source:** arXiv:2603.19461
- **What it does:** Meta-level self-modification — meta agent modifies itself AND the task agent
- **Type:** Self-improving self-improvement
- **Hermes applicability:** MEDIUM — foundation for autonomous capability growth

## Paradigm Shift (May 2026)

Self-improvement techniques now unify under **ERL pattern**:
- experience → heuristic memory → selective retrieval
- From: external feedback → self-generated verification
- From: response-level → policy-level changes
- From: single agent → multi-agent diagnosis teams

## Hermes Version Status (2026-05-23)

- **Latest:** v0.14.0 "Foundation Release" (May 16, 2026)
- **Stars:** 157.2K+ (global rank #46)
- **v0.15:** NOT released yet — searches confirm v0.14 still latest
- **Security:** CVE-2026-7396 affects v0.8.0 (file gateway) — update if using v0.8.x

## Related Reference Files
- `references/self-improving-agents-may-2026.md` — 12 techniques (May 13)
- `references/self-debugging-techniques-may-2026.md` — 7 techniques (May 17)
- `references/dgm-darwin-godel-machine-2026-05-22.md` — DGM details