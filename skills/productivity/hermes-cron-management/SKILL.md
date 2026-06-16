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
