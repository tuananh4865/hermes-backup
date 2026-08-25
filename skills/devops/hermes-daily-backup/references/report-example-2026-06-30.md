# Hermes Daily Backup — 2026-06-30 03:00 Run

**Status:** ✅ SUCCESS (with 2 mid-flight issues resolved)
**Operator:** Hermes Agent (cron job, no user present)
**Commits:** `89e69b2da` (hermes incremental) + `028bbab28` (content-creator metadata, force-amended)

---

## What happened

Standard 3AM backup ran with all PITFALL #21 protocols. Pre-flight .env snapshot clean (9 files). Git fetch showed local=origin, no divergence, no reset needed. Hermes incremental: 114 files committed + pushed (`89e69b2da`).

Content Creator metadata snapshot: wrote `snapshot.md` to `$OLDPWD/content-creator-meta-2026-06-30/`, then `cp -r "$OLDPWD/$SNAP_DIR" ./content-creator-meta-2026-06-30` from inside `~/.hermes` — this produced a **nested `content-creator-meta-2026-06-30/content-creator-meta-2026-06-30/snapshot.md`** because the destination dir already existed. Committed + pushed `0fab8e0bb` with the bug.

Then ran `git reset --soft HEAD~1` to fix the nesting — but **root volume was 100% full** (228Gi used, 119Mi free, `/tmp/powerlog` 23G Apple system lock). `git reset --soft` failed with "Out of diskspace" mid-flight. Repo state became: commit `0fab8e0bb` already on origin, working tree dirty with staged deletes, index.lock present.

## Recovery (3 steps)

1. **Disk free check first** (couldn't add files, but git status was readable): `df -m /` confirmed 119Mi free — only 119Mi available, but no large staging needed.
2. **`git restore --staged --worktree content-creator-meta-2026-06-30/`** — dropped the staged nested-dir deletes, restored the dir from HEAD.
3. **`cp <abs-path>/snapshot.md ~/.hermes/content-creator-meta-2026-06-30.md`** (option A from pitfall #22h — single file at top level, not nested).
4. **`git add content-creator-meta-2026-06-30.md` + `git rm -rf --cached content-creator-meta-2026-06-30/` + `git commit --amend`** (no message change, force-update).
5. **`git push origin main --force`** — pushed `028bbab28`, replacing `0fab8e0bb`. Verified blob hash identical (`86864576b2ff1c1174a1d5336fc4fb41eb0b9e52`) before force-push.

## Final state

| Item | Value |
|------|-------|
| Hermes commit | `89e69b2da` |
| Content Creator commit | `028bbab28` (force-amended) |
| Total commits | 2 (clean, no marker commits) |
| Force-push | 1 (safe — blob content unchanged) |
| .env files | 9 snapshotted, 0 needed restore |
| `.env` verified on disk | ✅ all 9 present, non-empty |
| Hermes URL | https://github.com/tuananh4865/hermes-backup/commit/028bbab28 |
| Disk full warning | ⚠️ 119Mi free — recommend anh clean `/tmp/powerlog` or other space hogs |

## Key takeaways

1. **PITFALL #22f — Diskspace check MUST run BEFORE git ops**, not after. The 06-30 failure was: ran pre-flight .env snapshot (PITFALL #21) ✅, but skipped pre-flight disk check → hit "Out of diskspace" mid-reset. **Fix**: add `df -m /` check at start of cron script, abort if <500Mi free.
2. **PITFALL #22h — `$OLDPWD` is unreliable across `terminal()` calls with different `workdir`** — the bug that created the nested dir. Use absolute paths or `rsync` with trailing slash. The recovery (pitfall #22g) works, but the prevention is cheaper.
3. **PITFALL #22g — `commit --amend` + `push --force` is the clean recovery** when (a) blob content is identical (verify via `git rev-parse`), (b) you control the repo alone, (c) it's a single-writer backup repo. 1 commit instead of 2, history clean.

## Disk cleanup recommendation for anh

```
$ df -h /
Filesystem        Size    Used   Avail Capacity
/dev/disk3s1s1   228Gi   202Gi   119Mi   100%   ← near full

Largest culprits:
- /tmp/powerlog: 23G (Apple system, requires sudo to purge)
- Time Machine local snapshots: variable size
- Hermes state.db: 1.0G
- Hermes hermes-agent/: 2.1G
- Hermes state-snapshots/: 704M
- Hermes cron/: 913M
```

Recommend: add a daily cron that prunes `~/.hermes/state-snapshots/` to last 7 days (vs current unbounded), and thin Time Machine local snapshots via `tmutil thinlocalsnapshots / 9999999999`.

## Maps to pitfalls
- #22f (NEW) — Pre-flight disk check
- #22g (NEW) — Recovery via amend + force-push
- #22h (NEW) — `$OLDPWD` nested-dir bug
- #20p — Template vs real .env classification (no templates today, all 9 are real)
- #21a — PITFALL #21 verified effective
- #22d — In-place repo (no rsync needed; `git reset --mixed` path)
- #22e — snapshot.md format (discovered from prior commit `d3625d846`)
- #22c — Quote paths with spaces (used throughout)
