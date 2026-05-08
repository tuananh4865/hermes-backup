---
name: gateway-manager
description: Manage Hermes Gateway lifecycle - restart, check status, troubleshoot
---

# Gateway Manager Skill

## Gateway Architecture trên macOS

Gateway chạy qua **2 lớp auto-restart**:

```
launchd (plist) → run_hermes_gateway.sh (while-true loop) → hermes gateway
```

### Layer 1: launchd plist
- **File**: `~/Library/LaunchAgents/ai.hermes.gateway.plist`
- **Auto-start**: khi macOS khởi động (RunAtLoad: true)
- **Restart**: nếu script crash (KeepAlive: SuccessfulExit: false)

### Layer 2: run_hermes_gateway.sh
- **Location**: `~/.hermes/run_hermes_gateway.sh`
- **Logic**: while-true loop → restart gateway nếu crash
- **Restart delay**: 5 giây

## Commands

### Check Gateway Status
```bash
# Tất cả gateway processes
ps aux | grep -E "hermes.*gateway|gateway.*run" | grep -v grep

# Kiểm tra process hierarchy (PPID=1 = launchd managed)
ps -p <PID> -o pid,ppid,start,command

# Xem logs
tail -20 ~/.hermes/logs/gateway.log
```

### Restart Gateway
```bash
~/.hermes/restart_gateway.sh
```

### Manual Start (nếu cần)
```bash
cd ~/.hermes && ./run_hermes_gateway.sh
```

## Troubleshooting

### Lỗi "Could not find service ai.hermes.gateway"
- Đây là lỗi systemd - BỎ QUA trên macOS
- Gateway chạy standalone, không dùng systemd

### Gateway không respond
```bash
pkill -f "hermes_cli.main gateway"
sleep 2
cd ~/.hermes && ./run_hermes_gateway.sh
```

### Tắt HOÀN TOÀN một agent gateway (không auto-restart)
Khi cần tắt hẳn một agent (vd: research agent gây trouble), `pkill` thường không đủ vì process tự restart. Cần kill cả parent shell:

```bash
# Tìm tất cả process liên quan
ps aux | grep -i "research-lead" | grep -v grep

# Kill -9 cả child VÀ parent shell (2 PID)
kill -9 <child_pid> <parent_shell_pid>

# Verify đã tắt hẳn
ps aux | grep -i "research-lead" | grep -v grep
```

Lý do: parent shell (`/bin/bash -lic ...`) sẽ restart child ngay lập tức nếu chỉ kill child.

### Duplicate Gateway Conflict
Nếu thấy 2+ gateway processes cùng chạy (conflict Telegram bot token):
1. Kiểm tra process hierarchy: `ps -p <PID> -o pid,ppid`
2. Nếu PPID=1 → được quản lý bởi launchd
3. Kill process thủ công hoặc unload plist:
   ```bash
   launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway.plist
   ```

### Check launchd Status
```bash
launchctl list | grep hermes
```

## YOLO Mode
- Config: `approvals.mode: off` trong config.yaml
- Env: `HERMES_YOLO_MODE=true` trong .env
- Toggle: `/yolo` trong chat
