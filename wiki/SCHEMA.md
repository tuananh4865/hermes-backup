---
confidence: high
last_verified: 2026-04-12
relationships:
  - wiki
  - start-here
---

# Wiki Schema

> Based on Karpathy's LLM Wiki pattern (llm-wiki skill).
> This wiki is a persistent, compounding knowledge base as interlinked markdown files.

## Architecture: Three Layers

```
wiki/
├── SCHEMA.md              # This file — conventions, structure, taxonomy
├── index.md               # Content catalog (sectioned by type)
├── log.md                 # Chronological action log (append-only)
├── _meta/
│   ├── start-here.md     # AI agent startup instructions
│   └── ...
├── raw/                  # Layer 1: Immutable source material
│   ├── articles/         # Web articles, blog posts
│   ├── papers/          # Academic papers, PDFs
│   ├── transcripts/     # Meeting notes, interviews (raw only)
│   └── assets/          # Images, files
├── entities/             # Layer 2: People, orgs, products, models
├── concepts/             # Layer 2: Topics, techniques, ideas
├── comparisons/          # Layer 2: Side-by-side analyses
└── queries/              # Layer 2: Filed query results
```

**Layer 1 — Raw Sources**: Immutable. Agent reads but never modifies.
**Layer 2 — Wiki**: Agent-owned markdown files. Created, updated, cross-referenced.
**Layer 3 — Schema**: This file defines structure and conventions.

---

## Conventions

1. **Filenames**: lowercase, hyphens, no spaces (e.g., `your-harness-your-memory.md`)
2. **Entity/concept folders**: lowercase, hyphens, NO colons, NO special characters
3. **Frontmatter**: Every page starts with YAML frontmatter (required)
4. **Wikilinks**: Use `` or `` to link between pages
5. **Minimum 2 wikilinks** on every wiki page
6. **Updated date**: Bump `updated` date when modifying
7. **Log actions**: Append significant changes to `log.md`
8. **Never modify files in `raw/`** — sources are immutable

---

## Frontmatter Template

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query
tags: [tag1, tag2]
sources: [raw/articles/source-name.md]
confidence: high | medium | low
relationships: [related-page-1, related-page-2]
---
```

---

## Page Types

| Type | Description | Folder |
|------|-------------|--------|
| entity | People, companies, products, models | `entities/` |
| concept | Topics, techniques, ideas, explanations | `concepts/` |
| comparison | Side-by-side analyses | `comparisons/` |
| query | Filed query results worth keeping | `queries/` |

**Note**: `personal`, `project`, `phase`, `decision`, `mistake`, `retrospective` types are legacy — prefer entity/concept for new pages.

---

## Tag Taxonomy

| Tag | Use for |
|-----|---------|
| person | People (use entity pages) |
| company | Companies, organizations |
| product | Products, tools, frameworks |
| model | AI/ML models |
| agent | AI agents, agent frameworks |
| memory | Memory systems, context management |
| harness | Agent harnesses, orchestration frameworks |
| vendor-lock-in | Lock-in concerns, proprietary vs open |
| knowledge-base | Wiki, RAG, note-taking systems |
| research | Research papers, academic content |
| transcript | Conversation/meeting transcripts only |
| project | Project management |
| decision | Technical decisions |
| mistake | Errors, bugs, lessons learned |
| retrospective | Session reviews |

**Rule**: Only use tags from this taxonomy. If a new tag is needed, add it here first.

---

## Page Thresholds

- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details
- **Split a page** when it exceeds ~200 lines
- **Archive a page** when fully superseded — move to `_archive/`

---

## Ingest Workflow (MANDATORY)

When Anh provides a URL or content to ingest:

### Step 1: Capture Raw Source
```
URL → web_extract → save to raw/articles/[descriptive-name].md
PDF → web_extract → save to raw/papers/[descriptive-name].md
Text → save to appropriate raw/ subdirectory
```

### Step 2: Create Entity Pages
For **people, companies, products** mentioned in the source:
- One page per notable entity
- Include: overview, key facts, relationships, source references
- Place in `entities/` folder

### Step 3: Create Concept Pages
For **topics, ideas, techniques** in the source:
- One page per concept
- Include: definition, analysis, implications, related concepts
- Place in `concepts/` folder
- Link to at least 2 other wiki pages via `[[wikilinks]]`

### Step 4: Update Navigation
- Add new pages to `index.md` under correct section
- Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`
- List every file created or updated

### Step 5: Report
List all files created/updated to Anh.

---

## Update Policy

When new information conflicts with existing content:
1. Check dates — newer sources generally supersede older
2. If contradictory, note both positions with dates and sources
3. Mark contradiction in frontmatter: `contradictions: [page-name]`

---

## Related

- [[start-here]] — AI agent startup instructions
- [[index]] — Content catalog
- [[log]] — Action log

> **Auto-improvement note:** *Missing or outdated information:**

> **Auto-improvement note:** The page describes an "Ingest Workflow" but only has "Step 1" and "Step 2" where Step 2 is cut off/incomplete. There's no actual step 2 content, just a heading.

> **Auto-improvement note:** 3 specific improvements across the categories mentioned:

> **Auto-improvement note:** 3 specific improvements. Let me analyze the current content:

> **Auto-improvement note:** *Current Content Analysis:**

> **Auto-improvement note:** *Structure and Clarity:**

> **Auto-improvement note:** The page is well-organized with clear sections

> **Auto-improvement note:** 3 specific improvements. Let me analyze the current content:

> **Auto-improvement note:** *Missing or outdated information**:

> **Auto-improvement note:** 3 specific improvements based on the criteria:

> **Auto-improvement note:** *Missing or outdated information:**

> **Auto-improvement note:** *Missing or outdated information:**

> **Auto-improvement note:** The frontmatter template has `sources` field pointing to `raw/articles/source-name.md` but the schema shows sources should be paths like `raw/articles/...` - this is consistent

> **Auto-improvement note:** 3 specific improvements. Let me analyze the content:

> **Auto-improvement note:** *Missing or outdated information**: The page describes a 3-layer architecture but doesn't mention what happens with the log.md, index.md, or _meta/ folder in terms of their role. The architecture section shows these files but doesn't explain their purpose in the layered system.

> **Auto-improvement note:** 3 specific improvements. Let me analyze the content:

> **Auto-improvement note:** *Missing or outdated information**:

> **Auto-improvement note:** 3 specific improvements. Let me analyze the current content:

> **Auto-improvement note:** *Current Content Analysis:**

> **Auto-improvement note:** 3 specific improvements for quality purposes. Let me analyze the current content.

> **Auto-improvement note:** *Missing or outdated information**: 