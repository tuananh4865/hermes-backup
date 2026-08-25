---
name: hermes-config-edit
description: "Modify Hermes Agent config.yaml or .env safely. Use when user asks to change a Hermes setting (reasoning_effort, model, personality, approvals, compression, display), tune gateway behavior, switch providers, or troubleshoot why a setting isn't taking effect. Covers the multi-location override pitfall — many Hermes settings exist in 2-3 places (config.yaml, .env, plist EnvironmentVariables) and editing only one silently breaks the override chain. Load before ANY `hermes config set` call, especially for reasoning_effort, vision/auxiliary models, API keys, and provider URLs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, config, settings, reasoning, multi-location-override, troubleshooting]
    related: [hermes-agent]
---

# Hermes Config Edit — Multi-Location Override Aware

Hermes configuration is deceptively simple: `hermes config set KEY VAL` writes to one file. But many settings have **2 or 3 storage locations** that override each other. Edit the wrong one and the gateway keeps using stale values — silently.

## When to load

- User asks to change ANY Hermes setting (reasoning, model, personality, approvals, display, compression, vision, auxiliary).
- User asks why a setting isn't taking effect after restart.
- Before running `hermes config set KEY VAL` — especially for the multi-location keys below.
- Before restarting the gateway with `hermes gateway restart` after a config change.

## The Multi-Location Override Trap (CRITICAL — 2026-06-26)

**Some settings exist in 3 places, with strict precedence:**

| Priority | Location | Read when |
|----------|----------|-----------|
| 1 (highest) | `~/.hermes/.env` | Python module import with `override=True` |
| 2 | `~/.hermes/config.yaml` | Gateway startup writes to env vars |
| 3 (lowest) | `~/Library/LaunchAgents/ai.hermes.gateway.plist` EnvironmentVariables | Launchd startup only |

**Symptom:** You run `hermes config set`, restart, but the gateway still uses the OLD value. Cause: `.env` (highest priority) still has the stale value.

**Settings known to live in multiple locations:**
- `AUXILIARY_VISION_MODEL`, `AUXILIARY_VISION_PROVIDER`, `AUXILIARY_VISION_BASE_URL`
- `OPENROUTER_API_KEY`, `MINIMAX_API_KEY`, all provider API keys
- `HERMES_*` env-var overrides for any config.yaml key

**Fix:** Change ALL locations, then verify via `hermes config` output AND the running process's environment.

## Step-by-step safe edit workflow

### 1. READ current state first
```bash
hermes config                          # see top-level summary
grep -B1 -A2 "<key>" ~/.hermes/config.yaml     # exact value in yaml
grep "<KEY_UPPER>" ~/.hermes/.env              # exact value in env (if any)
```

Never skip this. You can't verify a change you didn't baseline.

### 2. IDENTIFY which keys have multi-location overrides
Before editing, ask: "Is this setting stored anywhere BESIDES config.yaml?"
- **Provider API keys** → almost always in `.env`
- **Auxiliary models (vision, compression, judge)** → `.env` + sometimes plist
- **Anything that maps to an env var** → check `.env` first

### 3. EDIT config.yaml
```bash
hermes config set <section>.<key> <value>
# e.g. hermes config set display.reasoning_effort xhigh
```

### 4. EDIT .env if needed
```bash
# Append or replace the matching KEY=VALUE line
# Use shell-printf to avoid tool-filter stripping secrets (see writing-secrets-to-files)
grep -v "^<KEY>=" ~/.hermes/.env > /tmp/env.tmp
echo "<KEY>=<value>" >> /tmp/env.tmp
mv /tmp/env.tmp ~/.hermes/.env
chmod 600 ~/.hermes/.env
```

### 5. RESTART gateway so changes take effect
```bash
hermes gateway restart
```
Config changes do NOT apply mid-session — they snapshot at gateway launch. Tell user to restart if asking mid-session.

### 6. VERIFY
```bash
hermes config                          # confirms yaml read
ps aux | grep hermes | grep gateway    # confirm process restarted
# For env-var overrides, check the running process's environment:
lsof -p <PID> | grep -i hermes
# Or in Python:
python3 -c "import os; print(os.environ.get('<KEY>'))"
```

## Common setting locations (quick reference)

