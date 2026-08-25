# Session 2026-06-17 — Fable-5 100% Verification Session Log

> Real session transcript showing how "100% system-wide" claim was caught, then 5-layer matrix was applied. Use as a worked example.

## Session Flow

1. User applied 4 Fable-5 patterns (MCP Connector, Persistent Storage, Skills-First, Search Discipline) to SOUL.md files. Asked: "đã áp dụng system-wide chưa?"
2. Agent reported: "5/5 SOUL.md files comply, 4 mandatory + 5 contextual patterns, shared file 404 lines full" — sounded 100%.
3. User pushed: "Sao ko làm cho chắc chắn 100% đi nhỉ??"
4. Agent ran 5-layer matrix → found 2 silent bugs.

## The 2 Bugs Found

### Bug #1: 0/7 cron jobs had Fable-5 reference

**Symptom:** Cron jobs (running daily at 2AM/3AM/4AM/7AM/7:30AM/8AM) had no Fable-5 reminder in their prompts.

**Why missed:** The initial audit only checked SOUL.md files. Cron job prompts are stored in `~/.hermes/cron/jobs.json` — a different file, different layer.

**Detection command:**
```bash
jq -r '.jobs[].prompt' ~/.hermes/cron/jobs.json | grep -c "FABLE-5 MANDATE"
# Result: 0 (expected: 5 — number of LLM cron jobs)
```

**Fix:** Injected Fable-5 reminder block into 5 LLM cron prompts. 2 no_agent jobs (Wiki Health, Wiki Forget) skipped — they run scripts, not LLM.

```python
import json, shutil
from datetime import datetime

FABLE5_REMINDER = """

---

## 🆕 FABLE-5 MANDATE (2026-06-16) — APPLY ON THIS JOB

This job must follow 4 mandatory patterns from Claude Fable-5 harvest...
"""

jobs_path = "/Users/tuananh4865/.hermes/cron/jobs.json"
with open(jobs_path) as f:
    data = json.load(f)

# Backup
shutil.copy(jobs_path, f"{jobs_path}.pre-fable5-{datetime.now().strftime('%Y%m%d-%H%M')}")

for job in data["jobs"]:
    if job.get("no_agent"):  # Skip script-only
        continue
    if not job.get("prompt"):
        continue
    if "FABLE-5 MANDATE" in job["prompt"]:  # Idempotent
        continue
    job["prompt"] = job["prompt"].rstrip() + "\n" + FABLE5_REMINDER

with open(jobs_path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**Verification after fix:**
```bash
# Re-check all 5 LLM jobs
for job_id in 7cba6ba5f52a a4b8e528983f a5c02f2f0d87 5aea298eb0a8 546c141c8fb9; do
    jq -r ".jobs[] | select(.job_id == \"$job_id\") | .prompt" ~/.hermes/cron/jobs.json | grep -c "FABLE-5 MANDATE"
done
# Result: 1, 1, 1, 1, 1 (all 5 jobs PASS)
```

### Bug #2: Hook was SKIPPED — wrong function name

**Symptom:** Hook `fable5-compliance-check` had `def main()` instead of `def handle()`. Gateway silently rejected it. Hook did NOT fire on `session:start` for 7 days.

**Detection command:**
```bash
tail -50 ~/.hermes/logs/gateway.log | grep fable5
# Output: [hooks] Skipping fable5-compliance-check: no 'handle' function found
```

**Why missed:** Standalone test passed (`python3 handler.py` works). But standalone test doesn't validate hook discovery contract. Gateway has its own protocol: function name MUST be `def handle(event_type, context)`.

**Fix:** Renamed `def main()` → `def handle(event_type, context)` and added `if event_type != "session:start": return` guard.

**Verification after fix (post-gateway-reload):**
```bash
tail -50 ~/.hermes/logs/gateway.log | grep "fable5-compliance-check"
# Output: [hooks] Loaded hook 'fable5-compliance-check' for events: ['session:start']
```

## The 5-Layer Matrix Used

| Layer | Before | After fix | Evidence |
|-------|--------|-----------|----------|
| 1. SOUL.md | ✅ 5/5 | ✅ 5/5 | `check-fable5-compliance.sh` exit 0 |
| 2. Cron jobs | ❌ 0/5 LLM | ✅ 5/5 LLM | `jobs.json` grep |
| 3. Hook registration | ❌ SKIPPED | ✅ Loaded | `gateway.log` |
| 4. Shared reference | ✅ 16,285b | ✅ 16,285b | file size |
| 5. Compliance scripts | ✅ Both | ✅ Both | file check |

## Lessons Confirmed

1. **"100% system-wide" is a 5-layer claim, not 1** — single-layer (SOUL.md only) = false confidence.
2. **Cron job prompts are a separate layer** — they run in fresh agent context, no SOUL propagation.
3. **Hook discovery has its own contract** — `def handle()` is part of Hermes protocol, not Python convention.
4. **Standalone test is necessary but NOT sufficient** — gateway-level discovery is a separate contract.
5. **Backup before injection** — `cp jobs.json jobs.json.pre-fable5-TIMESTAMP` is the insurance.

## What User Said (Original Triggers)

- "yên tâm 100% system-wide" → need 5-layer matrix
- "Sao ko làm cho chắt chắc 100% đi nhỉ??" → 2 bugs found
- "verify, qa nghiêm ngặt" → 9-verify protocol

## Reusable Templates

This session produced 3 reusable artifacts:
1. **`auto-inject-on-profile-create.sh`** — wraps any system-wide injector for batch profile injection
2. **`session-auto-log` v2** — auto-extracts project_id/phase_id/task_id from user message
3. **Cron job injection script** — adds Fable-5 reminder to all LLM cron prompts

All 3 are now part of the `system-wide-mandate-enforcement` skill templates.
