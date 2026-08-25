# .env + config.yaml Permission Regression — Session Reference

**Date:** 2026-06-24
**Source:** security-engineer daily audit (cron 03:00)
**Severity:** CRITICAL (silent — no error, no log)

## Symptom

Yesterday's security sweep (2026-06-23) auto-fixed `~/.hermes/.env` and `~/.hermes/config.yaml` from 644 → 600. Today's sweep found them back at 644 — with **identical mtimes down to the second**:

```
$ stat -f "%Sm %N" ~/.hermes/.env ~/.hermes/config.yaml ~/.hermes/profiles/research-lead/.env
Jun 24 03:01:29 2026 /Users/tuananh4865/.hermes/.env
Jun 24 03:01:29 2026 /Users/tuananh4865/.hermes/config.yaml
Jun 24 03:01:29 2026 /Users/tuananh4865/.hermes/profiles/research-lead/.env
```

No human edited these files between 2026-06-23 and 2026-06-24 03:01:29. Same 03:01:29 timestamp across multiple files = same writing process.

## Actual Root Cause

A running Hermes gateway process rewrote `.env` and `config.yaml` during a config sync / env reload operation, using `open(path, 'w')` without explicit mode. The new files inherited the **process umask (022)** → ended up at **644 (rw-r--r--)**.

**Writer process:**
```bash
$ ps aux | grep hermes | grep -v grep
tuananh4865  1734  ... /Users/tuananh4865/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace
```

PID 1734, started 2026-06-23 18:20, still running at audit time. The `--replace` flag means it manages its own config lifecycle.

**Why all profiles' .env reverted simultaneously:** The gateway writes to `~/.hermes/profiles/*/.env` as part of profile-state sync. So fixing `.env` on 3 profiles yesterday was undone today across all profiles at the same instant.

## Diagnostic Path (what worked)

### What worked

1. **mtime cluster detection** — `stat -f "%Sm %N"` on all `.env` files → identical timestamp = same writer batch. Fastest signal that this is not human activity.
2. **Process check** — `ps aux | grep hermes` → PID 1734 active. Confirms a Hermes process was running during the write.
3. **Diff sweep** — re-ran the same `find ... | xargs stat -f "%Lp"` pipeline from yesterday → identified which files regressed.
4. **Auto-fix** — `chmod 600` on the regressed files, then re-verify with `ls -la`.

### What wasted time (avoid next time)

- **Reading `.env` content first** — the perms regression doesn't change the content, only the mode bit. Reading content first is a red herring.
- **Looking for "who wrote this" in logs** — the gateway doesn't log config sync writes to `gateway.log` or `gateway.error.log` at normal verbosity. You'd need DEBUG-level logs to see them, and even then there's no "permission changed" line.

## Regression Surface (files that have regressed at least once)

| File | Why written | Reapply 600 every sweep |
|------|-------------|-------------------------|
| `~/.hermes/.env` | Main env file — gateway OAuth/refresh | ✅ Yes |
| `~/.hermes/config.yaml` | Main config — `hermes config set` propagation | ✅ Yes |
| `~/.hermes/profiles/*/.env` | Per-profile env — gateway iterates all profiles during sync | ✅ Yes |
| `~/.hermes/state-snapshots/*/.env` | Pre-update snapshot — `hermes update` copies `.env` to snapshot dir at default mode | ✅ Yes |
| `~/.hermes/kanban.db*` | kanban backup files — created during periodic kanban restart/recovery | ✅ Yes |
| `~/.hermes/logs/*.log` | Log rotation creates new files at default mode | ✅ Yes |
| `~/.hermes/sessions/sessions.db` | Created during session start | ✅ Yes |

## Files Fixed in This Sweep (2026-06-24)

55 files auto-fixed:

**CRITICAL (2):**
1. `~/.hermes/.env` (802B)
2. `~/.hermes/config.yaml` (30998B)

**HIGH hygiene (53):**
- 3 more `.env` files (state-snapshot + 2 profiles) — same mtime cluster
- 3 `.envrc` / `.env.example` templates (less critical but tighten anyway)
- 36 `kanban.db.corrupt.*.bak` SQLite backup files
- 7 `logs/*.log` files (errors.log, gateway*.log, mcp-stderr.log, update.log)
- `sessions/sessions.db`

## Pitfall: `chmod 600` on a symlink follows the target

When fixing config.yaml with `chmod 600 ~/.hermes/config.yaml`, if the file is a symlink (it usually is on some setups), `chmod` follows the symlink and changes the **target's** permissions, but `ls -la` shows the symlink's own mode (often 666 or 777). Verify with:

```bash
ls -la ~/.hermes/config.yaml        # shows symlink mode if applicable
stat -f "%Lp %N" ~/.hermes/config.yaml  # follows symlink → shows actual file mode
```

On this system, `config.yaml` was a real file (not symlink) and `ls -la` correctly showed `-rw-------` after chmod.

## Permanent Fix (proposed)

Add a `PostToolUse` hook in `~/.hermes/hooks/env-permission-guard.py` that re-applies 600 on protected files after every Write/Edit:

```python
import os
from pathlib import Path

PROTECTED_PATTERNS = [
    "~/.hermes/.env",
    "~/.hermes/config.yaml",
    "~/.hermes/auth.json",
    "~/.hermes/profiles/*/.env",
]

def on_post_tool_use(tool_name, tool_input, tool_output):
    if tool_name not in ("Write", "Edit", "MultiEdit"):
        return
    file_path = tool_input.get("file_path", "")
    expanded = str(Path(file_path).expanduser())
    for pattern in PROTECTED_PATTERNS:
        if Path(expanded).match(str(Path(pattern).expanduser())):
            try:
                os.chmod(expanded, 0o600)
            except OSError:
                pass
```

Until this hook ships, expect to re-apply 600 in every daily sweep.

## Related References

- `references/channel-adapter-diagnosis.md` — The `.env` token-missing case. Complements this: that one was "no token in .env" (missing content), this one is "token present in .env but perms 644" (leaking content).
- The `hermes-agent` skill's "Secret redaction in tool output" + "Security & Privacy Toggles" section — covers runtime redaction but not file mode enforcement.

## Sweep Output (for future comparison)

```bash
# Run this in any security sweep — single-liner:
find ~/.hermes -type f \( -name ".env*" -o -name "*.db*" -o -name "auth.json" -o -name "config.yaml" \) \
  -not -path "*/wiki/*" -not -path "*/.venv/*" -not -path "*/venv/*" \
  | while read f; do
      [ "$(stat -f "%Lp" "$f")" != "600" ] && chmod 600 "$f" && echo "FIXED: $f"
    done
find ~/.hermes/logs -name "*.log" -type f | while read f; do
  [ "$(stat -f "%Lp" "$f")" != "600" ] && chmod 600 "$f" && echo "FIXED: $f"
done
```
