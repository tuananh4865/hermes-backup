# Session 2026-06-28 — Orchestrator Nightly Reflection Worked Example

> **Trigger context:** Orchestrator profile ran the "Nightly Self-Reflection" cron (4ea08c530657) at 23:00 on Sunday. Sibling to memory-curator but operates at the Orchestrator level — captures cross-system health + writes to `entities/learned-about-tuananh.md` + `MEMORY.md` + `DECISION_LOG.md`. Output is delivered to the cron destination, not Telegram.
>
> **Why this reference exists separately from `session-2026-06-28-gap-fill.md`:** Gap-fill is a *memory-curator* recovery pattern (vault mirroring). This is an *Orchestrator reflection* pattern (system health + lessons). Different outputs, different skills.

## Inputs gathered (10 source categories, parallel reads)

```bash
# 1. Session DB
sqlite3 ~/.hermes/state.db "SELECT datetime(started_at, 'unixepoch'), source, title FROM sessions WHERE started_at > strftime('%s','2026-06-26') ORDER BY started_at DESC LIMIT 20"

# 2. Cron job state
cat ~/.hermes/cron/jobs.json
ls -la ~/.hermes/cron/output/<job-id>/

# 3. Heartbeat sweep outputs (latest 2)
tail -200 ~/.hermes/cron/output/28c34e383254/2026-06-28_22-30-52.md

# 4. Per-cron logs (one grep per log file)
tail -50 ~/.hermes/cron/{autonomous,dojo,daily_ingest,proactive_research,lmstudio_agent,watchdog}.log

# 5. Wiki health report (today's 4AM run)
cat ~/.hermes/memories/wiki_health_report.json

# 6. MEMORY/USER/DECISION/TASK_STATE (current state files)
read_file ~/.hermes/memories/{MEMORY,USER,DECISION_LOG,TASK_STATE}.md

# 7. Latest trend-scan output (research-lead nightly)
cat ~/.hermes/cron/output/42a9ec3df0dc/2026-06-28_18-03-59.md | tail -80

# 8. Latest daily-session-review (Content Creator context)
cat ~/.hermes/cron/output/5aea298eb0a8/2026-06-28_00-04-13.md

# 9. Fable-5 compliance check
bash ~/.hermes/scripts/check-fable5-compliance.sh

# 10. Last 100 errors from errors.log
grep "TypeError\|FileNotFoundError\|FAILED\|Traceback" ~/.hermes/logs/errors.log | tail -30
```

**Parallelize aggressively** — these 10 reads are independent. Batch them in one tool-call round to avoid sequential latency.

## Health classification (always compute FIRST)

| Signal | Healthy | Stale | Fault |
|--------|---------|-------|-------|
| Heartbeat sweeps in last 12h | ≥20 | 5-19 | <5 |
| Fable-5 compliance | All profiles pass | 1-2 fail | >2 fail |
| Cron-truth (H38) | output/ mtimes within schedule × 1.5 | 1.5-3× | >3× |
| Last user session | <24h | 24-72h | >72h |
| Last MEMORY.md update | <48h | 48-168h | >168h |
| Skills at 100K limit | 0 | 1-3 | >3 (curator silently failing) |
| jobs.json freshness | matches output/ mtimes | drift 1-6h | drift >6h or all "never" |
| autonomous.log NEXT task stuck | rotates every sweep | same task 4-12h | same task >12h |

**Tonight's classification:**
- 16 heartbeat sweeps (15:00→22:30) = ✅ Healthy
- Fable-5 compliance = ✅ 9/9 profiles pass
- Cron-truth = ✅ 18/18 crons OK (via output/ mtimes)
- Last user session = 33h+ ago (2026-06-27 13:40) = ⚠️ Stale
- MEMORY.md = ✅ updated today (06-27 23:03)
- Skills at 100K limit = ⚠️ quality-checker ~106K, multi-agent-heartbeat ~107K (hermes-agent SKILL.md borderline but protected/bundled)
- jobs.json = 🚨 ALL 18 jobs show `last_run: "never"` despite recent activity
- autonomous.log NEXT task = ⚠️ "Restart watchdog daemon [80]" stuck 8h+ (15:00→22:00)

## Three findings worth capturing as anti-patterns

### Finding 1: Skill doc without patch = no help (NEW pattern)

