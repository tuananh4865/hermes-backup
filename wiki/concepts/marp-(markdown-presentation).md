---
confidence: high
last_verified: 2026-04-11
relationships:
  - [[karpathy-llm-wiki]]
  - [[markdown]]
  - [[llm-wiki]]
relationship_count: 3
---

# Marp (Markdown Presentation)

> An open-source markdown presentation tool that converts markdown files into slide decks.

## Overview

**Marp** (Markdown Presentation Ecosystem) is a markdown-based presentation tool that allows you to write slides in plain text and export them to HTML, PDF, or PowerPoint formats. It uses a markdown extension syntax for slide separation and element control.

## Why Marp

### Traditional vs Marp Workflow

**Traditional presentation creation:**
1. Open PowerPoint/Keynote
2. Click "New Slide" repeatedly
3. Add text, format, adjust positions
4. Spend hours on alignment
5. Update one slide → everything shifts

**Marp workflow:**
1. Write markdown with slide separators
2. Preview live in VS Code or browser
3. Export to HTML/PDF/PPTX
4. Edit text, slides auto-reflow
5. Version control with git

## Marp Syntax

### Slide Separation

Use `---` to separate slides:

```markdown
# Slide 1 Title

Content for slide 1

---

# Slide 2 Title

Content for slide 2
```

### Built-in Themes

Marp includes themes for different presentation styles:

```markdown
---
theme: default
---

# Default Theme
Slides with light background

---

<!-- theme: beige -->

# Beige Theme
Warm, cream-colored background

---

<!-- theme: black -->
<!-- theme: invert -->

# Dark Theme
High contrast dark slides
```

### Element Classes

```markdown
<!-- _class: lead -->

# This slide has the 'lead' class
Large centered text

---

<!-- _class: two-col -->

# Two Column Layout
Left column | Right column
```

## VS Code Integration

### Setup

1. Install **Marp for VS Code** extension
2. Create a `.md` file
3. Add Marp frontmatter:

```markdown
---
marp: true
theme: default
paginate: true
---

# Your Presentation
```

4. Use keyboard shortcut `Cmd/Ctrl + Shift + P` → "Marp: Preview"

### Features in VS Code

- **Live preview** alongside markdown
- **PDF export** directly from preview
- **Slide navigation** with prev/next
- **Presenter notes** with `///`

```markdown
# Slide Title

Slide content here.

/// This text only appears in presenter mode
/// Secret notes for the speaker
```

## Configuration Options

### Frontmatter Settings

```yaml
---
marp: true
theme: default
paginate: true         # Show page numbers
footer: "My Deck"      # Footer text
backgroundColor: white # Background color
math: katex            # Math rendering
emoji: true            # Emoji support
---
```

### Global Configuration (marp.config.js)

```javascript
module.exports = {
  themes: [
    {
      name: 'my-theme',
      via: 'uncover',  // Base theme to extend
      css: `
        section {
          background-color: #1a1a2e;
          color: white;
        }
        h1 {
          color: #e94560;
        }
      `
    }
  ],
  html: true,        // Enable raw HTML
  markdown: {
    breaks: true     // Line breaks become <br>
  }
}
```

## Code Highlighting

Marp supports syntax highlighting directly in slides:

```markdown
---

# Code Example

```python
def hello():
    print("Hello, World!")
```

---

# Multiple Code Blocks

```javascript
const greeting = "Hi there";
console.log(greeting);
```
```

## Exporting

### Export Formats

| Format | Command | Use Case |
|--------|---------|----------|
| **HTML** | `marp --html presentation.md` | Web hosting |
| **PDF** | `marp --pdf presentation.md` | Printing, sharing |
| **PPTX** | `marp --pptx presentation.md` | PowerPoint users |
| **PNG** | `marp --png presentation.md` | Image slides |

### CLI Usage

```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Preview with live reload
marp --server presentation.md

# Export to all formats
marp presentation.md --html --pdf --pptx

# Watch for changes
marp presentation.md --watch --server
```

## Best Practices

### Slide Design Tips

1. **One idea per slide** — Don't cram multiple concepts
2. **Use bullet points sparingly** — Max 4-6 per slide
3. **Code is fine in small doses** — Large code blocks are hard to read
4. **Images should be high contrast** — Test on projector beforehand

### Performance Notes

- Keep presentations under 50 slides
- Large images slow down rendering — optimize first
- Use `--allow-local-files` for local image paths

## Related Concepts

- [[karpathy-llm-wiki]] — LLM educational content (good for slide material)
- [[llm-wiki]] — Language model fundamentals

## References

- [Marp Official Site](https://marp.app/)
- [Marp CLI GitHub](https://github.com/marp-team/marp-cli)
- [Marp VS Code Extension](https://github.com/marp-team/marp-vscode)
