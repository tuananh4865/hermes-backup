# Telegram Bot-to-Bot Communication — Updated 2026-05-21

## CRITICAL: Telegram Group ID Format

**Wrong:** `-1005195161709` (with -100 prefix)
**Correct:** `-5195161709` (raw ID)

### Why This Matters
- Telegram returns `-100<chat_id>` via `getChat` API response
- But routing/bindings and curl API calls use raw numeric ID
- "Bad Request: chat not found" = bot not in group OR wrong ID format

### Verified Working (2026-05-21)
```bash
BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=-5195161709" \
  -d "text=@ClawdZ1E_Bot check skill: openclaw-agent-profiles"
```

Result: Message delivered successfully to Company group with bot mention.

### Company Group Info
- **Group Name:** Company
- **Raw ID:** `-5195161709`
- **Bots in group:** @ClawdZ1E_Bot (ResearchClaw), @Hermes_Agent_Pro (Hermes)

### Bot-to-Bot @mention Works When
1. Both bots are members of the group
2. Group has no restrictions blocking bot messages
3. Using correct raw group ID (no -100 prefix)
4. Bot @mention format: `@username` in message text

### Previous Error Analysis
Initial attempts used `-1005195161709` → "Bad Request: chat not found"
Switched to `-5195161709` → Success

Also discovered: Hermes and ResearchClaw use SAME bot token (@ClawdZ1E_Bot) - not separate tokens. This is Hermes agent's config using OpenClaw's bot.