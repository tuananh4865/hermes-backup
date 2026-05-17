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
          "requireMention": false
        }
      }
    }
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

## Known Issues & Pitfalls

### "Requested agent harness 'codex' is not registered"
**Symptom**: Bot shows ⚠️ "Something went wrong while processing your request"
**Cause**: Config has no explicit model/harness, so OpenClaw defaults to "codex" harness (OpenAI Codex CLI) which is not registered locally
**Fix**: The issue is in the session runtime — restart the gateway to clear stale sessions. If it persists, explicitly set the default model in config:
```bash
cd ~/.openclaw
npx openclaw config set agent.defaultModel "openai/gpt-5.5"
openclaw gateway restart
```

### Gateway crashes immediately
**Cause**: Invalid config (missing `gateway.mode` field)
**Fix**: Add `"gateway.mode": "local"` to openclaw.json

### Gateway token unauthorized
**Cause**: Device identity not configured
**Fix**: Run `openclaw gateway probe` or access dashboard to authenticate
**Note**: Telegram bot still works even if gateway shows "unreachable"

### "Secret provider 'minimax' is not configured"
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