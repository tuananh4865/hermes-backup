---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 wiki (extracted)
  - 🔗 index (extracted)
  - 🔗 search (inferred)
last_updated: 2026-04-11
tags:
  - wiki
  - navigation
  - structure
  - UX
---

# Wiki Navigation

> How to find your way around the wiki knowledge base.

## Overview

Our wiki has multiple navigation paths to help you find information:

1. **Top-level index** — Entry points to major sections
2. **Wikilinks** — Inline connections between concepts
3. **Search** — Find by keyword or concept
4. **Graph view** — Visualize connections

## Navigation Entry Points

### Start Here: _meta/start-here.md
If you're new, begin here:
```
Meta → Start Here
```

### Main Index: index.md
Overview of all sections:
```
index.md → concepts/, projects/, scripts/
```

### Concepts Index
All concept pages organized by category:
```
concepts/index.md → All concept pages
```

## Wikilinks Navigation

The primary navigation method:

```markdown
In any page, links like [[RAG]] take you to that concept.

Use "Back" button or Cmd+[ to return.
```

### Link Navigation
```
          → Go to page
[[Page Name|Text]]     → Go to page, see custom text
[[Page#Section]]       → Go to specific section
```

## Search

### Quick Search
```bash
# Press Cmd+K or Ctrl+K
# Type concept name
# Press Enter
```

### Command Line Search
```bash
# Search by content
python3 scripts/search.py "RAG implementation"

# Search by title
grep -i "rag" concepts/*.md
```

## Directory Structure

```
wiki/
├── _meta/              # Meta information
│   ├── index.md        # Entry point
│   └── start-here.md   # New user guide
├── concepts/           # Knowledge concepts (50+ pages)
│   ├── index.md        # All concepts
│   ├── agentic-ai.md   # Agentic AI
│   ├── rag.md          # RAG pattern
│   └── ...
├── projects/           # Project documentation
│   ├── daily-tasks/
│   └── wiki-quality-improvement/
├── scripts/            # Automation scripts
│   ├── wiki_lint.py
│   ├── wiki_self_heal.py
│   └── ...
└── index.md            # Main index
```

## Finding What You Need

### By Topic
```
index.md → Concepts → Find category → Find page
```

### By Project
```
index.md → Projects → Find project → Find task
```

### By Keyword
```
Search (Cmd+K) → Type keyword → Click result
```

## Breadcrumb Navigation

Many pages show where you are:
```markdown
Wiki > Concepts > AI Agents > RAG
```

## Internal Cross-References

### In "See Also" Sections
```markdown
## Related
- [[RAG]] — Retrieval patterns
- [[Embedding]] — Vector representation
- [[Agentic AI]] — Autonomous systems
```

### "Linked From" Sections
```markdown
## Linked From
- [[rag]] — RAG overview
- [[knowledge-base]] — KB concepts
```
Shows other pages that link to the current page.

## Quick Jumps

- [[index]] — Main wiki index
- [[log]] — Activity log
- [[SCHEMA]] — Wiki conventions

## Navigation Tips

1. **Follow wikilinks**: Start from index, follow links to related concepts
2. **Use search**: Cmd+K for quick access
3. **Check "Related"**: Every page has related concept links
4. **Use "Linked from"**: See what points to current page
5. **Check index**: For overview of any section

## Related Concepts

- [[wiki]] — Wiki system overview
- [[index]] — Index pages
- [[search]] — Search functionality
- [[cross-linking-strategy]] — How links connect content

## External Resources

- [Markdown Navigation](https://example.com)
- [Wiki Best Practices](https://example.com)