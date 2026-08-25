---
name: hermes-cron-management
description: Manage Hermes cron jobs — create, update delivery targets (especially Telegram groups/topics), audit schedules, troubleshoot missed runs. Use when the user asks to set/change/check cron notifications, redirect reports to a specific thread, audit existing schedules, or debug cron delivery failures.
---

# Hermes Cron Management

## When to Use

- User says "set cron notifications to thread X", "redirect all cron reports to...", "send all reports to this group/topic"
- User asks to list/check existing cron jobs
- User wants to create a new scheduled job
- A cron job is failing or not delivering
- User wants to audit the full cron schedule

## Core Workflow: Update Delivery Target (most common task)

### Step 1: List all jobs to know what to update
```
cronjob action='list'
```
Note each job's current `deliver` field — formats you'll see:
- `telegram:<chat_id>:<thread_id>` — explicit group/topic
- `telegram:<chat_id>` — main group chat, no specific topic
- `origin` — back to the chat where the user invoked the job
- `local` — save only, no delivery (used for `no_agent` scripts)
- `all` — fan out to every connected channel

### Step 2: Find the right target format

**For Telegram groups/topics, the format is:**
```
telegram:<chat_id>:<thread_id>
```

**How to discover chat_id + thread_id when you don't know them:**

The current session's session key tells you the answer directly:
```bash
echo "$HERMES_SESSION_KEY"
# Example: agent:main:telegram:group:-1003764041476:604
#                        ^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^
#                        |       chat_id:thread_id
# Parse: telegram:group:<chat_id>:<thread_id>
```

**Other ways to discover:**
- `send_message action='list'` — shows all groups + topics with friendly names; copy the exact `telegram:<id>:<id>` from the list
- For a topic the user is in RIGHT NOW: parse `HERMES_SESSION_KEY`
- DM with the user: `telegram:<user_id>` (no thread component)

**Pitfall — don't guess IDs from conversation history.** Old messages might reference a different topic. The session key is the source of truth for "the thread the user is in right now."

### Step 3: Update each job (parallel is fine)
```
cronjob action='update' job_id='<id>' deliver='telegram:<chat_id>:<thread_id>'
```
Multiple jobs can be updated in the same response (parallel tool calls). They are independent.

### Step 4: Verify
```
cronjob action='list'
```
Confirm every `deliver` field now matches the target. If any didn't change, re-check the format string (typos, missing colon).

## Decision Table: What to Set

| Scenario | Format |
|----------|--------|
| Notify in this thread (current conversation) | `telegram:<chat_id>:<thread_id>` from `HERMES_SESSION_KEY` |
| Notify in a specific named group | `send_message action='list'` → copy exact string |
| Notify in user's DM | `telegram:<user_id>` |
| Script-only cleanup, no output | `local` |
| Send to wherever user is when job fires | `origin` |
| Broadcast to every connected channel | `all` |

## Creating a New Cron Job

```
cronjob action='create'
  name='<short, descriptive>'
  schedule='<cron expression>'   # e.g. '0 3 * * *' = 3am daily
  prompt='<full self-contained prompt — the job runs with no chat context>'
  deliver='<target format>'
  skills=[<list of skill names to load>]
  model={provider: 'minimax', model: 'MiniMax-M2.7'}  # optional
```

**Critical pitfall — cron prompts are self-contained.** The job runs in a fresh session with no current-chat history. The prompt MUST include:
- Mission statement (what to do)
- All file paths, IDs, and config it needs
- Output format expected
- No reference to "the user said" — there's no user, just the prompt

## Diagnosing Failed Deliveries

If `last_delivery_error` is non-null on a job:
1. Check `deliver` field — typos in chat_id/thread_id cause silent failures
2. Verify the chat_id exists — use `send_message action='list'` to confirm
3. For topics: the thread must still exist; deleted topics cause delivery errors
4. For `origin`: works only if user has an active session at job-fire time
5. Check gateway logs: `tail -50 ~/.hermes/logs/gateway.log`

## Common Pitfalls

