# Wiki Log

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

## 2026-05-13

[Previous entries would be here]
