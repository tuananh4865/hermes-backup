---
name: on-session-start
description: Load relevant context when session begins - read project state, check pending work, prepare workspace
version: 1.0.0
category: automation
platforms: [macos, linux]
created: 2026-04-14
tags: [automation, session-start, context-loading, memory, hooks]
requires_toolsets: [terminal]
---

# On-Session-Start Hook

**Triggered when a new session begins.**

This hook ensures Hermes has context about current projects and pending work.

---

## When It Fires

**Event:** Session starts or resumes

Triggers:
1. Hermes starts
2. User says "continue where we left off"
3. User switches to a different project
4. Long idle period ends

---

## The On-Session-Start Workflow

### Step 1: Check for Active Projects

```
Look for: PROJECT_STATE.md files
Check: ~/wiki/projects/*/PROJECT_STATE.md
```

### Step 2: Load Project State

```
If project exists:
1. Read PROJECT_STATE.md
2. Summarize current status
3. Note what's in progress
```

### Step 3: Check Pending Work

```
Questions:
- What was being worked on?
- What are the next steps?
- Are there any blockers?
```

### Step 4: Load Relevant Context

```
Context to load:
- Recent session summaries
- Relevant skills
- User preferences (USER.md)
- Recent decisions
```

### Step 5: Prepare for User

```
Summary to provide:
- "You have X active project(s)"
- "Last work: {brief description}"
- "Continue with: {suggested action}"
```

---

## Session Start Template

```markdown
# Session Start: {YYYY-MM-DD HH:MM}

## Active Projects
| Project | Status | Last Updated |
|---------|--------|--------------|
| | | |

## Project Context

### {Project Name}
**Status:** {In Progress / Paused}
**Last Session:** {date}
**Progress:** {X}% complete

**Current Task:**
{Task description}

**Next Steps:**
1. {Next action}
2. {Next action}

**Blockers:**
- {blocker if any}

## Recent Decisions
| Decision | Rationale | Date |
|----------|-----------|------|
| | | |

## Relevant Skills
- {skill 1}
- {skill 2}

## User Preferences
{Notes from USER.md}
```

---

## Example Session

```
1. Session starts

2. Hook: on_session_start

3. Check for projects:
   Found: ~/wiki/projects/hermes-dojo/PROJECT_STATE.md

4. Load state:
   - Current task: Phase 2 Process Engine
   - Progress: 80%
   - Last session: 2026-04-14

5. Prepare summary:
   "Welcome back. You're working on Hermes Dojo - Phase 2.
   Progress: 80% complete. Next: Test R→P→I workflow.
   Shall I continue with Phase 2?"

6. Provide to user:
   "You left off working on Phase 2: Process Engine.
   R→P→I skills are created. Ready for QA.
   Continue with Phase 2 QA?"
```

---

## Key Principles

### Always Provide Context

```
NOT: "Ready. What do you want to do?"
BUT: "You're working on Hermes Dojo - Phase 2 is 80% complete.
      R→P→I skills are ready for testing.
      Shall I run QA for Phase 2?"
```

### Never Start Blank

```
NOT: Fresh session with no context
BUT: Always load project state, provide summary
```

---

## Integration

- Use [[update-project-state]] — Read current state
- Use [[memory-manage]] — Load episodic memories
- Use [[wiki_hooks.py]] — The hook engine

---

## Related

- [[on-session-end]] — Session compression
- [[on-ingest]] — Source processing
- [[on-schedule]] — Periodic maintenance
- [[update-project-state]] — State management
- [[wiki_hooks.py]] — Hook engine
