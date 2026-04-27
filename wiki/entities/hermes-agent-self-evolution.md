---
title: Hermes Agent Self-Evolution
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [agent, self-improvement, dspy, optimization, nousresearch]
sources: [raw/articles/nousresearch-hermes-agent-self-evolution.md]
confidence: high
relationships: [hermes-agent, dspy, dgepa, self-healing-wiki]
---

# Hermes Agent Self-Evolution

> GitHub: [NousResearch/hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution)
> Stars: 2311 | Forks: 245 | License: MIT | Published: 2026-03-09

Evolutionary self-improvement cho Hermes Agent — tự động optimize skills, prompts, và code sử dụng **DSPy + GEPA** (Genetic-Pareto Prompt Evolution).

## Key Features

- **No GPU training** — chỉ cần API calls, ~$2-10 per optimization run
- **5-phase roadmap** — từ skill files → tool descriptions → system prompts → code → continuous loop
- **Guardrails** — mọi variant phải pass test suite, size limits, semantic preservation
- **PR-based workflow** — không bao giờ commit trực tiếp, luôn qua human review

## Phases

| Phase | Target | Status |
|-------|--------|--------|
| 1 | Skill files (SKILL.md) | ✅ Implemented |
| 2 | Tool descriptions | 🔲 Planned |
| 3 | System prompt sections | 🔲 Planned |
| 4 | Tool implementation code | 🔲 Planned |
| 5 | Continuous improvement loop | 🔲 Planned |

## How It Works

GEPA đọc execution traces để hiểu *tại sao* thứ gì đó thất bại (không chỉ là thất bại), sau đó đề xuất cải tiến targeted. ICLR 2026 Oral.

## Related

- [[hermes-agent]] — Hermes Agent core
- [[hermes-agent-self-evolution]] — This project
- [[dspy]] — DSPy framework
- [[hermes-self-improvement-activation]] — Self-improvement features
- [[self-healing-wiki]] — Self-maintenance patterns

## Notes

Phase 1 (skill optimization) đã implemented — có thể dùng ngay để optimize skill files trong Hermes Agent repo.
