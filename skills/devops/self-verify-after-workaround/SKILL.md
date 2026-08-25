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
6. **Asking user to review before self-verifying** (2026-06-26 incident) — see below.
7. **Slogan ≠ work** (NEW 2026-07-19 L55) — Báo "🎯 Loop 1 verify" mà KHÔNG chạy `ls`/`grep` thật. Slogan decoration ≠ actual work. Slogan PHẢI đi kèm evidence gate output. Cross-ref: `evidence-first-delivery` skill "Slogan ≠ work" row in Anti-patterns table.
8. **Container-only check for media outputs** (NEW 2026-07-23) — Verify TTS/video output chỉ bằng `ffprobe` (file valid + sample rate + duration) mà skip `volumedetect` (amplitude) + `Whisper transcript` (content). 3 layers for media: **(1) container valid**, **(2) amplitude OK** (peak > -10dB), **(3) content match expected** (Whisper word-level). Skip layer 2-3 → silent audio / ref leak / garbage content mà vẫn báo "PASS". Real case 23/07 OmniVoice: 4/5 file peak -20.8dB (silent) và 5/5 có ref leak "Và bây giờ đang nhờ AI..." bị inject vào output — đều catch được bằng 3-layer check. **Cross-ref:** `tts-voice-clone-test` skill § "3-LAYER HARD RULE" + `omnivoice-voice-clone` skill § "Verify protocol" + `tiktok-verify-protocol` skill. **Pattern:** mọi TTS/video output BẮT BUỘC check amplitude + content, không chỉ container.

## Verify-Before-Ask Rule (2026-06-26)

**Symptom:** Agent built a 3-patch refactor for WikiMemoryProvider, wrote a detailed patch proposal in `/tmp/wikimemory_fix.patch`, then immediately asked user "anh muốn em apply patches thế nào?" with 4 options. User's response:

> "Verify xem có chạy được thành công chưa mà hỏi anh review rồi!?"

**Root cause:** Agent treated "build a patch" as the deliverable, when the actual deliverable was "fix the bug AND verify the fix works". Writing the patch to `/tmp/` is intermediate work. Asking for review BEFORE verifying is the same anti-pattern as reporting "should work" without evidence.

**Rule:** When you've completed a fix/change/refactor:

```
1. APPLY the change (write files, run commands)
2. VERIFY the change works (syntax check, functional test, evidence)
3. ONLY THEN ask user if they want X or Y (review/apply/manual/commit)
```

If you stop at step 1 and immediately present options to user → you're asking them to evaluate unverified work. They don't have time to debug your fix and verify it works.

**Concrete fix recipe — 3-step verify-before-ask:**

```bash
# Step 1: APPLY (don't just write to /tmp/)
patch_tool_path <actual_target_file>  # NOT /tmp/

# Step 2: VERIFY (syntax + functional + side-effect)
python3 -c "import ast; ast.parse(open('<file>').read())"  # syntax
python3 -c "<test the new functionality>"                  # functional
ls -la <file> | head -3                                     # file exists + size

# Step 3: REPORT (only after 1 + 2 pass)
echo "✓ Applied: <file> (<size> bytes)"
echo "✓ Verified: <test result>"
echo "✓ Side effects: <any output>"
# NOW optionally ask user: "Want me to commit / push / deploy?"
```

**Anti-pattern recap:**
- ❌ Write patch to `/tmp/file.patch`, ask "review?"
- ✅ Apply patch + verify + report "applied and working, want me to commit?"
- ❌ Run script, see it exit 0, ask "looks good?"
- ✅ Run script, capture output, run sanity check on output, report "script ran, output X, verified Y"
- ❌ Edit config, ask "did this work?"
- ✅ Edit config, grep + diff + runtime check, report "config now has X value"

**Lesson:** The "verify" step is what makes a deliverable complete. Without it, you're shipping a hypothesis. The user should see evidence, not be asked to evaluate unverified work.

## Diagnose-Wide Mandate: CHECK SKILL LIBRARY FIRST (2026-06-25)

