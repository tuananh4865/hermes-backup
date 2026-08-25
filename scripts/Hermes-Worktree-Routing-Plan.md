# Hermes Worktree Routing Plan — 10/07/2026

## Vấn đề (anh flag)

Hermes hiện đang leak file ra nhiều nơi ngoài `/Volumes/Storage-1/Hermes/`:

| Nơi leak | Loại file | Dung lượng | Tại sao sai |
|---|---|---:|---|
| `~/Movies/badminton-highlights/` | Video MP4 (highlight edit) | 23M | Edit video worktree của anh, em chỉ render vào đây theo quán cũ |
| `~/Downloads/` | Video MP4, PDF, MP3, ảnh | 290M | Telegram gửi file → em save vào đây |
| `~/.hermes/cache/` | Ảnh, audio, video, screenshots, delegation summary | 287M | Skill/config default path của Hermes runtime |
| `~/.hermes/cron/output/` | Cron job output files | ~50M | Cron default destination |
| `~/.hermes/cron/tiktok-monitor/videos/` | Video tiktok monitor | 62M | Watchdog cron save video |

**Anh muốn:** Mọi file lẻ (tạo file, tải file, screenshot, audio, video download, cron output) phải vào `/Volumes/Storage-1/Hermes/outputs/` — **NGOẠI TRỪ** project đã có worktree riêng.

## Worktree hiện có (kế thừa từ code cũ)

```
/Volumes/Storage-1/Hermes/
├── wiki/                 ← Knowledge base (articles, concepts, raw, projects)
├── projects/             ← Persistent project workspaces (cho project không cần video edit)
├── skills/               ← Hermes skills library (reusable skills)
├── scripts/              ← Helper scripts
├── secrets/              ← Encrypted credentials backup
├── archive/              ← Old data
├── cron/                 ← Cron config backups
├── memories/             ← Hermes memory state snapshots
├── Hop dong OPM716/      ← Single-project workspace (contract work)
├── dflash/, rowboat/, human-cli/, workers/  ← External git clones
└── temp_verify/          ← Verification scratchpad
```

**Worktree bị THIẾU:**
- `outputs/` — nơi em tạo file lẻ (ảnh, video download, audio, screenshots) — **CHƯA CÓ**
- `cron-output/` — nơi cron output — **CHƯA CÓ** (currently ở `~/.hermes/cron/output/`)
- `downloads/` — nơi em save file tải về — **CHƯA CÓ** (currently ở `~/Downloads/`)
- `tmp/` — scratchpad runtime — **CHƯA CÓ**

## Routing rules (anh đã chốt)

| Nơi | Loại worktree | Dùng cho |
|---|---|---|
| `/Volumes/Storage-1/Pocket3/Hermes-Edit/` | **WORKTREE EDIT VIDEO** (của anh) | Edit clip cầu lông, render TikTok, output video cuối |
| `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/` | **Worktree riêng project** (nội dung) | Content badminton — đã có |
| `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/` | **Worktree riêng project** (nội dung) | Content review lifestyle — đã có |
| `/Volumes/Storage-1/Hermes/outputs/` | **WORKTREE MẶC ĐỊNH** (mới) | Mọi file lẻ tẻ: download ảnh, download video, download audio, PDF, screenshots, transcript cache, etc. |

**Ngoại lệ (KHÔNG move):**
- `~/.hermes/.git/` — git history của Hermes runtime (không touch)
- `~/.hermes/hermes-agent/.venv/` — Python venv (đứng cố định)
- `~/.hermes/state.db`, `sessions/` — runtime DB + session storage (gateway đang mở)
- `~/.hermes/sandboxes/`, `lsp/`, `bin/` — runtime tooling

## Plan triển khai 4 phase

### Phase 1 — Tạo worktree `outputs/` chuẩn chỉnh (1 phút)

```bash
mkdir -p /Volumes/Storage-1/Hermes/outputs/{downloads,videos,images,audio,documents,screenshots,transcripts,cron-output,scratch}
```

Mỗi sub-folder có 1 README.md giải thích mục đích (cho agent khác đọc hiểu).

### Phase 2 — Cập nhật skill configs + hooks (5 phút)

