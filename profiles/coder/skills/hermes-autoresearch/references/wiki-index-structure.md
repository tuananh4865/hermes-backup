# Wiki Index Structure — Verified 2026-05-16

**Purpose:** Correct section headers in `/Volumes/Storage-1/Hermes/wiki/index.md` for patching

## Verified Section Headers

```markdown
### AI Engineering (line ~77)
- [[vibe-coding]]
- [[viral-app-principles]]
- [[ai-engineering-roadmap]]
- [[rag]]
- [[automation]]
- [[deep-research]]
- [[fine-tuning]]
- [[synthetic-data]]
- [[apple-silicon-llm-optimization]]
- [[intelligent-wiki-roadmap]]

### TikTok Content (line ~88) ← TikTok section, NOT "TikTok Research"
- [[tiktok-algorithm-2026]]
- [[tiktok-viral-script]]
- [[epoxy-floor-prompt-template]]
- [[tiktok-captcha-solver]]
- [[tiktok-trends-2026-04-29]]
- [[tiktok-trends-2026-04-30]]
- [[gen-z-slang-2026-04]]

### Auto-Ingest (line ~97)
- [[email]]
- [[rss]]

## Projects
- [[project-management]]
- [[mistake-log]]
- [[retrospectives]]
```

## Common Mistakes

1. **WRONG:** Searching for `## TikTok Research` — this section does NOT exist
2. **WRONG:** Using `###` in patch when wiki uses `###` for section headers, not `##`
3. **WRONG:** Assuming section names without reading first

## Correct Approach

Before patching index.md:
1. Read lines 77-105 to find actual section headers
2. Use exact header text (including `###` prefix)
3. Match surrounding context for uniqueness

## Adding New Research Sections

For X research or other research, add as new `###` sections:
- Place BEFORE `### Auto-Ingest` (top of existing sections)
- OR after `### Projects` (bottom of existing sections)
- Format: `### [Research Name]` followed by `- [[page-name]] — description`

## Example: Adding Hermes X Research

```markdown
### Hermes X Research
- [[hermes-x-research-2026-05-16]] — X mentions, v0.13 features, use cases, sentiment (2026-05-16)
- [[hermes-x-research-2026-05-15]] — X mentions, v0.13 Tenacity Release, 150K stars (2026-05-15)
```

**Note:** When adding date-stamped research pages, also update `wiki/queries/` with the research content, then link from index.md.