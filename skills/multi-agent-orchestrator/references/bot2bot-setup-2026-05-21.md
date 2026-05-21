# Telegram Bot-to-Bot @mention Setup (2026-05-21)

## Problem
Researcher bot (@ClawdZ1E_Bot) @mentions Hermes but Hermes doesn't see it.

## Root Cause — GROUP ID FORMAT

**Wrong**: `-1005195161709` (assumed supergroup format)
**Correct**: `-5195161709` (actual numeric ID without 100 prefix)

Telegram API accepts the raw numeric ID. The `getChat` call reveals the actual group ID.

## Verification Steps

```bash
BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2)

# Test with -100 prefix → "Bad Request: chat not found"
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getChat?chat_id=-1005195161709"
# Result: {"ok":false,"error_code":400,"description":"Bad Request: chat not found"}

# Test without 100 prefix → WORKS
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getChat?chat_id=-5195161709"
# Result: {"ok":true,"id":-5195161709,"title":"Company","type":"group",...}
```

## Working Test (May 21)

```bash
BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=-5195161709" \
  -d "text=@ClawdZ1E_Bot check skill: openclaw-agent-profiles"
# Result: ✅ {"ok":true,"result":{"message_id":56163,...}}

# @mention entity confirmed in response:
# "entities":[{"offset":0,"length":13,"type":"mention"}]
```

## What Was NOT the Fix

- `TELEGRAM_ALLOW_BOTS=all` was already set — did NOT help
- Privacy mode already disabled — did NOT help
- The issue was purely the group ID format (100 prefix)

## Related
- `references/telegram-bot-privacy-setup.md`
- `references/telegram-bot-mention-delegation.md`