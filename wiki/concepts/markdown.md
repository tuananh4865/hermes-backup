---
title: "Markdown"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [markdown, markup, writing, documentation]
---

# Markdown

## Overview

Markdown is a lightweight markup language that enables writers to format plain text documents using simple, readable syntax. Created by John Gruber in 2004 with contributions from Aaron Swartz, Markdown was designed to be easy to read and write by humans, while also being easily converted to HTML and other structured formats.

Unlike traditional markup languages such as HTML or LaTeX, Markdown uses punctuation characters strategically placed to indicate formatting elements. This makes it an ideal choice for documentation, note-taking, blogs, and any context where writing speed and readability matter. Markdown files are plain text, which means they can be edited in any text editor and version-controlled without compatibility issues.

Markdown has become one of the most widely used markup languages in software development and technical writing. It powers readme files on GitHub, documentation sites like GitBook and MkDocs, forum software, and content management systems. Its simplicity belies its power—complex documents can be authored quickly without fighting with complicated syntax.

## Syntax

### Headings

Headings are created using hash symbols (#) preceding the heading text. The number of hashes indicates the heading level, from one (# Heading 1) to six (###### Heading 6).

### Emphasis

Text can be made **bold** using double asterisks or underscores, or *italic* using single asterisks or underscores. Strikethrough uses double tildes.

### Lists

Unordered lists use hyphens, asterisks, or plus signs. Ordered lists use numbers followed by periods.

```
- Item one
- Item two
  - Nested item
```

### Links

Links are created using square brackets for the link text and parentheses for the URL: `[link text](https://example.com)`.

### Code

Inline code uses backticks: `code`. Code blocks use triple backticks with optional language specification:

```markdown
```python
def hello():
    print("Hello, world!")
``\
```

### Blockquotes

Blockquotes are created using the greater-than symbol (>), with nested quotes supported through additional > symbols.

### Horizontal Rules

Horizontal rules are created using three or more hyphens, asterisks, or underscores on their own line.

## Extensions

### GitHub Flavored Markdown (GFM)

GitHub Flavored Markdown extends standard Markdown with additional features useful for software documentation. GFM adds support for tables, task lists, autolinked URLs, strikethrough, and fenced code blocks with syntax highlighting. It also defines spec-compliant behavior for line breaks and HTML block elements.

### MDX

MDX is an extension that allows developers to embed JSX components within Markdown documents. This powerful combination enables authors to import and use interactive React components directly in their content, making it popular for documentation sites, blogs, and interactive tutorials where rich interactivity is needed.

### Other Extensions

Various Markdown processors implement additional extensions including footnotes, definition lists, custom containers, emoji support, and math equation rendering. Tools like Pandoc, Marked, and remark support extensive customization through these extensions.

## Related

- [[HTML]] — The hypertext markup language that Markdown commonly converts to
- [[documentation]] — A primary use case for Markdown
- [[wikilinks]] — The double-bracket link syntax used in this wiki
- [[writing]] — Markdown as a writing tool
- [[self-healing-wiki]] — The system that created this stub
