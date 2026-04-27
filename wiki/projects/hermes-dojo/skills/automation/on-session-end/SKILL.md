---
name: on-session-end
description: Compress and save session learnings when session ends - update project state, create episodic memory, log decisions
version: 1.0.0
category: automation
platforms: [macos, linux]
created: 2026-04-14
tags: [automation, session-end, memory-compression, episodic, hooks]
requires_toolsets: [terminal]
---

# On-Session-End Hook

**Triggered when a session ends.**

This hook ensures learnings are preserved and context is ready for the next session.

---

## When It Fires

**Event:** Session ending

Triggers:
1. User says goodbye
2. Session timeout
3. Task completed
4. Hermes shutting down
5. User switches to different project

---

## The On-Session-End Workflow

### Step 1: Update Project State

```
Read current PROJECT_STATE.md
Update:
- Task progress
- Decisions made
- Files modified
- Next steps
```

### Step 2: Compress Observations

```
For this session:
- What was the goal?
- What happened?
- What was decided?
- What was learned?
```

### Step 3: Create Episodic Memory

```markdown
# Session: {YYYY-MM-DD}

## Task
{What we worked on}

## Key Events
- {Event 1}
- {Event 2}

## Decisions
- {Decision} → {Rationale}

## Learnings
- {Learning 1}
- {Learning 2}

## Next Steps
- {Next action}
```

Save to: `memories/sessions/{date}_{slug}.md`

### Step 4: Update MEMORY.md

```
Add to Mistakes Learned table if applicable
Add to Skills Created table if applicable
Add to Recent Updates
```

### Step 5: Commit Changes

```
If code changes made:
- git add -A
- git commit -m "Session: {brief summary}"
```

---

## Session End Template

```markdown
# Session Summary: {YYYY-MM-DD HH:MM}

**Project:** {Project name}
**Duration:** {Approximate duration}
**Task:** {What was worked on}

## Accomplishments
- {Accomplishment 1}
- {Accomplishment 2}

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| | |

## Files Modified
| File | Change |
|------|--------|
| | |

## Key Learnings
- {Learning 1}
- {Learning 2}

## Mistakes Made
- {Mistake} → {Lesson}

## Next Steps
1. {Next action}
2. {Next action}

## State for Next Session
{Instructions for continuing}
```

---

## Example Session End

```
1. User: "OK that's all for today"

2. Hook: on_session_end

3. Update project state:
   - Task: Phase 2 Process Engine
   - Progress: 80% → 100%
   - Completed: Created 4 process skills
   - Status: Ready for QA

4. Create episodic memory:
   memories/sessions/2026-04-14_phase-2-process.md

5. Update MEMORY.md:
   - Added: "Phase 2 complete"
   - Added: "R→P→I workflow established"

6. Commit changes:
   git commit -m "Phase 2 Process: complete, ready for QA"

7. Summary to user:
   "Session complete. Phase 2 is 100% done.
   Created: research-command, plan-command, implement-command,
   cascade-prevention.
   Next: Phase 2 QA."
```

---

## Key Principles

### Always Preserve Learnings

```
NOT: "Goodbye"
BUT: "Goodbye. State saved. Learnings preserved.
      Next session will know exactly where we left off."
```

### Never End Without Update

```
If session ends without update:
- Next session starts blank
- Context lost
- Work appears wasted

Rule: If meaningful work happened, ALWAYS update state.
```

---

## Integration

- Use [[update-project-state]] — Update project state
- Use [[memory-manage]] — Create episodic memory
- Use [[skill-from-experience]] — Extract learnings
- Use [[wiki_hooks.py]] — The hook engine

---

## Related

- [[on-session-start]] — Session context loading
- [[on-ingest]] — Source processing
- [[on-schedule]] — Periodic maintenance
- [[update-project-state]] — State management
- [[wiki_hooks.py]] — Hook engine
