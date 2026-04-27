---
title: "Hermes Dojo Agentic System"
created: 2026-04-23
updated: 2026-04-23
type: concept
tags: [AI Agent, Workflow Design, Self-Evolving System, Memory Management, Python]
---

# Hermes Dojo Agentic System

## Summary
Hermes Dojo is a self-evolving wiki agentic system designed to be proactive and project-aware. Its core objective is to eliminate infinite cascade loops in development by enforcing strict workflows (Research → Plan → Implement) and utilizing a patch-only skill update mechanism. The system employs a multi-tiered memory structure and relies on automated hooks for event-driven maintenance and learning.

## Key Insights
- **R→P→I Workflow:** All tasks within the system follow a mandatory Research, Plan, Implement cycle, ensuring tasks are fully understood and verified before execution, minimizing errors and cascading failures.
- **Patch-Only Principle:** The system enforces strict skill updates where only changed portions are patched, preserving existing working code and ensuring stability during self-improvement cycles.
- **4-Tier Memory System:** Knowledge retention is managed through a hierarchical memory structure (session, episodic, semantic, procedural), allowing the agent to maintain short-term context while building long-term, cross-session knowledge graphs.

## Analysis
The architecture of Hermes Dojo is built around iterative development and rigorous quality assurance. The project follows a strict waterfall methodology where each phase must pass QA before proceeding, establishing a foundation of reliability. This structure begins with Phase 0 (Skeleton) and progresses through behavioral skills (Phase 1), process engine implementation (Phase 2), dependency tracking (Phase 3), memory lifecycle management (Phase 4), and finally, automation hooks (Phase 6).

The core functionality relies heavily on specialized scripts and skills. For instance, the `knowledge_graph.py` script was critical in fixing a database path bug, demonstrating that the system is designed not just for execution but also for self-correction and debugging. The use of dedicated entity extraction and confidence scoring skills further enhances the agent's ability to process raw data and make informed decisions.

The most significant architectural decision is the implementation of the patch-only rule combined with the R→P→I workflow. This combination ensures that the system can continuously improve its capabilities (self-evolving) without introducing instability, directly addressing the risk of "breaking B" when fixing "A." Phase 6, focusing on event-driven automation through `wiki_hooks.py`, completes the loop by enabling proactive maintenance and learning based on session events (`on_ingest`, `on_session_end`), making the entire system truly autonomous.

## Related
- [[Agent Frameworks]]
- [[Knowledge Graphs in AI]]
- [[R→P→I Methodology]]
- [[Memory Systems Design]]