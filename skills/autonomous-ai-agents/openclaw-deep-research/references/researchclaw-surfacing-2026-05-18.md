# ResearchClaw Surfacing Session — 2026-05-18

ResearchClaw (ClawdBotZ1 / @ClawdZ1E_Bot, user 8344881558) was surfacing in the O-Lab Engineering topic with tools like `grep -r "platform_allow_bots_map"` and checking for `config.yaml`.

## What ResearchClaw Was Looking For
ResearchClaw was trying to find bot-allowance config:
```
grep -r "platform_allow_bots_map\|allow_bots\|TELEGRAM_ALLOW_BOTS" ~/.openclaw/
grep -n "is_bot\|is_bot_message\|bot_channel" ~/.hermes/
```

## What the REAL Issue Was
`requireMention: false` in `~/.openclaw/openclaw.json` — simple config flag, no code search needed.

## Key Insight
ResearchClaw kept searching for complex explanations (`platform_allow_bots_map`, Hermes blocking bot messages, `TELEGRAM_ALLOW_BOTS` env var) when the fix was a one-line config change.

## Config File Location
OpenClaw uses `~/.openclaw/openclaw.json` — NOT `.yaml`. No `config.yaml` exists in OpenClaw.

## Git Status (2026-05-18 16:25)
```
5790ff9 [auto] session state sync 2026-05-18 16:18  ← last push
89a193a [fix] cron_daily_ingest.py: append_text → write_text for Python 3.14
e82432b fix: normalize / to - in wikilink path separator
```
42 untracked files (concept stubs + raw-transcripts) pending.

## Bot IDs in O-Lab Group
- ResearchClaw: `@ClawdZ1E_Bot`, user ID `8344881558`, is_bot=true
- Hermes: user ID `1132914873`, is_bot=false (Tuấn Anh's own account)
- Group: O-Lab, ID `-1003764041476`, forum topic `Engineering` thread `603`
