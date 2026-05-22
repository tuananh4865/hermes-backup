# Telegram Bot-to-Bot @mention Setup (2026-05-21)

## Problem
Researcher bot (@ClawdZ1E_Bot) @mentions Hermes but Hermes doesn't see it.

## Root Cause — GROUP ID FORMAT

**Wrong**: `-1005195161709` (assumed supergroup format)
**Correct**: `-5195161709` (actual numeric ID without 100 prefix)

Telegram API accepts the raw numeric ID. The `getChat` call reveals the actual group ID.

## Verified Working (May 21) ✅

**CONFIRMED**: Bot @mention WORKS between bots in Telegram groups. Both bots are now active:

| Agent | Bot Username | OpenClaw Profile | Token |
|-------|--------------|------------------|-------|
| ResearcherClaw | @ClawdZ1E_Bot | researcher | 8706108095:... |
| TechLeadClaw | @TechLead_ClawBot | techlead | (new token added May 21) |

**OpenClaw `ownerAllowFrom` format**:
```
telegram:123456789
```
Where `123456789` is the bot's numeric Telegram ID (not the group ID).

**Important**: @TechLead_ClawBot is a NEW bot separate from @ClawdZ1E_Bot. Each needs its own OpenClaw profile configured with its own bot token.

## OpenClaw Agent Profile Setup (May 21)

1. Create profile in OpenClaw config (`~/.hermes/openclaw/config.yaml`)
2. Add agent with `ownerAllowFrom: telegram:123456789` (bot's numeric ID)
3. Set workspace directory for the agent
4. **Gateway restart needed** after config changes

Example config snippet:
```yaml
agents:
  techlead:
    model: anthropic/claude-sonnet-4
    system: You are TechLead for Tuấn Anh's AI agent company...
    workspace: /Users/tuananh4865/.hermes/openclaw/workspaces/techlead
    ownerAllowFrom:
      - telegram:8344881558  # TechLeadClaw bot numeric ID
```

## Gateway Restart After Config Changes

After modifying OpenClaw config, restart the gateway:
```bash
# Check current status
ps aux | grep hermes | grep -v grep

# Restart if needed
~/.hermes/restart_gateway.sh
```

## Verification Steps

```bash
BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2)

# Test with -100 prefix → "Bad Request: chat not found"
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getChat?chat_id=-1005195161709"

# Test without 100 prefix → WORKS
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getChat?chat_id=-5195161709"

# Send mention to bot in group
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=-5195161709" \
  -d "text=@ClawdZ1E_Bot check skill: openclaw-agent-profiles"
```

## Related
- `references/telegram-bot-privacy-setup.md`
- `references/telegram-bot-mention-delegation.md`