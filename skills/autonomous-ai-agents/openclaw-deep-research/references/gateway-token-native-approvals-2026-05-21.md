# OpenClaw Gateway Token — Native Approvals

## What happened (2026-05-21)

After updating the Telegram bot token and restarting the gateway, the JSON log showed:
```
"connect error: unauthorized: gateway token not configured on gateway (set gateway.auth.token)"
"failed to start native approval handler: GatewayClientRequestError: unauthorized"
```

The Telegram bot kept retrying and couldn't connect its "native approval handler" to the gateway.

## Root cause

OpenClaw's Telegram plugin uses a "native approval handler" that connects to the gateway via WebSocket. When `gateway.auth.mode` is not set to `token`, OpenClaw generates a **runtime-only token** each time the gateway starts — different on every restart. The Telegram plugin stores the old token and can't reconnect after a restart.

## Why the health check still shows "live"

The health check only verifies the HTTP server is listening. It doesn't check whether the WebSocket native approvals layer is authenticated. So gateway appears fine even when Telegram native approvals are broken.

## The fix that worked

The bot actually recovered after the restart despite the error — the native approvals failure didn't block polling entirely. But to make it permanent:

```bash
cd ~/.openclaw
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "some-persistent-token-here"
npx openclaw gateway restart
```

## Verification

After restart, you should see in JSON log:
- `[telegram][diag] isolated polling ingress started spool=...` (normal polling still works)
- NO `connect error: unauthorized` (native approvals also connected)
- If still seeing unauthorized: the runtime token is still being used — check `gateway.auth.token` is actually persisted in `openclaw.json`

## Key insight

This is a **silent degradation** — the bot responds to messages (polling works) but the native approval flow (which handles things like inline commands and slash-command responses) may be degraded. Always check JSON logs for `native approval` errors when Telegram seems partially broken.