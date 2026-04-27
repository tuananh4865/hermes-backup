---
name: entity-extraction
description: Extract structured entities from raw sources - Person, Project, Library, Concept, File, Decision with relationships
version: 1.0.0
category: lifecycle
platforms: [macos, linux]
created: 2026-04-14
tags: [entity-extraction, knowledge-graph, structured-data, parsing]
requires_toolsets: [terminal]
---

# Entity Extraction

**Transform raw sources into structured knowledge.**

This skill extracts typed entities and relationships from text, feeding the knowledge graph.

---

## Entity Types

| Type | Attributes | Examples |
|------|------------|----------|
| Person | name, role | Tuấn Anh (user) |
| Project | name, status | Hermes Dojo (active) |
| Library | name, version, language | React, Python |
| Concept | name, definition | Knowledge Graph |
| File | path, type | src/app.py |
| Decision | title, date, rationale | API choice, DB schema |

---

## Relationship Types

| Type | Direction | Example |
|------|-----------|---------|
| `uses` | A → B | Project uses Library |
| `depends_on` | A → B | A depends on B |
| `contradicts` | A → B | A contradicts B |
| `caused` | A → B | Bug caused Error |
| `fixed` | A → B | PR fixed Issue |
| `supersedes` | A → B | New replaces Old |
| `owns` | Person → Project | Person owns Project |
| `related_to` | A → B | General relationship |

---

## The Extraction Workflow

### Step 1: Choose Source Type

```
Source types:
- Web page → Use web_extract first
- PDF → Use web_extract with PDF URL
- Code → Use grep + manual
- Conversation → Manual extraction
- Document → Use web_extract or manual
```

### Step 2: Extract Raw Content

```bash
# For web pages
web_extract(urls=["https://..."])

# Returns markdown content
```

### Step 3: Run Entity Extractor

```bash
python3 ~/.hermes/projects/hermes-dojo/scripts/entity_extractor.py \
  "text content here" \
  --source "source name" \
  --output entities.json
```

### Step 4: Review and Refine

```
Review extracted entities:
- Are names correct?
- Are types appropriate?
- Are relationships accurate?
- Any missing entities?

Manual corrections if needed.
```

### Step 5: Load into Graph

```bash
# Add entities to knowledge graph
python3 ~/.hermes/projects/hermes-dojo/scripts/knowledge_graph.py \
  --init

# Add entities
python3 ~/.hermes/projects/hermes-dojo/scripts/knowledge_graph.py \
  --add-entity Person "Tuấn Anh" 0.8

# Add relationships
python3 ~/.hermes/projects/hermes-dojo/scripts/knowledge_graph.py \
  --add-rel "Tuấn Anh" owns "Hermes Dojo"
```

---

## Manual Extraction

For sources that need human judgment:

```markdown
## Entities Found

### Persons
1. **Name:** Tuấn Anh
   - Role: User
   - Relationship: owns Hermes Dojo

### Projects
1. **Name:** Hermes Dojo
   - Status: active
   - Relationship: owned_by Tuấn Anh

### Concepts
1. **Name:** Knowledge Graph
   - Definition: Structured entity storage
   - Relationship: used_by Hermes Dojo
```

---

## Quality Checklist

- [ ] All entities have correct types
- [ ] All entities have names
- [ ] Relationships are directional
- [ ] No duplicate entities
- [ ] Source is documented
- [ ] Confidence scores assigned

---

## Confidence by Source

| Source Type | Initial Confidence |
|-------------|-------------------|
| Official docs | 0.9 |
| Article | 0.7 |
| Conversation | 0.5 |
| Guess | 0.3 |

---

## Integration

- Use [[knowledge_graph.py]] — Store extracted entities
- Use [[graph-query]] — Query the graph later
- Use with [[research-command]] — Research extracts entities

---

## Related

- [[graph-query]] — Query extracted entities
- [[knowledge_graph.py]] — Graph storage script
- [[entity_extractor.py]] — Extraction tool
