---
children_hash: ac45d499ef7dc245d413099d6886aa9ad02bfe32d0c0d7836e77f6cb3e0a18f7
compression_ratio: 0.4026996625421822
condensation_order: 2
covers: [formalized-skill-library-update-workflow.md, update_strategy/_index.md, user-feedback-driven-skill-library-evolution.md]
covers_token_total: 889
summary_level: d2
token_count: 358
type: summary
---
## Skill Library Update Workflow Overview

The evolution of the skill library is governed by a strict, prioritized execution sequence driven by user feedback signals.

### Core Workflow
The overall process follows a three-step workflow defined in `formalized-skill_library_update_workflow.md`:
1. User Feedback
2. Signal Identification
3. Preference Order Execution (Update/Patch/Add)

This sequence is also confirmed by `user-feedback-driven-skill_library_evolution.md`, establishing user interaction data as the primary driver for skill refinement. The underlying curation process involves Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation.

### Update Strategy
The strategy outlined in `update_strategy/_index.md` focuses on supporting active learning through class-level skills and explicit signal capture. Key changes include:
*   **Structure:** Restructuring the library to use CLASS-LEVEL skills, leveraging rich `SKILL.md` files and references instead of narrow entries.
*   **Signal Definition:** Defining clear signals for updates, covering style/tone corrections, workflow changes, new techniques, and outdated skills.

### Preference Order Execution
The execution preference order dictates the sequence of updates:
1. Update loaded skill
2. Update umbrella skill
3. Add support file

This strategy requires tracking user feedback across multiple sessions to inform all update sequences.