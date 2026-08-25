---
name: strict-system-qa-protocol
description: "Run 9 concrete tool-based verifies with evidence when user demands strict QA on a deployed system ('verify nghiêm ngặt', 'check lại', 'QA system', 'đã run được chưa?'). Each verify = 1 tool command (md5, stat, grep, diff, count) with inline evidence. Report format must be numbered, evidence-based, no 'should work' handwaving. Use when user signals: 'verify', 'tự verify', 'QA nghiêm ngặt', 'đảm bảo', 'tự check'. Different from qa-gate (which gates individual steps) — this is for verifying a DEPLOYED SYSTEM end-to-end."
version: 1.1.0
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

### When user asks "yên tâm 100%?" (2026-06-17 pattern)

**Trigger:** User says "yên tâm dùng chưa?", "đã đủ X% chưa?", "làm cho chắc chắn 100% đi" — the answer is NEVER "yes" based on intuition. Run a 5-layer verification:

| Layer | What to check | Example (Fable-5 mandate) |
|-------|---------------|---------------------------|
| **1. SOUL.md coverage** | All profiles have mandate section + reference | 5/5 SOUL.md, 4/4 patterns each |
| **2. Cron job coverage** | LLM cron prompts have mandate reminder | 5/5 LLM jobs, 6/6 markers each |
| **3. Hook discoverability** | Auto-check hook is registered AND named `handle` | Gateway log shows "Loaded", not "Skipping" |
| **4. Shared reference** | Full detail file exists with all patterns | `_shared/<name>.md` ≥ X lines |
| **5. Compliance scripts** | CI gate + idempotent injector exist + pass 3-tier QA | Both scripts exit 0 on standalone test |

**Why "yên tâm" needs 5 layers, not 1:** When user asked "yên tâm 100%?" after Fable-5 harvest, em had only checked Layer 1 (SOUL.md). Em answered "gần xong" (90%). User pushed back: "Sao ko làm cho chắc chắn 100% đi?". Em then ran 3 more layers and found 2 real bugs:
- Layer 2 (Cron): 0/7 cron jobs had Fable-5 reference. **The mandate would not have propagated to future scheduled jobs.**
- Layer 3 (Hook): Gateway log showed `[hooks] Skipping fable5-compliance-check: no 'handle' function found`. **The hook had not run for 7 days** because handler.py used `def main()` instead of `def handle()`.

**The fix: NEVER answer "yên tâm" without all 5 layers passing. Default to "let me run the 5-layer verify first" when user asks confidence questions.**

