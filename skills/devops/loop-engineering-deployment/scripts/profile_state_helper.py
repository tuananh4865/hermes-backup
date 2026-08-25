#!/usr/bin/env python3
"""
Profile State Helper — HERMES_HOME-aware
========================================

Manages state files for every Hermes profile. Use this when deploying
Loop Engineering system-wide so each profile (`content-director`,
`research-lead`, `coder`, `default`) has its own auto-logged state.

Production location: `~/.hermes/loop-engineering/profile_state.py`
Source: this file (shipped with the loop-engineering-deployment skill)

Usage (Python):
    from profile_state import append_verdict, append_run, read_state, ensure_state
    append_verdict("research-lead", "PASS", 9.3, [], goal="...", worker="...")

Usage (CLI):
    python3 profile_state.py verdict <profile> <PASS|FAIL|WARN> <score> <issues_json>
    python3 profile_state.py run <profile> <goal> <runs> <PASS|FAIL> <score>
    python3 profile_state.py read <profile>
    python3 profile_state.py ensure <profile>
    python3 profile_state.py list

Path resolution: uses os.environ.get("HERMES_HOME", ~/.hermes) — never hardcoded.
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

# HERMES_HOME-aware (NEVER hardcode ~/.hermes — see skill pitfalls)
TZ_VN = timezone(timedelta(hours=7))
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
TEMPLATE_PATH = HERMES_HOME / "profiles" / "_template" / "state.md"


def now_str():
    return datetime.now(TZ_VN).strftime("%Y-%m-%d %H:%M:%S %z")


def now_iso():
    return datetime.now(TZ_VN).isoformat()


def state_path(profile: str) -> Path:
    return HERMES_HOME / "profiles" / profile / "state.md"


def ensure_state(profile: str) -> Path:
    """Create state file from template if doesn't exist. Idempotent."""
    p = state_path(profile)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        if TEMPLATE_PATH.exists():
            content = TEMPLATE_PATH.read_text()
            content = content.replace("{profile_name}", profile)
            content = content.replace("{ISO date}", now_iso())
            p.write_text(content)
        else:
            # Fallback: minimal state
            p.write_text(_fallback_state(profile))
    return p


def _fallback_state(profile: str) -> str:
    return f"""---
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
"""


def append_verdict(profile, verdict, score, issues, goal="", worker=""):
    """Append a quality-checker verdict row to profile state."""
    ensure_state(profile)
    p = state_path(profile)
    content = p.read_text()
    issues_str = json.dumps(issues, ensure_ascii=False) if issues else "[]"
    n = content.count("| PASS |") + content.count("| FAIL |") + content.count("| WARN |") + 1
    row = f"| {n} | {now_str()} | {verdict} | {score} | {issues_str} | {worker} | {goal} |\n"
    marker = "## Recent Verdicts"
    if marker in content:
        parts = content.split(marker)
        after = parts[1]
        lines = after.split("\n")
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


def append_run(profile, goal, runs, result, score=0.0):
    ensure_state(profile)
    p = state_path(profile)
    content = p.read_text()
    n = content.count("| PASS |") + content.count("| FAIL |") + 1
    row = f"| {n} | {now_str()} | {goal} | {profile} | {runs} | {result} | {score} |\n"
    marker = "## Run History"
    if marker in content:
        parts = content.split(marker)
        after = parts[1].split("\n")
        new_after = []
        appended = False
        for line in after:
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
    p = state_path(profile)
    if not p.exists():
        ensure_state(profile)
    return p.read_text()


def list_profiles() -> list:
    profiles_dir = HERMES_HOME / "profiles"
    if not profiles_dir.exists():
        return []
    return sorted(p.name for p in profiles_dir.iterdir()
                  if p.is_dir() and (p / "state.md").exists())


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hermes Profile State Helper")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_v = sub.add_parser("verdict")
    p_v.add_argument("profile")
    p_v.add_argument("verdict", choices=["PASS", "FAIL", "WARN"])
    p_v.add_argument("score", type=float)
    p_v.add_argument("issues")
    p_v.add_argument("--goal", default="")
    p_v.add_argument("--worker", default="")
    p_r = sub.add_parser("run")
    p_r.add_argument("profile")
    p_r.add_argument("goal")
    p_r.add_argument("runs", type=int)
    p_r.add_argument("result", choices=["PASS", "FAIL"])
    p_r.add_argument("--score", type=float, default=0.0)
    p_rd = sub.add_parser("read")
    p_rd.add_argument("profile")
    p_e = sub.add_parser("ensure")
    p_e.add_argument("profile")
    sub.add_parser("list")
    args = parser.parse_args()
    if args.cmd == "verdict":
        issues = json.loads(args.issues)
        append_verdict(args.profile, args.verdict, args.score, issues, args.goal, args.worker)
        print(f"✅ Appended verdict to {args.profile}/state.md")
    elif args.cmd == "run":
        append_run(args.profile, args.goal, args.runs, args.result, args.score)
        print(f"✅ Appended run history to {args.profile}/state.md")
    elif args.cmd == "read":
        print(read_state(args.profile))
    elif args.cmd == "ensure":
        print(f"✅ State file: {ensure_state(args.profile)}")
    elif args.cmd == "list":
        for prof in list_profiles():
            print(f"  {prof}")
