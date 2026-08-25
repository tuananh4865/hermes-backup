---
title: Multi-Gateway Same-Bot-Token Conflict (session 2026-07-07)
created: 2026-07-07
type: reference
tags: [gateway, telegram, duplicate-process, profile-binding, model-override]
confidence: high
relationships: [gateway-manager, hermes-config-edit, hermes-agent, telegram-flood-control-diagnosis, channel-adapter-diagnosis]
---

# Multi-Gateway Same-Bot-Token Conflict — 2026-07-07 Capture

## Session context

User session began with three settings anh asked em to verify (model M3 default, reasoning xhigh, Telegram `require_mention` false) — confirmed all three were correct in `~/.hermes/config.yaml`. Then immediately anh reported:

> "nhưng mà nó đang báo là model minimax m2.7 không phải m3, và anh phải mention trong nhóm thì nó mới trả lời, check lại xem tại sao nó lại bị!!! hoặc restart gateway tele đi"

(Translation: but it's reporting model M2.7 not M3, and anh has to @mention in the group before it replies, check why it's broken! or restart the telegram gateway.)

→ User already knew the root cause was at the gateway layer, not config. The task was: **diagnose runtime state** and **propose kill-restart menu**, not edit config.

## Session evidence (verbatim from `ps aux`)

```
PID    ELAPSED  COMMAND
860    08:43:35 python -m hermes_cli.main --profile content-director gateway run --replace
9743   00:13:21 python -m hermes_cli.main                              gateway run --replace
```

Two gateway processes:
1. **`--profile content-director`** — PID 860, ELAPSED `08:43:35` (8 hours 43 minutes, started ~14:02 yesterday 06/07)
2. **default** — PID 9743, ELAPSED `00:13:21` (13 minutes, started this morning ~11:00)

## Profile model resolution

`~/.hermes/config.yaml` (parent):
```yaml
model:
  default: MiniMax-M3
  provider: minimax
```

`~/.hermes/profiles/content-director/config.yaml`:
```yaml
model:
  default: MiniMax-M2.7     ← override
  provider: minimax
```

`~/.hermes/profiles/default/`: doesn't exist (default profile uses parent config).

## Telegram bot token

`~/.hermes/.env` has one `TELEGRAM_BOT_TOKEN` line. Both PIDs read from this same `.env` → **both registered the same bot with Telegram Bot API** → race for every `getUpdates` long-poll.

The wrong-model symptom is exactly what happens when `--profile content-director` wins the race for a particular update: that PID's Python process loaded `MiniMax-M2.7` as the default model at gateway startup. The post-`/new` banner shows whatever model the replying process is bound to.

## Same-root-cause = require_mention in groups

Why both symptoms appear together (wrong model + bot ignoring non-mention messages in group): same PID 860 wins most group updates because it's been running longer and has the longer-polling session. Its effective config:

- `model.default: MiniMax-M2.7`
- The `require_mention: false` setting comes from parent config.yaml (Telegram section), but profile-binding can also affect HOW the Telegram adapter reads its `require_mention` (it goes through `gateway/config.py` deep-merge logic — see `hermes-config-edit` Pitfall #8). The mismatch between "I see require_mention false in parent" and "bot requires @mention in group" is also part of the same runtime drift.

## The 4-option fix menu delivered to user

Em did NOT auto-kill (an 8h43m-old PID could have pending sessions). Instead em delivered a menu:

| Option | Action | When |
|--------|--------|------|
| A | Kill PID 860 (stale content-director), keep PID 9743 (default) | User wants default-profile behavior — **recommended** |
| B | Kill PID 9743, keep PID 860 (content-director) | User is intentionally running a profile-specific stack |
| C | Update profile content-director config.yaml → MiniMax-M3, restart both | User wants BOTH running on same model |
| D | Stop BOTH, restart via `~/.hermes/run_hermes_gateway.sh` (default) | Clean slate after debugging |

Em recommended **A** because: parent config says M3 + agent should behave per parent. Killing the 8h-stale PID eliminates the bot-token race entirely (one PID owns the token now).

## Verification commands (the right ones)

```bash
# 1. List every gateway process
ps aux | grep -E "hermes_cli.main.*gateway" | grep -v grep

# 2. Per-PID profile binding
for pid in $(pgrep -f "hermes_cli.main.*gateway"); do
  echo "=== PID $pid ==="
  ps -p "$pid" -o pid,etime,command
  echo "Profile: $(ps -p "$pid" -o command | grep -oE -- '--profile [^\s]+' || echo default)"
done

# 3. Effective model per profile
grep -E "^  default:" "$HOME/.hermes/profiles"/*/config.yaml "$HOME/.hermes/config.yaml" 2>/dev/null
```

A correct fix is one where after kill -9 of the stale PID + restart of one default gateway, sending a NEW Telegram message shows in the post-`/new` banner the same model as `~/.hermes/config.yaml`.

## Anti-patterns that did NOT happen (but could have)

1. **Don't auto-kill an 8h+ PID without asking user.** The PID could be holding a long-running cron iteration loop or a finalized multi-turn session. Ask first.
2. **Don't just edit `~/.hermes/config.yaml`'s `model.default` and assume it propagates** — `--profile content-director` reads its own config.yaml at startup. Editing parent has zero effect on the running stale process.
3. **Don't claim "fixed" before killing the stale PID + restarting.** Even if config is correct, the running PID with the wrong profile binding is what answers Telegram.

## Side effects observed (none blocking)

- `.env` mtime 07:34 today — fresh, all secrets intact (verified 5-evidence gate from earlier turns: 866 bytes, mode 600, key length 125, MiniMax API live probe HTTP 200 with M3 in model list).
- 18 active crons healthy (verified separately by user earlier).
- No Telegram-message flood errors in `gateway.log` for this session.

## Related sessions

- 2026-07-02 21:24 (KarmaVid Telegram flood control) — sister concern but different root cause (Telegram API rate limit, not duplicate gateway)
- 2026-06-25 19:43 (log-vs-ground-truth misdiagnosis) — same defensive posture: verify ground truth BEFORE blaming a layer
- 2026-06-24 (env-permission regression) — yet another "tool says success, ground truth disagrees" pattern that was patched via hook
