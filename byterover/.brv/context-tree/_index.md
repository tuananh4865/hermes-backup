---
children_hash: a967ed2febd5648a1b6526ce4193ec90afdaa3ae1250e19f5db175d061140e2a
compression_ratio: 0.3456419063975955
condensation_order: 3
covers: [curation/_index.md, facts/_index.md, skill_library/_index.md, unknown_domain/_index.md]
covers_token_total: 2329
summary_level: d3
token_count: 805
type: summary
---
# Knowledge Structure Summary (Level d3)

This summary outlines the standardized RLM Curation Workflow and the key knowledge domains organized within the context tree.

## Core Curation Workflow
The knowledge base follows a consistent four-stage pipeline for content ingestion:
1. **Extraction**: Identifying key facts from source content.
2. **Deduplication**: Removing redundant or similar facts to maintain data integrity.
3. **Grouping**: Categorizing extracted facts by subject for structured organization.
4. **Curation**: Final structuring and formalization of knowledge into the context tree.

This pattern is uniformly applied across both `facts` and `skill_library` domains.

## Knowledge Domains Overview (`facts/_index.md`)
The factual knowledge is organized into several major areas:
*   **Financial & Royalty Structures**: Details on platform earnings, including royalty rates for Stock Platforms (Adobe Stock, Alamy, Shutterstock) and potential earnings from service platforms (Rover, TaskRabbit, TryMata, Userlytics, DoorDash).
*   **System & Process Facts**: Covers operational facts such as daily health checks (`health_check.md`), synchronization processes (`auto_sync.md`), script status confirmation (`byterover_checkpoint_py.md`, `byterover_knowledge_sync_py.md`), and memory management strategies (`memory_management.md`).
*   **Skill & Content Management**: Defines the structure for the Skill Library, mandating CLASS-LEVEL skills over flat lists (`skill_library_format.md`) and outlining the prioritization sequence for skill updates (`skill_update_strategy.md`). It also confirms specific skills like `tiktok-viral-script`.
*   **User Data & Interaction**: Focuses on curating facts about user personas (`user_information.md`), capturing explicit requirements (`user_expectations.md`), and analyzing interaction data (e.g., confirming no workflow changes occurred during the session via `user_interaction.md`).
*   **Agentic Memory & Fallback**: Documents the setup of the agentic memory system (`byterover_agentic_memory._index.md`) and the operational path for fallback mechanisms (`fallback_mechanism._index.md`), including handling worker status issues (`worker_status_issue._index.md`).

## Skill Library Evolution (`skill_library/_index.md`)
The skill library evolution is driven by user feedback signals, following a three-step workflow: User Feedback $\rightarrow$ Signal Identification $\rightarrow$ Preference Order Execution (Update/Patch/Add). The update preference order is strictly defined as: 1st (Update loaded skill), 2nd (Update umbrella skill), and 3rd (Add support file).

## Extracted User Insights (`unknown_domain/_index.md`)
The RLM Extraction process successfully identified key user insights, including:
*   **User Profile**: Interest in online income and freelancing opportunities.
*   **Earning Goal**: A specific target of earning $30 quickly was identified.
*   **Action Requested**: Request for proactive searching for online work opportunities.
*   **Recommendation Preference**: Preference for comprehensive alternatives over single recommendations.
*   **Language Context**: Primary language is Vietnamese, with all conversation language being in Vietnamese.