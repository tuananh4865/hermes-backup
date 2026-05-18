---
title: Hermes Autoresearch — Agentic Research Loop
name: hermes-autoresearch
created: 2026-04-27
updated: 2026-05-15
type: skill
tags: [autoresearch, self-improvement, karpathy-pattern, agentic]
description: Karpathy-style autonomous research loop — Skills Improvement + AI Agents + Hermes Agentic (16 capabilities, em TỰ CHỌN mỗi đêm), infinite repeat, NEVER STOP
trigger: Cron job 2AM hàng đêm, run forever until goal achieved
---

> Lấy cảm hứng từ [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
> Core philosophy: **give an agent narrow scope + git memory + never stop = autonomous improvement**

## Core Principles

- **program.md is the skill** — human programs the agent via markdown
- **Git is memory** — rollback on failure, commit on success
- **NEVER STOP** — run until goal achieved or human interrupts
- **Multi-dimensional research** — 3 focus areas simultaneously

---

## Repository Structure

```
~/.hermes/autoresearch/
├── program.md          ← Agent instructions (human edits)
├── knowledge.md        ← Persistent memory (insights, what worked/failed)
├── DISCARDED.md        ← Failed experiments (avoid repeating)
├── RESULTS.tsv         ← Log: commit, scores, status, description
└── research.py         ← Optional: benchmark script (not always needed)
```

---

## Three Research Focuses

### 1. Skills Improvement (PRIMARY — every night)
Improve skills in `~/.hermes/skills/`

Metrics:
```
SHS = stale_skills × 10 + missing_examples × 5 + broken_links × 3 + low_confidence × 2
Target: SHS = 0
```

What to improve:
- Add missing examples to skills
- Fix broken `[[wikilinks]]`
- Add pitfalls section
- Verify commands still work
- Raise confidence scores

**Gen Z Slang Sync (MANDATORY — every night):**
Research discovers new slang but it often stays in worker outputs, never syncing back to `entities/learned-about-tuananh.md`. Every autoresearch session MUST check:
1. Latest content-creator output: `~/.hermes/workers/content-creator/outputs/` (use ABSOLUTE path: `/Users/tuananh4865/hermes/workers/content-creator/outputs/`)
2. Look for "Gen Z Slang Update" section with newer date than `learned-about-tuananh.md` updated field
3. If found: UPDATE `entities/learned-about-tuananh.md` Gen Z Slang section with new terms
4. Commit the change

**Why this matters:** Gen Z slang evolves weekly. If research finds slang on Monday but it never gets synced to the authoritative source, future sessions use stale vocabulary in scripts → content feels outdated → Anh rejects scripts.

**Gen Z Slang Sync — MANDATORY STEP (2026-05-10 fix)**

The evening Orchestrator Monitor correctly noted "Gen Z slang list marked 'Updated 2026-05-04' — cần verify". The root cause: workers USE fresh slang in outputs but there's no automated sync back to `entities/learned-about-tuananh.md`.

**CRITICAL PATH BUG (2026-05-10):** The content-creator outputs are at `/Users/tuananh4865/.hermes/workers/content-creator/outputs/` (NOT the tilde path which doesn't expand in cron). The `/Volumes/Storage-1/Hermes/workers/content-creator/outputs/` is a different directory accessible from the wiki machine.

**MANDATORY SYNCHRONIZATION LOOP — add to every autoresearch session:**
```bash
# 1. Check content-creator outputs (use ABSOLUTE path — tilde doesn't expand in cron)
WORKER_OUTPUT=$(ls -t /Users/tuananh4865/hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)
if [ -n "$WORKER_OUTPUT" ]; then
    # 2. Check if slang was used that's newer than wiki file's updated date
    LATEST_SLANG=$(grep -iE "(Ối dồi ôi|Ra dại|Nam thư|lọ.*HOT|Các mom ơi|meoxink|Trình là gì|thơm vãi|pin trâu|sống nổi)" "$WORKER_OUTPUT" 2>/dev/null | head -5)
    if [ -n "$LATEST_SLANG" ]; then
        echo "FOUND newer slang in worker output:"
        echo "$LATEST_SLANG"
        echo "→ Must update entities/learned-about-tuananh.md Gen Z Slang section"
    fi
fi
```

**Direct paths for slang sync — CORRECTED (2026-05-13):**
- Worker outputs: `/Users/tuananh4865/hermes/workers/content-creator/outputs/` (NOT `/.hermes/workers/`)
- Wiki entity file: `/Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md`
- When slang is found in worker output → patch the wiki file's Gen Z Slang section

**⚠️ WORKER PATHS CONFIRMED (2026-05-14):** Workers write to `/Users/tuananh4865/hermes/workers/*/outputs/` (NOT `/.hermes/workers/`). This path is VERIFIED with May 13 evening content successfully written. Only check `/Users/tuananh4865/.hermes/workers/*/outputs/` if the primary path is empty.

```bash
# PRIMARY (verified working May 13):
ls -la /Users/tuananh4865/hermes/workers/content-creator/outputs/
# Shows: 2026-05-13-evening-content.md (9.3KB) ✅

# SECONDARY (may be empty/old):
ls -la /Users/tuananh4865/.hermes/workers/content-creator/outputs/
```

### Gen Z Slang Sync — DETECTING WORKER DEATH (2026-05-13)

**⚠️ NEW PITFALL:** Workers can stop firing (no new outputs) while their cron directories still have OLD files. The slang sync loop silently passes when workers are dead, producing no new slang even though slang may have evolved.

**MANDATORY DEATH DETECTION:**
```bash
# Check if workers have fired recently (within 48h)
CC_LAST=$(ls -t /Users/tuananh4865/.hermes/workers/content-creator/outputs/*.md 2>/dev/null | head -1)
if [ -n "$CC_LAST" ]; then
    CC_AGE=$(($(date +%s) - $(stat -f %m "$CC_LAST" 2>/dev/null || echo $(date +%s))))
    if [ "$CC_AGE" -gt 172800 ]; then  # 48h in seconds
        echo "⚠️ CONTENT CREATOR DEAD — last output $((CC_AGE/86400)) days ago"
        echo "→ Cannot sync slang from worker output — workers need restart"
    fi
fi
```

**⚠️ WORKER DEATH CONFIRMED (2026-05-16):** Workers stopped firing around May 11 (5+ days ago). Content Creator output directory still has May 11 files but no new ones since. Fallback: do web search for Gen Z slang instead of relying on worker output.

**Wiki index update — WRONG SECTION NAME (2026-05-16 fix):**

The X research session tried to find `## TikTok Research` in `index.md` — THIS SECTION DOES NOT EXIST. The actual TikTok section header is `### TikTok Content` (line ~88 in index.md).

**Correct patch pattern:**
```bash
# WRONG — section doesn't exist:
patch /Volumes/Storage-1/Hermes/wiki/index.md \
  --old_string "## TikTok Research" \
  --new_string "## Hermes X Research"

# CORRECT — find the actual TikTok section (### TikTok Content):
# Look for the TikTok section header and add Hermes X Research as a sibling
# The index.md structure has:
#   ### AI Engineering (line ~77)
#   ### TikTok Content (line ~88) ← this is the TikTok section
#   ### Auto-Ingest (line ~97)
# Add new research sections ABOVE ### Auto-Ingest or as new ### sections
```

**Wiki index sections (verified 2026-05-16):**
```
77|### AI Engineering
...
86|- [[intelligent-wiki-roadmap]]
87|
88|### TikTok Content   ← TikTok section header
89|- [[tiktok-algorithm-2026]]
...
97|### Auto-Ingest
98|- [[email]]
99|- [[rss]]
```

**Rule:** Before patching wiki index.md, READ the file first to find the actual section header. Never assume section names — verify by reading lines ~77-100.

### Gen Z Slang Rules
Research self-improvement patterns and agent frameworks.

Target: Document 5+ new techniques

Focus areas:
- Self-debugging patterns
- Agent skill creation
- Memory optimization
- Multi-agent coordination
- Self-improvement loops
- MCP, A2A protocols
- **Agent monetization (Felix Model)** ← see `ai-agent-business` skill

### 3. Hermes Agentic Features (em TỰ CHỌN mỗi đêm)
**Em TỰ QUYẾT ĐỊNH** capability nào để improve, dựa trên:
1. Highest impact cho công việc với anh
2. Quickest improvement (feasible trong 1 night)
3. Foundational (giúp cải thiện capabilities khác)

**16 Agentic Capabilities:**

| Category | Capability |
|----------|------------|
| Core | Self-Debugging, Self-Correction, Learning from Failures, Proactive Work |
| Knowledge | Memory Optimization, Knowledge Acquisition, Context Management |
| Skill/Tool | Skill Creation, Tool Use, Tool Creation |
| Planning | Goal Decomposition, Planning, Priority Setting, Reasoning |
| Collaboration | Multi-Agent Coordination, Delegation |

Metrics:
```
Hermes_Score = self_debug_fixed × 10 + skills_created × 20 + mistakes_prevented × 5
```

---

## Metrics

```
Skills_Score = skills_improved × 10
Agents_Score = frameworks × 10 + techniques × 5 + patterns × 3
Hermes_Score = capabilities_improved × 20 + wiki_updated × 2
```

**Note:** These are tracked qualitatively. Agent self-reports progress via telegram.

---

## Success Criteria (STOP when ANY met)

- `SHS = 0` (all skills healthy)
- `Hermes_Score >= 50`
- Documented **5+** new AI agent techniques
- Created **3+** new skills autonomously
- Error resolution rate > 80%

---

## Experiment Loop

```
LOOP FOREVER (until success criteria met OR human interrupts):

1. Read program.md, knowledge.md, DISCARDED.md
2. Pick ONE focus area
3. Research (web search, docs, experimentation)
4. Implement or document findings
5. Measure score improvement
6. If improved → git commit
7. If no progress → try different angle, git reset
8. Update knowledge.md
9. Every 30 min → send progress to telegram
10. STOP ONLY when success criteria met OR human interrupts
```

---

## ⚠️ CRITICAL: Skill Purpose vs Cron Prompt

**Skill = RESEARCH/AUTOMATION patterns. Cron prompt = EXECUTION instructions.**

**WRONG:** Adding session log analysis, memory management, daily consolidation to this skill.
**RIGHT:** Those belong in CRON PROMPT, not skill.

**The 3 focuses of THIS skill:**
1. Skills Improvement (improve ~/.hermes/skills/)
2. AI Agents Research (document techniques)
3. Hermes Agentic (self-improvement capabilities)

**Session log analysis + knowledge graph updates → Cron prompt, NOT skill.**

---

| Aspect | Karpathy AutoResearch | Hermes Autoresearch |
|--------|----------------------|---------------------|
| Domain | LLM training | 3 research focuses |
| Metric | val_bpb (single) | Multi-dimensional scores |
| Time | 5 min fixed | 5 min per experiment |
| Stop | Never | Goal achieved or human |
| Reports | None | Every 30 min to Telegram |

---

## Important Paths

| Path | Purpose |
|------|---------|
| `~/.hermes/autoresearch/` | Autoresearch repo |
| `~/.hermes/autoresearch/AGENTIC_COMPANY_PLAN.md` | Vision for agentic company |
| `~/.hermes/autoresearch/program.md` | Full 16 capabilities + decision framework |
| `~/.hermes/skills/` | Hermes skills (local, backed up to hermes-backup) |
| `/Volumes/Storage-1/Hermes/wiki/` | Wiki knowledge base (synced via Obsidian plugin) |
| `~/.hermes/hermes-agent/` | Hermes gateway code |

**NOTE (2026-05-08):** Skills were copied from `/Volumes/Storage-1/Hermes/skills/` to `~/.hermes/skills/`. External symlink removed. Backup now backs up `~/.hermes/` (full Hermes) to `hermes-backup` repo. Wiki syncs separately to `my-llm-wiki` via Obsidian plugin.

## ⚠️ CRITICAL: Attaching Skill to Cron = Skill Content Overwrites Prompt

**Symptoms (seen in 2026-05-08 session):**
- Cron created with `--skills ["hermes-autoresearch"]`
- Cron output shows full skill content (45KB SKILL.md) instead of intended cron prompt
- The skill's `[IMPORTANT: You are running as a scheduled cron job...]` wrapper appears in output

**Root cause:** When a skill is attached to a cron, the system injects the skill's full content into the prompt, replacing whatever prompt was written.

**Rule:** If you want a cron to run a specific prompt, do NOT attach a skill. Use `--skills []` (empty).
```
# WRONG — skill overwrites prompt:
cronjob create --skills ["hermes-autoresearch"] --prompt "MY CUSTOM PROMPT"
# Result: MY CUSTOM PROMPT is replaced by full hermes-autoresearch SKILL.md content

# CORRECT — no skill attachment:
cronjob create --skills [] --prompt "MY CUSTOM PROMPT"
# Result: MY CUSTOM PROMPT runs exactly as written
```

**May 9 run (2026-05-09 02:04):** Successfully completed with 10 NEW AI agent techniques documented (ERL, ICPO, Trajectory Memory, Hyperagents, MARS, RetroAgent, GEA, POLARIS, Self-Optimizing Multi-Agent, Hierarchical Self-Evolving). SHS = 0 (135 skills healthy). tiktok-viral-script skill improved (213 → 289 lines with 3 example scripts + 6-category pitfalls). Git commit: f8105fc.

# FOR AUTORESEARCH PURPOSE crons — only these should have skills attached:
# - a4b8e528983f (2AM Autoresearch) — this IS the autoresearch loop
# - a5c02f2f0d87 (7AM X Research) — research task, uses autoresearch pattern
```

**Verification after cron creation:**
```bash
cronjob list | grep {job_id}  # Check Skills: should be [] for custom prompts
```

## Cron Jobs

| Job ID | Name | Schedule | Skills | Purpose |
|--------|------|----------|--------|---------|
| a4b8e528983f | Autoresearch Nightly | 0 2 * * * (2AM) | hermes-autoresearch | Self-improvement loop, forever |
| a5c02f2f0d87 | Hermes X Research | 0 7 * * * (7AM) | hermes-autoresearch | Daily X research, 50+ results |
| 5aea298eb0a8 | Daily Session Review | 0 0 * * * (0AM) | [] | Session log review, wiki update |
| 7cba6ba5f52a | Hermes Daily Backup | 0 3 * * * (3AM) | [] | Backup full ~/.hermes to hermes-backup |

### ⚠️ CRITICAL: Skill Attached = Skill Content INJECTED into Prompt (2026-05-08)

**SYMPTOM:** Cron chạy ra nội dung từ skill (autoresearch) thay vì prompt mình viết.

**ROOT CAUSE:** Khi attach skill vào cron, skill content được LOAD vào prompt tại execution time.

**Scenario A — Cron WITH skill attached:**
```
cron prompt: "Read session logs..."
skill loaded: [FULL SKILL.md content]
→ Execution: Agent sees BOTH → runs SKILL instead of prompt ❌
```

**Scenario B — Cron with NO skill (`skills: []`):**
```
cron prompt: "Read session logs..."
→ Execution: Agent sees ONLY prompt → runs exactly what you wrote ✅
```

**WRONG:**
```
cron create --skills ["hermes-autoresearch"] --prompt "session review..."  ❌
```

**CORRECT — Always set `skills: []` when you want the cron to run its own prompt:**
```
cron create --skills [] --prompt "session review..."  ✅
```

**Verification after ANY cron create/update:**
```bash
cronjob list | grep job_id
# skill: null + skills: [] → runs ONLY prompt ✅
# skill: hermes-autoresearch + skills: [hermes-autoresearch] → runs SKILL ❌
```

**CORRECT:** Khi tạo cron với prompt cụ thể (không phải autoresearch loop):
```
cron create --prompt "session review..." --skills []  ✅
→ Cron chạy đúng prompt trực tiếp
```

**WHEN TO ATTACH SKILL:** Chỉ khi cron CẦN chạy cái skill đó (VD: 2AM autoresearch, 7AM X research).

**WHEN NOT TO ATTACH:** Cron mới với task cụ thể (session review, backup, daily report).

**VERIFICATION after creating cron:**
```bash
cronjob list | grep {job_id}
# Kiểm tra Skills column — phải là [] cho custom cron tasks
```
| 5aea298eb0a8 | Daily Session Review | 0 0 * * * (0AM) | Read yesterday's sessions, extract decisions/revenue/learnings, update wiki + knowledge graph, index for retrieval, report to Telegram |

### ByteRover Self-Improvement Review (2026-05-18)

**What happened:** ByteRover memory system auto-detected that `learned-about-tuananh.md` was updated (likely by a previous session's auto-save). The system sent a notification: "User profile updated" — this is an INFO-level notification, NOT a problem.

**Anh's question:** "Wiki trong memory provider có phải dựa trên skill llm-wiki của Karpathy không?"

**Answer:** CÓ và KHÔNG.
- `WikiMemoryProvider` (plugin tại `~/.hermes/plugins/memory/wiki/__init__.py`) **inspired by** Karpathy's LLM Wiki pattern — cùng directory structure, frontmatter convention, interlinked markdown.
- `llm-wiki` skill là **documentation pattern** (cách build/query wiki). WikiMemoryProvider là **implementation** (Python code xử lý memory operations).
- Không nhầm lẫn: skill ≠ plugin. Skill = documentation, Plugin = executable code.

**Auto-improvement pattern confirmed working:** ByteRover saves new knowledge after each session and checks/reverifies old knowledge periodically. This is the intended auto behavior — NOT something to call `brv_curate` manually for.

**Content Creator Morning cron (ce3701b4dcdd) RAN SUCCESSFULLY at 8AM on 2026-05-07:**
- Output file: `~/.hermes/workers/content-creator/outputs/2026-05-07-morning-brief.md` (8376 bytes)
- Research compiled: TikTok Shop Vietnam trends, trending sounds, Gen Z slang May 2026
- New trends discovered: "Cảnh báo có nam thư" (May 5, 2026), "Xuân Bính Ngọ" sound
- Script included: Day 1 script for "Dây Buộc Tóc Nhồi Bông Hình Thú" (56K orders)

**Verification pattern used:**
```bash
ls -la ~/.hermes/workers/content-creator/outputs/  # Output file exists ✅
```

**IMPORTANT: python3.14 Not Found (2026-05-06)**

### ⚠️ CRITICAL BUG: python3.14 Not Found (2026-05-06)

All cron jobs using Python scripts may fail with `FileNotFoundError: [Errno 2] No such file or directory: 'python3.14'`.

**Root cause:** Homebrew Python 3.14 is installed as `python3.14` but cron jobs may not find it in PATH. More critically, some scripts (e.g., `proactive_research_cron.py`) hardcode `python3.14` in subprocess calls.

**Fix:**
1. Check what Python is available: `which python3` and `ls /opt/homebrew/bin/python*`
2. If only `python3` available, scripts calling `python3.14` must be updated
3. Use full path in crontab: `/opt/homebrew/bin/python3.14` OR just `python3`

**Script fix pattern:**
```python
# WRONG:
subprocess.run(["python3.14", script_path], ...)

# RIGHT - use whatever python3 is in PATH:
import sys
python_bin = sys.executable  # gets the python running this script
subprocess.run([python_bin, script_path], ...)

# OR use crontab's PATH - just call python3:
subprocess.run(["python3", script_path], ...)
```

**For proactive_research_cron.py specifically:**
```bash
# The script at /Volumes/Storage-1/Hermes/wiki/scripts/proactive_research_cron.py
# Line 95 calls ["python3.14", script_path] — MUST change to ["python3", ...]
# Or better: use sys.executable approach
```

**Quick verification after fix:**
```bash
cd /Volumes/Storage-1/Hermes/wiki
python3 scripts/proactive_research_cron.py  # should run without FileNotFoundError
```

### ⚠️ PITFALL 5: Path.write_text() mode= Bug (Python 3.14)

**SYMPTOM:** `TypeError: Path.write_text() got an unexpected keyword argument 'mode'`

**AFFECTED:** `cron_daily_ingest.py` line 96:
```python
# WRONG (Python 3.14):
LOG_FILE.write_text(entry + '\n', mode='a')

# ALSO WRONG:
LOG_FILE.write_text(entry + '\n', 'a')  # second arg is not file mode
```

**ROOT CAUSE:** `Path.write_text()` does NOT accept a `mode=` parameter. The `mode` argument was removed/never existed for text-mode write. Use `Path.open()` with explicit mode instead.

**FIX:**
```python
# CORRECT - use Path.open() with context manager:
with LOG_FILE.open(mode='a') as f:
    f.write(entry + '\n')

# OR for first write (create file with header):
LOG_FILE.write_text(f"# Wiki Log\n\n> Chronological record.\n\n{entry}\n")

# NEVER use mode= with write_text()
```

**Verification after fix:**
```bash
cd /Volumes/Storage-1/Hermes/wiki
python3 -c "from pathlib import Path; p = Path('/tmp/test_log.md'); p.write_text('# Test\n'); p.open('a').write('entry\n'); print('✅ mode fix works' if 'entry' in p.read_text() else '❌')"
```

**Files to check for this bug:**
```bash
grep -rn "write_text.*mode=" /Volumes/Storage-1/Hermes/wiki/scripts/
```

### Worker Cron Jobs — STATUS (2026-05-07 CONFIRMED ✅)

**✅ VERIFIED WORKING (2026-05-07):** Content Creator Morning cron (ce3701b4dcdd) ran at 8AM and produced output.

**Evidence:**
```bash
# Content Creator Morning cron — ✅ WORKING
$ ls -la ~/.hermes/workers/content-creator/outputs/
# -rw-r--r--  1 tuananh4865  staff  8376 May  7 08:XX 2026-05-07-morning-brief.md

# Research Agent Evening — ✅ WORKING
$ ls -la ~/.hermes/workers/research-agent/outputs/
# -rw-r--r--  1 tuananh4865  staff  3655 May  6 18:31 2026-05-06-research-evening.md
```

**Orchestrator 9AM briefing — ✅ DELIVERED:** Morning report to Anh showing worker status.

**Orchestrator Agent Monitor — ✅ RUNNING (2026-05-07):** 6 runs confirmed today (10AM, 12PM, 2PM, 4PM, 6PM, 8PM). Last run at 8PM compiled full status based on worker outputs.

**Research Agent evening — ✅ VERIFIED 2026-05-07:** Ran at 18:50, produced TikTok Shop Vietnam analysis.

**Content Creator evening — ✅ VERIFIED 2026-05-07:** Ran at 18:03, script summary produced.

**Content Creator morning — ✅ VERIFIED 2026-05-07:** 8AM ran successfully, 8,376-byte morning brief with Gen Z slang, trending sounds, Day 1 script.

**Research Analyst morning — ✅ VERIFIED 2026-05-07 + 2026-05-08:**
- Output file: `~/.hermes/cron/output/e4fb0c36e9f7/*.md`
- 2026-05-07: Produced TikTok Shop monetization research (saved to `wiki/queries/tiktok-shop-monetization-research-2026-05.md`)
- 2026-05-08: Produced summer beauty + graduation + fee math brief (saved to `wiki/queries/tiktok-shop-morning-research-2026-05-08.md`)
- Pattern: Follows SOUL.md research format, saves to wiki queries, updates index.md + log.md

**Research Analyst evening — ✅ VERIFIED 2026-05-07:**
- Output file: `~/.hermes/cron/output/1c425ba42980/2026-05-07_18-50-40.md`
- 2026-05-07: Produced TikTok Shop monetization deep-dive, key finding = fee crisis (25-40% total cost)
- Status: ✅ DELIVERED Ran at 8:31AM, produced market research.

**⚠️ Still unverified (2026-05-07):** Orchestrator Nightly (9PM) — runs at 21:00, next check tomorrow.

**For full diagnosis + verification steps, see:** `references/worker-cron-verification.md`

```bash
# The CORRECT command is `cron edit`, NOT `cron update`
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron edit {job_id} --prompt "$(cat ~/.hermes/workers/{worker}/SOUL.md)" --clear-skills
```

**Root cause:** Worker SOUL.md files were created but cron prompts were never updated from the `hermes-autoresearch` default.

**Verification after fix:**
```bash
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list
# All 7 worker/orchestrator jobs now show: Skills: none (no hermes-autoresearch)
# Their prompts are now the raw SOUL.md content
```

### Worker Cron Job Registry

| Job ID | Name | Schedule | Worker | Expected Output | Status |
|--------|------|----------|--------|-----------------|--------|
| ce3701b4dcdd | Content Creator Morning | 0 8 * * * | content-creator | TikTok script in outputs/ | ✅ VERIFIED 2026-05-07 @ 08:05 |
| 50bc2c2dfbb3 | Content Creator Evening | 0 18 * * * | content-creator | Script summary in outputs/ | ✅ VERIFIED 2026-05-07 @ 18:03 |
| e4fb0c36e9f7 | Research Analyst Morning | 30 8 * * * | research-agent | Research in outputs/ | ✅ VERIFIED 2026-05-07 @ 08:31 |
| 1c425ba42980 | Research Analyst Evening | 30 18 * * * | research-agent | Research in outputs/ | ✅ VERIFIED 2026-05-07 @ 18:50 |
| 045a44210a59 | Orchestrator Morning | 0 9 * * * | orchestrator | Briefing for Anh | ✅ VERIFIED 2026-05-07 @ 09:01 |
| f1584a9a1d86 | Orchestrator Monitor | 0 */2 * * * | orchestrator | Worker nudge if stalled | ✅ VERIFIED 2026-05-07 — 6 runs today |
| fc2191d508a3 | Orchestrator Nightly | 0 21 * * * | orchestrator | Consolidation report | ⏳ Next run: 2026-05-07 21:00 |

**Summary (2026-05-07 8PM):** 6/7 verified working. All workers producing outputs. Orchestrator Monitor confirmed 6 runs today.

**Verification pattern:**
```bash
# Check output file exists AND has content
ls -la ~/.hermes/workers/{worker}/outputs/YYYY-MM-DD-*.md

# If file exists + >1KB → worker ran successfully
# If empty or missing → worker failed or didn't fire
```

### Worker SOUL.md Prompts (what each worker SHOULD run)

**Content Creator** (`~/.hermes/workers/content-creator/SOUL.md`):
- Role: TikTok script writer for Tuấn Anh (Vietnamese, mấy con vợ voice)
- Tasks: Gen Z slang research, viral script writing, TikTok trends analysis
- Output: Write scripts to `~/.hermes/workers/content-creator/outputs/[date]-script.md`

**Research Analyst** (`~/.hermes/workers/research-agent/SOUL.md`):
- Role: TikTok Shop product researcher
- Tasks: Competitor analysis, product trends, pricing strategies
- Output: Write research to `~/.hermes/workers/research-agent/outputs/[date]-research.md`

**Orchestrator** (`~/.hermes/workers/orchestrator/SOUL.md`):
- Role: Coordinator, NOT a worker — it's ME (Hermes)
- Tasks: Monitor workers, nudge stalled ones, compile daily briefing for Anh
- Output: Telegram report OR `[SILENT]` if nothing new

### How to Fix Worker Cron Misconfiguration

**⚠️ IMPORTANT:** Simply running `cron edit` does NOT guarantee the fix persists. Verification is MANDATORY after every fix attempt.

1. Read the worker's SOUL.md: `cat ~/.hermes/workers/{worker}/SOUL.md`
2. Find the job ID: `~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list`
3. Fix using Python subprocess (VERIFIED 2026-05-07):
   ```python
   import subprocess, sys
   with open('/Users/tuananh4865/.hermes/workers/{worker}/SOUL.md', 'r') as f:
       prompt = f.read()
   subprocess.run([
       sys.executable, '-m', 'hermes_cli.main', 'cron', 'edit',
       job_id, '--prompt', prompt, '--clear-skills'
   ], cwd='/Users/tuananh4865/.hermes/hermes-agent')
   ```
4. **MANDATORY VERIFICATION:** Run all 3 checks from `references/worker-cron-verification.md`
5. If verification fails → escalate

**NOTE:** `cron update` does NOT exist. Use `cron edit`.

### Worker Files Structure

```
~/.hermes/workers/
├── orchestrator/
│   ├── SOUL.md       — role: ME (Hermes), coordination duties
│   └── HEARTBEAT.md  — monitoring schedule (30min/2h/daily/nightly)
├── content-creator/
│   ├── SOUL.md       — voice: "anh" + "mấy con vợ", script structure
│   ├── HEARTBEAT.md  — schedule (30min/2h/6h/daily checks)
│   └── outputs/      — completed scripts (⚠️ EMPTY — workers not producing yet)
├── research-agent/
│   ├── SOUL.md       — research focus, output format
│   ├── HEARTBEAT.md  — schedule
│   └── outputs/      — completed research (⚠️ EMPTY — workers not producing yet)
└── memory/
    ├── MEMORY.md         — 3-layer (PARA + daily + tacit)
    ├── PENDING_TASKS.md  — task tracking
    └── daily/            — daily log entries (⚠️ EMPTY)
```

**KEY INSIGHT:** "Workers configured" ≠ "Workers running". SOUL.md files exist but cron prompts still run `hermes-autoresearch`. See `references/worker-cron-verification.md` for diagnosis.

---

## Critical: Goal Specificity Rule

**"Make X more agentic" = TOO VAGUE = WILL FAIL**

Karpathy-style autonomy requires TREMENDOUS specificity:

| ❌ Vague | ✅ Specific |
|----------|------------|
| "Make Hermes more agentic" | "Self-debugging: resolve 80% errors autonomously" |
| "Improve skills" | "SHS = 0 (stale×10 + missing_examples×5 + broken_links×3 + low_conf×2)" |
| "Research AI agents" | "Document 5 new techniques from arxiv/github" |

**Rule:** Every goal MUST have:
1. Metric formula (even if simplified)
2. Concrete stop condition (exact number)
3. Measurable output (wiki page, skill, prototype)

**KEY INSIGHT**: "Workers configured" ≠ "Workers running". SOUL.md files exist but cron prompts still run `hermes-autoresearch`. The orchestrator must fix the cron prompts.

---

## CRITICAL PITFALLS

**CRITICAL: The "Fixed" Documentation ≠ Reality (2026-05-06)**

The `session-continuity-gap.md` reference and PITFALL 17 claim the 4-tier fix is COMPLETE and VERIFIED. **Today's session proves otherwise:**

- `TASK_STATE.md` (559 bytes) — still the EMPTY TEMPLATE, never written by any code today
- `DECISION_LOG.md` (425 bytes) — still the EMPTY TEMPLATE, never written  
- `MEMORY.md` — last updated May 5 (cron run), NOT from today's user session (May 6)
- Files modified today: `Qwen3.5-2B-GGUF/` + `Qwen3.5-2B-mxfp4/` downloaded then DELETED — ZERO trace in any checkpoint

**What actually happened today that should have been captured:**
- Downloaded `nightmedia/Qwen3.5-2B-mxfp4-mlx` → failed (wrong file path)
- Downloaded `unsloth/Qwen3.5-2B-GGUF/Qwen3.5-2B-Q4_K_M.gguf` (1.2GB) → Jinja template error
- Deleted both 2B models → switched back to `gemma-4-e2b`
- ByteRover `qwen3.5-4b-awq-instruct` tested (~44s) but then disappeared from LM Studio server
- LM Studio workspace: `~/.lmstudio/models/lmstudio-community/`

**Root cause:** The WikiMemoryProvider `on_session_end()` code may exist but is NOT being called, OR the files it writes are going to a different location than where we're checking.

**DIAGNOSTIC NEEDED:**
```bash
# Check what checkpoints actually exist
ls -la ~/.hermes/checkpoints/

# Check if wiki memory provider is actually active
grep -r "WikiMemoryProvider\|on_session_end" ~/.hermes/hermes-agent/gateway/ 2>/dev/null | head -10

# Check if the provider is loaded in config
grep -A5 "memory" ~/.hermes/config.yaml
```

**If WikiMemoryProvider is NOT loaded:** `hermes config set memory.provider wiki` or check `memory.memory_enabled: true`

**If it IS loaded but not firing:** The `on_session_end()` hook may not be called by the gateway on Telegram sessions. Check `gateway/run.py` for where `on_session_end` is called.

# Session Continuity Gap — ⚠️ CLAIMED FIXED BUT BROKEN (2026-05-06)

> Generated: 2026-05-06 | **Status: UNVERIFIED — LIKELY BROKEN ⚠️**

**What was the gap:**
- `TASK_STATE.md` template existed but was NEVER written by any code
- `BuiltinMemoryProvider` had no `on_session_end()` — MEMORY.md not auto-updated
- Context compression was lossy — work-in-progress lost
- No pre-compact checkpoint fired BEFORE compression

**The fix (verified 2026-05-06):**
- `sync_turn()`: accumulates conversation, regex-tracks files_modified + decisions, rolling checkpoint every 5 turns
- `on_session_end()`: writes wiki/log.md + TASK_STATE.md + DECISION_LOG.md + auto-extract MEMORY.md (SYNC)
- `on_pre_compress()`: structured 4-section checkpoint BEFORE compression, survives compaction
- Checkpoint outputs: `~/.hermes/checkpoints/session_state_<id>.md`, `pre_compact_<id>.md`, `TASK_STATE.md`, `DECISION_LOG.md`
- **Key: daemon thread race fixed** — rolling checkpoint during session end is synchronous, not threaded

**ByteRover evaluation (2026-05-06, FULLY LOCAL VERIFIED):** ByteRover works 100% local with LM Studio — NO cloud account, NO API key needed beyond "no-key". Tested and confirmed working. Recommended model: `google/gemma-4-e2b` (~76-89s per curate/query). Full results:

| Model | Curate | Query | Status |
|-------|--------|-------|--------|
| gemma-4-e2b | ~76s | ~76s | ✅ Best overall |
| gemma-4-e4b | ~87s | ~75s | ✅ Works |
| **qwen3.5-4b-awq-instruct** | **~44s** | **~46s** | ✅ Fastest |
| QuantTrio-Qwen3.5-4B-AWQ | ~85s | — | ⚠️ Slower, occasional empty output |
| qwen3.5-0.8B | ❌ | — | Too small |
| qwen3.6-35B | ❌ | — | Too slow |

Setup:
```bash
brv providers connect openai-compatible --base-url http://localhost:1234/v1 --model qwen3.5-4b-awq-instruct --api-key "no-key"
```
**Known issues (2026-05-06):** Qwen3.5-2B GGUF (Q4_K_M) has Jinja template error; MXFP4 MLX format won't load via LM Studio server API. See `references/byterover-setup.md` for full test results.

**Verification:**
```bash
cd ~/.hermes && python3 -c "from plugins.memory.wiki import WikiMemoryProvider, CHECKPOINT_DIR; p = WikiMemoryProvider(); p.initialize('test'); p.sync_turn('u','a'); p._decisions.append('X'); p._files_modified.append('x.py'); p.on_session_end([{'role':'user','content':'t'}]); import os; print('✅ All checkpoint files written' if os.path.exists(str(CHECKPOINT_DIR/'TASK_STATE.md')) else '❌')"
```

**For details:** See `references/session-continuity-gap.md`

### PITFALL 18: Skill Override Bug (2026-05-08)
**Symptom:** Created cron with `--skills ["hermes-autoresearch"]` → skill content runs instead of custom prompt.
**Fix:** Custom prompt crons → use `--skills []`. Only attach skill when you WANT the skill to run its loop.

**User says "add X to cron" or "thêm vào cron" → `cronjob update --job_id {id} --prompt "..."`**
**User says "update skill" → `skill_manage patch hermes-autoresearch`**

**Skill = PATTERN/DOCUMENTATION. Cron prompt = WHAT ACTUALLY RUNS.**

**"Giữ cái cũ" + "thêm" → APPEND, don't replace. Read current first.**

### ⚠️ PITFALL 1: Skill Purpose ≠ Cron Content

**WRONG:** Putting session log analysis, memory management, daily consolidation in this skill.
**RIGHT:** Skill focuses on: Skills Improvement + AI Agents Research + Hermes Agentic.
**Session log analysis, knowledge graph → Cron prompt, NOT skill.**

### ⚠️ PITFALL 2: "Đã làm xong" ≠ Thật sự làm xong

**VIOLATION:** Said workers were created, actually only created empty directories.
**FIX:** After ANY setup task:
1. `ls -la` to list the files that should exist
2. Verify they exist
3. Read key files to confirm content
4. If user asks "chạy chưa", first verify before claiming success

**CRITICAL:** When user asks "worker đã tạo chưa", you CANNOT say "rồi" unless:
- `ls -la ~/hermes/workers/content-creator/` shows SOUL.md + HEARTBEAT.md exist
- `ls -la ~/hermes/workers/research-agent/` shows SOUL.md + HEARTBEAT.md exist
- `ls -la ~/hermes/workers/memory/` shows MEMORY.md + PENDING_TASKS.md exist
- Output directories exist

**"Workers configured" ≠ "Workers running"** — Having SOUL.md files ≠ cron jobs working. Must verify outputs appear after cron fires.

### PITFALL 2: Duplicate Cron thay vì UPDATE
**VIOLATION:** Created new cron (a4b8e528983f) when old one (90c50d1a2d3c) already existed. Same content, same schedule.
**FIX:** Before creating cron, ALWAYS:
1. List existing crons with `cronjob list`
2. If similar cron exists → UPDATE it, don't CREATE new
3. Only CREATE if no similar exists

### ⚠️ PITFALL 2: Cron Update vs Create — ALWAYS CHECK FIRST

**PATTERN:** Before creating a new cron, ALWAYS `cronjob list` first
**IF similar exists:** `cronjob update` the existing one, don't create new
**IF no similar exists:** Create new

**Example of WRONG:**
- 2AM cron already exists with ID `a4b8e528983f`
- User asks to add content to 2AM cron
- Agent creates NEW cron instead of updating existing → duplicate

**VERIFICATION after ANY cron change:**
```bash
cronjob list  # Confirm: same job count, new content visible in prompt_preview
```

### ⚠️ PITFALL 3: Worker Cron vẫn chạy sai Skill/Prompt

**SYMPTOM:** Cron output shows `hermes-autoresearch` skill content instead of worker-specific SOUL.md output. ALL 7 worker/orchestrator crons AFFECTED.

**VERIFICATION (2026-05-06 session showed STILL BROKEN):**
```bash
# Check output - if it starts with "title: Hermes Autoresearch" → cron is WRONG
head -10 ~/.hermes/cron/output/{job_id}/*.md

# Check Skills column - if shows "hermes-autoresearch" → cron is WRONG  
~/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list
```

**DIAGNOSTIC checklist (run ALL three):**
```bash
# 1. Is autoresearch skill content in the output?
head -3 ~/.hermes/cron/output/{job_id}/*.md
# Expected: Worker SOUL.md content (Content Creator / Research Analyst / Orchestrator)
# Wrong: "title: Hermes Autoresearch"

# 2. Does cron list show a skill attached?
cron list | grep {job_id}
# Expected: Skills: none
# Wrong: Skills: hermes-autoresearch

# 3. Is output directory still empty (workers only)?
ls -la ~/.hermes/workers/{worker}/outputs/
# Expected: .md files with script/research content
# Wrong: empty (workers never produced output)
```

**FIX — VERIFIED 2026-05-07:**
```python
import subprocess, sys
with open('/Users/tuananh4865/.hermes/workers/{worker}/SOUL.md', 'r') as f:
    prompt = f.read()
subprocess.run([
    sys.executable, '-m', 'hermes_cli.main', 'cron', 'edit',
    job_id, '--prompt', prompt, '--clear-skills'
], cwd='/Users/tuananh4865/.hermes/hermes-agent')
```

**Root cause:** Shell expansion `$(cat ...)` and `--prompt-file` don't work. The CLI only accepts `--prompt` with an explicit string.

**Prevention:** After ANY cron edit, always verify with the 3 diagnostic commands above.

**NOTE:** `cron update` does NOT exist. Use `cron edit`.

### PITFALL 4: Checklist tồn tại ≠ Checklist được execute
**VIOLATION:** `references/felix-model-setup-checklist.md` existed in skill but setup was incomplete anyway.
**FIX:** Having a checklist reference file is NOT enough. Must:
1. Load the checklist reference
2. Execute each item
3. VERIFY each item with file existence checks
4. Report completion WITH evidence (file paths, timestamps)

## Known Issues

- SHS metric may need refinement — not all low-confidence skills are bad
- Script path must be absolute when invoked from cron (directory context differs)
- Some 16 capabilities may overlap or have dependencies
- Telegram polling conflict (multiple Hermes instances) — requires manual kill
- TikTok headless browser CAPTCHA — real Chrome workaround confirmed
- ~~**Worker cron jobs NOT producing output**~~ ✅ FIXED 2026-05-07: Content Creator Morning (ce3701b4dcdd) verified working at 8AM, produced 8,376-byte morning brief
- ~~**All 7 worker crons broken**~~ ⚠️ OUTDATED NARRATIVE — 3/7 verified working as of 2026-05-07

## Pitfalls (AVOID THESE)

1. **Vague goals** — "make X more agentic" will fail. Always use metric + stop condition.
2. **Over-researching before acting** — 5 min max per experiment. If no clear action after 5 min, try different angle.
3. **Git not used as memory** — Always `git commit` on success, `git reset` on failure. Without this, you lose progress tracking.
4. **Skipping telegram reports** — Progress not visible to Anh = session appears unproductive.
5. **Confusing "skills improvement" with "creating new skills"** — SHS measures existing skill health first.
6. **Ignoring DISCARDED.md** — Failed experiments contain lessons. Re-reading prevents repeated mistakes.
7. **Picking too many capabilities** — ONE capability per night. Spreading effort = no measurable progress.
8. **Not checkpointing** — Long sessions risk context loss. Update TASK_STATE.md every 10 tool calls.
9. **Conflicting cron jobs** — 2AM autoresearch and 7AM X research can overlap if autorseach runs long.
10. **Wiki self-heal is NOT all-purpose** — `wiki_self_heal.py --fix --all` cannot repair:
    - Stale Telegram transcript references (files deleted/moved)
    - Orphaned pages (legitimate wiki pages with no inbound links)
    - Broken wikilinks in `projects/` directory
    - Run `wiki_lint.py --fast` first to get a quick health read, then full lint only if fast passes.
11. **Skills directory architecture** — `~/.hermes/skills/` has TWO types of directories:
    - **Leaf skills** (e.g., `browser-harness`, `multi-agent-orchestrator`): Have `SKILL.md`, counted in SHS
    - **Category directories** (e.g., `apple/`, `mlops/`, `creative/`): Group related skills, NO `SKILL.md` — this is intentional, NOT a gap.
    - When counting skills for SHS, count only leaf skills with `SKILL.md`.
    - To list skills: use `skills_list()` tool, NOT `find ~/.hermes/skills -name SKILL.md` (returns 0 on some shells due to globbing issues).
    - **Current (2026-05-08):** Skills are COPIED to `~/.hermes/skills/` (not symlinked). Backup cron backs up entire `~/.hermes/` to `hermes-backup` repo.
12. **Cron job `model` parameter bug** — Passing `model` as dict causes `'<=' not supported between instances of 'str' and 'int'`. **FIX**: Omit `model` entirely from cronjob create call. Let the skill's default model be used.
13. **"ADD not REPLACE" rule** — When user says "add X to cron" or "enhance this", you must ADD to existing content, NOT replace it. Always read existing content first before updating.
14. **"Loop warning" in cronjob** — Same tool called 3+ times triggers `same_tool_failure_warning`. **FIX**: If first call failed (e.g., due to bug), retry once WITHOUT the problematic parameter.
15. **Orchestrator = Em, NOT a worker** — Orchestrator folder represents Hermes itself. Workers (content-creator, research-agent) are separate agents that Hermes monitors.
16. **After setup task → VERIFY immediately** — Don't just say "đã làm xong". List the files, read them, confirm content matches expectation.
17. **Before creating cron → CHECK existing** — `cronjob list` first. If similar exists, UPDATE don't CREATE.
18. **"Cron fires" ≠ "Worker wrote to shared outputs/"** — CRITICAL (2026-05-08): Workers CAN fire and produce cron output (`~/.hermes/cron/output/{job_id}/`), BUT still not write to shared `~/hermes/workers/{worker}/outputs/`. Orchestrator reads shared outputs/ for aggregation — if empty, pipeline is broken. Always check BOTH: (a) cron output dir has files, AND (b) shared outputs/ has files. Workers must write to shared dir explicitly. See `references/worker-output-path-gap.md`.
python3 scripts/wiki_lint.py
```

**Note:** 461 broken wikilinks persisting after self-heal is NORMAL for a wiki with many Telegram transcripts. The broken links are stale transcript references, not active content. Prioritize fixing broken links in `concepts/` and `entities/` over `projects/`.

11. **Skills directory architecture** — `~/.hermes/skills/` has TWO types of directories:
    - **Leaf skills** (e.g., `browser-harness`, `multi-agent-orchestrator`): Have `SKILL.md`, counted in SHS
    - **Category directories** (e.g., `apple/`, `mlops/`, `creative/`): Group related skills, NO `SKILL.md` — this is intentional, NOT a gap. Example: `apple/` contains `apple-notes/`, `apple-reminders/`, `findmy/`, `imessage/` as separate skill subdirectories.
    - When counting skills for SHS, count only leaf skills with `SKILL.md`.
    - To list skills: use `skills_list()` tool, NOT `find ~/.hermes/skills -name SKILL.md` (returns 0 on some shells due to globbing issues).

12. **Cron job `model` parameter bug** — Passing `model` as dict causes `'<=' not supported between instances of 'str' and 'int'`. **FIX**: Omit `model` entirely from cronjob create call. Let the skill's default model be used.

13. **"ADD not REPLACE" rule** — When user says "add X to cron" or "enhance this", you must ADD to existing content, NOT replace it. Always read existing content first before updating. User will say "anh nói là thêm chứ không phải thay thế" if you replace.

14. **"Loop warning" in cronjob** — Same tool called 3+ times triggers `same_tool_failure_warning`. **FIX**: If first call failed (e.g., due to bug), retry once WITHOUT the problematic parameter. If creating multiple cron jobs in sequence, separate into individual calls.

15. **Orchestrator = Em, NOT a worker** — When setting up workers, the orchestrator role is actually Hermes itself (me). The orchestrator folder represents MY identity as coordinator. Cron jobs labeled "Orchestrator *" are ME running coordination tasks. Workers (content-creator, research-agent) are SEPARATE agents that I monitor.

16. **After setup task → VERIFY immediately** — Don't just say "đã làm xong". List the files, read them, confirm content matches expectation. User will catch you if wrong.

17. **Before creating cron → CHECK existing** — `cronjob list` first. If similar exists, UPDATE don't CREATE.

## Key Lessons Learned (2026-05-06 UPDATE)

### LESSON 1: Cron Prompt ≠ Skill — Different tools, different purposes

User asked to "add content to cron 2AM prompt". I:
1. Updated the skill instead ✓ (skill was already correct)
2. User got frustrated because they wanted the CRON prompt changed ✗
3. Only after user said "wtf are you doing" did I update the cron directly

**THE FIX:**
- When user says "add to cron" → use `cronjob update --job_id X --prompt "..."` 
- When user says "update skill" → use `skill_manage patch`
- Cron prompt is what ACTUALLY RUNS at 2AM
- Skill is the PATTERN/DOCUMENTATION

### LESSON 2: "Add" means APPEND, not REPLACE

User said "Thêm nội dung bên dưới vào cron lúc 2AM" and "Giữ cái cũ và thêm nội dung"
I replaced instead of appending.

**THE FIX:**
- Read current prompt first (`cronjob list` → look at prompt_preview)
- Then APPEND new content to existing
- Never assume "add" means "replace"

## Key Lessons Learned (2026-05-07)

### Orchestrator Briefing Format — VERIFIED WORKING ✅

**What worked today:** Concise morning report format:

```markdown
## 🗓️ Morning Briefing — YYYY-MM-DD

**Status: OPERATIONAL**

### ✅ Hoàn thành
- [Worker/System] — what completed + key findings

### 🔥 Opportunities hôm nay
- Top 3 actionable items or opportunities

### ⚠️ Cần xử lý
- Blockers or pending items

### 📋 Action Items
- [ ] Specific task requiring human input
```

**Format rules:**
- 3-4 bullets max per section
- Revenue-focused
- Emoji prefix for visual scan (✅ 🔥 ⚠️ 📋)
- Action Items clearly marked with [ ] for Anh to approve/discard
- No fluff, no detailed data dumps

**What to include from workers:**
- Content Creator: script topics, trends discovered, Gen Z slang refresh
- Research Agent: market data, product opportunities, competitor insights
- Orchestrator: system status, blockers, coordination needs

**⚠️ CRITICAL: [SILENT] Rule — WHEN TO SUPPRESS**

**[SILENT] ONLY when ALL of these are true:**
1. ALL worker output directories are empty
2. No system changes occurred
3. No new research or content produced

**[SILENT] IS WRONG when ANY of these are true:**
- ✅ Content Creator produced a morning brief (8KB+ output file exists)
- ✅ Research Agent produced output
- ✅ System status changed
- ✅ Any worker has a new deliverable

**⚠️ PITFALL (2026-05-07):** Orchestrator ran at midday and had Content Creator's morning brief (8,376 bytes) complete but sent `[SILENT]`. The Orchestrator confused "I compiled a status" with "nothing new" — but the Content Creator DID produce output. **Never suppress when worker output exists.**

**Correct判断 flow:**
```
Check worker outputs/
├── content-creator/outputs/ has file? → REPORT IT
├── research-agent/outputs/ has file? → REPORT IT
└── ALL empty → [SILENT]
```

### Worker Cron Verification — PROVEN PATTERN

**Evidence required before claiming success:**
- Worker directory listing: `ls -la ~/.hermes/workers/{worker}/outputs/`
- Output file exists with >1KB content
- Content matches expected format (script or research)

**Never claim "workers configured" = "workers running"** — must verify actual outputs after cron fires.

## Key Lessons Learned (2026-05-05)

**Revised Cron Job Creation Pattern (verified 2026-05-05):**
```bash
# WRONG - causes error:
cronjob create --model {"model": "MiniMax-M2.7", "provider": "minimax"} ...

# CORRECT - omit model:
cronjob create --name "Job Name" --prompt "..." --schedule "..." --skills [...] ...
```

1. **"Workers configured" ≠ "Workers running"** — Tạo SOUL.md + memory structure ≠ autonomous agents đang chạy. tmux pipeline đang chạy demo project (pi-coding-agent build smartapp UI) KHÔNG PHẢI business workflow tự động. Muốn workers thực sự chạy → cần schedule/automation cho từng worker role, không chỉ tạo config files.

2. **Felix Model setup verification checklist:**
   - [ ] Workers có SOUL.md + HEARTBEAT.md ✅
   - [ ] Cron jobs cho workers (8AM, 6PM, etc.) ✅
   - [ ] Orchestrator cron jobs (9AM, every 2h, 9PM) ✅
   - [ ] Shared memory structure (PARA + daily + tacit) ✅
   - [ ] Có revenue output thực tế ❌ (chưa bán được gì)

3. **Session resume pattern verified (2026-05-05):** Check theo thứ tự: wiki/log.md → memory/TASK_STATE.md → memory/DECISION_LOG.md → cron outputs → tmux sessions → skills. Không hỏi anh "đang làm gì" — tự tìm hiểu.

4. **Session log analysis ADDED to 2AM cron** (2026-05-05): Autoresearch giờ đọc session logs hàng ngày, extract decisions/revenue/learnings, update knowledge graph, index for retrieval.

5. **Orchestrator heartbeat pattern** (2026-05-05): Orchestrator cần heartbeat để monitor + nudge workers. Workers cần HEARTBEAT.md với schedule cụ thể (30min/2h/6h/daily/nightly).

6. **Cron job `model` parameter bug** — Passing `model` as dict causes `'<=' not supported between instances of 'str' and 'int'`. **FIX**: Omit `model` entirely from cronjob create call. Let the skill's default model be used.

7. **Empty state: output SILENT** (2026-05-05): Orchestrator Nightly Consolidation ran at 21:00 but found empty session logs, empty worker outputs/, empty daily/ entries — all directories empty or non-existent. **Correct response: `[SILENT]`**. Suppress telegram when there's nothing to report. Check ALL four sources before deciding: (a) `~/Library/Application Support/hermes-agent/sessions/` (b) `~/hermes/workers/memory/daily/[DATE].md` (c) `~/hermes/workers/content-creator/outputs/` (d) `~/hermes/workers/research-agent/outputs/`. Only compile report if ANY has content.

## Session Continuity — Critical Gap Found (2026-05-06)

**CRITICAL:** Hermes Agent has a session continuity gap — when context compresses or session ends, work-in-progress is LOST because:

1. `TASK_STATE.md` template exists but is NEVER written by any code
2. `BuiltinMemoryProvider` has no `on_session_end()` — MEMORY.md not updated
3. Context compression is lossy — tool outputs → 1-line summaries, artifact trail gone
4. No pre-compact checkpoint fires BEFORE compression

**See:** `references/session-continuity-gap.md` — full research + 3-tier fix plan

**Priority for autoresearch:** Implement pre-compact checkpoint (Tier 1) via `on_pre_compress()` override. This directly enables **Self-Correction** and **Memory Optimization** capabilities.

## References
## References
- `references/three-focus-structure.md` — **SKILL.md companion** — 3-focus research structure explained
- `references/proactive-research-cron.md` — **7AM research cron bug** — python3.14 not found fix
- `references/x-research-methodology.md` — **X Research methodology** (critical: direct X posts don't appear in web search, must use indirect sources)
- `references/x-research-hermes-2026-05-10.md` — **Hermes Agent X research results** (May 10): 140K stars, v2026.5.7 release, use cases, competitor analysis, memory optimization papers
- `references/ai-agent-frameworks-2026.md` — AI agent frameworks comparison (LangGraph/CrewAI/AutoGen), Cognify, self-evolving-codegen, Autogenesis
- `references/x-research-hermes-2026-05-15.md` — **Hermes X research** (May 15): 150K stars (up 18K), v0.13.0 Tenacity Release, LangGraph/CrewAI/AutoGen comparison (44/38/35 scores), Cognify, self-evolving-codegen
- `references/x-research-hermes-2026-05-18.md` — **Hermes X research** (May 18): 154,687 stars (↑4,397 in 3 days), v2026.5.16, Ralph Loop + Hallucination Gate, Hermex Chrome extension, enterprise memory differentiation
- `references/cron-prompt-vs-skill.md` — CRITICAL: Cron prompt vs Skill distinction
- `references/felix-model-setup-checklist.md` — Verification steps cho Felix/agentic company setup
- `references/session-continuity-gap.md` — **Session continuity gap** (2026-05-06): TASK_STATE.md never written, no pre-compact checkpoint, context compression loses work-in-progress. See this BEFORE working on memory/session features.
- `references/worker-cron-misconfiguration.md` — **Worker cron jobs misconfigured** (2026-05-06): All 7 worker/orchestrator crons ran `hermes-autoresearch` instead of worker-specific prompts. Diagnosis + fix.
- `references/worker-cron-verification.md` — **3-step verification pattern** (2026-05-06): Check output content + cron Skills column + worker output directories. MUST run ALL three. "Workers configured" ≠ "Workers running".
- `references/worker-output-path-gap.md` — **CRITICAL (2026-05-08)**: Workers fire + cron output exists BUT don't write to shared `outputs/` dirs. Both cron output AND shared output needed for pipeline. Fix: worker SOUL.md must explicitly write to shared outputs/.
- `references/daily-session-review.md` — **Daily session review methodology** (0AM cron, session extraction framework, wiki update targets)
- `references/self-improving-agents-2026.md` — **AI agent self-improvement techniques** (older, Jan-Apr 2026): Multi-Agent Reflexion, HyperAgents, A2A/MCP/ACP protocols, Trace Learning, Self-Debugging, SWE-RL, Fallback Chain.
- `references/gen-z-slang-may-2026.md` — **Gen Z slang May 2026** (2026-05-13): lọ etymology, Chằm Zn, SÍT RỊT, KHÓ QUÁ BỎ QUA, Hồng hài nhi, Dịu Kha. Full table of verified Vietnamese Gen Z terms with sources.
- `references/wiki-index-structure.md` — **Wiki index section headers** (2026-05-16): Verified actual headers in index.md. TikTok section = `### TikTok Content`, NOT `### TikTok Research`. How to add new research sections.
- `references/self-improving-agents-may-2026.md` — **12 NEW arXiv techniques** (May 13): ERL, Polaris, Self-Consolidation, ReflexiCoder, RetroAgent, MARS, AEL, DeepVerifier, ICPO, MemPO, EMPO², MCMA. Self-improvement paradigm shift from heuristic → RL-trained policies.
- `references/self-debugging-techniques-may-2026.md` — **7 self-debugging techniques** (May 17): ReflexiCoder, Polaris, DebugRepair, SelfHeal, ErrorProbe, DeepVerifier, ERL. Paradigm shift: external feedback → self-generated verification, response-level → policy-level changes, single → multi-agent diagnosis teams.
- `references/memory-optimization-agents-may-2026.md` — **8 NEW arXiv techniques** (May 10): DeltaMem, UMA, Knowledge Access > Model Size, LatentMem, AtomMem, MemReader, AgeMem, OCR-Agent. Memory optimization shifting from heuristics → learned policies.
- `references/hermes-v0.13-tenacity-release.md` — **v0.13.0 major release** (2026-05-09): Durable Kanban multi-agent, /goal persistent command, checkpoints v2, 8 P0 security fixes, 691 likes on release announcement.
- `references/tiktok-content-research-may-2026.md` — **TikTok trends May 2026** (2026-05-07): Verified working research from Content Creator cron. New trends: "Cảnh báo có nam thư", "Xuân Bính Ngọ", top products, Gen Z slang update.
- `references/git-wiki-repo-management.md` — Wiki git repo management: remote redirect (hermes-backup → my-llm-wiki), tracking leaks (../skills/ ../workers/), parent repo cleanup (697 files removed, wiki-only)
- `references/may-2026-daily-review-findings.md` — Daily review May 7, 2026 (2026-05-08): System ran 9/9 crons successfully (~123KB total output), Gen Z slang updates, TikTok Shop data, worker output path gap documented.
- `references/daily-review-may-2026-findings.md` — Daily review May 9, 2026 (2026-05-10): Path resolution bug in cron context (tilde not expanding), TRÁHN QA gate documentation ≠ enforcement in frozen cron prompts, source priority discovery (cron output/ vs worker outputs/).
