---
name: kanban-worker
description: Pitfalls, examples, and edge cases for Hermes Kanban workers. The lifecycle itself is auto-injected into every worker's system prompt as KANBAN_GUIDANCE (from agent/prompt_builder.py); this skill is what you load when you want deeper detail on specific scenarios.
version: 2.1.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, collaboration, workflow, pitfalls, silent-recovery, artifact-verification]
    related_skills: [kanban-orchestrator, kanban-codex-lane, multi-agent-heartbeat]
---

# Kanban Worker — Pitfalls and Examples

> You're seeing this skill because the Hermes Kanban dispatcher spawned you as a worker with `--skills kanban-worker` — it's loaded automatically for every dispatched worker. The **lifecycle** (6 steps: orient → work → heartbeat → block/complete) also lives in the `KANBAN_GUIDANCE` block that's auto-injected into your system prompt. This skill is the deeper detail: good handoff shapes, retry diagnostics, edge cases.

## Workspace handling

Your workspace kind determines how you should behave inside `$HERMES_KANBAN_WORKSPACE`:

| Kind | What it is | How to work |
|---|---|---|
| `scratch` | Fresh tmp dir, yours alone | Read/write freely; it gets GC'd when the task is archived. |
| `dir:<path>` | Shared persistent directory | Other runs will read what you write. Treat it like long-lived state. Path is guaranteed absolute (the kernel rejects relative paths). |
| `worktree` | Git worktree at the resolved path | If `.git` doesn't exist, run `git worktree add <path> ${HERMES_KANBAN_BRANCH:-wt/$HERMES_KANBAN_TASK}` from the main repo first, then cd and work normally. Commit work here. |

## Tenant isolation

If `$HERMES_TENANT` is set, the task belongs to a tenant namespace. When reading or writing persistent memory, prefix memory entries with the tenant so context doesn't leak across tenants:

- Good: `business-a: Acme is our biggest customer`
- Bad (leaks): `Acme is our biggest customer`

## Good summary + metadata shapes

The `kanban_complete(summary=..., metadata=...)` handoff is how downstream workers read what you did. Patterns that work:

**Coding task:**
```python
kanban_complete(
    summary="shipped rate limiter — token bucket, keys on user_id with IP fallback, 14 tests pass",
    metadata={
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "decisions": ["user_id primary, IP fallback for unauthenticated requests"],
    },
)
```

**Coding task that needs human review (review-required):**

For most code-changing tasks, the work isn't truly *done* until a human reviewer has eyes on it. Block instead of complete, with `reason` prefixed `review-required: ` so the dashboard surfaces the row as needing review. Drop the structured metadata (changed files, test counts, diff/PR url) into a comment first, since `kanban_block` only carries the human-readable reason — comments are the durable annotation channel. Reviewer either approves and runs `hermes kanban unblock <id>` (which re-spawns you with the comment thread for any follow-ups) or asks for changes via another comment.

```python
import json

kanban_comment(
    body="review-required handoff:\n" + json.dumps({
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "diff_path": "/path/to/worktree",  # or PR url if pushed
        "decisions": ["user_id primary, IP fallback for unauthenticated requests"],
    }, indent=2),
)
kanban_block(
    reason="review-required: rate limiter shipped, 14/14 tests pass — needs eyes on the user_id/IP fallback choice before merging",
)
```

Use `kanban_complete` only when the task is genuinely terminal — e.g. a one-line typo fix, a docs change with no functional consequences, or a research task where the artifact IS the writeup itself.

**Research task:**
```python
kanban_complete(
    summary="3 competing libraries reviewed; vLLM wins on throughput, SGLang on latency, Tensorrt-LLM on memory efficiency",
    metadata={
        "sources_read": 12,
        "recommendation": "vLLM",
        "benchmarks": {"vllm": 1.0, "sglang": 0.87, "trtllm": 0.72},
    },
)
```

