---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 karpathy-llm-knowledge-base (extracted)
  - 🔗 topic-workflow (extracted)
  - 🔗 project-tracker (extracted)
relationship_count: 3
---

# Wiki Enhancement Roadmap

## Vision
Transform wiki từ passive knowledge storage thành **autonomous knowledge agent** — tự động ingest, process, synthesize, và maintain knowledge.

## Priority Order

### 1. Self-Healing Wiki (Week 1-2) ← NEW PRIORITY
- [x] Broken link auto-fix hook (2026-04-11)
- [x] Missing frontmatter auto-filler (2026-04-11)
- [x] Stale page detector + auto-bump (already working)
- [x] Orphan pages resolution (2026-04-11)

### 2. Auto-Ingest System (Month 1)
- [x] **Bookmarklet** — Setup guide created, NOT tested on iOS
- [x] **RSS + iOS Shortcuts** — Setup docs ready (see auto-ingest/rss-auto-ingest.md + concepts/rss.md)
- [x] **Email forwarding** — Setup docs ready (see auto-ingest/email-forwarding.md)

### 2. LM Studio Wiki Agent (Month 2)
- [x] Uses LM Studio's local API
- [x] Reads raw content → generates concept pages
- [x] **Cron job chạy mỗi giờ** ✅ (2026-04-12: task_checker every 2.5h + lmstudio_wiki_agent every 1h)
- [ ] Quality improvement: fix frontmatter, reduce meta-commentary

### 3. Synthetic Fine-tuning (Month 3-4)
- [ ] Generate Q&A pairs từ wiki
- [ ] Fine-tune model nhỏ trên wiki content
- [ ] Kết quả: model "know" Anh's knowledge base

### 4. Dead Knowledge Detection (Month 3)
- [x] Detect stale content (>30 ngày không update) — wiki_lint.py created
- [x] Orphan pages (không có links) — resolved 2026-04-11
- [ ] Weekly lint script — Not scheduled

### 5. Knowledge Coverage Map (Low priority)
- [x] Visualize topic distribution — coverage_map.py created
- [x] Gap analysis → Deep research complete (2026-04-12, 240 sources, 229 unique URLs)

## Scripts Created

- [x] `wiki_lint.py` — Dead knowledge detection
- [x] `coverage_map.py` — Topic visualization
- [x] `lmstudio_wiki_agent.py` — Autonomous concept generator
- [x] `lmstudio_setup.py` — Check LM Studio connection

## Wiki Health (as of 2026-04-11)

| Metric | Count | Status |
|--------|-------|--------|
| Total pages | ~60+ | ✅ |
| Stale pages | 0 | ✅ |
| Missing frontmatter | 0 | ✅ Fixed 2026-04-11 |
| Broken links | 0 | ✅ Fixed 2026-04-11 |
| Orphan pages | 0 | ✅ Fixed 2026-04-11 |

> All 14 lint issues resolved: 3 missing frontmatter fixed, 11 orphan pages linked via hub files.

## Related
- [[karpathy-llm-knowledge-base]] — Inspiration
- [[topic-workflow]] — Current workflow
- [[project-tracker]] — Full task tracker
