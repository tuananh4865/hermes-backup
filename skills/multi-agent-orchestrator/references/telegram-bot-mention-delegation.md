# Telegram Bot Mention Delegation

## Context Discovery (2026-05-21)

Tuấn Anh said Telegram already supports bot-to-bot communication. This reference documents the discovery and implementation.

## Bot-to-Bot Architecture

```
User (Tuấn Anh)
    │
    ▼ @mention in group
@Researcher_Clawd_Bot ←── receives notification (Telegram forwards to this bot)
    │                   (Even when message comes from another bot)
    ▼ @mention in group
@HermesMainBot ←── receives notification
```

**Telegram DOES forward bot mentions** — even from other bots. The earlier belief that "bots cannot see bot messages" was incorrect for @mention cases.

## Configuration for Bot-to-Bot

### Hermes (main bot)
```yaml
# ~/.hermes/config.yaml
telegram:
  require_mention: true      # Must be @mentioned
  allowed_users: '*'          # Accept from all users AND bots
```

### .env
```bash
# ~/.hermes/.env
TELEGRAM_ALLOW_BOTS=all       # Critical: allow bot-to-bot messages
```

### OpenClaw (Researcher bot)
```json
// ~/.openclaw/openclaw.json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "8706108095:***",
      "dmPolicy": "open",
      "allowFrom": ["*"],
      "groupPolicy": "open",
      "groups": {
        "*": {
          "requireMention": true
        }
      }
    }
  },
  "commands": {
    "ownerAllowFrom": [
      "telegram:*"           // ← Changed from just Tuấn Anh's ID
    ]
  }
}
```

## Workflow: @mention to Delegate

```bash
# In group Company (-5195161709)
send_message(
  action=send,
  message="@Researcher_Clawd_Bot Research about agentic AI...",
  target="telegram:Company"
)

# Researcher bot receives the message via Telegram
# (Telegram forwards @mention regardless of sender being bot or human)
```

## Key Learning

**Earlier misconception**: "Bots cannot see messages directed at other bots"

**Correct understanding**: Telegram Bot API allows bots to receive @mentions directed at them. The key is:
1. Bot must be @mentioned (not just "saw a message")
2. Privacy mode must be disabled OR bot must be admin
3. `TELEGRAM_ALLOW_BOTS=all` in .env for Hermes to accept

**What STILL doesn't work**: Bots cannot see ALL messages in a group (only those where they're @mentioned or reply-targeted)

## Verification Test (2026-05-21)

```bash
# Test: Hermes @mention Researcher in group Company
# If Researcher responds → bot-to-bot mention works ✅
# If no response → check privacy mode + allow_bots config ❌
```

## Privacy Mode Fix

If bot cannot see messages even with @mention:
1. @BotFather → /mybots → Select bot → /setprivacy → **Disable**
2. Or ensure bot has admin role in the group