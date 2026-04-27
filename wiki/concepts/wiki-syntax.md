---
title: Wiki Syntax
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [wiki, markdown]
confidence: medium
---

# Wiki Syntax

The markup conventions used in this wiki for linking, tagging, and structuring content.

## Wikilinks

```markdown
           — Link to a page
[[page-name|Display]]   — Link with custom display text
```

## Tags

```yaml
tags: [tag1, tag2, tag3]
```

## Frontmatter

Every page starts with YAML frontmatter:

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | personal | meta | project | phase | decision | mistake | retrospective
tags: [tag1, tag2]
confidence: high | medium | low
relationships: [related-page1, related-page2]
---
```

## Headers

```markdown
# H1 — Page title (from frontmatter title)
## H2 — Major sections
### H3 — Subsections
```

## Lists

- Use `-` for unordered lists
- Use `1.` for ordered lists
- Indent with 2 spaces for nesting

## Code Blocks

````markdown
```language
code here
```
````

## Related

- [[wiki]] — The wiki system using this syntax
- [[backlinks]] — How links are tracked
- [[markdown]] — Standard markdown (this wiki extends it)
