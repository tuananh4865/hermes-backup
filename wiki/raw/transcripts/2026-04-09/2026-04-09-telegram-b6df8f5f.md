---
title: "Tìm process"
created: 2026-04-21
updated: 2026-04-21
type: transcript
tags: ['transcript']
---


[2026-04-09 09:12:49] 👤 Anh: Kiểm tra xem được chưa, anh muốn full conversation, hãy tìm cách thực hiện đúng yêu cầu của anh đi
[2026-04-09 09:12:49] 🤖 Em: Hook đã update xong. Format transcript JSONL đã confirm:

```json
{"role": "user", "content": "...", "timestamp": "..."}
{"role": "assistant", "content": "...", "timestamp": "..."}
```

**Hook mới `wiki-transcript`**:
- Trigger: `session:end` (khi session kết thúc)
- Action: Load full transcript từ `~/.hermes/sessions/*.jsonl`
- Output: Formatted wiki-style markdown vào `~/wiki/raw/transcripts/[date]/[topic].md`

**Cần restart gateway** để load hook. Anh chạy:

```bash
# Tìm process
ps aux | gre