**Review task:**
```python
kanban_complete(
    summary="reviewed PR #123; 2 blocking issues found (SQL injection in /search, missing CSRF on /settings)",
    metadata={
        "pr_number": 123,
        "findings": [
            {"severity": "critical", "file": "api/search.py", "line": 42, "issue": "raw SQL concat"},
            {"severity": "high", "file": "api/settings.py", "issue": "missing CSRF middleware"},
        ],
        "approved": False,
    },
)
```

Shape `metadata` so downstream parsers (reviewers, aggregators, schedulers) can use it without re-reading your prose.

## Claiming cards you actually created

If your run produced new kanban tasks (via `kanban_create`), pass the ids in `created_cards` on `kanban_complete`. The kernel verifies each id exists and was created by your profile; any phantom id blocks the completion with an error listing what went wrong, and the rejected attempt is permanently recorded on the task's event log. **Only list ids you captured from a successful `kanban_create` return value — never invent ids from prose, never paste ids from earlier runs, never claim cards another worker created.**

```python
# GOOD — capture return values, then claim them.
c1 = kanban_create(title="remediate SQL injection", assignee="security-worker")
c2 = kanban_create(title="fix CSRF middleware", assignee="web-worker")

kanban_complete(
    summary="Review done; spawned remediations for both findings.",
    metadata={"pr_number": 123, "approved": False},
    created_cards=[c1["task_id"], c2["task_id"]],
)
```

```python
# BAD — claiming ids you don't have captured return values for.
kanban_complete(
    summary="Created remediation cards t_a1b2c3d4, t_deadbeef",  # hallucinated
    created_cards=["t_a1b2c3d4", "t_deadbeef"],                   # → gate rejects
)
```

If a `kanban_create` call fails (exception, tool_error), the card was NOT created — do not include a phantom id for it. Retry the create, or omit the id and mention the failure in your summary. The prose-scan pass also catches `t_<hex>` references in your free-form summary that don't resolve; these don't block the completion but show up as advisory warnings on the task in the dashboard.

## Block reasons that get answered fast

Bad: `"stuck"` — the human has no context.

Good: one sentence naming the specific decision you need. Leave longer context as a comment instead.

```python
kanban_comment(
    task_id=os.environ["HERMES_KANBAN_TASK"],
    body="Full context: I have user IPs from Cloudflare headers but some users are behind NATs with thousands of peers. Keying on IP alone causes false positives.",
)
kanban_block(reason="Rate limit key choice: IP (simple, NAT-unsafe) or user_id (requires auth, skips anonymous endpoints)?")
```

The block message is what appears in the dashboard / gateway notifier. The comment is the deeper context a human reads when they open the task.

## Heartbeats worth sending

Good heartbeats name progress: `"epoch 12/50, loss 0.31"`, `"scanned 1.2M/2.4M rows"`, `"uploaded 47/120 videos"`.

Bad heartbeats: `"still working"`, empty notes, sub-second intervals. Every few minutes max; skip entirely for tasks under ~2 minutes.

## Retry scenarios

If you open the task and `kanban_show` returns `runs: [...]` with one or more closed runs, you're a retry. The prior runs' `outcome` / `summary` / `error` tell you what didn't work. Don't repeat that path. Typical retry diagnostics:

- `outcome: "timed_out"` — the previous attempt hit `max_runtime_seconds`. You may need to chunk the work or shorten it.
- `outcome: "crashed"` — OOM or segfault. Reduce memory footprint.
- `outcome: "spawn_failed"` + `error: "..."` — usually a profile config issue (missing credential, bad PATH). Ask the human via `kanban_block` instead of retrying blindly.
- `outcome: "reclaimed"` + `summary: "task archived..."` — operator archived the task out from under the previous run; you probably shouldn't be running at all, check status carefully.
- `outcome: "blocked"` — a previous attempt blocked; the unblock comment should be in the thread by now.

## Notification routing

