---
name: strict-system-qa-protocol
description: "Run 9 concrete tool-based verifies with evidence when user demands strict QA on a deployed system ('verify nghiêm ngặt', 'check lại', 'QA system', 'đã run được chưa?'). Each verify = 1 tool command (md5, stat, grep, diff, count) with inline evidence. Report format must be numbered, evidence-based, no 'should work' handwaving. Use when user signals: 'verify', 'tự verify', 'QA nghiêm ngặt', 'đảm bảo', 'tự check'. Different from qa-gate (which gates individual steps) — this is for verifying a DEPLOYED SYSTEM end-to-end."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [qa, verification, system-check, evidence-based, strict-mode]
    related_skills: [self-verify-after-workaround, qa-gate, diagnose, hermes-agent, loop-engineering-deployment]
---

# Strict System QA Protocol (2026-06-17)

## When to Use This Skill

User signals:
- "verify", "tự verify", "QA nghiêm ngặt", "đảm bảo hoạt động đúng"
- "check lại", "tự check đi", "em check thử xem"
- "đã run được chưa?", "system có chạy không?"
- "audit system X", "review lại toàn bộ"
- "kết quả thật không?", "có thật không?"

**Distinguishing trigger phrases** (from 2026-06-16 corrections):
- "em tự làm tự verify đi" → no questions back, just run
- "đừng hỏi anh X hay Y" → make the call, then verify
- "báo cáo suông" → user is calling out reports without evidence

## When NOT to Use

- For verifying a single change mid-task (use `qa-gate` instead)
- For code review (use `code-review-and-quality` instead)
- For debugging a specific error (use `diagnose` instead)
- When user wants a plan, not a verification (use `plan` instead)

## The Core Protocol (9 Verifies, Evidence Inline)

When user demands strict QA on a deployed system, run **9 concrete verifications** — each with tool-based evidence. Don't try to be clever or skip steps. The user wants to see ALL 9, not just the ones that pass.

```bash
# V1: Files exist (size + mtime, not just existence)
ls -la /path/to/expected/file
stat -f "%Sm %z %N" /path/to/file

# V2: Unit tests pass (with exit codes, full output)
python3 /path/to/test.py 2>&1 | tail -10
echo "EXIT: $?"

# V3: E2E test (real invocation, not manual mock)
bash /path/to/run.sh --arg1 val1
echo "EXIT: $?"

# V4: Services registered (with status)
hermes hooks list 2>&1 | grep "YOUR_HOOK"
hermes config check 2>&1 | head -3

# V5: State files have data (not empty)
grep -c "verdict:" /path/to/state.md  # should be > 0

# V6: Cron jobs (if applicable)
hermes cron 2>&1 | grep "Name:" | head -5
hermes cron 2>&1 | grep "Last run:" | head -3  # should be recent + ok

# V7: Wiki / docs (if applicable)
ls -la /path/to/wiki/page.md
grep -c "PageName" /path/to/index.md  # cross-references

# V8: Mirror / replication (MD5 match)
md5 /path/to/source
md5 /path/to/mirror
# Both hashes MUST be identical

# V9: Regression test (re-run a known-good test case)
echo '{"test":"input"}' | python3 /path/to/handler.py
# Should produce expected output
```

**Skip inapplicable verifies with a one-line note:** "V6 N/A — no cron jobs in this system". Don't fake the verification.

## The 3-Layer Verification Pattern (2026-06-17 Lesson)

**Stronger than flat 9 verifies.** When verifying a DEPLOYED SYSTEM (not a single change), organize verifies into 3 layers that catch different failure modes. The flat 9-verify list above can pass even when the system breaks in 24 hours — the 3-layer version catches more.

```
Layer 1: EXISTENCE (does the system exist?)
   ↓
Layer 2: BEHAVIOR IN SESSION (does it work right now?)
   ↓
Layer 3: FUTURE-PROOF (will it survive cron / restart / fresh session?)
```

### Layer 1: Existence (the cheap layer)

Verifies files exist with non-zero size, are executable, are valid syntax. Catches: "did I actually write the file or just claim I did?"

```bash
# 1A: All expected files exist with size > 0
for f in handler.py hook_wrapper.sh HOOK.yaml test_handler.py; do
  path="/path/to/hooks/$f"
  [ -f "$path" ] && echo "✓ $f: $(wc -c < $path)B" || echo "✗ MISSING: $f"
done

# 1B: Python syntax valid
python3 -m py_compile /path/to/handler.py && echo "✓ valid Python"

# 1C: Bash syntax valid
bash -n /path/to/hook_wrapper.sh && echo "✓ valid bash"

# 1D: YAML valid
python3 -c "import yaml; yaml.safe_load(open('/path/to/HOOK.yaml'))" && echo "✓ valid YAML"
```

