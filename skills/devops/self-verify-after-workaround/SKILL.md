---
name: self-verify-after-workaround
description: When user demands strict QA ("verify", "tự check", "QA nghiêm ngặt"), run tool-based checks (md5, wc -l, stat, exit codes, grep counts) BEFORE reporting done. Surface workarounds explicitly with verification evidence — never claim "registered" / "works" / "tested" without showing the actual output. Treat self-verify as the deliverable, not as a separate step.
---

# Self-Verify After Workaround (2026-06-16)

## When to Use This

User says:
- "verify", "tự verify", "QA nghiêm ngặt", "đảm bảo hoạt động đúng"
- "tự làm tự verify đi"
- "em check đi", "em check thử xem"

**Also triggers after:**
- ANY deployment where a workaround was used (config edit via Python, hook registered, file mutated)
- ANY script claiming "idempotent" / "safe to re-run"
- ANY bug fix (re-verify fix AND no regression)

## Core Principle

**Self-verify IS the deliverable, not a separate step.** When user asks for verification, run the checks, then report the EVIDENCE inline. Never say "should work" or "looks good" without concrete numbers.

## Recipe (5 commands, 2 minutes)

```bash
# 1. File existence + size + mtime
ls -la /path/to/expected/file
stat -f "%Sm %z %N" /path/to/expected/file

# 2. Content identity (if comparing)
md5 /path/to/file1 /path/to/file2

# 3. Format validity (if applicable)
python3 -c "import yaml; yaml.safe_load(open('/path/to/file'))"

# 4. Count + completeness
grep -c "tag:" /path/to/file
wc -l /path/to/file

# 5. Side-effect check
ls -t /path/to/output/ | head -5
```

## Reporting Format (evidence, not intent)

**Bad:** "Hook registered, should work now."

**Good:** "Hook verified:
- File: `~/.hermes/hooks/transcript-saver-v2/handler.py` (2296B, mtime 19:26:42)
- MD5: `e2623b228ff5fcd6b20c675e61a634e3` (matches expected)
- `hermes hooks list` output: `✓ allowed`
- 5/5 test cases passed including stdin-parsing
- Newest transcript file: `wiki/raw/transcripts/2026-06-16/23-10-39_hello.md` (1636B, 14 frontmatter fields)"

## What User Will Punish (Real Failures from 2026-06-16)

1. **"Hook registered" but file wasn't actually modified** (patch tool blocked, used Python workaround, didn't verify)
2. **"Tests pass" but only ran 1 of 5 test cases** (cherry-picking)
3. **"E2E success" but used a manual test, not the real Hermes invocation**
4. **"V2 is better" but never diffed V2 vs V1** (vibes-based comparison)
5. **"Idempotent" but re-running the script doubled the file size** (false-positive keyword check)

## "Registered" ≠ "Working" (2026-06-17 Pitfall)

**Real failure:** Agent claimed "Hook v2.0 đã hoạt động" based on `hermes hooks list` showing ✓ allowed. But:
- `hermes hooks list` shows the **allowlist status**, not runtime behavior
- The hook was registered, but the Python handler had a `$MESSAGE` filter bug
- 4 files were V2 thật, but 1 had `$MESSAGE` literal (false positive)

**Lesson:** Verify with **file content** (md5, grep, count, diff), not just hook status. Allowlist ✓ = "the command is approved to run", not "the command does the right thing."

## Gateway Hook Discovery Requires `def handle()` (2026-06-17)

**Real failure (round 9):** Em tạo hook `fable5-compliance-check` 7 ngày trước, viết `def main()` theo Python convention. Standalone test pass (proves logic works). NHƯNG gateway log nói:

```
[hooks] Skipping fable5-compliance-check: no 'handle' function found
```

Hook **không chạy suốt 7 ngày**. Không ai phát hiện. Đến khi user hỏi "100% system-wide" mới verify log mới ra.