You can configure the gateway to receive cross-profile Kanban task notifications by adding `notification_sources` to `~/.hermes/config.yaml`.
- `notification_sources: ['*']` accepts subscriptions from all profiles.
- `notification_sources: ['default', 'zilor-ppt']` or `"default,zilor-ppt"` restricts subscriptions to specified profiles.
- Omitting the key keeps the default behavior (profile isolation).

## Kanban Dispatcher — Diagnosing Spawn Failures

When the dispatcher reports `crashed=1` repeatedly and the worker log shows `Unknown skill(s): kanban-worker`, or workers exit immediately with `401` auth failures, two root causes are most common:

### Root Cause A: `kanban.db` index corruption → `disk I/O error`

The SQLite DB's `kanban_notify_subs` index can become corrupt (manifests as `disk I/O error` in `release_stale_claims`). Fix:

```python
# Check corruption
import sqlite3
conn = sqlite3.connect("/path/to/kanban.db")
result = conn.execute("PRAGMA integrity_check;").fetchone()
# Expected: ('ok',) — anything else means corruption

# Fix: REINDEX + WAL checkpoint (run on the DB before it causes cascading failures)
conn.execute("REINDEX;")
conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
print(conn.execute("PRAGMA integrity_check;").fetchone())
conn.close()
```

**Discovery path:** Gateway error log shows `kanban_notifier tick failed: disk I/O error` every ~5 seconds, followed by `kanban dispatcher: tick failed on board default` at `release_stale_claims`. Run `PRAGMA integrity_check` on `~/.hermes/kanban.db`.

### Root Cause B: Profile missing `.env` → worker 401 authentication

When a worker spawns under a named profile (e.g. `research-lead`), it reads that profile's own `.env`, NOT the root `~/.hermes/.env`. If the profile lacks API keys, the worker hits 401 immediately and exits.

**Symptoms:** Worker log shows `Unknown skill(s): kanban-worker` → then `AuthenticationError [HTTP 401]`. The `kanban-worker` skill is installed (at `skills/devops/kanban-worker/SKILL.md`), but the worker crashed before it could load anything — the error appears first.

**Fix:** Copy the root `.env` to all active profile directories:
```bash
cp ~/.hermes/.env ~/.hermes/profiles/<profile-name>/.env
```

**Verification:** Run a test spawn manually:
```bash
hermes -p <profile-name> chat -q "echo test"
# Must succeed before the dispatcher can spawn workers for that profile
```

Common profile names on this system: `research-lead`, `content-director`.

### Quick diagnostic checklist
```
1. tail -100 ~/.hermes/logs/gateway.log | grep -E "kanban|worker|spawn|skill"
2. cat ~/.hermes/kanban/logs/<task-id>.log
3. sqlite3 ~/.hermes/kanban.db "PRAGMA integrity_check;"
4. ps aux | grep kanban | grep -v grep    # dispatcher alive?
5. ls ~/.hermes/profiles/<profile>/.env    # profile has credentials?
```

### Worker `Unknown skill(s): kanban-worker` After Code Patch

**Scenario:** You patched `kanban_db.py` (e.g. `_kanban_worker_skill_available`) and workers still fail even after gateway restart.

**Root cause:** Gateway graceful restart (`hermes gateway restart` via request protocol) does NOT reload Python modules from disk. Pycache and memory-mapped module state persist.

**Diagnosis steps:**
```bash
# 1. Check if patch is actually in the file
grep -n "_kanban_worker_skill_available" ~/.hermes/hermes-agent/hermes_cli/kanban_db.py

# 2. Direct test of the patched function in venv Python
cd ~/.hermes/hermes-agent && venv/bin/python -c "
import sys; sys.path.insert(0, '.')
from hermes_cli.kanban_db import _kanban_worker_skill_available
from hermes_cli.profiles import resolve_profile_env
path = resolve_profile_env('research-lead')
print('Skill available:', _kanban_worker_skill_available(path))
"

# 3. Check worker log for the actual error
tail -5 ~/.hermes/kanban/logs/<task-id>.log
```

