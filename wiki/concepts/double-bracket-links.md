---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 wiki-syntax (related)
  - 🔗 zettelkasten (related)
  - 🔗 obsidian (related)
  - 🔗 roam-research (related)
relationship_count: 4
---

# Double Bracket Links

Double bracket links (`[[link]]`) are a wiki-style syntax used in networked note-taking applications to create internal hyperlinks between notes or documents. This syntax has become a cornerstone of the zettelkasten methodology and modern knowledge management systems like [[obsidian]].

## Overview

The double bracket syntax encloses a link target within two square brackets, like `[[target-note]]`. When rendered, this typically becomes a clickable link that navigates to the target note or creates it if it doesn't exist. This bidirectional linking mechanism enables users to build interconnected networks of ideas rather than hierarchical structures.

### Key Features

- **Automatic linking**: Links are created by simply typing the double brackets with a note name
- **Backlinks**: Most implementations automatically track which notes link to the current note
- **Alias support**: Many apps allow `[[target|alias]]` syntax to display different text
- **Unlinked references**: Some apps can detect mentions of a note's title without explicit brackets

## History and Origins

The double bracket syntax originated from early wiki systems. The concept was inspired by Niklas Luhmann's Zettelkasten system, which used paper-based linked notes.

## Common Implementations

### [[obsidian]]

Obsidian popularized the double bracket syntax in the modern PKM space. It supports:
- `` - basic linking
- `[[Note Title#Heading]]` - link to specific heading
- `[[Note Title#^block]]` - link to specific block
- `[[Note Title|display text]]` - aliased links

## Related Concepts

- [[wikilink]] - broader wiki formatting standards
- [[obsidian]] - the app that popularized this syntax
- [[knowledge-base]] - knowledge management systems that use linking

## Best Practices

1. **Use descriptive titles**: Note names should clearly indicate content
2. **Avoid duplicates**: Create single notes for topics rather than multiple variants
3. **Maintain consistent naming**: Decide on title case, date formats, or naming conventions early
4. **Leverage aliases**: Use `[[Target|Display Text]]` when the link context needs clarification

