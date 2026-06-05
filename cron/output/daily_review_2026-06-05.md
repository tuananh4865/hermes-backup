# Daily Review — 2026-06-05

## Cron Jobs Summary

| Job | Time | Status | Messages |
|-----|------|--------|----------|
| Daily Session Review | 00:03 | ✅ | 50 |
| Autoresearch Nightly | 02:05 | ✅ | 66 |
| Wiki Memory Forget | 03:00 | ✅ (dry-run) | — |
| Daily Backup | 03:01 | ✅ | 10 |
| Wiki Health | 04:00 | ✅ SILENT | — |
| X Research Daily | 07:02 | ✅ | 35 |

**Backup Stats:** +3,881 / −110 lines, commit `8fee7223e`

---

## ✅ Hoàn thành

- **MiniMax-M3 verified** — Đang chạy đúng model với 1M context, 59% SWE-Bench
  - Config: `~/.hermes/config.yaml` → `model.default: MiniMax-M3`
  - API endpoint hoạt động (dù có 1004 error khi list models — không ảnh hưởng việc chat)
- **Storytelling lesson** — Dạy Anh cách làm content viral bằng storytelling
- **Wiki Memory Forget** — Dry-run: 83 stale topics, 51 referenced topics (14 days)
- **Autoresearch** — Research Knowledge Acquisition: SIA + GEA + security

---

## 🧠 Learnings

1. **MiniMax-M3 API 1004 error** — Endpoint tồn tại nhưng `MINIMAX_API_KEY` env var không expand đúng lúc query list. Model vẫn chạy OK, chỉ không hiện trong `hermes model --list`

2. **Storytelling = vũ khí sắc nhất cho viral content** — Khán giả nhớ được câu chuyện > fact

3. **Wiki stale = 83 topics** — Chỉ 51 topics được refer trong 14 days, còn lại có thể xóa

---

## ⚠️ Cần xử lý

- **Wiki Memory Forget** — Chạy `DELETE_MODE=true` để xóa 83 stale topics (hiện tại dry-run)
- **Autoresearch knowledge** — Cần commit findings từ 2026-06-05 research

---

## Session Details

### DM (20:46-20:48 UTC+7)
- Anh hỏi model đang xài → MiniMax-M3
- Anh không thấy M3 trong list → Explain config OK, chỉ list bị lỗi 1004

### Group (21:08-21:10 UTC+7)
- Anh hỏi cách tập storytelling → Hermes dạy bài về viral content qua story

---

**Report generated:** 2026-06-06 00:01 UTC+7