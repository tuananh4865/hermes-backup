---
title: Hermes Agent Maintenance
created: 2026-05-03
updated: 2026-05-03
type: concept
tags: [hermes, maintenance, git]
confidence: high
relationships: [hermes-agent]
---

# Hermes Agent Maintenance

## Git Remote Setup (CRITICAL)

**Standard setup after clone from NousResearch:**
```
origin   https://github.com/NousResearch/hermes-agent.git (fetch/push)  # Repo gốc - dùng để update
backup  https://github.com/<your-fork>.git (fetch/push)              # Repo của bạn - dùng để backup
```

**Lệnh setup:**
```bash
cd ~/.hermes/hermes-agent
git remote set-url origin https://github.com/NousResearch/hermes-agent.git
git remote add backup https://github.com/<your-fork>.git
git remote -v  # Verify
```

**Cách dùng:**
```bash
git pull origin main   # Update từ repo gốc NousResearch
git push backup main   # Backup lên repo của bạn
```

**Sai lầm phổ biến:** Nếu `origin` trỏ về fork của bạn thay vì repo gốc, `git pull` sẽ merge code của bạn lên chứ không phải update từ upstream.

## Browser Capabilities

Hermes có 2 browser stack riêng biệt:

### 1. Hermes Native Browser Tools (`browser_tool.py`)

| Tool | Mô tả |
|------|--------|
| `browser_navigate` | Điều hướng đến URL |
| `browser_snapshot` | Chụp accessibility tree |
| `browser_click` | Click element (ref ID) |
| `browser_type` | Nhập text |
| `browser_scroll` | Cuộn lên/xuống |
| `browser_back` | Quay lại trang trước |
| `browser_press` | Bấm phím |
| `browser_console` | Đọc console logs + run JS |
| `browser_get_images` | Lấy danh sách images |
| `browser_vision` | Screenshot + AI phân tích |

**Advanced:**
- `browser_cdp` - Raw DevTools Protocol passthrough
- `browser_dialog` - Handle JS dialogs (alert, confirm, prompt)

### 2. Vision Tool (`vision_tools.py`)

```python
vision_analyze_tool(image_url: str, user_prompt: str, model: str = None)
```

- Auto-detect vision provider: main provider → OpenRouter → Nous Portal
- Support URL và local file
- SSRF protection, 50MB file cap, auto cleanup
- Config: `auxiliary.vision.provider`, `auxiliary.vision.model`, `auxiliary.vision.timeout`

## So sánh với browser-harness

| Tính năng | Hermes Browser | browser-harness |
|------------|---------------|-----------------|
| Screenshots | Qua vision AI | Full screenshot files |
| Tabs | Không | Có |
| Uploads | Không | Có |
| Downloads | Không | Có |
| Drag-and-drop | Không | Có |
| Vision AI | Có (tích hợp) | Cần external |
| Cloud browser | Có (Browserbase, Firecrawl) | Không |

## Related
- [[hermes-agent]] - Full Hermes Agent guide
- [[learned-about-tuananh]] - Tuấn Anh preferences
