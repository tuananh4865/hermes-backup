# Autonomous Task Loop Detection — task_checker.py

**Found**: 2026-05-08 by Orchestrator session
**File**: `scripts/task_checker.py`

## Symptom

`autonomous.log` shows same task picked repeatedly without execution:

```
[2026-05-08 14:00:47] TASKS: 24 pending | NEXT: Restart watchdog daemon [80]
🤖 **AUTONOMOUS MODE: Executing highest priority task...**
[2026-05-08 16:00:47] TASKS: 24 pending | NEXT: Restart watchdog daemon [80]
🤖 **AUTONOMOUS MODE: Executing highest priority task...**
```

Task [80] ("Restart watchdog daemon") is picked at 14:00 and 16:00 — but never actually executes. The task count stays at 24 pending.

## Root Cause Hypothesis

`task_checker.py` has logic to "execute" a task but:
1. Either the execution path raises an exception silently
2. Or the "execute" step doesn't actually call the fix — it just logs the intent
3. Next run 2.5h later → same task still pending → picked again

## Detection Query

```bash
# Check for loop pattern in autonomous.log
grep -E "Executing highest priority task|NEXT:.*\[80\]" ~/.hermes/cron/autonomous.log | tail -10

# Count consecutive identical task picks
grep "Executing highest priority task" ~/.hermes/cron/autonomous.log | tail -5
```

## Real Fix Actions

When loop detected, do NOT wait for autonomous checker:

```bash
# Option 1: Restart watchdog daemon manually
launchctl kickstart -k system/com.apple.watchdogd

# Option 2: Check if watchdog is actually running
ps aux | grep watchdog | grep -v grep

# Option 3: Write directly to PENDING_TASKS.md to clear/flag the task
```

## Escalation Rule

If same task picked 3+ consecutive runs → manual intervention required:
1. Do the fix manually
2. Update PENDING_TASKS.md to mark task done
3. Report in next orchestrator brief
