---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 wikilinks (extracted)
  - 🔗 karpathy-llm-wiki (extracted)
  - 🔗 karpathy-llm-knowledge-bases (extracted)
  - 🔗 autonomous-wiki-agent (extracted)
  - 🔗 wiki-self-evolution (extracted)
relationship_count: 5
---

# llm-wiki

LLM-readable knowledge base stored as structured markdown. The foundation pattern for building AI agents that can reason over personal knowledge — inspired by Andrej Karpathy's LLM Wiki approach.

## Core Concept

Traditional RAG retrieves chunks at query time. LLM Wiki takes a different approach: maintain a living, structured wiki that compounds over time. The LLM becomes both curator and consumer of knowledge.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  THREE-LAYER STACK                                          │
├─────────────────────────────────────────────────────────────┤
│  RAW SOURCES     │ Raw notes, papers, transcripts           │
│                  │ Unstructured, LLM-readable formats       │
├─────────────────────────────────────────────────────────────┤
│  WIKI            │ Structured markdown with frontmatter     │
│                  │ Interlinked, searchable, LLM-compiled     │
├─────────────────────────────────────────────────────────────┤
│  SCHEMA          │ Conventions: frontmatter, wikilinks       │
│                  │ Rules: file naming, link format          │
└─────────────────────────────────────────────────────────────┘
```

## Key Properties

1. **LLM-Readable**: Plain markdown with frontmatter — no database, no embedding store
2. **Queryable**: Natural language search through wiki files
3. **Compounding**: Each query potentially adds to the wiki
4. **Self-Maintaining**: Automated linting, gap analysis, quality scoring

## Maintenance Pipeline

| Tool | Purpose |
|------|---------|
| `wiki_self_heal.py` | Auto-fix broken links, missing frontmatter |
| `wiki_self_critique.py` | Score quality across dimensions |
| `wiki_gap_analyzer.py` | Find topics mentioned but not pages |
| `wiki_cross_ref.py` | Suggest missing wikilinks |
| `lmstudio_wiki_agent.py` | Generate pages via local LLM |

## vs. Traditional RAG

| Dimension | RAG | LLM Wiki |
|-----------|-----|----------|
| **Storage** | Vector database | Markdown files |
| **Query** | Semantic similarity | Natural language file search |
| **Maintenance** | Embedding updates | Git-based version control |
| **Compound knowledge** | Limited | Built-in |
| **Setup complexity** | High | Low |
| **Transparency** | "Black box" retrieval | Explicit file structure |

## Implementation in This Wiki

Our implementation uses:
- **Raw layer**: `raw/transcripts/` — conversation logs
- **Wiki layer**: `concepts/` — structured concept pages
- **Schema**: YAML frontmatter, `[[wikilinks]]`, flat structure

## Related

- [[karpathy-llm-wiki]] — Karpathy's specific implementation
- [[karpathy-llm-knowledge-bases]] — Detailed breakdown
- [[autonomous-wiki-agent]] — Our autonomous implementation
- [[wiki-self-evolution]] — Self-improvement pipeline

## Further Reading

- [Karpathy's LLM Wiki explanation](https://antigravity.codes/blog/karpathy-llm-knowledge-bases)
- [MindStudio: What Is Andrej Karpathy's LLM Wiki?](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code/)