**Symptom:** `hermes-agent` SKILL.md documents the `Path.write_text(mode='a')` fix (Python 3.14 removed the `mode` kwarg). Three cron scripts (`watchdog_processor.py:392`, `cron_daily_ingest.py:95`, `topic_workflow.py:254`) STILL use the broken pattern. ~600 TypeErrors/day silently fail log writes.

**Root cause:** Skills document fixes but don't apply them. Skill author assumed downstream consumers would update their own code.

**Anti-pattern (codify in `write-a-skill` and `nightly-memory-curation`):**
- ❌ **Documenting a fix in a skill DOES NOT APPLY THE FIX** to any scripts. The agent that reads the skill still has to patch each affected file.
- ❌ **Assuming downstream consumers will self-patch** — they won't, especially if they're scripts not actively maintained.
- ❌ **Adding "See skill X for fix" cross-references** — that just defers the work.

**Correct pattern:**
- When documenting a fix in a skill, **always include the exact sed/replacement recipe** AND **add a verification step** (e.g., `grep -rn "write_text.*mode" /Volumes/Storage-1/Hermes/wiki/scripts/` → expected 0 results after fix).
- For recurring-class bugs, **promote to a CI gate** (pre-commit hook, scheduled lint cron). Pattern: "37+ days of documented bug = must CI gate."

**Detection recipe for tonight's bug:**
```bash
grep -rn "write_text.*mode='" /Volumes/Storage-1/Hermes/wiki/scripts/ 2>/dev/null
grep -c "TypeError.*write_text" ~/.hermes/cron/*.log 2>/dev/null | grep -v ":0"
```

Expected: `grep ... scripts/` returns 0 lines (fix applied). `grep ... cron/*.log` returns 0 counts (no TypeErrors).

### Finding 2: jobs.json staleness = internal-bookkeeping lies (NEW pattern)

**Symptom:** `cron/jobs.json` field `last_run: "never"` for ALL 18 active jobs. But output directories dated Jun 28 show jobs ran today. `hermes cron list` reports wrong freshness.

**Root cause:** Unknown. Could be (a) same `write_text` bug writing corrupt JSON, (b) separate writer that doesn't update `last_run`, (c) jobs.json schema mismatch. Investigation deferred.

**Workaround (operationalize in `operations-manager-routing-audit` and `nightly-memory-curation`):**
- ❌ Don't trust `hermes cron list` output for freshness signals.
- ✅ Use H38 cron-truth recipe: verify each cron ran by checking `~/.hermes/cron/output/<job-id>/` directory mtimes.
- ✅ Cross-validate via `~/.hermes/logs/agent.log` grep for cron job IDs.
- ✅ Heartbeat sweep should EXPLICITLY note "jobs.json freshness unverified — using output/ mtimes."

**Detection recipe:**
```bash
# Count cron output dirs modified in last 24h
find ~/.hermes/cron/output -type d -mtime -1 | wc -l

# Compare to jobs.json enabled count
python3 -c "import json; print(len([j for j in json.load(open('~/.hermes/cron/jobs.json'))['jobs'] if j.get('enabled')]))"
```

If counts diverge: cron-truth from output/, not jobs.json.

### Finding 3: Autonomous queue can stuck on single task (NEW pattern)

**Symptom:** `cron/autonomous.log` shows same "NEXT: Restart watchdog daemon [80]" across 8 hours of sweeps (15:00, 16:00, 17:00, 18:00, 19:00, 20:00, 21:00, 22:00). `cron/last_task_check.json` doesn't refresh.

**Root cause:** Unknown. Hypotheses: (a) queue dequeue broken, (b) watchdog keeps failing so retries forever, (c) `last_task_check.json` writer broken (possibly same `write_text` issue).

**Workaround:**
- ❌ Don't assume autonomous queue liveness from logs alone.
- ✅ Add queue-liveness check: count distinct NEXT tasks across last N log lines. If only 1 distinct = stuck.
- ✅ When stuck task is "Restart watchdog daemon", investigate watchdog first — recursive failure pattern.

**Detection recipe:**
```bash
# Last 10 autonomous.log entries, count distinct NEXT tasks
grep "NEXT:" ~/.hermes/cron/autonomous.log | tail -10 | awk '{print $NF}' | sort -u | wc -l
```

