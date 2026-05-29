# Telegram Group Bot "no-mention" Skip Pattern

## The Symptom

Bot is running and receiving messages (visible in logs as `Inbound message... -> @Researcher_Clawd_Bot`) but repeatedly logs show:

```
{"reason":"no-mention"} "skipping group media before download"
```

The bot appears silent in the group — it never replies.

## Root Cause

OpenClaw's `telegram-auto-reply` module has a `requireMention` check. In group chats, if the bot is **not @mentioned** in the message, it silently skips processing.

This is **intentional behavior**, not a crash or error.

## Log Evidence

```
# Bot receives message but skips it:
Inbound message telegram:group:-1003764041476:topic:4081 -> @Researcher_Clawd_Bot (group, 30 chars)
{"chatId":-1003764041476,"reason":"no-mention"} skipping group media before download

# Bot is alive and polling:
[telegram] [diag] isolated polling ingress started spool=...
```

## Verification Steps

```bash
# 1. Check if bot process is running
ps aux | grep -E "(openclaw|ResearchClaw)" | grep -v grep

# 2. Check recent logs for inbound messages
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -E "(Inbound|no-mention)"

# 3. Verify bot token is valid
curl -s "https://api.telegram.org/bot<TOKEN>/getMe" | jq
```

## Fix Options

### Option A: User Must @mention the Bot (Default Behavior)
In group chats, users must explicitly @mention the bot for it to respond:
```
@Researcher_Clawd_Bot [message]
```

### Option B: Disable requireMention in Config
In `~/.openclaw/openclaw.json`, under the Telegram channel config:

```json
{
  "channels": {
    "telegram": {
      "requireMention": false
    }
  }
}
```

Then restart the gateway.

### Option C: Check OpenClaw Config for Group Settings
```bash
cat ~/.openclaw/openclaw.json | jq '.channels.telegram'
```

## Key Distinction

| Scenario | Expected Behavior |
|----------|-------------------|
| DM to bot | Always responds (no mention needed) |
| Group + @mention | Responds |
| Group, no mention | **Silently skips** (logs `no-mention`) |

This is NOT a bug — it's a privacy/antispam feature. The bot ignoring messages without mention prevents it from responding to every conversation in a large group.

## Related

- OpenClaw Telegram channel config: `~/.openclaw/openclaw.json`
- Log location: `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- Gateway restart: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`