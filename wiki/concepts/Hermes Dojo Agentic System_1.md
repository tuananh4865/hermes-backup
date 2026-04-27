---
title: "Hermes Dojo Agentic System"
created: 2026-04-23
updated: 2026-04-23
type: concept
tags: [agentic system, workflow, self-improvement, knowledge graph]
---

# Hermes Dojo Agentic System

## Summary
Hermes Dojo is a comprehensive, self-evolving wiki agentic system designed to operate proactively and autonomously. Its core objective is to eliminate infinite cascade loops in development by enforcing a strict Research → Plan → Implement (R→P→I) workflow and utilizing a patch-only skill update protocol. The system employs a multi-tiered memory structure and a knowledge graph to ensure continuous self-awareness and project fidelity.

## Key Insights
- **Patch-Only Protocol:** The system strictly adheres to a "patch-only" rule for skill updates, ensuring that existing working components are never overwritten, thereby minimizing risk during development.
- **R→P→I Workflow:** All tasks follow a mandatory Research (Understand), Plan (Define Steps), and Implement (Execute) sequence, which is fundamental to dependency tracking and preventing cascading failures.
- **Phased QA Enforcement:** The entire project was developed using a strict waterfall methodology where each phase must pass Quality Assurance (QA) before proceeding, establishing a robust quality gate for the agentic system itself.

## Analysis
The development of Hermes Dojo focused on creating an agent that is not only task-oriented but also self-aware and capable of self-improvement. This was achieved by segmenting the development into six distinct phases, each building upon the last—from initial skeleton creation (Phase 0) to full knowledge graph implementation (Phase 5). This phased approach allowed for rigorous testing and validation at every step, which is critical when building complex, interconnected systems where failure in one area can trigger widespread instability.

A central architectural decision was the implementation of a four-tier memory system (session, episodic, semantic, procedural) to ensure the agent maintains context across different interactions and sessions. Furthermore, the integration of specialized scripts and skills, such as `dependency_tracker.py` and `knowledge_graph.py`, transforms the system from a simple executor into a proactive entity capable of monitoring its own state and dependencies. This shift allows the agent to identify potential issues (like dependency conflicts) before they become critical failures.

The core philosophy governing all operations is the constraint-based approach: prioritizing stability and controlled evolution over rapid, unverified changes. By enforcing the R→P→I workflow and the patch-only rule, Hermes Dojo ensures that self-improvement mechanisms (`skill-self-improve`, `mistake-logging`) are contained and predictable. This design minimizes the risk of "infinite cascade loops," allowing the agent to evolve its capabilities systematically rather than chaotically.

## Related
- [[Agentic Systems]]
- [[Workflow Design Patterns (RPI)]
- [[Knowledge Graphs in AI]]
- [[Wiki Maintenance Strategies]]