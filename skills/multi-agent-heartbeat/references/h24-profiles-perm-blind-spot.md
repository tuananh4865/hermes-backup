# H24 — Profile subdir perm blind spot (2026-06-24 18:31)

## What happened

The 30m heartbeat at 2026-06-24 18:31 caught a security regression that H11-H23 all
missed: 8 files in `~/.hermes/profiles/*/` regressed from 600→644, undetected for
13 consecutive sweeps (~9.5 hours).

Affected files (all 644 → fixed to 600):
- `~/.hermes/profiles/security-engineer/config.yaml`
- `~/.hermes/profiles/operations-manager/config.yaml`
- `~/.hermes/profiles/qa-agent/config.yaml`
- `~/.hermes/profiles/engineering-lead/config.yaml`
- `~/.hermes/profiles/research-lead/config.yaml`
- `~/.hermes/profiles/code-reviewer/config.yaml`
- `~/.hermes/profiles/research-lead/kanban.db`
- `~/.hermes/profiles/content-director/kanban.db`

## Root cause

The H11 recipe (originated 2026-06-24 08:31 when `~/.hermes/config.yaml` regressed)
only `stat`'d a hardcoded list of paths:

```bash
stat -f "%Sp %N" ~/.hermes/config.yaml ~/.hermes/auth.json ~/.hermes/state.db ~/.hermes/profiles/*/state.db
```

That command:
- ✅ Catches `config.yaml` / `auth.json` / `state.db` in `~/.hermes/` root
- ✅ Catches `state.db` in each profile
- ❌ MISSES `config.yaml` / `kanban.db` / `auth.json` in profile subdirs

When H19-H23 re-ran the watch (per the H11 "re-verify after fix" rule), they
checked the same hardcoded list and reported "0 regressions" every sweep — but
the profile subdir files were already 644. The watch had a silent blind spot.

## Why it took 13 sweeps to notice

The H11 recipe was designed to verify the SINGLE file that originally regressed
(`~/.hermes/config.yaml` in `~/.hermes/`). The "re-verify cadence" rule
(H19-H23 used it correctly) was a fix-stability check, not a comprehensive
sweep. As long as `config.yaml` stayed 600, the heartbeats confidently
reported "0 regressions" — but the 8 profile-subdir files had drifted to 644
undetected for the entire 9.5h window.

## The fix

Replace the per-file `stat` with a `find`-based full-sweep:

```bash
find ~/.hermes -maxdepth 3 \( \
    -name "*.env" -o -name "auth.json" -o -name "config.yaml" \
    -o -name "*.db" -o -name "kanban.db" -o -name "memory_store.db" \
    -o -name "sessions.db" -o -name "trajectory_index.db" \
\) -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/state-snapshots/*" \
  2>/dev/null | while read f; do
    mode=$(stat -f "%Lp" "$f")
    if [ "$mode" != "600" ] && [ "$mode" != "700" ]; then
        echo "REGRESSION: $mode $f"
    fi
done
```

This enumerates ALL sensitive files by NAME (not by hardcoded path), so future
file additions in any subdir are caught automatically.

## Lessons for the heartbeat protocol

1. **Hardcoded path lists = silent blind spots.** Use `find -name` patterns
   that match by FILE TYPE, not by explicit path. The same lesson applies to
   the file-existence checks in `references/operations-manager-audit-template.md`
   and any other watch that uses a fixed list of targets.

2. **"Re-verify after fix" is a stability check, not a full sweep.** The H11
   watch verified the SAME file it fixed. For comprehensive coverage, the
   sweep must enumerate ALL candidates every time — not just the one that
   was last known to regress.

3. **"0 regressions for 9.5h" is suspicious, not reassuring.** When the same
   check has reported zero findings for an unusual number of consecutive
   sweeps, treat that as a SIGNAL to widen the check, not as confirmation
   the system is clean. The 8 profile-subdir files were 644 the entire time.

4. **Defense in depth: pre-fix content check.** Before `chmod 600`, grep for
   plaintext secrets. All 8 H24 files contained `env:MINIMAX_API_KEY` or
   empty values, so they were safe to auto-fix. If a file contains a literal
   `sk-cp-...` or `ghp_...` string, the fix is escalation, not `chmod`.

## Pattern: "watch evolution" audit

When a security/QA watch has been running unchanged for >7 sweeps, the
heartbeat should:

1. Note the watch in the row ("H24: security watch widening per H11 lesson")
2. Explicitly expand the find to cover more file types
3. Document the old vs new find command in the sweep note
4. Update the skill (this file is the result)

This is a **one-time widening per watch class**, not a per-sweep check. After
the widening, the expanded find is the new baseline.

## Related

- H11 (2026-06-24 08:31) — original `~/.hermes/config.yaml` regression + first auto-fix
- H19-H23 (2026-06-24 14:04-18:00) — "re-verify after fix" sweeps that all
  reported "0 regressions" while the profile-subdir drift was already 644
- H24 (this file) — full-sweep expansion + 8-file fix
