---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 link (extracted)
  - 🔗 markdown (extracted)
  - 🔗 wiki (inferred)
last_updated: 2026-04-11
tags:
  - wiki
  - wikilinks
  - markdown
  - syntax
---

# Wikilinks

> The `` syntax for creating internal wiki links.

## Overview

Wikilinks are internal links in wiki pages using the `` syntax. They connect concepts within the wiki, creating a knowledge graph instead of isolated documents.

## Syntax

### Basic Link
```markdown

```

Renders as: [Page Name](./Page_Name.md)

### Display Text
```markdown
[[Page Name|Display Text]]
```

Shows "Display Text" but links to "Page Name".

### Case Insensitivity
```markdown
[[rag]]
[[RAG]]
[[Rag]]
```

All resolve to the same page.

## Examples

### In Content
```markdown
RAG combines retrieval with generation. See [[RAG]] for details.

The [[Transformer]] architecture uses [[Attention]] mechanisms.

For implementation, see [[RAG Implementation]].
```

### With Display Text
```markdown
We use [[Local LLM Agents|LM Studio]] for local development.
We use [[Local LLM Agents|Ollama]] for production.

[[Agentic AI|Agentic systems]] can plan and execute autonomously.
```

### Linked Headers
```markdown
See the [[Wiki#navigation|Navigation section]].
Link to a specific section by adding #header:
[[Getting Started#installation]]
```

## Wikilink Processing

Our wiki processes wikilinks with these rules:

### 1. Page Lookup
```python
import re

def resolve_wikilink(link_text: str) -> Optional[Path]:
    # Case-insensitive search in concepts/
    page_name = link_text.strip()
    candidates = [
        f"{page_name}.md",
        f"{page_name.lower()}.md",
        # Also check spaces
        page_name.replace(" ", "-") + ".md"
    ]
    for candidate in candidates:
        path = Path("concepts") / candidate
        if path.exists():
            return path
    return None
```

### 2. Broken Link Detection
```python
def find_broken_links(content: str) -> List[str]:
    wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
    broken = []
    for link in wikilinks:
        if not resolve_wikilink(link):
            broken.append(link)
    return broken
```

### 3. Auto-Creation
When a wikilink points to a missing page:
```python
def create_stub_page(link_text: str):
    page_name = link_text.strip()
    content = f"""---
confidence: medium
last_verified: {datetime.now().strftime('%Y-%m-%d')}
relationships:
  - 🔗 self-healing-wiki (extracted)
---

# {page_name}

> This page was auto-created by [[self-healing-wiki]] to fill a broken link.
> Please expand with real content.

## Overview

{Write overview here}

## Related

- [[self-healing-wiki]]
"""
    path = Path(f"concepts/{page_name}.md")
    path.write_text(content)
    return path
```

## Wikilink Patterns

### Plural Links
```markdown
[[LLM]] → Links to "llm.md"
[[LLMs]] → Can either:
  - Link to "llms.md" (if exists)
  - Show broken link warning
```

### Spaces and Special Chars
```markdown
[[Machine Learning]] → machine-learning.md
[[API Design]] → api-design.md
[[C++]] → c.md (if file named c.md)
[[Q&A]] → q-and-a.md or qa.md
```

### Renaming Pages
When renaming a page, add redirect:
```markdown
---
redirect_to: new-page-name
---
```

## In Different Contexts

### Inline
```markdown
The [[RAG]] pattern is fundamental.
```

### In Lists
```markdown
Related topics:
- [[RAG]]
- [[Embedding]]
- [[Vector DB]]
```

### In Tables
```markdown
| Pattern | Description |
|---------|-------------|
| [[RAG]] | Retrieval-Augmented Generation |
| [[Fine-tuning]] | Model adaptation |
```

## Validation

### Check All Wikilinks
```bash
python3 scripts/wiki_lint.py --check-links
```

### Auto-Fix
```bash
# Create stubs for missing pages
python3 scripts/wiki_lint.py --create-stubs

# Or remove broken links
python3 scripts/wiki_lint.py --remove-broken
```

## Related Concepts

- [[link]] — Links in general (includes external)
- [[markdown]] — Markdown syntax
- [[wiki]] — Wiki system overview

## External Resources

- [Wiki Creole 1.0](https://www.wikicreole.org/wiki/links) — Wikilink standard
- [Markdown Links](https://www.markdownguide.org/basic-syntax/#links) — Standard markdown links