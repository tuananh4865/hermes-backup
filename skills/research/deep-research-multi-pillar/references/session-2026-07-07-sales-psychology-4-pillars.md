# Session 2026-07-07 — 4-Pillar Sales Psychology Research + Master Framework Synthesis

**User:** Tuấn Anh
**Request:** *"Tìm và học về nghệ thuật bán hàng, tâm lý bán hàng, tâm lý học đám đông, thói quen người tiêu dùng, khoa học hành vi. Deep research trên 200 kết quả cho anh! Ngoài tìm trên báo thì phải tìm trên X nữa!!!"*

**Channel:** Telegram (mobile, không ngồi Mac)

## Outcome

| Metric | Value |
|---|---|
| Subagents dispatched | 4 (parallel) |
| Total runtime | 4m24s |
| Total URLs delivered | 319 (≥200 target) |
| Output files | 4 research + 1 master framework |
| User satisfaction | Hiện chưa có feedback (synthesis sent, waiting) |

## Lessons — Verified

### L1: Auto-skip scope confirm khi user đã rõ deliverables
- User đã chỉ rõ: 5 chủ đề (sales + crowd + consumer + behavioral) → gom thành 4 trụ, 200+ URLs, "báo + X/Twitter".
- Skill default = confirm scope. Nhưng anh-escalation style = skip confirm, dispatch ngay.
- **Update:** Bước 1 giờ là "Scope (auto-detect khi user đã rõ deliverables)" — skip khi user đã liệt kê rõ domain + số trụ + source minimum + channel hints.

### L2: 4 subagent batch OK khi tasks độc lập
- Default config = 3 concurrent. Tasks độc lập hoàn toàn (4 file output khác nhau, không share state, không cần output của nhau) → scale up OK.
- **Update:** Bước 2 "Launch song song subagent" — thêm concurrent limit table: 4-5 OK nếu tasks độc lập, 6+ split waves.

### L3: Pitfall #10 (no poll) — đã apply đúng
- Sau khi `delegate_task` trả "dispatched" → em update todo + báo user "đang đợi" + KHÔNG poll.
- Kết quả tự re-enter 4m24s sau.

### L4: Telegram embed cho master framework — applied đúng
- Sau khi 4 subagent trả về → em verify 4 file (size + URL count) → write master framework → embed full summary trong reply Telegram (không chỉ save file).
- Reply structure: top-of-reply counts + 7 armed principles table + 11-phase blueprint + 1-line summary + file paths cho bookmark.

### L5: NEW — Master Framework Synthesis từ 4 files (Pitfall #12)
- Sau khi 4 subagents trả summary (mỗi cái 100-200 dòng), em PHẢI đọc lại 4 file thật (grep `## Top 5 Master Insights`) để cross-pollinate principles từ ≥2 trụ.
- Synthesis không thể dựa vào subagent summary đơn thuần — quá mỏng, không đủ actionable.
- Master framework structure 8 sections verified (overview table + ASCII diagram + N armed principles + content blueprint + customer journey + 90-day plan + don'ts + 1-line summary).

## Deliverables (paths verified)

- `wiki/concepts/research-sales-psychology-2026-07-07.md` — 35,844 bytes, 65 URLs
- `wiki/concepts/research-crowd-psychology-2026-07-07.md` — 23,542 bytes, 56 URLs
- `wiki/concepts/research-consumer-behavior-2026-07-07.md` — 27,117 bytes, 109 URLs
- `wiki/concepts/research-behavioral-science-2026-07-07.md` — 32,868 bytes, 89 URLs
- `wiki/concepts/sales-psychology-master-framework-2026-07-07.md` — 11,317 bytes (master framework synthesis)

## Source citation format verified working

- Format: `[N] Author. Title. Source. Date. URL.` ← end with period
- Total URLs counted by `grep "http"` = 319 (counted every http:// occurrence, including Twitter/X URLs from @AlexHormozi, @DanLokOfficial, @DonaldMiller, @SamOvens threads)
- Paraphrase discipline: <15 words/source — applied by all 4 subagents

## Anti-patterns avoided

1. ✅ Auto-skip scope confirm (anh đã rõ 4 trụ + 200+ + báo + X)
2. ✅ Dispatch 4 parallel thay vì tuần tự (save 6 phút)
3. ✅ Verify file size + URL count sau khi subagent complete (trước khi synthesis)
4. ✅ Read 4 files thật để extract top insights (không dùng subagent summary đơn thuần)
5. ✅ Embed master framework trong reply Telegram (không chỉ save file)

## Cross-references

- Bước 1 (Scope auto-skip) — update mới 2026-07-07
- Bước 2 (4-subagent batch OK khi độc lập) — update mới 2026-07-07
- Bước 4.5 (Master Framework Synthesis) — NEW 2026-07-07
- Pitfall #10 (no poll) — verified lần 2, 2026-07-07
- Pitfall #12 (master framework synthesis cross-pollination) — NEW 2026-07-07