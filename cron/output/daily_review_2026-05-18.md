# Hermes Daily Review — 2026-05-18

## 📊 Session Summary

**Sessions analyzed:** 4 (Tuấn Anh DM, O-Lab group x3)  
**Total messages:** ~280 across all sessions  
**Active workers:** Content Creator (May 11), Research (May 12) — stale 7 days

---

## ✅ Hoàn thành

### OpenClaw Gateway Fix
- **Issue**: OpenClaw gateway không start được — `MINIMAX_API_KEY` bị truncated (125→13 chars) trong LaunchAgent plist
- **Fix**: 
  1. Đọc full key từ `~/.hermes/.env` (125 chars)
  2. Update `~/Library/LaunchAgents/ai.openclaw.gateway.plist` với full key
  3. Restart LaunchAgent — gateway live ✅
- **Discovery**: Config có `mcpServers` key không được hỗ trợ → gây fail → đã xóa

### OpenClaw requireMention Fix
- **Issue**: Bot @Researcher_Clawd_Bot không reply khi được mention trong O-Lab group
- **Root cause**: 
  1. `mcpServers` config gây gateway fail
  2. Truncated API key gây authentication error
  3. Config cache không reload sau fix
- **Fix**: Xóa mcpServers, fix full key, restart gateway → bot hoạt động ✅

### HyperFrames Animation Fix
- **Issue**: Video gửi cho anh không có motion — toàn opacity fade
- **Root cause**: GSAP timeline không auto-trigger trong HyperFrames render
- **Fix**: ResearchClaw dùng `window.__timelines` pattern để HyperFrames seek animation đúng
- **Result**: 45s video với 4 phases có actual motion (orb pulse, spheres float, glass slide, ring expand)

### OpenClaw Daemon Setup
- **Confirmed**: `ai.openclaw.gateway` LaunchAgent đang chạy (pid varies per session)
- **Startup**: Tự khởi động khi máy reboot
- **Logs**: `/tmp/openclaw/openclaw-YYYY-MM-DD.log` — 51MB log file

---

## 🧠 Learnings

### OpenClaw on macOS
1. **Gateway start qua launchd** — không inherit terminal env vars
2. **plist env vars** — phải set trực tiếp trong plist, không đọc .env
3. **mcpServers config** — không được OpenClaw hỗ trợ, gây fail silently
4. **requireMention** — set `true` trong `groups.*` config, hoạt động per-topic

### HyperFrames + GSAP
1. **window.__timelines** — pattern để HyperFrames access GSAP timelines
2. **gsap_css_transform_conflict** — warning khi CSS transform + GSAP tween cùng animate scale
3. **Seek vs Play** — HyperFrames seek animation cần timeline object reference

### Wiki Memory Architecture
1. **Context compaction** xảy ra trong session — hệ thống auto-summarize middle turns
2. **Stub vs Full** — WikiMemoryProvider stub (136 lines) loaded thay vì full (1458 lines) — plugin load path priority issue
3. **Hooks working**: `sync_turn()`, `on_pre_compress()`, `on_session_end()` verified

---

## ⚠️ Cần xử lý

1. **Workers stale 7 days** — Content Creator (May 11), Research (May 12) cần restart hoặc pause
2. **OpenClaw skills** — ResearchClaw workspace có AGENTS.md, SOUL.md, IDENTITY.md nhưng 0 SKILL.md files. OpenClaw setup không có `skills/` directory
3. **Gateway device identity** — `gateway connect failed: device identity required` khi check status, nhưng gateway vẫn hoạt động
4. **Log rotation** — 51MB log file cho 1 ngày, cần cleanup hoặc rotate

---

## 📁 Files Created/Updated

### Wiki
- `log.md` — updated với daily review entries
- `hermes-x-research-2026-05-18` — Hermes X research (v2026.5.16, 154K stars, Kanban multi-agent)

### Cron Output
- `daily_review_2026-05-18.md` — this file

---

*Report generated: 2026-05-19 00:00 AM*
*Sessions: 4 total | Messages: ~280 | Model: MiniMax-M2.7*