- **Don't pass `--no-agent` jobs through `deliver=telegram:`** — `no_agent: true` jobs (script-only) have no message to deliver; `local` is correct
- **`origin` is sticky to where the job was created** — if the user moves to a different thread, the job still delivers to the original "origin" chat. For "always deliver here", use explicit `telegram:<chat>:<thread>`
- **Updating `deliver` does not restart the job** — schedule and last-run state are preserved
- **Pausing a job does not change its `deliver`** — `paused_at` is independent
- **Cron prompts are self-contained** — they run in a fresh session with zero chat history. The prompt MUST include: mission, file paths, IDs, output format. NEVER reference "the user said" / "anh vừa nói" — there is no user at runtime
- **Schedule drift after rename** — when bulk-updating prompts to repurpose a job (e.g. changing "Hermes Agent X Research" → "Shopee Affiliate Trending"), you MUST also update `schedule` to match the new mission's intended fire time. Old schedule + new prompt = confused cron
- **Audit job referencing non-existent infrastructure → report 0s, don't fabricate** (2026-06-26): if a cron prompt asks to audit a multi-agent system (operations-manager, qa-agent, routing log, etc.) but the system has only `.env.backup` stubs and no live state files on disk, the report MUST show 0 stuck / 0 pending QA / 0 idle workers. NEVER invent counts to fill the table — that becomes persistent self-imposed state the next session cites against itself. The honest report (with root-cause + recommendation) is the deliverable.
- **`hermes cron list` is ground truth, file mtime is NOT** (H38 lesson — 2026-06-26): A profile's `state.md` mtime tracks the last WRITE, but cron-driven audit logs only get appended when there's something to report. Clean cron runs may not rewrite state.md for hours/days even when the cron fires on schedule. Therefore: when checking "is this profile's cron healthy?", `hermes cron list` exit_status + last_run is the source of truth. File mtime is a secondary confirmation, not a primary signal. See `references/cron-truth-h38-recipe.md` for the full recipe + recovery sequence.
- **Phantom-cron claim risk** (H37 → H39 recovery, 2026-06-26): If `hermes cron list` does NOT show a cron you're tracking but you have prior evidence it existed, do NOT report "phantom cron" as a fault. Re-check at the next sweep — cron registry is mutable and may transiently hide a job during re-registration. Only classify as "cron missing" after 2+ consecutive sweeps confirm absence. See `references/cron-truth-h38-recipe.md`.
- **macOS `ls --time-style=full-iso` is GNU-only** (recurring pitfall, 2026-06-26): Cron audit scripts that call `ls --time-style=full-iso` will fail on macOS BSD `ls` with `unrecognized option`. Use BSD-compatible alternatives: `ls -laT` (BSD long-format with mtime), `stat -f "%Sm %N" file`, or `find -printf '%T@ %p\n'` (GNU only — also broken on macOS, prefer BSD). Audit scripts in cron prompts should pre-test for macOS vs GNU `ls` and use portable patterns.
- **Telegram document batch flood control** (2026-06-26, KarmaVid 19:30): Sending >1 file via `send_message` in <30s triggers Telegram Bot API rate limit (`RetryAfter: Flood control exceeded. Retry in 34 seconds`). Even though retries succeed, UX lags. Cron-driven tools that deliver >1 file in one run should batch with 3-5s delay between sends. See `references/telegram-document-batch-flood.md` for full pattern.
- **`hermes cron list` is current-state only — past 401 bursts are invisible** (2026-06-28, weekly cleanup): The cron list shows the most recent run status. An auth failure that affected 27 sessions between Jun 25-26 (MiniMax API key rotation) was completely invisible in the 2026-06-28 cleanup because by then every job's last run was `ok`. To catch historical-but-recovered incidents, always run Layer 2 grep: `grep -l "non_retryable_client_error.*401" ~/.hermes/sessions/*.json | wc -l` + check the most recent 401 timestamp. A "current ok" with "27 historical 401s" tells anh a real incident happened, even though the system looks healthy now. See `references/cron-historical-401-audit.md`.

