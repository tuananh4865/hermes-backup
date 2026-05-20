---
title: OpenClaw Deep Research Agent
name: openclaw-deep-research
created: 2026-05-18
type: skill
tags: [openclaw, telegram, deep-research, agentic]
description: Setup OpenClaw as a deep researcher Telegram bot with personality and skills
trigger: When user wants to setup OpenClaw as a deep researcher Telegram bot
---

# OpenClaw Deep Research Agent

> Setup OpenClaw as a deep researcher Telegram bot with personality and skills

## Architecture

```
OpenClaw (~/.openclaw/)
├── openclaw.json          # Main config
├── workspace/
│   └── SOUL.md           # Agent personality
├── logs/
│   └── gateway.log       # Service logs
└── skills/               # Installed skills

Gateway: ws://127.0.0.1:18789 (local loopback)
Telegram: @Researcher_Clawd_Bot (token: 8706108095:***)
```

## Setup Steps

### 1. Verify Installation
```bash
ls ~/.openclaw/version.txt  # Check installed
openclaw --version          # CLI version
```

### 2. Create Config (~/.openclaw/openclaw.json)
```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "BOT_TOKEN",
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
      "telegram:YOUR_TELEGRAM_USER_ID"
    ]
  },
  "secrets": {
    "providers": {
      "PROVIDER_NAME": {
        "source": "env",
        "allowlist": ["ENV_VAR_NAME"]
      }
    }
  },
  "models": {
    "providers": {
      "PROVIDER_NAME": {
        "baseUrl": "https://api.minimax.io/anthropic",
        "apiKey": {
          "source": "env",
          "provider": "PROVIDER_NAME",
          "id": "ENV_VAR_NAME"
        },
        "models": [
          {
            "id": "MODEL_ID",
            "name": "Model Display Name"
          }
        ]
      }
    }
  }
}
```

> ⚠️ **CRITICAL**: MiniMax baseUrl MUST end with `/anthropic` — the OpenAI-compatible endpoint (`https://api.minimax.io/v1`) returns 404 for all model requests. The plugin hardcodes `MINIMAX_API_BASE_URL = "https://api.minimax.io/anthropic"` internally, but custom providers must also use the Anthropic path.

### 3. Start Gateway
```bash
cd ~/.openclaw
openclaw gateway install    # Install LaunchAgent
openclaw gateway start      # Start service
# Or run directly:
node ... openclaw gateway --port 18789 &
```

### 4. Verify Telegram Bot
```bash
curl -s https://api.telegram.org/bot<TOKEN>/getMe
# Expected: {"ok":true,"username":"BotName"}
```

### 5. Configure Agent Personality
Edit `~/.openclaw/workspace/SOUL.md`:
```markdown
# SOUL.md - Deep Researcher Persona

You are an elite deep research specialist...

## Research Methodology
- Multi-source verification
- Primary sources优先
- Cross-reference claims
...
```

### 6. Check Gateway Status
```bash
cd ~/.openclaw && npx openclaw status
# Gateway should show: running (pid XXXX, state active)
```

### 7. Verify Bot Receives Messages
```bash
tail -50 ~/.openclaw/logs/gateway.log | grep -E "(inbound|outbound|sendMessage)" -i
```

## Config Validation
```bash
cd ~/.openclaw && npx openclaw config validate
```

## Key Commands
```bash
openclaw gateway start      # Start
openclaw gateway stop       # Stop  
openclaw gateway restart    # Restart
openclaw status             # Full status
openclaw skills list        # List skills
npx openclaw status         # Alternative status
```

## Daemon Management Commands
```bash
# Verify LaunchAgent status (macOS)
launchctl print gui/$(id -u) 2>&1 | grep -A3 "ai.openclaw.gateway"
# Expected: pid XXXX (pe) ai.openclaw.gateway — enabled

# Check if daemon is running
ps aux | grep openclaw | grep -v grep

# Full status with npx
cd ~/.openclaw && npx openclaw status
```

## Known Issues & Pitfalls

## Known Issues & Pitfalls