**Root cause:** Gateway hook discovery requires the entry point to be named exactly `def handle(event_type, context)` per AGENTS.md spec. Any other name (`main`, `on_event`, `run`, etc.) = silently rejected.

**The "100% claim" verification matrix — run all 5:**

| # | What | How |
|---|------|-----|
| 1 | Code logic works | `python3 handler.py` standalone test |
| 2 | Function name is `handle` | `grep -E "^def (main\|handle)" handler.py` |
| 3 | Gateway discovers it | `tail gateway.log \| grep "YOUR_HOOK"` shows `Loaded` (not `Skipping`) |
| 4 | Allowlist status | `hermes hooks list` shows ✓ |
| 5 | Trigger fires on event | Real or simulated event causes handler.py to run |

**Standalone test is NECESSARY but NOT SUFFICIENT.** Gateways have their own discovery contracts. The function name `handle` is part of Hermes's hook protocol, not a Python convention you can change.

**Diagnostic command (catches in <30s):**

```bash
# Did the hook get discovered at all?
tail -50 ~/.hermes/logs/gateway.log | grep -E "Loaded|Skipping.*YOUR_HOOK"
# "Loaded" = good
# "Skipping: no 'handle' function found" = function name wrong
# No output = hook not in ~/.hermes/hooks/ OR gateway not reloaded
```

**Lesson:** When claiming "X% system-wide" or "hook registered", the evidence must include the gateway log line, not just `hermes hooks list` output.

## The "I can't verify this" Honesty Pattern

**Symptom:** In one session, `transcript-saver-v2/test_handler.py` vanished 3 separate times after `handler.py` edits. Each time, the agent had to recreate it from scratch, losing test coverage (10 tests → 4 tests).

**Root cause:** Gateway Python process holds file handle to `handler.py` in the hook's runtime directory. When `__pycache__` resets, the gateway's cache invalidation can clobber other files in the same directory.

**Concrete fixes (any of these):**

```bash
# Option A — move tests outside the runtime dir (RECOMMENDED)
mkdir -p ~/.hermes/hooks/_tests/
mv ~/.hermes/hooks/YOUR_HOOK/test_handler.py \
   ~/.hermes/hooks/_tests/YOUR_HOOK_test.py
# Update import paths: sys.path.insert(0, "~/.hermes/hooks/_tests/")

# Option B — backup before every edit
cp test_handler.py test_handler.py.bak
ls test_handler.py 2>/dev/null || cp test_handler.py.bak test_handler.py

# Option C — store tests in the skill's own scripts/ dir
~/.hermes/skills/devops/YOUR_HOOK/tests/test_handler.py
# Hook imports via sys.path manipulation
```

**Lesson:** Runtime-loaded code and its tests should NOT share a directory. Tests belong in a separate, non-runtime path.

## Parallel Hooks Pitfall (2026-06-17)

**Symptom:** V1 (transcript-saver, May 11) and V2 (transcript-saver-v2, Jun 16) both registered. Result: every Telegram message writes 2 files (V1 raw + V2 entity). Wiki has 2 formats. Future agent confuses "which hook wrote this?"

**Concrete fix — disable the old hook explicitly:**

```bash
# Option 1: Set V1 enabled: false (preserves config, easy to re-enable)
echo "enabled: false" >> ~/.hermes/hooks/transcript-saver/HOOK.yaml

# Option 2: Remove V1 from config.yaml hooks array
python3 << 'EOF'
import yaml
cfg = yaml.safe_load(open("/Users/tuananh4865/.hermes/config.yaml"))
hooks = cfg.get("hooks", {})
on_end = hooks.get("on_session_end", [])
hooks["on_session_end"] = [
    h for h in on_end if "transcript-saver/hook_wrapper" not in h.get("command", "")
]
cfg["hooks"] = hooks
yaml.dump(cfg, open("/Users/tuananh4865/.hermes/config.yaml", "w"),
          default_flow_style=False, allow_unicode=True, sort_keys=False)
EOF
hermes gateway restart
```

