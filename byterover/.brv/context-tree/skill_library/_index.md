---
children_hash: ac5cacf9e80cdc7a5b290cd7a90444573b202e727d51bbf275308d7c1e303d6d
compression_ratio: 0.8513119533527697
condensation_order: 2
covers: [update_strategy/_index.md]
covers_token_total: 343
summary_level: d2
token_count: 292
type: summary
---
# Skill Library Update Strategy

This strategy defines the process for updating the skill library to support active learning by shifting focus to class-level skills and explicit signal capture.

## Core Changes
*   **Structure:** The library is restructured to utilize CLASS-LEVEL skills via rich `SKILL.md` files and references, moving away from narrow, one-session entries.
*   **Signal Definition:** Clear signals are established for skill updates, encompassing style/tone corrections, workflow changes, new techniques, and outdated skills.

## Update Workflow
The process follows a defined sequence: User Feedback $\rightarrow$ Signal Identification $\rightarrow$ Preference Order Execution (Update/Patch/Add).

## Execution Preference Order
Updates must follow a strict priority:
1.  Update loaded skill
2.  Update umbrella skill
3.  Add support file

## Dependencies and Focus
The strategy relies on tracking user feedback signals across multiple sessions to inform updates. The primary focus is capturing explicit corrections and emerging patterns as first-class skill signals.

For detailed implementation, refer to the `skill_library_update_strategy.md` entry.