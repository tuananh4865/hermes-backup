# Daily Backup Report Format — 2026-06-06

## Standard report shape Anh expects

After every daily backup cron run, produce a short report with:

- **Status** — ✅ SUCCESS or ❌ FAILED (with reason)
- **Commit SHA** — full 11-char hash from `git log --oneline -1`
- **Push** — short range like `8fee7223e..859d44e61 main -> main` from `git push` output
- **Files changed** — count from `git diff --cached --shortstat` (the `<N> files changed` field)
- **Insertions / deletions** — the `+N / -N` pair from the same `--shortstat` output
- **Errors** — always include the line "None" if no errors (Anh wants explicit confirmation, not silence)

## Commands that produce the exact fields

```bash
# Files changed + insertions + deletions (one line, ~140 chars)
git diff --cached --shortstat
# Output: " 1335 files changed, 178287 insertions(+), 41388 deletions(-)"

# Last commit hash (full 11 chars)
git log --oneline -1 | awk '{print $1}'

# Push range (captured from git push output)
git push origin main 2>&1 | grep "main -> main"
# Output: "   8fee7223e..859d44e61  main -> main"
```

## Inline git identity for cron

Cron-spawned sessions have no global `user.name`/`user.email` configured by default. `git commit` fails with `Author identity unknown`. Always pass identity inline:

```bash
git -c user.name="Hermes Backup" -c user.email="backup@hermes.local" \
  commit -m "Backup hermes full: $(date +%Y-%m-%d)"
```

Do NOT use `git config user.name "..."` (writes to repo `.git/config`, pollutes state). The `-c` flag is per-command only.

## Snapshot rotation — how deltas appear (observed 2026-06-06)

The `state-snapshots/` directory holds dated folders like:
- `20260531-114251-pre-update/` — previous snapshot
- `20260605-134405-pre-update/` — new snapshot

On each backup, git detects these as **renames** (not deletes + creates) because file contents overlap. The `git commit` output shows lines like:
```
rename state-snapshots/{20260531-114251-pre-update => 20260605-134405-pre-update}/config.yaml (99%)
```

This is normal — explains why daily diffs look "large" when in practice it's just a snapshot folder rotation. Don't flag this as unexpected churn in the report.

## Observed scale (2026-06-06 baseline)

- ~1,300 files changed per day
- ~+178K / -41K lines per day
- Push completes in seconds (repo is text-heavy, no large binaries)
- Commit typically takes < 2s for `git add .` even with 1,300+ files (most are small JSON/MD)
