# Python Debugging with debugpy Reference

Formerly a standalone skill. Content absorbed into `systematic-debugging`.

## Setup

```bash
pip install debugpy
```

## Launch Python with debugpy

```bash
# Listen for debugger connections
python -m debugpy --listen 5678 --wait-for-client -m my_module

# Launch and break immediately
python -m debugpy --listen localhost:5678 --wait-for-client
```

## VS Code Configuration

```json
{
  "name": "Python: Remote Debug",
  "type": "python",
  "request": "attach",
  "connect": { "host": "localhost", "port": 5678 },
  "justMyCode": false
}
```

## Key Commands

- `debugpy.listen()` in code to attach programmatically
- Set breakpoints: `debugpy.breakpoint()`
- Conditional breakpoints supported
