# Wiki Log

## 2026-06-05

### Daily Activity
- **MiniMax-M3** running with 1M context, 59% SWE-Bench (config verified)
- **API issue**: 1004 error on model list endpoint — model works, list broken
- **Storytelling lesson**: Hermes taught Anh viral content via storytelling
- **Wiki Memory Forget**: 83 stale topics identified (dry-run)

### Cron Jobs (All ✅)
| Job | Time | Status |
|-----|------|--------|
| Daily Session Review | 00:03 | ✅ |
| Autoresearch Nightly | 02:05 | ✅ (66 messages) |
| Wiki Memory Forget | 03:00 | ✅ dry-run |
| Daily Backup | 03:01 | ✅ +3,881/-110 |
| Wiki Health | 04:00 | ✅ SILENT |
| X Research | 07:02 | ✅ (35 messages) |

### Sessions
- **DM 20:46**: Model question → MiniMax-M3 confirmed, config explained
- **Group 21:08**: Storytelling viral content lesson

---

## 2026-05-14

### Ngày nghỉ ngơi — Cron jobs đã tắt

**重大事件**: Anh tắt toàn bộ cron jobs (7 jobs) lúc 10:48 AM

#### Hoàn thành:
- Computer_use feature enabled và verified (TCC permissions OK, drag NOT supported)
- New income stream research: Affiliate + AI Tools, Roblox + AI
- Trending keywords Vietnam e-commerce May 7-14
- TikTok Shop product links for trending keywords (15 products)
- GitHub backup completed (+1456/-36)

#### Skills Updated:
- macos-computer-use (setup, drag limitation, browser-harness pitfall)
- chrome-tabs-applescript (active tab vs window name)
- business-opportunity-research (new skill created)
- tiktok-viral-script (LỌ vs LỎ elevated to TRÁHN-level)
- hermes-autoresearch (dual-output-path)
- hermes-github-backup (non-fast-forward recovery)
- multi-agent-orchestrator (PITFALL 23 patched)

#### Key Discoveries:
- computer_use: backend expects 0.5.0, 0.1.5 works
- browser-harness fails on login-gated sites (X, TikTok)
- Summer Cooling NOW: 37-40°C Vietnam, Neck Fan 64% margin

#### Cần xử lý:
- Pipeline Google Sheets → Facebook viral → affiliate comment (chưa build)
- computer_use scroll còn nhầm sang BetterDisplay

---

## 2026-05-21

### Memory Health Check
- Wiki: 1,768 files, ~2,785 broken wikilinks, ~192 orphan pages
- Builtin memory: state.db (456 sessions, 20,026 messages)
- Bug: WikiMemoryProvider rapid writes (5 writes in 8ms) corrupting USER.md
- Decision: Keep wiki as primary memory — Mem0 NOT needed
- Action: Cleaned USER.md + MEMORY.md (reset garbage)

### X/Twitter Automation — FAILED
- Playwright: Upload OK, Post button disabled by X anti-automation
- browser-harness: Can't read encrypted Chrome cookies
- Root cause: X detects automation → aria-disabled="true"
- **Solution: Setup xurl with X API credentials**

---

## 2026-05-22

### OpenClaw Multi-Agent Setup
- Created `techlead` agent in OpenClaw
- Added @TechLead_ClawBot token to config (NEW bot, separate from @ClawdZ1E_Bot)
- Two agents now active: ResearcherClaw + TechLeadClaw
- Correct Telegram group ID format: `-5195161709` (not `-1005195161709`)

### Memory Architecture
- Decision: Keep wiki as primary memory — Mem0 NOT needed (cloud-only, no Hermes integration)
- Bug: WikiMemoryProvider rapid writes corrupting USER.md
- Action: Cleaned USER.md + MEMORY.md (reset garbage)
- Mem0 OSS requires direct Python library usage, not a plugin

### X Automation Blockers (PERSISTENT)
- X.com anti-bot detection blocks Playwright automation
- xurl installed but NOT authenticated — needs X Developer OAuth credentials
- Cookie export from Chrome doesn't maintain X login state
- **Action needed**: X Developer account + xurl setup

### Wiki Maintenance
- Created 3 wiki content pages to fix broken links
- ~2,615 broken wikilinks remain (old Telegram dumps) — not critical
- tiktok-viral-script content lives in `learning/` directory, not `.md` stubs

### Bot2Bot Collaboration
- OpenClaw `ownerAllowFrom` format: `telegram:123456789`
- Telegram bot @mention WORKS between bots in groups

---

## 2026-05-24

### Skills Umbrella-Building Consolidation
- Merged 5 narrow skills into class-level umbrellas:
  - `hyperframes` + `motion-graphic-video` → merged (TikTok motion graphics)
  - `xurl` + `x-repost` + `playwright-automation` + `x-repost-workflow` → `xurl` umbrella (X.com automation)
  - `deep-research-wiki` → merged into `hermes-autoresearch` (deep research methodology)