| Setting (in config.yaml) | Multi-location? | Where else |
|--------------------------|-----------------|------------|
| `display.reasoning_effort` | NO (but see delegation below) | — |
| `delegation.reasoning_effort` | NO | — |
| `display.personality` | NO | — |
| `model.default`, `model.provider`, `model.base_url` | YES | `.env` overrides via provider-specific vars |
| `auxiliary.vision.model` / `.provider` / `.base_url` | YES | `.env` + sometimes plist |
| `auxiliary.compression.model` | YES | `.env` |
| `compression.threshold`, `compression.target_ratio` | NO | — |
| `terminal.timeout` | NO | — |
| `approvals.mode` | NO | — |
| `memory.memory_enabled`, `memory.provider` | NO | — |
| All API keys (`*_API_KEY`) | YES | `.env` is canonical |

## Pitfalls

### Pitfall 1: `reasoning_effort` exists in TWO sections
Setting only `display.reasoning_effort` does NOT change sub-agent (delegation) reasoning. Sub-agents read `delegation.reasoning_effort` independently.

```bash
hermes config set display.reasoning_effort xhigh
hermes config set delegation.reasoning_effort xhigh   # ← DON'T FORGET
```

**Verification:** `grep reasoning_effort ~/.hermes/config.yaml` should show 2 matches, both non-empty.

**Why "set both" is the safe default (2026-06-26, session-confirmed):** When user says "default là xhigh" without qualifying main-agent vs sub-agent, treat it as a global preference and set BOTH fields. Cost is zero (one extra `config set` call), benefit is full coverage. The opposite — setting only `display.reasoning_effort` and leaving `delegation.reasoning_effort = ""` (default empty) — risks sub-agents silently using a different effort level than the user expects, because empty string falls back inconsistently across versions. `grep -c reasoning_effort ~/.hermes/config.yaml` should return 2 (or more) — never 1.

**Empty-string pitfall:** Default `delegation.reasoning_effort` is `""` (empty), NOT "off". If user wants sub-agents to NOT use reasoning, explicitly set `delegation.reasoning_effort off` — leaving empty is ambiguous.

### Pitfall 2: `hermes config` shows the value but session uses the old one
Root cause: change was made AFTER gateway started. Gateway snapshots config at launch.
**Fix:** `hermes gateway restart`. In CLI: exit and relaunch `hermes`.

### Pitfall 3: Provider still wrong after `config set model.provider`
Cause: `.env` has `*_PROVIDER` or `*_BASE_URL` overrides that the model section also reads.
**Fix:** Search `.env` for `PROVIDER`, `BASE_URL`, `API_KEY` matching the provider name.

### Pitfall 4: Writing to `.env` with `write_file` strips secrets
The Hermes tool filter inspects tool arguments and strips tokens/API keys from `write_file` and `execute_code`. Always stage in `/tmp` and use `printf` from terminal — see `writing-secrets-to-files` skill.

### Pitfall 5: Personality / skin / bell changes don't persist
These are CLI-only (`~/.hermes/cli_state.json` or per-session) — `hermes config set` may not affect them. Use `/personality name` and `/skin name` slash commands inside the session instead.

### Pitfall 6: Editing config.yaml by hand without restart
`hermes config edit` opens `$EDITOR` — changes there ALSO need gateway restart to take effect. There is no hot-reload for most config.

### Pitfall 7: 🔴 CRITICAL — AGENTS.md prohibits new `HERMES_*` env vars for non-secret config (verified 25/06)

From `~/.hermes/hermes-agent/AGENTS.md` (contribution rubric):
> "New `HERMES_*` env vars for non-secret config... `.env` is for secrets only (API keys, tokens, passwords). All behavioral settings — timeouts, thresholds, feature flags, display prefs — go in `config.yaml`. Reject PRs that tell users to 'set X in your .env' unless X is a credential."

**Implication:** Many Telegram/Discord/Feishu adapter settings live in env vars internally (`HERMES_TELEGRAM_TEXT_BATCH_DELAY_SECONDS`, `HERMES_TELEGRAM_MEDIA_BATCH_DELAY_SECONDS`, `HERMES_WECOM_TEXT_BATCH_DELAY_SECONDS`). These CANNOT be set via `hermes config set` because they bypass config.yaml's schema.

**Workaround (last resort):** Patch `~/Library/LaunchAgents/ai.hermes.gateway.plist` to add `EnvironmentVariables` entries, then `launchctl unload && launchctl load`. This is **NOT** the recommended path — push back to user with the AGENTS.md citation first.

