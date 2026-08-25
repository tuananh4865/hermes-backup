# State File Template — security-engineer

The canonical state file lives at `~/.hermes/profiles/security-engineer/state.md` (NOT `state/state.md` — that subdirectory path is wrong; see SKILL.md Pitfall #4). On first run, no bootstrap is needed: just `write_file` the full template below with the first run's data filled in.

## Full Template

```markdown
# Security Engineer — Daily Scan State

**Profile:** security-engineer
**Owner:** Tuấn Anh
**Cron schedule:** Daily

---

## Last Run: YYYY-MM-DD

**Status:** ✅ PASS — N CRITICAL, N HIGH, N MEDIUM (auto-fixed), N LOW

### Scans Performed

| Scan | Result |
|------|--------|
| Profile `.env` perms (N files) | ✅ All 600 / ❌ N wrong |
| Main `~/.hermes/.env` perms | ✅ 600 / ❌ was XXX |
| `auth.json` perms (N files) | ✅ All 600 / ❌ N wrong |
| `shell=True` in profile/hook .py | ✅ 0 matches / ❌ N matches (CRITICAL) |
| `eval()` in profile/hook .py | ✅ 0 matches (excluding safe wrappers) / ❌ N matches |
| `exec()` in profile/hook .py | ✅ 0 matches / ❌ N matches |
| `pickle.loads` in profile/hook .py | ✅ 0 matches / ❌ N matches |
| Hardcoded API keys (sk-, ghp_, glpat-, hf_, AKIA, anthropic-, Bearer eyJ) | ✅ 0 / ❌ N |
| Hardcoded secret/token literals | ✅ 0 / ❌ N |
| Hook dir perms (should be 700) | ✅ All 700 / ⚠️ N at 755 → **FIXED** |
| Hook .py file perms (should be 600) | ✅ All 600 / ⚠️ N at 644 → **FIXED** |

### Findings

#### CRITICAL (auto-fix NOT authorized — manual review needed)
- **None this run** / List each finding here with file:line, the dangerous pattern, and recommended fix.

#### HIGH (auto-fixed)
- **N `.env` / `auth.json` files at wrong perms**:
  - `<full-path>` (was X, fixed to 600)
- **Action:** `chmod 600` on N files
- **Risk:** Local users + processes inheriting umask could read API keys / OAuth tokens.

#### MEDIUM (auto-fixed)
- **N hook subdirs at 0o755** (world-readable):
  - `<full-path>` for each
- **N hook .py files at 0o644/0o711**:
  - `<full-path>` for each
- **Action:** `chmod 700` on dirs, `chmod 600` on .py files
- **Risk:** Session metadata and hook handler logic readable by other local users.

#### LOW (informational — intentional)
- `hook_wrapper.sh` files at `0o755` — must be executable for Hermes gateway
- `gsd-*.sh/.js` hooks at `0o755` — invoked by Claude Code as executables
- `<other informational items>`

### Out of Scope (not scanned)
- Skill subdirs under `~/.hermes/profiles/*/skills/*/scripts/*.py` — third-party Hermes Hub skill content, not security-engineer's own code
- macOS Spotlight `.DS_Store` files
- `~/.hermes/hermes-agent/` source code (vendored)

### Notes
- No CRITICAL findings this run. / Found N CRITICAL — see findings above.
- All N profile `.env` files consistently at `0o600` — `env-permission-guard` hook is doing its job.
- No changes to `.env` content (no rotate triggered).
- Previous run date: YYYY-MM-DD (for diff context)

---

## Run History

| Date | CRITICAL | HIGH | MEDIUM | LOW | Auto-Fixed |
|------|----------|------|--------|-----|------------|
| YYYY-MM-DD | N | N | N | N | ✅ Yes / ❌ No |
```

## Cron Delivery Summary

The cron job emits a compact summary in the delivery channel (Telegram topic). Use this format:

```
🛡️ Security Daily Scan — YYYY-MM-DD

Summary: ✅ PASS / ❌ FAIL — N CRITICAL, N HIGH, N MEDIUM (auto-fixed), N LOW

| Scan | Result |
|------|--------|
| .env perms (N) | ✅ 600 |
| auth.json (N) | ✅ 600 |
| shell=True | ✅ 0 |
| eval/exec | ✅ 0 |
| Hardcoded secrets | ✅ 0 |
| Hook dirs | ⚠️ N at 755 → FIXED |
| Hook .py | ⚠️ N wrong → FIXED |

Findings:
- 🟡 MEDIUM (auto-fixed): N hook subdirs tightened from 0o755 to 0o700
- 🟡 MEDIUM (auto-fixed): 2 hook .py files tightened to 0o600 (one also had stray +x bit stripped)
- 🟢 LOW: hook_wrapper.sh / gsd-*.sh at 0o755 — intentional

State updated: ~/.hermes/profiles/security-engineer/state/state.md
```

## First-Run Bootstrap

If `state.md` does not exist yet, no bootstrap is needed — just `write_file` the full template above with the first run's data filled in. The path is `~/.hermes/profiles/security-engineer/state.md` (one file, no subdirectory).

## Updating Run History

After every run, append one row to the table by editing the file directly. The table stays short — past N runs can be archived.

## State Hygiene

- Keep state.md under 200 lines — older history can move to `state.archive.md`
- Never edit past "Last Run" sections — only append new "Last Run" at top, rotate old to archive
- Always include the previous run date in "Notes" — gives the cron reader diff context

## When to Update Manually

Auto-fix updates state.md after each run. Manual updates only needed when:

- A new class of finding appears (extend the "Findings" template)
- The cron schedule changes (edit the header)
- The owner authority expands (update the SKILL.md "Owner Authority" table — this propagates to next cron)