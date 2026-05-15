---
children_hash: e59fdb69f40d55d939e129089cac3820c859f1d876529ec7c07514f756a49e97
compression_ratio: 0.9389830508474576
condensation_order: 1
covers: [skill_library_update_strategy.md]
covers_token_total: 295
summary_level: d1
token_count: 277
type: summary
---
# Skill Library Update Strategy

This strategy outlines the process for updating the skill library to support active learning by focusing on class-level skills and explicit signal capture.

## Core Changes
*   **Structure:** The library is restructured to use CLASS-LEVEL skills, utilizing rich `SKILL.md` files and references instead of narrow, one-session entries.
*   **Signal Definition:** Clear signals are defined for skill updates, including style/tone corrections, workflow changes, new techniques, and outdated skills.
*   **Update Preference Order:** The execution preference is strictly ordered: 1. Update loaded skill, 2. Update umbrella skill, 3. Add support file.

## Workflow
The process follows a defined flow: User Feedback $\rightarrow$ Signal Identification $\rightarrow$ Preference Order Execution (Update/Patch/Add).

## Dependencies and Focus
*   **Dependency:** The strategy requires tracking user feedback signals across multiple sessions to inform updates.
*   **Highlight:** The primary focus is on capturing explicit corrections and emerging patterns as first-class skill signals.