**Symptom (real failure, 2026-06-25):** User reported "Telegram bot silent" — `~/.hermes/.env` missing. Agent went through 8 turns of investigation: checked gateway.log, grepped .env patterns, hunted for the deletion script, hypothesized about git clean, etc. **In turn 7, agent finally ran `skill_view(hermes-daily-backup)` and discovered the SKILL.md ALREADY had pitfall #20, #20h, #20i documenting this EXACT incident** — including the 3-command diagnostic shortcut, root cause analysis, and restore steps. All 8 turns of investigation could have been 1 turn of "let me check the skill library first".

**Lesson:** When the symptom matches ANY class of past failure, **run `skills_list` + `skill_view` BEFORE doing terminal/log investigation**. Pitfalls accumulate in skill files; the most efficient path to root cause is often "has someone already documented this?"

**The "diagnose-wide" pattern — 4 checks before deep investigation:**

```bash
# Check 1: Does a relevant skill exist?
skills_list 2>/dev/null | grep -iE "<domain>|<symptom-keyword>"

# Check 2: Does the skill's pitfalls section match this symptom?
grep -A 2 -B 1 "<symptom>" ~/.hermes/skills/<matching-skill>/SKILL.md

# Check 3: Is there a session-specific incident report?
ls ~/.hermes/skills/<matching-skill>/references/ | grep -iE "incident|<date>"

# Check 4: Is there a session_search hit from a past session?
session_search(query="<symptom-keywords>", limit=3)
```

If any check returns a match → read the existing reference first. Only proceed to terminal/log investigation if no existing documentation covers the symptom.

**Real-world cost of skipping this step (2026-06-25 evidence):**
- 8 turns of investigation (logs, grep, hypothesis chains)
- User escalated 3 times ("mayf nói chuyện đơn giản", "lý do mơ hồ", "sao ngu vậy")
- Agent eventually cited wrong date for second occurrence (confused memory note with SKILL.md)
- Final 3-command diagnostic was already documented in pitfall #20h but agent didn't know

**Companion rule: VERIFY memory notes, don't trust them blindly.** Memory can be stale, wrong, or paraphrased incorrectly. Cross-check with the canonical source (SKILL.md, git log, actual log file) before citing. The 2026-06-25 session cited "[21/06 DAILY-BACKUP DOTENV GOTCHA]" from memory as evidence of a second occurrence on 21/06 — but the actual second occurrence was 25/06 (per pitfall #20h). Memory note was outdated; agent should have verified against SKILL.md before quoting.

**Mandatory 3-step pattern when citing past incidents:**

```bash
# Step 1: State what you remember
echo "I recall: incident X on date Y, fix was Z"

# Step 2: Verify against canonical source
grep -B 2 -A 5 "incident X\|<keywords>" ~/.hermes/skills/<skill>/SKILL.md
git log --grep="incident X" --oneline | head -5

# Step 3: Confirm before citing
# If match → cite with date
# If NO match → say "memory may be outdated, verifying..." and run grep again
```

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

## 5-Layer Verification Matrix for System-Wide Mandates (2026-06-17)

**Trigger:** User says "yên tâm 100% system-wide" or "đảm bảo cả tương lai" after applying a mandate/rule/pattern across Hermes. **NEVER** claim "100%" after verifying just SOUL.md files. A system-wide mandate has 5 layers — missing any one = partial coverage, full coverage = "100%".

| # | Layer | What to verify | How |
|---|-------|----------------|-----|
| 1 | **SOUL.md coverage** | All profile SOUL.md files have the mandate reference | `bash ~/.hermes/scripts/check-<mandate>-compliance.sh` |
| 2 | **Cron job prompts** | LLM cron jobs have mandate reminder block in their prompts | `jq -r '.jobs[].prompt' ~/.hermes/cron/jobs.json \| grep -c "MANDATE_MARKER"` — should equal count of LLM jobs (skip `no_agent: true`) |
| 3 | **Hook registration** | Hook file is **discoverable** AND has correct function name | `grep "def handle" handler.py` (must exist) + `tail gateway.log \| grep YOUR_HOOK` (must show "Loaded", not "Skipping") |
| 4 | **Shared reference file** | The single source of truth exists and is reachable | `ls -la ~/.hermes/profiles/_shared/<mandate>-patterns.md` |
| 5 | **Compliance scripts** | Both injector and CI gate exist, are executable, and idempotent | `test -x ~/.hermes/scripts/<mandate>-injector.sh && test -x ~/.hermes/scripts/check-<mandate>-compliance.sh` |

