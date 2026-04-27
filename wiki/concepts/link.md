---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 wikilinks (extracted)
  - 🔗 cross-linking-strategy (extracted)
  - 🔗 navigation (inferred)
last_updated: 2026-04-11
tags:
  - wiki
  - linking
  - navigation
---

# Link

> Links connect wiki pages, creating a knowledge graph rather than isolated documents.

## Overview

In our wiki, links come in two types:
1. **Internal links** (wikilinks): ``
2. **External links**: `[Text](https://example.com)`

Links transform a collection of pages into a navigable knowledge graph.

## Wikilinks

### Syntax
```markdown
           # Link to page
[[Page Name|Display]]   # Link with custom text
```

### Examples
```markdown
See [[RAG]] for details.
The [[Transformer]] architecture uses [[Attention]].
[[Local LLM Agents|LM Studio]] and [[Local LLM Agents|Ollama]] support local models.
```

### Alias Handling
If a page has multiple names or spellings:
```markdown
[[Large Language Model|LLM]]  # "LLM" displays, links to "Large Language Model"
[[RAG]]  # Direct link
[[rag]]  # Case-insensitive
```

## External Links

### Syntax
```markdown
[Link Text](https://example.com)
[GitHub](https://github.com)
[Report](./reports/analysis-2024.md)  # Relative path
```

### Best Practices
```markdown
<!-- Good -->
[Hugging Face Transformers](https://huggingface.co/transformers)

<!-- Bad - no description -->
Click [here](https://example.com) for more.
```

## Link Validation

### Check for Broken Links
```bash
python3 scripts/wiki_lint.py --broken

# Output:
# ERROR: concepts/rag.md links to [[nonexistent-page]] which doesn't exist
```

### Auto-Fix Broken Links
```bash
# Creates stub pages for missing links
python3 scripts/wiki_lint.py --auto-fix

# Or remove the broken link
python3 scripts/wiki_lint.py --remove-broken
```

## Link Density

Each page should have appropriate outbound links:
- **Too few** (< 2): Page is isolated, misses context
- **Just right** (3-8): Well-connected to related concepts
- **Too many** (> 15): Link spam, hard to read

## Backlinks (Inbound Links)

Pages that link TO a given page:
```markdown
<!-- In transformer.md -->
Transformers power [[LLM]] models.

<!-- In llm.md, "Linked from" section shows: -->
## Linked From
- [[transformer]]

This helps discover how pages are used.

## Link Placement

### First Paragraph
Introduce core concepts:
```markdown
# RAG

RAG combines [[Retrieval]] with [[Generation]] to...

This pattern is fundamental to modern [[Knowledge Base]] systems.
```

### Examples Section
Reference implementations:
```markdown
## Implementation

See [[RAG Implementation]] for code examples.
Uses [[Chroma]] as the vector database.
```

### Related Section
Curated connections:
```markdown
## Related

- [[Knowledge Base]] — Building knowledge stores
- [[Vector DB]] — Embedding storage
- [[Embedding]] — How text becomes vectors
```

## Broken Link Patterns

### Misspellings
```markdown
<!-- Wrong -->
[[attention]], [[Transfromer]]

<!-- Correct -->
[[Attention]], [[Transformer]]
```

### Renamed Pages
When renaming a page:
1. Update all links pointing to it
2. Or create redirect: `redirect_to: new-page-name`

## Related Concepts

- [[wikilinks]] — Wikilink syntax
- [[cross-linking-strategy]] — Link best practices
- [[navigation]] — How to navigate the wiki

## External Resources

- [Markdown Links](https://www.markdownguide.org/basic-syntax/#links)
- [Wiki Creole Link Syntax](https://www.wikicreole.org/wiki/links)