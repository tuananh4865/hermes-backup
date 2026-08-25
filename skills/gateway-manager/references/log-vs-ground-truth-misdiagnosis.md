# Reference: "Log says X broken, but service is fine" misdiagnosis

**Date:** 2026-06-25 19:43 Vietnam time
**Session:** `20260625_194300` (Telegram → CLI bridge)
**Skill that should have been loaded first:** `gateway-manager` (not loaded — agent improvised from scratch)

## What the user said

> "check gateway xem có hoạt động không mà anh nhắn trên tele không được!!!"

## What the agent did wrong

1. Read `~/.hermes/logs/gateway.log`
2. Saw 30 lines of `APIConnectionError` against `https://api.minimax.io/anthropic` (provider = `minimax`, model = `MiniMax-M3`)
3. Concluded: "API MiniMax down → that's why Telegram messages not responding"
4. Asked user to choose between "restart gateway", "switch fallback model", or "check ping"

## What user pushed back with

> "anh đang nhắn cho em đây cũng đang dùng minimax api mà em vẫn trả lời được đây thôi!"

Translated: "I'm messaging you RIGHT NOW from the same Telegram bot using the same MiniMax API, and you ARE responding to me. So the API is fine."

## The ground truth

- Agent is running from the same CLI session the user is talking to.
- Agent's own responses prove the API path is healthy.
- The `Connection error` log lines were from **background cron jobs** during a transient provider hiccup — NOT from the user's messages.
- The "missed Telegram messages" cause is still UNKNOWN (could be flood control, could be a different network path, could be a Telegram API rate limit, etc.) — but it is NOT "API provider down".

## Diagnostic steps that should have been run first

```bash
# 1. Confirm the user-facing path is alive (this CLI session proves it)
# If you can answer the user, the API path works.

# 2. Find WHICH messages are missed — not "any" messages, the specific ones
grep -E "Failed to deliver|update_id" ~/.hermes/logs/gateway.log | tail -20

# 3. Correlate log errors with timestamps of user's reports
# "User said 19:30 message not delivered" → grep for 19:30 ± 5 min in log

# 4. Distinguish request_dump files from real user message failures
ls -lt ~/.hermes/sessions/request_dump_*.json 2>/dev/null | head -5
# request_dump files = cron-generated context, not user messages

# 5. Verify the suspected broken endpoint from THIS terminal right now
curl -m 5 -o /dev/null -w "HTTP %{http_code}\n" https://api.minimax.io/anthropic
```

## The wrong-vs-right framing

| Agent said (wrong) | Should have said (right) |
|--------------------|--------------------------|
| "API MiniMax down, that's why Telegram không respond" | "Gateway đang chạy (PID X). Để em check log xem tin nhắn cụ thể nào bị miss trước khi kết luận." |
| "Restart gateway? Switch model? Check ping?" (3 options, no data) | "Để em grep log cho tin nhắn cụ thể của anh — pattern sẽ cho biết là flood control, network, hay gì." |

## Lesson encoded

The skill `gateway-manager` "Channel Adapter Not Connected" section already covers:
- Token missing (rank 1)
- Token rotated (rank 2)
- Network/DNS blocks (rank 4)
- Adapter crash in getUpdates (rank 5)
- Webhook vs polling conflict (rank 6)

**It did NOT cover:** "Log shows errors from a layer that is currently working." This is a class of misdiagnosis — not a hardware issue, not a config issue, but a **reasoning** issue (jumping to conclusion from log text without verifying ground truth).

The fix is in `SKILL.md` under "Channel Adapter Not Connected" → "Critical pitfall: Log says 'Connection error' but service is actually fine."

## When this pattern recurs

Any time the agent sees an error in a log file and the user is currently able to talk to the agent, the error is from a DIFFERENT code path. Don't conflate them. This applies to:
- `gateway.log` API errors during active user chat
- `error.log` exceptions during successful sub-agent runs
- Cron `request_dump` files when the user just got a successful response

## Cross-references

- `telegram-flood-control-diagnosis` — covers layer 1 (Telegram rate limit)
- `telegram-video-20mb-limit` — covers layer 2 (Telegram file size cap)
- `gateway-manager` (this skill, after patch) — covers layer 3 (log vs ground truth)
- `qa-gate` — verify before reporting done (general principle)
- `self-verify-after-workaround` — run tool checks before claiming "X works"
