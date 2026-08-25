# Cron Truth Recipe — `hermes cron list` is Ground Truth

**Lesson learned (2026-06-26, qa-agent H34/H38):** State.md file mtime is **NOT** a reliable proxy for cron health. A "0 findings, 0 pending" audit log entry is only APPENDED if there is something to report — clean cron runs do not always rewrite state.md. Mtime can lag cron by hours or days even when cron is firing on schedule.

This caused 32+ sweeps of false-positive "multi-profile cron fault" classifications before being corrected with one `hermes cron list` call.

## The Recipe (always apply when assessing cron health)

```bash
hermes cron list
```

Output fields that matter:
- `Last run: <timestamp>` — when cron actually last fired
- `ok` / `error: <message>` — exit status from that run
- `Next run: <timestamp>` — schedule confirmation

**If `last_run` is recent AND status is `ok` → profile is HEALTHY** regardless of state.md mtime.

## Verification table from H34 (correlates file mtime vs cron truth)

| Profile | state.md mtime | cron last_run | gap | diagnosis |
|---|---|---|---|---|
| code-reviewer | 2026-06-26 12:01:01 | 2026-06-26 12:01:06 | 5s | HEALTHY (mtime IS the audit append) |
| security-engineer | 2026-06-25 20:16:09 | 2026-06-26 03:01:10 | ~7h | HEALTHY (mtime from prior day, cron ran today) |
| operations-manager | 2026-06-26 12:00:54 | 2026-06-26 12:01:30 | 36s | HEALTHY |
| memory-curator | 2026-06-16 20:12:50 | 2026-06-26 02:03:26 | ~10d | HEALTHY (mtime stale 10d, cron fires daily) |
| research-lead | 2026-06-25 20:16:09 | 2026-06-25 18:01:46 | -2h | ⚠️ REAL FAULT (Connection error) |

**Lesson:** Mtime gap alone is not a fault signal. Cross-reference with `hermes cron list` before classifying.

## When state.md mtime IS the right signal

- When the cron writes to state.md as part of its normal output (e.g., operations-manager audit, code-reviewer noon watcher) — mtime ≈ last_run
- When the cron does NOT touch state.md on clean runs (e.g., security-engineer daily vuln scan only appends on findings) — mtime can lag

## Anti-pattern: cascading false-positive fault pattern

The H28/H29/H34 "multi-profile cron fault pattern" was a measurement artifact reinforced by 32+ sweeps of measuring the wrong signal. The pattern looked convincing (3 profiles, 217h+ staleness, recurring) but dissolved once ground truth was checked.

**Rule:** Before declaring a recurring fault pattern across 3+ profiles, run `hermes cron list` ONCE and cross-reference. If 0 errors there, the pattern is a measurement artifact.

## Related

- H28 (code-reviewer), H29 (security-engineer), H34 (operations-manager) "faults" — all RESCINDED, were mtime-vs-cron gaps
- Real research-lead Trend Scan fault — 2026-06-25 18:01, RuntimeError: Connection error + telegram delivery failed
- 2026-06-26 18:03: research-lead cron recovered, last_run ok

## See also

- `hermes cron list` — ground-truth source
- `references/cron-subprocess-path-issue.md` — different cron pitfall (PATH for python3.14 in crontab)
