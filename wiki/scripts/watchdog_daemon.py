#!/opt/homebrew/bin/python3.14
"""
Wiki Watchdog Daemon
- Polls wiki directory for changes (macOS FSEvents compatible)
- Triggers Hermes agent via subprocess when changes detected
- Debounces to avoid spam on bulk file operations
- Logs all activity to watchdog.log

Usage:
  python3 watchdog_daemon.py              # foreground (debug)
  python3 watchdog_daemon.py --daemon     # background (production)
  ./start_watchdog.sh                      # use helper script
"""

import os
import sys
import time
import subprocess
import json
import hashlib
from pathlib import Path
from datetime import datetime

WIKI_DIR = Path("/Volumes/Storage-1/Hermes/wiki")
LOG_FILE = WIKI_DIR / "scripts" / "watchdog.log"
PID_FILE = WIKI_DIR / "scripts" / "watchdog.pid"
EVENT_FILE = WIKI_DIR / "scripts" / "watchdog_event.json"
POLL_INTERVAL = 5  # seconds
DEBOUNCE_SECONDS = 10

SKIP_PATTERNS = {
    ".git/", ".obsidian/", "__pycache__/", ".DS_Store",
    "watchdog.log", "watchdog.pid", "watchdog_event.json",
    "watchdog.pending", "watchdog.out", ".lock", ".pyc"
}

SKIP_EXTENSIONS = {".pyc", ".png", ".jpg", ".lock", ".pdf"}


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def is_watched_file(path: Path) -> bool:
    path_str = str(path)
    for pattern in SKIP_PATTERNS:
        if pattern in path_str:
            return False
    if path.suffix in SKIP_EXTENSIONS:
        return False
    if path.name.startswith("."):
        return False
    return True


def get_file_hash(path: Path) -> str:
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    except Exception:
        return "error"


def scan_directory():
    """Scan wiki directory and return changed files."""
    changes = []
    try:
        for root, dirs, files in os.walk(WIKI_DIR):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for filename in files:
                filepath = Path(root) / filename
                if is_watched_file(filepath):
                    changes.append({
                        "path": str(filepath.relative_to(WIKI_DIR)),
                        "hash": get_file_hash(filepath),
                        "modified": os.path.getmtime(filepath)
                    })
    except Exception as e:
        log(f"scan_directory error: {e}")
    return changes


def trigger_agent(changes: list):
    """Trigger Hermes agent with file change info."""
    log(f"TRIGGER: {len(changes)} file(s) changed — invoking agent")

    try:
        # Write event file for the agent to read
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "files": [c["path"] for c in changes],
            "count": len(changes)
        }
        with open(EVENT_FILE, "w") as f:
            json.dump(event_data, f, indent=2)

        # Trigger via hermes cron tick
        result = subprocess.run(
            ["hermes", "cron", "tick"],
            capture_output=True, text=True, timeout=60,
            cwd=str(WIKI_DIR)
        )
        log(f"Cron tick triggered: exit={result.returncode}")
        if result.returncode != 0 and result.stderr:
            log(f"cron stderr: {result.stderr[:200]}")

    except FileNotFoundError:
        log("hermes CLI not found in PATH")
    except subprocess.TimeoutExpired:
        log("Cron tick timed out")
    except Exception as e:
        log(f"ERROR triggering agent: {e}")


def is_already_running():
    """Check if daemon is already running."""
    if not PID_FILE.exists():
        return False
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)
        return True
    except (ValueError, ProcessLookupError, PermissionError):
        try:
            PID_FILE.unlink()
        except Exception:
            pass
        return False


def write_pid():
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))


def main():
    args = sys.argv[1:]
    daemon_mode = "--daemon" in args

    if is_already_running():
        log("WATCHDOG already running — exiting")
        sys.exit(0)

    if daemon_mode:
        log("WATCHDOG DAEMON STARTED")
        write_pid()

    # Initial scan — populate hash map without triggering
    initial_files = scan_directory()
    last_hashes = {f["path"]: f["hash"] for f in initial_files}
    log(f"Initial scan complete: {len(last_hashes)} files indexed")

    log(f"Wiki Watchdog running — polling every {POLL_INTERVAL}s")
    log(f"Watching: {WIKI_DIR}")

    last_trigger_time = 0
    last_hashes = {}

    while True:
        try:
            current_files = scan_directory()
            current_hashes = {f["path"]: f["hash"] for f in current_files}

            changed = []
            for path, hash_val in current_hashes.items():
                if path not in last_hashes or last_hashes[path] != hash_val:
                    f = next((f for f in current_files if f["path"] == path), None)
                    if f:
                        changed.append(f)

            if changed:
                now = time.time()
                if now - last_trigger_time > DEBOUNCE_SECONDS:
                    trigger_agent(changed)
                    last_trigger_time = now
                    log(f"Changes detected and agent triggered: {[c['path'] for c in changed]}")
                else:
                    log(f"Changes debounced: {[c['path'] for c in changed]}")

            last_hashes = current_hashes
            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            log("WATCHDOG STOPPED")
            if PID_FILE.exists():
                try:
                    PID_FILE.unlink()
                except Exception:
                    pass
            break
        except Exception as e:
            log(f"ERROR: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
