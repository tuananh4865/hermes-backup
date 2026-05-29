# Hermes v0.15.0 Session Learnings

## Critical: Always use .venv

Hermes code uses Python 3.10+ syntax (`type | None` = PEP 604 union syntax). System Python 3.9 on this Mac will throw `TypeError: unsupported operand type(s) for |` on `tools/registry.py:182`.

**Every terminal session inspection must be prefixed with:**
```bash
cd ~/.hermes/hermes-agent && source .venv/bin/activate
```

## session_search returns JSON string, NOT dict

Common mistake: `result['sessions']` → `TypeError: string indices must be integers`

Must parse first:
```python
import json
data = json.loads(result)
# Then: data['results'], data['success'], etc.
```

Direct dict access fails silently or crashes depending on the mode.

## hermes bundles (PLURAL)

Every user will try `hermes bundle` first. It fails with `"invalid choice"`.
The correct command is `hermes bundles list`.

## websockets missing

`tools.browser_dialog_tool` fails with `ModuleNotFoundError: No module named 'websockets'`.
Not fatal for most users — only affects browser dialog feature. Can be installed with `pip install websockets` in .venv if needed.

## Python version check order

1. `.venv/bin/python` (3.12.11) — CORRECT for Hermes
2. `/usr/bin/python3` (3.9.6) — WRONG for Hermes internals
3. `python3` in PATH — could be either

Always verify with `python --version` inside activated venv before assuming behavior.
