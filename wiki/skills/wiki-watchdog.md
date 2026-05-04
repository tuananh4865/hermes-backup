---
title: "Wiki Watchdog Skill"
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [auto-filled]
---

# Wiki Watchdog Skill

## Trigger Conditions

- Watchdog daemon detects file changes in `~/wiki`
- Git post-commit hook fires
- `watchdog.pending` or `watchdog_event.json` file exists
- Agent receives `wiki:change` event

## Context Gathering

When triggered, the agent should:

```bash
# Read the event file
python3 ~/wiki/scripts/watchdog_context_builder.py

# Check what changed
cat ~/wiki/scripts/watchdog_event.json

# Read project state
cat ~/wiki/concepts/project-tracker.md
```

## Agent Behavior Loop

```
1. OBSERVE
   ├── Read watchdog_event.json → what files changed?
   ├── Read project-tracker.md → what project am I tracking?
   └── Read relevant changed files → what happened?

2. ASSESS
   ├── Broken links introduced? → auto-fix
   ├── New content added? → update cross-links, frontmatter
   ├── Duplicate content? → flag for merge
   ├── Stale content updated? → refresh freshness score
   └── New topic discovered? → create concept page

3. ACT
   ├── Fix what can be fixed automatically
   ├── Flag what needs human review
   └── Update project-tracker.md checkpoint

4. LEARN
   └── If this fix worked, remember the pattern
```

## Auto-Fix Categories

**Auto-fix immediately:**
- Missing frontmatter → generate from content
- Broken wikilinks → fix or remove
- Circular links → break cycle
- Missing cross-links → add links to index

**Flag for review:**
- Duplicate pages detected
- Contradicting claims found
- Stale content (needs human refresh)
- New topic suggestions

**Log only:**
- Project checkpoint updates
- Freshness score changes
- Cross-link additions

## Output Format

After each watchdog trigger, the agent should update `project-tracker.md`:

```markdown
## Watchdog Session: YYYY-MM-DD HH:MM

### Changes Detected
- [file1.md] — action taken
- [file2.md] — action taken

### Auto-fixes Applied
- link fixes: N
- frontmatter added: N

### Flags for Human Review
- [issue description]

### Next Actions
- [ ] task 1
- [ ] task 2
```

## Checkpoint Before Exit

Before ending a watchdog session:
```bash
python3 ~/wiki/scripts/project_state.py checkpoint \
  --action-text "Completed watchdog self-heal" \
  --next-action "review flagged items" \
  --phase "phase-3-watchdog"
```

## Debouncing

- Watchdog debounces: 10 seconds between triggers
- Bulk operations (git commit with many files) → single trigger
- Agent should batch fixes, not fix one file at a time

## Success Criteria

- No broken links after agent exits
- All changed files have frontmatter
- project-tracker.md updated with checkpoint
- Flags sent to Telegram if human review needed

## Related

- [[log]] — Wiki activity log
- [[watchdog-system]] — Watchdog daemon

> **Auto-improvement:** *Clarity of instructions**: The skill has a good structure but some areas could be clearer:

> **Auto-improvement:** 2 concrete improvements in JSON format.

> **Auto-improvement:** 2 concrete improvements. Let me analyze the current skill file and identify areas for improvement.

> **Auto-improvement:** *Error handling and edge cases**: The skill describes a happy path but doesn't cover what happens when things go wrong. For example:

> **Auto-improvement:** 2 concrete improvements. Let me analyze the current skill file and identify areas that could be improved.

> **Auto-improvement:** 2 concrete improvements. Let me analyze the skill file for potential issues:

> **Auto-improvement:** watchdog.md skill file and suggest 1-2 concrete improvements. Let me analyze the current skill file:

> **Auto-improvement:** watchdog.md skill file and suggest 1-2 concrete improvements in JSON format. Let me analyze this skill file for potential issues:

> **Auto-improvement:** watchdog.md skill file to identify concrete improvements.

> **Auto-improvement:** *Error handling is missing**: The skill describes a happy path but doesn't cover:

> **Auto-improvement:** watchdog" agent and suggest 1-2 concrete improvements. Let me analyze this skill file for issues:

> **Auto-improvement:** watchdog.md" and suggest 1-2 concrete improvements to make it more effective. I need to focus on clarity, completeness, and avoiding pitfalls.