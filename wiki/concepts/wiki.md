---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 user-profile (extracted)
  - 🔗 self-healing-wiki (extracted)
  - 🔗 automation (extracted)
  - 🔗 lm-studio (extracted)
  - 🔗 local-llm (extracted)
  - 🔗 knowledge-base (extracted)
  - 🔗 obsidian (extracted)
  - 🔗 karpathy-llm-knowledge-base (extracted)
  - 🔗 intelligent-wiki-roadmap (extracted)
relationship_count: 9
---

# Wiki

## Overview

Personal wiki của [[user-profile]] — một Markdown-based knowledge base được quản lý bởi AI agent.

## Design Principles

1. **Markdown-native** — Pure text files, không lock-in
2. **AI-first** — Được thiết kế để AI đọc và viết
3. **Auto-maintain** — [[self-healing-wiki]] tự sửa chữa
4. **Continuously improving** — [[automation]] tự bổ sung kiến thức

## Architecture

```
~/wiki/
├── _meta/              # System files (SCHEMA.md, start-here.md)
├── concepts/           # Concept pages
├── raw/
│   └── transcripts/    # Raw conversation transcripts
├── scripts/            # Automation scripts
├── auto-ingest/        # Setup guides
└── log.md             # Activity log
```

## Key Features

### Auto-Ingest
- **Transcripts**: Passive capture via Hermes hook
- **Email**: Email forwarding setup
- **RSS**: Auto-ingest via Fiery Feeds

### Self-Maintenance
- **self-healing-wiki**: Auto-fix broken links, missing frontmatter
- **scripts/**: Automation scripts in `scripts/` directory

### AI Tools
- [[lm-studio]] — Local LLM inference
- [[local-llm]] — Local model usage pattern

## Scripts

| Script | Purpose |
|--------|---------|
| wiki_lint.py | Link checking + frontmatter validation |
| wiki_self_heal.py | Auto-fix broken links, missing frontmatter |
| wiki_self_critique.py | Quality scoring |
| wiki_gap_analyzer.py | Missing topic detection |
| wiki_cross_ref.py | Cross-link suggestions |
| wiki_auto_improve.py | Auto-generate content for gaps |

## Related

- [[knowledge-base]] — Knowledge management patterns
- [[obsidian]] — Alternative wiki tool reference
- [[karpathy-llm-knowledge-base]] — Inspiration source
- [[intelligent-wiki-roadmap]] — Future vision
