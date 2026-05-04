# Telegram Bot Privacy Mode Setup (2026-05-04)

## Verified Bot Tokens & Profiles

| Profile | Bot | Token | Status |
|---------|-----|-------|--------|
| default | @TyayUno | main | Primary |
| content-director | @SaturdayClawdBot | `8594106827:AAGu2sUPd-IgPiln7PaRAaSYP7JI-5kxiq4` | ✅ Running |
| research-lead | @Researcher_Clawd_Bot | `8706108095:AAGByOUlkf1_tjmun0bzKoif-K-gsSnyrd0` | ✅ Running |

## Bot Info Check

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getMe"
```

Returns fields:
- `id` - bot numeric ID
- `is_bot` - always true
- `username` - bot handle
- `can_join_groups` - can be added to groups
- `can_read_all_group_messages` - **CRITICAL for bot-to-bot**

## Privacy Mode Fix

When `can_read_all_group_messages: false`:
1. Open @BotFather
2. Send `/mybots`
3. Select bot (e.g., @Researcher_Clawd_Bot)
4. Send `/setprivacy`
5. Select "Disable" 

Or set in .env:
```
TELEGRAM_ALLOWED_USERS=*
```

## Launch Gateway for Profile

```bash
cd ~/.hermes/hermes-agent && ./venv/bin/python -m hermes_cli.main --profile <name> gateway run --replace 2>&1 &
```

## Log Locations

| Profile | Log Path |
|---------|----------|
| content-director | `~/.hermes/profiles/content-director/logs/gateway.log` |
| research-lead | `~/.hermes/profiles/research-lead/logs/gateway.log` |

## Check Running Processes

```bash
ps aux | grep "hermes.*gateway" | grep -v grep
```
