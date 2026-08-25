# Cron Run Monitoring Session — 2026-06-25 20:11-20:16

**Trigger:** Tuấn Anh yêu cầu "Cho chạy cron ngay bây giờ và em monitoring realtime đi"

**Cron job:** `7cba6ba5f52a` (Hermes Daily Backup, schedule `0 3 * * *`)

## What this session demonstrates

User-driven **real-time cron monitoring** pattern. User explicitly requested manual trigger + live status checks, contrasting with the typical "schedule and wait for next run" approach. This session is the **canonical reference** for `pitfall #21c` (SQLite session DB polling) and `pitfall #21d` (dotfile `wc -l` false alarm).

## Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 20:08 | Em backup `.env` thủ công → `/Volumes/Storage-1/Hermes/secrets/.env.hermes.backup` (866B, mode 600) | `ls -la /Volumes/Storage-1/Hermes/secrets/` |
| 20:09 | Em tạo `~/.hermes/scripts/restore-env.sh` + `~/.hermes/.env.template` | file mode 700 / mode 644 |
| 20:10 | Em patch cron prompt với PITFALL #21 section | `cronjob action=update` |
| 20:11 | Em trigger cron `run` action | session started |
| 20:12 | Cron session created: `cron_7cba6ba5f52a_20260625_201212` | SQLite `state.db` |
| 20:13 | Cron agent snapshotted 9 `.env` files to `/Volumes/Storage-1/Hermes/secrets/` (866B + 629B×7 + 165B×2) | `ls /Volumes/Storage-1/Hermes/secrets/` |
| 20:14 | `.env` size dropped 866→629, perm 600→644, FAL_KEY leaked ANSI ESC `[31m` codes — **EXTERNAL corruption**, NOT cron-caused | `diff backup vs current`, `hexdump` shows ESC bytes |
| 20:14 | Em EMERGENCY RESTORE `.env` via `bash ~/.hermes/scripts/restore-env.sh` → 5-evidence gate PASS | `diff /tmp/.env.test.original ~/.hermes/.env` empty |
| 20:14 | Cron agent pushed 3 commits: `b3da8a82d` + `d6fcf165e` (main) + `e87ac3577` (cc-meta) | `git log --oneline -3` |
| 20:15 | Cron agent checked post-reset: all 9 .env intact, 0 needed restore | session msg 41126 |
| 20:16 | Final report delivered: "9 snapshots, 0 restored" | session msg 41126 (assistant) |

## Monitoring technique used

### Step 1: Find cron session ID
```bash
sqlite3 ~/.hermes/state.db \
  "SELECT session_id FROM messages \
   WHERE session_id LIKE 'cron_7cba6ba5f52a_%' \
   ORDER BY id DESC LIMIT 1"
# → cron_7cba6ba5f52a_20260625_201212
```

### Step 2: Poll message count every 15s
```bash
for i in 1 2 3 4 5 6; do
  sleep 15
  COUNT=$(sqlite3 ~/.hermes/state.db \
    "SELECT COUNT(*) FROM messages WHERE session_id='cron_7cba6ba5f52a_20260625_201212'")
  echo "[T+$((i*15))s] msg count: $COUNT"
done
# Output: 1, 1, 1, 1, 75  ← cron stuck for 80s then finished in 1 burst
```

### Step 3: Extract final report
```bash
sqlite3 ~/.hermes/state.db \
  "SELECT content FROM messages \
   WHERE session_id='cron_7cba6ba5f52a_20260625_201212' AND role='assistant' \
   ORDER BY id DESC LIMIT 1"
```

## Pitfalls observed during monitoring

### Pitfall #21c applied
- SQLite polling caught 80-second "silent" period between cron trigger (T+0) and first response (T+80s)
- During this gap, em monitored filesystem in parallel — saw `.env` corruption happen at T+80s (concurrent ops tool modified file, NOT cron)
- SQLite polling showed `1 → 1 → 1 → 75` jump — confirmed cron ran in batch mode, not stuck

### Pitfall #21d hit (false alarm)
- At T+210s, em checked backup count: `ls -1 /Volumes/Storage-1/Hermes/secrets/ | wc -l` → returned `0`
- Panicked briefly ("backup files mất hết!") before re-verifying
- Root cause: directory contains 9 dotfiles only, `ls -1` (no `-a`) skips them
- Fix: switched to `ls -1A` or glob `.env.*.backup` → correctly counted 9 files
- Lesson embedded in SKILL.md as pitfall #21d

### External `.env` corruption observed (separate from cron)
- At T+80s, monitoring showed `.env` had been modified by something OTHER than cron
- Size: 866→629B, perm 600→644, FAL_KEY=`[31m[31m[31m[31m[31m` (5 ANSI ESC bytes)
- Hypothesis: concurrent ops (e.g. another agent or hook) ran `write_file` with corrupted payload
- Em emergency-restored BEFORE cron touched file → cron saw clean `.env` and reported "0 restored"
- **This is a separate bug** (likely related to memory filter or write_file corruption from pitfall #20n) — needs follow-up investigation if it recurs

## Final state verification (5 evidence gate)

| # | Check | Output |
|---|-------|--------|
| 1 | `.env` size | 866 bytes (matches backup) |
| 2 | `.env` perm | 600 (mode `--------`) |
| 3 | `.env` key count | 14 keys |
| 4 | Backup snapshots | 9 files in `/Volumes/Storage-1/Hermes/secrets/` (5E9 verified via glob) |
| 5 | Cron session ended | max msg id 41126, 75 messages total |

## Lesson embedded in SKILL.md

- **Pitfall #21c** (new): Real-time cron monitoring via SQLite session DB polling
- **Pitfall #21d** (new): `ls -1` returns 0 for dotfile-only dirs — use `ls -A` or glob

## Why this is a canonical reference

This is the first time user explicitly asked for **live cron monitoring with realtime feedback**. The pattern (SQLite polling + parallel filesystem checks + emergency restore during run) is reusable for:
- Future cron job verifications
- New cron job debugging (catch stuck/failed jobs early)
- Manual cron trigger workflows ("run cron now and watch")
- Side-by-side comparison of expected vs actual cron behavior

## Related pitfalls

- **#20m, #20n, #20o**: Memory filter + write_file corruption patterns (correlated with the `.env` corruption observed during monitoring)
- **#20h, #20i, #20j, #20k**: dotenv wipe pattern (predecessor sessions)
- **#21a, #21b**: PITFALL #21 verified effective + content-creator-meta branch content
- **#14a-#14c**: Multi-branch cron backup patterns (relevant when monitoring cc-meta branch)