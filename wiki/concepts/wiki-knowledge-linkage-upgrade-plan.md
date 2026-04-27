---
title: Wiki Knowledge Linkage Upgrade Plan
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [wiki, automation, self-evolution, knowledge-base]
confidence: high
relationships:
  - 🔗 karpathy-llm-wiki (source pattern)
  - 🔗 wiki-self-heal (execution skill)
  - 🔗 wiki-self-evolution (upgrade pipeline)
  - 🔗 deep-research (research skill)
  - 🔗 wiki-lint (health check)
  - 🔗 priority-gaps (gap analysis)
  - 🔗 wiki-cross-ref (link suggestions)
  - 🔗 wiki-self-critique (quality scoring)
relationship_count: 8
---

# Wiki Knowledge Linkage Upgrade Plan

## Tổng quan

**Mục tiêu:** Nâng cấp wiki để đạt high knowledge linkage — thuận tiện truy vấn thông tin, nội dung chất lượng cao, và liên kết knowledge chặt chẽ theo mô hình Karpathy LLM Wiki.

**Tham chiếu:** Karpathy LLM Wiki pattern — LLM-compiled wiki từ raw sources, compounding knowledge over time.

---

## Tình trạng hiện tại (2026-04-11)

### Wiki Health
| Metric | Value | Status |
|--------|-------|--------|
| Total pages | 199 concepts + projects | — |
| Broken links | 4 | ❌ |
| Orphan pages | 8 | ⚠️ |
| Stale pages | 0 | ✅ |
| Missing frontmatter | 0 | ✅ |

### Quality Distribution
| Grade | Score | Count | Pages |
|-------|-------|-------|-------|
| Excellent | 8+ | 2 | Batch 1 plan, Wiki Master Plan |
| Good | 6-8 | ~24 | Various concept pages |
| Fair | 4-6 | ~8 | Mixed quality |
| Poor/Stub | <4 | 16+ | Stub pages at 3.6/10 |

### Missing Topics (Priority Gaps)
| Topic | Score | Status |
|-------|-------|--------|
| kubernetes | 10.0 | ❌ Not created |
| stt (speech-to-text) | 10.0 | ❌ Not created |
| tts (text-to-speech) | 10.0 | ❌ Not created |
| apple-silicon | 10.0 | ❌ Not created |
| llama.cpp | 10.0 | ❌ Not created |
| docker | 10.0 | ❌ Not created |
| rlhf | 10.0 | ❌ Not created |
| dpo | 10.0 | ❌ Not created |
| api | 10.0 | ❌ Not created |
| sqlite | 10.0 | ❌ Not created |
| ollama | 10.0 | ✅ Exists |
| vector-db | 8.0 | ✅ Exists |
| logseq | 8.0 | ❌ Not created |

### Cross-Link Status
| Priority | Count |
|----------|-------|
| High (bidirectional missing) | 556 |
| Medium (same tag, no link) | 2328 |
| Total suggestions | 2884 |

---

## Nâng cấp theo Priority

### Priority 1: Fix Critical Broken Links + Orphans (30 min)
**Lý do:** 4 broken links trong wiki-navigation.md block navigation.

**Actions:**
- [ ] Fix `wiki-navigation.md` broken links → remove `/index.md` references
- [ ] Verify orphan status — many are false positives (deep-research-karpathy, karpathy-nobriars)
- [ ] Add inbound links to legitimate orphans

### Priority 2: Expand Stub Pages (2-3 hours)
**Lý do:** 16+ pages at 3.6/10 — minimal content, no value for querying.

**Stub pages cần expand:**
```
context-window-(language-models).md    3.6/10
structured-outputs-(json).md          3.6/10
observability-in-ai.md                3.6/10
jwt-vs-database-sessions.md           3.6/10
ephemeral-vs-persistent-storage.md    3.6/10
agent-protocols.md                    3.6/10
marp-(markdown-presentation).md       3.6/10
voice-agents.md                       3.6/10
serverless-database-solutions.md      3.6/10
sqlite-in-serverless-environments.md  3.6/10
```

**Method:** Research each topic → write quality content → link to related pages.

### Priority 3: Create Missing Topic Pages (3-4 hours)
**Lý do:** 15 gaps with score 10 — topics mentioned but no dedicated page.

**Topics cần tạo:**
1. `kubernetes.md` — Orchestration (related: docker, ci-cd)
2. `speech-to-text.md` — STT / Whisper (related: whisper, audio)
3. `text-to-speech.md` — TTS (related: voice-agents, audio)
4. `apple-silicon-mlx.md` — Apple Silicon / MLX (related: llama.cpp, mlx)
5. `llama.cpp.md` — GGUF / llama.cpp (related: local-llm, lm-studio)
6. `docker.md` — Containerization (related: ci-cd, kubernetes)
7. `rlhf.md` — Reinforcement Learning from Human Feedback (related: fine-tuning, dpo)
8. `dpo.md` — Direct Preference Optimization (related: fine-tuning, rlhf)
9. `api-design.md` — API design patterns (related: rest, graphql)
10. `sqlite.md` — SQLite in serverless (related: database, vercel)

### Priority 4: High-Priority Bidirectional Links (1-2 hours)
**Lý do:** 556 bidirectional links missing — pages mention topics but don't link.

**Top 20 suggestions:**
```bash
# Execute these cross-links
Add [[wiki]] → [[schema]]
Add [[user-profile]] → [[schema]]
Add [[self-healing-wiki]] → [[schema]]
Add [[project-management]] → [[schema]]
Add [[watchdog-system]] → [[log]]
Add [[github]] → [[index]]
Add [[fine-tuning]] → [[index]]
Add [[local-llm]] → [[lm-studio]]
Add [[karpathy-llm-wiki]] → [[karpathy-llm-knowledge-base]]
Add [[agent-memory]] → [[memory-systems]]
```

### Priority 5: Quality Deep-Dive (ongoing)
**Lý do:** Research-driven content upgrade cho các pages quan trọng.

**Focus areas:**
- `ai-agent-trends-2026-04-10.md` — Update với latest trends
- `agent-frameworks.md` — LangGraph vs CrewAI vs AutoGen comparison
- `agent-memory-architecture.md` — Mem0 vs Zep vs Letta vs Cognee
- `mcp.md` — MCP protocol updates

---

## Implementation Plan

### Phase 1: Quick Wins (1-2 hours)
```
1. Fix 4 broken links in wiki-navigation.md
2. Add 20 bidirectional links (schema references)
3. Verify 8 orphans — remove false positives
```

### Phase 2: Content Expansion (1 day)
```
4. Expand 10 stub pages to quality 7+
5. Create 10 missing topic pages
6. Add cross-links for new pages
```

### Phase 3: Quality Deep-Dive (ongoing)
```
7. Research update cho trending topics
8. Cross-link density pass
9. Quality scoring re-run
```

---

## Success Metrics

| Metric | Before | After Target |
|--------|--------|--------------|
| Broken links | 4 | 0 |
| Stub pages (3.6/10) | 16+ | <5 |
| Pages at 7+ | ~26 | 50+ |
| Missing topics (score 10) | 15 | <5 |
| Bidirectional links added | 0 | 100+ |

---

## Related
- [[karpathy-llm-wiki]] — Source pattern
- [[wiki-self-evolution]] — Upgrade pipeline