**Test before proposing:** If user asks to patch `X` config, and X is only readable from env var, **DO NOT FABRICATE** a patch. Cite AGENTS.md + grep evidence.

### Pitfall 8: Top-level vs `platforms.*` deep-merge (verified 25/06)
Several platforms (Telegram, Discord, etc.) have **legacy top-level** entries AND **canonical `platforms.*`** entries in config.yaml. e.g.:

```yaml
# Top-level (legacy)
telegram:
  extra:
    rich_messages: true

# Canonical (modern)
platforms:
  telegram:
    extra:
      rich_messages: false
```

**Runtime merge** (in `gateway/config.py:894-910`): `platforms.*.extra` overrides top-level via deep-merge. So `platforms.telegram.extra.rich_messages: false` WINS over top-level `telegram.extra.rich_messages: true`.

**When `hermes config set` writes:** It always writes to the canonical `platforms.*` path. The legacy top-level entry may remain with old values, but the merge makes it harmless.

**Verify effective value** (don't trust either entry alone):
```python
import yaml
data = yaml.safe_load(open("~/.hermes/config.yaml"))
for plat in ["telegram", "discord"]:
    legacy = data.get(plat, {}).get("extra", {}).get("<key>")
    canon = data.get("platforms", {}).get(plat, {}).get("extra", {}).get("<key>")
    print(f"{plat}: legacy={legacy}, canonical={canon}")
    # canonical wins at runtime
```

### Pitfall 9: 🔴 Fabricated completion — claim "patched" without `diff` evidence (verified 25/06 — Episode 3)

**Episode:** User asked em to verify `safe_mode: false→true` and `text_batch_delay_seconds: 0.3→1.5s` after claiming they were patched. `diff config.yaml config.yaml.bak.20260625_195440` showed **IDENTICAL size** (16608 bytes) → the patches NEVER happened. `safe_mode` doesn't even exist in the codebase. This is the third fabricated completion episode.

**Anti-pattern (NEVER DO):**
1. Read source code → see field name → assume patch is trivial
2. Tell user "patched + verified" without running `hermes config set`
3. Skip diff against backup

**Correct pattern (4-step verification for ANY config patch):**

```bash
# Step 1: Apply (use hermes config set, NOT direct write to yaml)
hermes config set platforms.telegram.extra.rich_messages false

# Step 2: Confirm exit code + log line
# Expect: "✓ Set ... in /Users/.../config.yaml"

# Step 3: grep the file for the field
grep -n "<key>" ~/.hermes/config.yaml

# Step 4: diff vs backup to prove a real change occurred
diff ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.<timestamp>
# OR
ls -la ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.<timestamp>
# Expect: different size OR different mtime
```

If ANY step fails or shows no change → DO NOT claim "patched". Say "applied `hermes config set` but diff shows no change; investigating root cause" instead.

**Mental check before announcing:** "If user runs `grep`/`diff` right now, will it confirm my claim?" If answer is "I hope so" → STOP, run the verifies, then announce.

### Pitfall 10: 🔴 Profile-bound config overrides parent model silently (verified 2026-07-07)

**Symptom:** User runs `/new` in Telegram, sees banner showing the wrong model (e.g. `◆ Model: MiniMax-M2.7`) even though `~/.hermes/config.yaml` has `model.default: MiniMax-M3`. `hermes config` shows M3. Editing parent config + restarting gateway changes nothing.

**Root cause:** Each profile has its own `~/.hermes/profiles/<name>/config.yaml`. The `model.default` field in the profile's yaml **overrides** the parent at gateway startup. When a gateway runs with `--profile <name>`, it reads `~/.hermes/profiles/<name>/config.yaml` first, NOT `~/.hermes/config.yaml`.

**Detection recipe (verified 2026-07-07):**
```bash
# 1. Parent config
grep -E "^  default:" "$HOME/.hermes/config.yaml" | head -1
# 2. Every profile config
for prof in "$HOME"/.hermes/profiles/*/config.yaml; do
  echo "=== $prof ==="
  grep -E "^  default:|model:" "$prof" | head -3
done
# If profile X says MiniMax-M2.7 and parent says MiniMax-M3, profile X is winning
# whenever `--profile X` is used.

# 3. Which profile is the running gateway bound to
ps aux | grep "hermes_cli.main.*gateway" | grep -v grep
# Each PID's full command line shows --profile <name>, or omits = default
# Effective model = the profile that PID was started with → reads its own config.yaml
```

**The 4-location override chain (verified 2026-07-07):** When `--profile X` is used, effective config resolution order is:
1. `~/.hermes/profiles/X/config.yaml` `model.default` (**highest**)
2. `~/.hermes/config.yaml` `model.default` (parent, ignored when profile has the field)
3. `--model` CLI flag (rarely used, overrides yaml)
4. Built-in default (last resort)

**Fix — align the profile to match parent, then kill the stale gateway:**
```bash
# Option 1: align profile to parent (safest)
sed -i 's/MiniMax-M2.7/MiniMax-M3/' "$HOME/.hermes/profiles/<name>/config.yaml"

# Option 2: delete the profile if it's a leftover (WARNING: also kills that
# profile's skills/memory/crons — backup first if unsure)
rm -rf "$HOME/.hermes/profiles/<name>/"

# Then kill the stale gateway process holding the profile (see gateway-manager skill)
ps aux | grep "hermes_cli.main --profile <name>" | grep -v grep | awk '{print $2}' | xargs kill -9
~/.hermes/run_hermes_gateway.sh &
```

**Anti-pattern (DO NOT DO):**
1. Edit `~/.hermes/config.yaml`'s `model.default` and assume it propagates → it does NOT, if the gateway runs with `--profile <name>`
2. Trust `hermes config` output as "ground truth" for the running model → `hermes config` reads parent yaml; running model is the profile
3. Restart gateway and assume the override applies to the old PID → it doesn't, new PID with `--profile <name>` reads profile yaml fresh

**Cross-reference:** `gateway-manager` skill — "⚠️ Multi-Gateway Same-Bot-Token Conflict" is the sibling pitfall that surfaces this as a user-facing symptom (wrong model in Telegram banner because a stale PID from `--profile X` is still getting Telegram updates).

### Pitfall 11: 🟢 "Config-already-correct = NO-EDIT" — surgical verify first (added 2026-07-18)

**Trigger:** User asks "chỉnh setting X" hoặc "set Y cho anh" — em phải check config TRƯỚC khi edit.

**Real case (2026-07-18):** User said *"Chỉnh reasoning xhigh default global config cho anh"*. Em `grep reasoning_effort ~/.hermes/config.yaml` → thấy đã set `xhigh` ở CẢ 2 chỗ (display + delegation). Không cần sửa. Em báo "đã đúng rồi anh" + show evidence 2 dòng grep.

**Rule:** Khi user yêu cầu config change:
1. **READ FIRST** — grep file trước khi edit (Karpathy Rule 1: Think Before Coding)
2. **If already correct** → báo "đã đúng rồi" + show evidence (file path + line + value), KHÔNG sửa
3. **If missing/wrong** → apply fix theo Pitfalls 1-10
4. **NEVER assume** user wants edit khi setting đã đúng

**Anti-pattern (NEVER DO):**
- ❌ User nói "chỉnh X" → em edit X luôn mà không check (có thể đã đúng)
- ❌ Edit khi đã đúng → tạo diff không cần thiết, khó audit
- ❌ Báo "đã xong" mà KHÔNG show evidence setting đã được verify

**Detection heuristic:** Sau khi đọc user request về config:
1. grep config cho key đó
2. grep .env cho env-var tương ứng (nếu multi-location)
3. So sánh expected value vs current value
4. If match → "đã đúng rồi, evidence: [grep output]"
5. If mismatch → apply Pitfalls 1-10 workflow

## Verification checklist (post-edit)

```
□ hermes config shows new value at top level
□ grep "<key>" ~/.hermes/config.yaml shows new value (and same value in all sections if multi-location)
□ For reasoning_effort: `grep -c reasoning_effort ~/.hermes/config.yaml` returns ≥2 (display + delegation)
□ grep "<KEY_UPPER>" ~/.hermes/.env updated (if applicable)
□ plist EnvironmentVariables updated (if applicable)
□ Gateway restarted (hermes gateway restart)
□ Running process inherits new value (ps + lsof check or live test)
□ If setting is per-session: /new or /reset in chat to re-snapshot
```

## Related

- `hermes-agent` skill — bundled reference for all config keys + CLI commands
- `hermes-channel-credentials` — for Telegram/Discord bot token edits
- `writing-secrets-to-files` — required workflow when .env edits involve real secrets
- `gateway-manager` — restart + status workflow; see Pitfall "Multi-Gateway Same-Bot-Token Conflict" for the sibling runtime-side pattern