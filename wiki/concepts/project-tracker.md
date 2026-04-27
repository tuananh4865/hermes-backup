---
title: "Wiki Enhancement Project Tracker"
created: 2026-04-08
updated: 2026-04-09
type: project
tags: [project, tracker, wiki-enhancement, intelligent-wiki]
---

# Wiki Enhancement Project Tracker

## Project: Transform Wiki into Autonomous Knowledge Agent

**Started:** 2026-04-08
**Last Updated:** 2026-04-09
**Status:** Phase 2 - Architecture Design

---

## Current Phase: Phase 2 - Intelligent Architecture

### Phase 2 Tasks

| Task | Status | Priority | Notes |
|------|--------|----------|-------|
| Design memory architecture | 🔄 IN PROGRESS | This document |
| Implement project state tracking | ⬜ TODO | Checkpoint pattern |
| Create transcript summarizer | ⬜ TODO | Compress old transcripts |
| Add duplicate detector | ⬜ TODO | Merge similar pages |
| Implement contradiction detector | ⬜ TODO | Flag conflicts |

### Phase 1 Completed (2026-04-09)

| Task | Status | Notes |
|------|--------|-------|
| Wiki cleanup & refactor | ✅ DONE | 54→26 concepts, 0 broken links |
| Auto-ingest scripts | ✅ DONE | bookmarklet, email, RSS |
| Self-healing scripts | ✅ DONE | wiki_lint, wiki_self_heal |
| Weekly cron job | ✅ DONE | Monday 9AM |

---

## Architecture: Memory Management

### Problem Statement

Agent lose context when:
1. Restart mid-task
2. Switch tasks and return later
3. Wiki doesn't track "what was I doing?"

### Solution: Structured Memory Layers

```
┌─────────────────────────────────────────────────────────────┐
│  WORKING MEMORY (project-tracker.md)                       │
│  Current state: what I'm doing, what's next, blockers     │
├─────────────────────────────────────────────────────────────┤
│  EPISODIC MEMORY (raw/transcripts/)                        │
│  Full conversation history - immutable, timestamped          │
├─────────────────────────────────────────────────────────────┤
│  SEMANTIC MEMORY (concepts/)                              │
│  Processed knowledge - structured, linked, versioned      │
├─────────────────────────────────────────────────────────────┤
│  PROCEDURAL MEMORY (scripts/)                              │
│  How-to knowledge - automation recipes, executable         │
└─────────────────────────────────────────────────────────────┘
```

### Implementation: Checkpoint Pattern

```yaml
# Checkpoint format in project-tracker.md
checkpoints:
  - id: cp-20260409135927
    timestamp: 2026-04-09T13:59:27+07:00
    action: "Phase 4 complete - self-evolution agent tested"
    next_action: "Phase 5: cross-agent coordination"
    blockers: []
    phase: phase-4-done

  - id: cp-20260409132048
    timestamp: 2026-04-09T13:20:48+07:00
    action: "Created duplicate_detector.py freshness_score.py contradiction_detector.py"
    next_action: "Update cron with self-improve + contradiction check"
    blockers: []
    phase: phase-3-knowledge-lifecycle

  - id: cp-20260409125337
    timestamp: 2026-04-09T12:53:37+07:00
    action: "Researched agentic memory systems, created intelligent wiki architecture"
    next_action: "Implement duplicate_detector.py, update cron with self-improve"
    blockers: []
    phase: phase-2-architecture

  - id: checkpoint-001
    timestamp: 2026-04-09T12:00:00+07:00
    phase: phase-2-architecture
    action: "Designed intelligent wiki architecture"
    next_action: "Implement memory management scripts"
    blockers: []
    artifacts:
      - concepts/intelligent-wiki-architecture.md
      - concepts/intelligent-wiki-roadmap.md
```

### Script: Project State Manager

**Purpose**: Manage project state across sessions

