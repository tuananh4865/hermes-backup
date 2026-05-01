---
title: Transcript 2026-05-01 09:52:57
created: 2026-05-01
platform: telegram
user_id: 1132914873
session_id: 20260501_084046_126f05
timestamp: 2026-05-01 09:52:57
type: transcript
tags: [transcript]
---

## User Message (2026-05-01 09:52:57)

[Tuấn Anh] Pglite bug đó là gì, khắc phục triệt để được ko?

---

## Assistant Response

Tìm thấy đầy đủ rồi. **Có 2 failure modes:**

| Mode | Error | Nguyên nhân |
|------|-------|-------------|
| **Mode 1** | `Aborted().` | macOS 26.3 + PGLite WASM runtime conflict |
| **Mode 2** | `/$bunfs/root/pglite.data` | Binary compiled thiếu PGLite WASM assets |

Anh đang gặp **Mode 2** — binary đã compiled nhưng PGLite WASM assets không được bundle vào.

**Fix triệt để — 3 cách:**

### Cách 1: Dùng `bun run` thay vì binary (ĐANG DÙNG — OK)
```bash
alias gbrain='cd ~/gbrain && PATH="$HOME/

---
_Saved by transcript-saver hook at 2026-05-01 09:52:57_