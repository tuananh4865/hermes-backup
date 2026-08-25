#!/usr/bin/env python3
"""
Hermes Log Helper v2 — Append-only JSONL changelog
Industry pattern: Stripe/CloudTrail audit log style.

Usage:
    # Log 1 edit
    python3 log_helper.py append /path/to/file.md --reason "Update hub.md"
    python3 log_helper.py append /path/to/file.md --reason "Create new skill" --action create

    # Query history
    python3 log_helper.py query                           # All today
    python3 log_helper.py query --file Hermes/wiki/foo.md  # Filter by file
    python3 log_helper.py query --date 2026-07-19          # Filter by date
    python3 log_helper.py query --last 5                  # Last 5 entries

Storage:
    /Volumes/Storage-1/Hermes/logs/daily/YYYY-MM-DD.jsonl
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ICT = timezone(timedelta(hours=7))
LOGS_DIR = Path("/Volumes/Storage-1/Hermes/logs")
DAILY_DIR = LOGS_DIR / "daily"

# Mirror roots — paths bắt đầu bằng root này → mirror bằng root.name + relative
MIRROR_ROOTS = [
    Path("/Volumes/Storage-1/Hermes"),
    Path("/Volumes/Storage-1/Pocket3"),
    Path("/Users/tuananh4865"),
]


def now_iso() -> str:
    return datetime.now(ICT).isoformat()


def today() -> str:
    return datetime.now(ICT).strftime("%Y-%m-%d")


def mirror(file_path: str) -> str:
    """Convert absolute path → mirror path (e.g., '/Volumes/Storage-1/Hermes/wiki/foo.md' → 'Hermes/wiki/foo.md')"""
    p = Path(file_path).resolve()
    for root in MIRROR_ROOTS:
        try:
            return f"{root.name}/{p.relative_to(root.resolve())}".replace("\\", "/")
        except ValueError:
            continue
    return str(p).replace("\\", "/")


def file_size(file_path: str) -> int:
    try:
        return Path(file_path).stat().st_size
    except OSError:
        return 0


def detect_action(file_path: str, action: str = None) -> str:
    """Auto-detect create / modify / delete based on file existence."""
    if action:
        return action
    return "create" if not Path(file_path).exists() else "modify"


def append_log(file_path: str, reason: str, action: str = None, before: int = None, after: int = None) -> str:
    """Append 1 JSONL entry to today's log file. Returns path to log file."""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    log_file = DAILY_DIR / f"{today()}.jsonl"

    entry = {
        "ts": now_iso(),
        "file": mirror(file_path),
        "action": detect_action(file_path, action),
        "reason": reason,
        "before": before if before is not None else file_size(file_path),
        "after": after if after is not None else file_size(file_path),
    }

    with open(log_file, "a", encoding="utf-8") as f:
        # Use compact JSON (no space after :) — NDJSON standard for grep-friendly
        f.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")

    return str(log_file)


def query_logs(file_filter: str = None, date: str = None, last: int = None) -> list:
    """Read JSONL entries, optionally filter."""
    if date:
        files = [DAILY_DIR / f"{date}.jsonl"]
    else:
        files = sorted(DAILY_DIR.glob("*.jsonl"), reverse=True)

    entries = []
    for fp in files:
        if not fp.exists():
            continue
        with open(fp, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if file_filter and file_filter not in entry.get("file", ""):
                        continue
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue

    if last:
        entries = entries[-last:]
    return entries


def main():
    parser = argparse.ArgumentParser(description="Hermes Log Helper v2 — JSONL changelog")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # append
    a = sub.add_parser("append", help="Log a file edit")
    a.add_argument("file", help="Path to edited file")
    a.add_argument("--reason", "-r", required=True, help="Why this edit")
    a.add_argument("--action", choices=["create", "modify", "delete"], help="Force action")

    # query
    q = sub.add_parser("query", help="Query history")
    q.add_argument("--file", "-f", help="Filter by file path substring")
    q.add_argument("--date", "-d", help="Filter by date (YYYY-MM-DD)")
    q.add_argument("--last", "-n", type=int, help="Show last N entries")
    q.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if args.cmd == "append":
        path = append_log(args.file, args.reason, action=args.action)
        print(f"✅ Logged → {path}")
    elif args.cmd == "query":
        entries = query_logs(args.file, args.date, args.last)
        if args.json:
            for e in entries:
                print(json.dumps(e, ensure_ascii=False))
        else:
            print(f"\n📜 {len(entries)} entries\n" + "=" * 80)
            for e in entries:
                delta = e.get("after", 0) - e.get("before", 0)
                sign = "+" if delta > 0 else ""
                print(f"\n[{e['ts']}] {e['action'].upper()}: {e['file']}")
                print(f"  Reason: {e['reason']}")
                print(f"  Size:   {e.get('before', 0)} → {e.get('after', 0)} ({sign}{delta} bytes)")


if __name__ == "__main__":
    main()