```python
# scripts/project_state.py
class ProjectState:
    def __init__(self, wiki_path):
        self.tracker = wiki_path / "concepts/project-tracker.md"
    
    def checkpoint(self, action: str, next_action: str, blockers: List[str]):
        """Save current state as checkpoint"""
        
    def get_recent_context(self, days: int = 7) -> str:
        """Build context from recent transcripts"""
        
    def get_current_phase(self) -> Dict:
        """Get current project phase and tasks"""
        
    def update_task_status(self, task_id: str, status: str):
        """Update task status in project tracker"""
```

---

## Knowledge Lifecycle Management

### 1. Capture → Process → Organize → Evolve

```python
# Knowledge lifecycle tracking
knowledge_states = {
    "raw": "raw/transcripts/",           # Original capture
    "processing": "raw/.processing/",    # Being processed
    "draft": "concepts/.draft/",        # LLM generating
    "published": "concepts/",           # Final knowledge
    "archived": "concepts/.archived/",  # Obsolete, kept for history
}
```

### 2. Duplicate Detection & Merge

**Algorithm**:
1. Find pages with similar titles (Levenshtein distance < 3)
2. Find pages with >50% content overlap
3. Find pages linking to each other (circular references)

**Merge Strategy**:
- Keep newer page, archive older
- Or combine into single comprehensive page
- Redirect all links from archived page

### 3. Staleness Detection

**Freshness Score** = f(time_since_update, source_change_rate, topic_velocity)

```python
def freshness_score(page: Path) -> float:
    age = days_since_update(page)
    source_changes = check_source_urls(page)
    topic_velocity = change_frequency(page.topic)
    
    # Penalize old, reward active
    return (1 / (1 + age * 0.1)) * source_changes * topic_velocity
```

### 4. Contradiction Detection

**Pattern**: Same claim stated differently across pages

```python
# Flag for human review when:
# - Page A claims "X is true"
# - Page B implies "X may not be true"
# → Add to contradiction log
```

---

## Transcript Summarization

### Problem

Old transcripts (30+ days) still take full token space when building context.

### Solution: Progressive Summarization

```
Day 0-7:    Full transcript (raw/transcripts/{date}/)
Day 8-30:   Condensed (200 word summary + key decisions)
Day 31+:    Indexed only (title, date, key outcomes, linked concepts)
```

**Implementation**:

```python
# scripts/summarize_transcript.py
def summarize_transcript(transcript_path: Path) -> Dict:
    """Generate condensed summary from full transcript"""
    return {
        "title": extract_title(transcript),
        "date": extract_date(transcript),
        "key_decisions": extract_decisions(transcript),
        "topics_discussed": extract_topics(transcript),
        "outcomes": extract_outcomes(transcript),
        "linked_concepts": extract_links(transcript),
        "word_count": len(transcript.words)
    }
```

---

## Next Actions (This Week)

### Immediate (Today)

1. [ ] Create `scripts/project_state.py` — Project state manager
2. [ ] Create `scripts/summarize_transcript.py` — Transcript summarizer  
3. [ ] Create `scripts/duplicate_detector.py` — Find merge candidates
4. [ ] Update `project-tracker.md` with checkpoint pattern

### This Week

5. [ ] Setup knowledge lifecycle tracking
6. [ ] Implement freshness scoring
7. [ ] Add contradiction detection
8. [ ] Update cron to run self-heal + auto-improve

### Next Month

9. [ ] Phase 3: Gap detection & auto-fill
10. [ ] Phase 4: Autonomous content generation

---

## Configuration

- **Default Model:** `mlx-qwen3.5-0.8b-claude-4.6-opus-reasoning-distilled`
- **LM Studio URL:** `http://192.168.0.187:1234`
- **GitHub Repo:** `github.com/tuananh4865/my-llm-wiki`
- **Weekly Lint Cron:** Monday 9AM (job_id: 2edad9dcad43)
