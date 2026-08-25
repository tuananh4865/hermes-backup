# Telegram Bot API — Rate Limits Reference

> **Source:** Telegram Bot API official docs + community references (verified 24/06/2026)
> **Use:** Reference khi debug "Message delivery failed" errors

## Official limits (Telegram Bot API)

| Scope | Limit | Notes |
|-------|-------|-------|
| **Same chat** (1-on-1) | **1 message/second** | Strict per chat_id |
| **Same group** | **20 messages/minute** | Applies to groups AND channels |
| **Global** (different chats) | **30 messages/second** | Across all chats bot sends to |
| **Edit message** | Counts toward same-chat limit | Use sparingly |
| **Forward message** | Counts toward same-chat limit | |
| **sendMessage with `reply_to_message_id`** | Counts as new message | |

## Error response

```json
{
  "ok": false,
  "error_code": 429,
  "description": "Too Many Requests: retry after 26",
  "parameters": {
    "retry_after": 26
  }
}
```

**Key field:** `parameters.retry_after` (integer seconds) — Telegram explicitly tells bot when to retry.

## Common causes (real session data 18/06)

1. **Burst from sub-agent delegation** (37% of 839 events) — 3-8 sub-agents send progress messages within 1-2s window
2. **Rich message fallback chain** (46% of 839 events) — `sendRichMessage` fail → `sendMessage` fallback = 2× flood per message
3. **Cron jobs at same hour** — 5+ jobs firing at 0h/2h → 5 messages within 1s
4. **Long conversation, many small messages** — Hermes streams tokens, may send partial messages that get rejected

## What NOT to do

- ❌ Send 5+ messages within 1 second to same group
- ❌ Retry immediately after `retry_after` (must wait the full duration)
- ❌ Use `sendMessage` + `editMessage` repeatedly for same content (counts as 2)
- ❌ Forward/copy messages between groups in bulk

## Best practices

1. **Batch messages:** If sending 5+ related messages, combine into 1 long message
2. **Respect `retry_after`:** If Telegram says 26s, wait AT LEAST 26s
3. **Use exponential backoff + jitter:** 2s → 4s → 8s → 16s with ±1s random
4. **Stagger cron schedules:** 0h, 0:05, 0:10 instead of all 0h
5. **Disable rich messages during flood risk:** Plain `sendMessage` (no markdown) = 1 attempt per message
6. **Use `sendChatAction` for "typing" indicator:** Doesn't count toward rate limit, signals activity

## Telegram libraries that handle this correctly

- **python-telegram-bot (PTB):** Built-in rate limiter (`rate_limiter=True` in Application)
- **aiogram 3.x:** Built-in `ThrottlingMiddleware` for flood control
- **python-telegram-bot-raw:** Manual — must handle `retry_after` yourself

## Verifying current state (Hermes)

```bash
# Check Hermes's retry behavior
grep -A 5 "def.*send" ~/.hermes/hermes-agent/gateway/platforms/telegram.py | head -30

# Check recent flood events
grep "Flood control exceeded" ~/.hermes/logs/gateway.log | tail -10
```

## Sources

- https://core.telegram.org/bots/api#rate-limits (official)
- https://grammy.dev/advanced/flood (grammY framework guide)
- https://zernio.com/telegram/errors (error code reference)
- https://stackoverflow.com/questions/45905266/what-is-the-limit-of-sending-messages-from-a-telegram-bot
