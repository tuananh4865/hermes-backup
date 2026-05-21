# Mem0 Architecture + WikiMemoryProvider Hybrid Plan

**Created:** 2026-05-21  
**Purpose:** Long-term memory system upgrade — Mem0-style retrieval + WikiMemoryProvider persistence

---

## Mem0 Architecture (Key Learnings)

### 3-Signal Retrieval Pipeline

```
Query → Semantic (vector) + BM25 (keyword) + Entity Graph (entity boost)
         ↓
    RRF Fusion → Combined score per memory
```

| Signal | Purpose | Mem0 Benchmark |
|--------|---------|----------------|
| Semantic (vector) | Conceptual queries | Primary for "what does user think about X" |
| BM25 keyword | Factual/exact matches | Primary for "what meetings last week" |
| Entity graph | Entity-centric retrieval | Boost when query mentions entities |

**Result:** 91.6% LoCoMo (new v2) vs 68.5% (old v1)

### ADD-Only Extraction (No Forget)

```
New conversation → LLM extracts "candidate facts" →
Compare with existing → ADD / UPDATE / DELETE / NOOP
```

**Key:** Memories accumulate — nothing overwritten. When facts contradict, BOTH survive. Temporal context preserved.

### Entity Linking

```
Entity: "Tuấn Anh" → linked memories [preferences, workflows, skills, decisions]
When querying → entity boost pulls ALL related memories
```

### Memory Layers

| Layer | Lifetime | Use |
|-------|----------|-----|
| Conversation | Single turn | Tool calls, intermediate calcs |
| Session | Minutes-hours | Current task |
| User | Weeks-forever | Preferences, facts |
| Org | Configured | Shared team knowledge |

---

## WikiMemoryProvider Current State

| Đã có | Cần thêm |
|-------|----------|
| ✅ Hybrid BM25 + n-gram (RRF) | ❌ Real vector embeddings |
| ✅ Structured USER.md (6 sections) | ❌ Entity graph / linking |
| ✅ Entity extraction (regex patterns) | ❌ LLM-powered fact extraction |
| ✅ Session start topic parsing | ❌ Temporal bi-temporal model |
| ✅ Importance scoring | ❌ Self-evolution loop |
| ✅ Rolling checkpoint | |
| ✅ Episode logging | |
| ✅ Git push sync | |

---

## Option A: Phase 1 — Vector Embeddings (Tuần này)

### Install

```bash
pip install sentence-transformers faiss-cpu numpy scikit-learn
# Model: sentence-transformers/all-MiniLM-L6-v2 (fast) hoặc Qwen3-0.6B (local)
```

### Add to WikiMemoryProvider

**New file:** `plugins/memory/wiki/embeddings.py`

```python
from sentence_transformers import SentenceTransformer

class LocalEmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        
    def encode(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True)
```

### Replace `_semantic_search()` (current: n-gram) with real vector search

```python
def _semantic_vector_search(self, query: str, entries: List[Dict], k: int = 10) -> List[tuple]:
    embeddings = self._embedding_model.encode([e["text"] for e in entries])
    query_emb = self._embedding_model.encode([query])
    # cosine similarity
    scores = np.dot(embeddings, query_emb.T).flatten()
    # return top-k
```

### 3-Signal RRF Fusion

```python
def _rrf_fusion_3signal(self, bm25, semantic, entity, k=60, top_k=8):
    combined = {}
    for rank, (text, score) in enumerate(bm25):
        combined[text[:80]] = combined.get(text[:80], 0) + 0.4 * (1 / (k + rank + 1))
    for rank, (text, score) in enumerate(semantic):
        combined[text[:80]] = combined.get(text[:80], 0) + 0.4 * (1 / (k + rank + 1))
    for rank, (text, score) in enumerate(entity):
        combined[text[:80]] = combined.get(text[:80], 0) + 0.2 * (1 / (k + rank + 1))
    return sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_k]
```

---

## Option A: Phase 2 — Entity Graph + LLM Fact Extraction (Tuần sau)

### Entity Store

```python
class EntityStore:
    def __init__(self):
        # entity_name → EntityRecord(type, memories[], last_seen, confidence)
        self._entities: Dict[str, EntityRecord] = {}
    
    def link_entity(self, entity_name: str, entity_type: str, memory_id: str):
        if entity_name not in self._entities:
            self._entities[entity_name] = EntityRecord(type=entity_type)
        self._entities[entity_name].memories.append(memory_id)
    
    def get_related_memories(self, entity_name: str, limit: int = 10) -> List[str]:
        return self._entities.get(entity_name, {}).memories[-limit:]
```

### LLM Fact Extraction (replace regex)

```python
async def _extract_facts_llm(self, conversation: List[Dict]) -> List[Fact]:
    prompt = f"""
Extract atomic facts from this conversation. Return JSON:
{{"type": "preference|tool|workflow|skill|project", "value": "...", "evidence": "..."}}

Conversation: {self._format_conversation(conversation)}
"""
    response = await self._llm.generate(prompt)
    facts = json.loads(response)
    for fact in facts:
        self._add_fact(fact)  # ADD-only semantics
```

---

## Option A: Phase 3 — Self-Evolution Loop (Tuần 3)

### Workflow Outcome Tracking

```python
{
    "task_type": "wiki_cleanup",
    "approach": "delete stubs",
    "outcome": "success|failed|partial",
    "duration_turns": 12,
    "quality_score": 0.9,
    "learned": "don't use auto-stub creation"
}
```

### Nightly Cron (2AM)

```python
def nightly_self_evolution():
    # 1. Load all memories from past 24h
    # 2. Extract new facts + entity relationships
    # 3. Update entity graph
    # 4. Analyze workflow outcomes → insights
    # 5. Write GROWTH_LOG update
    # 6. Git push
```

---

## Timeline

| Phase | Tuần | Deliverable |
|-------|------|-------------|
| 1 | Tuần này | Vector embeddings + 3-signal RRF |
| 2 | Tuần sau | Entity graph + LLM extraction |
| 3 | Tuần 3 | Self-evolution loop + workflow tracking |
| 4 | Tuần 4 | Integration + testing |

---

## Expected Outcome

| Metric | Before | After |
|--------|--------|-------|
| Retrieval accuracy | ~65% | ~90% |
| Entity linking | None | Full graph |
| Fact extraction | Regex | LLM-powered |
| Self-improvement | Manual | Automated nightly |
| Memory permanence | Checkpoint only | ADD-only + temporal |

---

## Key Mem0 Paper Insights

- **ADD-only extraction** — memories accumulate, nothing deleted. Temporal context preserved (+29.6% on temporal queries).
- **Multi-signal retrieval** — BM25 + semantic + entity fusion outperforms any single signal.
- **Entity linking** — graph-based boosting for entity-centric queries (+23.1% on multi-hop).
- **LLM as fact classifier** — LLM decides ADD/UPDATE/DELETE/NOOP for each candidate fact.
- **LoCoMo benchmark** — 91.6% accuracy with new v2 algorithm.