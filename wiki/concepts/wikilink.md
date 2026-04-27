---
title: Wikilink
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [wikilinks, obsidian, linking, knowledge-management]
---

# Wikilink

## Overview

A wikilink, short for "wiki link," is a hyperlink created using double bracket syntax `[[link target]]` that connects one document or note to another within a wiki-style knowledge base. Originally popularized by Wikipedia and early wiki systems, wikilinks enable rapid, frictionless navigation between related pieces of information. Unlike traditional HTML hyperlinks that require explicit URL formatting, wikilinks reference documents by their titles or identifiers, allowing authors to create connections intuitively while the system resolves the actual destination behind the scenes.

Wikilinks form the backbone of networked note-taking and personal knowledge management systems. By embedding connections directly into content, users can build associative webs of information where ideas naturally link to related concepts. This approach mirrors how human memory works through association rather than hierarchy, making wikilinks particularly powerful for knowledge synthesis, research, and long-term information retention. When a wikilink points to a document that does not yet exist, many systems offer to create the target document automatically, encouraging incremental knowledge building.

## Syntax

The fundamental wikilink syntax consists of double brackets surrounding the target document's name or identifier. The most common forms include `` for linking to a page by its exact title, and `[[Document Title|Display Text]]` for creating a link that shows alternative text while still pointing to the original target. Some systems also support anchors within pages using the hash symbol, such as `[[Document Title#Section Header]]`, which links directly to a specific section rather than the top of the document.

Wiki-style link resolution varies by platform. Most systems perform case-insensitive matching against document titles, handling spaces and special characters automatically. When a wikilink's target matches multiple documents, some systems present disambiguation options while others select the closest match. Many modern implementations also support relative linking, where `[[./Sibling Document]]` or `[[../Parent Document]]` navigates relative to the current document's location in a folder structure. Alias links allow `[[Original Title]]` to redirect to a different document, enabling flexible naming without duplicating content.

## Best Practices

Effective wikilink usage follows several established conventions that improve readability and maintainability. Link text should be descriptive and meaningful outside of context, avoiding generic phrases like "click here" or "read more." When linking to a concept, use the document's canonical title as the link text rather than paraphrasing it, which ensures consistency and helps readers recognize when they encounter the same topic across different notes.

Naming conventions matter significantly in wikilink-based systems. Adopt a consistent title format, whether sentence case, title case, or all lowercase with hyphens. Some teams prefer kebab-case titles like `knowledge-management` for URL compatibility, while others use natural language titles that read naturally when displayed. Regular maintenance helps prevent broken links as documents are renamed or reorganized; many tools include broken link detection to identify connections that no longer resolve correctly.

Balance link density to keep documents readable. Over-linking every名词 creates visual noise and dilutes the significance of connections, while under-linking misses opportunities for association. A good practice is linking to concepts when they are first introduced or when the link provides direct value to the reader's understanding. Finally, use stub notes strategically. Creating a minimal page with `[[wikilinks]]` to future topics seeds the knowledge base gradually and makes emerging ideas findable.

## Related

- [[Zettelkasten]] - A note-taking method that heavily relies on wiki-style linking for building interconnected knowledge graphs
- [[Backlinks]] - The reverse references that show which documents link to the current page, essential for discovering unexpected connections
- [[Knowledge Graph]] - A structured representation of interconnected knowledge that wikilinks help build at the document level
- [[Obsidian]] - A popular note-taking application that popularized the use of wikilinks in personal knowledge management
- [[Markdown Links]] - Standard markdown link syntax that predates and differs from wiki-style double bracket links
- [[Digital Garden]] - An approach to knowledge sharing where wikilinks create navigable networks of interconnected notes
- [[Bidirectional Linking]] - The concept of links that connect in both directions, where backlinks enable traversing knowledge in multiple directions