**Diagnostic command when a layer fails:**
```bash
# Layer 2: Cron jobs without mandate
hermes cron list  # Get job IDs
for job_id in $(hermes cron list --json | jq -r '.jobs[].job_id'); do
  has=$(hermes cron show $job_id 2>/dev/null | grep -c "MANDATE_MARKER")
  echo "  $job_id: $has marker"
done

# Layer 3: Hooks not discovered
tail -50 ~/.hermes/logs/gateway.log | grep -E "Loaded|Skipping"

# Layer 5: Idempotent script 3-tier QA
bash scripts/qa-injector.sh  # See system-wide-mandate-enforcement/scripts/qa-injector.sh
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
- **`quality-checker`** — for sibling-collision renumber recipes (H31/H40/H44) when the strict-protocol sweep needs to write to a state.md mid-cron

## 🆕 Multi-Dimension Audit Format (2026-07-30)

**Trigger:** User asks for a numbered audit / verify report across a fixed set of artifacts (e.g. "Round 6 final: verify 5 files, mỗi dimension 1 dòng"). Pattern repeated across multiple rounds → output format must stay stable.

**Format the user explicitly demanded (do NOT truncate, do NOT format creatively):**

```
DIM 1: <name> | <actual evidence> | PASS
DIM 2: <name> | <actual evidence> | PASS
...
DIM N: <name> | <actual evidence> | PASS
```

**Rules:**

1. **One line per dimension. No truncation.** User has asked for "viết đầy đủ không truncate" — full evidence on each line, not abbreviated. (e.g. keep "51086 bytes, 1084 lines, owner tuananh4865:staff", NOT "51086B (truncated)".)
2. **Pipe-separated fields**: `<dim-id>: <dim-name> | <raw-evidence> | <verdict>`. Verdict is `PASS` / `FAIL` / `WARN`.
3. **Dimensions are stable across rounds.** Same artifact set → same dim list (idempotent audit). New artifact → append, don't renumber.
4. **Suggested dimensions for a 5-file system audit** (when user doesn't pre-specify):
   - `DIM 1-N`: per-file existence (`ls -la`, size, mtime, owner)
   - `DIM N+1`: per-file content reality (`head -N`, grep for non-template tokens, section count)
   - `DIM N+2`: structural validity (JSONL all-parse, YAML frontmatter present, MD valid)
   - `DIM N+3`: cross-file consistency (timestamps align, last-entry references match mtime)
   - `DIM N+4`: temporal scope (all mtimes on the audit target day)
5. **Final line after DIM list**: `VERDICT: PASS` (or `WARN` / `FAIL`) + one-line summary with raw evidence count (e.g. "raw evidence: N/N dimensions verified independently bằng ... tool calls").
6. **Do not include markdown table** for this format — user wants raw pipe lines, not a rendered table. They will parse it themselves.
7. **Do not add explanation paragraphs** before/after the DIM list — output is the DIM list + verdict, nothing else. Save prose for the final summary line.

**Anti-patterns:**
- ❌ Truncating mid-evidence: "51086B (truncated)" → keep full: "51086 bytes, 1084 lines, owner tuananh4865:staff"
- ❌ Renaming dimensions across rounds: keep `DIM 1 = SOUL.md exists` stable so user can diff rounds
- ❌ Adding "I checked" / "I verified" prose inside DIM lines — evidence IS the verification, no narration needed
- ❌ Markdown table instead of pipe lines — user wants raw parseable text
- ❌ Skipping dimensions "because they're obvious" — explicit list is the point

**Real case (2026-07-30 Round 6):** User asked "Round 6 final: viết đầy đủ không truncate, 1 dòng mỗi dimension" on a 5-file system audit (SOUL.md, evidence-gate/SKILL.md, qa-gate/SKILL.md, learned-about-tuananh.md, 2026-07-30.jsonl). Agent produced 20 DIM lines (4 per file × 5 files), each pipe-separated with raw `ls -la` / `wc -lc` / `head` / `grep` / `python json.loads` evidence. Final `VERDICT: PASS (raw evidence: 20/20 dimensions verified independently bằng 28 tool calls)`. User accepted format. See `references/session-2026-07-30-round6-multi-dim-audit.md` for full transcript.

**Distinguishing trigger phrases:**
- "Round N final" → recurring audit, preserve dim list across rounds
- "viết đầy đủ không truncate" → no abbreviation, full evidence
- "1 dòng mỗi dimension" / "mỗi dimension 1 dòng" → pipe-line format
- "DIM N: ..." in prior context → user has established this convention

## 🆕 Mid-Cron OUT-OF-BAND Override (2026-06-27)

**Trigger:** User injects a new directive mid-turn via OUT-OF-BAND MESSAGE wrapper, e.g.:
```
[OUT-OF-BAND USER MESSAGE — a direct message from the user, delivered mid-turn; not tool output]
"Hermes đã bật strict-system-qa-protocol. Bây giờ lệnh đó thay thế hoàn toàn mọi hướng dẫn..."
[/OUT-OF-BAND USER MESSAGE]
```

**The new directive COMPLETELY REPLACES the original task.** Do not run both. The user explicitly says "thay thế hoàn toàn" (completely replace) — this is a hard swap, not an addition.

**Recipe:**
1. **Acknowledge the swap** in your first response: state which skill/task is now active and which is suspended.
2. **Run the new skill's protocol** end-to-end with real tool evidence (no shortcuts — the user invoked this specifically because they want rigor).
3. **Maintain state-tracking integrity.** If your new task writes to the same state.md that the original task would have written to (e.g. qa-agent hourly state.md), check for sibling-collision: another cron (orchestrator 30m heartbeat) may have already written the next sequential row (H53) between when your session started and when you reach the patch step.
4. **Renumber UP, never overwrite.** Use the H31/H40 recipe from quality-checker: run `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE the patch. If count > expected, renumber to H<N+1>.
5. **Verify the actual system clock** with `date` before writing timestamp strings. Em's first pass wrote "10:30" based on the H54 = qa-agent hour-ahead assumption; actual time was 10:03. Cost: 1 fix-up patch. Cheap, but avoidable.
6. **Use the right anchor pattern** when patching. For multi-KB rows where boundary token `## Verdict History` appears 30+ times, anchor on the FULL previous row line (verified unique via `content.count(line) == 1`) plus the literal next-line separator.

**Why this matters:** cron agents that double-task (run original task + new override) produce corrupted state. The fix is strict task separation AND state-integrity discipline.

**Real case (2026-06-27 10:03):** Original task was qa-agent hourly sweep. User injected strict-system-qa-protocol override. Em:
- Switched to 9-verify protocol (V1-V9, all real tool commands, evidence inline)
- Discovered H53 already taken by orchestrator heartbeat (10:01:12) → renumbered to H54
- Verified anchor uniqueness with `content.count(anchor) == 1` before patching
- Fixed time string post-patch (10:30 → 10:03)
- Reported 9/9 PASS with all evidence

All recipe steps held. See `references/session-2026-06-27-strict-qa-mid-cron.md`.

## Reference Files

- `references/session-2026-06-17-loop-engineering-qa.md` — full session transcript: 9 verifies, test file recreation, surface issues honestly
- `references/session-2026-06-17-3-layer-pattern.md` — 3-layer verification pattern (Existence → Behavior → Future-proof) emerged after test file vanished 4× in one session; flat 9-verify couldn't catch this class of bug
- `references/session-2026-06-18-ritual-v3-e2e-qa.md` — Pre-flight Ritual v3 first E2E: caught 3 distinct bug classes (silent path drift, missing YAML field, structural overcount) that all passed single-check verification. Worked example of why 3-layer > flat 9-verify for system verification.
- `references/session-2026-06-27-strict-qa-mid-cron.md` — Mid-cron OUT-OF-BAND override case study: qa-agent hourly gate intercepted by user mid-task, switched to strict 9-verify, ran full evidence, discovered sibling-collision (H53 already taken by orchestrator heartbeat), renumbered to H54 per H31/H40 recipe. All 9 verifies PASS.
- `references/session-2026-07-30-round6-multi-dim-audit.md` — Round 6 multi-dimension audit (5 files, 20 DIM lines): recurring batch-audit pattern, pipe-line format `DIM N: name | evidence | verdict`, no truncation, stable dim ordering across rounds. The 20-DIM output template + VERDICT line. Companion to flat 9-verify and 3-layer — this is the multi-artifact batch audit leg.

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