- **Cron script path MUST be relative to `~/.hermes/scripts/`** (2026-07-19, Hermes-Only-Folder-Rule migration): The `cronjob action='update'` tool **refuses absolute paths** for the `script` field. Error: `Script path must be relative to ~/.hermes/scripts/. Got absolute or home-relative path: '/Volumes/Storage-1/Hermes/...'. Place scripts in ~/.hermes/scripts/ and use just the filename.` Real case: 2 cron jobs (`Wiki Log Rotate Daily` e19078cba7d9, `Wiki Smart Cleanup Weekly` 8bafccaa8585) failed silently because script was at `/Volumes/Storage-1/Hermes/wiki/scripts/wiki_log_rotate_wrapper.sh` but cron expected `~/.hermes/scripts/wiki_log_rotate_wrapper.sh`. Two-fix options: (1) symlink the script into `~/.hermes/scripts/`: `ln -sf /Volumes/Storage-1/Hermes/wiki/scripts/wiki_log_rotate_wrapper.sh ~/.hermes/scripts/`. (2) Move the actual script into `~/.hermes/scripts/`. Option 1 (symlink) is preferred when you want to keep all scripts under `/Volumes/Storage-1/Hermes/` per Hermes-Only-Folder-Rule. **Always verify the symlink works** by running it standalone (`~/.hermes/scripts/wiki_log_rotate_wrapper.sh`) BEFORE declaring the cron fixed. After symlink, `last_status: error` cached from previous runs will only update on the next scheduled run (could be 1-7 days). See `references/cron-script-path-symlink.md` for full recipe.

- **`last_status: error` can be FALSE POSITIVE if script exits 2 by design** (2026-07-19, smart-cleanup case): A cron job reports `last_status: error` in `hermes cron list` → first instinct is "script broken". BUT some scripts intentionally exit non-zero on successful operations to trigger downstream notifications. Real case: `Wiki Smart Cleanup Weekly` (8bafccaa8585) script comment: `# Exit codes: 0 = OK no cleanup, 1 = Error, 2 = Cleanup happened (notification fired)`. So `Exit 2 = success + Telegram notification fired`. The cron tool marks ANY non-zero exit as `error` status → false positive. **Diagnostic workflow when `last_status: error`:** (1) `cat ~/.hermes/cron/output/<job_id>/<date>.md` → read the actual output, look for "Status: script failed" + actual exit code. (2) Check the script source's exit code comment block (every well-written wrapper script documents its exit codes). (3) Check the script log file (e.g., `~/.hermes/cron/wiki_smart_cleanup.log`) for evidence of success (e.g., "Cleanup detected (500 files) — sending notification"). (4) If exit code is intentional (0/2 = success, 1/3 = error), report as `success-with-design-intent`, not as broken. Only treat as true broken if the script log shows uncaught exception OR the script's "OK" branch returned non-zero.

- **Config changes require gateway restart — gateway BLOCKS self-restart** (2026-07-19, hermes-file-log hook deployment): Adding a new `post_tool_call` hook to `~/.hermes/config.yaml` does NOT take effect until gateway restart. But `hermes gateway restart` from inside the running gateway **fails with: `Blocked: cannot restart or stop the gateway from inside the gateway process. The gateway would kill this command before it could complete (SIGTERM propagates to child processes).` Run `hermes gateway restart` from a separate shell outside the running gateway.** Real workflow: (1) edit `~/.hermes/config.yaml` + `~/.hermes/shell-hooks-allowlist.json`, (2) provide user with helper script (`bash ~/.hermes/restart-hermes-gateway.sh`) that runs the kill + auto-respawn via launchctl, (3) wait 30s for new gateway PID, (4) test with a real Telegram message. This is the same pattern as any daemon config change — README should always include the restart command when hooks are added/modified.

## Audit Cron Patterns (operations-manager, qa-agent, idle-agent detection)

When a cron job is an audit/inspection task (not a research/automation task), the run-time agent has no shared state with past runs. Use this 4-step pattern to produce verifiable output:

1. **Inventory phase** — enumerate the artifacts the audit expects to find:
   ```bash
   find <wiki_root> -name "state.md" -not -path "*/.git/*" -not -path "*/node_modules/*"
   find <wiki_root> -name "*operations*" -not -path "*/.git/*"
   ls <wiki_root>/cron/   # state files from other audits
   cat <wiki_root>/.crontab   # confirm this audit job is actually scheduled
   ```
2. **Classify** — for each artifact category: (a) live + has data, (b) live + empty, (c) backup-only (e.g. `.env.<role>.backup`), (d) absent.
3. **Report with all zeros if missing** — table MUST show 0/0/0 honestly. Add a "Root cause" section explaining why the system is absent (env stub only, no live process, no crontab entry).
4. **Save routing log** to `wiki/cron/<job-name>-<frequency>-<date>.md` even when there's nothing to report — preserves the audit trail and tells the next run "this is run N, all previous runs found the same gap".

