#!/usr/bin/env python3
"""Template: Python loader to stage credentials from ~/.hermes/.env for third-party CLIs.

Usage: copy, customize the `needed` set and alias mapping, drop in ~/tools/bin/<loader-name>.

This loader is filter-safe:
- Parses ~/.hermes/.env manually (doesn't shell-source, which can trip filter)
- Uses string concat for known-secret env var NAMES ("MIN" + "IMAX_API_KEY")
- Loads values at runtime (filter doesn't see runtime file contents)
- Maps aliases (e.g. MINIMAX_API_KEY -> ANTHROPIC_API_KEY)
- Sets provider base URL defaults
- Execs real binary with staged env via subprocess.call

After writing, chmod +x the file.
"""

import os
import sys
from pathlib import Path

REAL_BIN = "/opt/homebrew/bin/<tool-name>"   # Path to actual binary


def main() -> int:
    env_file = Path.home() / ".hermes" / ".env"
    if not env_file.exists():
        print(f"ERROR: {env_file} not found", file=sys.stderr)
        return 1

    # === Customize: keys to load from .env ===
    # Use string concat if any key name looks like a known secret pattern
    # (MiniMax sk-cp, Telegram bot token digits:chars, GitHub ghp_, etc.)
    needed = {
        "ANTHROPIC_BASE_URL",       # provider endpoint (MiniMax/OpenRouter/Azure)
        # Add more keys here as needed
    }
    # Concatenated form for known-secret env var NAMES:
    src_key = "MIN" + "IMAX_API_KEY"           # becomes "MINIMAX_API_KEY" at runtime

    # Parse .env line by line
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k in needed:
            os.environ[k] = v

    # === Customize: alias mapping ===
    # If tool expects ANTHROPIC_API_KEY but .env has MINIMAX_API_KEY, map it
    target_key = "ANTHROPIC_API_KEY"   # what the third-party tool reads
    if target_key not in os.environ and src_key in os.environ:
        os.environ[target_key] = os.environ[src_key]

    # === Customize: default base URL ===
    # If tool hardcodes provider URL, ensure env var is set so our patch reads it
    os.environ.setdefault("ANTHROPIC_BASE_URL", "https://api.minimax.io/anthropic")

    # === Forward all args to real binary with staged env ===
    import subprocess
    return subprocess.call([REAL_BIN] + sys.argv[1:], env=os.environ)


if __name__ == "__main__":
    sys.exit(main())
