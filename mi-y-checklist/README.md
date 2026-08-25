# 🍝 Mì Ý Yum Yum Checklist

> Web app cho Tuấn Anh quản lý tiến lý mở tiệm mì Ý online tại Kon Tum.
> Mỗi tick trên web được sync realtime về Obsidian vault qua local API + Tailscale Funnel.

## Kiến trúc

```
[Vercel Frontend] → rewrite /api/local/* → [Tailscale Funnel HTTPS] → [Local FastAPI :7891] → [/Volumes/Storage-1/Hermes/wiki/projects/mi-y-kontum-research/checklist.md]
```

## File structure

- `backend/main.py` — FastAPI app (CRUD checklist, ghi file Obsidian)
- `backend/launchd/*.plist` — macOS auto-start
- `frontend/app/page.tsx` — UI checklist
- `frontend/next.config.js` — rewrite rule `/api/local/*` → local API
- `docs/launch.md` — hướng dẫn cho Tuấn Anh

## Quick start (development)

### Backend

```bash
cd backend
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python main.py
# → http://127.0.0.1:7891
```

### Tailscale Funnel

```bash
tailscale funnel --bg 7891
# → https://tuananhs-mac-mini.taila86c48.ts.net
```

### Frontend (Vercel)

```bash
cd frontend
npm install
npx next dev -p 3000
# → http://127.0.0.1:3000
```

Deploy Vercel: connect this repo, framework auto-detect = Next.js, no env vars needed.

## API endpoints

| Method | Path | Body | Effect |
|---|---|---|---|
| GET | /healthz | — | liveness |
| GET | /api/projects | — | list project slugs |
| GET | /api/projects/{slug} | — | full checklist parsed |
| PUT | /api/projects/{slug}/tasks/{id} | `{done: bool}` | toggle one task |
| POST | /api/projects/{slug}/tasks | `{phase, text, done?}` | add task |
| DELETE | /api/projects/{slug}/tasks/{id} | — | remove task |
| POST | /api/projects/{slug}/notes | `{phase, text}` | append note |

## Checklist file format

```markdown
---
title: "..."
project: mi-y-kontum-research
last_modified: 2026-08-01 09:45:00
---

# Đồng bộ từ web

## Phase 0: Setup

- [ ] Đăng ký hộ kinh doanh `id:p0_1`
- [x] Tập huấn ATTP `id:p0_2`
```

`id:` marker trên mỗi task cho phép frontend edit task cụ thể mà không cần index.

## License

MIT
