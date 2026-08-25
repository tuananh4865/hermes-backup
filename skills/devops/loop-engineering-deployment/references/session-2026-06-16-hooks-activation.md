---
title: "Session 2026-06-16 (2nd) — Hermes Shell Hooks Activation + memory-curator + Cron Integration"
date: 2026-06-16
author: Hermes Agent
session_type: activation
related: session-2026-06-16-example.md, session-2026-06-16-profile-terminology.md
---

# Session 2026-06-16 (Round 2) — Activating Hooks + Adding 4th Profile + Cron Integration

## What was activated in this round

After the initial 5-component deployment earlier on 2026-06-16, the user said:
> "cả 3. verify từng cái rồi làm"

("All 3. Verify each one then do")

The 3 activation items were:
1. **Activate hook** — register shell hooks in `~/.hermes/config.yaml` so they auto-fire
2. **Create `memory-curator` profile** — 4th profile for the company (wiki/memory specialist)
3. **Hook into cron jobs** — make existing cron jobs log to their profile's state.md

## 1. Hermes Shell Hooks Activation

### Discovery: wrong event names

Initial attempt used `agent:end`, `session:start`, `session:end` (from the `hermes-agent.nousresearch.com/docs/user-guide/features/hooks` docs). All 3 hooks were silently rejected:

```bash
$ hermes hooks list
No shell hooks configured in ~/.hermes/config.yaml.
```

Investigation revealed two facts:

1. **The docs are wrong about what's in VALID_HOOKS.** The correct source is `hermes_cli/plugins/__init__.py`:
   ```python
   from hermes_cli.plugins import VALID_HOOKS
   print('\n'.join(sorted(VALID_HOOKS)))
   # → on_session_end, on_session_finalize, on_session_reset, on_session_start,
   #   post_api_request, post_approval_response, post_llm_call, post_tool_call,
   #   pre_api_request, pre_approval_request, pre_gateway_dispatch, pre_llm_call,
   #   pre_tool_call, subagent_start, subagent_stop, transform_llm_output,
   #   transform_terminal_output, transform_tool_result, api_request_error
   ```
