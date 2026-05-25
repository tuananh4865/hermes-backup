# Gateway & Cron Health Check Reference

## Session Pattern (from 2026-05-25)

Every `check gateway` session should run these 4 commands in parallel:

```bash
# 1. Gateway processes (multiple PIDs = normal if multi-profile)
ps aux | grep -E "hermes.*gateway|gateway.*run" | grep -v grep

# 2. launchd-managed processes
launchctl list | grep hermes

# 3. Gateway logs (filter for errors/warnings)
tail -20 ~/.hermes/logs/gateway.log

# 4. Cron job status (critical for automated operations)
# → via cronjob action='list' tool
```

## Key Metrics to Report

### Gateway
- PID count + profile per PID
- PPID (1 = launchd managed = good)
- Started time
- Last Telegram activity timestamp

### Cron Jobs
- Total count
- Enabled vs paused
- Next run vs last run
- Status (ok / error / paused)
- Delivery target (telegram chat ID if configured)

### Telegram
- Last message timestamp
- Network error recovery (automatic reconnect pattern)
- Response time

## Red Flags

| Flag | Meaning | Action |
|------|---------|--------|
| Single PID when multiple profiles expected | Profile crashed, check logs | Restart |
| Cron job `last_status: error` | Job failed, check delivery | Investigate |
| Cron job `state: paused` | Job manually paused | Ask if intentional |
| PPID != 1 | Not launchd managed | Check plist |
| Telegram reconnect loop >5min | Network issue | Check firewall/proxy |

## Cron Job States (from 2026-05-25)

```python
# State machine from cronjob tool response
state: "scheduled"   # Will run next scheduled time
state: "paused"       # Manually paused, no auto-run
state: "completed"    # One-shot job finished
```

## Known Issues (2026-05-25)

- **ByteRover crons paused** since May 18 — `ffda9e65a08b` (Knowledge Sync) + `ba3953434244` (Health Check)
  - Both have `last_status: error` and `enabled: false`
  - Workers also dead since ~May 14
  - Root cause unclear — memory provider issue?