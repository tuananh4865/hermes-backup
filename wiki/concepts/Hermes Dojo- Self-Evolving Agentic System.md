---
title: "Hermes Dojo: Self-Evolving Agentic System"
created: 2024-05-29
updated: 2026-04-14
type: concept
tags: [AI, Agentic System, Workflow, Wiki Development]
---

# Hermes Dojo: Self-Evolving Agentic System

## Summary
Hermes Dojo is a comprehensive framework designed to build a proactive, self-aware, and self-developing wiki agentic system. Its primary goal is to eliminate infinite cascade loops in task execution by enforcing strict research, planning, and implementation workflows while utilizing a dynamic memory lifecycle and a knowledge graph. The system operates under a rigorous QA-first methodology, ensuring stability and continuous improvement through patch-only skill updates.

## Key Insights
- **R→P→I Workflow:** All tasks follow a mandatory Research → Plan → Implement sequence, ensuring thorough understanding and verification before execution.
- **Patch-Only Rule:** Skill updates are strictly limited to patching existing skills rather than full rewrites, preserving working functionality and reducing risk.
- **Multi-Tiered Memory:** The system employs a 4-tier memory structure (session, episodic, semantic, procedural) to manage context, learnings, and long-term facts effectively.

## Analysis
The development of Hermes Dojo followed a strict waterfall approach, dividing the project into six distinct phases, each requiring QA sign-off before proceeding. Phase 0 established the skeleton, followed by Phase 1 (Behavior skills), Phase 2 (Process Engine: R→P→I workflow), and Phase 3 (Dependency Tracking). These initial phases focused on creating the foundational logic and ensuring core scripts like `dependency_tracker.py` and `knowledge_graph.py` were functional.

The latter stages concentrated on advanced self-improvement mechanisms. Phase 4 implemented the Memory Lifecycle components, including skills for self-improvement (`skill-self-improve`) and mistake logging, enabling the agent to learn from errors. Phase 5 focused on Knowledge Graph implementation, allowing the system to extract entities from sources and query relationships efficiently. The successful completion of these phases demonstrated the viability of the core architecture.

The current focus is on Phase 6: Automation via Wiki Hooks. This phase involves creating an event-driven engine (`wiki_hooks.py`) that allows for automated actions upon specific events (e.g., `on_ingest`, `on_session_start`). This automation layer completes the system's loop, allowing it to proactively manage context loading, data processing, and session compression, solidifying its status as a truly self-evolving agentic system.

## Related
- [[Phase 0 Skeleton Status]]
- [[knowledge_graph.py Script Documentation]]
- [[Patch-Only Protocol Guide]]