# WikiMemoryProvider — Dual Location Bug (2026-05-08)

## Problem Summary

WikiMemoryProvider has **two source locations**, but only one is loaded by the memory plugin system. The stub (136 lines, non-functional hooks) was active instead of the full implementation (1458 lines, all hooks working).

## Dual Location Architecture

```
~/.hermes/plugins/
├── wiki/__init__.py          → 136 lines  ⚠️ STUB (active, wrong)
└── memory/wiki/__init__.py   → 1458 lines ✅ FULL (ignored, right)
```

The memory plugin loader in `plugins/memory/__init__.py` uses `find_provider_dir(name)`:

```python
def find_provider_dir(name: str) -> Optional[Path]:
    # Bundled
    bundled = _MEMORY_PLUGINS_DIR / name   # → plugins/memory/wiki/
    if bundled.is_dir() and (bundled / "__init__.py").exists():
        return bundled
    # User-installed
    user_dir = _get_user_plugins_dir()    # → ~/.hermes/plugins/wiki/
    user = user_dir / name
    if user.is_dir() and (user / "__init__.py").exists():
        return user
```

Wait — this checks `memory/wiki/` FIRST, then `~/.hermes/plugins/wiki/`. But in this case, `memory/wiki/` WAS the full implementation and `wiki/` was the stub. The stub was being loaded because of how `_load_provider_from_dir` resolves module paths.

Actually, looking more carefully at `_load_provider_from_dir`:

```python
_is_bundled = _MEMORY_PLUGINS_DIR in provider_dir.parents or provider_dir.parent == _MEMORY_PLUGINS_DIR
module_name = f"plugins.memory.{name}" if _is_bundled else f"_hermes_user_memory.{name}"
```

When loaded from `~/.hermes/plugins/wiki/` → module name = `_hermes_user_memory.wiki`.
When loaded from `plugins/memory/wiki/` → module name = `plugins.memory.wiki`.

Both paths are checked, but the **bundled path takes precedence on collision** IF the bundled path exists. The issue was actually:

- `~/.hermes/plugins/wiki/` existed (stub, 136 lines)
- `~/.hermes/plugins/memory/wiki/` also existed (full, 1458 lines)  
- Both point to `WikiMemoryProvider` class
- Python cached the first one loaded → stub was active

## Symptom

- All 3 hooks (`sync_turn`, `on_session_end`, `on_pre_compress`) appear to be implemented in code
- But **hooks never fire** — no checkpoints written, no memory extracted
- Gateway logs show no `sync_turn` calls for the wiki provider
- Only 1 `sync_turn` found in agent.log (from builtin provider, not wiki)

## How to Diagnose

```bash
# 1. Check which file is actually loaded
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / '.hermes' / 'hermes-agent'))
from plugins.memory import load_memory_provider
mp = load_memory_provider('wiki')
print(f'Module: {mp.__class__.__module__}')
print(f'File: {sys.modules[mp.__class__.__module__].__file__}')
"

# 2. Count lines in both locations
wc -l ~/.hermes/plugins/wiki/__init__.py
wc -l ~/.hermes/plugins/memory/wiki/__init__.py

# 3. Check if hooks are pass/stubs
grep -n "sync_turn\|on_session_end\|on_pre_compress" ~/.hermes/plugins/wiki/__init__.py
```

## The Fix

Replace the stub with the full implementation:

```bash
cp ~/.hermes/plugins/memory/wiki/__init__.py ~/.hermes/plugins/wiki/__init__.py
```

Then **restart the gateway** to reload the module:
```bash
hermes gateway restart
```

## Prevention

After any WikiMemoryProvider update, verify the correct file is loaded:

```bash
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / '.hermes' / 'hermes-agent'))
from plugins.memory import load_memory_provider
mp = load_memory_provider('wiki')
print(f'Lines: {len(open(sys.modules[mp.__class__.__module__].__file__).readlines())}')
mp.initialize(session_id='test', platform='cli')
print(f'Has _turn_count: {hasattr(mp, \"_turn_count\")}')
"
```

Expected: Lines > 1000, `_turn_count` exists.

## Related

- Full WikiMemoryProvider implementation: `~/.hermes/plugins/memory/wiki/__init__.py`
- Memory architecture: `references/memory-architecture.md`
- Bug fix 2026-05-06: `references/wikimemoryprovider-bugfix-2026-05-06.md`
