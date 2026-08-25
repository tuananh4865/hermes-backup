#!/usr/bin/env python3
"""
Verify task-log structure cho MỌI project.
Usage: python3 _verify_logs.py [--project=name] [--verbose]

Check:
- File _task-log.jsonl exists và là JSONL valid
- Mỗi entry có 4 required fields: ts, action, file, reason
- Action ∈ {create, modify, delete, redeploy, restart, test, fix, query, deploy}
- ts parse được thành datetime
- Helper script _log_task.py exists + executable

Output: per-project report + overall PASS/FAIL
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki/projects")
REQUIRED = {"ts", "action", "file", "reason"}
VALID_ACTIONS = {"create", "modify", "delete", "redeploy", "restart", "test", "fix", "query", "deploy", "verify", "check", "scan", "init", "delegate", "research"}
TS_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S.%f"]


def check_project(name: str, path: Path, verbose: bool = False) -> dict:
    """Check one project. Returns dict with stats."""
    log_path = path / "_task-log.jsonl"
    helper_path = path / "_log_task.py"

    result = {
        "name": name,
        "log_exists": log_path.exists(),
        "helper_exists": helper_path.exists(),
        "helper_executable": helper_path.exists() and os.access(helper_path, os.X_OK),
        "total_entries": 0,
        "valid_entries": 0,
        "invalid_entries": [],
        "last_log_ts": None,
        "last_action": None,
        "first_log_ts": None,
    }

    if not log_path.exists():
        result["error"] = "_task-log.jsonl NOT FOUND"
        return result

    with open(log_path) as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            result["total_entries"] += 1
            try:
                d = json.loads(line)
                if not REQUIRED.issubset(d.keys()):
                    result["invalid_entries"].append({"line": i, "reason": f"missing fields: {REQUIRED - d.keys()}"})
                elif d["action"] not in VALID_ACTIONS:
                    result["invalid_entries"].append({"line": i, "reason": f"invalid action: {d['action']}"})
                else:
                    result["valid_entries"] += 1
                    # Try parse ts
                    parsed_ts = False
                    for fmt in TS_FORMATS:
                        try:
                            datetime.strptime(d["ts"], fmt)
                            parsed_ts = True
                            break
                        except ValueError:
                            continue
                    if parsed_ts:
                        if result["first_log_ts"] is None:
                            result["first_log_ts"] = d["ts"]
                        result["last_log_ts"] = d["ts"]
                        result["last_action"] = d["action"]
                    else:
                        result["invalid_entries"].append({"line": i, "reason": f"invalid ts: {d['ts']}"})
            except json.JSONDecodeError as e:
                result["invalid_entries"].append({"line": i, "reason": f"JSON parse: {e}"})

    return result


def main():
    args = sys.argv[1:]
    verbose = "--verbose" in args
    project_filter = next((a.split("=")[1] for a in args if a.startswith("--project=")), None)

    overall_pass = True
    print("=" * 70)
    print("📋 TASK-LOG STRUCTURE VERIFICATION")
    print("=" * 70)

    for proj_dir in sorted(WIKI_ROOT.iterdir()):
        if not proj_dir.is_dir():
            continue
        name = proj_dir.name
        if name.startswith("_") or name.startswith("."):
            continue  # skip _template, .next, etc
        if project_filter and name != project_filter:
            continue

        r = check_project(name, proj_dir, verbose)
        
        # Status icon
        if not r["log_exists"]:
            status = "❌"
            overall_pass = False
        elif r["invalid_entries"]:
            status = "⚠️"
            overall_pass = False
        elif not r["helper_exists"] or not r["helper_executable"]:
            status = "⚠️"
        else:
            status = "✅"

        print(f"\n{status} {name}/")
        print(f"   log: {'YES' if r['log_exists'] else 'NO'} ({r['total_entries']} entries, {r['valid_entries']} valid)")
        print(f"   helper: {'YES' if r['helper_exists'] else 'NO'} ({'exec' if r['helper_executable'] else 'NOT exec'})")
        if r["last_log_ts"]:
            print(f"   last: {r['last_log_ts']} ({r['last_action']})")
            print(f"   first: {r['first_log_ts']}")
        
        if r["invalid_entries"] and verbose:
            print(f"   ⚠️ {len(r['invalid_entries'])} invalid entries:")
            for inv in r["invalid_entries"][:5]:
                print(f"      line {inv['line']}: {inv['reason']}")
            if len(r["invalid_entries"]) > 5:
                print(f"      ... +{len(r['invalid_entries']) - 5} more")

    print("\n" + "=" * 70)
    if overall_pass:
        print("✅ OVERALL: PASS — all projects log structure OK")
        sys.exit(0)
    else:
        print("❌ OVERALL: FAIL — some projects have issues")
        sys.exit(1)


if __name__ == "__main__":
    main()