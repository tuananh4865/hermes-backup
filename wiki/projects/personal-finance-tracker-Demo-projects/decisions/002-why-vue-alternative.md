---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 001-tech-stack (extracted)
  - 🔗 phase-1-init (extracted)
relationship_count: 2
---

# 002 — Why Not Vue

## Context
Considered using Vue.js for this project since it was mentioned as an option.

## Options Considered
1. **Vue.js** — Lightweight, easy to learn, great documentation
2. **React** — More ecosystem, more job market relevance, better AI tool support

## Decision Made
**Chosen**: React (via Next.js)

## Rationale
- React có better integration với AI coding agents (Claude Code, Copilot)
- Next.js cung cấp SSR + API routes trong 1 project, tiện hơn Next.js so với Nuxt
- Ecosystem lớn hơn — có nhiều library hỗ trợ finance (charts, date handling)
- Tuổi thọ lâu hơn Vue theo community trend

## Consequences
- Steep learning curve cho beginners (JSX vs Template syntax)
- React ecosystem thay đổi nhanh (cần theo dõi React Server Components mới)

## Related
- [[001-tech-stack]]
- [[phase-1-init]]
