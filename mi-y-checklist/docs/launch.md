# Mì Ý Yum Yum Checklist Web App

> **Anh dùng ở:** Điện thoại (mở web) hoặc Mac (mở web + tick + Obsidian reload).

## 🎯 Cách hoạt động

```
[Anh tick trên web] → [Vercel] → [Tailscale Funnel] → [Local API port 7891] → [File checklist.md trong Obsidian vault]
                          ↑                                                                       ↓
                       [HTTPS từ internet]                                              [Obsidian reload tự động]
```

## ✅ Đã setup xong (verified ngày 2026-08-01)

| Component | Status | Đường dẫn / URL |
|---|---|---|
| Backend FastAPI | ✅ Running | `http://127.0.0.1:7891` |
| Tailscale Funnel | ✅ Live | `https://tuananhs-mac-mini.taila86c48.ts.net` |
| Frontend Vercel | 🔄 Đang build | URL sẽ có sau khi deploy (xem Telegram) |
| File checklist Obsidian | ✅ Created | `/Volumes/Storage-1/Hermes/wiki/projects/mi-y-kontum-research/checklist.md` |
| Auto-start launchd | ⏳ Cần enable | `/Volumes/Storage-1/Hermes/mi-y-checklist/backend/launchd/com.tuananh.miy-checklist-api.plist` |

## 🔄 Tự khởi động khi Mac bật

Em đã viết launchd plist. Anh chạy 1 lần để enable:

```bash
# Copy plist vào launchd directory
cp /Volumes/Storage-1/Hermes/mi-y-checklist/backend/launchd/com.tuananh.miy-checklist-api.plist ~/Library/LaunchAgents/

# Enable (auto-start khi login + tự restart nếu crash)
launchctl load ~/Library/LaunchAgents/com.tuananh.miy-checklist-api.plist

# Verify
launchctl list | grep miy-checklist
```

Sau khi enable, backend sẽ **tự chạy** mỗi khi anh bật Mac, kể cả không mở Terminal.

## 🛑 Dừng backend (nếu cần)

```bash
# Stop + remove auto-start
launchctl unload ~/Library/LaunchAgents/com.tuananh.miy-checklist-api.plist

# Or just kill process nếu đang chạy manual
pkill -f "mi-y-checklist/backend/main.py"
```

## 📁 File structure

```
/Volumes/Storage-1/Hermes/mi-y-checklist/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── requirements.txt
│   └── launchd/com.tuananh.miy-checklist-api.plist
└── frontend/
    ├── app/page.tsx         # UI checklist
    ├── app/layout.tsx
    ├── app/globals.css
    ├── next.config.js       # rewrite /api/local/* → local API
    ├── package.json
    └── tailwind.config.js

/Volumes/Storage-1/Hermes/wiki/projects/mi-y-kontum-research/
└── checklist.md             # ← file Obsidian sẽ thấy (đã có 30 tasks)
```

## 🧪 Test thủ công

```bash
# Health check
curl https://tuananhs-mac-mini.taila86c48.ts.net/healthz

# Get checklist
curl https://tuananhs-mac-mini.taila86c48.ts.net/api/projects/mi-y-kontum-research

# Toggle 1 task
curl -X PUT https://tuananhs-mac-mini.taila86c48.ts.net/api/projects/mi-y-kontum-research/tasks/p0_1 \
  -H "Content-Type: application/json" -d '{"done": true}'

# Verify file
grep "Đăng ký hộ kinh doanh" /Volumes/Storage-1/Hermes/wiki/projects/mi-y-kontum-research/checklist.md
```

## ⚠️ Giới hạn

- **Cần Mac bật + online** để backend hoạt động
- **Nếu Mac tắt** → web trên điện thoại sẽ báo lỗi "API unreachable"
- **Giải pháp nâng cao sau:** Git sync (web → GitHub → Mac pull cron 5 phút/lần) — sẽ làm nếu anh cần