Expected: ≥3 distinct tasks (queue is rotating). Stuck: =1.

## Output structure (Orchestrator nightly reflection template)

The Orchestrator nightly reflection differs from memory-curator: it produces a **system health report**, not a wiki page update. Format:

```markdown
# 🌙 Nightly Self-Reflection — {YYYY-MM-DD HH:MM} ({weekday})

## 1. Today's Session Activity
- User-facing sessions: {N} (last: {datetime})
- Cron activity: {list of crons that ran + health}
- Telegram gateway: {fetch fallbacks, recoveries}

## 2. Failures Today (root cause + prevention)
### 🚨 CRITICAL: {name}
- Impact: {count today}
- Affected: {files:line}
- Root cause: {one sentence}
- Prevention rule (NEW or CONTINUING): {rule}

### ⚠️ {other category}
{same structure, less verbose}

## 3. Lessons Learned
**L{N} ({NEW|CONTINUING}):** {name}
- {evidence}
- {rule}
- {action item}

## 4. Memory Updates
| File | Change |
|------|--------|
| {path} | {one-line description} |

## 5. State Sync
- MEMORY.md: {updated/synced/touched}
- DECISION_LOG.md: {updated/synced/touched}
- USER.md: {reason}
- TASK_STATE.md: {reason}

## 6. Output — Reflection Summary
- System: ✅/⚠️/🚨
- {one-line summary}
- Top 3 priorities for tomorrow
- Decision: deliver to user tonight? {Yes/SILENT}

---

*Generated by Orchestrator nightly cron · {datetime}*
```

## Decisions made (template)

```markdown
[{datetime}] **{Action verb} {thing}.** {reasoning}. {evidence}.
```

Common action verbs: PROMOTE, INVESTIGATE, DEFER, ACCEPT, MONITOR, WATCH.

**Anti-pattern:** Don't write vague decisions ("Looks healthy overall"). Always pair observation with action.

## When to deliver to user vs [SILENT]

| Condition | Action |
|-----------|--------|
| User session in last 24h + new insight | Deliver summary, surface insights |
| User session 24-72h + CRITICAL finding | Deliver ONLY the critical finding, no flood |
| User session >72h + no CRITICAL | [SILENT] — wait for them to return |
| User explicitly asked for reflection | Deliver always |

Tonight's classification: User session 33h+ ago, NO CRITICAL finding (system healthy, bug is recurring-known) → **No flood-deliver.** Reflection stored in memory files for next interactive session to surface on demand.

## Verification checklist

Before delivering:

- [ ] Health classification computed and documented (table above)
- [ ] At least 3 independent sources cross-validated for each finding
- [ ] Each finding has: evidence (grep output / log lines), root cause, prevention rule
- [ ] MEMORY.md updated with today's key entry (use patch tool, append-only)
- [ ] DECISION_LOG.md updated with timestamped decisions
- [ ] `entities/learned-about-tuananh.md` appended (NOT overwritten) with new section
- [ ] No fabrication — "No new insight today" is a valid finding
- [ ] Frontmatter `updated:` date matches today
- [ ] If bug discovered: file/line path included, fix recipe included, NOT just "see skill X"

## Related

- `references/session-2026-06-27-structural-pitfalls.md` — Previous structural pitfalls (background-review toolset + SKILL.md 100K limit). Tonight's "skill doc without patch" finding is a NEW structural class.
- `references/session-2026-06-28-gap-fill.md` — Sibling reference for the memory-curator (different agent, different output).

## Pitfalls specific to Orchestrator nightly reflection

- ❌ **Don't repeat yesterday's findings verbatim** — even if the pattern continues, find a NEW angle or note "recurring, no new evidence."
- ❌ **Don't fabricate user insights when user is absent** — "No new anh insight today" is a valid output, not a failure.
- ❌ **Don't promote every bug to CRITICAL** — reserve CRITICAL for blocking, recurring, multi-day issues. Use ⚠️ for single-day warnings.
- ❌ **Don't update TASK_STATE.md unless actively driving it** — it's stale by design if the task hasn't been touched.
- ❌ **Don't dump overnight activity to user on return** — wait for their prompt. The reflection lives in memory files.
- ❌ **Don't trust file mtime for cron freshness** — only output/ directory mtimes are reliable (jobs.json may lie).