# Multi-Agent Setup with Telegram (Agentic Company)

## Overview
Hermes supports creating multiple independent agents, each with:
- Isolated profile (config, sessions, skills, memory)
- Own Telegram bot token for DM capability
- Custom SOUL.md defining role
- Domain-specific knowledge base

## Architecture Pattern
```
Tuấn Anh (CEO - human)
├── @SaturdayClawdBot (Content Director) ← test agent
├── @ResearchLeadBot (future)
├── @SecurityEngineerBot (future)
└── ... more agents
```

## Setup Steps

### Step 1: Create Telegram Bot
1. Message @BotFather on Telegram
2. `/newbot` → name → username
3. Copy token (format: `123456:ABC-DEF...`)

### Step 2: Create Hermes Profile
```bash
hermes profile create <name> --clone-from default
# Example: hermes profile create content-director
```

### Step 3: Configure Token
```bash
# Edit profile .env
nano ~/.hermes/profiles/<name>/.env

# Add/modify:
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_ALLOWED_USERS=1132914873  # Tuấn Anh's Telegram ID
TELEGRAM_HOME_CHANNEL=1132914873
HERMES_YOLO_MODE=true
```

### Step 4: Define Role (SOUL.md)
Edit `~/.hermes/profiles/<name>/SOUL.md`:
```markdown
# <Role Name> Agent — SOUL.md

You are **<Role Name>**, the <expertise> expert for Tuấn Anh's agentic company.

## IDENTITY
- **Role**: <Role description>
- **Reports to**: Tuấn Anh (CEO)
- **Collaboration**: Works with <other agents>

## <Domain> EXPERTISE
... domain-specific knowledge ...
```

### Step 5: Start Gateway
```bash
hermes gateway --profile <name> start
# Or with explicit token:
TELEGRAM_BOT_TOKEN=xxx hermes gateway --profile <name> start
```

### Step 6: Verify
```bash
# Check status
hermes gateway --profile <name> status

# Check logs
tail ~/.hermes/profiles/<name>/logs/gateway.log

# Look for: ✓ telegram connected
```

## Tuấn Anh's Agents

| Agent | Profile | Bot | Status |
|-------|---------|-----|--------|
| Content Director | content-director | @SaturdayClawdBot | ✅ Online |

## Tuấn Anh's Agentic Company Structure (2026-05-04)
- CEO: Tuấn Anh (human)
- Executive: Research Lead, Content Director, Engineering Lead
- Q&A: Security Engineer, Code Reviewer, Refactor Specialist, QA Agent
- Ops: Operations Manager, Autoresearch Agent

## Useful Commands
```bash
# List all profiles
hermes profile list

# Show profile details
hermes profile show <name>

# Start/stop gateway
hermes gateway --profile <name> start/stop/restart

# Check gateway status
hermes gateway --profile <name> status

# View logs
tail -f ~/.hermes/profiles/<name>/logs/gateway.log
tail -f ~/.hermes/profiles/<name>/logs/gateway.error.log
```

## Notes
- Profile path: `~/.hermes/profiles/<name>/`
- Profile config: `~/.hermes/profiles/<name>/config.yaml`
- Profile .env: `~/.hermes/profiles/<name>/.env`
- Profile SOUL.md: `~/.hermes/profiles/<name>/SOUL.md`
- Gateway logs: `~/.hermes/profiles/<name>/logs/gateway.log`
