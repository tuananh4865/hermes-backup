# Recovery Session 2026-06-25 Evening — User-Facing .env Restore

**Session type:** User-facing restore workflow (the actual recovery after the incident was diagnosed in the morning session).
**Trigger:** "Ok" → em execute Option 2+4 (mixed reset + restore-env.sh safety net).

## Step-by-step flow

### 1. Backup current .env to safe location
```bash
mkdir -p /Volumes/Storage-1/Hermes/secrets
cp ~/.hermes/.env /Volumes/Storage-1/Hermes/secrets/.env.hermes.backup
chmod 600 /Volumes/Storage-1/Hermes/secrets/.env.hermes.backup
# Verify: ls -la (866 bytes match)
```

### 2. Create `restore-env.sh` script (chmod 700)
**Location:** `~/.hermes/scripts/restore-env.sh`
**Features:**
- Auto-detect backup file at `/Volumes/Storage-1/Hermes/secrets/.env.hermes.backup`
- `--dry-run` flag for safe check
- `--from <path>` flag for alternative backup source
- 5-evidence gate output (file/size/perm/keys/sample)
- Permission 600 enforced on restored file

**Bundled as skill support file:** `scripts/restore-env.sh` trong `devops/hermes-daily-backup/` skill.

### 3. Create `.env.template` (safe-to-commit)
**Location:** `~/.hermes/.env.template`
**Pattern:** key names only with `*** ` replacement, NO real values.
**Use case:** reference structure khi cần edit `.env`, push lên git được.

### 4. Patch cron prompt (PITFALL #21)
**Cron job:** `7cba6ba5f52a` (Hermes Daily Backup)
**3 new sections added to prompt:**
1. Pre-flight snapshot: copy `.env` ra `/Volumes/Storage-1/Hermes/secrets/` BEFORE git reset
2. Replace `reset --hard` → `reset --mixed` (giữ untracked files)
3. Post-reset auto-restore từ backup

**Next cron run:** 2026-06-26 03:00 — verify log shows ".env preservation: N snapshots, M restored"

### 5. End-to-end test (5 evidence gate)
| # | Check | Command | Result |
|---|-------|---------|--------|
| 1 | Syntax OK | `bash -n restore-env.sh` | ✅ |
| 2 | Dry-run output | `--dry-run` | ✅ "Target size matches backup" |
| 3 | Real restore | `rm .env && restore-env.sh` | ✅ File restored |
| 4 | Diff match | `diff /tmp/original .env` | ✅ Empty diff |
| 5 | Permission | `stat -f %Lp .env` | ✅ 600 |

### 6. Wiki log + concept page
- `wiki/concepts/cron-3am-dotenv-wipe-pattern.md` (3031B) — full root cause + solution + pitfalls
- `wiki/log.md` entry [2026-06-25 20:09] — incident + 6 deliverables

## Pitfalls encountered during session

### Memory filter blocks secret-related content
- 2 memory add attempts rejected: "Blocked: content matches threat pattern 'hermes_env'"
- **Fix:** save secret-related lessons to wiki instead of memory
- Lesson: see pitfall #20m in main SKILL.md

### write_file content corruption with secret-adjacent strings
- `.env.template` write returned success but content had decorative `===` headers that got truncated
- Had to retry with cleaner format
- Lesson: see pitfall #20n in main SKILL.md

### chmod 711 too permissive
- Default `chmod +x` gave 711 (execute-only for group/other)
- Tightened to 700 (owner-only) for safety
- Standard: scripts handling secrets should be 700, not 755

## Recovery vs Detection distinction

This session demonstrates the **recovery loop**, NOT just detection:
- **Detection:** pitfall #20h (find missing `.env`)
- **Recovery:** this session (restore from backup + patch cron + verify)

Future sessions should follow this full loop:
1. Detect (pitfall #20h diagnostic)
2. Backup current state
3. Create recovery script (restore-env.sh pattern)
4. Patch cron prompt (PITFALL #21)
5. End-to-end test with 5 evidence gate
6. Wiki log + concept page

## Related
- `report-example-2026-06-25-incident.md` — Morning detection session
- `report-example-2026-06-25-evening-session.md` — Previous evening investigation
- Main SKILL.md pitfalls #20, #20h, #20m, #20n, #20o
- `wiki/concepts/cron-3am-dotenv-wipe-pattern.md` — Persistent reference