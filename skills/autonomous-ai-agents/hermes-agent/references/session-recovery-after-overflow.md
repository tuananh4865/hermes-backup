# Session Recovery After Context Overflow

**Problem:** When context exceeds 122K+ tokens, session auto-resets. The agent starts fresh — wiki loads but session WORKING STATE is lost.

**What gets saved:**
- ✅ `transcript-saver` hook → transcripts in `wiki/raw/transcripts/YYYY-MM-DD/`
- ✅ Wiki content (start-here, SCHEMA, index, log, learned-about-tuananh)

**What is LOST on reset:**
- ❌ Current task context (what was being researched, built, decided)
- ❌ Active work state (round number in research, partial results)
- ❌ Conversation buffer mid-thought

**Evidence from 2026-06-01:**
- Anh asked "Context trước về youtube" — expected context to persist
- Em found transcripts from 2026-05-31, 2026-06-01 but session WORKING STATE was gone
- Round 1 of 100-round YouTube research was done but not recoverable

## Current Hook Architecture

| Hook | What it saves | When |
|------|--------------|------|
| `transcript-saver` | Raw message text | After every user/assistant message |
| `wiki-session-start` | Wiki context (start-here, SCHEMA, index, log) | On session start |
| `memory` (WikiMemoryProvider) | Extracted facts to MEMORY.md/USER.md | On pre-compress, session end |

**Gap:** Nothing saves the current WORKING STATE (task progress, partial outputs) between messages.

## Recovery Workflow (Current — Manual)

```bash
# 1. Find recent session transcripts
ls wiki/raw/transcripts/2026-05-31/
ls wiki/raw/transcripts/2026-06-01/

# 2. Read the last message before reset
cat wiki/raw/transcripts/YYYY-MM-DD/HH-MM-SS_telegram_*.md

# 3. session_search for context
session_search(query="youtube", limit=3)
```

## Needed: Auto-Session-Checkpoint Hook

A hook that runs **after every assistant turn** and saves working state:

```python
# Concept: checkpoint hook that writes to session_state.md
"""
After each assistant response, if meaningful work was done:
- Current task: "100-round YouTube deep research"
- Round: 1/100
- Last action: Searched YouTube algorithm 2026
- Key finding: CTR + AVD = winning formula
"""
```

**Location:** `~/.hermes/plugins/hooks/session_checkpoint.py`

This is an **architecture gap** — not yet implemented.

## Session Summary Pattern (Manual Workaround)

After any significant milestone (every 10-20 turns), write a session checkpoint:

```
# ~/.hermes/memories/TASK_STATE.md
### Current Task
100-round YouTube deep research
### Progress
- Round 1: Algorithm 2026 ✅
- Round 2-5: Content Strategy (pending)
### Key Findings
- Algorithm tests, doesn't push
- CTR + AVD = winning formula
```

This file is read on session start if it exists.

## Lesson

Anh expects context to persist after reset. The system saves transcripts but not working state. For long-running research tasks (100-round deep research), manual checkpointing is required until a session checkpoint hook is implemented.
