# Transcript Saver v2.0 — Final Verification Session (2026-06-17)

## Context

Round 2 of transcript-saver-v2 work (following the initial build round 2026-06-16). User asked the agent to verify the hook was actually running for real Telegram messages, after the agent had reported "Hook registered" multiple times without showing real-file evidence.

## Critical signals in this session

1. **User repeated "tự verify", "tự làm tự verify đi", "verify nghiêm ngặt"** — exhaustion signal. The user wanted to know if the hook ACTUALLY runs in production, not just that it was registered.

2. **User asked "kết quả là đã run được chưa?"** — direct question, no room for hand-waving. The agent had to run evidence before answering.

3. **User triggered 2 final "hello" / "test test" messages** — gave the agent a chance to verify hook fires for real messages.

## Bugs found during self-verification (NOT in initial build)

| # | Bug | Root cause | Fix |
|---|-----|-----------|-----|
| 1 | `transcript-saver-v2/test_handler.py` kept disappearing after `handler.py` edits | gateway Python process holds file handle, `__pycache__` reset clobbers test files in same dir | Store tests OUTSIDE the hook's runtime dir (e.g. `_tests/` or skill `scripts/`) |
| 2 | One V2 file had literal `$MESSAGE`, `$USER_ID` in frontmatter | Race condition with config.yaml env-var args expanding to empty strings | Add defensive skip in handler: `if user_message.startswith("$"): return` |
| 3 | V1 hook still running in parallel with V2 (47 files/day vs 4 files/day) | No mechanism to disable V1 when V2 is added | Update V1 HOOK.yaml `enabled: false` OR remove from config.yaml |
| 4 | Report claimed "Hook registered" but `stat` showed config was modified by `yaml.dump` (block style, not flow style) | patch tool blocked, workaround used, format changed | Surface workaround in report, run `yaml.safe_load` to verify parse, show before/after key count |

## The 9-Verify Structured QA Workflow (worked 2026-06-17)

When the user demands strict QA, the agent ran 9 concrete verifications, each with evidence:

```
1. Files exist        → ls -la, stat -f "%Sm %z %N"
2. Unit tests pass    → bash test.sh, python3 test.py (with exit codes)
3. E2E test           → run real hook invocation, check side effects
4. Hooks registered   → hermes hooks list | grep "transcript-saver-v2"
5. State files        → grep -c "| PASS |" state.md
6. Cron jobs          → hermes cron | grep -E "Name:"
7. Wiki pages         → ls wiki/concepts/, grep index.md
8. Obsidian mirror    → md5 wiki/... vs md5 obsidian/... (must match)
9. Stdin parsing      → echo '{json}' | python3 handler.py (regression test)
```

**Key insight:** Don't try to be clever. Just run 9 simple verifications and report the result of each. The user wants to see ALL 9, not just the ones that pass.

## Real findings from running 9 verifies

- **V1 PASS**: 9/9 core files exist, 4 skill files, 6 state files, 2 wrappers
- **V2 PARTIAL FAIL (then fixed)**: `test_handler.py` was missing. Had to recreate from scratch. 4 essential tests instead of original 10. **Net regression in test coverage.**
- **V3 PASS**: E2E loop-goal ran 2 iterations, condition parser correctly detected missing variable
- **V4 PASS**: 4/4 Hermes shell hooks allowed
- **V5 PASS**: 43 verdicts across 5 profiles (default: 33, content-dir: 6, research-lead: 4)
- **V6 PASS**: 7/7 cron jobs active, last runs OK
- **V7 PASS**: 2 wiki concept pages (10.9KB total), 2 index refs, 1 log entry
- **V8 PASS**: Obsidian MD5 `fed36981d0696138728c222f258d5496` matched wiki
- **V9 PASS**: stdin JSON regression test created file in temp dir

**Final result: 9/9 PASS after the V2 test-file fix.**

## The "I can't verify this" honesty pattern (extended)

The agent ran the verifications. Some verifications had caveats:

> "V2 hook chỉ tạo 4 files thật (23-08-26×2, 23-10-39 hello, manual test). V1 hook tạo 51 files. Performance impact: 2x writes per message — unmeasured."

> "Coder + memory-curator profiles chưa có verdicts (chưa dùng tới, không phải bug)."

The user prefers "here's what I verified, here's what I didn't" over "everything works" hand-waving.

## Anti-pattern: reporting from a stale mental model

The agent at one point claimed "Hook v2.0 đã hoạt động" based on `hermes hooks list` showing ✓ allowed. But:
- `hermes hooks list` shows the allowlist status, not runtime behavior
- The hook was registered but the Python handler had a `$MESSAGE` filter bug
- 4 files were V2 thật, but 1 was a fake (had `$MESSAGE` literal)

**Lesson:** "Registered" ≠ "Working". Verify with file content, not just hook status.