2. **The `agent:end` event is BROKEN in gateway mode** (NousResearch/hermes-agent#14583, open as of 2026-06-16). It loads but never dispatches.

### Fix: use the right event names

Changed to 3 working events:

```yaml
hooks:
  on_session_start:    # Was: session:start (didn't exist)
    - command: "/Users/tuananh4865/.hermes/loop-engineering/hook_wrapper.sh --event on_session_start"
      timeout: 10
  on_session_end:      # Was: session:end (didn't exist)
    - command: "/Users/tuananh4865/.hermes/loop-engineering/hook_wrapper.sh --event on_session_end --output $RESPONSE"
      timeout: 15
  post_tool_call:      # Was: agent:end (broken in gateway mode)
    - command: "/Users/tuananh4865/.hermes/loop-engineering/hook_wrapper.sh --event post_tool_call --output $TOOL_RESULT --goal $TOOL_NAME"
      timeout: 30
hooks_auto_accept: true
```

### Allowlist format gotcha

Even after `hermes hooks test` returns exit 0, hooks show as "not allowlisted" until the JSON file is in the EXACT format Hermes expects.

**WRONG formats tried first:**

```json
{
  "entries": [
    {"command": "...", "events": ["..."], "added_at": "...", "reason": "..."}
  ]
}
```

```json
{
  "approvals": [
    {"event": "on_session_start", "command": "/path/to/script"}
  ]
}
```

**CORRECT format:**

```json
{
  "approvals": [
    {
      "event": "on_session_start",
      "matcher": null,
      "command": "/Users/tuananh4865/.hermes/loop-engineering/hook_wrapper.sh --event on_session_start"
    }
  ]
}
```

Key requirements:
- Top-level key is `"approvals"` (not `"entries"`)
- Each item MUST have `event` (string), `matcher` (null for non-pre/post_tool_call events), `command` (string with FULL command + args, not just path)
- `command` must match EXACTLY the `command:` field in config.yaml, including all `--flag value` args

Verify with:
```bash
$ hermes hooks doctor
✓ script exists and is executable
✓ allowlisted (approved ?)
✓ produced valid JSON on synthetic payload (exit=0, 0.033s)
All shell hooks look healthy.
```

### Hook wrapper script pattern

Used a bash wrapper instead of inline `python3 -c "..."` in YAML to:
1. Avoid YAML escaping nightmares (quotes, $ signs, newlines)
2. Make hooks testable standalone: `./hook_wrapper.sh --event on_session_start`
3. Set HERMES_HOME + HERMES_PROFILE env vars before exec

```bash
#!/bin/bash
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
HERMES_PROFILE="${HERMES_PROFILE:-default}"
export HERMES_HOME
export HERMES_PROFILE
exec python3 "$HERMES_HOME/loop-engineering/hook.py" "$@"
```

## 2. memory-curator Profile

### Why a 4th profile

Existing 3 profiles each had clear scope:
- `content-director` — TikTok content
- `research-lead` — Research
- `coder` — Code

**No profile for wiki/memory.** The orchestrator was being asked to do wiki ingestion directly, which is busywork.

### Creation via official Hermes CLI

```bash
hermes profile create memory-curator \
  --description "Manages wiki (Obsidian/Hermes), ingests content, updates memory entries, archives stale info, maintains knowledge graph for the company."
```

Output:
- Profile created at `~/.hermes/profiles/memory-curator/`
- 73 bundled skills synced
- Wrapper created at `~/.local/bin/memory-curator`

### SOUL.md customization

Auto-generated SOUL.md is generic ("You are Hermes Agent..."). Replaced with role-specific persona covering identity, mission, workflow, voice, tools, and anti-patterns.

### State.md init

Used `profile_state.py ensure memory-curator` to create `state.md` from the `_template/state.md` template.

### How memory-curator is invoked (workflow)

The orchestrator (default) routes to memory-curator via:
1. **Kanban** — assign tasks with `assignee="memory-curator"`
2. **Direct command** — `memory-curator chat "Ingest this URL..."`
3. **Cron** — wiki health check job (routes to memory-curator per the cron mapping)

## 3. Cron Job Hook Integration

### Discovery: no cron completion event

Audited Hermes cron source. Searched for hook event firing points — no matches. Cron runs the prompt as a normal agent conversation; no end-of-cron hook fires.

**No `on_cron_done` event in VALID_HOOKS either.** So shell hooks can't auto-fire on cron completion.

### Workaround: inject into the prompt

Appended a mandatory "Loop Engineering hook" section to each of 7 cron jobs' prompts:

```markdown
---

## 🔄 LOOP ENGINEERING HOOK (auto-appended YYYY-MM-DD)

**Mandatory:** Before delivering results, run this hook to log to state.md:

```bash
python3 ~/.hermes/loop-engineering/profile_state.py run <profile_name> "<goal summary>" 1 <PASS|FAIL> <score>
```

This hook is part of the system-wide Loop Engineering pattern. Don't skip it.
---
```

### Profile mapping per cron job

7 jobs mapped to 4 profiles:

| Job name | Profile | Rationale |
|----------|---------|-----------|
| `Hermes Daily Backup` | `default` | Infrastructure |
| `Hermes Autoresearch Nightly` | `research-lead` | Name contains "research" |
| `Hermes Agent X Research Daily` | `research-lead` | Name contains "research" |
| `Hermes Daily Session Review` | `default` | Cross-cutting |
| `Wiki Health Daily` | `memory-curator` | Wiki domain |
| `Wiki Memory Forget Daily` | `memory-curator` | Memory domain |
| `TikTok 5-Channel Nightly Monitor` | `content-director` | TikTok domain |

**Generalization rule for future cron additions:**
- `*Backup*`, `*Review*` → `default`
- `*Research*`, `*Autoresearch*`, `*X*` → `research-lead`
- `*Wiki*`, `*Memory*` → `memory-curator`
- `*TikTok*`, `*Monitor*` → `content-director`
- `*Coder*`, `*Code*` → `coder`

**Better long-term fix:** Have the orchestrator update each cron job's mapping when profiles change. For now, manual injection per deployment is acceptable.

## Final state after this round

```
Profiles (5): default, content-director, research-lead, coder, memory-curator
Hooks (3): all allowlisted, valid JSON, exit=0
  - on_session_start
  - on_session_end
  - post_tool_call
State files: 5 (one per profile) + 1 template
Cron jobs: 7 (all with loop engineering hook prompt section)
```

## Verification commands

```bash
# 1. All hooks healthy
hermes hooks doctor

# 2. All profiles present
hermes profile list

# 3. Each profile has state.md
ls ~/.hermes/profiles/*/state.md
ls ~/.hermes/profiles/default/state.md 2>/dev/null || ls ~/.hermes/state.md

# 4. All cron jobs have hook section
grep -c "LOOP ENGINEERING HOOK" ~/.hermes/cron/jobs.json  # Should be 7

# 5. State file actually gets written
HERMES_PROFILE=content-director python3 ~/.hermes/loop-engineering/hook.py \
  --event on_session_start
```

## Lessons encoded in skill

1. **Hermes shell hook event names** — added to Component 4 spec with VALID_HOOKS list and broken-`agent:end` warning
2. **Allowlist format** — added with WRONG vs CORRECT format examples
3. **Cron integration via prompt injection** — added as a "Cron Job Hook Integration" subsection
4. **`memory-curator` profile pattern** — explicit creation command documented

## What to do differently next time

- **Inject the loop-engineering hook into ALL cron jobs at cron creation time** (not retroactively). Save an `inject_cron_hooks.py` script for the skill's `scripts/` directory.
- **Verify hook event names against `VALID_HOOKS` BEFORE writing config.yaml.** Add a `hermes hooks validate` wrapper or just use `python3 -c "from hermes_cli.plugins import VALID_HOOKS; print(...)"` as a sanity check.
- **Document the memory-curator mapping for future profiles.** When the company gets a 5th profile, this skill's cron mapping table needs a row added.

## Related references
- `session-2026-06-16-example.md` — first deployment (5 components, terminology fix)
- `session-2026-06-16-profile-terminology.md` — why we use "Profile" not "Worker"