### Telegram "Bot not initialized" retry loop
**Symptom**: JSON log `/tmp/openclaw/openclaw-YYYY-MM-DD.log` floods with:
```
"spooled update N handler failed; keeping for retry: Bot not initialized!
Either call `await bot.init()`, or directly set the `botInfo` option"
```
Gateway.log shows Telegram auto-restarting repeatedly (attempt 1/10, 2/10...).
**Fix**: `cd ~/.openclaw && npx openclaw gateway restart` — clears the stuck Telegram provider session.
**Verification**: After restart, gateway.log should show `starting provider (@BotName)` once, no retry loop.

### ResearchClaw bot responds to ALL messages (no mention required)
**Symptom**: Bot replies to every message in group, not just @mentions — spamming the channel
**Root cause**: `openclaw.json` has `"requireMention": false` under `channels.telegram.groups.*`
**Fix**:
```bash
# 1. Edit config
sed -i '' 's/"requireMention": false/"requireMention": true/' ~/.openclaw/openclaw.json

# 2. Restart gateway
cd ~/.openclaw && npx openclaw gateway restart
```
**Verification**:
```bash
# Confirm the setting is true
grep -A2 '"groups"' ~/.openclaw/openclaw.json
# Should show: "requireMention": true

# Check logs after restart — bot should only show "inbound message" for @mentioned messages
tail -50 ~/.openclaw/logs/gateway.log | grep -i "inbound"
```

### Two log files — different purposes
| File | Purpose | Format |
|------|---------|--------|
| `~/.openclaw/logs/gateway.log` | Human-readable summary | plain text |
| `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Structured JSON details | JSON (use for debugging) |

When troubleshooting Telegram issues: check both. The JSON log has the full error; gateway.log has the readable summary.

### "Requested agent harness 'codex' is not registered"
**Symptom**: Bot shows ⚠️ "Something went wrong while processing your request"
**Cause**: Config has no explicit model/harness, so OpenClaw defaults to "codex" harness (OpenAI Codex CLI) which is not registered locally
**Fix**: The issue is in the session runtime — restart the gateway to clear stale sessions. If it persists, explicitly set the default model in config:
```bash
cd ~/.openclaw
npx openclaw config set agent.defaultModel "openai/gpt-5.5"
openclaw gateway restart
```

### Bot Token Revoked → 401 Crash Loop
**Symptom**: JSON log (`/tmp/openclaw/openclaw-YYYY-MM-DD.log`) floods with:
```
telegram deleteWebhook failed: Call to 'deleteWebhook' failed! (404: Not Found)
telegram deleteMyCommands failed: Call to 'deleteMyCommands' failed! (404: Not Found)
[default] channel exited: Call to 'deleteWebhook' failed! (404: Not Found)
[default] auto-restart attempt N/10 in Xs
```
Health check still returns `{"ok":true,"status":"live"}` — gateway appears fine.
`curl -s https://api.telegram.org/bot<TOKEN>/getMe` returns `{"ok":false,"error_code":401,"description":"Unauthorized"}`.
Restart counter in log reaches 440+ restart attempts in hours.
**Root cause**: Bot token has been revoked or is empty. Telegram API returns 401 for all operations.

**Diagnosis — ALWAYS verify token FIRST before touching config**:
```bash
# Token may appear masked in config output (e.g. "8706108095:***").
# The actual full token IS stored — just use it directly from the config file.
# DO NOT re-extract from display output — the full token works:

# Test token validity
curl -s "https://api.telegram.org/bot8706108095:AAGByOUlkf1_tjmun0bzKoif-K-gsSnyrd0/getMe"
# {"ok":false,"error_code":401,"description":"Unauthorized"} = revoked
# {"ok":true,"username":"BotName","is_bot":true} = valid
```

**Fix — update token + restart**:
```python
# Update token directly in openclaw.json
python3 -c "
import json
cfg = json.load(open('/Users/tuananh4865/.openclaw/openclaw.json'))
cfg['channels']['telegram']['botToken'] = 'NEW_TOKEN_HERE'
json.dump(cfg, open('/Users/tuananh4865/.openclaw/openclaw.json', 'w'), indent=2, ensure_ascii=False)
print('Updated')
"
# Restart gateway
cd ~/.openclaw && npx openclaw gateway restart
# Verify health
sleep 5 && curl -s http://localhost:18789/health
```

