---
title: Transclusion
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [wiki, wiki-syntax]
confidence: low
---

# Transclusion

Transclusion is the inclusion of one page's content within another page via a link reference. The content is embedded (not just linked), enabling modular, reusable content in wikis.

## Concept

Instead of copying content, you reference it:
```
{{transclude: some-page}}
```

The content of `some-page` is rendered in-place at the location of the transclusion.

## Use Cases

- **Templates**: Include a standard header/footer across pages
- **Reusable Blocks**: Share content without duplication
- **Living Documents**: Update once, reflect everywhere

## Relationship to Backlinks

Transclusion is the complementary pattern to [[backlinks]]:
- Backlinks show WHAT points TO a page
- Transclusion shows HOW to embed a page's content

## Implementation in This Wiki

This wiki uses markdown-based transclusion via Obsidian-compatible syntax where supported.

## Related

- [[wiki]] — Where transclusion is used
- [[wiki-syntax]] — Syntax details
- [[backlinks]] — Related navigation mechanism
