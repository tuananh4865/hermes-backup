# Session Storage Architecture — 2026-07-27

## Problem
Jul 26 session metadata in `sessions.json` showed `input_tokens=0, output_tokens=0, total_tokens=0` — no message content could be extracted. Session existed but was unreadable.

## Root Cause Analysis

### Storage Layers (in order of priority)

**Layer 1: `sessions.db` (SQLite)**
- Path: `~/.hermes/sessions/sessions.db`
- Tables: `sessions`, `messages`
- Status on 2026-07-27: **EMPTY (0 bytes)** — no content for Jul 25-26
- Status on 2026-07-28: **RECOVERED** — db back to normal, contains Jul 27 sessions
- **Lesson:** Transient corruption; db can recover without manual intervention. If db is empty during a cron run, re-check next day before escalating.

**Layer 2: `sessions.json` (JSON flat-file)**
- Contains: metadata only (session_id, created_at, input_tokens, output_tokens, etc.)
- Does NOT contain: message content
- Status on 2026-07-27: **Jul 26 sessions show input_tokens=0, output_tokens=0**

**Layer 3: `request_dump*.json` (raw request logs)**
- Latest on 2026-07-27: Jul 23 only — no Jul 25-26

**Layer 4: `*.jsonl` (session transcript logs)**
- Latest on 2026-07-27: May 28 2026 only

## Diagnosis Protocol

```bash
# Step 1: Check sessions.db
file ~/.hermes/sessions/sessions.db  # should say "empty" if the issue exists

# Step 2: Check sessions.json for zero tokens
python3 -c "
import json
with open('/Users/tuananh4865/.hermes/sessions/sessions.json') as f:
    data = json.load(f)
for sid in data.keys():
    if '2026-07-26' in str(data[sid].get('created_at','')):
        print(f'{sid}: tokens={data[sid].get(\"input_tokens\")}/{data[sid].get(\"output_tokens\")}')
"

# Step 3: Check request_dump dates
ls -lt ~/.hermes/sessions/request_dump* 2>/dev/null | head -3
```

## Implication for Daily Session Review

When all layers show empty/recent-data-missing:
→ Session content is **not recoverable locally**
→ Must ask user to verify, or check Telegram history directly
→ Report "NO SESSION DATA" with honest note about storage state