**2a. Skill defaults:**
- Skill `tiktok-video-editor`: thay đường dẫn output mặc định sang `/Volumes/Storage-1/Hermes/outputs/videos/`
- Skill `video-download-yt-dlp`: thay `~/Downloads/` → `/Volumes/Storage-1/Hermes/outputs/downloads/`
- Skill `youtube-content-download`: cùng pattern
- Skill `gif-search`: thay `~/Downloads/` → `/Volumes/Storage-1/Hermes/outputs/videos/`
- Skill `telegram-video-analysis`: thay `~/.hermes/cache/videos/` → `/Volumes/Storage-1/Hermes/outputs/videos/`
- Skill `image_generate` defaults: thay sang `/Volumes/Storage-1/Hermes/outputs/images/`
- Skill `analyze-transcript`: thay sang `/Volumes/Storage-1/Hermes/outputs/transcripts/`

**2b. Hook pre-tool-call** (`~/.hermes/hooks/worktree-router/`):
- Tự động detect khi tool có path nằm ngoài `/Volumes/Storage-1/Hermes/` HOẶC `/Volumes/Storage-1/Pocket3/Hermes-Edit/` HOẶC `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-*/`
- Nếu file lẻ (không phải project worktree) → **WARN** agent: "File này sẽ rơi vào `~/` hoặc `~/.hermes/`. Anh muốn route vào `/Volumes/Storage-1/Hermes/outputs/<type>/` chứ?"
- User confirm → continue, hoặc skip với lý do (project đã có worktree).

### Phase 3 — Move/symlink data cũ (5 phút)

Không move file cũ (rủi ro break runtime). Tạo **alias file** ở `/Volumes/Storage-1/Hermes/outputs/` để anh biết nơi cũ:

```bash
# Tạo symlink-style manifest (không symlink thật để tránh confusion)
cat > /Volumes/Storage-1/Hermes/outputs/_legacy-paths.md <<EOF
# ⚠️ LEGACY PATHS — file cũ từ trước 2026-07-10 vẫn ở đây
# Mọi file MỚI phải save vào /Volumes/Storage-1/Hermes/outputs/<type>/

~/Downloads/                  (290M) — Telegram downloads, PDF, MP3 cũ
~/.hermes/cache/              (287M) — Ảnh, video, audio cache
~/.hermes/cron/output/        — Cron job outputs
~/.hermes/cron/tiktok-monitor/videos/ — TikTok monitor videos
~/Movies/badminton-highlights/ (23M) — Highlight edit renders cũ

# Khi nào clean up: sau khi chạy 30 ngày không có issue → em move batch vào đây
EOF
```

### Phase 4 — Verify + commit (2 phút)

```bash
# Verify
- ls /Volumes/Storage-1/Hermes/outputs/ có đủ 9 sub-folders
- Test 1 tool (write_file) vào outputs/transcripts/test.md → OK
- Test skill hook → trigger warn cho path ngoài worktree

# Commit
cd /Volumes/Storage-1/Hermes
git init  (nếu chưa) 
git add outputs/
git commit -m "feat(outputs): worktree mặc định cho file lẻ + routing rules"
```

## File cần tạo

| Path | Mục đích |
|---|---|
| `/Volumes/Storage-1/Hermes/outputs/README.md` | Overview routing rules |
| `/Volumes/Storage-1/Hermes/outputs/_legacy-paths.md` | Manifest file cũ |
| `/Volumes/Storage-1/Hermes/outputs/{downloads,videos,...}/README.md` | Mỗi sub-folder 1 README giải thích |
| `~/.hermes/hooks/worktree-router/handler.py` | Pre-tool-call router hook |
| `~/.hermes/hooks/worktree-router/HOOK.yaml` | Hook registration |
| Updated configs: skills mentioned ở 2a | Patch save paths |
| `/Volumes/Storage-1/Hermes/scripts/worktree-router-test.md` | Test suite |

## Rollback plan

Nếu hook fail:
1. `~/.hermes/config.yaml` patch rules → disable hook block
2. Không cần undo file di chuyển vì Phase 3 KHÔNG move file cũ

## Estimated total time

- Phase 1: 1 phút
- Phase 2: 5 phút (5-7 skill patches)
- Phase 3: 5 phút (chỉ viết manifest, không move data)
- Phase 4: 2 phút (verify + git init)

**Total: ~15 phút.**

---
*Plan created: 2026-07-10 — Tuấn Anh flag "mọi hoạt động Hermes đều phải lưu ở Volumes/Storage-1/Hermes"*