See `references/cron-audit-patterns.md` for the full template (root-cause checklist, recommendation boilerplate, what to grep when the audit target is ambiguous).

## Cron Health Check Recipe (H38 — 2026-06-26)

When auditing whether a profile's cron is healthy (e.g., operations-manager 6h audit, qa-agent hourly sweep, idle-agent detector), use this 5-check recipe instead of trusting state.md file mtime alone. File mtime lags reality — a clean cron run doesn't always rewrite state.md.

```bash
# 1. Ground truth: cron registry
hermes cron list | grep -E "<profile-name>|<job-name>"
# Look for: exit_status, last_run timestamp, next_run

# 2. Secondary: state.md mtime
stat -f "mtime: %Sm" ~/.hermes/profiles/<profile>/state.md

# 3. Recent errors
grep -E "ERROR|WARNING|error" ~/.hermes/logs/errors.log | tail -20

# 4. Recent sessions for this profile
sqlite3 ~/.hermes/state.db \
  "SELECT COUNT(*), MAX(started_at) FROM sessions \
   WHERE source='cron' AND id LIKE '<profile-name>%' \
   AND started_at > strftime('%s', 'now', '-1 day');"

# 5. Cross-validate with sibling audit profile
# (e.g., qa-agent hourly + operations-manager 6h should agree)
```

**Decision rule:** If `hermes cron list` shows `exit_status: ok` AND `last_run` is recent → profile is **HEALTHY** regardless of state.md mtime. Only classify as "faulted" when the cron registry itself shows `error:` or `last_run` is outside its expected cadence window.

**Phantom-cron warning:** If `hermes cron list` does NOT show a cron you've tracked previously, do NOT report "phantom cron" based on a single sweep. Cron registry is mutable — re-check at next sweep. Only classify as "cron missing" after 2+ consecutive confirmations.

Full recipe + recovery sequence + phantom-cron history: see `references/cron-truth-h38-recipe.md`.

## Designing Research Cron Prompts (Content Creator / Affiliate workflow)

When the user asks to design a fleet of research cron jobs around a niche (content creator, affiliate, market research, etc.), use this template structure. Proven pattern from Content Creator fleet (2026-05-02).

### Standard Prompt Structure (apply to every job)

```
# <JOB_NAME>

## Mission
<1-2 sentences: what to research, output, when, where>

## Context (IMMUTABLE — same across all jobs in the fleet)
<User persona, audience segments, quality bar, sources priority, affiliate channels, platform mix>

## Scope hôm nay
<Sub-niche rotation table by day-of-week, OR specific keyword/topic list>

## Research Rules (BẮT BUỘC)
1. Số lượng nguồn: ≥5 nguồn/claim (each with URL + access date + author/org)
2. Source priority list (rank 1 → N)
3. Data freshness: trending data ≤ 7 days, specs = official site, policy = ≤ 30 days
4. KHÔNG tự đoán/bịa — if can't hit 5 sources → ghi "KHÔNG ĐỦ DỮ LIỆU ĐÁNG TIN" và skip claim

## Routing Rule
- Mặc định: tự research bằng web_search/exa
- Delegate cho research bot (VD: Researcher_Clawd_Bot) khi: >10 sản phẩm cần crawl HOẶC >30 phút research

## Deliverable
### File 1: Markdown research file
Path: `~/Workspace/Claude/Projects/<Project>/Research/{YYYY-MM-DD}/{slug}.md`
Structure:
- YAML frontmatter (title, date, job, scope, sources_count, confidence)
- TL;DR (3-5 dòng)
- Top Findings (table with ≥3 items, columns: item/giá/rating/review/affiliate_link/source)
- Phân tích chi tiết (per item)
- Khuyến nghị cho user
- Nguồn (numbered, [Tên](URL) — truy cập YYYY-MM-DD)

### File 2: Telegram summary
<3-5 dòng: emoji + top pick + file path + sources count + confidence>

## Anti-patterns (TUYỆT ĐỐI KHÔNG)
<List of specific don'ts derived from user's quality bar>

## Timing & Budget
- Max 30 phút execution
- Max 50 tool calls
- Nếu vượt → top 3 thay vì top 5 + ghi "BUDGET EXCEEDED"

## Verification Checklist
- [ ] TL;DR 3-5 dòng, mỗi dòng 1 insight cụ thể
- [ ] Top findings table có ≥3 items
- [ ] Mỗi claim có ≥5 nguồn
- [ ] Mỗi nguồn có URL + ngày truy cập
- [ ] Path file đúng format
- [ ] Telegram message <5 dòng
- [ ] Không có claim thiếu nguồn
```

