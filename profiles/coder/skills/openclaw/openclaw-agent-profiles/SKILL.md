---
title: openclaw-agent-profiles
name: openclaw-agent-profiles
description: Hướng dẫn Researcher bot cách tự setup thêm agent profiles trong OpenClaw config để có quyền tạo agent mới
trigger: Agent cần tạo thêm agent profiles trong OpenClaw, hoặc cần hiểu cách multi-agent hoạt động
tags: [openclaw, agents, configuration, bot-to-bot]
confidence: high
relationships: [agentic-ai, multi-agent-orchestrator]
---

# OpenClaw Agent Profiles Setup

## Tổng quan

OpenClaw cho phép chạy **multiple isolated agents** — mỗi agent có workspace riêng, session riêng, và có thể route messages đến đúng agent.

**File config chính:** `~/.openclaw/openclaw.json`

---

## Cấu trúc Agent Config

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "anthropic/claude-sonnet-4-6" },
    },
    list: [
      {
        id: "main",           // unique ID
        default: true,        // agent mặc định
        name: "Main Agent",
        workspace: "~/.openclaw/workspace-main",
        agentDir: "~/.openclaw/agents/main/agent",
        skills: ["github", "weather"],
        identity: {
          name: "Clawd",
          emoji: "🦞",
        },
        groupChat: {
          mentionPatterns: ["@openclaw"],
        },
        tools: {
          profile: "full",    // tool access level
          allow: ["read", "write", "exec"],
          deny: ["browser"],
        },
      },
      // Thêm agent mới ở đây
    ],
  },

  // Routing: map channel/account → agent
  bindings: [
    { agentId: "main", match: { channel: "telegram" } },
  ],

  // Bot-to-bot communication
  tools: {
    agentToAgent: {
      enabled: true,
      allow: ["main", "researcher"],  // cho phép các agent này chat với nhau
    },
  },
}
```

---

## Cách thêm Agent mới

### Bước 1: Tạo workspace directory

```bash
mkdir -p ~/.openclaw/workspace-<agent-id>
```

### Bước 2: Thêm vào `agents.list`

```json5
{
  id: "researcher",
  name: "Research Agent",
  workspace: "~/.openclaw/workspace-researcher",
  agentDir: "~/.openclaw/agents/researcher/agent",
  skills: ["web-search", "wikipedia"],
  identity: {
    name: "ResearchClaw",
    emoji: "🔬",
  },
  tools: {
    profile: "coding",
    allow: ["read", "write", "exec", "process"],
    deny: ["gateway", "cron"],
  },
}
```

### Bước 3: Cấu hình routing (bindings)

```json5
bindings: [
  {
    agentId: "researcher",
    match: {
      channel: "telegram",
      peer: { kind: "group", id: "-1005195161709" },  // Company group
    },
  },
]
```

---

## Quyền cần thiết để tạo Agent

### Owner-only commands (cần `commands.ownerAllowFrom`):
- `/config` — đọc/ghi `openclaw.json`
- `/mcp` — quản lý MCP servers
- `/diagnostics` — chẩn đoán system

### Tools cần thiết:
```json
tools: {
  allow: ["read", "write", "edit", "apply_patch", "exec", "process"],
  deny: ["gateway", "cron"],  // hoặc allow tùy nhu cầu
}
```

### Để tạo agent mới, agent cần:
1. **Quyền write** trên config file (`~/.openclaw/openclaw.json`)
2. **Tool `apply_patch`** để edit config
3. **Tool `exec`** để tạo workspace directories

---

## Agent-to-Agent Communication

### Bật tính năng:
```json5
tools: {
  agentToAgent: {
    enabled: true,
    allow: ["main", "researcher", "other-agent"],
  },
}
```

### Gửi message giữa các agents:
Dùng tool `sessions_send` hoặc `sessions_spawn` để:
- Gửi message đến agent khác
- Spawn sub-agent để làm task

---

## Workspace Structure

```
~/.openclaw/
├── openclaw.json              # Main config
├── workspace-main/             # Main agent workspace
│   ├── SOUL.md
│   ├── AGENTS.md
│   ├── TOOLS.md
│   └── memory/
├── workspace-researcher/       # Researcher workspace
│   ├── SOUL.md
│   └── ...
├── agents/
│   ├── main/
│   │   ├── agent/             # Auth profiles, codex-home
│   │   └── sessions/          # Chat history
│   └── researcher/
│       ├── agent/
│       └── sessions/
└── credentials/                # Channel credentials
```

---

## Ví dụ: Researcher bot tự tạo agent mới

```json5
// Config patch để thêm researcher-secondary agent
{
  agents: {
    list: [
      // existing agents...
      {
        id: "researcher-secondary",
        name: "Research Assistant",
        workspace: "~/.openclaw/workspace-researcher-sec",
        agentDir: "~/.openclaw/agents/researcher-secondary/agent",
        skills: ["web-search"],
        tools: {
          profile: "coding",
          allow: ["read", "write", "exec", "process"],
          deny: ["gateway", "cron", "browser"],
        },
      }
    ]
  },
  bindings: [
    {
      agentId: "researcher",
      match: { channel: "telegram", peer: { kind: "group", id: "-1005195161709" } }
    },
    {
      agentId: "researcher-secondary",
      match: { channel: "telegram", peer: { kind: "dm" } }
    }
  ]
}
```

---

## Lệnh CLI hữu ích

```bash
# Xem current config
openclaw config show

