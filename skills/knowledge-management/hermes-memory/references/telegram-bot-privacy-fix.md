# Telegram Bot Privacy — Hermes Read Access

## Problem
Hermes Agent (primary Telegram bot) could not see messages from other bots (e.g. @Researcher_Clawd_Bot) in the O-Lab group, even though it was receiving and replying to human messages.

## Root Cause
**Telegram Bot Privacy Mode** (default for all Telegram bots). When enabled, bots can ONLY read:
- Messages that @mention them
- Messages that reply directly to them
- DMs to the bot

 Bots CANNOT read messages from other bots in groups.

## Solution
The OTHER bot (@Researcher_Clawd_Bot) needs to disable privacy mode via @BotFather:

1. Open Telegram → Chat with **@BotFather**
2. Send: `/setprivacy`
3. Select: `@Researcher_Clawd_Bot`
4. Choose: **"Disable"** (change from default "Restrict")

After this, @Researcher_Clawd_Bot can read ALL messages in the group (including messages from other bots).

## Verification
After disable, Hermes can read messages from @Researcher_Clawd_Bot in the O-Lab group. Messages appear garbled/truncated (workflow format) but they ARE visible to Hermes.

## Key Config (Hermes side)
```yaml
# ~/.hermes/config.yaml
telegram:
  allowed_users: '*'
  require_mention: false
  allowed_chats: ''
```

This confirms Hermes has no restrictions — it was purely the sender bot's privacy setting.

## OpenClaw Gateway Note
OpenClaw uses a DIFFERENT gateway (`~/.openclaw/`). Its bot (@Researcher_Clawd_Bot) is separate from Hermes Agent. Both can coexist in the same group, but they are independent systems.

Restart OpenClaw if stalled sessions occur:
```bash
npx openclaw gateway restart
```