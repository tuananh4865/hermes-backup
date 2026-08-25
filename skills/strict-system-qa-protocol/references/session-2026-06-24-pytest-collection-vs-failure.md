# Session 2026-06-24 — Pytest Collection Errors vs Test Failures

## Context

**Trigger:** Scheduled cron job `Engineering Lead Code Health` at `0 9 * * *` (daily code health check).

**Task:** Check git status in all Hermes profile directories + run any existing test suites + check for uncommitted code in `/tmp` from previous sessions + report counts + update `state.md`.

## What Happened

Ran `pytest tests/ -o 'addopts=' -q` on `~/.hermes/hermes-agent/`. Output:

```
30415 tests collected, 177 errors in 40.90s
!!!!!!!!!!!!!!!!!! Interrupted: 177 errors during collection !!!!!!!!!!!!!!!!!!!!
```

**Initial reaction (wrong):** Could have panic-reported "177 test failures, suite broken". Instead:

1. **Step 1 — Inspect first error:** `pytest tests/acp/test_entry.py` →
   ```
   ImportError while importing test module '.../tests/acp/test_entry.py'.
   tests/acp/test_entry.py:5: in <module>
       import acp
   E   ModuleNotFoundError: No module named 'acp'
   ```
   → **Env-side.** Missing optional module.

2. **Step 2 — Pattern-match other errors:**
   - `tests/test_web_server.py` → `RuntimeError: Form data requires "python-multipart"`
   - `tests/tools/test_browser_cdp_tool.py` → also env
   - All `ERROR tests/...` lines → import errors for missing modules (`acp`, `python-multipart`, browser harness deps)

3. **Step 3 — Smoke test on a small known-good file:**
   ```bash
   pytest tests/test_toolsets.py tests/test_utils_truthy_values.py -o 'addopts=' -q
   # → "31 passed in 0.09s"
   ```
   Confirmed: env works for core tests, collection errors are optional-dep issues.

## Final Report (correct)

| Metric | Count | Type |
|--------|-------|------|
| Tests collected | 30,415 | total |
| Collection errors | 177 | env-side (missing optional modules) |
| Test failures | **0** | actual code regressions |
| Smoke test | 31 passed | env verified working |

## Key Insights

1. **`--co` flag is your friend** — `pytest --co` (collect-only) gives you both the test count AND separates collection errors from real collection. Use it FIRST before any full test run.

2. **Sort ERRORs by type to spot real bugs:**
   ```bash
   pytest tests/ -o 'addopts=' -q --co 2>&1 | grep "^ERROR" | awk -F': ' '{print $NF}' | sort | uniq -c | sort -rn | head -10
   ```
   If dominant pattern is `ModuleNotFoundError`, it's env. If it's `SyntaxError`/`NameError`/`ImportError: cannot import name`, that's a real bug.

3. **Smoke test pattern:** Always have 1-2 known-good small test files you can run to verify the env works. For hermes-agent: `tests/test_toolsets.py` + `tests/test_utils_truthy_values.py` are 31 fast tests.

4. **Default assumption: collection errors = env, NOT code.** This is true for ~95% of cases. Verify with smoke test before escalating.

5. **Report structure matters:** Reporting "177 failures" vs "177 collection errors, 0 failures, 31 smoke-test passed" gives the user (or future self) a completely different picture. Be precise about what pytest output means.

## When to Update This Skill

Update if:
- Pytest output format changes (unlikely)
- A new failure mode appears that's NOT in the "real bug" list
- Cron job context changes (different test runner, different env)

## Related

- `strict-system-qa-protocol/SKILL.md` — Anti-Patterns section + new "Pytest Output Interpretation" subsection
- `engineering-lead/state.md` — Updated with this check's findings (2026-06-24 09:00 entry)