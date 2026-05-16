---
children_hash: 1db399feadb92b653472224e57b9c31e2d2226be9562a2159f957411dd9bb4a5
compression_ratio: 0.2861736334405145
condensation_order: 2
covers: [auto_sync/_index.md, byterover_agentic_memory/_index.md, byterover_agentic_memory_skill/_index.md, byterover_checkpoint_py/_index.md, byterover_knowledge_sync_py/_index.md, fallback_mechanism/_index.md, health_check/_index.md, reviewed_skills/_index.md, skill_library_format/_index.md, skill_update_strategy/_index.md, specific_skill_content/_index.md, user_feedback_signals/_index.md, user_interaction/_index.md, worker_status_issue/_index.md]
covers_token_total: 2488
summary_level: d2
token_count: 712
type: summary
---
# Knowledge Structure Summary (Level d2)

This summary organizes knowledge related to system processes, agent memory, skill management, and operational health checks. The underlying knowledge curation process is consistently structured as Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation across most domains.

## System Operations & Scheduling
This domain covers automated system tasks and monitoring routines.
*   **Auto Sync**: Details the daily synchronization schedule (1 AM cron job) and its fact collection flow (`auto_sync.md`).
*   **Health Check**: Documents system health checks, noting a daily execution at 6 AM via cron job (`health_check.md`).

## Agentic Memory & Core Components
This domain focuses on the status and structure of the ByteRover agentic memory system and related scripts.
*   **Agentic Memory**: Confirms the system is fully set up, grouping facts for retrieval (`byterover_agentic_memory.md`). The associated skill is confirmed as Loaded (`byterover_agentic_memory_skill.md`).
*   **Worker Status & Sync Scripts**: Documents the status of key components: `byterover_checkpoint.py` (Working) and `byterover_knowledge_sync.py` (Working). The 'Worker Status Issue' was classified as a system issue, not a skill gap (`worker_status_issue.md`).

## Skill Management & Library
This domain outlines the methodology for defining, updating, and documenting skills.
*   **Skill Library Format**: Defines the required structure for skills, emphasizing CLASS-LEVEL skills over flat lists (`skill_library_format.md`).
*   **Update Strategy**: Specifies the priority order for skill updates: 1st (loaded skill), 2nd (umbrella skill), and 3rd (support file) (`skill_update_strategy.md`).
*   **Specific Skill Content**: Details the fact extraction flow for specific skills, noting that `tiktok-viral-script` documents a dual-path worker output architecture (`specific_skill_content.md`).
*   **Reviewed Skills**: Confirms the identification of specific skills, including `tiktok-viral-script` and `research-analyst` (`reviewed_skills.md`).

## Feedback & Interaction Signals
This domain captures user input and interaction data used for refinement.
*   **User Feedback Signals**: Documents that style/format corrections and workflow changes are primary signals for skill refinement, following an Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation flow (`user_feedback_signals.md`).
*   **User Interaction**: Analysis showed no direct user corrections or workflow changes occurred during the session, indicating execution via cron (`user_interaction.md`).

## Fallback Mechanism
This domain covers resilience and alternative paths.
*   **Fallback Mechanism**: Confirms an operational web search fallback path for the Gen Z slang skill (`fallback_mechanism.md`).