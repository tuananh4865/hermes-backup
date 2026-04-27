---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 intelligent-wiki-roadmap (extracted)
  - 🔗 self-healing-wiki (extracted)
  - 🔗 project-tracker (extracted)
  - 🔗 knowledge-base (extracted)
relationship_count: 4
---

# Intelligent Wiki Architecture

## Tổng Quan

Transform wiki từ **passive storage** thành **autonomous knowledge agent** — một hệ thống có memory riêng, tự quản lý lifecycle của kiến thức, và liên tục self-improve.

## Core Memory Architecture

Hệ thống sử dụng **4 loại memory** như agentic AI systems:

### 1. Episodic Memory (Raw Transcripts)
- **Location**: `raw/transcripts/{date}/`
- **Purpose**: Lưu lại toàn bộ conversation history — "những gì đã xảy ra"
- **Properties**: Immutable, timestamped, full context
- **Access**: Sequential read cho context building

### 2. Semantic Memory (Concept Pages)
- **Location**: `concepts/`
- **Purpose**: Lưu processed knowledge — "những gì ta biết"
- **Properties**: Structured, linked, versioned
- **Access**: Random read theo wikilinks

### 3. Procedural Memory (Scripts & Automation)
- **Location**: `scripts/`
- **Purpose**: Lưu "cách làm" — automation recipes
- **Properties**: Executable, composable
- **Access**: Import và execute

### 4. Working Memory (Project State)
- **Location**: `concepts/project-tracker.md`
- **Purpose**: Lưu current task state — "đang làm gì"
- **Properties**: Checkpointed, incrementally updated
- **Access**: Read/write per session

## Knowledge Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CAPTURE   │────▶│  PROCESS    │────▶│   ORGANIZE  │
│  raw/ feed  │     │  transcripts│     │  concepts/  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
┌─────────────┐     ┌─────────────┐           ▼
│  RETRIEVE   │◀────│   REASON    │◀────┌─────────────┐
│  on-demand  │     │  synthesize │     │   EVOLVE    │
└─────────────┘     └─────────────┘     │ self-improve│
                                        └─────────────┘
```

### Capture (Input)
- **Transcripts**: Passive capture via Hermes hook
- **Bookmarks**: Web clipping via bookmarklet
- **Email**: Email forwarding to wiki
- **RSS**: Auto-ingest từ feeds

### Process (Parse & Understand)
- Extract key concepts từ raw content
- Identify relationships (supports, contradicts, builds-on)
- Flag confidence level

### Organize (Structure)
- Create/update concept pages
- Add wikilinks to related concepts
- Update frontmatter (timestamp, tags, type)
- Merge duplicates, archive obsolete

### Evolve (Self-Improve)
- Detect knowledge gaps
- Generate missing content
- Self-critique quality
- Update stale content

## Memory Management Patterns

### Lightweight ≠ Token-Heavy

1. **Compression at Storage**: Store raw, compress semantic
2. **Retrieval by Need**: Don't load full wiki, load relevant subset
3. **Summarize Old Context**: Older transcripts → condensed summaries
4. **Selective Retention**: Not everything needs to be in semantic memory

### Context Building for Agents

```
Session Start:
  1. Read project-tracker.md (current state)
  2. Read recent transcripts (last 7 days)
  3. Read related concept pages (by tags)
  4. Build context window
  
Session End:
  1. Update project-tracker.md
  2. Archive processed transcripts
  3. Commit to GitHub
```

## Project Management Integration

### Why Project Tracking Matters

Dự án dài hơi sẽ mất context nếu:
- Agent restart giữa chừng
- Switch sang task khác rồi quay lại
- Wiki không track được "đang làm gì, đã làm gì"

### Solution: Structured Project State

```yaml
# project-tracker.md
---
current_project: intelligent-wiki-architecture
phase: 2  # Architecture design
status: in_progress
checkpoints:
  - id: phase-1-complete
    date: 2026-04-09
    summary: Cleanup & refactor done
  - id: phase-2-start
    date: 2026-04-09
    summary: Architecture design
    pending_tasks: [...]
next_action: Design memory management
blocked_by: none
```

### Checkpoint Pattern

Mỗi khi完成任务 quan trọng:
1. Append checkpoint vào project state
2. Update pending/completed tasks
3. Note blockers và dependencies
4. Commit to GitHub

→ Agent sau có thể resume ngay lập tức

## Self-Healing & Self-Evolving

### Self-Healing (Current)

| Issue | Detection | Fix |
|-------|-----------|-----|
| Broken links | wiki_lint.py | Auto-fix or create stub |
| Missing frontmatter | wiki_lint.py | Auto-add defaults |
| Stale pages | Age > 30 days | Flag for review |
| Orphan pages | No links | Suggest connections |

### Self-Evolving (Next)

| Capability | Pattern | Implementation |
|-----------|---------|----------------|
| Merge Duplicates | Same content in 2 pages | Merge with redirect |
| Update Stale | Source URL changed | Fetch new content |
| Gap Filling | Mentioned but undefined | Generate stub + LLM expand |
| Contradiction | Same fact, different claims | Flag for human review |
| Outdate Detection | "recent" for old info | Replace with dated version |

## Architecture Diagram

```
                    ┌──────────────────┐
                    │   HERMES AGENT    │
                    │  (this system)    │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  INPUT HANDLERS │  │  KNOWLEDGE BASE │  │  AGENT SCRIPTS  │
│                 │  │                 │  │                 │
│ •transcript hook│  │ •concepts/      │  │ •wiki_lint.py   │
│ •bookmarklet    │  │ •raw/           │  │ •wiki_self_*    │
│ •email forward  │  │ •scripts/       │  │ •wiki_auto_*    │
│ •RSS ingest     │  │                 │  │                 │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                    GIT SYNC                            │
│            (commit after every action)                  │
└─────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   GITHUB REPO   │
                    │  (offsite backup)│
                    └─────────────────┘
```

## Implementation Roadmap

### Phase 1: Foundation (Done ✅)
- [x] Wiki structure established
- [x] Auto-ingest scripts
- [x] Self-healing scripts (wiki_lint.py, wiki_self_heal.py)
- [x] Weekly cron job

### Phase 2: Architecture (Current)
- [ ] Design memory management system
- [ ] Implement project state tracking
- [ ] Add checkpoint pattern
- [ ] Create knowledge lifecycle management

### Phase 3: Intelligence
- [ ] Gap detection & auto-fill
- [ ] Duplicate merging
- [ ] Contradiction detection
- [ ] Self-critique improvement

### Phase 4: Autonomy
- [ ] Autonomous content generation
- [ ] Self-improvement feedback loop
- [ ] Evolution tracking

## Related

- [[intelligent-wiki-roadmap]] — Detailed implementation roadmap
- [[self-healing-wiki]] — Self-healing capabilities
- [[project-tracker]] — Current project state
- [[knowledge-base]] — Knowledge management patterns
