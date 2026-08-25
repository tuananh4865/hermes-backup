# OpenClaw Bot Permission Config (2026-05-21)

## Problem
@Researcher_Clawd_Bot không reply khi được @mention từ Hermes bot.

## Root Cause
OpenClaw config (`~/.openclaw/openclaw.json`) có `ownerAllowFrom` chỉ cho phép Tuấn Anh (1132914873):
```json
"commands": {
  "ownerAllowFrom": ["telegram:1132914873"]
}
```

## Fix Options

### Option 1: Allow all Telegram users/bots
```json
"commands": {
  "ownerAllowFrom": ["telegram:*"]
}
```

### Option 2: Allow specific group + Tuấn Anh
```json
"commands": {
  "ownerAllowFrom": [
    "telegram:1132914873",
    "telegram:group:-5195161709"
  ]
}
```

## Location
File: `~/.openclaw/openclaw.json`
Path in JSON: `commands.ownerAllowFrom`

## Context
- Researcher bot đã bị xóa worker profile (2026-05-21) - đã xóa content-creator và research-agent workers
- Nhưng OpenClaw bot (@Researcher_Clawd_Bot) vẫn còn trong group Company
- Hermes giờ là Orchestrator, @mention bot khác để giao task