**Fix:** Hard kill the gateway, then restart:
```bash
ps aux | grep "hermes_cli.main gateway" | grep -v grep
kill -9 <pid>
sleep 2
cd ~/.hermes && ./run_hermes_gateway.sh
```

**The `_kanban_worker_skill_available` patch:** The dispatcher checks skills by resolving `HERMES_HOME` from the profile env. When workers spawn under a named profile (e.g. `research-lead`), the check must resolve to the profile's skills dir (`~/.hermes/profiles/<profile>/skills/`), not the default `~/.hermes/skills/`. The patch adds `resolve_profile_env(profile_arg)` as a fallback before calling the skill check function.

## Result visibility — writing to accessible locations

Research tasks often store results only in `task_runs.summary` (DB) and log files. Users cannot see DB contents directly. **Always write the actual result artifact to a visible, persistent location:**

- **Log file:** Prepend the full result to the task log at `~/.hermes/kanban/logs/<task_id>.log` so humans can `tail` it.
- **Workspace:** If using `scratch` or `dir:` workspace, write a `result.md` or `output.json` inside it.
- **Comments:** Use `kanban_comment` to post a readable excerpt to the task thread — this is visible in the dashboard.

**Why this matters:** A task can be `done` in the DB while the user says "I don't see the worker output." The result must live where the human can find it — not only in structured DB fields.

**Minimum pattern for research tasks:**
```python
# Write visible artifact first
result_md = f"# Research: {title}\n\n{findings}\n"
log_path = f"/Users/tuananh4865/.hermes/kanban/logs/{os.environ['HERMES_KANBAN_TASK']}.log"
with open(log_path, "w") as f:
    f.write(result_md)

# Then complete with structured metadata
kanban_complete(
    summary=f"{topic}: {recommendation}. Full report at $HERMES_KANBAN_WORKSPACE/result.md",
    metadata={"recommendation": recommendation, "sources_read": n, "artifacts": ["result.md"]},
)
```

**Bad pattern (output trapped in DB):**
```python
# Completes but result is invisible to human
kanban_complete(summary="AI Services Agency — $1M ARR path, 70-80% margins")
# Log file has only the lifecycle noise, not the actual research
```

### Pitfall: Task shows "done" but user can't see output

If the task completes with `status=done` and `consecutive_failures=0` but the user says "I don't see the worker response," the result is probably trapped in `task_runs.summary` (DB only). 

**Check:** `sqlite3 ~/.hermes/kanban.db "SELECT summary FROM task_runs WHERE task_id='<id>' ORDER BY started_at DESC LIMIT 1;"`

**Fix:** Ensure your final worker action writes the result to `~/.hermes/kanban/logs/<task_id>.log` — this is what users check with `tail`. The DB field is for downstream agents, not for humans.

## Support Files

- `references/tailscale-serve.md` — Tailscale serve / funnel diagnostics for exposing local services to tailnet or internet

## Do NOT

- Call `delegate_task` as a substitute for `kanban_create`. `delegate_task` is for short reasoning subtasks inside YOUR run; `kanban_create` is for cross-agent handoffs that outlive one API loop.
- Modify files outside `$HERMES_KANBAN_WORKSPACE` unless the task body says to.
- Create follow-up tasks assigned to yourself — assign to the right specialist.
- Complete a task you didn't actually finish. Block it instead.

## Pitfalls

**Task state can change between dispatch and your startup.** Between when the dispatcher claimed and when your process actually booted, the task may have been blocked, reassigned, or archived. Always `kanban_show` first. If it reports `blocked` or `archived`, stop — you shouldn't be running.

**Workspace may have stale artifacts.** Especially `dir:` and `worktree` workspaces can have files from previous runs. Read the comment thread — it usually explains why you're running again and what state the workspace is in.

