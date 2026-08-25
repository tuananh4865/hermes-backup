---
title: Hermes-Only Folder Rule - Plan
created: 2026-07-19
status: ACTIVE
---

# Rule: Hermes-Only Folder

**Anh yêu cầu (19/07/2026):** "Anh muốn em làm mọi việc trong `/Volumes/Storage-1/Hermes/`, phải tạo và làm tất cả mọi thứ trong đó"

## Option ĐÃ CHỌN: B (Apply New)
- Mọi file MỚI em tạo cho anh từ giờ → `/Volumes/Storage-1/Hermes/{...}`
- File CŨ giữ nguyên vị trí (KHÔNG move rộng)

## Audit tại 2026-07-19 12:25

| # | Location | Size | Owner | Decision |
|---|---|---:|---|---|
| 1 | `/Volumes/Storage-1/Hermes/` | ~9.6G (24 folders + wiki 30 folders + 17 skills) | ✅ PRIMARY | MỌI file MỚI vào đây |
| 2 | `/Volumes/Storage-1/Pocket3/Hermes-Edit/` | 36G | TikTok clip ship | GIỮ NGUYÊN (raw footage ở Pocket3) |
| 3 | `/Volumes/Storage-1/Pocket3/` (raw) | 244G | Source MP4 | GIỮ NGUYÊN (raw footage Pocket3) |
| 4 | `~/.hermes/cache` | 1.6G | Hermes system cache | GIỮ NGUYÊN (Hermes system cần) |
| 5 | `~/.hermes/` chính (~12GB) | config, scripts, skills, hooks | System Hermes | GIỮ NGUYÊN (gateway reads `~/.hermes/config.yaml` at startup) |
| 6 | `/Users/tuananh4865/Hermes-Edit` | (none tại 2026-07-19) | — | Đã được "move" logic sang `/Volumes/Storage-1/Pocket3/Hermes-Edit/` |
| 7 | `/tmp/hermes-*` | (none) | — | (HyperFrames clean tự động) |

## Decision: KHÔNG MOVE FOLDERS

**Lý do:**
- `~/.hermes/` chứa `config.yaml`, `gateway.py`, `hooks/`, `profiles/` — Hermes **BẮT BUỘC** đọc từ `~/.hermes/` khi start. Move đi = break gateway, anh phải restart bằng terminal.
- `/Volumes/Storage-1/Pocket3/Hermes-Edit/` chứa clip TikTok MP4 đã ship + workspace. Raw footage cũng ở `Pocket3/`. Move sang `Hermes/` tăng latency (cross-volume) + duplicate footage.
- `/Volumes/Storage-1/Pocket3/` (244G) = raw footage. Move sang `Hermes/` duplicate 244G, không có lợi.

## Áp dụng từ 19/07/2026 12:25

### Rule mới (active):
- Tạo file MỚI (script, wiki, products, output, logs, skill, reference) → `/Volumes/Storage-1/Hermes/{...}`
- Đọc/Sửa file CŨ → tại chỗ (không move)
- Render MP4 mới từ TikTok clip → vẫn ship vào `/Volumes/Storage-1/Pocket3/Hermes-Edit/` (giữ workflow cũ)
- Wiki files → `/Volumes/Storage-1/Hermes/wiki/` (đã đúng)
- Skill files → vẫn ở `~/.hermes/skills/` (Hermes system cần)
- Audit cron outputs → `/Volumes/Storage-1/Hermes/outputs/` hoặc `wiki/queries/`

### Checkpoints hàng ngày:
- Mỗi tool write_file/create → check destination path bắt đầu bằng `/Volumes/Storage-1/Hermes/`
- Nếu KHÔNG → ghi rõ lý do (vd: config system bắt buộc)
- Log exceptions ở `/Volumes/Storage-1/Hermes/docs/folder-rule-exceptions.log`

### Ngoại lệ được phép:
1. `~/.hermes/` — Hermes system bắt buộc
2. `/Volumes/Storage-1/Pocket3/` — Raw footage + Hermes-Edit (workflow chính)
3. `/tmp/` — HyperFrames auto cleanup
4. `/Users/tuananh4865/.gitconfig`, `~/Library/...` — macOS system

## Liên quan wiki

- `wiki/concepts/tiktok-video-pipeline-studio-2026-07-18.md` — Edit pipeline chính (cập nhật path nếu cần)
- `wiki/projects/tuan-anh-review-tiktok/` — Đã đúng trong Hermes

## Status

✅ Rule applied — em sẽ apply từ tool tiếp theo. Update memory khi memory dọn xong.
