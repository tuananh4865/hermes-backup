---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 self-healing-wiki (extracted)
  - 🔗 wiki-health (extracted)
  - 🔗 link (inferred)
last_updated: 2026-04-11
tags:
  - wiki
  - orphans
  - health
  - links
---

# Orphan Page

> A page with no inbound links — isolated from the knowledge graph.

## Overview

An orphan page is a wiki page that no other page links to. While the content may exist, it becomes difficult to discover because there's no path from other pages.

**Goal:** Zero orphan pages. Every page should be reachable from at least one other page.

## Why Orphans Are a Problem

1. **Discoverability**: Users can't find pages unless they know to search
2. **Knowledge gaps**: Orphans suggest disconnected concepts
3. **Maintenance burden**: Easy to forget about orphan pages
4. **Quality issues**: Often indicates incomplete linking strategy

## Finding Orphans

### Our Script
```bash
# Find all orphan pages
python3 scripts/wiki_lint.py --orphans

# Output:
# Orphan pages found:
# - concepts/rag-(retrieval-augmented-generation).md
# - concepts/self-healing-wiki.md
# - ...
```

### Manual Check
```python
from pathlib import Path
import re

def find_orphans():
    pages = list(Path("concepts").glob("*.md"))
    links = set()
    
    # Collect all links
    for page in pages:
        content = page.read_text()
        wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        links.update(wikilinks)
    
    # Find unlinked pages
    orphans = []
    for page in pages:
        name = page.stem
        # Check if page name is in links (case-insensitive)
        if not any(name.lower() == l.lower() for l in links):
            orphans.append(page)
    
    return orphans
```

## Fixing Orphans

### 1. Add Links from Related Pages
```markdown
<!-- Find the most related page -->
<!-- Add link to orphan -->

In [[rag]]:
RAG is a powerful pattern. For implementation, see [[RAG Implementation]].
```

### 2. Add to Index Pages
```markdown
<!-- In _meta/index.md or concepts/index.md -->

## All Concepts

- [[Self-Healing Wiki]] — Wiki that fixes itself
- [[Autonomous Wiki Agent]] — Agent managing wiki
```

### 3. Create Cross-References
```markdown
<!-- In orphan.md, add "Linked from" section -->

## Linked From
- [[related-concept-1]]
- [[related-concept-2]]
```

## Orphan Prevention

### Pre-Publishing Checklist
```
□ Does this page link to 3+ related concepts?
□ Is this page linked from at least 1 other page?
□ Have I added it to the index if it's important?
□ Does it appear in relevant lists?
```

### Link Density Monitor
```python
def check_link_density():
    """Ensure every page has minimum links."""
    pages = Path("concepts").glob("*.md")
    
    for page in pages:
        content = page.read_text()
        wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        
        if len(wikilinks) < 3:
            print(f"Warning: {page.name} only has {len(wikilinks)} links")
```

## Wiki Health Metrics

| Metric | Good | Warning | Poor |
|--------|------|---------|------|
| Orphan count | 0 | 1-5 | 5+ |
| Pages with <2 links | <10% | 10-30% | 30%+ |

## Auto-Fix with Self-Healing

Our self-healing script can auto-link orphans:

```bash
# Run self-heal
python3 scripts/wiki_self_heal.py --fix-orphans

# Script will:
# 1. Find orphan pages
# 2. Identify related pages
# 3. Add wikilinks
# 4. Update index if needed
```

## Related Concepts

- [[self-healing-wiki]] — Auto-healing mechanisms
- [[wiki-health]] — Overall wiki health
- [[link]] — Links in wiki
- [[cross-linking-strategy]] — Linking best practices

## External Resources

- [Wikipedia: Orphan Pages](https://en.wikipedia.org/wiki/Wikipedia:Orphan)
- [WikiLink Checker](https://example.com/checker)