- Archived 5 skill directories to `.archive/`
- X credentials: `@TyayUno` (Anh Trinh's X account), cookies at `/tmp/x_cookies.json`

### Hermes Autoresearch — Complete Failure
- Web search completely down all night (both `web_search` HTTP 400 + `mcp_exa` unreachable)
- Workers completely dead — output directories empty (no files at all)
- Git commit `988c9b5be`: "autoresearch 2026-05-24: Wiki clean (1829 files, 0 issues), 238 skills healthy, Workers DEAD, web search down"
- Reference doc: `references/autoresearch-2026-05-24-complete-failure.md`

### Hermes Daily Backup — Success
- Files changed: 12, Insertions: +1581, Deletions: -38
- Git push: `60c57630d → f0aabeef0` ✅

### Wiki Status
- 1829 files, 0 issues — clean wiki health
- 238 skills healthy — SHS = 0 (perfect)

### Cần xử lý (2026-05-24)
- [BLOCKER] Workers dead — Content Creator + Research Agent cần manual restart
- [BLOCKER] Web search down — API keys/config cần check
- [PENDING] X Developer account + xurl OAuth setup
- [BLOCKED] Gen Z slang sync — workers dead + web search down

### Google I/O 2026 Content
- 30s video: Dark sphere → Glass cards → 3 products
- Gemini 3.5 Flash, Omni, Spark, Intelligent Search, Universal Cart, Smart Glasses, Antigravity

---

## 2026-05-25

### Workers Deleted by User
- User commanded: "Xoá toàn bộ workers"
- Deleted: `memory/` and `orchestrator/` worker directories
- Workers permanently removed from system

### Hermes v0.14.0 "Foundation Release" (May 16)
- **157.2K+ GitHub stars**, #46 global OpenRouter rank
- Native Windows beta (no WSL2), 180x faster browser (CDP rewrite)
- Live session handoffs (`/handoff`), Local OpenAI proxy
- LINE + SimpleX + Microsoft Teams integrations
- X Premium + Grok now integrated
- **Nvidia partnership**: "Hermes Unlocks Self-Improving AI Agents" on RTX AI Garage
- **Milestone**: Overtook OpenClaw as most-used open-source AI agent on OpenRouter

### Autoresearch Nightly (2AM) — Workers DEAD
- Workers: Content Creator + Research Analyst dead 6-8 days
- Wiki: Clean (1,579 concept files, 0 issues)
- Skills: 233 healthy, SHS=0
- Research: Multi-Agent Coordination (5 techniques documented)
- **→ Workers deleted by user later in day**

### Daily Backup (3AM) — Success
- 56 files changed, +5,888 insertions, -296 deletions
- Commit: `0b3b39f90`

### X Research Daily (7AM) — Success
- Hermes v0.14.0 milestone: 157.2K stars, +869 stars/week
- v0.14.0 features: Windows, 180x faster browser, vision, handoffs
- Top use cases: Multi-agent teams (12 parallel), business automation, skills marketplace

---

## 2026-05-26

### No User Revenue Activity
- Workers deleted May 25 — Content pipeline offline
- No TikTok Shop affiliate sessions today
- Gen Z slang sync: web search fallback blocked (Kaiwa/phongvu 400/403 errors)

### Cron Sessions Summary
| Session | Time | Content |
|---------|------|---------|
| Daily Review | 00:00 | Workers deleted, Hermes v0.14.0 milestone documented |
| Autoresearch | 02:00 | MOSS self-evolution (arXiv:2605.22794), wiki clean 1,835 files |
| Backup | 03:00 | GitHub: 44 files, +5,060/-358 |
| X Research | 07:00 | Memento-Skills (arXiv:2603.18743), web_extract fallback rule |

### Key Learnings
- **MOSS**: Self-Evolution through Source-Level Rewriting — agents rewrite own source code (24th technique)
- **Memento-Skills**: frozen LLM + editable skill library = 80% task success (+78% vs baseline)
- **Bumblebee**: perplexityai Go scanner for supply-chain compromises (npm/pip/cargo)
- **web_extract 400 errors**: Consistent failures on github.com, venturebeat.com — fallback chain needed

### Skills Updated
- `hermes-autoresearch`: web_extract fallback rule, MOSS + Memento-Skills references added

### Wiki Health
- Files: 1,835 | Issues: 0 | Skills: 233 healthy, SHS=0

---

## 2026-05-30

### No TikTok Shop Revenue Activity
- Workers deleted May 25 — Content pipeline offline
- No TikTok Shop affiliate sessions today
- User focus shifted to YouTube channel planning

### YouTube Channel Research — Anh Cường Project
- **Session**: 20260530_125522 (12:55 PM - O-Lab thread 1961)
- **Source**: Think Media video "Genius YouTube Advice for 15 Minutes Straight"
- **Research**: Summary + growth strategy extraction

### Key YouTube Learnings (from Think Media)
1. **100 videos rule** — Post consistently to master your niche
2. **Niche emergence** — Passion + audience demand intersection
3. **CTA best practice** — Clear call-to-action increases engagement
4. **Curiosity titles** — "Why" and "How" titles drive clicks
5. **Trend surfing** — Ride trending topics in your niche
6. **Patience** — YouTube growth takes time

### Hermes v0.15.0 Features
- Discussed in Telegram session 20260530_212752

### Cron Sessions Summary
| Session | Time | Content |
|---------|------|---------|
| Daily Review | 00:00 | Workers still offline, YouTube focus |
| Autoresearch | 07:00 | Skills improvement, wiki updates |

---

## 2026-05-31

### ⚠️ CRITICAL: Session Recording Broken
- **Last session logged:** May 28, 2026 — No sessions found for May 29, 30, 31
- **sessions.db:** 0 bytes (empty/corrupted)
- **Root cause:** Unknown — Could be disk space, permission, or Hermes service issue
- **Cron jobs still running** — evidenced by output files up to May 31 07:03

### No User Activity
- Workers offline since May 25 (deleted by user)
- Content pipeline dead
- TikTok Shop: No revenue activity
- YouTube: Research phase only (no filming sessions)

### Cron Jobs Status
- Daily Review, Autoresearch, Backup — all still running
- Session recording to `sessions/` directory broken

---

## 2026-05-13