# Thêm agent mới via wizard
openclaw agents add <agent-id>

# Setup workspace
openclaw setup --workspace ~/.openclaw/workspace-<agent-id>

# Kiểm tra config
openclaw doctor
```

---

## Cấu hình cho ResearchClaw

Để ResearchClaw bot có thể tạo thêm agent, cần:

1. **Thêm vào `ownerAllowFrom`** (nếu cần owner commands):
```json5
commands: {
  ownerAllowFrom: ["telegram:1132914873", "telegram:<researcher-bot-id>"]
}
```

2. **Tool permissions** đủ để modify config:
```json5
tools: {
  allow: ["read", "write", "edit", "apply_patch", "exec", "process", "gateway"],
  profile: "full",
}
```

3. **Agent-to-agent enabled**:
```json5
tools: {
  agentToAgent: {
    enabled: true,
    allow: ["main", "hermes", "researcher"],
  },
}
```

---

## ⚠️ CRITICAL: Bindings Format (Tested 2026-05-21)

The `bindings.match.peer` structure is **rejected by OpenClaw** with error "bindings.1: Invalid input".

**Working format** (from backup):
```json
// DON'T use this — it FAILS:
"bindings": [
  {
    "agentId": "techlead",
    "match": {
      "channel": "telegram",
      "peer": { "kind": "dm" }  // ❌ Rejected
    }
  }
]
```

**When bindings fail**, OpenClaw gateway refuses to start. Use `openclaw doctor --fix` or restore backup.

**Safe approach**: Skip bindings entirely for DM routing. Let `requireMention: true` in group settings handle mention-based routing, and route DMs by default to main agent.

If you need explicit routing, test the bindings format with a simple config first before adding to production.

---

## Bot-to-Bot @mention (CONFIRMED WORKING 2026-05-21)

**Telegram @mention between bots WORKS in groups.** Do NOT assume it doesn't work.

**Requirements**:
- Bot must be member of the group
- Use correct group ID format: `-5195161709` (NOT `-1005195161709`)
- Message must mention the bot with `@username`

**Test command**:
```bash
BOT_TOKEN="<your-bot-token>"
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=-5195161709" \
  -d "text=@TargetBotName mention test"
```

---

## Khắc phục lỗi thường gặp

### "Agent not found" khi binding
→ Kiểm tra `agentId` trong `bindings` khớp với `id` trong `agents.list`

### "Tool not available"
→ Kiểm tra `tools.allow`/`tools.deny` và `tools.profile`

### "Bot-to-bot message not delivered"
→ Telegram filter chặn bot-to-bot @mention. Workaround:
  - Dùng DM thay vì group @mention
  - Hoặc forward qua human relay
  - Hoặc dùng `sessions_send` tool thay vì chat message

---

## Reference

- [[agentic-ai]] — Agentic AI concepts (L0-L4 levels)
- [[multi-agent-orchestrator]] — Multi-agent coordination patterns
- [OpenClaw docs: agents config](https://docs.openclaw.ai/gateway/config-agents)
- [OpenClaw docs: multi-agent](https://documentation.openclaw.ai/concepts/multi-agent)
- [OpenClaw docs: agents config](https://docs.openclaw.ai/gateway/config-agents)
- [OpenClaw docs: multi-agent](https://documentation.openclaw.ai/concepts/multi-agent)