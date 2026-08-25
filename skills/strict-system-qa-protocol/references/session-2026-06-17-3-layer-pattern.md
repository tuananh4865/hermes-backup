# Session 2026-06-17 — 3-Layer Verification Pattern Emerges

**Context:** After multiple rounds of transcript-saver-v2 hook QA, a pattern emerged that catches MORE bugs than flat 9-verify: organize verifies into 3 layers (Existence → Behavior → Future-proof).

## The Trigger

User asked: "Verify thêm" after a round of strict QA. Agent re-ran verifications and **discovered test file `test_handler.py` had vanished 4 times** in the same session, even though:
- File existed (Layer 1 ✓)
- File was created, ran, passed (Layer 2 ✓)
- File disappeared in <1 minute (Layer 3 ✗)

The flat 9-verify list couldn't categorize this — it would either mark as PASS (if the file happened to exist at verify time) or FAIL (if not). The 3-layer structure **separates the survival question** as its own layer, making it a first-class concern.

## The Pattern (now in SKILL.md)

```
Layer 1: EXISTENCE (does the system exist?)
   - Files exist with size > 0
   - Valid Python / Bash / YAML syntax

Layer 2: BEHAVIOR IN SESSION (does it work right now?)
   - 2A: Direct invocation (stdin JSON, args)
   - 2B: Via wrapper (matches runtime path)

Layer 3: FUTURE-PROOF (will it survive env changes?)
   - 3A: Cron survival (no auto-delete)
   - 3B: Fresh session (gateway restart, context compression)
   - 3C: Real message (gold standard — fires for actual user input)
```

## Real Failure Mode That 3-Layer Caught (2026-06-17)

**Test file `test_handler.py` vanishing:**

| Layer | What happened | What 3-layer would say |
|-------|---------------|------------------------|
| L1 | `ls test_handler.py` showed file 5 min ago, then disappeared | L1 = "files exist NOW" — but it disappeared DURING the verify run |
| L2 | Test ran successfully | L2 = "test passed" — but the test FILE itself is gone |
| L3 | ??? | **L3 = "did anything change that would invalidate this?"** — yes, file vanished mid-session |

**Without L3, this would have been reported as "L1 PASS, L2 PASS" — the user would be told the system works, then in 24 hours wonder why tests are missing.**

## What Layer 3 Uniquely Catches

| L3 sub-layer | Failure mode it catches |
|--------------|-------------------------|
| **3A** Cron | Cron script with `os.remove()` that deletes your files (the agent's "user mistake" — wasn't on purpose but happened) |
| **3B** Restart | Gateway caches old hook list; new hook registered but only fires after manual restart |
| **3C** Real input | Hook works for synthetic stdin but fails for actual Telegram message (different code path) |

## How to Use This Pattern

1. **Start with 3-layer structure** when verifying a deployed system
2. **Layer 1 first** — if files don't exist, skip 2 and 3
3. **Layer 2 next** — if behavior doesn't work, no point checking survival
4. **Layer 3 last** — this is where the "works in lab, breaks in prod" bugs hide
5. **3C is the gold standard** — if 3C passes, the system is real

## When 3-Layer > Flat 9-Verify

**Use 3-layer for:** deployed systems, infrastructure (hooks, cron, plugins), anything with environment dependencies
**Use flat 9-verify for:** single-change verification, code review checks, mid-task QA

## Future Investigation: Test File Vanishing Root Cause (RESOLVED)

The 3-layer structure flagged "test file vanishing" as a survival problem. **Root cause was identified later same day** when user said "Điều tra thêm": Hermes's built-in `disk_cleanup` plugin auto-deletes `test_*.py` / `tmp_*.py` / `*.test.py` files at `on_session_end`.

**Diagnostic command (catches in <30s — check FIRST when test file vanishes):**
```bash
tail -50 ~/.hermes/disk-cleanup/cleanup.log | grep "$(basename $YOUR_TEST_FILE)"
# TRACKED + DELETED entries with timestamps 8-15s apart = disk_cleanup is the culprit
```

**Full root cause + fix recipes:** see `self-verify-after-workaround` skill → "disk_cleanup Plugin Auto-Deletes test_*.py Files" section, and `references/session-2026-06-17-disk-cleanup-investigation.md` in that skill.

**Lesson for future 3-layer investigations:** When 3-layer surfaces a survival problem where L1 passes initially but the artifact disappears during the verify run, the culprit is almost always an **environment-side process** (cleanup plugin, watchdog, cron), not the agent's own tools. Diagnose via system audit logs FIRST (`~/.hermes/disk-cleanup/cleanup.log`, `~/.hermes/logs/gateway.log`, `tail -f` of relevant logs) before assuming a tool bug.

## What Was Updated in `loop-engineering-deployment` Skill (related)

In the same session, em updated `loop-engineering-deployment` to add:
- "Test File Vanishing After Edit Pitfall" section (already there)
- Defensive pattern: snapshot test file before editing handler.py
- Better practice: keep `test_handler.py` in separate path (e.g. `~/.hermes/hooks/_tests/`)
- "Hook Allowlist Format" + "Hermes Shell Hooks Pass JSON via STDIN" (already there)

The 3-layer pattern complements these — `loop-engineering-deployment` says "what can go wrong" and `strict-system-qa-protocol` 3-layer says "how to verify each category of failure mode systematically."