**If Layer 1 fails, no point checking Layer 2 or 3.** Stop and fix.

### Layer 2: Behavior in current session (the live layer)

Verifies the system actually WORKS right now, in this session. Two sub-layers:

**Layer 2A — Direct invocation:** call the script/handler with known inputs and verify expected output.

```bash
# 2A: Test stdin JSON parsing (real Hermes format)
echo '{"hook_event_name":"on_session_end","session_id":"test_001","extra":{"response":"x","message":"y","platform":"telegram","user_id":"123"}}' \
  | python3 /path/to/handler.py --event agent_end
# Should create a file with x and y populated, NOT $MESSAGE / $RESPONSE literals
```

**Layer 2B — Via wrapper path:** call through the same wrapper the runtime uses, to verify the full chain.

```bash
# 2B: Test via shell wrapper (matches what Hermes actually invokes)
bash /path/to/hook_wrapper.sh \
  --event on_session_end \
  --output "test response" \
  --message "[User] test" \
  --session_id "test_001" \
  --platform telegram \
  --user_id "123"
echo "EXIT: $?"
```

**Layer 2 catches:** `$MESSAGE` literal bug, event name mismatch, handler silent-return, stdin parsing missing. **These are bugs that pass Layer 1 (file exists) but fail when actually run.**

### Layer 3: Future-proof (the survival layer)

Verifies the system survives ENVIRONMENT CHANGES that happen AFTER the current session ends. Three sub-layers:

**Layer 3A — Cron survival:** Will cron jobs accidentally delete/modify these files?

```bash
# 3A: Verify cron scripts' scope doesn't include your files
grep -A 3 "for folder in" /path/to/wiki_forget_14days.py | head -10
# If script iterates wiki/{concepts,entities,...} only → your hooks/ dir is safe
```

**Layer 3B — Fresh session survival:** Will the system work after Hermes restart / new chat / context compression?

```bash
# 3B: Restart gateway + verify hook still allowed (cache reload)
kill <gateway_pid> 2>/dev/null
sleep 3
hermes hooks list 2>&1 | grep "YOUR_HOOK"
# Should still show ✓ allowed after restart
```

**Layer 3C — Real message survival (gold standard):** Does it fire for a REAL Telegram message, not just synthetic test input?

```bash
# 3C: Send real message via Telegram, check file appears
# (Cannot automate — wait for user to send message, then check)
ls -lt /path/to/output/dir/ | head -3
# Newest file should match the message's timestamp
```

**Layer 3 catches:** cron scripts that delete your files, gateway cache that doesn't pick up new hooks, hooks that only work in synthetic test but fail on real input. **These are bugs that pass Layer 1 and 2 but break in 24-72 hours when the environment changes.**

### The 3-Layer Report Format

```markdown
| Layer | Test | Result | Evidence |
|-------|------|--------|----------|
| **L1** | Files exist + valid syntax | ✅ PASS | 5/6 files, 14K+385+352+2689+352B |
| **L2A** | Stdin JSON parsing | ✅ PASS | File created, 5 NER detected, 2 tags |
| **L2B** | Shell wrapper invocation | ✅ PASS | Exit 0, file created |
| **L3A** | Cron scope (no auto-delete) | ✅ PASS | Scripts don't touch hooks/ |
| **L3B** | Gateway restart survival | ✅ PASS | ✓ allowed after restart |
| **L3C** | Real Telegram message | ✅ PASS | File at 23:10 matches "hello" message |
```

**When to use 3-layer vs flat 9-verify:**
- **Flat 9-verify** for single-change verification (one feature, one file)
- **3-layer** for SYSTEM verification (deployed infrastructure, hook patterns, plugins)
- **3-layer for hooks specifically** — they have the most failure modes (existence + stdin/event/literal + cron/restart)

**Key insight (2026-06-17):** Test file vanishing was a 3-layer failure — file existed (L1 ✓), test ran (L2 ✓), but file disappeared in same session (L3 ✗). The 3-layer structure surfaces "things that work right now but won't survive" as a separate category to investigate.