### Workflow: Design a Research Fleet

1. **Clarify the niche** (5 câu hỏi tối thiểu — see `references/designing-research-fleet.md`):
   - Sub-niche cụ thể (rotation plan)
   - Audience segments
   - Platform priority
   - "Uy tín" = gì
   - Affiliate/data sources

2. **Thiết kế fleet** — propose 5-7 jobs với schedule rải đều (morning: trending, mid-day: deep-dive, evening: review, night: backup)

3. **Confirm with user** trước khi apply — show bảng tên+schedule+mục đích

4. **Apply in parallel** — `cronjob action='update'` cho từng job song song

5. **Verify** — `cronjob action='list'` để check tất cả fields đúng (đặc biệt schedule — dễ bị miss khi rename job)

6. **Save template** — tạo `~/.hermes/cron/templates/research-job-template.md` để dùng lại cho fleet sau

### Quality Bar Settings (User-Specific)

The user's quality bar varies by use case. Ask the user to confirm these before designing:

| Setting | Common Values | Notes |
|---------|---------------|-------|
| Sources per claim | 2 (basic) / 5 (strict) / 10 (paranoid) | Default: 5 for affiliate research |
| Source priority #1 | Shopee (no automation block) / TikTok / Amazon / Google Trends | Depends on whether they monetize that channel |
| Data freshness | 7 days (trending) / 30 days (policy) / static (specs) | |
| Output format | full .md file + Telegram summary / inline only / spreadsheet | Default: .md file |
| Routing bot | Yes (with threshold) / No (always inline) | If yes, specify threshold |

## Related Tools
- `cronjob action='list'` — see all jobs, their schedules, last runs, delivery targets
- `cronjob action='update'` — change schedule, prompt, deliver, model, skills
- `cronjob action='pause' / 'resume'` — temporary stop without losing config
- `cronjob action='remove'` — delete (always list first to confirm job_id)
- `cronjob action='run'` — trigger immediately (debug use)
- `send_message action='list'` — discover all Telegram chat/topic targets

## Related Files
- `references/designing-research-fleet.md` — full step-by-step for designing a research cron fleet (clarify questions, fleet design table, parallel update checklist)
- `references/telegram-target-discovery.md` — how to find the right `telegram:<chat>:<thread>` format from HERMES_SESSION_KEY or send_message list
- `references/cron-audit-patterns.md` — pattern for inspection/audit cron jobs (operations-manager, qa-agent, idle-agent detection). 4-step template: inventory → classify → honest zero-report → save log. Use when the cron prompt is "audit X" or "check X" rather than "research X" or "automate X".
- **`references/cron-truth-h38-recipe.md`** — NEW 2026-06-26: `hermes cron list` is ground truth, NOT state.md file mtime. Lesson from qa-agent's 32+ sweep phantom "multi-profile cron fault pattern" corrected in one sweep. Includes 5-check audit recipe + phantom-cron recovery sequence. Use whenever auditing whether a cron-driven profile is healthy.
- **`references/cron-historical-401-audit.md`** — NEW 2026-06-28: Layer-2 of cron health. `hermes cron list` only shows current `ok/error` — past 401 bursts (MiniMax API key rotation, OAuth token expiry) are invisible to the current-state check. Grep session request dumps for historical `non_retryable_client_error.*401` patterns. Caught 27 historical 401s from 2026-06-25 orchestrator-heartbeat that `cron list` reported as "ok". Pair with H38 recipe for complete cron health picture.
- **`references/telegram-document-batch-flood.md`** — NEW 2026-06-26: Telegram Bot API rate-limits `sendDocument` calls. Sending >1 file in <30s triggers flood control (`RetryAfter: 34s`). Cron-driven tools delivering multiple files must batch with 3-5s delay. Three-option decision tree: 4s delay loop, env-var delay, or zip-archive for >5 files.
