# OpenClaw + Telegram Bot-to-Bot Reference

## Telegram Group ID Format — CRITICAL DISCOVERY

**Wrong format (fails):** `-1005195161709`
**Correct format (works):** `-5195161709`

The `-100` prefix is the supergroup/channel indicator in Telegram's Bot API, but OpenClaw routing uses the raw ID without the prefix.

### How to Verify
```bash
# Get bot info first - confirms which bot token is active
BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN ~/.hermes/.env | cut -d= -f2)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe"

# Test group access - use raw ID (no -100 prefix)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=-5195161709" \
  -d "text=@ClawdZ1E_Bot test mention"
```

### Why This Matters
- Telegram returns `-100<chat_id>` when you getChat with a supergroup ID via API
- But the actual numeric ID for routing/bindings is just the last digits
- "Bad Request: chat not found" = bot not in group OR wrong ID format

---

## Adding New Agent to OpenClaw Config

### Config Location
`~/.openclaw/openclaw.json`

### Structure for `agents.list`
```json
{
  "id": "techlead",
  "name": "TechLead",
  "workspace": "~/.openclaw/workspace-techlead",
  "identity": {
    "name": "TechLead",
    "emoji": "👨‍💻",
    "theme": "senior engineer, architecture expert"
  },
  "groupChat": {
    "mentionPatterns": ["@techlead", "techlead"]
  },
  "tools": {
    "profile": "full",
    "allow": ["read", "write", "exec", "process", "apply_patch", "edit", "browser", "gateway", "cron"],
    "deny": []
  },
  "skills": ["code-review-and-quality", "engineering-tdd", "planning-and-task-breakdown"]
}
```

### Structure for `bindings`
```json
{
  "agentId": "techlead",
  "match": {
    "channel": "telegram",
    "peer": {
      "kind": "dm"  // or "group" with "id": "-5195161709"
    }
  }
}
```

### Create Workspace
```bash
mkdir -p ~/.openclaw/workspace-<agent-id>
mkdir -p ~/.openclaw/agents/<agent-id>/agent
mkdir -p ~/.openclaw/agents/<agent-id>/sessions
```

---

## OpenClaw Bot Token

Current setup uses @ClawdZ1E_Bot token (not Hermes bot).
- Bot name: ClawdBotZ1
- Bot username: @ClawdZ1E_Bot
- Token: stored in `~/.hermes/.env` as `TELEGRAM_BOT_TOKEN`

---

## ownerAllowFrom Format

```json
"commands": {
  "ownerAllowFrom": ["telegram:1132914873", "telegram:<bot-id>"]
}
```

Format: `telegram:<user_id>` or `telegram:<bot_id>`

---

## OpenClaw Process Management

OpenClaw runs via npx (not installed globally):
```
/opt/homebrew/bin/node /Users/tuananh4865/.npm/_npx/8718c3904bb5fece/node_modules/openclaw/dist/index.js gateway --port 18789
```

Restart via `/restart` command to @ClawdZ1E_Bot bot.