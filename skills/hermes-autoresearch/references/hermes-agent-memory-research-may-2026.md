---
title: "Autoresearch Reference — Hermes Agent Memory & Self-Improvement"
created: 2026-05-21
updated: 2026-05-21
type: concept
tags: [hermes, memory, self-improvement, research]
confidence: high
relationships: [hermes-autoresearch, hermes-agent]
---

*Session: 2026-05-21 02:00 AM | Focus: Hermes v0.14 memory issues + agent self-improvement patterns*

---

## Issue #22357: Gateway Sessions Reset Memory Nudge Counter — FIXED

**Problem:** In gateway mode (Telegram), Hermes creates a fresh AIAgent per message. `_turns_since_memory` resets to 0 each time → self-improvement review never triggers.

**4 PRs merged May 9, 2026:**
- PR #22376: `fix(agent): hydrate _turns_since_memory from history in gateway mode`
- PR #22377: `fix(agent): seed memory/skill nudge counters from history in gateway mode`
- PR #22559: `fix(run_agent): hydrate memory nudge counter from history in gateway sessions`
- PR #22774: `fix(agent): hydrate memory-nudge counters from conversation_history`

**Fix pattern:**
```python
prior_user_turns = sum(1 for msg in conversation_history if msg.get("role") == "user")
self._turns_since_memory = prior_user_turns % self._memory_nudge_interval
```

**Why this matters:** The "Self-Correction" capability for gateway-mode users was broken. This is now fixed.

---

## Issue #25833: Self-Created Skills Lack Mechanism-Level Guarantees — OPEN

**Problem:** Hermes agents are simultaneously author + executor + quality inspector of own skills. No external validation point exists.

**Failure classes:**
1. No cross-session consistency — same skill + input = different outputs
2. Self-validation problem — model writes AND judges skill correctness
3. No automated quality checks on create/edit (Issue #416 still open)

**Proposed fixes:**
- Execute new skills in isolated context before persisting
- Compare actual output against claimed behavior → tag `verified: true/false`
- Parse tool references and validate against live tool registry
- Detect `TODO`, `FIXME`, placeholder values in skill body

**Why this matters:** Skill Creation is a 16-agentic capability. Skills auto-created by Hermes may have blind spots invisible to the creating model.

---

## Trajectory-Informed Memory Generation (arXiv:2603.10600v1)

**14.3% improvement on AppWorld benchmark, 149% relative gain on complex tasks**

Four components:
1. **Trajectory Intelligence Extractor** — semantic analysis of agent reasoning patterns
2. **Decision Attribution Analyzer** — which decisions led to failures/recoveries
3. **Contextual Learning Generator** — strategy tips, recovery tips, optimization tips
4. **Adaptive Memory Retrieval** — injects relevant learnings based on multi-dimensional similarity

**Pattern:** Stores execution patterns (not conversational facts) with provenance. Matches ERL (Experiential Reflective Learning).

---

## agentmemory — Pull-Model Memory for Self-Improving Agents (May 15, DEV Community)

**New library for self-improving agents that takes deletion seriously.**

**Design principles:**
1. **No background work** — memory should NOT consolidate while agent is idle
2. **Real deletes** — "forget X" = X gone (no tombstone, no derived artifact)
3. **Pull, never push** — agent retrieves memories explicitly via API
4. **Show the trace** — every injection shows event IDs + exact prompt that produced summary

**Components:**
- `EpisodicStore`: append-only event log, real-delete API
- `OnDemandSummarizer`: pull-model context builder, returns the trace
- `MemoryDriftWatcher`: rolling-window detector for retrieval-quality drops

**Cost:** 200ms-2s cold-start latency. Exchange is auditable, reversible memory.

**Why it matters:** Current push-model (background consolidation) makes memory drift irreversible. For a system that markets self-improvement, silent drift is a trust problem.

---

## Gen Z Slang — May 21, 2026 Update

**6 new terms from slangloom.com May 2026:**
- **Căng** — serious situation, intense
- **Bóc phốt** — expose someone's drama publicly
- **Ngáo** — acting weird/clueless
- **Cà khịa** — playful teasing
- **Hóng** — waiting eagerly for news
- **Bó tay** — speechless, helpless

**Existing terms (May 18, 2026):**
- Xịn sò, Kèo, Quẩy, Tạch, Tấu hài, Hết nước chấm

---

## Hermes v0.14.0 Key Stats

| Metric | Value |
|--------|-------|
| Stars | 159K+ |
| Release Date | May 16, 2026 |
| Browser CDP calls | 180x faster |
| Messaging platforms | 22 |
| Cross-session prompt cache | 1h for Claude |
| `/handoff` | Live session transfer |

---

## Workers Status (May 21, 2026)

Workers still dead — Content Creator last output May 11, Research Agent May 12. 10+ days stale. Need restart if revenue pipeline is priority.

---

*Last updated: 2026-05-21*