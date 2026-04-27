---
name: on-ingest
description: Auto-process new sources when added to wiki - extract entities, update graph, check quality
version: 1.0.0
category: automation
platforms: [macos, linux]
created: 2026-04-14
tags: [automation, ingest, entity-extraction, knowledge-graph, hooks]
requires_toolsets: [terminal]
---

# On-Ingest Hook

**Triggered automatically when a new source is added to the wiki.**

This hook ensures every new source is immediately processed, extracted, and integrated.

---

## When It Fires

**Event:** New source added to wiki

Sources include:
- Web pages (via web_extract)
- Documents
- PDFs
- Code files
- Conversations/notes

---

## The On-Ingest Workflow

### Step 1: Detect New Source

```
Check: Is this a new source (not seen before)?
If yes → Trigger on_ingest
If no → Skip
```

### Step 2: Extract Content

```
For web pages:
- web_extract(urls=["url"])

For documents:
- Read file content
- Parse relevant sections
```

### Step 3: Extract Entities

```bash
python3 ~/.hermes/projects/hermes-dojo/scripts/entity_extractor.py \
  "content" \
  --source "source_name" \
  --output /tmp/entities.json
```

### Step 4: Update Knowledge Graph

```bash
# Add entities to graph
python3 ~/.hermes/projects/hermes-dojo/scripts/knowledge_graph.py \
  --add-entity {type} {name} {confidence}
  
# Add relationships
python3 ~/.hermes/projects/hermes-dojo/scripts/knowledge_graph.py \
  --add-rel {from} {type} {to}
```

### Step 5: Quality Check

```
- Is content well-structured?
- Are there broken links?
- Is it worth saving?
- Score confidence
```

### Step 6: Update Index

```
- Add to wiki index if needed
- Create wikilinks to related pages
- Add to relevant category
```

---

## On-Ingest Template

```markdown
# Ingest: {Source Name}

**Date:** {YYYY-MM-DD}
**Source:** {URL or path}
**Type:** {web, document, pdf, code, note}

## Content Summary
{Brief summary of what the source contains}

## Entities Extracted
| Entity | Type | Confidence |
|--------|------|------------|
| | | |

## Relationships Found
| From | Type | To |
|------|------|-----|
| | | |

## Quality Check
- [ ] Content well-structured
- [ ] No broken links
- [ ] Confidence score: {X}
- [ ] Ready to publish: {Y/N}

## Actions Taken
- [ ] Entities added to graph
- [ ] Relationships added
- [ ] Wiki index updated
- [ ] Wikilinks created
```

---

## Example: Web Page Ingest

```
1. User shares URL: https://example.com/article

2. Hook triggers: on_ingest

3. Content extracted:
   web_extract → markdown content

4. Entities extracted:
   - Company: Example Inc
   - Product: Example Product
   - Technology: React

5. Graph updated:
   - [Company] Example Inc
   - [Product] Example Product  
   - [Library] React (uses)
   - Example Inc → owns → Example Product

6. Index updated:
   - Created: companies/example-inc.md
   - Linked to: technology/react.md
```

---

## Quality Thresholds

| Content Type | Min Score | Auto-Publish |
|--------------|-----------|--------------|
| Concept | 7.0 | Yes |
| Tutorial | 7.5 | Yes |
| Research | 8.0 | No (needs review) |
| Deep Dive | 8.5 | No (needs review) |

---

## Integration

- Use [[entity-extraction]] — Extract entities
- Use [[graph-query]] — Update graph
- Use [[wiki-quality-score]] — Quality check
- Use [[wiki_hooks.py]] — The hook engine

---

## Related

- [[on-session-start]] — Session context loading
- [[on-session-end]] — Session compression
- [[on-schedule]] — Periodic maintenance
- [[entity-extraction]] — Entity extraction
- [[wiki_hooks.py]] — Hook engine
