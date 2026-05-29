---
name: qa-gate
description: QA Gate Protocol — verify every step before proceeding. Use when starting any task, before delivering results, or when asked "are you sure?". Load when working on research tasks, API questions, or any task where accuracy matters.
---

# QA Gate Protocol — Mỗi Bước Nhỏ Đều Phải QA

## Critical Lesson (2026-05-29)

**What happened:** Said MiniMax-M2.7 doesn't support Anthropic-compatible endpoint. Was 100% wrong. Correct: `https://api.minimax.io/anthropic` supports M2.7, M2.7-highspeed, M2.5, M2.5-highspeed, M2.1, M2.1-highspeed, M2.

**Root cause:** Relied on stale memorized knowledge instead of researching current docs.

## 3 Loại QA Gate

### Gate 1: Pre-Execution QA (TRƯỚC KHI LÀM)

```
Confidence Score Check:
- Score ≥ 9 → Proceed (verify nhanh 1 nguồn)
- Score < 9 → Research BẮT BUỘC trước
- Score < 5 → Deep research bắt buộc
```

### Gate 2: Mid-Execution QA (TRONG KHI LÀM)

**Trigger:** Sau mỗi milestone nhỏ — verify output trước khi đi tiếp.

### Gate 3: Post-Execution QA (SAU KHI LÀM)

**Trigger:** Trước khi deliver result — checklist.

## API/Model Compatibility — ALWAYS Web-Search First

**Never answer without web search:**
- Model hỗ trợ endpoint nào
- Base URL chính xác cho provider
- Tool X có dùng được với model Y không
- API format (Anthropic vs OpenAI) cho bất kỳ provider nào

**Workflow:**
1. Web search docs của provider đó
2. Extract endpoint, base URL, model ID
3. Verify với official documentation
4. Then answer — kèm source reference

## Quick QA Rules

| Scenario | Action |
|----------|--------|
| Em muốn deliver ngay | ❌ Stop → Verify trước |
| Không chắc về fact | → Research, don't guess |
| API specs, endpoints | → ALWAYS search web first |
| Đã deliver xong thấy uncertain | → Correct ngay |

## Case Study
- `references/minimax-api-verification-2026-05-29.md` — WRONG answer delivered without research: said M2.7 doesn't support Anthropic-compatible endpoint. Reality: it does. QA gate would have caught this.

## Related
- [[hermes-agent-self-evolution]]