# Hermes Multi-Gateway × Profile Collision Playbook

**Session-captured: 2026-07-07** — Tuấn Anh reported two Telegram symptoms that looked unrelated but traced to the same root: "model M2.7 instead of M3" + "have to @mention the bot in groups".

## TL;DR — The 3-Signal Pattern

| Symptom in Telegram | What user sees | Root cause | One-line fix |
|---|---|---|---|
| "Model: MiniMax-M2.7" in `/new` banner | Wrong model displayed | Profile-scoped `model.default` overrides `~/.hermes/config.yaml` | `hermes model` in the active profile, OR delete the profile |
| Bot ignores group messages without @mention | "I have to ping it" | Two gateways running against the same Telegram bot token | `ps aux \| grep hermes` → kill all but one |
| Different answers depending on group vs DM | Intermittent / confusing | One of N gateways answers; race condition | Same as above — single gateway |

## Signal 1: Multi-Gateway Bot-Token Collision

**Symptom.** User reports "group mention no longer works" or "answers are inconsistent between DMs and groups". `hermes doctor` looks fine. Gateway log is quiet.

**Diagnosis (3 commands):**
```bash
ps aux | grep "hermes_cli.main" | grep -v grep
# → look for >1 rows, especially any containing "--profile"

grep -E "require_mention" ~/.hermes/config.yaml
# → if false but user can't talk in groups, suspect a stale gateway

grep -E "MINIMAX|^[A-Z_]+=" ~/.hermes/.env | sed 's/=.*/=<SET>/' | wc -l
# → confirms tokens all present
```

**Root cause.** Telegram Bot API uses long-polling. Two `python -m hermes_cli.main gateway run` processes sharing one `TELEGRAM_BOT_TOKEN` race for `getUpdates()`:
- The first to poll steals the update.
- The second may throw `terminated by other getUpdates request` and idle.
- Behavior becomes non-deterministic: "which gateway replied" depends on process scheduling.

**Confounders:**
- PID 860 (older, `--profile content-director`) running M2.7
- PID 9743 (newer, no profile flag) running M3
- User sees M2.7 = the older gateway won the last race.
- User can't talk in groups = the older gateway's profile has `require_mention: true` overriding the default's `false`.

**Fix recipe:**
1. List all PIDs: `ps aux | grep "hermes_cli.main" | grep -v grep`
2. For each non-canonical PID, identify whether it's a user-intentional `--profile <name>` instance:
   - Yes (e.g. a long-running cron-loop profile) → `kill <pid>` and restart cleanly with `--profile`
   - No (orphan from a previous `/reset` that forgot to clean up) → `kill <pid>`
3. Restart with one canonical gateway:
   ```bash
   # foreground
   hermes gateway run --replace
   # OR background
   nohup hermes gateway run > ~/.hermes/logs/gateway.log 2>&1 &
   ```
4. Verify: `ps aux | grep "hermes_cli.main" | grep -v grep | wc -l` → must be `1`.

**Pinned skills often hide duplicates.** Loop-style workers (e.g. `content-director` loop goal) register their own gateway. If you `kill` it without unpinning, the cron eventually respawns it. Check `hermes cron list` BEFORE killing profile-bound gateways.

## Signal 2: Profile-Scoped Model Override

**Symptom.** User sets `model.default: MiniMax-M3` in `~/.hermes/config.yaml`, restarts gateway, but Telegram `/new` banner still shows `MiniMax-M2.7`. `hermes config` correctly shows M3. Agent's own session sees M3.

**Root cause.** Each profile under `~/.hermes/profiles/<name>/` has its own `config.yaml`. The `--profile <name>` flag (used by gateway instances) loads that profile's config INSTEAD of the root one. The profile's `model.default` is what wins.

**Where to look:**
```bash
ls ~/.hermes/profiles/
# → _shared/ _template/ default/ code-reviewer/ ... 11+ profiles

for p in ~/.hermes/profiles/*/config.yaml; do
  echo "=== $p ==="
  grep -A 3 "^model:" "$p" | head -5
done
# → shows which profile sticks to which model
```