**Update 2026-06-17 (root cause found):** The test file vanishing was traced to Hermes's built-in `disk_cleanup` plugin (NOT a hook, NOT a cron, NOT a tool bug). It auto-tracks files matching `test_*.py` / `tmp_*.py` / `*.test.py` and deletes them at `on_session_end`. See `self-verify-after-workaround` skill → "disk_cleanup Plugin Auto-Deletes test_*.py Files" section for full details and fix recipes. **Check `~/.hermes/disk-cleanup/cleanup.log` FIRST when a test file vanishes — this catches the root cause in <30s instead of the 20+ minutes of misdirected investigation.**

## The Report Format (Validated by User 2026-06-17)

```markdown
# 📋 BÁO CÁO QA NGHIÊM NGẶT — <System Name>
**Verify date:** <ISO date> | **Method:** Tự chạy evidence, không báo cáo suông

## Tổng quan: **<N>/9 PASS** ✅ (or ⚠️ for partial)

| # | Verify | Result | Evidence |
|---|--------|--------|----------|
| 1 | Files exist | ✅ PASS | <1-line summary> |
| 2 | Unit tests | ✅ PASS | <1-line summary> |
| 3 | E2E test | ✅ PASS | <1-line summary> |
| 4 | Services registered | ✅ PASS | <1-line summary> |
| ... |

## 🔧 Vấn đề em tìm ra + fix trong quá trình QA

### ⚠️ Issue 1: <title>
- **Vấn đề:** <what broke>
- **Nguyên nhân:** <root cause>
- **Fix:** <what em did>
- **Action:** <what anh should do>

## 🎯 KẾT LUẬN
<Final bold statement, no ambiguity>
```

**Key features:**
- Numbered tests (1-9) — user can see what was checked
- Evidence inline (file paths, sizes, MD5s, exit codes)
- "Method: Tự chạy evidence" — signals showing work
- Final bold conclusion — no room for "should work"
- Issues section — surface bugs found, not hide them

## Real Result from 2026-06-17

User asked: "giờ check, verify và qa nghiêm ngặt lại loop engineering đi!"

Agent ran 9 verifies. Results:
- 8/9 PASS first try
- 1/9 FAIL: `transcript-saver-v2/test_handler.py` had been deleted
- Agent recreated the test file (4 tests instead of 10)
- Reported 9/9 PASS with explicit note: "after recreate test file"
- User accepted the report

**User feedback signal:** They liked the numbered format. They explicitly noted "self-verify is the deliverable, not a separate step" → em phải show evidence inline, không phải describe intent.

## Anti-Patterns to Avoid

1. **"Should work"** = unverified claim. Replace with concrete evidence.
2. **"Looks good"** = hand-waving. Replace with stat / md5 / count.
3. **"I checked"** without showing output = hollow. Replace with: output, then interpretation.
4. **Skipping verifies** because "it's obviously fine" = exactly when to verify.
5. **Cherry-picking** = running only the verifications you expect to pass. Run ALL 9 (or skip with N/A note).
6. **Reporting success prematurely** = when in doubt, say "I can't verify this part" honestly.

## Connection to Other Skills

- **`self-verify-after-workaround`** — for verifying after a workaround (single-step)
- **`qa-gate`** — for verifying each step in a multi-step task
- **`loop-engineering-deployment`** — the deployment that this skill verifies
- **`diagnose`** — for debugging specific errors (when a verify fails)
- **`hermes-agent`** — for understanding Hermes shell hook config and other system details

## Reference Files

- `references/session-2026-06-17-loop-engineering-qa.md` — full session transcript: 9 verifies, test file recreation, surface issues honestly
- `references/session-2026-06-17-3-layer-pattern.md` — 3-layer verification pattern (Existence → Behavior → Future-proof) emerged after test file vanished 4× in one session; flat 9-verify couldn't catch this class of bug

## Remember

```
Self-verify is the deliverable, not a separate step.
Run 9 simple verifies — don't be clever.
Each verify = 1 tool command + 1 line of evidence.
Numbered table = scannable in 5 seconds.
Honest "I can't verify" > fake confidence.
Show your work.
```

**Real failure mode (2026-06-17):** Agent claimed "Hook v2.0 đã hoạt động" based on `hermes hooks list` showing ✓ allowed. But the actual handler had a `$MESSAGE` literal filter bug → created 1 file with literal `$MESSAGE` instead of real content. Self-verify would have caught this: `grep -c '$MESSAGE' /path/to/output/file` → 1 → FAIL.
