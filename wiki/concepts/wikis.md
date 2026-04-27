---
title: "Wikis"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [knowledge-management, documentation, collaboration, software, web]
---

# Wikis

## Overview

A wiki is a collaborative website that allows users to create, edit, and interlink pages using a web browser, typically through simplified markup or WYSIWYG editing. The canonical wiki—and the origin of the concept's name—is Wikipedia, launched in 2001 by Jimmy Wales and Larry Sanger, which demonstrated that collaborative authorship could produce comprehensive reference works trusted by millions. The Hawaiian word "wiki" means "quick," reflecting the founding principle: rapid collaborative editing without barriers.

Wikis differ from traditional websites in their decentralized editing model. Rather than requiring technical knowledge to publish or requiring content to pass through gatekeepers, wikis let any authorized user edit any page. This creates a different content lifecycle: pages evolve through incremental improvements rather than planned releases. The wiki captures not just content but the editing history, enabling reconstruction of how understanding developed over time.

The technology underpins knowledge management systems, intranets, documentation platforms, and collaborative writing environments. MediaWiki—the software powering Wikipedia—remains the most deployed wiki engine, but alternatives like Confluence, Notion, GitBook, and Docusaurus serve specific niches. Personal wikis like Obsidian and Logseq bring the interlinked, non-linear organization to individual knowledge management.

## Key Concepts

**Interlinking** is the defining feature that distinguishes wikis from document collections. Pages contain hyperlinks to other pages, creating a web of knowledge rather than a hierarchy. Wiki pages often use `` syntax to create links, where the link target may be an existing page (creating a connection) or a new page (stub creation). Backlinks—references to the current page from other pages—enable discovery of related content without knowing exact page names.

**Revision History** records every change made to a page, storing the previous content and metadata about who changed it and when. This history enables collaboration by providing a safety net—mistakes can be reverted, and the evolution of ideas becomes traceable. Some wikis support comparing versions side-by-side, diff views highlighting additions and deletions. The history feature transforms content from ephemeral drafts into persistent records.

**Namespaces** organize pages into separate virtual spaces within a single wiki, preventing name collisions and providing logical grouping. A wiki might have a `User:` namespace for personal pages, `Help:` for documentation about editing, `Template:` for reusable page fragments, and `Category:` for organizational groupings. Namespace prefixes appear before page titles, like `Project:Architecture` versus `User:John/Notes`.

**Templates** enable content reuse and consistency. A template is a page whose content is transcluded (included) into other pages by reference. A `Note` template might wrap content in a styled box, a `Related` template might auto-generate a list of related pages, and a `Stub` template might mark incomplete articles. Templates propagate changes to all pages that use them—a single edit can update dozens of pages simultaneously.

## How It Works

Wiki engines typically store content in one of three ways: file-based storage (flat files in a directory structure), database storage (relational or NoSQL), or hybrid approaches. MediaWiki uses MySQL/PostgreSQL for content and Elasticsearch for search. The database schema represents pages, revisions, user accounts, and the link graph (which pages reference which). Each revision is stored as a complete snapshot rather than deltas, enabling reconstruction of any historical state.

The rendering pipeline converts wiki markup (or HTML for WYSIWYG wikis) into HTML for display. Parser functions process templates, magic words (special variables like `{{CURRENTYEAR}}`), and markup syntax. Caching layers (Redis, Memcached) store rendered HTML to avoid reparsing for every view. The link graph is computed during parsing and stored separately for backlink queries and link validation.

Permission systems control who can read, edit, create, and delete pages. Simple wikis use open models (anyone can edit), while enterprise wikis implement fine-grained permissions—restricting certain namespaces to specific user groups, requiring approval for edits to protected pages, or logging all changes for audit purposes.

## Practical Applications

**Documentation** is the most common enterprise wiki use case. Internal knowledge bases, product documentation, API references, and runbooks live in wikis where they can be collaboratively maintained. Unlike static documentation in repositories, wiki documentation can be updated by non-technical contributors, iterated rapidly, and organized by topic rather than by file location. Git-sync features in modern wikis like Gollum or GitBook bridge the gap with code documentation.

**Project Wikis** serve as living records of project decisions, meeting notes, architecture discussions, and onboarding materials. Rather than scattered in email threads or meeting recordings, project knowledge accumulates in searchable, interlinked pages. Status tracking, owner assignment, and template-based page creation help maintain structure as projects grow.

**Personal Knowledge Management (PKM)** has embraced wiki principles through tools like Obsidian, Logseq, and Roam Research. These "second brain" applications apply bidirectional linking, block references, and graph views to individual note collections. The distinction between wiki and PKM tools blurs as both evolve—Notion combines wiki structure with databases, while Obsidian supports community plugins and publish capabilities.

## Examples

A typical MediaWiki article with common markup:

```mediawiki
= Main Heading =
== Section ==
This is a paragraph with a [[Link]] to another page.

=== Subsection ===
Lists are easy:
* First item
* Second item
* Third item

{{Note|This is a template transclusion}}

[[Category:Examples]]
```

This demonstrates headings, paragraphs, internal links, lists, template transclusion, and categorization—the core building blocks of wiki content.

## Related Concepts

- [[Markdown]] - Lightweight markup syntax used by many wikis
- [[Knowledge Management]] - The discipline wikis support
- [[Interlinked Data]] - The graph structure wikis create
- [[MediaWiki]] - The software powering Wikipedia
- [[Documentation]] - Content often hosted on wikis

## Further Reading

- [MediaWiki Documentation](https://www.mediawiki.org/wiki/Documentation)
- [Wiki Principles (Wikipedia)](https://en.wikipedia.org/wiki/Wiki#Key_principles)
- [Building Your Second Brain (Tiago Forte)](https://www.buildingasecondbrain.com/)

## Personal Notes

Wikis thrive on contribution frequency, but many corporate wikis stagnate because editing feels like a chore. I've found that reducing friction—quick ways to capture notes, templates for common page types, and visible activity—keeps wikis alive. For personal use, Obsidian's local-first approach and graph visualization have changed how I think about connecting ideas. The wiki principle of links as first-class citizens applies far beyond traditional wikis.