**Success verification**: Log should show `starting provider (@BotName)` + `[telegram][diag] isolated polling ingress started` — no more 401/404 errors.

### Gateway crashes immediately
**Cause**: Invalid config (missing `gateway.mode` field)
**Fix**: Add `"gateway.mode": "local"` to openclaw.json

### Config warnings cause gateway degradation
**Symptom**: Gateway starts and responds to health checks (`{"ok":true,"status":"live"}`) but Telegram bot silently fails to reply to @mentions. JSON logs show `"reason":"no-mention"` even when the bot was correctly @mentioned. Config validation shows warnings like `Key 'mcpServers' was ignored — not recognized`.
**Root cause**: `openclaw.json` contains a `mcpServers` section (copy-pasted from template or previous config). OpenClaw does NOT support `mcpServers` as a top-level config key — unrecognized keys produce warnings and cause the config to be partially invalid, which breaks mention detection in Telegram groups.
**Fix**:
```bash
# 1. Remove the mcpServers section from openclaw.json
# Look for and delete the entire "mcpServers" block (starts at line with "mcpServers": {)

# 2. Restart gateway
launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 3. Verify no config warnings
cd ~/.openclaw && npx openclaw config validate

# 4. Test mention in Telegram group
```
**Note**: Even if `npx openclaw config validate` shows warnings, the gateway may still start and show `{"ok":true,"status":"live"}` — the config warnings are subtle and don't block startup entirely, but they break group mention detection. Always check the logs for unrecognized key warnings after modifying config.

### Stalled Session — bot receives but never responds
**Symptom**: JSON log shows `stalled session` entries:
```
15:09:47 stalled session: sessionId=92af056c... sessionKey=agent:main:telegram:group:... topic=4081 state=processing age=13
15:10:17 stalled session age=16s (still stuck)
```
Bot receives messages and starts processing, but hangs forever — never replies.
**Fix**:
```bash
cd ~/.openclaw && npx openclaw gateway restart
```
**Verify**: After restart, JSON log should show `⇄ res ✓` within seconds of inbound messages.

### Gateway Token Missing — Native Approvals Fail
[See references/gateway-token-native-approvals-2026-05-21.md]

### MINIMAX_API_KEY missing — LaunchAgent env var issue
**Symptom**: Gateway fails to start with `SecretProviderResolutionError: Secret provider "minimax" is not configured (ref: env:minimax:MINIMAX_API_KEY)`
**Cause**: The `apiKey: "ref+env:minimax:MINIMAX_API_KEY"` syntax means "use secret provider 'minimax' to look up env var MINIMAX_API_KEY". OpenClaw requires an explicit secret provider with matching name, even when the env var exists.
**Fix**: Add a `secrets.providers.minimax` block to openclaw.json:
```bash
openclaw config set secrets.providers.minimax --json '{"source":"env","allowlist":["MINIMAX_API_KEY"]}'
openclaw gateway restart
```
This adds to config:
```json
"secrets": {
  "providers": {
    "minimax": {
      "source": "env",
      "allowlist": ["MINIMAX_API_KEY"]
    }
  }
}
```
**Verification**: `openclaw secrets audit` should show minimax as REF_RESOLVED (not REF_UNRESOLVED).

### MiniMax baseUrl 404 "model_not_found"
**Symptom**: All model requests fail with `HTTP 404: page not found`, `FailoverError: model_not_found`, `chain_exhausted`
**Cause**: Custom provider baseUrl uses `https://api.minimax.io/v1` (OpenAI path). MiniMax only responds to `https://api.minimax.io/anthropic` (Anthropic-compatible path).
**Fix**: Update the baseUrl in models.providers.minimax to use the `/anthropic` path:
```json
"baseUrl": "https://api.minimax.io/anthropic"
```
**Verification**: `curl -s -X POST "https://api.minimax.io/anthropic/v1/messages" -H "Authorization: Bearer $MINIMAX_API_KEY" -d '{"model":"MiniMax-M2.7","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'` should return a valid response.

