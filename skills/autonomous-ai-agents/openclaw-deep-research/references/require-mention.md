# OpenClaw ResearchClaw Bot Setup — Session 2026-05-18

## Goal
Make @Researcher_Clawd_Bot only respond when @mentioned in group (not auto-spam every message).

## Key Finding
ResearchClaw was spamming the O-Lab group because `requireMention: false` was set in `openclaw.json`.

## Fix Applied
**File:** `~/.openclaw/openclaw.json`
```json
"groups": {
  "*": {
    "requireMention": true   // was: false
  }
}
```

## Verification
```bash
# Check current setting
grep requireMention ~/.openclaw/openclaw.json

# Restart gateway
cd ~/.openclaw && npx openclaw gateway restart

# Verify bot only responds when @mentioned
# Send message WITHOUT @mention → no response
# Send message WITH @mention → responds
```

## Commands Reference
```bash
cd ~/.openclaw && npx openclaw gateway restart   # Restart gateway
npx openclaw status                             # Check status
tail -30 ~/.openclaw/logs/gateway.log          # View logs
```

## GitHub Repo Sync Status (as of session)
- Wiki at `/Volumes/Storage-1/Hermes/wiki` is independent git repo
- Pushed to `https://github.com/tuananh4865/my-llm-wiki`
- Hermes root git DELETED to prevent wrong repo push
- Latest commit: `5790ff9 [auto] session state sync 2026-05-18 16:18`