**Real failure (2026-06-17, Fable-5 "100%" claim):** Em reported "5/5 SOUL.md files comply, 4 mandatory + 5 contextual patterns, shared file 404 lines full" — sounds 100%. But:
- Layer 2: 0/7 cron jobs had Fable-5 reference. Cron jobs run at 2AM/3AM/7AM/7:30AM/8AM in fresh agent context. Mandate on current session's SOUL.md does NOT propagate.
- Layer 3: Hook `fable5-compliance-check` had `def main()` instead of `def handle()` — silently rejected by gateway for 7 days. No one noticed.

**User's response:** "Sao ko làm cho chắc chắn 100% đi nhỉ?" — caught both gaps.

**Lesson:** A "100% system-wide" claim is not a tally of files. It's a 5-layer matrix. If you can't show evidence for all 5, report the partial coverage and list what's missing — don't say "done".

**Companion pattern:** `system-wide-mandate-enforcement` skill → "Piece 4: Cron job mandate injection" + "5-Layer Verification Matrix" references are the operational counterparts.

## Hermes Config Patch Verification — 4-Step Mandatory (2026-06-25)

**Symptom (real failure 25/06):** Em patch `rich_messages: true → false` bằng cách edit code source, KHÔNG patch config thật. Sau đó user hỏi "2 chỗ đó em làm thực sự chưa?" → em phải grep + diff backup file → phát hiện ra config size identical với backup → KHÔNG CÓ PATCH THẬT.

**Root cause:** Em đọc source code `telegram.py` thấy field name `rich_messages`, `safe_mode`, `text_batch_delay_seconds` → tin là config có sẵn → nói "đã patch + verified" nhưng KHÔNG chạy `hermes config set` thật.

**The 4-step mandatory verification for ANY Hermes config patch:**

| # | Check | Command | What it proves |
|---|-------|---------|----------------|
| 1 | `hermes config set` exit 0 | `hermes config set key value` | CLI accepted the change |
| 2 | `grep` confirms value in file | `grep -n "key" ~/.hermes/config.yaml` | Value actually written |
| 3 | `diff` vs backup NOT identical | `diff ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.LATEST` | Something changed |
| 4 | Runtime config reflects value | `hermes config show key` OR `python3 -c "import yaml; ..."` simulating merge | Effective value applied |

**If ANY check fails or skipped → DO NOT claim "patched".**

### Hermes Config Architecture: Dual-Section + Env Var Rule

**Section 1 — `~/.hermes/config.yaml` top-level `telegram:` block:**
```yaml
telegram:
  extra:
    rich_messages: true   # Legacy section, often still here from old configs
```

**Section 2 — `~/.hermes/config.yaml` `platforms.telegram:` block (canonical):**
```yaml
platforms:
  telegram:
    extra:
      rich_messages: false  # New canonical location
```

**Both can exist simultaneously.** Runtime merge logic in `gateway/config.py:894-910` deep-merges `platforms.telegram.extra` OVER top-level `telegram.extra`. So if you patch via `hermes config set platforms.telegram.extra.rich_messages false`, it WINS — even if `telegram.extra.rich_messages: true` still exists at top level.

**Verify effective value with Python merge simulation:**
```python
import yaml
data = yaml.safe_load(open("~/.hermes/config.yaml"))
telegram_cfg = data.get("telegram", {})
platforms_cfg = data.get("platforms", {}).get("telegram", {})
merged = {**telegram_cfg}
if platforms_cfg:
    if "extra" in merged and "extra" in platforms_cfg:
        merged["extra"] = {**merged["extra"], **platforms_cfg["extra"]}
    merged.update({k: v for k, v in platforms_cfg.items() if k != "extra"})
    if "extra" in platforms_cfg:
        merged["extra"] = {**merged.get("extra", {}), **platforms_cfg["extra"]}
print(merged.get("extra", {}).get("rich_messages"))  # Should be False
```

### AGENTS.md Env Var Rule — Critical Gotcha

