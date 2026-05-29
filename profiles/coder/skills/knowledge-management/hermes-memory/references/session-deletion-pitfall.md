# Session Deletion — Pitfall: Must Read Before Delete

## The Mistake

Today, I deleted 50 old `.jsonl` session files without first reading them and curating their knowledge to ByteRover.

**What should have happened:**
```
1. READ session file
2. Extract knowledge (facts, preferences, learnings, tasks)
3. BRV CURATE each piece of knowledge
4. THEN delete the session file
```

**What actually happened:**
```
1. DELETED session files immediately
2. Lost knowledge permanently
```

## Lesson (Encoded in hermes-memory skill)

**RULE: Never delete session history without extracting knowledge first.**

This applies to:
- `.jsonl` files in `~/.hermes/sessions/`
- Session checkpoint files
- Any conversation history files
- `memory_store.db` or similar

## Safe Deletion Checklist

Before deleting any session/history file:

- [ ] Have I read the content?
- [ ] Have I extracted user facts, preferences, learnings?
- [ ] Have I curated each item to ByteRover?
- [ ] Only THEN proceed to delete

## When in Doubt

If unsure whether a session has valuable knowledge:
- **Don't delete it**
- Ask the user: "Should I delete these old sessions? I want to make sure I save any important learnings first."

## Exception

Files that are clearly temporary/generated (not user conversations):
- `.tmp`, `.temp` files
- `__pycache__`, `.pyc` files
- Build artifacts

These can be deleted without knowledge extraction.

## Related

- See `hermes-memory` skill: "Critical Workflow: Session File Deletion" section