**Don't rely on the CLI when the guidance is available.** The `kanban_*` tools work across all terminal backends (Docker, Modal, SSH). `hermes kanban <verb>` from your terminal tool will fail in containerized backends because the CLI isn't installed there. When in doubt, use the tool.

## Verify artifact exists before claiming done (silent-recovery pitfall, 2026-06-30)

The kanban dispatcher records artifact paths in `task_runs.metadata.artifacts` JSON when you call `kanban_complete()`. **It does NOT verify the file actually exists on disk.** If you write `metadata={"artifacts": ["path/to/result.md"]}` without first ensuring the file is on disk (e.g. you crashed mid-write, used a wrong path, the directory wasn't created, parent-task auto-completion flipped you to `done` based on child tasks), the task will be marked `done` in the DB with a phantom artifact path. The audit will report "task done" but the human will see an empty workspace.

**The 3-layer truth cascade** (cheaper to verify now than debug later):

| Layer | Source | Ground truth? |
|---|---|---|
| 1. `task_runs.summary` (DB) | Your free-form summary | NO — prose, not a file |
| 2. `task_runs.metadata.artifacts` (DB) | Path strings you provided | NO — recorded before write verify |
| 3. Actual file on disk | `os.path.exists(path) and stat().st_size > 0` | **YES — the only ground truth** |

**Worker-side recipe — verify before `kanban_complete`:**

```python
import os

artifacts = ["result.md", "data/findings.json"]
for path in artifacts:
    full = os.path.join(workspace, path)
    assert os.path.exists(full), f"Artifact missing: {full}"
    assert os.path.getsize(full) > 0, f"Artifact empty: {full}"

# Now safe to claim done
kanban_complete(
    summary="...",
    metadata={"artifacts": artifacts, ...},
)
```

**If your task is "compute answer X" and X is a string** (no file artifact), the answer itself is the artifact — write it to `$HERMES_KANBAN_WORKSPACE/result.md` AND record that path in `metadata.artifacts`. Don't trust the dispatcher to "do the right thing" with a `result` string in metadata — humans and downstream agents need a file path to `cat`/`tail`.

**Auto-completion trap:** If your task is a parent of N children, and the dispatcher auto-flips you to `done` when all children complete, your own final-artifact file may never have been written — and you won't get a re-prompt. Always write the final synthesis BEFORE your children complete, or guard the auto-completion with a post-condition check.

**Detection on the audit side (multi-agent-heartbeat / operations-manager):** The kanban DB can report `status='done'` with a phantom artifact path. The 4th verification check (after V23's 3-call recipe) is: for every task the DB says is `done` in the last 30 days, `ls` the workspace and confirm artifact files exist with non-zero size. Full recipe in `~/.hermes/skills/multi-agent-heartbeat/references/kanban-log-vs-kanban-db-false-positive.md` § "Silent-recovery bug".

**Real case (t_3a73b0af, 2026-06-30):** YouTube-niche research task. Worker wrote `metadata.artifacts=["youtube-channel-research-final.md"]` and `kanban_complete()` succeeded. Workspace dir was created at `~/.hermes/kanban/workspaces/t_3a73b0af/` but contained 0 files. Same bug fired twice (run 24 on 2026-05-29, run 34 on 2026-06-30) — both runs marked `done` in DB, both workspaces empty on disk. Root cause: worker claimed completion without verifying file write actually persisted.

## CLI fallback (for scripting)

Every tool has a CLI equivalent for human operators and scripts:
- `kanban_show` ↔ `hermes kanban show <id> --json`
- `kanban_complete` ↔ `hermes kanban complete <id> --summary "..." --metadata '{...}'`
- `kanban_block` ↔ `hermes kanban block <id> "reason"`
- `kanban_create` ↔ `hermes kanban create "title" --assignee <profile> [--parent <id>]`
- etc.

Use the tools from inside an agent; the CLI exists for the human at the terminal.
