# Hermes Gateway — 2026-06-25 .env Restore Session (companion to incident report)

## Context
This file documents the **user-facing restore session** that followed the 25/06 .env re-deletion. Companion to `report-example-2026-06-25-incident.md` (which covers diagnostic + fix pattern). This file covers the **step-by-step recovery workflow** when user reports "gateway không hoạt động" or "nhắn Telegram không nhận".

## Session Trigger
User report (verbatim): *"check gateway xem có hoạt động không mà anh nhắn trên tele không được!!!"*

User follow-up after initial diagnosis miss: *"mới test ko được! mày kiểm tra cho đàng hoàng chi tiết xem nào!"* — escalation signal, user wants DEEP diagnosis, not just "API is up".

User decision: *"khôi phục lại và tìm cho tao nguyên nhân khiến nó liên tục bị xoá"* — wants BOTH restore AND root cause analysis.

## Restore Workflow (verified path)

### Step 1: Find last known good commit containing .env
```bash
cd ~/.hermes
# Find commits that touched .env
git log --all --oneline --diff-filter=D -- .env
# 927547443 Backup hermes incremental: 2026-06-18 03:00 (untrack .env secrets + content updates)
# → this is the commit that DELETED .env, find the one BEFORE

# Find last commit with .env content
for c in $(git log --all --format=%H -- .env | head -20); do
  SIZE=$(git cat-file -s "$c:.env" 2>/dev/null || echo "0")
  if [ "$SIZE" -gt 0 ]; then
    echo "Last commit with .env ($SIZE bytes): $c"
    git log -1 --format="%h %s" "$c"
    break
  fi
done
```

### Step 2: Extract .env content from that commit
```bash
cd ~/.hermes
git show <commit-sha>:.env
```

**IMPORTANT** — git may have ALREADY redacted tokens at commit time. Check the output:
- If you see `MINIMAX_API_KEY=***` or `TELEGRAM_BOT_TOKEN=***` → redaction happened at commit, real tokens LOST from git history
- If you see actual token values → safe to restore as-is

**Verified 25/06**: git history had `MINIMAX_API_KEY=***` (18 chars placeholder). Token MUST be re-entered from password manager. This is a security feature, not a bug.

### Step 3: Create skeleton .env
```bash
touch ~/.hermes/.env
chmod 600 ~/.hermes/.env
```

### Step 4: Populate with real values
Ask user to provide:
- `MINIMAX_API_KEY` — from MiniMax dashboard (https://api.minimax.io → API Keys)
- `TELEGRAM_BOT_TOKEN` — from @BotFather on Telegram
- `FAL_KEY` — from fal.ai dashboard
- `EXA_API_KEY`, `AUXILIARY_VISION_API_KEY`, `LM_API_KEY` — auxiliary providers

**Safe-write pattern for secrets** (avoid tool-filter stripping):
```bash
# DO NOT echo secret into terminal command (gets redacted from logs)
# Write to /tmp first, then move
cat > /tmp/env-secure.sh << 'EOF'
#!/bin/bash
cat > ~/.hermes/.env << 'ENV_EOF'
MINIMAX_API_KEY=sk-cp-YOUR-REAL-KEY-HERE
HERMES_YOLO_MODE=true
TELEGRAM_BOT_TOKEN=YOUR-REAL-BOT-TOKEN
TELEGRAM_ALLOWED_USERS=1132914873
TELEGRAM_HOME_CHANNEL=1132914873
TELEGRAM_HOME_CHANNEL_THREAD_ID=118389
TELEGRAM_ALLOW_BOTS=all
FAL_KEY=YOUR-REAL-FAL-KEY
ENV_EOF
chmod 600 ~/.hermes/.env
EOF
# User runs this manually, NOT through agent tool calls (avoid log capture)
```

### Step 5: Verify .env
```bash
test -f ~/.hermes/.env && echo "EXISTS" || echo "MISSING"
test -s ~/.hermes/.env && echo "NON-EMPTY" || echo "EMPTY"
ls -la ~/.hermes/.env   # should show -rw------- (600)
```

### Step 6: Restart gateway
```bash
# macOS (Tuấn Anh's setup)
~/.hermes/restart_gateway.sh

# Or manual
ps aux | grep "gateway run" | grep -v grep | awk '{print $2}' | xargs kill
cd ~/.hermes && nohup python -m hermes_cli.main gateway run --replace > /tmp/gateway.log 2>&1 &
```

### Step 7: Verify Telegram platform loaded
```bash
# Wait 30s for startup
sleep 30
grep "Starting Hermes" ~/.hermes/logs/gateway.log | tail -1
grep "Telegram" ~/.hermes/logs/gateway.log | tail -3
# Should see "[Telegram] Connected" or similar, NOT "No messaging platforms enabled"
```

### Step 8: User test
User sends a test message to Telegram bot → expects reply within 30s.

## Common pitfalls during restore

1. **Token redaction in git history** — `git show` returns `***` for secrets that were redacted at commit time. This is INTENTIONAL security, not a bug. User must provide real tokens from password manager.

2. **Token redaction in agent tool output** — when agent writes .env via `write_file` or `cat > ~/.hermes/.env`, the tool layer may redact token values from logs. Workaround: write to /tmp staging file, then have user manually `cp` to final location.

3. **Tool filter strips tokens from terminal commands** — same redaction as #2. Workaround: use heredoc to /tmp file, execute script manually.

4. **`.env` ownership** — after restore, check `ls -la ~/.hermes/.env`. Should be `-rw------- tuananh4865 staff`. If `chmod 644` or other, gateway may still skip loading.

5. **Gateway doesn't pick up new .env** — even after restart, if .env was missing at gateway startup time, gateway may have cached "no platforms" state. Verify by checking log line: `grep "Loaded environment from" ~/.hermes/logs/gateway.log` or similar.

## User Communication Pattern (verified)

When user reports gateway issue:
- **First reply**: Brief root cause statement (1-2 lines) + propose 2-3 fix options. Don't dump technical layers.
- **After user picks option**: Execute + show evidence (file size, grep counts, restart log).
- **After fix**: STOP. Don't ask "anh cần em làm gì thêm không?". Wait for user to verify by sending test message.

User's style (from learned-about-tuananh):
- "được chưa" / "ok" = success, move on
- "khôi phục lại VÀ tìm nguyên nhân" = needs both immediate fix + RCA
- Detailed commands preferred over vague questions
- VIETNAMESE casual, not formal

## Related
- `report-example-2026-06-25-incident.md` — Diagnostic + fix pattern
- `report-example-2026-06-21-incident.md` — First .env deletion incident
- SKILL.md pitfall #20 — Original fix (didn't work)
- SKILL.md pitfall #20h — Recurrence evidence + 3-command diagnostic
- SKILL.md pitfall #20i — "Invisible silent failure window" (new, this file's session)
