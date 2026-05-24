---
title: Deep Research Wiki Skill
name: deep-research-wiki
description: Comprehensive research on a topic using web search, synthesis of findings, and writing a detailed wiki page with proper structure and relationships.
trigger: deep research, research a topic, deepresearch, comprehensive research, wiki research
interval: rarely
min_context: 5 tool calls
last_updated: 2026-05-23
version: 1.0.0
tags: [research, wiki, multi-step, agentic]
confidence: high
relationships: [wiki-self-heal, hermes-autoresearch, gsd-ns-ideate]
---

# Deep Research Wiki Skill

## Purpose
Research a topic thoroughly using web search, synthesize findings from multiple sources, and write a comprehensive wiki page that:
- Has proper frontmatter (title, created, updated, type, tags, confidence, relationships)
- Covers the topic comprehensively (not surface-level)
- Links to at least 2 other wiki pages
- Updates `index.md` and `log.md` after creation

## When to Use
- User asks for "deep research", "deepresearch", "research about X"
- Request requires synthesizing information from 10+ sources
- Topic is complex enough to warrant a full wiki page

## Workflow

### Phase 1: Research (Parallel Web Searches)
Run 3-5 web searches in parallel covering different angles of the topic:
```
- Main concept search
- Framework/tool-specific search  
- Comparison search
- Latest developments search
- Case studies/examples search
```

Use `mcp_MiniMax_web_search` (more reliable than exa MCP which keeps failing).
If exa MCP fails, fall back to MiniMax immediately — don't retry exa.

### Phase 2: Extract Key Content
For each promising URL, extract content with `web_extract`.
If `web_extract` fails (400/403), use browser tool as fallback.
If extraction fails entirely, note the URL in the wiki page sources but skip the content.

### Phase 3: Synthesize & Write Wiki Page
Structure the wiki page:
```
1. Executive Summary (2-3 sentences)
2. Core Concepts/Definitions
3. [Framework/Tool] Deep Dive
4. Implementation Patterns
5. Comparison Matrix (if applicable)
6. Best Practices
7. Key Insights / Takeaways
8. Sources (URLs)
```

**Frontmatter required:**
```yaml
---
title: [Topic Name]
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | comparison
tags: [tag1, tag2, tag3]
confidence: high | medium | low
relationships: [related-page-1, related-page-2]
---
```

### Phase 4: Update Navigation
After writing the wiki page:
1. Add entry to `index.md` under appropriate section
2. Append to `log.md`: `## [YYYY-MM-DD] research | [Brief description]`

### Phase 5: Report
Report to user:
- Brief summary of key findings
- Wiki page location
- Any notable gaps or things to explore further

## Pitfalls

### Exa MCP Unreachable
- **Signal:** "MCP server 'exa' is unreachable after 4 consecutive failures"
- **Fix:** Stop retrying exa, fall back to `mcp_MiniMax_web_search` immediately
- **Prevention:** Don't put exa in a retry loop — try once, fallback to MiniMax

### Web Extract Fails with 400
- **Signal:** `web_extract` returns status 400
- **Fix:** Use browser tool to navigate and read content
- **Prevention:** For known difficult sites (langchain.com, microsoft.com), use browser directly

### Wiki Page Too Long
- If page exceeds ~200 lines, split into multiple pages
- Use comparison pages for multi-framework comparisons

## Quality Gates
- [ ] At least 3 web searches covering different angles
- [ ] At least 5 sources cited
- [ ] Frontmatter complete with relationships to 2+ wiki pages
- [ ] index.md updated
- [ ] log.md updated
- [ ] Content is comprehensive (not just definitions)

## Example Output
```
Done! Research complete.

**Key Findings:**
- Supervisor pattern most common in LangGraph/CrewAI/AutoGen
- Hermes Kanban (v0.12+) enables real multi-agent collaboration
- 6 active GitHub issues on multi-agent feature gaps

**Wiki:** concepts/multi-agent-orchestrator-patterns-deep-research.md (21KB)
```

## Related Skills
- [[hermes-autoresearch]] — Nightly autonomous research (different use case: scheduled, self-initiated)
- [[wiki-self-heal]] — Wiki maintenance and link repair
- [[gsd-ns-ideate]] — Exploration and idea capture