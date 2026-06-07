# TikTok Lesson-Learn System

>Auto-updated mỗi đêm bởi cron `546c141c8fb9`
>Created: 2026-06-07

## Overview

Lesson-learn files accumulate TikTok insights over time from competitor monitoring. Each night, the cron extracts NEW patterns from 10 videos (5 channels × 2 videos) and APPENDS to existing lesson files.

**Never overwrite** — always append so insights compound.

---

## File Structure

```
~/.hermes/cron/tiktok-monitor/lessons/
├── README.md           ← Index + overview
├── hooks.md           ← Hook patterns (pattern disrupt, bold statement, open loop...)
├── cta.md             ← CTA patterns (question vs directive, engagement CTAs...)
├── storytelling.md    ← Storytelling structures (problem→solution, rags to riches...)
└── tiktok-shop.md     ← TikTok Shop specific ("1 mẹo" format, expert positioning...)
```

---

## Lesson File Format

Each lesson file follows this structure:

```markdown
# [Topic] — Lesson Learns

>Ngày: YYYY-MM-DD
>Nguồn: N videos từ [channels]

---

## [Pattern Name]

### Format
- Description

### Ví dụ
- ✅ Good example
- ❌ Bad example

### Why it works
- Psychological/algorithmic reason

### Khi nào dùng
- When to apply this pattern

---

## [YYYY-MM-DD] Updates

### New patterns found:
- [pattern] — [channel]
- [pattern] — [channel]
```

---

## Update Protocol

When cron runs, it appends new findings to each file:

1. **hooks.md** — New hook patterns, hook structures
2. **cta.md** — New CTA formats, engagement techniques  
3. **storytelling.md** — New narrative structures, POV styles
4. **tiktok-shop.md** — New product content patterns, conversion techniques

Each update is timestamped with `## [YYYY-MM-DD] Updates` header.

---

## Source Channels

| Channel | Niche | Followers |
|---------|-------|-----------|
| @duymuoi | Content creator tips | 1.3M |
| @anhsacanh.vn | Food/lifestyle | 199.7K |
| @nguyenducduong9699 | Growth/strategy | - |
| @tam_thefox | Expert/authority | - |
| @goccontent | Content tips | - |

---

## How to Use

1. **Before writing script** → read hooks.md + storytelling.md
2. **After drafting** → read cta.md to refine CTA
3. **Product content** → read tiktok-shop.md for commerce patterns

---

## Related
- [[tiktok-content-writing-2026]] — Hooks, structure, 17 viral formulas
- [[tiktok-video-analysis-workflow]] — Frame extraction + vision analysis pipeline
- [[gen-z-slang-june-2026]] — Current slang + Gen Z behavior
