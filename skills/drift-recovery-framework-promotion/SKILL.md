---
name: drift-recovery-framework-promotion
description: Class-level pattern for when user escalates framework rules to VĨNH VIỄN + KHÔNG BỎ khi compaction. Covers the 4-mechanism defense (Wiki Persistent Storage + Daily Curator + DRIFT-1 Active-Checklist + Holographic Memory).
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [system-wide-rule, compaction-safe, drift-recovery, user-feedback, anh-tuấn-anh]
    references: [wiki/concepts/drift-recovery-3-systems-2026-07-19.md, references/anti-compaction-recipe-2026-07-19.md]
---

# Drift Recovery — Framework Promotion to VĨNH VIỄN (Class Skill)

> **Class scope:** Bất kỳ khi nào user escalate 1 rule từ "khuyến nghị" → "BẮT BUỘC VĨNH VIỄN + KHÔNG BỎ khi compaction", áp dụng pattern này. Đã verified 19/07 với 3 framework (Fable 5 + Karpathy + Loop Engineering) + anh Tuấn Anh.

## Khi nào dùng skill này

User có câu escalation dạng:
- "BẮT BUỘC tuân theo..."
- "VĨNH VIỄN"
- "KHÔNG BAO GIỜ bỏ qua..."
- "KHÔNG ĐƯỢC skip khi compaction"
- "Toàn bộ thời gian hiệu lực..."
- "Bất kể task nào..."

→ **KHÔNG** patch nhỏ. **PHẢI** chuyển sang VĨNH VIỄN + 4 mechanism compaction-safe.

## 4 Mechanism Compaction-Safe (BẮT BUỘC activate tất cả)

### Mechanism 1: Wiki Persistent Storage
- Save concept page vào `/Volumes/Storage-1/Hermes/wiki/concepts/<topic>-<YYYY-MM-DD>.md`
- Volume riêng (Storage-1) — KHÔNG bị memory compact
- **Verified:** 19/07 concept page `drift-recovery-3-systems-2026-07-19.md` (8.9KB) survive qua 1 lần compaction khi entities file reset

### Mechanism 2: Daily Memory Curator (cron 02:00)
- `~/.hermes/skills/devops/nightly-memory-curation/` skill auto-re-derive entities từ concept page
- Mỗi đêm cron chạy → entities file được restore từ concept page nguồn

### Mechanism 3: DRIFT-1 Active-Checklist (TRƯỚC mỗi response)
- Em PHẢI tự check 5 câu trước khi gửi response:
  1. **Karpathy #1**: Em đã state assumption? (Y/N)
  2. **Karpathy #4**: Em có plan checklist? (Y/N)
  3. **Fable §3**: Em đã load skill liên quan chưa? (Y/N)
  4. **Loop 1**: Output có verify được không? (Y/N)
  5. **Khẩu hiệu 🎯**: Em có nói systems used không? (Y/N)

### Mechanism 4: Holographic Memory (importance:1.0)
- Memory backend `provider: holographic` (LOCAL, no API key)
- Try save importance:1.0 entry vào memory tool → entry LUÔN persist qua compaction
- **Lưu ý:** Memory tool có limit 2200 chars → batch remove entries cũ trước khi add mới
- **Fallback:** nếu memory limit đầy → rely on M1+M2+M3 (3 mechanism đã đủ)
- **Detailed recipe:** See `references/anti-compaction-recipe-2026-07-19.md` (Option A/B/C + 3-step batch + decision tree + real case study)

## Workflow 4 Action BẮT BUỘC khi user escalate

1. **Patch SOUL.md** § FIRST-CLASS ngay tại vị trí dễ thấy (đầu file hoặc sau System-Wide Rule cũ)
   - Thêm table 3 system + 4 mechanism + 5-command verify
   - Reference concept page path
2. **Update concept page** với anh's verbatim quote + FINAL STATUS section
3. **Append log entries** vào `/Volumes/Storage-1/Hermes/logs/daily/<YYYY-MM-DD>.jsonl` (manual vì hook auto-log chưa fire)
4. **Verify 5 command:**
   ```bash
   ls -la /Volumes/Storage-1/Hermes/wiki/concepts/<topic>.md
   grep "3 HỆ THỐNG BẮT BUỘC VĨNH VIỄN" ~/.hermes/SOUL.md
   grep "L55\|<lesson-id>" /Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md
   hermes cron list | grep memory-curator
   grep "provider: holographic" ~/.hermes/config.yaml
   ```

## Anti-pattern TUYỆT ĐỐI

- ❌ Patch nhỏ rồi báo "xong" — phải có đủ 4 mechanism
- ❌ Chỉ save vào memory tool mà không có wiki concept page → compact mất
- ❌ Bỏ qua verify step vì "đã rõ ràng"
- ❌ Hỏi lại user "anh muốn em patch full scope không?" — user đã nói rồi, execute ngay
- ❌ Retry memory call 5+ lần khi memory đầy — memory tool KHÔNG auto-evict, retry sẽ fail mãi
- ❌ Skip Option B (batch remove+shorten+add) vì "phức tạp" — đây là cách DUY NHẤT activate mechanism 4

## Related

- `wiki/concepts/drift-recovery-3-systems-2026-07-19.md` — Original concept page
- `wiki/entities/learned-about-tuananh.md` § L55 + L55.b
- `~/.hermes/SOUL.md` § "🚨🚨🚨 3 HỆ THỐNG BẮT BUỘC VĨNH VIỄN"
- `references/anti-compaction-recipe-2026-07-19.md` — Memory tool limit work-around (Option A/B/C choice + 3-step batch + decision tree + real case study) — VERIFIED session 19/07
- `references/verify-compaction-safe.md` — 5-command verify recipe (TODO)
- `evidence-first-delivery` § Drift Recovery Pattern — 4-step recovery when anh flags drift
- `system-wide-mandate-enforcement` § Layer 7 — anti-compaction chi tiết
- `hermes-memory-providers` — provider selection + limit management