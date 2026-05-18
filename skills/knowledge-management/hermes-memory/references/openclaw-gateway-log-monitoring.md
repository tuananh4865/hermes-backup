# OpenClaw Gateway Log Monitoring

**Path:** `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

**What it contains:** All OpenClaw gateway activity — Telegram inbound/outbound, skills loading, errors, Chrome automation, channel status.

**Query patterns:**
```bash
# View recent activity (last 50 lines)
tail -50 /tmp/openclaw/openclaw-2026-05-18.log

# Filter for Telegram messages
tail -100 /tmp/openclaw/openclaw-YYYY-MM-DD.log | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line)
        msg = d.get('message','')
        t = d.get('time','')
        if any(x in msg.lower() for x in ['inbound', 'outbound', 'telegram']):
            print(f'{t} → {msg[:120]}')
    except: pass
"

# Check bot status
grep -E "Inbound message|res.*message.action" /tmp/openclaw/openclaw-YYYY-MM-DD.log | tail -20
```

**Key bots monitored via logs:**
| Bot | Token | Log Pattern |
|-----|-------|-------------|
| `@Researcher_Clawd_Bot` | `8706108095:***` | `-> @Researcher_Clawd_Bot` in log |
| `@TyayUno` | Primary bot | Direct messages |
| `@SaturdayClawdBot` | Content director | Direct messages |

**Critical openclaw commands:**
```bash
openclaw status              # Quick status check
openclaw gateway restart     # Restart if Telegram crashed
openclaw gateway probe       # Detailed probe
tail -f ~/.openclaw/logs/gateway.log  # Live gateway log
```

**⚠️ Skill path escaping:** OpenClaw logs many "Skipping escaped skill path" warnings — these are benign, filter out when searching for errors.