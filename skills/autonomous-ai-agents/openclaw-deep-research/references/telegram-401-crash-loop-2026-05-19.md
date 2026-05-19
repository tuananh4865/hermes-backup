# ResearchClaw Bot Token Revoked — 2026-05-19

## Session Summary
ResearchClaw bot (`@Researcher_Clawd_Bot`) stopped responding to @mentions in the Telegram group.
Gateway health was fine (`{"ok":true,"status":"live"}`) but Telegram channel was in a crash loop.

## Root Cause
Bot token `8706108095:***` returned **401 Unauthorized** on all Telegram API calls.

## Diagnosis Commands
```bash
# Check if process running
ps aux | grep openclaw | grep -v grep

# Health check (gateway OK even if Telegram down)
curl -s http://localhost:18789/health

# Test Telegram token
curl -s https://api.telegram.org/bot<TOKEN>/getMe

# Count restart attempts (440 = severe crash loop)
grep -c "auto-restart attempt" /tmp/openclaw/openclaw-2026-05-19.log

# Last entries in JSON log
tail -100 /tmp/openclaw/openclaw-2026-05-19.log | grep -E "(deleteWebhook|deleteMyCommands|auto-restart|channel exited)" -i
```

## Key Log Excerpt
```
[default] channel exited: Call to 'deleteWebhook' failed! (404: Not Found)
[default] auto-restart attempt 6/10 in 169s
...
[default] auto-restart attempt 7/10 in 300s
...
[default] starting provider
```

## Resolution
Need new bot token from @BotFather. Config update required.

## Related
- SKILL.md: openclaw-deep-research → Known Issues → Bot Token Revoked → Crash Loop