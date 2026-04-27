---
title: "Hermes Dojo - Self-Evolving Wiki Agentic System"
created: 2026-04-14
updated: 2026-04-15
type: project
tags: [hermes, wiki, agentic, self-evolving, project]
description: "Project xây dựng hệ thống wiki agentic tự tiến hóa với 8 phases, 25 skills, 6 scripts"
sources: [raw/transcripts/2026-04-14-tun-https-youtu.md]
---

# Hermes Dojo

## Tóm tắt

Hermes Dojo là project xây dựng hệ thống wiki agentic tự tiến hóa cho Hermes Agent, hoàn thành ngày 2026-04-14. Gồm **8 phases** với **25 skills** và **6 scripts**. Mục tiêu: eliminate infinite cascade loop (fix A → break B → fix B → break C).

## 8 Phases

| Phase | Name | Status | Skills |
|-------|------|--------|--------|
| 0 | Skeleton | ✅ PASS | - |
| 1 | Behavior | ✅ PASS | 3 |
| 2 | Process | ✅ PASS | 5 |
| 3 | Dependency | ✅ PASS | 5 |
| 4 | Memory Lifecycle | ✅ PASS | 4 |
| 5 | Knowledge Graph | ✅ PASS | 2 |
| 6 | Automation | ✅ PASS | 4 |
| 7 | Quality | ✅ PASS | 4 |
| 8 | Proactive | ✅ PASS | 4 |

## Key Scripts

| Script | Purpose |
|--------|---------|
| `dependency_tracker.py` | Theo dõi dependencies trong codebase |
| `entity_extractor.py` | Trích xuất entities từ text |
| `knowledge_graph.py` | Knowledge graph database |
| `confidence_scorer.py` | Đánh giá confidence score |
| `nudge_trigger.py` | Tự động nhắc nhở |
| `wiki_hooks.py` | Event-driven automation |

## Key Principles

- **Patch-only rule**: Không rewrite full skills, chỉ patch phần thay đổi
- **R→P→I workflow**: Research → Plan → Implement
- **QA-first**: Mỗi phase cần pass QA trước khi tiếp tục
- **4-tier memory**: Working, Episodic, Semantic, Procedural

## Bugs Fixed During Testing

1. `knowledge_graph.py`: `db_path` not converted to Path object
2. `dependency_tracker.py`: `--check` wasn't scanning entire codebase
3. `dependency_tracker.py`: `rglob` fails when path is a file

## Files Created

- Project: `/Users/tuananh4865/wiki/projects/hermes-dojo/`
- 25 skills across 7 categories
- Retrospective: `retrospectives/2026-04-14-hermes-dojo-build/SKILL.md`

## Related

- [[hermes-skill-self-improvement]]
- [[cascade prevention]]
- [[R→P→I workflow]]
