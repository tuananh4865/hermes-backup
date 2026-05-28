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
# Tất cả gateway processes (nhiều PID = bình thường nếu nhiều profile)
ps aux | grep -E "hermes.*gateway|gateway.*run" | grep -v grep

# Check launchd quản lý (PID 790 = content-director, PID 64965 = default — cả 2 PPID=1 = launchd managed)
launchctl list | grep hermes

# Kiểm tra process hierarchy (PPID=1 = launchd managed, OK)
ps -p <PID> -o pid,ppid,start,command

# Xem logs ( Telegram reconnect attempts auto-recover )
tail -20 ~/.hermes/logs/gateway.log
```

### Multiple Profiles = Multiple PIDs (BÌNH THƯỜNG)
Mỗi `--profile` chạy một process riêng:
| PID | Profile | Managed by |
|-----|---------|------------|
| 790 | content-director | launchd (PPID=1) |
| 64965 | default | launchd (PPID=1) |

→ Không phải conflict, không cần kill. Muốn kill profile cụ thể → `launchctl unload` plist tương ứng.

### Restart Gateway
```bash
~/.hermes/restart_gateway.sh
```

### Manual Start (nếu cần)
```bash
cd ~/.hermes && ./run_hermes_gateway.sh
```

## WARNING: Gateway Graceful Restart Does NOT Reload Python Modules

**Critical pitfall:** `hermes gateway restart` (via request protocol) is a **graceful restart** — it restarts the service but Python modules stay MEMORY-MAPPED. Old `.pyc` pycache files and previously-loaded module state persist.

**When this matters:**
- After patching `kanban_db.py` or other core modules
- After clearing `__pycache__`
- When workers still fail despite code fixes

**Symptom:** Worker continues failing with the same error even after multiple `hermes gateway restart` calls. Gateway logs show the new code isn't being picked up.

**Fix: Hard kill + start fresh**
```bash
# 1. Find gateway PIDs
ps aux | grep "hermes_cli.main gateway" | grep -v grep

# 2. Kill hard (not graceful restart)
kill -9 <pid>  # -9 = SIGKILL, forces process death

# 3. Wait a moment
sleep 2

# 4. Restart via run_hermes_gateway.sh
cd ~/.hermes && ./run_hermes_gateway.sh
```

**When to use hard kill vs graceful restart:**
| Scenario | Method |
|----------|--------|
| Config change only | graceful restart OK |
| Code/patch change | Hard kill required |
| Worker still crashing after graceful restart | Hard kill required |
| Pycache suspected | Hard kill required |

### Debugging Worker Issues After Patch

When workers fail with `Unknown skill(s): kanban-worker` or similar errors after patching code:

```bash
# 1. Verify patch is in the file
grep -n "_kanban_worker_skill_available" ~/.hermes/hermes-agent/hermes_cli/kanban_db.py

# 2. Verify skill exists at expected path
find ~/.hermes/profiles/<profile>/skills -name "kanban-worker" -type f

# 3. Clear pycache in the hermes-agent venv
find ~/.hermes/hermes-agent/hermes_cli -name "__pycache__" -exec rm -rf {} +

# 4. Hard kill the gateway (NOT graceful restart)
ps aux | grep "hermes_cli.main gateway" | grep -v grep
kill -9 <pid>

# 5. Restart
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

### Tailscale Serve — Remote Access to Dashboard

Use `tailscale serve` to expose the Hermes Dashboard to other Tailscale devices (iPad, iPhone, other machines on your tailnet):

```bash
# Start dashboard on all interfaces (required for Tailscale to proxy)
hermes dashboard --host 0.0.0.0 --port 9119 --insecure --no-open &

# Expose via Tailscale — USE HTTP PROTOCOL, NOT https+insecure
# Using https+insecure causes 502 errors (TLS mismatch with uvicorn)
tailscale serve --bg http://localhost:9119

# Verify
curl https://tuananhs-mac-mini.taila86c48.ts.net/
```

**Result:** `https://<hostname>.taila86c48.ts.net/` — accessible from any device logged into your Tailscale.

**Common failure:** `https+insecure://` protocol causes 502 from Tailscale edge even though local curl works. Always use `http://` for plain HTTP backends.
