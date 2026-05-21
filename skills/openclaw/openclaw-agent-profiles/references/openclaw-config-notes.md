# OpenClaw Config Notes (2026-05-21)

## Bot Tokens (Production)
| Bot | Token | Username |
|-----|-------|----------|
| ResearchClaw | `8706108095:AAGByOUlkf1_tjmun0bzKoif-K-gsSnyrd0` | @ClawdZ1E_Bot |
| TechLead | `8497520334:AAHpProGEY6UXsnfRpemBn7IYKRvoLcdx90` | @TechLead_ClawBot |

## Group Chat ID
- Company group: `-5195161709` (NOT `-1005195161709`)

## Config Location
- Main config: `~/.openclaw/openclaw.json`
- Backup: `~/.openclaw/openclaw.json.bak`
- Workspace for techlead: `~/.openclaw/workspace-techlead/`

## Startup
```bash
# Start gateway
cd ~/.openclaw && node /Users/tuananh4865/.npm/_npx/8718c3904bb5fece/node_modules/openclaw/dist/index.js gateway --port 18789

# Health check
curl http://localhost:18789/health
```

## Known Issues
- `bindings.match.peer` structure causes "Invalid input" error — avoid complex binding configs
- OpenClaw gateway may be managed by launchd on macOS — check with `lsof -i :18789`
