---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 telegram (extracted)
  - 🔗 discord (extracted)
  - 🔗 messaging (extracted)
  - 🔗 webhooks (inferred)
last_updated: 2026-04-11
tags:
  - messaging
  - gateway
  - integration
  - automation
---

# Gateway

> The messaging gateway connects Hermes to various communication platforms (Telegram, Discord, Slack, etc.).

## Overview

The Gateway is Hermes's system for receiving messages from and sending messages to various chat platforms. It provides:
- **Unified interface**: Same agent works across all platforms
- **Platform adaptation**: Translates between platform-specific formats
- **Session management**: Persistent conversations per user
- **Slash commands**: Platform-agnostic command handling

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PLATFORMS                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │Telegram│  │ Discord │  │ Slack  │  │ Signal │       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
│       │            │            │            │             │
│       └────────────┴────────────┴────────────┘             │
│                         │                                   │
│                         ▼                                   │
│              ┌────────────────────┐                        │
│              │   GATEWAY LAYER   │                        │
│              │ - Session mgmt    │                        │
│              │ - Command routing │                        │
│              │ - Message dispatch │                        │
│              └─────────┬──────────┘                        │
│                        │                                    │
│                        ▼                                    │
│              ┌────────────────────┐                        │
│              │    HERMES AGENT   │                        │
│              └────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Supported Platforms

| Platform | Status | Features |
|----------|--------|----------|
| **Telegram** | ✅ Production | DM, groups, bots |
| **Discord** | ✅ Production | Servers, channels, webhooks |
| **Slack** | ✅ Production | Workspaces, threads |
| **WhatsApp** | 🔄 Beta | Via Twilio |
| **Signal** | 🔄 Beta | E2E encrypted |
| **Email** | 🔄 Beta | SMTP/IMAP |

## Message Flow

### Incoming Message
```
1. Platform receives message (Telegram bot receives update)
2. Gateway extracts: chat_id, user_id, text, attachments
3. Gateway creates/retrieves session
4. Session routes to agent
5. Agent processes and responds
6. Gateway formats response for platform
7. Gateway sends via platform API
```

### Outgoing Message
```python
# Gateway formats message per platform
async def send_message(platform: str, chat_id: str, text: str):
    if platform == "telegram":
        await telegram.send_message(chat_id, text)
    elif platform == "discord":
        await discord.send_message(chat_id, text)
    # ...
```

## Session Management

Each user gets a persistent session:
```python
class Session:
    user_id: str
    platform: str
    conversation_history: list[Message]
    created_at: datetime
    last_active: datetime
    metadata: dict  # Platform-specific data
```

### Session Storage
- **SQLite** (default): Simple, local
- **PostgreSQL**: Production, scalable
- **Redis**: Fast, for high-traffic

## Slash Commands

Commands work across all platforms:
```
/help          — Show commands
/search       — Search wiki
/todo         — Manage tasks
/model        — Switch model
/skin         — Change theme
```

### Command Registration
```python
COMMAND_REGISTRY = [
    CommandDef("help", "Show help", ...),
    CommandDef("search", "Search the wiki", ...),
    # Platform-specific commands also registered
]
```

## Platform Adapters

Each platform has its own adapter:
```
gateway/
└── platforms/
    ├── telegram.py      # Telegram bot API
    ├── discord.py       # Discord bot API
    ├── slack.py         # Slack API
    └── ...
```

### Adapter Interface
```python
class PlatformAdapter:
    async def connect(self): ...
    async def disconnect(self): ...
    async def send_message(self, chat_id: str, text: str): ...
    async def send_file(self, chat_id: str, file_path: str): ...
    async def send_image(self, chat_id: str, image_url: str): ...
```

## Webhook Integration

For platforms that use webhooks:

```python
# Telegram webhook
@app.post("/webhook/telegram")
async def telegram_webhook(update: TelegramUpdate):
    await gateway.process_update(update)
    return {"ok": True}

# Discord webhook
@app.post("/webhook/discord")
async def discord_webhook(payload: DiscordPayload):
    await gateway.process_message(payload)
    return {"ok": True}
```

## Gateway Configuration

### config.yaml
```yaml
gateway:
  session_db: ~/.hermes/sessions.db
  platforms:
    telegram:
      enabled: true
      bot_token: ${TELEGRAM_BOT_TOKEN}
    discord:
      enabled: true
      bot_token: ${DISCORD_BOT_TOKEN}
```

## Home Channels

Set default delivery target:
```yaml
home_channels:
  telegram: home  # Your personal DM
  discord: "#notifications"  # Discord channel
```

## Rate Limiting

Each platform has different limits:
- **Telegram**: 30 msg/sec, 20 msg/min to same chat
- **Discord**: Varies by tier
- **Slack**: Varies by plan

Gateway queues messages and respects limits.

## Related Concepts

- [[telegram]] — Telegram bot setup
- [[discord]] — Discord integration
- [[messaging]] — Messaging patterns
- [[webhooks]] — Webhook configuration

## External Resources

- [Telegram Bot API](https://core.telegram.org/bots)
- [Discord Developer Portal](https://discord.com/developers)
- [Slack API](https://api.slack.com/)