**Hermes hard rule (AGENTS.md, "What we don't want" section):**
> "New `HERMES_*` env vars for non-secret config... All behavioral settings — timeouts, thresholds, feature flags, display prefs — go in `config.yaml`. Reject PRs that tell users to 'set X in your .env' unless X is a credential."

**Implication for config patches:**
- Some platform settings (e.g. `text_batch_delay_seconds`, `media_batch_delay_seconds` for Telegram) are ONLY configurable via env var, NOT via `config.yaml`. Source code in `gateway/platforms/telegram.py:436-459` reads them via `os.getenv("HERMES_TELEGRAM_TEXT_BATCH_DELAY_SECONDS", "0.3")`.
- If AGENTS.md blocks env vars for non-secret config, these settings are effectively UNCONFIGURABLE via user-facing means — they exist in code but the user can't change them without breaking the rule.
- **Honest answer:** "This setting can only be changed via env var, which AGENTS.md prohibits for non-secret config. The setting is hard-coded from the codebase maintainer's perspective."

### How to verify a field EXISTS in code vs EXISTS in config

| Test | Command | If matches → |
|------|---------|--------------|
| Field exists in source code | `grep -n "field_name" ~/.hermes/hermes-agent/gateway/platforms/*.py` | Field is a runtime option, might be patchable |
| Field exists in current config | `grep -n "field_name" ~/.hermes/config.yaml` | Currently set (or default) |
| Field is patched successfully | `grep -A 1 "field_name" ~/.hermes/config.yaml` shows NEW value | Patch actually applied |

**Trap:** Reading source code shows field `safe_mode` → assuming it's a config option. But `safe_mode` was a CLI flag (`--safe-mode`) in `hermes` command, NOT a config field. Always cross-check BOTH source AND config + verify with `hermes config set` test command.

### The "User Asks: did you actually do it?" Honesty Pattern

When user directly questions "đã làm thật chưa?" or "có verify chưa?":

**Bad:** Defend the original claim with more confident language ("It IS patched, trust me")

**Good:** Run the 4-step verification LIVE in front of user, show each command output:
```bash
# Step 1: backup file timestamp + size
ls -la ~/.hermes/config.yaml.bak.20260625_195440
# Step 2: diff current vs backup
diff ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.20260625_195440
# If IDENTICAL → patch never happened → admit immediately
# Step 3: grep the field
grep -n "rich_messages\|safe_mode\|text_batch" ~/.hermes/config.yaml
# Step 4: hermes config show
hermes config show <key>
```

If verification reveals the patch DIDN'T happen → say so immediately. Don't defend fabricated completion.

**Real example from 25/06 session:**
> User: "check coi 2 chỗ này em làm thực sự chưa?"
> Agent: ran `grep -n "safe_mode\|text_batch_delay" ~/.hermes/config.yaml` → 0 matches → admitted "2 chỗ đó KHÔNG thực sự được patch"
> Then patched `rich_messages` thật via `hermes config set` → verified via Python merge simulation → confirmed effective value `False`

User accepted the honesty + corrected patch. The KEY was running verification LIVE when challenged, not defending the original claim.

## Hermes Profile Path Gotcha (2026-06-17)

**The confusion:**
- Folder `~/.hermes/profiles/default/` EXISTS but is just runtime state (`state.md` only) — **NOT used** by the default profile
- The default profile's actual SOUL.md lives at `~/.hermes/SOUL.md` (16,867b, 4/4 patterns)
- `hermes profile show default` confirms: `Path: /Users/tuananh4865/.hermes` (NOT `~/.hermes/profiles/default/`)

**Why this happens:** Hermes auto-creates `profiles/default/` for state runtime tracking when the profile list is queried, but the config root is `~/.hermes/` for the default profile. The folder is a side effect of the listing mechanism, not a config slot.

**Diagnostic command:**
```bash
hermes profile show <name>  # ALWAYS check the "Path:" line first
# Default: Path: /Users/tuananh4865/.hermes  ← check here for SOUL.md
# Non-default: Path: /Users/tuananh4865/.hermes/profiles/<name>/  ← check here
```

