---
children_hash: 21cd126fbe7b3e1ad1f2c10de50a8fa3f2685c2a166dce2dde0f8051c1c2986c
compression_ratio: 0.4410828025477707
condensation_order: 2
covers: [formalized-skill-library-update-workflow.md, update_strategy/_index.md]
covers_token_total: 628
summary_level: d2
token_count: 277
type: summary
---
# Skill Library Update Strategy Overview

This strategy governs the evolution of the skill library by formalizing a prioritized execution sequence based on user feedback signals. The underlying curation process follows an Extraction $\rightarrow$ Deduplication $\rightarrow$ Grouping $\rightarrow$ Curation flow.

## Core Changes
The library structure has been updated to utilize CLASS-LEVEL skills, relying on rich `SKILL.md` files and references instead of narrow entries. Clear signals are defined for updates, including style/tone corrections, workflow changes, new techniques, and outdated skills.

## Update Workflow
The process strictly follows the sequence: User Feedback $\rightarrow$ Signal Identification $\rightarrow$ Preference Order Execution (Update/Patch/Add).

## Update Preference Order
Updates are executed in a strict priority order:
1. Update loaded skill
2. Update umbrella skill
3. Add support file

This strategy requires tracking user feedback signals across multiple sessions to inform the updates. For detailed workflow steps, refer to `formalized-skill-library-update-workflow.md`.