### clawhub install fails
**Issue**: "Skill not found or unavailable" — rate limit or wrong slug
**Workaround**: 
- Wait for rate limit reset (~20s)
- Check correct slug via `clawhub search <name>`
- Try different slug formats

### Skills needs setup
**Issue**: Skills show "needs setup" 
**Fix**: Run `openclaw skills install <skill-name>` for each

### Telegram "Bot not initialized" — spam-restart loop
[See references/launchagent-env-var.md]

### MINIMAX_API_KEY missing — LaunchAgent env var issue
**Symptom**: Gateway fails to start with:
```
SecretRefResolutionError: Environment variable "MINIMAX_API_KEY" is missing or empty.
Gateway failed to start: Startup failed: required secrets are unavailable.
```
**Root cause**: `npx openclaw gateway start` on macOS actually triggers a LaunchAgent (`launchd`) service. Launchd services do NOT inherit shell environment variables — they run in an isolated context with only the env vars defined in the plist file.

**Fix**: Add env vars directly to the LaunchAgent plist at `~/Library/LaunchAgents/ai.openclaw.gateway.plist`:
```bash
# 1. Read current plist
cat ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 2. Edit and add EnvironmentVariables dict:
# MINIMAX_API_KEY, TELEGRAM_ALLOW_BOTS, HERMES_YOLO_MODE, etc.

# 3. Reload the service
launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 4. Verify gateway starts
sleep 8 && curl -s http://localhost:18789/health
# Expected: {"ok":true,"status":"live"}
```
**Key insight**: User asked "Sao lại là launch agent? Tại sao không phải là gateway?" — The answer: `openclaw gateway start` on macOS spawns a background launchd service, not a direct process. The gateway process IS running fine — it's the launchd wrapper that doesn't have the env vars.

**⚠️ CRITICAL PITFALL — MINIMAX_API_KEY truncation**:
When reading `~/.hermes/.env` via `grep` or `cat`, the MINIMAX_API_KEY value appears TRUNCATED in terminal output (e.g., `sk-cp-...hU9A` instead of the full 125-char key). Naively copying this output leads to a broken plist with a 13-char key instead of 125.

**Correct approach** — use binary read to extract the actual key:
```python
with open('/Users/tuananh4865/.hermes/.env', 'rb') as f:
    data = f.read()
start = data.find(b'MINIMAX_API_KEY=') + len(b'MINIMAX_API_KEY=')
end = data.find(b'\n', start)
key = data[start:end].decode('utf-8')  # Full 125-char key
```

**Verification**: After writing plist, key length must be 125 chars, not 13. Use:
```bash
grep -a "MINIMAX_API_KEY=" ~/.hermes/.env | wc -c  # Should be ~142 (incl prefix + newline)
```

**Verification**: Check logs at `/tmp/openclaw/openclaw-YYYY-MM-DD.log` for `[SECRETS_RELOADER_DEGRADED]`. After fix, should see `gateway: auto-enabled plugins...` and `starting...` without secrets errors.

## Skills Available (2026.5.12)
20/59 ready including:
- browser-automation (ready)
- clawhub (needs setup)
- coding-agent (needs setup)
- deep-research (may not be available on clawhub)

## Testing
```bash
# Send DM to bot on Telegram
# Check inbound in logs:
tail -f ~/.openclaw/logs/gateway.log | grep telegram

# Check outbound:
tail -50 ~/.openclaw/logs/gateway.log | grep sendMessage
```

## Paths
| Path | Purpose |
|------|---------|
| `~/.openclaw/` | OpenClaw root |
| `~/.openclaw/openclaw.json` | Main config |
| `~/.openclaw/workspace/SOUL.md` | Personality |
| `~/.openclaw/logs/gateway.log` | Gateway logs |
| `~/.openclaw/workspace/skills/` | Installed skills |

## Related
- [[agentic-company-setup]] — Hermes multi-agent setup (different framework)