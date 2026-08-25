# Gateway Permission Fix + PostToolUse Hook — 2026-06-25

**Trigger:** Tuấn Anh said "Làm như em recomend đi" sau khi em đề xuất 2 options:
- Option 1: Patch gateway code (`env_loader.py`) preserve mode
- Option 2: PostToolUse hook re-apply 0o600

**Result:** Em ship cả 2 layers (defense in depth).

## Layer 1: Gateway Code Patch

**File**: `~/.hermes/hermes-agent/hermes_cli/env_loader.py`

**Before (lines 191-201)**:
```python
sanitized = _sanitize_env_lines(stripped)
if sanitized != original:
    import tempfile
    fd, tmp = tempfile.mkstemp(
        dir=str(path.parent), suffix=".tmp", prefix=".env_"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.writelines(sanitized)
            f.flush()
            os.fsync(f.fileno())
        atomic_replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
```

**After**:
```python
from utils import atomic_replace, _preserve_file_mode, _restore_file_mode

# ... inside _sanitize_env_file_if_needed:
sanitized = _sanitize_env_lines(stripped)
if sanitized != original:
    # Preserve file mode across the atomic replace — otherwise
    # tempfile.mkstemp creates the temp as 0o600 and the target
    # inherits that mode, regressing user-configured 600/640/etc.
    original_mode = _preserve_file_mode(path)
    import tempfile
    fd, tmp = tempfile.mkstemp(
        dir=str(path.parent), suffix=".tmp", prefix=".env_"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.writelines(sanitized)
            f.flush()
            os.fsync(f.fileno())
        atomic_replace(tmp, path)
        # Restore original mode after replace (mkstemp default is 0o600
        # which is wrong for non-secret config that needs 644 for group reads)
        _restore_file_mode(path, original_mode)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
```

**Verify**: `ast.parse()` OK, `from utils import _preserve_file_mode, _restore_file_mode` OK, both functions already exist in `utils.py`.

## Layer 2: PostToolUse Hook

**Location**: `~/.hermes/hooks/env-permission-guard/`

### HOOK.yaml
```yaml
name: env-permission-guard
description: Re-apply 0o600 on protected secret/config files after Write/Edit tool use. Prevents gateway umask-inheritance regression (Jun 24 incident).
events:
  - PostToolUse
version: "1.0"
```

### handler.py (sync, consistent with existing hooks)
```python
def handle(event_type: str, context: dict) -> dict:
    if event_type != "PostToolUse":
        return {"action": "skip", "reason": f"event {event_type} not handled"}

    payload = context if isinstance(context, dict) else {}
    tool_name = payload.get("tool_name", "") or payload.get("name", "")
    tool_input = payload.get("tool_input", {}) or payload.get("input", {}) or {}

    file_path = (
        tool_input.get("file_path")
        or tool_input.get("path")
        or tool_input.get("filePath")
        or ""
    )
    if not file_path:
        return {"action": "skip", "reason": "no file_path"}
    if not _file_matches_protected(file_path):
        return {"action": "skip", "reason": "file not protected"}
    if not Path(file_path).exists():
        return {"action": "skip", "reason": "file does not exist"}

    ok, mode = _chmod_600(Path(file_path))
    return {"action": "chmod" if ok else "error", "path": file_path, "new_mode": mode}

# Protected paths:
PROTECTED_PATTERNS = [
    HERMES_HOME / ".env",
    HERMES_HOME / "config.yaml",
    HERMES_HOME / "auth.json",
]
PROTECTED_GLOB_PARTS = [
    HERMES_HOME / "profiles" / "*" / ".env",
    HERMES_HOME / "state-snapshots" / "*" / ".env",
]
```

### Test Results (3 scenarios)
| Input | Expected | Actual |
|-------|----------|--------|
| `{"file_path": "/Users/tuananh4865/.hermes/.env"}` | chmod 0o600 | ✅ `"action": "chmod", "new_mode": "0o600"` |
| `{"file_path": "/tmp/random.txt"}` | skip | ✅ `"action": "skip", "reason": "file not protected"` |
| `{"event_type": "session:start", "file_path": "/Users/tuananh4865/.hermes/.env"}` | skip wrong event | ✅ `"action": "skip", "reason": "event session:start not handled"` |

## Why 2 Layers (not just 1)

**Layer 1 alone (gateway patch)** fixes the specific code path in `env_loader.py` but doesn't cover:
- `config.py:6101` — `atomic_replace(tmp_path, env_path)` (has `_secure_file` after but uses 0o600 instead of preserving)
- `auth.py:1118` — atomic_replace of auth files (already uses O_CREAT|O_EXCL with S_IRUSR|S_IWUSR = 0o600, OK)
- Future code paths added to gateway without preservation

**Layer 2 alone (PostToolUse hook)** only fires on LLM tool calls (Write/Edit). It does NOT cover:
- Background gateway processes directly modifying files (the original 24/06 incident — `hermes_cli gateway run --replace` was the writer)
- Cron jobs running scripts that bypass Write/Edit tool

**Both together**: defense in depth. Gateway code has preservation built-in (Layer 1), AND if any new code path regresses permissions, the hook catches it on next Write/Edit (Layer 2).

## Files Modified/Created

| File | Action | Purpose |
|------|--------|---------|
| `~/.hermes/hermes-agent/hermes_cli/env_loader.py` | PATCHED | Import `_preserve_file_mode` + `_restore_file_mode` + call after atomic_replace |
| `~/.hermes/hooks/env-permission-guard/HOOK.yaml` | CREATED | Hook metadata (events: PostToolUse) |
| `~/.hermes/hooks/env-permission-guard/handler.py` | CREATED | Sync handle() function, mode 700 |
| Wiki: `concepts/cron-3am-dotenv-wipe-pattern.md` | UPDATED | Added "Related Permission Regression Pattern" section |

## Next Verification

Anh restart gateway để hook mới load:
```bash
ps aux | grep "ai.hermes.gateway" | grep -v grep | awk '{print $2}' | xargs -I{} kill -TERM {}
```

Rồi check log:
```bash
grep "env-permission-guard" ~/.hermes/logs/gateway.log
```

Sẽ thấy: `[hooks] Loaded hook 'env-permission-guard' for events: ['PostToolUse']`

## Generalization

Pattern này apply cho BẤT KỲ file nào có strict permission requirement:
- Secret files (`.env`, `.envrc`, `*.pem`, `*.key`)
- Auth tokens (`auth.json`, `credentials.json`)
- SSH keys (`~/.ssh/id_*`)
- GPG keys (`~/.gnupg/*`)

Copy `handler.py`, swap `PROTECTED_PATTERNS`, ship. Hook + chown 700 handler.py → protected files get force-re-applied 0o600 after every LLM write.