"""Fable-5 Compliance Check Hook

Runs on session:start. Verifies all SOUL.md files have the 4 required Fable-5 patterns.
Warns (logs) if any file is missing patterns. NEVER blocks the main pipeline.

Tuấn Anh mandate: 4 patterns (MCP Connector, Persistent Storage, Skills-First,
Search Discipline) must be BẮT BUỘC applied to EVERY agent context (2026-06-16).
"""

import os
import sys
from pathlib import Path

HERMES_ROOT = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))

# Pattern names (case-insensitive grep)
PATTERNS = [
    "MCP CONNECTOR",
    "PERSISTENT STORAGE",
    "SKILLS-FIRST",
    "SEARCH DISCIPLINE",
]


def find_soul_files():
    """Find all SOUL.md files except docker templates."""
    soul_files = []
    for path in HERMES_ROOT.rglob("SOUL.md"):
        if "docker" not in str(path):
            soul_files.append(path)
    return soul_files


def check_file(soul_file: Path) -> list:
    """Return list of missing pattern names for a SOUL.md file."""
    try:
        content = soul_file.read_text(encoding="utf-8").upper()
    except Exception as e:
        return [f"READ_ERROR: {e}"]

    return [p for p in PATTERNS if p not in content]


def check_compliance() -> tuple:
    """Check all SOUL.md files. Returns (total_files, files_with_issues_list)."""
    soul_files = find_soul_files()
    if not soul_files:
        return (0, [])

    files_with_issues = []
    for sf in soul_files:
        missing = check_file(sf)
        if missing:
            files_with_issues.append((sf, missing))

    return (len(soul_files), files_with_issues)


def handle(event_type: str, context: dict) -> None:
    """
    Hook entry point. Called by gateway on session:start event.

    Context dict may contain:
      - session_id: str
      - platform: str
      - user_id: str
    """
    try:
        # Only run on session:start
        if event_type != "session:start":
            return

        total, files_with_issues = check_compliance()

        if files_with_issues:
            print(f"[fable5-check] ⚠️  {len(files_with_issues)}/{total} SOUL.md file(s) missing Fable-5 patterns:")
            for sf, missing in files_with_issues:
                print(f"  - {sf}")
                for m in missing:
                    print(f"      • {m}")
            print(f"[fable5-check] Fix with: bash {HERMES_ROOT}/scripts/add-fable5-to-soul.sh <file>")
            print(f"[fable5-check] Full report: bash {HERMES_ROOT}/scripts/check-fable5-compliance.sh")
        else:
            print(f"[fable5-check] ✅ All {total} SOUL.md files comply with Fable-5 mandate")

        # WARN ONLY — never raise (per AGENTS.md: hooks never block)
    except Exception as e:
        print(f"[fable5-check] Hook error (non-fatal): {e}", file=sys.stderr)


if __name__ == "__main__":
    # Allow standalone test
    handle("session:start", {})
    sys.exit(0)
