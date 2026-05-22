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

### Cần xử lý
- [BLOCKER] X Developer account + xurl authentication
- [PENDING] OpenClaw gateway restart after config changes
- [PENDING] Ollama not installed (for potential Mem0 local setup)

### Google I/O 2026 Content
- 30s video: Dark sphere → Glass cards → 3 products
- Gemini 3.5 Flash, Omni, Spark, Intelligent Search, Universal Cart, Smart Glasses, Antigravity

---

## 2026-05-13

[Previous entries would be here]
