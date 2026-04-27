---
name: update-project-state
description: Update project state after each session - ensures Hermes never forgets what it was working on
version: 1.0.0
category: memory
platforms: [macos, linux]
created: 2026-04-14
tags: [project-state, progress-tracking, session-management, memory]
requires_toolsets: [terminal]
---

# Update Project State

**After every session: update the state. Before every session: read it.**

This skill ensures Hermes always knows where it left off and what needs to happen next.

---

## When to Use

**Rule: Update at end of EVERY session.**
**Rule: Read at start of EVERY session.**

### End of Session Triggers
1. Task completed
2. Session ending (human says goodbye)
3. Significant progress made
4. Session timeout/imminent disconnect

### Start of Session Triggers
1. Session begins
2. Human says "continue where we left off"
3. Human asks about project status

---

## The Update Workflow

### Step 1: Read Current State

```
Read PROJECT_STATE.md for current project
Confirm which project you're working on
Identify what's in progress
```

### Step 2: Update Task Progress

```
What was the goal?
What was accomplished this session?
What remains?
```

### Step 3: Document Decisions

```
Were any decisions made this session?
Log them with rationale.
```

### Step 4: Note Blockers

```
Any current blockers?
What needs to happen to unblock?
```

### Step 5: Define Next Steps

```
What should happen in the next session?
Prioritize the next 1-3 actions.
```

### Step 6: Update the File

```
Write changes to PROJECT_STATE.md
Use the template structure
Be specific and complete
```

---

## Update Template

```markdown
## Current Task
**Task:** {Brief description}
**Started:** {date}
**Status:** In Progress / Completed

## Task Status
- [x] Research - Completed {date}
- [x] Plan - Completed {date}
- [ ] Implementation - 60% complete
  - [x] Step 1
  - [x] Step 2
  - [ ] Step 3 - IN PROGRESS

## Decisions Made
- {date}: {Decision} → {Rationale}

## Recent Changes
- {date}: {Description} - {files}

## Blocker
- Current: {blocker description}
- To unblock: {action needed}

## Next Steps
1. {Next action}
2. {Next action}

## Context for Next Session
{Paragraph explaining where we are and what needs to happen}
```

---

## Example Session Update

```
Session: Fix payment bug

BEFORE UPDATE:
- Task: Fix payment bug
- Progress: 40% - found root cause
- Next: Implement fix

AFTER UPDATE:
- Task: Fix payment bug
- Progress: 80% - fix implemented, testing
- Completed this session:
  - Identified root cause (config hardcoded to 10MB)
  - Updated config to 50MB
  - Added error handling
- Next steps:
  1. Test 50MB upload
  2. Test error message displays
  3. Run full test suite
- Context: "We're testing the fix. Config changed, error handling added.
  Need to verify both work correctly before marking done."
```

---

## The Critical Rule

```
If you end a session WITHOUT updating PROJECT_STATE.md,
the next session will be LOST.

The next Hermes will not know:
- What you were working on
- Where you left off
- What needs to happen next

This creates the cascade of:
"Continue where we left off"
"I don't know what we were doing"
```

---

## Session Start: Read First

At the START of every session:

```
1. Read PROJECT_STATE.md
2. Ask: "Are we continuing a project?"
3. If yes: Summarize where we are
4. Confirm with human before proceeding
```

**Template:**
```
Based on PROJECT_STATE.md:
- Current project: {name}
- Current task: {description}
- Progress: {X}%
- Last session: {date}
- Next steps: {list}

Shall I continue with this?
```

---

## Integration

- Use [[memory-manage]] — For memory tier management
- Use with [[implement-command]] — After completing implementation steps
- Use with [[research-command]] — After completing research
- Use with [[plan-command]] — After creating plan

---

## Related

- [[memory-manage]] — Memory tier management
- [[PROJECT_CONTEXT.md.template]] — Template for project state
- [[mistake-logging]] — Log mistakes separately
- [[MEMORY]] — Global memory for broader learnings