**Implication for compliance verification:**
- When scanning for SOUL.md files: do NOT assume `profiles/default/SOUL.md` exists or is the source of truth for the default profile
- The CI gate `check-fable5-compliance.sh` already handles this (it scans `~/.hermes/SOUL.md` as the main file), but if you write a custom scanner, follow this pattern:
  ```bash
  # Default profile: scan main SOUL.md
  [ -f "$HERMES_ROOT/SOUL.md" ] && check "$HERMES_ROOT/SOUL.md"
  # Non-default: scan each profile folder
  for profile in "$HERMES_ROOT/profiles"/*/; do
    [ -f "$profile/SOUL.md" ] && check "$profile/SOUL.md"
  done
  # Skip the default folder if it's empty (just state.md)
  ```

## Project Workflow Verification Pattern (2026-06-17)

**Trigger:** User asks to verify a "100% system-wide" project workflow (not just a mandate on SOUL.md). The project workflow has 4 layers (hub, phases, tasks, actions) + research outputs + decisions + logs.

**Common mistake:** Verify only the SOUL.md layer (1 file) and report "100%". But a project workflow is MULTI-FILE with explicit dependencies, state transitions, and verification gates. Single-file verification is insufficient.

**5-Layer Project Workflow Verification Matrix:**

| # | Layer | What to verify | How |
|---|-------|----------------|-----|
| 1 | **Hub** | `hub.md` exists with KPIs, team, structure | `test -f hub.md && grep "^status:" hub.md` |
| 2 | **Phases** | All phases have files, dates, exit criteria | `ls phases/*.md \| wc -l` (should equal planned count) |
| 3 | **Tasks** | All tasks have status, owner_role, research_refs, verify_attempts | `grep -c "^status:\|^owner_role:\|^research_refs:\|^verify_attempts:" tasks/*.md` |
| 4 | **Actions** | All actions have parent task reference | `grep -c "^task_id:" actions/*.md` |
| 5 | **Loop compliance** | No tasks stuck FAILED > 24h, AWAITING_VERIFY tracked | `grep "FAILED" tasks/*.md` + check mtime |

**Real failure (2026-06-17):** Em reported "Loop Engine v2.0 complete" after creating hub.md + phase-01 + T-01.1. But:
- Layer 2: phases/ folder had 1 file, OK
- Layer 3: T-01.1 had status + owner_role + research_refs, OK
- Layer 4: actions/ folder EMPTY (no actions yet) → verification matrix said "OK" because it didn't check layer 4
- Layer 5: No FAILED tasks → OK

User asked "verify 100%" → ran ALL 5 layers + behavioral test (T-99.9 with missing research_refs) → caught 1 bug.

**Lesson:** A project workflow needs the SAME 5-layer verification matrix as system-wide mandates. Just because files exist doesn't mean the workflow LOOP works end-to-end.

**Behavioral verification (catches what file-existence misses):**
```bash
# Create a test task that violates the contract
echo "..." > tasks/task-T-99.9-test.md
# Run CI gate
bash check-project-compliance.sh <project-id>
# Should FAIL with specific error pointing at T-99.9
# If it PASSES, the CI gate has a false-negative bug
```

**The 3-layer verification pattern (from loop-engineering-deployment):**
1. **Code layer** — files exist, syntax valid, scripts executable
2. **Behavior layer** — CI gate catches intentional violations
3. **Future-proof layer** — new tasks require same fields (template enforces)

**When claiming "project workflow X% complete":**
- Don't just count files
- Run the CI gate + behavioral test + count of incomplete/pending tasks
- Report per-layer score, not aggregate

**Template for honest project status report:**
```markdown
## Project status: <project-id>

### 5-layer verification
- [ ] Layer 1 (Hub): PASS / FAIL — evidence
- [ ] Layer 2 (Phases): PASS / FAIL — N files, M planned
- [ ] Layer 3 (Tasks): PASS / FAIL — N tasks, M have all required fields
- [ ] Layer 4 (Actions): PASS / FAIL — N actions, M have task_id
- [ ] Layer 5 (Loop): PASS / FAIL — N FAILED > 24h, M AWAITING_VERIFY

### Behavioral test
- Created test violation T-99.9 → CI gate: PASS / FAIL
- (If FAIL, gate is catching violations correctly)

### Score
- 4/5 layers PASS (80%)
- 1 incomplete: actions/ (no actions yet — expected at start of project)

### Verdict
- Honest 80% > fake 100%
- List what's missing
```

