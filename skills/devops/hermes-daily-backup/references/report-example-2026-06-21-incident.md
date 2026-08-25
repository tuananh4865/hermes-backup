# Session Note — 2026-06-21 (.env deletion incident & Telegram bot silent)

## What happened (user-visible)
- Telegram bot `@ClawdZ1E_Bot` (ID 8344881558) silently stopped responding.
- Gateway log showed: `WARNING gateway.run: No messaging platforms enabled.` + `[Telegram] Connect attempt 1/3 failed: Timed out` (a stale warning from the previous failure mode — not the current cause).
- User reported: "kiểm tra telegram bot token xem tại sao anh nhắn cho bot không được!"

## Root cause (5-step trace)
1. `~/.hermes/.env` did not exist. `ls ~/.hermes/.env*` returned nothing.
2. `~/.hermes/.env` had been written at 11:47 on 2026-06-18 (after the previous day's setup) with 18 lines including `TELEGRAM_BOT_TOKEN=***...M1rs`.
3. The 3AM cron job `Hermes Daily Backup` (job hash `7cba6ba5f52a`) ran at 03:01:54 on 2026-06-18 and produced commit `9275474432f2e8596c94a7e41a999b6291cf62ac`:
   - Title: "Backup hermes incremental: 2026-06-18 03:00 (untrack .env secrets + content updates)"
   - Diff: `diff --git a/.env b/.env / deleted file mode 100644` (the file went away from the working tree, not just untracked)
   - `.gitignore` got 9 new lines (`.env`, `.env.*`, `**/.env`, `**/.env.*`, `*.pem`, `*.key`, `secrets/`)
4. After 2026-06-18 the `~/.hermes/.env` file never came back, because the cron script that did the untrack did NOT run the `test -f ~/.hermes/.env` sanity check from pitfall #10.
5. User noticed on 2026-06-21 morning; the diagnosis chain was: gateway says "No messaging platforms enabled" → `~/.hermes/.env` missing → git log shows commit 927547443 deleted it → token was the same one user had on hand (8344881558:***...M1rs) → token was re-written to `~/.hermes/.env` (chmod 600) → gateway restarted → Telegram adapter connected → 30 commands registered → `@ClawdZ1E_Bot` polling.

## What worked
- `git log --all --diff-filter=D --name-only -- .env` immediately pointed at commit `927547443` (the offendor).
- `git show 927547443^:.env` showed the full content (18 lines, all 5 needed env vars).
- User still had the original token in chat history, so re-issuing the .env took < 2 minutes instead of a BotFather trip.

## What did NOT work / time-sinks
- The first instinct was to look at "Telegram connection failed" warnings in the log, but those were stale from 3 days prior. The real signal was the quieter `No messaging platforms enabled` line buried in the rolling log.
- Searching shell history (`grep -E "rm |\.env" ~/.zsh_history`) for who deleted the file was a dead end — turns out it was a cron job, not a human. Future debug: when a file "mysteriously" disappears, check `git log --diff-filter=D -- <path>` BEFORE checking shell history.
- `disk-cleanup` plugin was initially suspected (it has a `_SECRET_FILE_NAMES` whitelist) but `disk_cleanup.py:559` explicitly SKIPS `.env` — it was a red herring.

## Fix shipped this session
- Re-created `~/.hermes/.env` (chmod 600) with token `8344881558:***...M1rs` and full TELEGRAM_*_USERS allowlist.
- Verified token via `curl https://api.telegram.org/bot<token>/getMe` → returns the expected bot info.
- Killed old gateway PID 44698 (and the auto-restart child 45038, 45356), let the supervisor respawn it.
- Confirmed `logs/gateway.log` shows `[Telegram] Connected to Telegram (polling mode)` + `set_my_commands OK` + `Sent post-update notification to telegram:-1003764041476 (exit=0)`.

## Skill update delivered
- New pitfall #20 in `hermes-daily-backup` SKILL.md documenting the 2-step pattern: (1) `cp` `.env` to `/tmp` BEFORE untracking, (2) `test -f ~/.hermes/.env && [ -s ~/.hermes/.env ]` AFTER the untrack command, BEFORE the commit. Failure path: restore from `/tmp` and `exit 1`.
- New `Verification` step #4 in SKILL.md: every backup run should assert `.env` exists and is non-empty AFTER the secret-scan step. If the file is gone, the backup is a no-op FAIL even if the push succeeds.

## Open follow-up (not done this session)
- Setup auto-backup of `~/.hermes/.env` encrypted to `/Volumes/Storage-1/Hermes/backups/env-encrypted/` via 2AM cron, separate from the git backup. So even if a future cron bug deletes the file, the encrypted copy is recoverable without needing to dig through git history. Suggested key: machine UUID + user passphrase.
- Daily 7AM cron that checks `test -f ~/.hermes/.env && [ -s ~/.hermes/.env ]` and Telegrams the user a warning if missing, BEFORE the user notices.
- Audit `git log --all --diff-filter=D --name-only` in `~/.hermes` for OTHER files that may have been deleted from the working tree by the same cron step (cron/output/ and other tracked paths). Anything still missing should be restored from the matching commit.

## Lessons that belong in OTHER skills
- **`telegram-bot-debug` / gateway troubleshooting**: when a bot is "silent", the FIRST diagnostic step is `test -f ~/.hermes/.env && echo OK || echo MISSING` + `tail -50 ~/.hermes/logs/gateway.log | grep -E "messaging platforms enabled|telegram adapter"`. The 30-second check beats 5 minutes of chasing connection warnings.
- **`cron-script-debug`**: when a file goes missing without an obvious human action, immediately check `git log --diff-filter=D -- <path>` — 3-second query, often nails the cause.
- **Universal rule for any "untrack / disable / remove X" step in an automation script**: pair it with a `test -f` / `test -e` assertion AFTER the destructive command. The "before" assertion (`test -e` before delete) is a check; the "after" assertion is the safety net.
