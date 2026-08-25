# MiniMax API Verification — Case Study (2026-05-29)

## What happened

**Question:** "MiniMax-M2.7 có hỗ trợ Anthropic-compatible endpoint không?"

**My answer (WRONG):** "Không — chỉ M2.1 mới support"

**Correct answer:** Có — `https://api.minimax.io/anthropic` hỗ trợ M2.7, M2.5, M2.1, M2

## Why I was wrong

1. Relied on stale knowledge about MiniMax API capabilities
2. Didn't web-search before answering
3. Delivered with false confidence (said "không" như chắc chắn 100%)
4. No QA gate — didn't verify before deliver

## Verified MiniMax API Endpoints (2026-05-29)

### Anthropic-Compatible (Recommended for M2.7)
```
Base URL: https://api.minimax.io/anthropic
Endpoint: POST /anthropic/v1/messages
Auth: Bearer token
```

**Supports:** M2.7, M2.7-highspeed, M2.5, M2.5-highspeed, M2.1, M2.1-highspeed, M2

### OpenAI-Compatible
```
Base URL: https://api.minimax.io/v1
Endpoint: POST /chat/completions
Auth: Bearer token
```

**Supports:** M2.7, M2.7-highspeed

## Lesson

**For ANY question about:**
- API endpoints / base URLs
- Model compatibility matrices
- Provider feature support
- Protocol support (Anthropic vs OpenAI vs REST)

→ ALWAYS web-search first. API specs change constantly. Your knowledge has a cutoff date.

## Workflow for API compatibility questions

1. Web search the official provider docs
2. Extract specific endpoint, base URL, model IDs
3. Verify with official documentation
4. Then answer with confidence + source reference