## What the user actually wanted (revealed by repeated "tự verify")

The user's repeated "tự verify" wasn't asking for "run my checks" — it was asking for **independent verification of the agent's own claims**. The agent must:
1. List every claim it made
2. Run a check for each claim
3. Show the result of each check
4. Flag claims it CANNOT verify (don't fake it)

This is different from "do what I say" or "follow my recipe." The user wants the agent to design its own QA, then execute it transparently.

## Test file persistence pitfall (CONCRETE FIX)

The transcript-saver-v2 test file vanished 3 times in 1 session. Concrete fix:

**Option A — move tests outside the runtime dir:**
```bash
mkdir -p ~/.hermes/hooks/_tests/
mv ~/.hermes/hooks/transcript-saver-v2/test_handler.py \
   ~/.hermes/hooks/_tests/transcript-saver-v2_test.py
# Update import paths in the moved test file
```

**Option B — keep a `.bak` and restore script:**
```bash
# Before any handler.py edit
cp test_handler.py test_handler.py.bak
# After edit, restore if missing
ls test_handler.py 2>/dev/null || cp test_handler.py.bak test_handler.py
```

**Option C — store tests in the skill's `scripts/` directory:**
```bash
# Skill umbrella owns the test, runtime hook just imports it
~/.hermes/skills/devops/transcript-saver/tests/test_handler.py
# Hook code: sys.path.insert(0, ".../tests/")
```

**Recommended: Option A.** Tests in a separate `_tests/` directory are never touched by the gateway's runtime cache invalidation.

## Parallel hook pitfall (CONCRETE FIX)

V1 + V2 both registered → 2x writes per message. Two real consequences:
1. 2x file I/O per Telegram message
2. Wiki has both formats; future agent confuses "which hook wrote this?"

**Concrete fix — disable V1:**
```bash
# Option 1: Set V1 enabled: false
echo "enabled: false" >> ~/.hermes/hooks/transcript-saver/HOOK.yaml

# Option 2: Remove V1 from config.yaml
python3 << 'EOF'
import yaml
from pathlib import Path
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
# Restart gateway
hermes gateway restart
```

**Lesson:** When adding a new hook, ALWAYS check `hermes hooks list` for duplicates. If old hook is superseded, disable it explicitly — don't leave both running.

## Final QA report format (the user-validated one)

```markdown
# ✅ KẾT QUẢ VERIFY — Hook v2.0 ĐÃ RUN

## Facts (với evidence chứ không báo cáo suông)

### Test 1: Hook registered
```
✓ /Users/tuananh4865/.hermes/hooks/transcript-saver-v2/hook_wrapper.sh
✓ Status: allowed
```

### Test 2: Hook chạy cho REAL messages của anh
3 file V2 mới nhất từ real Telegram messages:
| File | Time | Message gốc |
|------|------|-------------|
| `23-14-39_20260603_...md` | 23:14 | "sao anh thấy vẫn chưa hoạt động giống fa..." |
| `23-12-09_20260601_em-tự-làm-tự-verify-đi.md` | 23:12 | "em tự làm tự verify đi" |
| `23-10-39_20260601_hello.md` | 23:10 | "hello" |

### Test 3: Content là real message
- Tất cả files có `## User Message` section với nội dung thật
- Có session_id `20260601_103236_358b5947` (anh's session)
- Có 4-5 NER wikilinks + 3-4 tags auto-extracted

### Test 4: Obsidian mirror OK
- 6 files V2 trong Obsidian transcripts/
- MD5 identical với wiki files

### Test 5: Manual re-trigger works
```
[transcript-saver-v2] Saved: 23-14-55_verify_1_verify-hook-run.md
[transcript-saver-v2] Mirrored to Obsidian
```

## 🎯 KẾT LUẬN
**Hook v2.0 đã RUN cho real Telegram messages của anh.**
```

**Key features of this format:**
- "Facts (với evidence chứ không báo cáo suông)" — signals the agent is showing work
- "Test N:" enumeration — exhaustive coverage, user can see what was checked
- Tables with concrete data — not "should work" but actual file paths and sizes
- Final bold conclusion — no ambiguity, the user can paste-cite

## Cross-references

- `session-2026-06-16-event-name-filter.md` (loop-engineering-deployment skill) — why handler's event_name filter rejected `on_session_end` silently
- `session-2026-06-16-stdin-json-payload.md` — why the bash wrapper args are useless
- `session-2026-06-16-transcript-saver-v2.md` — initial build round
- `session-2026-06-16-self-verify.md` — earlier self-verify mandate (this file extends it)
- `session-2026-06-16-user-correction-verify.md` — why "fake report" is the worst failure mode
- Main SKILL.md "The 'I can't verify this' Honesty Pattern" — base pattern, extended here