**Fix options:**
- **Edit the profile's config** (preserve the per-profile tooling like skills/auth, just update model)
- **Delete the profile** (if it's truly redundant — and verify nothing references it first)
- **Restart with explicit `--profile default`** to force root config load

**Always verify post-fix:**
```bash
hermes config | grep -i "model\|provider" | head -5
# then in Telegram: /new → banner shows the right model
```

## Signal 3: Profile Proliferation Audit

**Symptom.** `/Users/tuananh4865/.hermes/profiles/` has 12+ entries but the user only ever interacts with one. Profiles eat disk (each holds a full venv, skills cache, sessions.db). Stale profiles leak state and confuse diagnostics.

**Audit recipe:**
```bash
# 1. Total + size per profile
ls ~/.hermes/profiles/
du -sh ~/.hermes/profiles/*/ | sort -h
# → typically the most-used profile is ~150K, cron-loop profiles ~30-50M each

# 2. What references each profile?
hermes cron list | grep -E "profile:|--profile"
# → if a cron job references a profile, killing it breaks the cron

# 3. Which profile does each running gateway use?
ps -eo pid,etime,command | grep "hermes_cli.main" | grep -v grep
# → look for "--profile <name>" in the command line
```

**When the user says "delete unused profiles" — checklist before rm -rf:**
1. `hermes cron list` → confirm zero crons reference each candidate
2. `ps -eo pid,command | grep "hermes_cli.main" | grep "<profile-name>"` → confirm zero live gateways
3. **`mv` to `/tmp/hermes-profiles-backup-<date>/` BEFORE deleting** — profiles contain sessions.db, skills, custom auth.json. Lost work is unrecoverable.
4. After deletion: `kill <gateway-pid>` for each killed profile (else orphan gateway lingers).
5. Restart single canonical gateway.

**Recommended cleanup (when only `default` is in use):**
```bash
# 1. Kill all running gateways
pkill -f "hermes_cli.main gateway"

# 2. Move (not delete) profiles to backup
mkdir -p /tmp/hermes-profiles-backup-$(date +%Y%m%d)
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  case "$name" in
    _shared|_template|default) ;; # keep
    *) mv "$p" "/tmp/hermes-profiles-backup-$(date +%Y%m%d)/$name" ;;
  esac
done

# 3. Restart single gateway
nohup hermes gateway run > ~/.hermes/logs/gateway.log 2>&1 &

# 4. Verify
ps aux | grep "hermes_cli.main" | grep -v grep | wc -l   # → 1
hermes config | grep -A 2 "^model:"
```

## Anti-Pattern: Treating the `/new` Telegram Banner as a User Task

**Symptom caught in session.** After a `/new` reset in Telegram, Hermes prints a banner like:
```
✨ Session reset! Starting fresh.
◆ Model: MiniMax-M2.7
◆ Provider: minimax
◆ Context: 204K tokens (detected)
✦ Tip: DingTalk uses Stream Mode — no webhooks or public URL needed.
```

**Mistake.** An inexperienced agent reads this as "user wants me to switch to M2.7" or "user is configuring DingTalk" and starts a configuration task. The user then has to clarify: "đó là tin nhắn anh nhận được khi /new trong tele" (it's just the system banner).

**Rule.** Any message whose content is **bracketed by `✨ / ◆ / ✦` symbols** OR **prefixed with "Session reset", "Starting fresh", "Context:"** is a **system banner**, NOT user input. Acknowledge briefly (≤2 sentences) and ask what the user actually wants.

**Sibling pattern.** Same applies to:
- `<OUT-OF-BAND USER MESSAGE>` blocks mid-tool — those ARE user messages
- `[CONTEXT COMPACTION]` markers — system, not user
- Tool output footers like "On branch main, your branch is ahead by N commits" — informational, not actionable

The discriminator: **real user content has natural-language intent**. Templates/banners have symbols and structured fields.

## Cross-References

- `references/telegram-group-no-mention.md` — sibling, scoped to the `require_mention` half of the bug
- `references/multi-agent-setup.md` — for the "I want profiles back later" path
- `~/.hermes/memories/USER.md` [PREFERENCES] → "Solution First, Explanation Never" rule applies to fix reports

## When to Capture This Pattern

Capture when ANY of:
- User reports "wrong model in Telegram" but `hermes config` shows correct model
- User reports "had to mention the bot in a group" but `require_mention: false` in config
- `ps aux | grep hermes | grep -v grep | wc -l` returns > 1
- Multi-profile setup has existed for >30 days without explicit user request
