---
title: "Wiki Self-Maintaining System"
created: 2026-04-12
updated: 2026-04-12
type: project
status: active
phase: phase-a-verify-scripts
tags: [wiki, self-improvement, autonomous, maintenance]
confidence: high
relationships:
  - karpathy-llm-wiki
  - your-harness-your-memory
  - wiki-self-evolution
---

# Wiki Self-Maintaining System

**Status**: Active
**Started**: 2026-04-12
**SDD**: This is the implementation of SDD for proactive wiki upgrade

---

## Mission

Transform wiki from passive knowledge storage into **proactive, self-maintaining memory system** for LLM agent.

> Wiki = External Memory Harness (Harrison Chase principle)
> LLM should actively manage its own knowledge base

---

## Phases

### Phase A: Verify Scripts ✓ DONE (2026-04-12)
- [x] Verify `wiki_lint.py` — ✓ 36 orphan pages found
- [x] Verify `wiki_self_heal.py` — ✓ 2 broken links, 5 missing frontmatter, 69 orphans
- [x] Verify `wiki_self_critique.py` — ✓ 697 pages, avg 5.8/10, 84 poor
- [x] Verify `wiki_gap_analyzer.py` — ✓ Found gaps: cron, vector, vault, plugins
- [x] Verify `semantic_search.py` — ✓ Working
- [x] Verify `wiki_cross_ref.py` — ✓ 7428 suggestions, 1545 high priority
- [x] Verify `wiki_self_evolution_agent.py` — ✓ Full cycle ran

### Phase B: Cron Schedule Setup ✓ DONE (already configured)
- [x] 7:30AM — Daily Agentic Morning Ritual (last_run: ok)
- [x] 9PM — Daily Knowledge Extraction (last_run: ok)
- [x] 3AM — Wiki Daily Self-Heal (last_run: ok)
- [x] Monday 2AM — Wiki Weekly Health Check
- [x] Every 2h — Autonomous Wiki Agent (last_run: ok)

### Phase C: Self-Improvement Loop ✅ DONE (2026-04-12)
- [x] Create `topic_workflow.py` — Raw source → concept pipeline (llm-wiki standard)
- [x] Create `cron_daily_ingest.py` — Daily ingest orchestrator
- [x] Create `watchdog_processor.py` — Event-driven self-healing
- [x] Fix cascading broken links (12 pages fixed, 0 broken links remaining)
- [x] Fix missing frontmatter (0 remaining)
- [x] Create stub pages to resolve orphan link chains

**Wiki health (final state):**
- Broken wikilinks: 0 ✅
- Missing frontmatter: 0 ✅
- Stale pages (>30 days): 0 ✅
- Total pages: 717

### Phase D: Cron Integration ✅ DONE (2026-04-12)
- [x] Updated 5 cron job prompts to align with new three-layer wiki structure
- [x] Daily Self-Heal (3AM): Auto-fix broken links + missing frontmatter, skip templates
- [x] Daily Knowledge Extraction (9PM): Correct transcript vs article distinction
- [x] Daily Morning Ritual (7:30AM): Research + plan with wiki structure awareness
- [x] Autonomous Wiki Agent (2h): Task execution + deep research with structure awareness
- [x] Weekly Health Check (Mon 2AM): Comprehensive audit + improvement recommendations

### Phase E: Orphan Resolution ✅ DONE (2026-04-12)
74 orphan pages analyzed:
- Session notes (8): `Tun - 2026-04-12.md`, `hello - 2026-04-12.md`, etc. — LEGITIMATE, don't link
- Plans (7): `plan.md`, `sdd.md`, `readme.md`, etc. — LEGITIMATE, don't link
- Project meta (5): wiki meta files — LEGITIMATE, don't link
- Actual concepts (37): `zod`, `zustand`, `tavily`, `upstash`, etc. — should be linked but low priority

**Decision: Skip orphan linking for now.** Most orphans are session notes/plans that don't need wikilinks. The actual orphan concepts (37) are mostly edge cases. This is a low-value task compared to quality expansion.

### Phase F: Quality Upgrade — IN PROGRESS
422 low-quality pages. Current average: 5.8/10. Running batch expansion via cron.

### Phase G: Cascade Link Fix ✅ DONE (2026-04-12)
Fixed cascading broken wikilinks (138 → 2 → 0):
- Kafka.md: Event Streaming, CQRS, Apache ZooKeeper, Kafka Streams
- CDN.md: DNS, DDoS Protection, Web Performance, Anycast
- MobX.md: Reactive Programming, Observable Pattern
- Batch-Processing.md: Stream Processing, ETL
- Plus 60+ other pages with broken link targets

Created 60+ stub pages for missing concepts:
- event-streaming, cqrs, ddos-protection, anycast, reactive-programming
- observable-pattern, stream-processing, etl, web-performance, apache-zookeeper
- kafka-streams, dns, pubsub, ab-testing, message-broker, amqp
- apache-kafka, erlang, devops, test-driven-development, canary-releases
- build-automation, containerization, scrum, kanban, user-stories
- product-backlog, kano-model, rice-scoring, agile-methodology
- flux-architecture, action-objects, observer-pattern, local-state
- server-side-rendering, data-pipelines, apache-spark, apache-hadoop
- workflow-orchestration, codepen, jsfiddle, webpack, frontend-development
- algorithmic-accountability, data-ethics, discriminatory-ai
- elk-stack, object-relational-mapping, mean, mern, express.js
- fastify, socket.io, websockets, serverless-computing, gulp, npm, npx
- v8-engine, rest-apis, sphinx, docusaurus, readme-files, api-documentation
- strategic-planning, competitive-advantage, digital-transformation
- porter-s-five-forces, swot-analysis, exceptions, resilience-patterns
- token-based-authentication, sso, cascading-goals, smart-goals, mbo
- performance-management, active-record, data-mapper, database-migration
- prototypal-inheritance, event-loop, v8, css, dom, url

**Wiki health (current):**
- Broken wikilinks: 0 ✅
- Missing frontmatter: 0 ✅
- Stale pages (>30 days): 0 ✅
- Total pages: 831 (up from 717)

### Phase H: Batch Expansion — ONGOING
Running through autonomous-wiki-agent cron. Batch 7 completed: 21 stubs expanded (Drizzle, HTML, JavaScript, Kafka, Logging, Memcached, MoSCoW, MobX, Node.js, OAuth2, OKRs, ORM, RabbitMQ, RCS, RICE, Redux, SAML, SMPP, SS7, SSG, SSR)

---

## Progress Log

### 2026-04-12 - Phase A Started

| Script | Status | Notes |
|--------|--------|-------|
| wiki_lint.py | ⏳ | |
| wiki_self_heal.py | ⏳ | |
| wiki_self_critique.py | ⏳ | |
| wiki_gap_analyzer.py | ⏳ | |
| semantic_search.py | ⏳ | |
| wiki_cross_ref.py | ⏳ | |
| wiki_self_evolution_agent.py | ⏳ | |

---

## Related
- [[karpathy-llm-wiki]] — Original pattern
- [[your-harness-your-memory]] — Harrison Chase validation
- [[wiki-self-evolution]] — Self-improvement pipeline
