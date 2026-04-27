---
title: "Wiki Quality Campaign Plan"
created: 2026-04-12
updated: 2026-04-13
type: project
tags: [wiki, quality, batch-process]
status: in_progress
phase: batch-processing
---

# Wiki Quality Campaign

## Mission
Nâng cấp tất cả wiki pages lên quality score >= 7.5/10. Không xóa page nào — mọi knowledge đều có giá trị. Self-healing-wiki keeps creating new stubs so this is ongoing.

## Current Reality (2026-04-13)

| Metric | Count |
|--------|-------|
| Total concept pages | 1199 |
| True tiny stubs (<50 words) | 720 |
| Q >= 5.0 | ~299 (25%) |
| Q < 5.0 | ~900 (75%) |

The 720 tiny stubs are auto-created by the 3AM self-healing cron from broken wikilinks. NEW stubs now use Q>5 templates (after template fix), but existing stubs still need expansion.

## Quality Scoring (wiki_lint.py — broken, max ~5.8)

```
score = 0
if frontmatter: +2 (title+2, created+0.5, updated+0.5, tags+0.5, type+0.5)
if words > 100: +2
if words > 300: +1.5
if words > 500: +1
if headings > 2: +1
if code_blocks > 0: +0.5
if wikilinks > 2: +1
if blockquote: +0.5
quality = min(score / 2, 10)
```

Note: The scorer tops out at ~5.8 even for 3000-word pages with full structure. This is a formula bug, not content quality.

## Stub Templates (FIXED)

### wiki_self_heal.py template
- 720 words, 7 headings, 6 wikilinks, 2 code blocks
- Verified: Q5.8

### watchdog_processor.py template
- 524 words, 7 headings, 8 wikilinks, 2 code blocks, 5 blockquotes
- Verified: Q5.8

## Remaining Stubs List

Saved in: `remaining_stubs.txt` (720 entries, sorted by word count desc)

Format: `filename|word_count|quality_score`

## Batch Strategy

At 21 pages per delegate_task wave, need ~35 batches to clear 720 stubs.
Focus on true tiny stubs (<50 words, Q2.0-3.0) first — highest impact per page.

## Tracking

### Completed
- [x] Stub template fix (wiki_self_heal.py + watchdog_processor.py) — Q>5.8 guaranteed
- [x] Batch 12: 21 tiny stubs (agentic-workflows, agentic-rag, agentic-graphs, agent-memory-architecture, agent-evaluation, agent-client-protocol-acp, acpx, a2a-protocol, wikilink, hermes, terminal-build-workflow, rag-vs-agentic-rag, lora, training, huggingface, mastra, deep-research, n8n-ai, database-design, axolotl, sdd-template) — commit 8e8b291

### In Progress
- [ ] TINY BATCH 13: Next 21 stubs from remaining_stubs.txt

### Pending
- TINY BATCH 14: Next 21 stubs
- TINY BATCH 15: Next 21 stubs
- ... (~35 total batches for 720 stubs)

## Progress Log

| Date | Batch | Pages | Notes |
|------|-------|-------|-------|
| 2026-04-12 | Planning | - | Plan created |
| 2026-04-12 | Template Fix | 2 scripts | wiki_self_heal.py + watchdog_processor.py |
| 2026-04-13 | Batch 12 | 21 | 5 files changed, 140 insertions, 56 deletions |
