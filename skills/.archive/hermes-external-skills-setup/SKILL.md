---
title: Hermes External Skills Directory Setup
name: hermes-external-skills-setup
description: Cách thêm đường dẫn skills bên ngoài vào Hermes Agent qua config.yaml
category: hermes
tags: [hermes, skills, configuration]
created: 2026-04-27
updated: 2026-04-27
---

# Hermes External Skills Directory Setup

## Vấn đề

Mặc định `skill_manage(action='create')` tạo skills vào `~/.hermes/skills/`. Nếu muốn skills ở đường dẫn khác (VD: `/Volumes/Storage-1/Hermes/skills/`), có 2 cách:

### Cách 1: Symlink (CŨ - Phức tạp)
```bash
# Di chuyển skills sang đường dẫn mới
mv ~/.hermes/skills/hermes-autoresearch /Volumes/Storage-1/Hermes/skills/

# Xóa thư mục cũ và tạo symlink
rm -rf ~/.hermes/skills
ln -s /Volumes/Storage-1/Hermes/skills ~/.hermes/skills
```
**Nhược điểm:** Symlink chỉ 1 chiều, `skill_manage` vẫn không biết đường dẫn mới.

### Cách 2: external_dirs config (ĐÚNG - Khuyến nghị) ✅
Thêm vào `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - /Volumes/Storage-1/Hermes/skills
```

**Ưu điểm:**
- Hermes tự động scan cả local và external dirs
- Không cần symlink
- Dùng `skill_manage(action='create')` bình thường
- An toàn, không ảnh hưởng hệ thống

## Cách làm

### 1. Tạo thư mục skills ở đường dẫn mới
```bash
mkdir -p /Volumes/Storage-1/Hermes/skills
```

### 2. Thêm vào config.yaml
```yaml
skills:
  external_dirs:
    - /Volumes/Storage-1/Hermes/skills
  creation_nudge_interval: 5
```

### 3. Verify
```bash
hermes skills list
```

Skills ở cả 2 đường dẫn sẽ xuất hiện:
- `~/.hermes/skills/` (local)
- `/Volumes/Storage-1/Hermes/skills/` (external)

## Tạo skill mới sau khi config

Dùng `skill_manage(action='create')` bình thường — skill sẽ được tạo ở `~/.hermes/skills/`. Sau đó có thể di chuyển sang external directory nếu cần.

## Lưu ý

- `external_dirs` hỗ trợ nhiều đường dẫn
- Đường dẫn có thể dùng `~` hoặc environment variables  
- Duplicate paths được tự động skip
- Local skills (`~/.hermes/skills/`) không bị ảnh hưởng bởi external_dirs config