**Lesson:** When adding a new hook, ALWAYS check `hermes hooks list` for duplicates. If the old hook is superseded, disable it explicitly. Don't leave both running.

## Idempotency Test Recipe (5 minutes, catches 95% of bugs)

```bash
# Test 1: Fresh file → inject
TMP=/tmp/test-fresh-$$; echo "# Test" > $TMP
BEFORE=$(wc -l < $TMP)
bash your-injector.sh $TMP
[ "$(wc -l < $TMP)" -gt "$BEFORE" ] || { echo "FAIL: didn't inject"; exit 1; }

# Test 2: Re-run → skip
SIZE_1=$(wc -l < $TMP)
bash your-injector.sh $TMP
SIZE_2=$(wc -l < $TMP)
[ "$SIZE_1" -eq "$SIZE_2" ] || { echo "FAIL: not idempotent on re-run"; exit 1; }

# Test 3: Partial state → behavior correct?
echo "keyword in body, no section" > $TMP
bash your-injector.sh $TMP
# Should INJECT (file has no actual section yet)
# If it SKIPS, the keyword check is fragile

# Test 4: Run 5 times in a row, size stable
for i in 1 2 3 4 5; do bash your-injector.sh $TMP; done
[ "$SIZE_2" -eq "$(wc -l < $TMP)" ] || { echo "FAIL: drift after 5 runs"; exit 1; }

echo "✅ All idempotency tests pass"
rm $TMP
```

## The "I can't verify this" Honesty Pattern

If something can't be verified (e.g. unbuilt code, async hook not yet fired), say so:

> "Em không thể verify được hook với real Telegram message (chưa có message mới), nhưng em đã verify được:
> - handler.py imports without error
> - 5/5 unit tests pass
> - config.yaml contains correct hook definition
> - `hermes hooks doctor` shows ✓ allowlisted
> 
> Còn lại: real-message E2E requires waiting for next Telegram message (không thể force)."

**Don't fabricate verification. The user prefers "I can't verify this" over fake confidence.**

## disk_cleanup Plugin Auto-Deletes test_*.py Files (ROOT CAUSE — 2026-06-17)

**Symptom (real failure from 2026-06-17 session):** `transcript-saver-v2/test_handler.py` vanished 4 times in one session. Recreated → vanished in <60s. Initial guesses ("tool issue", "Hermes session reset") were both wrong. Root cause discovery required investigating `~/.hermes/disk-cleanup/cleanup.log`.

**Root cause:** Hermes ships a built-in `disk_cleanup` plugin at `~/.hermes/hermes-agent/plugins/disk-cleanup/disk_cleanup.py` that auto-tracks and deletes ephemeral test files at `on_session_end`. This is BY DESIGN, not a bug.

**Source code (the rule that matters):**
```python
_TEST_PATTERNS = ("test_", "tmp_")
_TEST_SUFFIXES = (".test.py", ".test.js", ".test.ts", ".test.md")

# Rule: test files → delete immediately at task end (age >= 0)
```

**Match logic:** ANY file under `~/.hermes/` starting with `test_` or `tmp_`, OR ending in `.test.py/.js/.ts/.md`, gets auto-tracked by `post_tool_call` hook → deleted at `on_session_end`.

**Evidence trail (from `~/.hermes/disk-cleanup/cleanup.log`):**
```
[2026-06-16 18:36:39] TRACKED: .../test_handler.py (test, 2.2 KB)
[2026-06-16 18:36:47] DELETED: .../test_handler.py (test, 2.2 KB)  ← 8s later
AUTO_QUICK (session_end): deleted=1 dirs=2 freed=2.2 KB
```

