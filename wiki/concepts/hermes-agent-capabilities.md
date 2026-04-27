---
title: "Hermes Agent Capabilities"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [hermes, agent, capabilities]
---

# Hermes Agent — System Capabilities Wiki

> Document này mô tả toàn bộ khả năng của Hermes Agent (version đang chạy trên máy này).
> Được tạo để em luôn hiểu rõ bản thân mình.

## Version & Environment

- **Hermes**: v0.8.0 (2026.4.8) — 182 commits behind upstream
- **Project path**: `/Users/tuananh4865/.hermes/hermes-agent`
- **Python**: 3.11.15
- **Config**: `~/.hermes/config.yaml`

## Core Architecture

```
Telegram/Slack/Discord → Gateway → Session Store → AIAgent (run_agent.py)
                                                      ↓
                                              Tool Registry (40+ tools)
                                                      ↓
                                           Terminal / File / Web / Browser
```

### Agent Loop
1. Receive message → build system prompt (SOUL.md + memory + skills)
2. Call LLM with tools → receive tool calls or text response
3. Execute tools → return results → repeat until done
4. Save to memory (Honcho) + trajectory logs

---

## Available Tools (40+)

### Terminal & Execution
| Tool | Description |
|------|-------------|
| `terminal_tool` | Run shell commands, manage background processes |
| `code_execution_tool` | Execute Python scripts in sandbox |
| `delegate_task` | Spawn subagents for parallel work |

### File Operations
| Tool | Description |
|------|-------------|
| `file_tools` | read, write, search, patch files |
| `file_operations` | glob, find, ls with pattern matching |

### Web & Browser
| Tool | Description |
|------|-------------|
| `web_tools` | search (Parallel, Firecrawl), extract URLs |
| `browser_tool` | CDP browser automation via Camofox |

### Memory & Session
| Tool | Description |
|------|-------------|
| `memory_tool` | Save/read to Honcho memory (MEMORY.md, USER.md) |
| `session_search_tool` | FTS5 full-text search across sessions |

### Skills & Skillsets
| Tool | Description |
|------|-------------|
| `skill_manager_tool` | Create, update, list skills |
| `skills_tool` | Load and execute skills |
| `skills_hub` | Browse agentskills.io marketplace |

### Cron & Scheduling
| Tool | Description |
|------|-------------|
| `cronjob_tools` | Create, list, pause, resume scheduled jobs |

### MCP (Model Context Protocol)
| Tool | Description |
|------|-------------|
| `mcp_tool` | Connect to MCP servers |
| `mcp_oauth` | OAuth handling for MCP servers |

### Other
| Tool | Description |
|------|-------------|
| `vision_tools` | Analyze images |
| `transcription_tools` | Audio transcription |
| `tts_tool` | Text-to-speech |
| `send_message_tool` | Send to Telegram/Discord/etc |
| `todo_tool` | Manage task list |
| `patch_parser` | Apply unified diffs |

---

## Learning Loop System

Detailed in: [hermes-agent-complete-guide.md](./hermes-agent-complete-guide.md) (§03-05)

### 1. Trajectory Saving
```
~/.hermes/memories/trajectory_samples.jsonl  (success)
~/.hermes/memories/failed_trajectories.jsonl  (failures)
```
Each conversation saved in ShareGPT format. Can be used to train models.

### 2. Skill Creation & Self-Improvement
After completing complex task:
1. `skill_manager_tool` detect repeated patterns
2. Create `~/.hermes/skills/{skill-name}/SKILL.md`
3. Skills self-improve through usage

**Status on this machine**: Manual creation only. Auto-creation not yet observed in v0.8.0.

### 3. Honcho Memory
```
~/.hermes/memories/MEMORY.md    → Agent's knowledge
~/.hermes/memories/USER.md      → User profile & preferences
```
Sync after each turn, prefetch before next turn.

### 4. Session Search
SQLite FTS5 index for searching conversation history with LLM summarization.

---

## Multi-Agent / Subagent

### Delegate Tool
```python
delegate_task(goal="...", context="...", toolsets=["terminal","file"], model="...")
```

**Constraints:**
- MAX_DEPTH = 2 (parent → child, no grandchild)
- Blocked tools: {delegate_task, clarify, memory, send_message, execute_code}
- max_concurrent_children = 3
- Heartbeat mechanism to prevent gateway timeout

**Use cases:**
- Batch processing multiple tasks in parallel
- Isolate dangerous operations
- Parallel research (search multiple sources simultaneously)

### ACP (Agent Communication Protocol)
```
acp_adapter/ → VS Code / Zed / JetBrains integration
acp_registry/ → capability registry for cross-agent handoff
```
Hermes can communicate with Claude Code, Codex via structured interface.

---

## Messaging Gateway

### Platforms
- **Telegram** (active, chat_id: 1132914873)
- WhatsApp
- Discord
- Slack
- Signal
- Home Assistant

### Features
- Cross-platform conversation continuity
- Slash commands via message
- Voice memo transcription
- `/new`, `/retry`, `/undo`, `/model`, `/personality`
- Platform-specific: `/status`, `/sethome`, `/approve`

---

## Cron Scheduling

Jobs stored in `~/.hermes/cron/`:
- Delivery to Telegram, Discord, or local file
- Native cron syntax: `0 9 * * *` or human: `every 2h`
- Can chain: job A → job B after completion

---

## Skills System

### agentskills.io Standard
Skills follow agentskills.io spec — compatible with Claude Code, Codex, Cursor.

### Current Skills (92+ skills)
```
~/.hermes/skills/
├── apple/                    # Apple ecosystem (iOS, SwiftUI, etc.)
├── autonomous-app-builder/   # iOS app pipeline
├── apple-skills/            # Apple official skills plugin
├── wiki/                     # Wiki operations
├── ... (88 more)
```

### Skill Loading
Skills are injected into system prompt as user message (not system prompt) to preserve prompt caching.

---

## Configuration

### Key Settings (config.yaml)
```yaml
model:
  default: MiniMax-M2.7
  provider: minimax

agent:
  max_turns: 300
  gateway_timeout: 1800
  inactivity_timeout: 7200
  reasoning_effort: medium

terminal:
  backend: local
  timeout: 180

browser:
  cloud_provider: camofox

compression:
  enabled: true
  threshold: 0.85
```

### 16 Personalities
kawaii, catgirl, pirate, shakespeare, surfer, noir, uwu, philosopher, hype...

---

## Known Features Not Yet Fully Utilized

1. **Skill自改进 (Self-improving Skills)**: Skills auto-evolve from feedback. Currently manual on this machine.
2. **Honcho用户建模**: Not configured. Would enable deeper user preference inference.
3. **Trajectory saving**: Available but not enabled by default.
4. **hermes-dojo**: Self-improvement system. Not explored.
5. **hermes-skill-factory**: Auto-generates skills from workflows. Not tested.

---

## See Also

- [Hermes Agent Complete Guide (橙皮书)](./hermes-agent-complete-guide.md) — Full 17-chapter guide by 花叔
- [Awesome Hermes Agent](https://github.com/0xNyk/awesome-hermes-agent) — Ecosystem resources