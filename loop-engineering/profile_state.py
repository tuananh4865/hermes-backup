#!/usr/bin/env python3
"""
Profile State Helper — HERMES_HOME-aware
Quản lý state file cho mọi Hermes profile.

Usage (CLI):
    python3 profile_state.py verdict <profile> <PASS|FAIL|WARN> <score> <issues_json>
    python3 profile_state.py run <profile> <goal> <runs> <PASS|FAIL> <score>
    python3 profile_state.py read <profile>
    python3 profile_state.py ensure <profile>     # Tạo từ template nếu chưa có
    python3 profile_state.py list                 # Liệt kê profiles có state file

Usage (Python):
    from profile_state import append_verdict, append_run, read_state, ensure_state
"""
import os
import sys
import json
import argparse
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

TZ_VN = timezone(timedelta(hours=7))
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
TEMPLATE_PATH = HERMES_HOME / "profiles" / "_template" / "state.md"


def now_str() -> str:
    return datetime.now(TZ_VN).strftime("%Y-%m-%d %H:%M:%S %z")


def now_iso() -> str:
    return datetime.now(TZ_VN).isoformat()


def state_path(profile: str) -> Path:
    """Resolve state file path for a profile."""
    return HERMES_HOME / "profiles" / profile / "state.md"


def ensure_state(profile: str) -> Path:
    """Create state file from template if doesn't exist."""
    p = state_path(profile)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        if TEMPLATE_PATH.exists():
            content = TEMPLATE_PATH.read_text()
            # Substitute placeholders
            content = content.replace("{profile_name}", profile)
            content = content.replace("{ISO date}", now_iso())
            p.write_text(content)
        else:
            # Fallback: minimal state
            p.write_text(f"""---
profile: {profile}
updated: {now_iso()}
loop_engineering: enabled
---

# Profile State — {profile}

## Current Goal
None

## Recent Verdicts
| # | Time | Verdict | Score | Issues | Goal |
|---|------|---------|-------|--------|------|

## Run History
| # | Time | Goal | Runs | Result | Score |
|---|------|------|------|--------|-------|

## What Worked
- None yet

## What Failed
- None yet

## Open Items
- None
""")
    return p


def append_verdict(profile: str, verdict: str, score: float, issues: list, goal: str = "", worker: str = ""):
    """Append a quality-checker verdict row to profile state."""
    ensure_state(profile)
    p = state_path(profile)
    content = p.read_text()
    
    # Find "## Recent Verdicts" section
    issues_str = json.dumps(issues, ensure_ascii=False) if issues else "[]"
    
    # Count existing verdicts
    n = content.count("| PASS |") + content.count("| FAIL |") + content.count("| WARN |") + 1
    
    row = f"| {n} | {now_str()} | {verdict} | {score} | {issues_str} | {worker} | {goal} |\n"
    
    # Find the table under "## Recent Verdicts" and append
    marker = "## Recent Verdicts"
    if marker in content:
        parts = content.split(marker)
        # Find end of table (next blank line or next section)
        after_marker = parts[1]
        lines = after_marker.split("\n")
        # Skip header, separator, append after last data row
        new_after = []
        in_table = False
        appended = False
        for line in lines:
            new_after.append(line)
            if "|" in line and not line.strip().startswith("|---") and not line.startswith("| #") and "|" in line[1:]:
                # data row
                if not appended:
                    new_after.append(row.rstrip())
                    appended = True
                    in_table = True
            elif in_table and line.strip() == "":
                # End of table
                in_table = False
        if not appended:
            # Just append after separator
            for i, line in enumerate(new_after):
                if "|" in line and "---" in line:
                    new_after.insert(i+1, row.rstrip())
                    appended = True
                    break
        parts[1] = "\n".join(new_after)
        content = marker.join(parts)
    
    # Update timestamp in frontmatter
    content = content.replace(
        f"updated: {now_str().split()[0]}",
        f"updated: {now_iso()}"
    )
    
    p.write_text(content)
    return row


def append_run(profile: str, goal: str, runs: int, result: str, score: float = 0.0):
    """Append a loop-goal run history row."""
    ensure_state(profile)
    p = state_path(profile)
    content = p.read_text()
    
    n = content.count("| PASS |") + content.count("| FAIL |") + 1
    row = f"| {n} | {now_str()} | {goal} | {profile} | {runs} | {result} | {score} |\n"
    
    marker = "## Run History"
    if marker in content:
        parts = content.split(marker)
        after_marker = parts[1]
        lines = after_marker.split("\n")
        new_after = []
        appended = False
        for line in lines:
            new_after.append(line)
            if "|" in line and not line.strip().startswith("|---") and not line.startswith("| #"):
                if not appended:
                    new_after.append(row.rstrip())
                    appended = True
        if not appended:
            for i, line in enumerate(new_after):
                if "|" in line and "---" in line:
                    new_after.insert(i+1, row.rstrip())
                    appended = True
                    break
        parts[1] = "\n".join(new_after)
        content = marker.join(parts)
    
    p.write_text(content)
    return row


def read_state(profile: str) -> str:
    """Read state file content."""
    p = state_path(profile)
    if not p.exists():
        ensure_state(profile)
    return p.read_text()


def list_profiles() -> list:
    """List profiles with state files."""
    profiles_dir = HERMES_HOME / "profiles"
    if not profiles_dir.exists():
        return []
    result = []
    for p in sorted(profiles_dir.iterdir()):
        if p.is_dir() and (p / "state.md").exists():
            result.append(p.name)
    return result


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hermes Profile State Helper")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    # verdict
    p_v = sub.add_parser("verdict", help="Append quality-checker verdict")
    p_v.add_argument("profile")
    p_v.add_argument("verdict", choices=["PASS", "FAIL", "WARN"])
    p_v.add_argument("score", type=float)
    p_v.add_argument("issues", help="JSON array of issues")
    p_v.add_argument("--goal", default="")
    p_v.add_argument("--worker", default="")
    
    # run
    p_r = sub.add_parser("run", help="Append loop-goal run history")
    p_r.add_argument("profile")
    p_r.add_argument("goal")
    p_r.add_argument("runs", type=int)
    p_r.add_argument("result", choices=["PASS", "FAIL"])
    p_r.add_argument("--score", type=float, default=0.0)
    
    # read
    p_rd = sub.add_parser("read", help="Read state file")
    p_rd.add_argument("profile")
    
    # ensure
    p_e = sub.add_parser("ensure", help="Create state from template")
    p_e.add_argument("profile")
    
    # list
    sub.add_parser("list", help="List profiles with state files")
    
    args = parser.parse_args()
    
    if args.cmd == "verdict":
        issues = json.loads(args.issues)
        row = append_verdict(args.profile, args.verdict, args.score, issues, args.goal, args.worker)
        print(f"✅ Appended verdict to {args.profile}/state.md")
    elif args.cmd == "run":
        row = append_run(args.profile, args.goal, args.runs, args.result, args.score)
        print(f"✅ Appended run history to {args.profile}/state.md")
    elif args.cmd == "read":
        print(read_state(args.profile))
    elif args.cmd == "ensure":
        p = ensure_state(args.profile)
        print(f"✅ State file: {p}")
    elif args.cmd == "list":
        for prof in list_profiles():
            print(f"  {prof}")
