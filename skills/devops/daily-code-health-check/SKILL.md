---
name: daily-code-health-check
description: Daily cron-driven code health audit across Hermes profile directories — git status (main repo + tracked subdirs like hermes-agent/), test suite inventory, /tmp session leftovers, profile state.md freshness, pending task detection, and state.md update. Use when a cron job says "daily code health check", "engineering-lead daily audit", "report N uncommitted files, N test failures, N pending tasks", or any recurring inspection of working tree + profile state across the multi-agent system. Distinct from `hermes-daily-backup` (which pushes to remote) and `hermes-security-audit` (which scans for vulnerabilities).
category: devops
---

# Daily Code Health Check (Engineering-Lead)

## Problem

A cron job (or engineering-lead profile) needs a recurring, low-cost audit of the Hermes codebase to detect:
- Uncommitted code drift (working tree vs HEAD)
- Test suite health (location, last run, failures)
- Stale `/tmp` artifacts from previous sessions
- Profile state.md freshness + pending task inventory
- Anomalies (e.g. 580 modified files in a tracked subdir that isn't a submodule)

Output: a single report with N uncommitted files, N test failures, N pending tasks + state.md update at `~/.hermes/profiles/<profile>/state.md`.

**Distinguish from neighbors:**
- `hermes-daily-backup` → pushes git commits to remote (this skill READS git state, doesn't mutate remote)
- `hermes-security-audit` → scans for vulnerabilities (this skill is broader: drift + tests + state)
- `multi-agent-heartbeat` → sweeps all profiles for pending tasks (this skill focuses on ONE profile + git state)

## 5-Step Process

### Step 1: Git status — main repo
```bash
cd ~/.hermes
echo "=== Untracked ===" && git ls-files --others --exclude-standard | head -20
echo "=== Modified code (.py/.sh/.yaml) ===" && git status --porcelain | grep -E "\.(py|sh|yaml|yml|js|ts)$"
echo "=== Actual diffs ===" && git diff --name-only -- '*.py' '*.sh' '*.yaml' '*.yml' '*.js' '*.ts'
echo "=== Last commit ===" && git log -1 --format="%cd %s" 2>/dev/null
```

### Step 2: Git status — tracked subdirs (the 580-modified-files trap)
A tracked subdir (like `~/.hermes/hermes-agent/`) can show hundreds of "modified" files even though it's NOT a submodule. Detection:
```bash
cd ~/.hermes
git ls-files --stage hermes-agent 2>/dev/null | head -3
# 100644 → regular tracked file
# 160000 → gitlink (true submodule)
```

If mode is `100644` → it's a regular tracked subdir, NOT a submodule. The 580-file anomaly is normal in this setup (likely pre-commit staging or a worktree pattern). Flag as ⚠️ in the report but don't try to "fix" it — that's a separate investigation.

```bash
cd ~/.hermes/hermes-agent
echo "=== Modified count ===" && git status --porcelain | wc -l
echo "=== Modified .py count ===" && git status --porcelain | awk '{print $2}' | grep -c "\.py$"
echo "=== Last commit ===" && git log -1 --format="%cd %s" 2>/dev/null
```

### Step 3: Profile directories
All Hermes profile dirs SHOULD have NO `.git` (they're isolated runtime dirs, subdirectories of the SINGLE shared `~/.hermes` git repo). Detection:
```bash
for profile_dir in ~/.hermes/profiles/*/; do
  name=$(basename "$profile_dir")
  if [ -d "$profile_dir/.git" ]; then
    echo "⚠️ $name has .git (unexpected)"
  else
    # Count files, list state.md mtime
    state_md="$profile_dir/state.md"
    if [ -f "$state_md" ]; then
      size=$(stat -f%z "$state_md")
      mtime=$(stat -f%Sm -t "%Y-%m-%d %H:%M" "$state_md")
      echo "✅ $name: state.md ${size}b ($mtime)"
    fi
  fi
done
```

**DO NOT run `git -C ~/.hermes/profiles/<name> status` per profile** — all 15 profiles share one parent repo at `~/.hermes`, so per-profile git output is identical 15x. Step 1 already covers the whole tree.

### Step 4: Test suites + /tmp scan
```bash
# Test inventory
find ~/.hermes/hermes-agent -name "test_*.py" -o -name "verify_*.py" 2>/dev/null | head -10

# /tmp leftovers — distinguish actionable code from benign upgrade markers
ls -lat /tmp/ 2>/dev/null | grep -E "\.(py|sh|yaml|json|md)$" | head -10
# Actionable: hermes-* scripts, agent-written code
# Benign (skip): cc-meta-sha.txt, hermes-commit-sha.txt, hermes-env-skeleton.txt
```

**Don't run full test suite** — 5-10 min cost inappropriate for daily cron. Report test LOCATION + COUNT instead. Run full suite on-demand when code changes detected.

### Step 5: Report + state.md update
Output report + update `~/.hermes/profiles/<profile>/state.md` with:
- Summary table (uncommitted, test failures, pending tasks)
- Recommendations (1-3 actionable items max)
- Date stamp

Report template:
```
📊 Daily Code Health Check — YYYY-MM-DD (<profile>)

### Git Status — main repo
- Uncommitted: N (breakdown by category)
- Last commit: <date> <subject>

### Git Status — <tracked-subdir>
- Uncommitted: N (M modified + ?? untracked)
- ⚠️ Flag: <anomaly description if applicable>

### Profile Dirs (N profiles)
- Fresh today: <list>
- Stale: <list>

### Test Suites
- Location: <path>
- Status: <deferred / last run / failures>

### /tmp Leftovers
- Actionable: <list>
- Benign (skip): <list>

### Summary
| Metric | Value | Status |
| Uncommitted code | N | ✅/⚠️ |
| Test failures | N | ⏸️ |
| /tmp leftovers | N | ✅ |
| Pending tasks | N | ✅/⚠️ |

### Recommendations
1. ...
2. ...
```

## Pitfalls

1. **Don't run full pytest suite on daily cron** — 5-10 min cost. Inventory location + count instead. Run full suite only when triggered by code changes detected in step 1-2.

2. **Tracked subdir ≠ submodule** — `git ls-files --stage <path>` showing `100644` (regular file mode) means it's a regular tracked directory, not a gitlink (which would be `160000`). Don't run `git submodule status` on a non-submodule. The 580-file "anomaly" in `~/.hermes/hermes-agent/` is a feature of this setup (pre-commit staging), not a bug to investigate unless explicitly flagged by user.

3. **State.md size variance is NORMAL** — Profiles like `default` (56KB) and `qa-agent` (50KB) have large state.md because they accumulate handoff history. Other profiles (153B) are nearly empty. This is not a bug — it's auto-managed by the loop-engineering system. Don't try to "compact" or "normalize" without explicit user instruction.

4. **Profile dirs without `.git` is EXPECTED** — Don't try to `git init` them. They're isolated runtime dirs, version-controlled by the parent `~/.hermes` repo.

5. **Filter cron-output dirs from "untracked" count** — `~/.hermes/cron/output/<job-hash>/<timestamp>.md` is expected runtime output. When counting untracked files, filter:
   ```bash
   git ls-files --others --exclude-standard | grep -vE "^cron/output/" | wc -l
   ```
   Otherwise the count looks alarming (11+ files just from today's cron runs).

6. **Use parallel terminal calls for speed** — Steps 1-4 are independent. Run them in parallel using the terminal tool's `background=false` mode but grouping into 1-2 batches. Sequential = 4 round-trips; parallel = 1-2 round-trips. Saves time on daily cron budget.

7. **Cron delivery: don't use send_message** — When run as a cron job, the final report IS the delivery. The system auto-delivers it to the configured destination. Just produce the report as the final response. If you have nothing to report (truly silent day), respond with exactly `[SILENT]` to suppress delivery.

8. **State.md update is MANDATORY for engineering-lead profile** — The cron prompt explicitly says "Update state.md". Don't skip this step. Use `patch` (not `write_file`) to preserve existing content + add a new "Daily Code Health Check — YYYY-MM-DD" section at the end.

9. **/tmp has many benign upgrade markers** — `hermes-commit-sha.txt`, `hermes-env-skeleton.txt`, `hermes-env-restore.sh` (978b) are from `hermes update` operations, NOT from session work. Don't include them in "actionable leftovers" count.

10. **Date format consistency** — Use `YYYY-MM-DD` (ISO 8601) throughout the report. The state's `updated:` field uses ISO 8601 with timezone offset (`2026-06-26T09:05:00+07:00`). Stay consistent.

11. **Filter table by category, not just count** — "84 uncommitted" alone is meaningless. Break down by:
    - Runtime state (caches, cron outputs, snapshots) → expected, ignore
    - Code changes (.py/.sh) → report separately as "uncommitted CODE"
    - Untracked (??) vs modified (M) → distinguish
    - Then categorize as ✅/⚠️/🔴 based on the breakdown

12. **Test count from `find` ≠ test coverage** — Reporting "3000 tests" doesn't mean they're passing. Daily health check should NOT claim test health without running them. Use "Not run today (cron job)" as the honest status.

13. **Profile state.md mtime is auto-updated** — When the engineering-lead cron runs daily, it overwrites `state.md`. This shows in the mtime as "today". Don't interpret this as "the profile was actively worked on today" — it's just the cron cycle. Cross-reference with the handoff history table inside state.md to know real activity.

14. **macOS has NO `timeout` command** — `timeout 60 cmd` fails with `timeout: command not found` on macOS (it exists on Linux/WSL only). For bounded test runs on macOS, use ONE of:
    - `gtimeout` (install via `brew install coreutils` — may not be present)
    - **`terminal(background=true)` + `process(action='poll')` — preferred pattern** (see pitfall #15)
    - Pure `&` shell backgrounding inside `terminal(foreground)` errors with "Foreground command uses '&' backgrounding. Use terminal(background=true)"

15. **Use `terminal(background=true)` for test suites that may exceed the foreground timeout** — pattern:
    ```bash
    terminal(command="cd ~/.hermes/hermes-agent && ./venv/bin/pytest tests/test_X.py -q > /tmp/health.log 2>&1; echo EXIT:\$? >> /tmp/health.log",
             background=true, notify_on_complete=true, timeout=120)
    ```
    Then poll: `process(action='poll', session_id=<id>, timeout=60)` or wait for notification. Read result with `read_file(path=/tmp/health.log)`. This is the ONLY safe pattern for bounded-time test execution on macOS.

16. **Use the hermes-agent venv pytest, not system pytest** — full path is `~/.hermes/hermes-agent/venv/bin/pytest` (Python 3.11). System `python3 -m pytest` and `/usr/bin/python3 -m pytest` both fail with `No module named 'pytest'`. The venv also has all hermes-agent's dependencies installed. Same venv pattern: `./venv/bin/python`, `./venv/bin/pytest`.

17. **Sample test runs, not full suite** — for daily health, run 3-5 FAST test files (5-10 tests each, < 2s wall) to get a real pass/fail signal in < 2s total. Full suite takes 5+ min and is dominated by integration/e2e/stress tests that don't add health signal. Suggested sampler (fast, self-contained, no env deps):
    - `tests/test_output_cap_parsing.py`
    - `tests/test_code_skew.py`
    - `tests/test_account_usage.py`
    - `tests/test_bitwarden_secrets.py`
    - `tests/test_yuanbao_pipeline.py`
    ~148 tests in ~1.4s, gives both pass count and any regressions in core logic.
    
    **3-file minimum is enough for daily cron (06-29 verified):** `test_account_usage.py` + `test_bitwarden_secrets.py` + `test_yuanbao_pipeline.py` = 131 tests in 0.95s. Skip the 2 extras unless investigating a specific regression.

18. **Treat 13 pre-existing test collection errors as KNOWN STATE, not new failures** — see `references/session-2026-06-28.md` for the full list. They're interface drift in the hermes-agent source (`tools.approval._strip_line_comment`, `tools.cronjob_tools._execute_job_now`, `gateway.slash_commands._model_switch_skew_guard` all missing). Daily check flags them as `⚠️ Stale test files` — do not try to fix in daily health scope.

19. **Cron output dirs accumulate fast and inflate "untracked" counts** — `~/.hermes/cron/output/<job-hash>/` adds 12-24 files per cron run per day. The engineering-lead profile's own daily health check generates ~12-24 output files in `~/.hermes/cron/output/28c34e383254/` per day. After 5-7 days, the directory has 100+ files. The untracked count is dominated by these. Don't add `cron/output/` to `.gitignore` — the untracked count is informative (low count = cron not firing). Just disclose in the report.

20. **Use `--ignore=tests/honcho_plugin` to skip a known-bad collection set** (06-29 verified) — The `tests/honcho_plugin/` subdirectory has 7+ test files that error during collection. Without the filter, the full suite aborts on first collection error (with `-x`) or shows 13+ errors. With `--ignore=tests/honcho_plugin`, you get a clean baseline run and can track the 13 pre-existing interface-drift errors as a stable number. Add the flag to all daily-check pytest invocations.

21. **Dojo tasks.json overnight delta is a leading indicator** (06-29 first observed) — The dojo task count changed from 63→64 between 06-28 09:11 and 06-29 09:02, despite the daily check showing "0 pending" both days. Some background job (likely content-director or dojo-internal scheduler) created AND completed a task overnight. Report the delta, not just the snapshot:
    ```bash
    jq '.tasks | map(.status) | group_by(.) | map({status: .[0], count: length})' ~/.hermes/dojo/tasks.json
    ```
    A delta > 0 between consecutive days means the dojo pipeline is alive; delta = 0 for 3+ days is a stuck-system signal.

22. **State.md bloat early-warning at >200KB (qa-agent is the canary)** (06-29 verified at 216KB) — The `multi-agent-heartbeat` skill triggers compaction at 250KB. Daily check should WARN at 200KB so the team has a 50KB buffer to act. Add to the profile freshness loop:
    ```bash
    for f in ~/.hermes/profiles/*/state.md; do
      size=$(wc -c < "$f")
      if [ "$size" -gt 204800 ]; then
        echo "⚠️ $(basename $(dirname $f)): state.md ${size}b (>200KB)"
      fi
    done
    ```

## Verification

After updating state.md:
```bash
test -f ~/.hermes/profiles/<profile>/state.md && echo "state.md updated"
tail -20 ~/.hermes/profiles/<profile>/state.md | grep -q "Daily Code Health Check — $(date +%Y-%m-%d)" && echo "today's section present"
```

If using git, the state.md change will be uncommitted (it's runtime state, not source code) — that's expected.

## Related Skills

- `hermes-daily-backup` — Git push to remote (mutates remote, this skill is read-only)
- `hermes-security-audit` — Vulnerability scan (different scope)
- `multi-agent-heartbeat` — Cross-profile pending task sweep (different scope)
- `self-verify-after-workaround` — Verification methodology when reporting counts

## Support Files

- `references/report-template-2026-06-26.md` — Real output from the first run (this skill was created from that session). Documents the 580-modified-tracked-subdir finding, profile state.md size variance pattern, and the parallel-call structure used.
- `references/baseline-2026-06-27.md` — Steady-state numbers from 2 consecutive runs. Use to detect anomalies fast: diff new metrics against this baseline, report only deltas, keep recommendations ≤3.
- `references/session-2026-06-28.md` — 3rd-run findings: shared-git-repo architecture insight, test collection errors as known state, sample-test pattern (5 files, 1.4s, 148 tests), cron-output-dir accumulation pattern, /tmp leftovers unchanged for 2 days. Use for the macOS-no-timeout + venv pytest + bounded-test pattern (terminal(background=true) + process(poll)).
- `references/session-2026-06-29.md` — 4th-run refinements: `--ignore=honcho_plugin` flag, 3-file sample minimum (131 tests in 0.95s), dojo overnight delta as leading indicator, state.md bloat early-warning at >200KB, confirmed 0/17 profiles have own .git.