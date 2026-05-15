---
children_hash: 2624c7e7f18be436abd18c1a519db17242abd29b65668dca98d5ae8f65382a0b
compression_ratio: 0.45977011494252873
condensation_order: 3
covers: [facts/_index.md, skill_library/_index.md]
covers_token_total: 957
summary_level: d3
token_count: 440
type: summary
---
Structural Summary of Knowledge Entries

This summary outlines the organization and management strategies for skill library curation, fallback mechanisms, and system status tracking.

## Skill Library Management Structure
The skill library is structured around CLASS-LEVEL skills, requiring dedicated `SKILL.md` files and a `references/` directory to prioritize rich skills over flat lists. The standard curation flow involves Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation (`skill_library_format/_index.md`).

*   **Confirmed Skills**: The system confirms the existence of `tiktok-viral-script` (documenting a dual-path worker output architecture) and `research-analyst`.
*   **Update Strategy**: Updates follow a strict priority order: 1st Priority (Update loaded skill), 2nd Priority (Update umbrella skill), and 3rd Priority (Add support file) (`skill_update_strategy/_index.md`).

## Feedback and Signal Processing
User feedback signals are treated as primary inputs for skill updates, covering style/format corrections and workflow changes. The processing flow is Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation (`user_feedback_signals/_index.md`). Analysis of user interaction showed no direct user corrections or workflow changes in `user_interaction/_index.md`.

## Fallback and System Status
*   **Fallback Mechanism**: A web search fallback path is operational for the Gen Z slang skill, documented in `fallback_mechanism/_index.md`.
*   **Worker Status**: System events like "Workers dead (May 14)" are classified as business/system issues, organized via Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation (`worker_status_issue/_index.md`).