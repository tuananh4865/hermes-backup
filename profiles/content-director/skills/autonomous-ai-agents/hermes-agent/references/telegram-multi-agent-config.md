# Telegram Multi-Agent Privacy & Mention Config

## The Problem
Multiple Hermes agents (Content Director, ClawdBotZ1, Research Lead) running on the same Telegram supergroup were ALL responding to every message — even without being @mentioned.

## Root Cause
Two-layer issue:
1. **BotFather Privacy Mode was DISABLED** → Telegram forwards ALL messages to the bot (not just @mentions)
2. **`require_mention: true` was in the WRONG section** — under `discord:` instead of `telegram:`

## The Fix (in config.yaml)

```yaml
platforms:
  telegram:
    require_mention: true    # Must be here, NOT under discord:
  discord:
    require_mention: true     # Discord config stays separate
```

**Then restart the gateway:**
```bash
tmux kill-session -t hermes 2>/dev/null; sleep 1
cd ~/.hermes && ./run_hermes_gateway.sh &
```

## BotFather Privacy Mode Reference

| BotFather Setting | Telegram forwards... | require_mention needed? |
|-------------------|----------------------|------------------------|
| Privacy: **Enabled** (strict) | Only @mention messages | No (Telegram already filters) |
| Privacy: **Disabled** (permissive) | ALL messages | **Yes** (you must filter) |

**Key insight:** "Disable group policy" on BotFather = permissive mode = MORE messages sent to bot = MUST have `require_mention: true` in telegram config.

## Verification

```bash
# Check which profile is running which bot
ps aux | grep "gateway run" | grep -v grep

# Check config for require_mention
grep -n "require_mention" ~/.hermes/config.yaml

# Check Telegram platform config section
grep -A 10 "telegram:" ~/.hermes/config.yaml
```

## Multiple Profiles Pattern

Tuấn Anh runs multiple agents with separate profiles:
- `content-director` — Content Director bot
- `research-lead` — Research agent (currently killed/disable)
- `clawd` — ClawdBotZ1

Each profile has its own:
- `~/.hermes/profiles/<name>/config.yaml`
- `~/.hermes/profiles/<name>/.env` (with separate bot tokens)
- Gateway process

## Related
- [[hermes-agent]] skill — Gateway Manager section
- [[tiktok-content-director]] skill — Tuấn Anh's TikTok workflow
