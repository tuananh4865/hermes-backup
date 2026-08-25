#!/usr/bin/env python3
"""
Hermes Browser Control — Python wrapper (Phase 6.5: WebSocket)

Connects to the native host WebSocket server on ws://localhost:9876.
Native host (Node.js) forwards commands to Chrome extension Service Worker,
which executes chrome.tabs.* / chrome.scripting.* APIs.

Architecture:
  Hermes Agent (bash tool)
    ↓ python3 scripts/browser.py navigate <url>
    ↓
  This wrapper (Python)
    ↓ WebSocket ws://127.0.0.1:9876
    ↓
  native-host/hermes_browser_host.js (Node.js WebSocket server)
    ↓ chrome.runtime.connectNative (one-way: extension → native)
    ↓
  Extension Service Worker (executes chrome.* APIs)
    ↓ response back via same port
    ↓
  Node.js WebSocket → Python wrapper

Usage:
  python3 browser.py navigate <url>
  python3 browser.py read-page
  python3 browser.py get-text
  python3 browser.py tab-list
  python3 browser.py tab-new [url]
  python3 browser.py tab-close [tab_id]
  python3 browser.py status
  python3 browser.py ping

Examples:
  python3 browser.py navigate https://google.com
  python3 browser.py read-page
  python3 browser.py tab-new https://github.com
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

# === CONFIG ===
WS_HOST = "127.0.0.1"
WS_PORT = 9876
WS_URI = f"ws://{WS_HOST}:{WS_PORT}"

# Native host binary path (for starting the WS server if not running)
HOST_DIR = Path(__file__).parent.parent / "native-host"
NODE_BIN = Path(os.path.expanduser("~/.hermes/node/bin/node"))
HOST_SCRIPT = HOST_DIR / "hermes_browser_host.js"

WS_REQUEST_TIMEOUT = 15  # seconds


def ensure_native_host_running():
    """Start the native host WS server if not already running.

    The native host is started via chrome.runtime.connectNative from the extension
    Service Worker on startup. If it's not running (e.g., extension not loaded),
    we launch it directly as a Node.js process for testing.
    """
    # Check if WS server is already responsive
    try:
        import socket
        with socket.create_connection((WS_HOST, WS_PORT), timeout=1):
            return  # Already running
    except (socket.error, ConnectionRefusedError):
        pass

    # Not running — launch it manually (only for testing without Chrome)
    if not HOST_SCRIPT.exists():
        print(f"❌ Native host script not found: {HOST_SCRIPT}", file=sys.stderr)
        print("   Run install.sh first, or load the extension in Chrome.", file=sys.stderr)
        sys.exit(1)

    if not NODE_BIN.exists():
        print(f"❌ Node.js not found: {NODE_BIN}", file=sys.stderr)
        sys.exit(1)

    # Launch in background
    print(f"🚀 Starting native host WS server: {HOST_SCRIPT.name}", file=sys.stderr)
    proc = subprocess.Popen(
        [str(NODE_BIN), str(HOST_SCRIPT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Wait for WS to come up
    import time
    for _ in range(30):
        time.sleep(0.3)
        try:
            with socket.create_connection((WS_HOST, WS_PORT), timeout=1):
                print(f"✅ Native host WS server up on ws://{WS_URI}", file=sys.stderr)
                return
        except (socket.error, ConnectionRefusedError):
            continue
    print(f"❌ Native host failed to start WS server on port {WS_PORT}", file=sys.stderr)
    sys.exit(1)


async def ws_call(tool: str, params: dict | None = None, timeout: int = WS_REQUEST_TIMEOUT):
    """Send a JSON-RPC request to the native host via WebSocket and return the result."""
    try:
        import websockets
    except ImportError:
        print("❌ websockets module not installed. Run: pip install websockets", file=sys.stderr)
        sys.exit(1)

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool, "arguments": params or {}},
    }

    async with websockets.connect(WS_URI, open_timeout=5) as ws:
        await ws.send(json.dumps(request))
        try:
            raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
        except asyncio.TimeoutError:
            raise RuntimeError(f"Native host timeout after {timeout}s")

    response = json.loads(raw)
    if "error" in response:
        raise RuntimeError(f"RPC error: {response['error']}")
    return response.get("result", response)


# === TOOL FUNCTIONS ===
def navigate(url: str, tab_id: int | None = None):
    return asyncio.run(ws_call("navigate", {"url": url, "tabId": tab_id}))


def read_page():
    return asyncio.run(ws_call("read_page", {}))


def get_text():
    return asyncio.run(ws_call("get_page_text", {}))


def tabs_list():
    return asyncio.run(ws_call("tabs_context_mcp", {}))


def tab_new(url: str = "about:blank", active: bool = True):
    return asyncio.run(ws_call("tabs_create_mcp", {"url": url, "active": active}))


def tab_close(tab_id: int | None = None):
    return asyncio.run(ws_call("tabs_close_mcp", {"tabId": tab_id}))


def status():
    return asyncio.run(ws_call("status", {}))


def ping():
    return asyncio.run(ws_call("ping", {}))


# === CLI ===
TOOLS = {
    "navigate": navigate,
    "read-page": read_page,
    "get-text": get_text,
    "tabs-list": tabs_list,
    "tab-new": tab_new,
    "tab-close": tab_close,
    "status": status,
    "ping": ping,
}


def main():
    parser = argparse.ArgumentParser(
        description="Hermes Browser Control — control Chrome via WebSocket",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s navigate https://google.com
  %(prog)s read-page
  %(prog)s tab-new https://github.com
  %(prog)s tab-close 12345
  %(prog)s tabs-list
  %(prog)s ping
        """,
    )
    parser.add_argument("tool", choices=sorted(TOOLS.keys()), help="Tool to invoke")
    parser.add_argument("args", nargs="*", help="Tool arguments")

    args = parser.parse_args()

    # Auto-start native host if not running
    try:
        ensure_native_host_running()
    except Exception as e:
        print(f"❌ Could not start native host: {e}", file=sys.stderr)
        sys.exit(1)

    tool_fn = TOOLS[args.tool]

    if args.tool == "navigate":
        if not args.args:
            print("❌ navigate requires a URL", file=sys.stderr)
            sys.exit(1)
        result = tool_fn(args.args[0])
    elif args.tool == "tab-new":
        url = args.args[0] if args.args else "about:blank"
        result = tool_fn(url=url)
    elif args.tool == "tab-close":
        tab_id = int(args.args[0]) if args.args else None
        result = tool_fn(tab_id=tab_id)
    else:
        result = tool_fn()

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted", file=sys.stderr)
        sys.exit(130)
