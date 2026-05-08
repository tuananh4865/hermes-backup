# Telegram Bot-to-Bot Thread Communication

## Discovery (2026-05-04)

Telegram @mention does NOT trigger bots — only notifies users reading the chat.
True bot-to-bot communication requires direct message sending.

## Target Format for Supergroup Threads

```
telegram:-1003764041476:603
```

- **Negative chat ID** for supergroups (e.g., `-1003764041476`)
- **Thread ID** appended after colon (e.g., `603`)
- Full format: `platform:chat_id:thread_id`

## Verified Working

| Direction | Format | Status |
|-----------|--------|--------|
| Content Director → Thread 603 | `telegram:-1003764041476:603` | ✅ |
| Bot receives @mention | Any bot in same thread | ✅ (receives update, not triggered by mention) |
| Direct bot-to-bot DM | `telegram:chat_id` | ✅ |

## ClawdBotZ1 / @ClawdZ1E_Bot

- Username: `@ClawdZ1E_Bot`
- Persona name: `ClawdBotZ1` or `ResearchClaw`
- Profile: `research-lead` at `~/.hermes/profiles/research-lead/`
- Token: `8706108095:AAGByOUlkf1_tjmun0bzKoif-K-gsSnyrd0` (Researcher_Clawd_Bot)

## Multi-Agent Setup (O-Lab Thread 603)

- **Content Director** (current bot) — TikTok scripts
- **@ClawdZ1E_Bot** (ClawdBotZ1) — Research bot  
- **@Researcher_Clawd_Bot** — Research Lead (same token as ClawdBotZ1)

All 3 can collaborate in thread 603 of O-Lab supergroup.