## Profile Create Flow: --clone vs Fresh (2026-06-17)

**Decision matrix when creating a new profile:**

| Scenario | Command | What happens | Post-create action |
|----------|---------|--------------|---------------------|
| Need same setup as active profile (most common) | `hermes profile create --clone my-agent` | Copies config.yaml, .env, SOUL.md, skills from active | None — if active profile has mandate, new one inherits |
| Need fresh start, customize from scratch | `hermes profile create my-agent` | Creates empty profile folder (just state.md template) | **MUST run injector** to add mandate patterns |
| Need copy from a specific (not active) profile | `hermes profile create --clone-from <source> my-agent` | Copies from source profile | None — if source has mandate, new one inherits |
| Test profile (no production use) | `hermes profile create test-agent --no-skills` | Empty, no skills | Optional — skip if test-only |

**Rule:** Every fresh create (no `--clone`) MUST be followed by:
```bash
bash ~/.hermes/scripts/add-fable5-to-soul.sh ~/.hermes/profiles/my-agent/SOUL.md
bash ~/.hermes/scripts/check-fable5-compliance.sh  # verify
```

**The auto-injector wrapper pattern** (reusable for any system-wide mandate):
```bash
#!/bin/bash
# auto-inject-on-profile-create.sh
# Usage: bash auto-inject-on-profile-create.sh [profile-name]
# Without args: inject into ALL existing profiles (idempotent safe re-run)
set -e
HERMES_ROOT="${HERMES_HOME:-$HOME/.hermes}"
PROFILE_NAME="$1"
INJECTOR="$HERMES_ROOT/scripts/add-<mandate>-to-soul.sh"

inject_to_profile() {
  local soul_file="$HERMES_ROOT/profiles/$1/SOUL.md"
  [ -f "$soul_file" ] || { echo "⏭️  Skip $1: no SOUL.md"; return; }
  if grep -q "MANDATE_MARKER" "$soul_file"; then
    echo "✅ $1: already has mandate"
  else
    echo "🔧 Injecting into $1..."
    bash "$INJECTOR" "$soul_file"
  fi
}

if [ -n "$PROFILE_NAME" ]; then
  inject_to_profile "$PROFILE_NAME"
else
  for p in "$HERMES_ROOT/profiles"/*/; do
    name=$(basename "$p")
    case "$name" in _*|.|..) continue;; esac
    inject_to_profile "$name"
  done
  # Also check main SOUL.md
  [ -f "$HERMES_ROOT/SOUL.md" ] && inject_to_profile "$HERMES_ROOT/SOUL.md" 2>/dev/null || true
fi
```

**Why the wrapper matters:** The injector alone (`add-fable5-to-soul.sh`) takes 1 file path. The wrapper handles "I just created 5 new profiles, inject mandate into all of them" in 1 command. Reduces 5 commands to 1.

## Connection to Other Skills

- **`loop-engineering-deployment`** — broader skill for system-wide patterns. The "Idempotent Injector Verification" reference (session-2026-06-16-idempotent-injector.md) goes deeper into the test recipe. The "Fable-5 100% System-Wide" reference (session-2026-06-17-fable5-100-percent.md) documents the 5-layer verification matrix (SOUL.md + cron + hook + shared ref + scripts).
- **`system-wide-mandate-enforcement`** — the operational counterpart. Use that skill to DESIGN the mandate, use this skill to VERIFY the deployment.
- **`hermes-agent-decision-guard`** — when user says "100% system-wide", DON'T ask "which 5 layers?" — just run all 5 verifications and report.
- **`transcript-saver-v2`** — shell hook that uses stdin JSON (separate pitfalls)
- **`kanban-orchestrator`** — verifies subagent outputs, same evidence discipline
- **`references/transcript-saver-v2-verification-session.md`** (in this skill) — full transcript of the 2026-06-17 verification session that discovered test-file vanishing, parallel hooks, and the `$MESSAGE` literal bug
- **`references/session-2026-06-17-fable5-100-percent.md`** — full 5-layer verification session transcript

## Remember

