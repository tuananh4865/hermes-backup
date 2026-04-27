---
title: "Rowboat"
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [ai-agent, note-taking, knowledge-graph, local-first]
---

# Rowboat

> Open-source AI coworker that turns work into a knowledge graph and acts on it.

Rowboat connects to email and meeting notes, builds a long-lived knowledge graph, and uses that context to help users get work done — privately, on their machine.

## Executive Summary

Rowboat is a local-first AI assistant that maintains an [[Obsidian-compatible vault]] of plain Markdown notes with backlinks. It integrates with Gmail, Google Calendar, and meeting note services (Fireflies/Rowboat native) to build a personal knowledge graph that can be queried contextually. Unlike cloud-first assistants, Rowboat keeps all data local and readable/editable with standard tools.

## Key Features

### Knowledge Graph
- Builds personal knowledge graph from email, meetings, notes
- Tracks people, companies, topics through live notes
- [[Graph State Tracking|mtime + SHA-256 hash]] hybrid state tracking — only re-processes when content actually changes
- In-memory knowledge index for fast search of People, Orgs, Projects, Topics
- Full git-style versioning via `version_history.ts`

### AI Agents
Rowboat uses specialized agents defined as plain `.md` files:

| Agent | Function |
|-------|----------|
| `note_creation` | Extract entities from email/meeting → create/update notes |
| `labeling` | Label emails with tags |
| `note_tagging` | Auto-tag notes |
| `inline_task` | Handle inline tasks |
| `agent_notes` | AI records user preferences |

Agent definitions in `WorkDir/agents/` use YAML frontmatter:
```markdown
---
model: gpt-5.2
tools:
  workspace-writeFile:
    type: builtin
---
# Context
[system prompt body]
```

### Integrations
- **Gmail** — email integration
- **Google Calendar** — calendar events
- **Fireflies** or **Rowboat native** — meeting notes
- **MCP SDK** — full integration (stdio, StreamableHTTP, SSE transports)
- **Composio** — 1000+ external tools
- **Deepgram** — voice input
- **ElevenLabs** — voice output
- **Exa** — web search

### Business Model
- 14-day free trial
- Credit-based pricing after trial
- Mac/Windows/Linux desktop app (Electron)

## Architecture

### Core Packages (`apps/x/packages/core/src/`)

```
├── knowledge/
│   ├── build_graph.ts     # Main graph builder (file watcher → agents)
│   ├── note_creation.ts   # Note creation agent prompt
│   ├── note_system.ts    # Note type definitions (People, Orgs...)
│   ├── graph_state.ts    # mtime+hash state tracking
│   ├── knowledge_index.ts # Fast search index
│   └── version_history.ts # Git-style versioning
├── agents/
│   ├── repo.ts           # FS agents repo (.md files)
│   └── runtime.ts        # Agent runtime (Vercel AI SDK)
├── workspace/
│   └── workspace.ts      # File ops với safe path resolution
├── mcp/
│   └── mcp.ts           # MCP client (stdio/HTTP/SSE)
└── di/
    └── container.ts     # Awilix DI setup
```

### Monorepo Structure

```
rowboat/
├── apps/
│   ├── x/                 # Electron desktop app
│   ├── rowboat/           # Next.js web dashboard
│   ├── rowboatx/          # Next.js frontend
│   ├── cli/               # CLI tool
│   ├── python-sdk/        # Python SDK
│   └── docs/              # Documentation site
└── CLAUDE.md              # AI coding agent context
```

### Tech Stack
- **Electron** — cross-platform desktop
- **React + Vite** — renderer UI
- **Vercel AI SDK** — agent runtime
- **pnpm workspaces** — monorepo management
- **Awilix** — dependency injection

## Comparison: Rowboat vs Obsidian

| Feature | Rowboat | Obsidian |
|---------|---------|----------|
| Meeting notes | Fireflies + Granola | Native |
| Price | Free trial, then credit-based | $4.99/mo |
| Target | Knowledge workers | Power users |
| AI Agents | Built-in, specialized | Via plugins |
| Knowledge graph | Auto-built | Manual linking |
| Data storage | Local-first | Local vault |
| API keys | Deepgram, ElevenLabs, Exa, Composio | Community plugins |

## Local-First Design

**Core principle:** `Workspace = Obsidian vault = plain .md files`

- All notes stored as plain Markdown
- Full git-style versioning
- No vendor lock-in — use Obsidian to read/edit directly
- Privacy-first: all processing can happen locally

## Related Topics

- [[Knowledge Graph]]
- [[Local-First Software]]
- [[AI Agents]]
- [[MCP (Model Context Protocol)]]
- [[Obsidian]]

## References

- Repo: https://github.com/rowboatlabs/rowboat
- Website: https://www.rowboatlabs.com
- Download: https://www.rowboatlabs.com/downloads
