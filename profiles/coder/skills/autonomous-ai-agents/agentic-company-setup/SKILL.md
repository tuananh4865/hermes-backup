---
title: Agentic Company Setup
name: agentic-company-setup
created: 2026-05-04
type: skill
tags: [hermes, multi-agent, telegram, agentic]
description: Setup multiple Hermes agents as company employees - each with own Telegram bot, profile, role, and inter-agent communication
trigger: When user wants to create/expand agentic company structure
---

# Agentic Company Setup

> Setup multiple Hermes agents as company employees — each with own Telegram bot, profile, role, and inter-agent communication

## Architecture

```
Tuấn Anh (CEO - Human, Telegram: @TyayUno)
│
├── Hermes (Anh's main agent - default profile)
│
└── Company Agents (separate Hermes profiles + Telegram bots)
    ├── Content Director (@SaturdayClawdBot) ← TESTED 2026-05-04
    ├── Research Lead (pending)
    ├── Engineering Lead (pending)
    ├── Security Engineer (pending)
    ├── Code Reviewer (pending)
    ├── Refactor Specialist (pending)
    ├── QA Agent (pending)
    └── Operations Manager (pending)
```

## Core Concept

**Each agent = Hermes Profile + Telegram Bot Token**

| Component | Description |
|-----------|-------------|
| Profile | Isolated config, skills, memory, SOUL.md |
| Bot Token | Telegram bot API token for DM capability |
| Role | Defined in SOUL.md |
| Knowledge | Domain-specific wiki |

## Setup Steps (per agent)

### 1. Create Telegram Bot
```
1. Open @BotFather on Telegram
2. Send /newbot
3. Follow prompts to name bot
4. Copy API token
```

### 2. Create Hermes Profile
```bash
hermes profile create <agent-name> --clone-from default
```

### 3. Configure Bot Token
```bash
# Add to profile's .env
TELEGRAM_BOT_TOKEN=<token>
TELEGRAM_ALLOWED_USERS=<user_id>  # Anh's Telegram ID: 1132914873
```

### 4. Define Role in SOUL.md
```bash
nano ~/.hermes/profiles/<agent-name>/SOUL.md
```

### 5. Start Gateway
```bash
hermes gateway --profile <agent-name> start
```

### 6. Verify
```bash
hermes gateway --profile <agent-name> status
tail ~/.hermes/profiles/<agent-name>/logs/gateway.log
```

## Inter-Agent Communication

**CRITICAL: Telegram bots CANNOT DM each other directly**

Solution: Shared Telegram Group
```
1. Anh creates company group on Telegram
2. Adds all agent bots to group
3. Bots communicate via group messages
4. Use @mention to direct message specific agent
```

## Content Director (Tested 2026-05-04)

| Property | Value |
|----------|-------|
| Bot | @ClawdZ1E_Bot |
| Token | (current session token) |
| Profile | content-director |
| Gateway | Running |
| Status | ✅ Online — bot-to-bot working in thread 603 |

## Research Lead (Tested 2026-05-04)

| Property | Value |
|----------|-------|
| Bot | @Researcher_Clawd_Bot |
| Token | `8706108095:AAGByOUlkf1_tjmun0bzKoif-K-gsSnyrd0` |
| Profile | research-lead (pending setup) |
| Gateway | Starting |
| Status | ✅ Verified 2026-05-04 |

## Inter-Bot Communication (Verified 2026-05-04)

**Bot-to-bot messaging in Telegram supergroup topics WORKS:**
- Use format: `telegram:-1003764041476:603` (NEGATIVE chat ID + thread ID)
- Both bots must be admins in the supergroup
- Both bots must be in the same thread/topic
- @mention between bots WORKS — bot receives it via Telegram Bot API
- Latency: ~39s for bot-to-bot round-trip (2 API calls)

**Setup for new bot:**
1. Create bot via @BotFather → copy token
2. Add bot as admin to O-Lab supergroup
3. Ensure bot is added to `channel_directory.json` (auto-updated by gateway)
4. Use `telegram:-1003764041476:THREAD_ID` as target for send_message

## Role Definitions

### Content Director
- TikTok content strategy
- Script writing
- Trend analysis
- Gen Z slang expertise

### Research Lead (TODO)
- Deep research
- Competitive intel
- Trend monitoring

### Engineering Lead (TODO)
- Code implementation
- Pipeline automation
- Technical architecture

### Security Engineer (TODO)
- Vulnerability scanning
- Security audits
- Threat analysis

### Code Reviewer (TODO)
- PR quality gates
- Code analysis
- Best practices enforcement

### Refactor Specialist (TODO)
- Code quality improvement
- Technical debt reduction
- Pattern optimization

### QA Agent (TODO)
- Testing frameworks
- Error detection
- Quality assurance

### Operations Manager (TODO)
- Task coordination
- Workflow optimization
- Progress tracking

## Known Issues

1. **Telegram bots can't DM each other** - must use shared group
2. **Profile tokens stored in .env** - ensure security
3. **Gateway per profile** - each needs separate process

## Paths

| Path | Purpose |
|------|---------|
| `~/.hermes/profiles/` | All agent profiles |
| `~/.hermes/profiles/<name>/SOUL.md` | Role definition |
| `~/.hermes/profiles/<name>/.env` | Bot token |
| `~/.hermes/profiles/<name>/logs/` | Gateway logs |

## Testing New Agent

```bash
# 1. Check bot is reachable
curl https://api.telegram.org/bot<TOKEN>/getMe

# 2. Start gateway
hermes gateway --profile <name> start

# 3. Check logs
tail -f ~/.hermes/profiles/<name>/logs/gateway.log

# 4. Send test message via BotFather
# Or: DM the bot on Telegram
```
