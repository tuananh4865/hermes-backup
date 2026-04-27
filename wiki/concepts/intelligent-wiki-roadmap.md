---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 intelligent-wiki-architecture (extracted)
  - 🔗 project-tracker (extracted)
  - 🔗 self-healing-wiki (extracted)
  - 🔗 knowledge-base (extracted)
relationship_count: 4
---

# Intelligent Wiki — Self-Evolution Roadmap

## Vision

Transform wiki từ passive storage thành **autonomous knowledge agent** — tự xử lý thông tin như con người: hiểu context, phát hiện lỗi, tự cập nhật kiến thức lỗi thời, và liên tục nâng cấp chính nó.

**Core principle**: Lightweight, không ngốn token, truy xuất thông minh.

---

## Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  WORKING MEMORY         │  Current state checkpoint         │
│  (project-tracker.md)   │  What I'm doing, next, blockers   │
├─────────────────────────────────────────────────────────────┤
│  EPISODIC MEMORY        │  Full conversation history        │
│  (raw/transcripts/)    │  Immutable, timestamped          │
├─────────────────────────────────────────────────────────────┤
│  SEMANTIC MEMORY        │  Processed knowledge             │
│  (concepts/)           │  Structured, linked, versioned    │
├─────────────────────────────────────────────────────────────┤
│  PROCEDURAL MEMORY     │  Automation recipes              │
│  (scripts/)            │  Executable, composable          │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Foundation ✅ (Done 2026-04-09)

**Goal:** Wiki tự phát hiện và tự sửa lỗi của chính mình

| Task | Status | Script |
|------|--------|--------|
| Broken link detector | ✅ Done | wiki_lint.py |
| Missing frontmatter filler | ✅ Done | wiki_self_heal.py |
| Stale page detector | ✅ Done | wiki_lint.py |
| Orphan page detector | ✅ Done | wiki_lint.py |
| Weekly cron job | ✅ Done | Monday 9AM |

### Phase 2: Memory & State Management 🔄 (In Progress)

**Goal:** Agent không bao giờ mất context

| Task | Status | Script |
|------|--------|--------|
| Project state manager | ⬜ TODO | project_state.py |
| Transcript summarizer | ⬜ TODO | summarize_transcript.py |
| Checkpoint pattern | ⬜ TODO | in project-tracker.md |
| Context builder | ⬜ TODO | build_context.py |

**Key Scripts:**

```python
# scripts/project_state.py
class ProjectState:
    def checkpoint(self, action, next_action, blockers):
        """Save checkpoint before major actions"""
        
    def get_recent_context(self, days=7):
        """Build context from recent transcripts + project state"""
        
    def get_current_phase(self):
        """Get current project phase and pending tasks"""
```

### Phase 3: Knowledge Lifecycle 🔜 (Next)

**Goal:** Tự động quản lý lifecycle của kiến thức

| Task | Status | Script |
|------|--------|--------|
| Duplicate detector | ⬜ TODO | duplicate_detector.py |
| Staleness scorer | ⬜ TODO | freshness_score.py |
| Contradiction detector | ⬜ TODO | contradiction_detector.py |
| Archive obsolete pages | ⬜ TODO | archive_old.py |

### Phase 4: Self-Evolution 🔜 (Later)

**Goal:** Wiki chủ động học, tự tạo content mới

| Task | Status | Script |
|------|--------|--------|
| Gap detector | ⬜ TODO | gap_detector.py |
| Auto content generator | ⬜ TODO | generate_content.py |
| Self-critique improvement | ⬜ TODO | self_critique.py |
| Evolution tracker | ⬜ TODO | evolution_tracker.py |

---

## Knowledge Lifecycle Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CAPTURE   │────▶│  PROCESS    │────▶│   ORGANIZE  │
│  raw/ feed  │     │  summarize  │     │  concepts/  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
┌─────────────┐     ┌─────────────┐           ▼
│  RETRIEVE   │◀────│   REASON    │◀────┌─────────────┐
│  on-demand  │     │  synthesize │     │   EVOLVE    │
└─────────────┘     └─────────────┘     │ self-improve│
                                        └─────────────┘
```

### States

| State | Location | Purpose |
|-------|----------|---------|
| raw | raw/transcripts/ | Original capture, immutable |
| summarized | raw/.summarized/ | Condensed for old transcripts |
| draft | concepts/.draft/ | Being generated |
| published | concepts/ | Final knowledge |
| archived | concepts/.archived/ | Obsolete, kept for history |

---

## Project State Tracking

### Checkpoint Format

```yaml
checkpoints:
  - id: cp-001
    timestamp: 2026-04-09T12:00:00+07:00
    phase: phase-2-architecture
    action: "Designed intelligent wiki architecture"
    next_action: "Implement project_state.py"
    blockers: []
    artifacts:
      - concepts/intelligent-wiki-architecture.md
```

### Context Building Pattern

```
Session Start:
  1. Read project-tracker.md → current state
  2. Read recent transcripts (7 days) → what happened
  3. Read related concepts (by tags) → relevant knowledge
  4. Build context window → composite prompt
  
Session End:
  1. checkpoint() → save state
  2. Update pending tasks
  3. Commit to GitHub → persist
```

---

## Immediate Next Steps

### Today

1. [ ] Create `scripts/project_state.py`
2. [ ] Create `scripts/summarize_transcript.py`
3. [ ] Update `project-tracker.md` with checkpoint pattern
4. [ ] Create `scripts/duplicate_detector.py`

### This Week

5. [ ] Implement freshness scoring
6. [ ] Setup knowledge lifecycle states
7. [ ] Update cron to include self-improve

### Configuration

- **LM Studio:** 192.168.0.187:1234
- **Default Model:** mlx-qwen3.5-0.8b-claude-4.6-opus-reasoning-distilled
- **Copyist Model:** qwen3.5-2b-mlx
- **GitHub:** github.com/tuananh4865/my-llm-wiki
- **Cron:** Monday 9AM

## Related

- [[intelligent-wiki-architecture]] — Architecture details
- [[project-tracker]] — Current project state
- [[self-healing-wiki]] — Self-healing capabilities
- [[knowledge-base]] — Knowledge management patterns
