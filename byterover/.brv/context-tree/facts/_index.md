---
children_hash: cf4d9549bb86dbc2e6cb3a4d74e17a50e0d830e59472741eb7546d7c0136fb87
compression_ratio: 0.22139303482587064
condensation_order: 2
covers: [adobe_stock/_index.md, alamy/_index.md, auto_sync/_index.md, byterover_agentic_memory/_index.md, byterover_agentic_memory_skill/_index.md, byterover_checkpoint_py/_index.md, byterover_knowledge_sync_py/_index.md, doordash/_index.md, facebook_marketplace/_index.md, fallback_mechanism/_index.md, health_check/_index.md, memory_management/_index.md, memory_saving_status/_index.md, reviewed_skills/_index.md, rover/_index.md, shutterstock/_index.md, skill_library_format/_index.md, skill_update_strategy/_index.md, specific_skill_content/_index.md, taskrabbit/_index.md, tool_usage_policy/_index.md, trymata/_index.md, user_expectations/_index.md, user_feedback_signals/_index.md, user_information/_index.md, user_interaction/_index.md, userlytics/_index.md, usertesting/_index.md, worker_status_issue/_index.md]
covers_token_total: 4422
summary_level: d2
token_count: 979
type: summary
---
# Knowledge Structure Overview (Level d2)

This summary organizes factual knowledge across various domains, focusing on platform economics, system status, skill management processes, and user data.

## Financial & Royalty Structures
*   **Stock Platforms:**
    *   Adobe Stock pays a 33% royalty on sold photos (`adobe_stock.md`).
    *   Alamy offers a commission of 40-60% on sold photos (`alamy.md`).
    *   Shutterstock pays a royalty rate of 15-40% on sold photos (`shutterstock.md`).
*   **Service Earnings:**
    *   Rover offers potential earnings ranging from $15 to $30 per walk (`rover.md`).
    *   TaskRabbit offers potential earnings ranging from $30 to $100 per task (`taskrabbit.md`).
    *   TryMata offers payouts ranging from $5 to $30 per test (`trymata.md`).
    *   Userlytics offers payouts ranging from $5 to $90 per test (`userlytics.md`).
    *   UserTesting provides payouts ranging from $10 to $60 per test (`usertesting.md`).
    *   DoorDash offers potential earnings ranging from $15 to $25 per delivery (`doordash.md`).

## System & Process Facts
*   **System Health:** A cron job executes a daily health check at 6 AM (`health_check.md`).
*   **Synchronization:** The Auto sync process runs a daily synchronization at 1 AM, following an Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping flow (`auto_sync.md`).
*   **Script Status:** Components like `byterover_checkpoint.py` and `byterover_knowledge_sync.py` are confirmed to be Working (`byterover_checkpoint_py.md`, `byterover_knowledge_sync_py.md`).
*   **Memory Management:** Focuses on strategies for saving application state to memory (`memory_management.md`), with the status showing no additional items found to save (`memory_saving_status.md`).
*   **Tool Policy:** Tool access is strictly limited to memory and skill management tools (`tool_usage_policy.md`).

## Skill & Content Management
*   **Skill Library Structure:** The format mandates CLASS-LEVEL skills, emphasizing detailed `SKILL.md` files over flat lists (`skill_library_format.md`).
*   **Skill Update Strategy:** The preferred update priority is: 1st (Update loaded skill), 2nd (Update umbrella skill), 3rd (Add support file) (`skill_update_strategy.md`).
*   **Skill Identification:** Confirmed skills include `tiktok-viral-script` and `research-analyst` (`reviewed_skills.md`).
*   **Specific Content:** The `tiktok-viral-script` documents a dual-path worker output architecture (`specific_skill_content.md`).

## User Data & Interaction
*   **User Information:** Focuses on curating factual statements about user persona, preferences, and personal details (`user_information.md`).
*   **User Expectations:** Captures explicit user requirements regarding operational behavior and work style (`user_expectations.md`).
*   **Feedback Signals:** Style/Format corrections and Workflow corrections are treated as primary skill signals, following an Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation flow (`user_feedback_signals.md`).
*   **Interaction Analysis:** Analysis showed no user corrections or workflow changes occurred during the session, indicating execution via a cron run (`user_interaction.md`).

## Agentic Memory & Fallback
*   **Agentic Memory Status:** The ByteRover agentic memory system is fully set up, with knowledge facts grouped for retrieval (`byterover_agentic_memory._index.md`). The `byterover-agentic-memory` skill status is Loaded (`byterover_agentic_memory_skill._index.md`).
*   **Fallback Mechanism:** The Gen Z slang fallback skill has an operational web search fallback path (`fallback_mechanism._index.md`).
*   **Worker Status Handling:** The "Workers dead (May 14)" event was classified as a valid business/system issue rather than a skill gap, following Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation (`worker_status_issue._index.md`).