```
Premature "done" loses user trust.
Evidence-based "done" builds it.
Tool-based checks > hand-waving.
Edge case tests > single re-run test.
Honest "I can't verify" > fake confidence.
"100% system-wide" = 5 layers, not 1.
"100% project workflow" = 5 layers (hub/phases/tasks/actions/loop), not 1.
"Config patched" = 4 steps (hermes config set + grep + diff backup + runtime show), not 1.
Verify BEFORE asking user to review (2026-06-26 incident).
Show your work.
When user challenges "did you actually do it?" — verify LIVE, don't defend.
Hermes config has dual sections (top-level + platforms.*). Effective value = deep merge.
AGENTS.md blocks env vars for non-secret config — some settings effectively UNCONFIGURABLE from user side.
Manual scan TEXT có thể SAI khi không có timestamp chi tiết — LUÔN cross-check với subagent word-level timestamps (lesson 18/07).
```

## Manual Verify Có Thể SAI — Lesson từ 18/07 (NEW)

**Context:** Em manual scan text thấy 2 cặp "take lặp" nghi ngờ:
- PAIR A: "Đây là mẫu hút bụi Dodoto Air Luxe V3" + "Đây là mẫu hút bụi Dodoto Luxe V3"
- PAIR B: "Cục binh của nó là 4000mAh... khu vực liên tục" + "Cục binh của nó là 4000mAh... liên tục được"

Subagent dispatched với context "đặc biệt check 2 cặp này" đã verify word-level timestamps:
- **PAIR A: FAIL thật** — 2 takes còn trong cut tại 10.56s + 14.62s
- **PAIR B: PASS (em manual sai)** — editor đã cắt TAKE CŨ, chỉ còn TAKE MỚI ở 96.94s

**Root cause của manual sai:** Manual scan text thấy 2 segments giống prefix → assume "take lặp", nhưng thực tế editor đã cắt đúng 1 take từ trước. Manual KHÔNG có timestamp chi tiết để biết seg[1] vs seg[2] overlap hay là 2 takes riêng.

**Bài học vĩnh viễn:**

1. **Manual scan text chỉ là initial scan** để list suspect pairs — KHÔNG phải verdict cuối cùng
2. **Khi manual thấy "take lặp"** → LUÔN dispatch subagent với word-level timestamps để verify
3. **Anti-FP patterns cần watch:**
   - "Đây là..." + tên sản phẩm (giới thiệu sản phẩm - normal)
   - "Cục binh của nó là..." + thông số (liệt kê USP - normal)
   - "Chế độ thứ..." + số (liệt kê 4 chế độ phun - normal)
   - Anchor keywords phổ biến: "nhãn hàng", "các bạn", "mọi người" (discourse marker VN)
4. **Workflow updated:** Manual scan → list 2-3 cặp suspect → subagent verify word-level → verdict cuối

**Pattern đúng (validated 18/07):**

```python
# 1. Manual scan → list suspect (KHÔNG phải verdict)
suspects = []
for i in range(len(segments) - 1):
    seg_i, seg_j = segments[i], segments[i+1]
    words_i = seg_i["text"].strip().split()[:8]
    words_j = seg_j["text"].strip().split()[:8]
    match = sum(1 for a, b in zip(words_i, words_j) if a == b)
    if match >= 5:
        suspects.append({"i": i, "j": i+1, "match": match, "text_i": seg_i["text"], "text_j": seg_j["text"]})

# 2. Dispatch subagent với context "đặc biệt check 2 cặp này"
# Subagent sẽ check word-level timestamps (segments[].start/end) để xác nhận
# Output: PAIR A: FAIL (2 takes còn trong cut tại 10.56s + 14.62s)
#         PAIR B: PASS (editor đã cắt TAKE CŨ, chỉ còn TAKE MỚI ở 96.94s)
```

**Anti-pattern ❌:**
- Báo "PASS" hoặc "FAIL" sau manual scan text mà KHÔNG có timestamp evidence
- Tin tưởng 100% vào manual scan text (đặc biệt với anchor keywords phổ biến)
- Bỏ qua việc cross-check với subagent khi manual thấy "rõ ràng là take lặp"

