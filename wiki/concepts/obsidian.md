---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 user-profile (extracted)
  - 🔗 wikilinks (extracted)
  - 🔗 double bracket links (extracted)
  - 🔗 auto-ingest/obsidian-web-clipper (extracted)
  - 🔗 wikilinks (extracted)
  - 🔗 wiki (extracted)
  - 🔗 auto-ingest/obsidian-web-clipper (extracted)
  - 🔗 core-brain-concepts (extracted)
relationship_count: 8
---

# Obsidian

## Overview

Obsidian là local-first markdown note-taking app. Wiki của [[user-profile]] sử dụng pure Markdown structure (không dùng Obsidian) nhưng tham khảo nhiều concepts từ Obsidian ecosystem.

## Obsidian Concepts Used in Wiki

- [[wikilinks]] — `[[double bracket links]]` pattern từ Obsidian
-  — Folder structure concept
-  — Automation patterns

## Obsidian Web Clipper

Xem [[obsidian-web-clipper]] cho bookmarklet-based web clipping.

## Why Not Obsidian?

Wiki dùng pure markdown files thay vì Obsidian vì:
1. **AI-first**: AI có thể đọc/ghi markdown files trực tiếp
2. **No lock-in**: Không phụ thuộc vào Obsidian database
3. **Git-friendly**: Dễ sync với GitHub
4. **Tool-agnostic**: Có thể dùng bất kỳ text editor nào

## Vault Structure

```
~/wiki/                  ← Wiki vault root
├── concepts/            ← Main knowledge pages
├── raw/                 ← Original captures
│   ├── conversations/   ← Meeting notes, transcripts
│   ├── bookmarks/       ← Saved web content
│   └── emails/          ← Email captures
├── _meta/               ← System pages (start-here, schema)
├── scripts/             ← Automation scripts
└── auto-ingest/         ← Setup guides
```

## Essential Plugins

### Core Plugins
| Plugin | Purpose |
|--------|---------|
| File recovery | Backup and version history |
| Backlinks | See what links to current page |
| Outline | Document structure navigation |
| Search | Full-text search across vault |

### Community Plugins
| Plugin | Purpose |
|--------|---------|
| obsidian-git | Auto-sync vault to GitHub |
| Various | Check `.obsidian/community-plugins.json` for full list |

## Configuration

### `.obsidian/workspace.json`
Stores:
- Open tabs
- Pinned files
- Panel layouts
- Recent files

## Workflow Integration

### Capture
- **Bookmarklet**: Save web pages via browser bookmark
- **iOS Shortcuts**: Save from any app
- **RSS**: Auto-ingest via Fiery Feeds

### Processing
- Raw captures → `raw/` folder
- LLM agent → Parse and create concept pages in `concepts/`
- Wikilinks → Connect to existing knowledge graph

### Retrieval
- **Graph view**: Visualize connections
- **Backlinks panel**: See incoming links
- **Quick switcher** (Cmd+O): Fast file switching

## Related

- [[wikilinks]] — Link syntax used
- [[wiki]] — The wiki implementation
- [[obsidian-web-clipper]] — Web clipping method
- [[core-brain-concepts]] — Knowledge management principles