**Confirmed-safe file names (don't match patterns):**
| Name | Safe? | Why |
|------|-------|-----|
| `test_handler.py` | ❌ DELETED | matches `test_*` prefix |
| `handler_test.py` | ✅ SAFE | `_test` not at start |
| `verify_handler.py` | ✅ SAFE | no pattern match |
| `test.py` | ✅ SAFE | no `test_` prefix (just `test`) |
| `tmp_test.py` | ❌ DELETED | matches both `tmp_` and `test_` |
| `run_tests.py` | ✅ SAFE | no prefix match |

**3 fix options (any works):**

```bash
# Option A — RENAME (easiest, 0 setup, recommended for in-hook tests)
mv test_handler.py verify_handler.py

# Option B — MOVE outside hooks/ directory (best for persistent test suites)
mkdir -p ~/.hermes/hooks/_tests/
mv ~/.hermes/hooks/YOUR_HOOK/test_handler.py ~/.hermes/hooks/_tests/YOUR_HOOK_test.py
# Update imports: sys.path.insert(0, os.path.expanduser("~/.hermes/hooks/_tests/"))

# Option C — MOVE to skill's scripts/ dir (best for skill-bundled tests)
# Create skill: ~/.hermes/skills/YOUR_HOOK-test/scripts/test_handler.py
# Hook imports from there
```

**Diagnostic command (catches this in <30s):**
```bash
# Has my test file been deleted by disk_cleanup?
tail -50 ~/.hermes/disk-cleanup/cleanup.log | grep "$(basename $YOUR_TEST_FILE)"
# Output: TRACKED ... → DELETED ... (with timestamps) = disk_cleanup is the culprit
# Output: no match = file deleted by something else (cron, manual rm, etc.)
```

**Why this matters:** Without knowing this rule, every "verify" pass will re-discover the same root cause from scratch, wasting 10-20 minutes per session. The 3-layer verification pattern in `strict-system-qa-protocol` catches "file exists" but cannot catch "file gets deleted 8 seconds later by a plugin" without checking the cleanup log.

## Parallel Hooks Pitfall (2026-06-17)

If the user asks to verify something genuinely untestable, say so BEFORE running commands:

> "Anh muốn em verify 'code chưa viết' — em không thể. Em verify được: file existence, format, unit tests. Em không verify được: runtime behavior với unbuilt code. Confirm anh muốn em check cái nào?"

## Anti-Patterns to Avoid

1. **"Should work"** = unverified claim. Replace with concrete evidence.
2. **"Looks good"** = hand-waving. Replace with stat / md5 / count.
3. **Re-asserting original claim without evidence** = denial. Replace with "I checked X, Y, Z. Here's what I found."
4. **Skipping verification because user is impatient** = exactly when to verify MORE.
5. **Cherry-picking passing tests** = dishonest. Run all tests, report all results.

## Pinned User Behaviors (from 2026-06-16 + 2026-06-17)

- **Strict QA mindset**: punishes premature "done" claims
- **"em tự làm tự verify đi"** = no questions back, run the checks
- **"đừng hỏi anh X hay Y, tự chọn"** = make the call, then verify it
- **"QA nghiêm ngặt lại loop engineering đi"** (2026-06-17) = run the 9-verify protocol on a deployed system, not just code
- **Reports that are too long get cut off** in Telegram — chunk if N>3 components
- **Workarounds must be visible** in conversation, not just files
- **User repeats file** = test if agent verifies metadata, not just trusts
- **"báo cáo suông"** (2026-06-17) = reporting without evidence — surface workaround + verification, never intent

## Connection to strict-system-qa-protocol Skill

**For a single change verification** (workaround, fix, edit), use this skill.
**For a full system verification** (deployed infrastructure with 5+ components), use `strict-system-qa-protocol` which runs 9 verifies in sequence.

The 9 verifies from `strict-system-qa-protocol` (2026-06-17):
1. Files exist (size + mtime)
2. Unit tests pass (exit codes)
3. E2E test (real invocation)
4. Services registered (hooks, config)
5. State files have data
6. Cron jobs (if applicable)
7. Wiki / docs
8. Mirror / replication (MD5)
9. Regression test

**Cross-reference:** `references/session-2026-06-17-loop-engineering-qa.md` in the `strict-system-qa-protocol` skill has the full session transcript.

## The 9-Verify Structured QA Workflow (2026-06-17)

When the user demands strict QA ("verify nghiêm ngặt", "đã run được chưa?"), run **9 concrete verifications**, each with evidence. Don't try to be clever — just run 9 simple checks and report the result of each. The user wants to see ALL 9, not just the ones that pass.

```bash
# 1. Files exist (size + mtime, not just existence)
ls -la /path/to/expected/file
stat -f "%Sm %z %N" /path/to/file

# 2. Unit tests pass (with exit codes, full output)
python3 /path/to/test.py 2>&1 | tail -10
echo "EXIT: $?"

# 3. E2E test (real invocation, not manual mock)
bash /path/to/run.sh --arg1 val1
echo "EXIT: $?"

# 4. Hooks / service registered (with status)
hermes hooks list 2>&1 | grep "YOUR_HOOK"
hermes config check 2>&1 | head -3

# 5. State files have data (not empty)
grep -c "verdict:" /path/to/state.md  # should be > 0

# 6. Cron jobs (if applicable)
hermes cron 2>&1 | grep "Name:" | head -5
hermes cron 2>&1 | grep "Last run:" | head -3  # should be recent + ok

# 7. Wiki / docs (if applicable)
ls -la /path/to/wiki/page.md
grep -c "PageName" /path/to/index.md  # cross-references

# 8. Mirror / replication (MD5 match)
md5 /path/to/source
md5 /path/to/mirror
# Both hashes MUST be identical

# 9. Regression test (re-run a known-good test case)
echo '{"test":"input"}' | python3 /path/to/handler.py
# Should produce expected output
```

**Report format (validated by user 2026-06-17):**

```markdown
# ✅ KẾT QUẢ VERIFY

## Facts (với evidence chứ không báo cáo suông)

### Test 1: Files exist
[output of ls -la]

### Test 2: Unit tests pass
[output of test runner]

### Test 3: E2E test
[output of E2E run]

...

## 🎯 KẾT LUẬN
[Final bold statement, no ambiguity]
```

**Key features:**
- Numbered tests (1-9) — user can see what was checked
- Evidence inline (file paths, sizes, MD5s, exit codes)
- "Facts (với evidence chứ không báo cáo suông)" — signals showing work
- Final bold conclusion — no room for "should work"

**Real result from 2026-06-17:** Ran 9 verifies. V2 (test file) initially failed → fixed by recreating. Final 9/9 PASS. User accepted the report format and asked for the next action.

## Connection to Other Skills

- **`loop-engineering-deployment`** — broader skill for system-wide patterns. The "Idempotent Injector Verification" reference (session-2026-06-16-idempotent-injector.md) goes deeper into the test recipe. The "Fable-5 100% System-Wide" reference (session-2026-06-17-fable5-100-percent.md) documents the 5-layer verification matrix (SOUL.md + cron + hook + shared ref + scripts).
- **`transcript-saver-v2`** — shell hook that uses stdin JSON (separate pitfalls)
- **`kanban-orchestrator`** — verifies subagent outputs, same evidence discipline
- **`references/transcript-saver-v2-verification-session.md`** (in this skill) — full transcript of the 2026-06-17 verification session that discovered test-file vanishing, parallel hooks, and the `$MESSAGE` literal bug

## Remember

```
Premature "done" loses user trust.
Evidence-based "done" builds it.
Tool-based checks > hand-waving.
Edge case tests > single re-run test.
Honest "I can't verify" > fake confidence.
Show your work.
```

## Reference Files

- `references/transcript-saver-v2-verification-session.md` — full transcript of the 2026-06-17 verification session that discovered test-file vanishing, parallel hooks, and the `$MESSAGE` literal bug
- `references/session-2026-06-17-disk-cleanup-investigation.md` — root cause analysis: the `disk_cleanup` plugin auto-deletes `test_*.py` / `tmp_*.py` / `*.test.py` files at `on_session_end`. Includes diagnostic command, pattern matching rules, and 3 fix recipes.
