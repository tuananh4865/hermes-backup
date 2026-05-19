# OpenClaw Token Revocation — 401 Crash Loop

**Date:** 2026-05-19  
**Severity:** CRITICAL — bot completely down  
**Symptom:** ~440 crash/restart cycles in hours

## Root Cause

Bot token revoked by Telegram OR token set to empty string in config.

## Symptom Progression

1. `deleteWebhook` → 401 Unauthorized
2. `setMyCommands` → 401 Unauthorized
3. `[default] channel exited` → crash
4. Auto-restart attempt 1/10, 2/10... → loops infinitely
5. JSON log at `/tmp/openclaw/openclaw-YYYY-MM-DD.log` floods with:
   ```
   "spooled update N handler failed; keeping for retry: Bot not initialized!"
   "telegram deleteWebhook failed: Call to 'deleteWebhook' failed! (404: Not Found)"
   "telegram deleteMyCommands failed: Call to 'setMyCommands' failed! (404: Not Found)"
   ```

## Health Check Misleading

```bash
curl -s https://api.telegram.org/bot<TOKEN>/getMe
# Returns: {"ok":false,"error_code":401,"description":"Unauthorized"}
```

But gateway `/health` still returns `{"ok":true,"status":"live"}` — gateway process alive but Telegram auth dead.

## Diagnosis

```python
# Extract token from config
python3 -c "
import json
d=json.load(open('/Users/tuananh4865/.openclaw/openclaw.json'))
print(d['channels']['telegram']['botToken'])
"

# Test token
curl -s https://api.telegram.org/bot<TOKEN>/getMe
# {"ok":false,"error_code":401,"description":"Unauthorized"} = revoked
# {"ok":true,"username":"BotName"} = valid
```

## Fix

1. Get new token from **@BotFather** on Telegram
2. Update `~/.openclaw/openclaw.json` → `channels.telegram.botToken`
3. Restart gateway: `cd ~/.openclaw && npx openclaw gateway restart`

## Prevention

Add token validation to startup health check:
```bash
# Before starting gateway, verify token is valid
TOKEN=$(python3 -c "import json; d=json.load(open('/Users/tuananh4865/.openclaw/openclaw.json')); print(d['channels']['telegram']['botToken'])")
curl -s "https://api.telegram.org/bot${TOKEN}/getMe" | grep '"ok":true' || echo "TOKEN_INVALID"
```

## Related

- `openclaw-deep-research` skill — OpenClaw Telegram bot setup
- `references/telegram-network-outage-2026-05-19.md` — Telegram connectivity patterns