# Telegram Bot-to-Bot Threads Reference

## Thread Format
```
telegram:-1003764041476:603
```
- Chat ID: `-1003764041476` (NEGATIVE for supergroups)
- Thread ID: `603`

## Channel Directory Entry
```json
{
  "id": "-1003764041476:603",
  "name": "O-Lab / topic 603",
  "type": "group",
  "thread_id": "603"
}
```

## Bot Privacy Mode (CRITICAL - UPDATED 2026-05-04)

### Problem: Two distinct issues from privacy mode

**Issue 1: Can't read messages**
- Bot receives messages from itself but not from other users
- "can_read_all_group_messages: false — privacy mode enabled"

**Issue 2: Auto-responds to ALL messages WITHOUT @mention** (Tuấn Anh's reported issue)
- Symptom: "Các em vẫn đang tự trả lời mà không cần mention"
- Bot responds to any message in the group, not just @mentions
- This happens because privacy mode restricts what the bot CAN see, but in restricted mode the bot will respond to any message it CAN see

### Fix (MUST do for each bot):
1. Open @BotFather
2. Send `/mybots`
3. Select the bot (e.g., @ClawdBotZ1, @Researcher_Clawd_Bot)
4. → Bot Settings → Privacy → **Disable**

**Bots affected (2026-05-04)**: @ClawdBotZ1, @Researcher_Clawd_Bot — both needed privacy disabled

After disabling, bots will ONLY respond when:
- Explicitly @mentioned
- Replied to directly
- Sent as a direct message (DM)

## API Retry Behavior
**MiniMax API timeout** causes retry loops:
```
⏳ Retrying in 2.3s (attempt 1/3)...
⏳ Retrying in 5.7s (attempt 2/3)...
⚠ Max retries (3) exhausted — trying fallback...
❌ API failed after 3 retries — Connection error.
```

**Mitigation**: 
- Have fallback provider configured (OpenAI/Anthropic)
- Or wait for MiniMax to recover

## Stuck Bot Recovery (2026-05-04)
When a bot is stuck in retry loop due to API timeout:
1. Find wrapper PID: `ps aux | grep "research\|84977\|85293"`
2. Kill wrapper + bot: `kill <wrapper_pid> <bot_pid>`
3. Verified: killed PID 84977 (ResearchClaw) + 85293 (auto-restart wrapper)

## Verified (2026-05-04)
- ✅ Bot-to-bot @mention in same thread WORKS
- ✅ `send_message` to `telegram:-1003764041476:603` delivers to thread
- ✅ Both bots must be members of the group
- ✅ Privacy mode must be disabled for cross-bot reading
- ⚠️ MiniMax API timeout causes extended retry loops
- ⚠️ API timeout = bot stuck forever in retry → must kill manually

## Stuck Bot Recovery — Kill Research Agent (2026-05-04)

When ResearchClaw/Researcher_Clawd_Bot is stuck in retry loop:

```bash
# Step 1: Find the process
ps aux | grep -i "research-lead\|clawd" | grep -v grep

# Example output:
# tuananh4860  86556   ... ./venv/bin/python -m hermes_cli.main --profile research-lead gateway run --replace
# tuananh4860  86553   ... /bin/bash -lic set +m; cd ~/.hermes/hermes-agent && ./venv/bin/python ...

# Step 2: Kill both wrapper AND bot process (both need killing)
kill -9 86556 86553

# Step 3: Verify they're gone
ps aux | grep -i "research-lead" | grep -v grep
# Should return empty
```

**Key insight**: Both the wrapper bash process (86553) AND the python gateway process (86556) must be killed. Killing only the wrapper leaves the gateway orphan; killing only the gateway lets the wrapper restart it.
