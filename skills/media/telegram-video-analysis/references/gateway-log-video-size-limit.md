---
title: Gateway Log + Video Size Limit (Telegram Bot API 20MB)
created: 2026-06-24
type: reference
tags: [telegram, video, gateway, troubleshooting, pitfall-37, pitfall-38]
related: [../SKILL.md]
---

# Gateway Log + Video Size Limit

## Problem

User says "I sent you a video" but tool input to agent is text-only (no attachment). Agent sees empty text, reports "empty message" — but the video is real, it was just rejected by the Telegram Bot API silently.

**What actually happened:**

1. User sent video > 20MB via Telegram
2. Telegram Bot API received the message but `getFile` call FAILED (server-side 20MB cap)
3. Hermes adapter (line 6287-6302 in `plugins/platforms/telegram/adapter.py`) caught exception, logged `WARNING [Telegram] Failed to cache video: File is too big`
4. Adapter set `event.media_urls = []` and `event.text = ""` (because the only content WAS the video)
5. Agent received `text=""` + `media_urls=[]` → concluded "empty message, user sent nothing"

## Why "empty message" is the wrong conclusion

The agent has 3 distinct signals to disambiguate:

| Signal | Meaning | Correct response |
|--------|---------|------------------|
| Gateway log shows `Failed to cache` / `File is too big` | Video > 20MB, Bot API rejected | Tell user about size limit + propose 3 alternatives |
| `~/.hermes/cache/videos/` has new file | Video cached successfully | Proceed with normal pipeline |
| Both log + cache empty | Message not yet received, or user sent link | Ask user to confirm |

The agent MUST check the log first. The cache is unreliable when video > 20MB.

## Diagnostic Commands

```bash
# Primary: check gateway log for warnings
tail -100 ~/.hermes/logs/gateway.log 2>/dev/null | \
  grep -iE "Failed to cache|File is too big|attachment" | tail -10

# Secondary: check cache for new files
ls -lat ~/.hermes/cache/videos/*.mp4 2>/dev/null | head -5

# Sanity: check if any inbound message exists at all
tail -200 ~/.hermes/logs/gateway.log 2>/dev/null | \
  grep "inbound message" | tail -5
```

## What to tell the user

When log shows `File is too big`, respond with the 3 options template from Pitfall #38. Don't just say "I don't have the file" — give the user a path forward.

## Why the log exists

The Hermes adapter writes structured WARNING/ERROR logs for every attachment processing attempt:

- `~/.hermes/logs/gateway.log` — main gateway log (inbound messages + adapter events)
- `~/.hermes/logs/gateway.error.log` — error-level only
- `~/.hermes/logs/errors.log` — top-level errors across all components

These are persistent on disk and never rotated during a session. The `Failed to cache` warning will stay there for hours, easy to find with `tail` + `grep`.

## Telegram Bot API limits (reference)

| Resource | Limit | Notes |
|----------|-------|-------|
| `getFile` download | 20 MB | Public Bot API, hard cap |
| `sendMessage` text | 4096 chars | Per message |
| Photo upload | 10 MB | 10 MB per photo, 2000x2000 max |
| Video upload | 50 MB | But getFile capped at 20 MB |
| Audio upload | 50 MB | Same getFile cap |
| File upload (document) | 50 MB | Same getFile cap |

**To send > 20MB through Telegram, you need a self-hosted Local Bot API server.** Default public API cannot serve files > 20MB regardless of client.

## Real session that triggered this (2026-06-24)

User sent video 22:30. Hermes logged at 13:06:06:
```
WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Failed to cache video: File is too big
```

Agent (me) at 13:01 said:
> "Em thấy có video trong cache nhưng tất cả đều từ Jun 9-18 (5+ ngày trước). Video hôm nay anh gửi CHƯA VỀ CACHE."

User replied:
> "Ủa tại sao tao gửi video qua telegram mà mày lại bảo tin nhắn rỗng????"

Agent (me) at 13:08 still said:
> "VẪN KHÔNG CÓ VIDEO MỚI"

User replied:
> "Tao chắc chắn mày chỉ đang đọc đầu vào tin nhắn của tele rồi!"

Agent (me) THEN checked the log and found the warning.

**Total time wasted: 7 minutes, 3 user messages, trust damage.**

## Prevention (Pitfall #37, 38)

Encode these into Step 1 of the SKILL.md workflow:

1. **Step 1a: Check log first** (5 sec grep)
2. **Step 1b: Then check cache** (existing logic)
3. **Step 1c: If log shows error, respond with 3-option template**

This is a 5-second check that prevents a 7-minute user trust failure.

## Related

- SKILL.md Pitfall #37 (workflow fix)
- SKILL.md Pitfall #38 (response template)
- `~/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py` line 502 + 6287-6302 (actual logic)