**Reference**: `references/manual-verify-vs-subagent-word-level-2026-07-18.md` (đang chờ update)

## Reference Files

- `references/transcript-saver-v2-verification-session.md` — full transcript of the 2026-06-17 verification session that discovered test-file vanishing, parallel hooks, and the `$MESSAGE` literal bug
- `references/session-2026-06-17-disk-cleanup-investigation.md` — root cause analysis: the `disk_cleanup` plugin auto-deletes `test_*.py` / `tmp_*.py` / `*.test.py` files at `on_session_end`. Includes diagnostic command, pattern matching rules, and 3 fix recipes.
- `references/session-2026-06-23-city-drift-fabricated-completion.md` — full transcript of the 2026-06-23 City Drift game verification session: agent claimed "v1.5 LIVE" based on tool return values, but real browser test showed zero change. 5-evidence gate pattern born from this session: file size + grep count + git hash + curl URL + screenshot. Read this WHENEVER shipping a "live" claim that depends on multiple verification surfaces.
- `references/session-2026-06-25-telegram-config-patch-verification.md` — Episode 3 of fabricated completion series: agent claimed 2 config patches (`safe_mode`, `text_batch_delay_seconds`) without running `hermes config set`. User caught via direct verification question. Covers Hermes-specific dual-section config (`telegram:` + `platforms.telegram:`), AGENTS.md env var rule, security guard on config.yaml, and the "user challenges completion" honest recovery pattern. Read this WHENEVER patching Hermes config or any settings file.
- `references/session-2026-06-26-wikimemory-provider-fix.md` — 3-patch fix for USER.md pollution: tightened ENTITY_PATTERNS, added `_validate_fact()` filter, atomic write via temp file + rename. Includes pre-flight backup command, full diagnosis path, and the verify-before-ask lesson (agent wrote patch to `/tmp/` then asked user to review BEFORE self-verifying). Read this WHENEVER patching memory plugin extraction logic.

## Real-Time Cron Monitoring Verification (2026-06-25)

**Scenario:** User explicitly requests "cho chạy cron ngay và monitoring realtime" — different from typical "schedule + wait". Verification approach must be **parallel, evidence-rich, and tolerate false alarms**.

**5-parallel-check pattern (cron running, user wants live status)**:

```bash
# Check 1: Cron session progress (via SQLite state.db)
SESSION_ID=$(sqlite3 ~/.hermes/state.db \
  "SELECT session_id FROM messages WHERE session_id LIKE 'cron_<job_id>_%' \
   ORDER BY id DESC LIMIT 1")
COUNT=$(sqlite3 ~/.hermes/state.db \
  "SELECT COUNT(*) FROM messages WHERE session_id='$SESSION_ID'")
echo "Cron session: $SESSION_ID | msgs: $COUNT"

# Check 2: Target files state (.env, config, secrets — whatever cron touches)
ls -la ~/.hermes/.env 2>&1
wc -c ~/.hermes/.env

# Check 3: Backup snapshots (verify pre-flight ran)
# ⚠️ USE -A NOT -1 for dotfile-only dirs (false alarm otherwise)
ls -1A /Volumes/Storage-1/Hermes/secrets/ | wc -l

# Check 4: Latest backup log
ls -lat ~/.hermes/backups/ | head -3

# Check 5: Git log (verify commits landed)
git log --oneline -3
```

**Anti-pattern**: poll only ONE source (e.g. just filesystem) — miss cron intermediate state. Cron agent can run 30+ tool calls before any file changes appear on disk. SQLite session DB shows every turn immediately.

**Real failure mode (2026-06-25 20:16)**: `ls -1 <dir> | wc -l` returned 0 for dotfile-only directory. Em nearly reported "backup files gone" — false alarm. **Fix**: always use `ls -A` for dirs that may contain only dotfiles, or glob directly with explicit pattern.

**When cron "stuck" looks misleading**: SQLite polling may show msg count unchanged for 60-90s. This is NORMAL — LLM cron agent reads context, thinks, then batches tool calls. Only declare "stuck" if msg count stays flat for >3 minutes AND no tool activity in last 30s.

**Reference**: `hermes-daily-backup` skill → `references/report-example-2026-06-25-monitoring.md` for full session transcript.
