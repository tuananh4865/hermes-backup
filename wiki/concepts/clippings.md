---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 bookmarks (extracted)
  - 🔗 reading (extracted)
  - 🔗 knowledge-management (inferred)
last_updated: 2026-04-11
tags:
  - reading
  - content
  - bookmarks
  - knowledge
---

# Clippings

> Clippings are saved excerpts from content you read — a way to capture and revisit important information.

## Overview

Clippings let you save parts of documents, articles, or books for later reference. Unlike full copies, clippings capture only the essential parts you want to remember.

## Why Clippings Matter

- **Focus**: Save only what matters, not entire documents
- **Review**: Easy to revisit key points
- **Reference**: Quick access to important quotes
- **Synthesis**: Combine clippings from multiple sources

## Tools for Clippings

### Bookmarking Services
| Service | Best For | Export |
|---------|----------|--------|
| **Pocket** | Read-later articles | HTML, JSON |
| **Instapaper** | Long-form reading | HTML |
| **Raindrop.io** | All types of content | HTML, JSON |
| **Notion** | Structured notes | Markdown |
| **Obsidian** | Markdown notes | Markdown |

### Browser Extensions
```javascript
// Example: Save to Obsidian via Templater
const saveClipping = async () => {
    const selection = window.getSelection().toString();
    const page = document.title;
    const url = window.location.href;
    
    const content = `> ${selection}\n\nSource: [${page}](${url})`;
    await navigator.clipboard.writeText(content);
};
```

## Clipping Workflow

### 1. Capture
```
User reads article → Select key passage → Save to app
```

### 2. Organize
```
Clippings → Add tags → Link to existing notes → Store
```

### 3. Review
```
Weekly review → Connect ideas → Write synthesis
```

### 4. Use
```
Reference in writing → Add to wiki → Build knowledge
```

## Clipping Formats

### Plain Text
```
"The best time to plant a tree was 20 years ago.
The second best time is now."

— Chinese Proverb
Source: Productivity blog, 2026
```

### Markdown
```markdown
> "The best time to plant a tree was 20 years ago.
> The second best time is now."
>
> — Chinese Proverb
>
> [Source](https://example.com/article)
> Tags: #productivity #motivation
```

### With Annotation
```
> "The best time to plant a tree was 20 years ago.
> The second best time is now."
>
> My note: This applies to wiki building too. Start today.
```

## Our Wiki Clippings

For our wiki, clippings become knowledge:

```markdown
## Clippings: Agentic AI

### From: Karpathy's LLM Wiki
> The real value isn't in the raw data — it's in the synthesized understanding.

### From: Anthropic Cookbook
> Claude can use tools like bash, code execution, and web search.

### From: CrewAI Blog
> Multi-agent systems outperform single agents on complex tasks.
```

## Related Concepts

- [[bookmarks]] — Saving entire pages
- [[reading]] — Reading and processing content
- [[knowledge-management]] — Organizing knowledge
- [[wiki]] — Where clippings become wiki entries

## External Resources

- [Pocket](https://getpocket.com/)
- [Instapaper](https://www.instapaper.com/)
- [Raindrop.io](https://raindrop.io/)