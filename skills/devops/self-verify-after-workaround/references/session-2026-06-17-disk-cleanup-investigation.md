# Session 2026-06-17: disk_cleanup Root Cause Investigation

**Context:** During strict QA of the transcript-saver-v2 hook system, the test file
(`~/.hermes/hooks/transcript-saver-v2/test_handler.py`) vanished 4 separate times in
a single session. Each time it was recreated, it disappeared again within 60-120
seconds. The agent initially assumed the cause was "write_file tool issue",
"Hermes session reset", or "iCloud sync" — all wrong.

**Time spent on misdirected investigation:** ~20 minutes
**Time to find root cause after checking cleanup.log:** <2 minutes

## Investigation Path That Worked

1. **Eliminated obvious culprits:**
   - Cron jobs (3 candidates) — verified scripts only touch `wiki/{concepts,entities,...}`, not `hooks/`
   - All hook handlers (`transcript-saver`, `loop-engineering`, etc.) — `grep` showed no delete logic for `hooks/` dir
   - GSD scripts (`.js` files) — only operate in `.planning/` dir
   - iCloud sync — file system is local APFS, no xattr markers

2. **Discovered the smoking gun:**
   ```bash
   ls -la /Users/tuananh4865/.hermes/disk-cleanup/
   # Found: cleanup.log + tracked.json + tracked.json.bak
   cat ~/.hermes/disk-cleanup/cleanup.log | grep "test_handler"
   # Found: TRACKED + DELETED entries with timestamps 8s apart
   ```

3. **Confirmed the rule from source:**
   ```bash
   grep -A 2 "_TEST_PATTERNS\|_TEST_SUFFIXES" \
     ~/.hermes/hermes-agent/plugins/disk-cleanup/disk_cleanup.py
   # Shows: ("test_", "tmp_") and (".test.py", ".test.js", ".test.ts", ".test.md")
   ```

## Key Diagnostic Command (Use This First When Test File Vanishes)

```bash
# Is disk_cleanup the culprit? (catches in <30s)
tail -50 ~/.hermes/disk-cleanup/cleanup.log | grep "$(basename $YOUR_TEST_FILE)"
# Expected output if disk_cleanup is the cause:
#   [2026-06-17 01:42:00] TRACKED: .../test_handler.py (test, 2.2 KB)
#   [2026-06-17 01:42:08] DELETED: .../test_handler.py (test, 2.2 KB)
# If no match: file was deleted by something else (cron, manual rm, OS cleanup)
```

## Pattern Matching Rule (Verified Empirically)

| Filename | Auto-deleted by disk_cleanup? | Why |
|----------|------------------------------|-----|
| `test_handler.py` | ❌ YES | starts with `test_` |
| `handler_test.py` | ✅ NO | `_test` is suffix, not prefix |
| `verify_handler.py` | ✅ NO | no match |
| `test.py` | ✅ NO | `test_` requires trailing underscore (single word doesn't match) |
| `tmp_test.py` | ❌ YES | starts with `tmp_` |
| `run_tests.py` | ✅ NO | no match |

**Empirically verified via Python simulation:**
```python
_TEST_PATTERNS = ("test_", "tmp_")
_TEST_SUFFIXES = (".test.py", ".test.js", ".test.ts", ".test.md")
name = "test_handler.py"
matches = name.startswith(_TEST_PATTERNS) or any(name.endswith(s) for s in _TEST_SUFFIXES)
# matches = True → DELETED
```

## Cleanup Log Evidence Trail (Real Timestamps from this Session)

```
[2026-06-16 18:36:39] TRACKED: .../test_handler.py (test, 2.2 KB)
[2026-06-16 18:36:47] DELETED: .../test_handler.py (test, 2.2 KB)  ← 8 seconds!
AUTO_QUICK (session_end): deleted=1 dirs=2 freed=2.2 KB
```

The gap between TRACKED and DELETED was **8-15 seconds** in every case. The plugin fires
synchronously when `on_session_end` event is emitted by the gateway.

## The Plugin's Role (Why It Exists)

The `disk_cleanup` plugin is designed to prevent ephemeral test/temp files from
accumulating in `~/.hermes/` over time. From the source comments:

> "**Rules:**
>   - test files → delete immediately at task end (age >= 0)
>   - temp files → delete after 7 days
>   - cron-output → delete after 14 days
>   - empty dirs → always delete (under HERMES_HOME)
>   - research → keep 10 newest, prompt for older (deep only)
>   - chrome-profile → prompt after 14 days (deep only)
>   - >500 MB files → prompt always (deep only)"

It's a **feature**, not a bug. The agent just needs to know about it.

## Fix Recipe (Recommended)

```bash
# Rename test file to a safe name (no infrastructure changes needed)
mv ~/.hermes/hooks/YOUR_HOOK/test_handler.py ~/.hermes/hooks/YOUR_HOOK/verify_handler.py
# Update import statements if any reference the old name
# Re-run tests — they should now persist across session restarts
```

For persistent test suites (run across many sessions), prefer **Option B** (move
outside `hooks/` dir) to a stable location like `~/.hermes/hooks/_tests/`.

## Cross-References

- `self-verify-after-workaround` SKILL.md → "disk_cleanup Plugin Auto-Deletes test_*.py Files" section
- `strict-system-qa-protocol` SKILL.md → "Update 2026-06-17 (root cause found)" note
- Hermes source: `~/.hermes/hermes-agent/plugins/disk-cleanup/disk_cleanup.py`
- Cleanup log: `~/.hermes/disk-cleanup/cleanup.log` (append-only audit trail)
- Tracked files: `~/.hermes/disk-cleanup/tracked.json` (current tracked items)
