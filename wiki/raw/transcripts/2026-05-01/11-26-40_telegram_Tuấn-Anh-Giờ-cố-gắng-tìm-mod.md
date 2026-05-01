---
title: Transcript 2026-05-01 11:26:40
created: 2026-05-01
platform: telegram
user_id: 1132914873
session_id: 20260501_103655_3eb8c4
timestamp: 2026-05-01 11:26:40
type: transcript
tags: [transcript]
---

## User Message (2026-05-01 11:26:40)

[Tuấn Anh] Giờ cố gắng tìm model nào embedded 1536 dimensions đi

---

## Assistant Response

Tin xấu Anh — **không có model 1536 dims nào support OpenAI-compatible endpoint cả**.

Research findings:

| Model | Dims | Issue |
|-------|------|-------|
| jina-embeddings-v4 (base) | 2048 | Too large, only GGUF via vLLM/transformers |
| jina-embeddings-v4-text-retrieval | 2048 | Same — needs Qwen2.5-VL arch |
| jina-embeddings-v4-text-code | 1536 | Chỉ hỗ trợ code, không phải text embedding |
| nomic-embed-text-v1.5 | 768 | OK but small |
| mxbai-embed-large-v1 | 1024 | **Currently in use — 

---
_Saved by transcript-saver hook at 2026-05-01 11:26:40_