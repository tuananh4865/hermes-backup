#!/usr/bin/env python3
"""
daily_brief.py — Read-only daily brief generator for life-review skill.

Parses Tuấn Anh's Obsidian vault at WIKI_ROOT and emits a Telegram-ready
JSON payload. READ-ONLY: never writes to the wiki.

Output schema:
    {
      "date": "YYYY-MM-DD",
      "top_3_goals": [str, str, str],
      "one_metric": str,
      "one_project_next": {file, hub_path, next_action, mtime_iso},
      "active_habits": [{name, done_7d, total_7d}],
      "recent_log_entries": [{date, heading, snippet}],
      "telegram_message": "<=200 word Vietnamese-headed compact brief"
    }

Usage:
    python3 daily_brief.py --wiki /Volumes/Storage-1/Hermes/wiki [--self-check]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# --- heuristic limits (Telegram-friendly) -------------------------------
WORD_LIMIT = 200
MAX_GOALS = 3
MAX_LOG_ENTRIES = 3
MAX_HABITS = 5

# --- file conventions in Tuấn Anh's vault --------------------------------
LOG_HEADING_RE = re.compile(r"^##\s+\[(?P<date>\d{4}-\d{2}-\d{2})\]")
NEXT_ACTION_RE = re.compile(r"^next_action\s*:\s*(?P<value>.+?)\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^status\s*:\s*(?P<value>\S+)", re.MULTILINE)
NUMBER_LINE_RE = re.compile(r"^[-*]?\s*(\d[\d,.\s]*[a-zA-Z%₫đkKmM]?|[A-Z][\w\s]{2,40})\s*[:=]\s*(?P<num>-?\d[\d,.\s]*[%]?)", re.MULTILINE)
GOAL_BULLET_RE = re.compile(r"^[-*]\s+(?P<g>.+?)\s*$", re.MULTILINE)


def read_head(path: Path, n: int = 20) -> list[str]:
    """Return the first N lines of a file, dropping blank ones for content density."""
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[:n]
    return [ln for ln in lines if ln.strip()]


def recent_log_entries(log_path: Path, n: int = MAX_LOG_ENTRIES) -> list[dict[str, str]]:
    """Parse the most-recent n dated heading blocks from log.md.

    Filter heuristic: a heading is "substantive" if its body has at least 2 non-blank,
    non-list-only lines AND the heading line itself is not a sub-bullet. This skips
    the noisy `watchdog:batch` lines that just say "Batch scan: N changes" so the
    brief surfaces curator/setup/cron narratives instead.
    """
    if not log_path.exists():
        return []
    text = log_path.read_text(encoding="utf-8", errors="replace")
    blocks: list[tuple[str, str, str]] = []
    current: list[str] = []
    current_date: str | None = None
    current_heading: str | None = None
    for line in text.splitlines():
        m = LOG_HEADING_RE.match(line)
        if m:
            if current_date is not None and current:
                blocks.append((current_date, current_heading or "", "\n".join(current).strip()))
            current_date = m.group("date")
            current_heading = line.strip()
            current = []
        elif current_date is not None:
            current.append(line)
    if current_date is not None and current:
        blocks.append((current_date, current_heading or "", "\n".join(current).strip()))
    # Newest first; logs are append-only and chronological. Materialize reversed() before slicing.
    blocks_sorted = list(reversed(blocks[-100:]))

    def is_substantive(heading: str, body: str) -> bool:
        # Skip watchdog:batch-only entries (just say "Batch scan: N changes")
        if "Batch scan:" in heading and len([ln for ln in body.splitlines() if ln.strip()]) <= 2:
            return False
        # Skip session-meta lines (just "session | 20260816_xxx, Turns: N")
        if heading.startswith("## [") and "session |" in heading:
            return False
        # Need at least 2 non-blank content lines (bullets OK; watchdog entries have
        # only 1-2 short bullets like "- entities/x.md: modified")
        content_lines = [ln for ln in body.splitlines() if ln.strip()]
        if len(content_lines) < 3:
            return False
        return True

    out: list[dict[str, str]] = []
    for date, heading, body in blocks_sorted:
        if not is_substantive(heading, body):
            continue
        first_line = next(
            (ln.strip() for ln in body.splitlines() if ln.strip()),
            "",
        )
        # Prefer non-list-bullet lines when present (more informative)
        substantive = next(
            (
                ln.strip()
                for ln in body.splitlines()
                if ln.strip() and not ln.strip().startswith(("-", "*", "|"))
            ),
            first_line,
        )
        snippet = substantive[:160]
        # Heading source: strip the ## prefix + date for cleaner display
        clean_heading = re.sub(r"^##\s+\[\d{4}-\d{2}-\d{2}\]\s*", "", heading).strip()[:80]
        out.append({"date": date, "heading": clean_heading, "snippet": snippet})
        if len(out) >= n:
            break
    return out


def most_recent_project_hub(projects_dir: Path) -> tuple[Path | None, dict[str, Any]]:
    """Pick the most-recently-modified wiki/projects/<name>/HUB.md, skipping _*."""
    if not projects_dir.exists():
        return None, {}
    candidates: list[tuple[float, Path]] = []
    for hub in projects_dir.glob("*/HUB.md"):
        if hub.parts[-2].startswith("_"):
            continue  # skip _template, _backup, _meta
        try:
            candidates.append((hub.stat().st_mtime, hub))
        except OSError:
            continue
    if not candidates:
        return None, {}
    candidates.sort(reverse=True)
    top = candidates[0][1]
    name = top.parts[-2]
    meta: dict[str, Any] = {"file": f"wiki/projects/{name}/HUB.md", "mtime_iso": dt.datetime.fromtimestamp(top.stat().st_mtime).isoformat()}
    return top, meta


def extract_next_action(hub_path: Path) -> str | None:
    if not hub_path.exists():
        return None
    text = hub_path.read_text(encoding="utf-8", errors="replace")
    m = NEXT_ACTION_RE.search(text)
    return m.group("value").strip() if m else None


def extract_metric(hub_path: Path) -> str | None:
    """Pick the first numeric value from the Current Numbers block (heuristic)."""
    if not hub_path.exists():
        return None
    text = hub_path.read_text(encoding="utf-8", errors="replace")
    in_metrics = False
    for line in text.splitlines():
        if re.match(r"^##\s+Current Numbers", line, re.IGNORECASE):
            in_metrics = True
            continue
        if in_metrics and line.startswith("##"):
            break
        if in_metrics:
            m = NUMBER_LINE_RE.search(line + "\n") or re.search(r"[:=]\s*(-?\d[\d,.\s]*[%]?)", line)
            if m:
                # Prefer numeric groups over labels.
                num_match = re.search(r"(-?\d[\d,.\s]*[%]?)", line)
                if num_match:
                    return f"{line.strip()[:140]}"
    return None


def top_goals_from_active_project(projects_dir: Path, active_name: str | None, n: int = MAX_GOALS) -> list[str]:
    """Best-effort: look in the active project's `goals.md` or `HUB.md` Goals block."""
    if not active_name:
        return []
    pdir = projects_dir / active_name
    goals_md = pdir / "goals.md"
    src = goals_md if goals_md.exists() else (pdir / "HUB.md" if (pdir / "HUB.md").exists() else None)
    if not src:
        return []
    text = src.read_text(encoding="utf-8", errors="replace")
    in_goals = False
    goals: list[str] = []
    for line in text.splitlines():
        if re.match(r"^##\s+Goals", line, re.IGNORECASE):
            in_goals = True
            continue
        if in_goals and line.startswith("##"):
            break
        if in_goals:
            m = GOAL_BULLET_RE.match(line)
            if m:
                goals.append(m.group("g").strip())
        if len(goals) >= n:
            break
    return goals[:n]


def habit_summary(wiki_root: Path) -> list[dict[str, Any]]:
    """Pull last-7-days habit log from wiki/habits.md OR projects/_meta/habits.md if present."""
    candidates = [wiki_root / "habits.md", wiki_root / "projects" / "_meta" / "habits.md"]
    habits_path = next((p for p in candidates if p.exists()), None)
    if not habits_path:
        return []
    text = habits_path.read_text(encoding="utf-8", errors="replace")
    # Heuristic: a table-like row per habit. Avoid fragility by counting occurrences of
    # `[x]` (done) in the most-recent 7 lines per habit section. Keep conservative.
    out: list[dict[str, Any]] = []
    current_name: str | None = None
    rows: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current_name and rows:
                done = sum(1 for r in rows[-7:] if "[x]" in r.lower())
                out.append({"name": current_name, "done_7d": done, "total_7d": 7})
            current_name = line[3:].strip()
            rows = []
        elif current_name:
            rows.append(line)
    if current_name and rows:
        done = sum(1 for r in rows[-7:] if "[x]" in r.lower())
        out.append({"name": current_name, "done_7d": done, "total_7d": 7})
    return out[:MAX_HABITS]


def build_telegram_message(payload: dict[str, Any]) -> str:
    """Compose a <=WORD_LIMIT compact, Vietnamese-headed brief."""
    lines: list[str] = []
    lines.append(f"📅 Daily Brief — {payload['date']}")
    lines.append("")
    goals = payload["top_3_goals"]
    if goals:
        lines.append("🎯 Top goals:")
        for i, g in enumerate(goals, 1):
            lines.append(f"  {i}. {g}")
    else:
        lines.append("🎯 Top goals: no active goal block found")
    lines.append("")
    metric = payload.get("one_metric") or "no metric tracked"
    lines.append(f"📊 Metric: {metric}")
    lines.append("")
    nxt = payload.get("one_project_next") or {}
    if nxt:
        lines.append(f"🚧 Project next: {Path(nxt['hub_path']).parts[-2]} — {nxt.get('next_action') or '(no next_action)'}")
    else:
        lines.append("🚧 Project next: no active project hub")
    lines.append("")
    log_entries = payload.get("recent_log_entries") or []
    if log_entries:
        lines.append("📝 Recent log:")
        for entry in log_entries:
            lines.append(f"  - {entry['date']}: {entry.get('heading', '')[:90]}")
    lines.append("")
    habits = payload.get("active_habits") or []
    if habits:
        hb = ", ".join(f"{h['name']} {h['done_7d']}/{h['total_7d']}" for h in habits)
        lines.append(f"🔁 Habits (7d): {hb}")
    else:
        lines.append("🔁 Habits (7d): no habits.md tracked")
    text = "\n".join(lines).strip()
    # Truncate to WORD_LIMIT words; if overflow, slice on word boundary.
    words = text.split()
    if len(words) > WORD_LIMIT:
        words = words[:WORD_LIMIT]
    return " ".join(words)


def self_check(out: dict[str, Any]) -> tuple[bool, list[str]]:
    """Sanity passes for evidence-gate Recipe 2 discipline."""
    failures: list[str] = []
    if "date" not in out:
        failures.append("missing date")
    if "telegram_message" not in out:
        failures.append("missing telegram_message")
    elif len(out["telegram_message"].split()) > WORD_LIMIT + 5:
        failures.append(f"telegram_message word count overflow ({len(out['telegram_message'].split())})")
    return (len(failures) == 0, failures)


def run(wiki_root: Path) -> dict[str, Any]:
    today = dt.datetime.now().astimezone().date().isoformat()
    log_path = wiki_root / "log.md"
    projects_dir = wiki_root / "projects"
    entity = wiki_root / "entities" / "learned-about-tuananh.md"

    head = read_head(entity, n=20)
    log_entries = recent_log_entries(log_path)
    hub_path, hub_meta = most_recent_project_hub(projects_dir)
    active_project_name = hub_path.parts[-2] if hub_path else None

    next_action = extract_next_action(hub_path) if hub_path else None
    metric = extract_metric(hub_path) if hub_path else None
    goals = top_goals_from_active_project(projects_dir, active_project_name)
    if not goals:
        # Fall back: empty list — never invent goals.
        goals = []

    payload: dict[str, Any] = {
        "date": today,
        "top_3_goals": goals,
        "one_metric": metric,
        "one_project_next": {
            **hub_meta,
            "hub_path": str(hub_path) if hub_path else None,
            "next_action": next_action,
        },
        "active_habits": habit_summary(wiki_root),
        "recent_log_entries": log_entries,
        "context_window_lines": len(head),
        "source_paths": [
            str(log_path),
            str(entity),
            str(hub_path) if hub_path else None,
        ],
        "data_quality": "ok" if (log_entries and (next_action or metric)) else "low",
    }
    payload["telegram_message"] = build_telegram_message(payload)
    return payload


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="life-review daily brief generator")
    p.add_argument("--wiki", default="/Volumes/Storage-1/Hermes/wiki", help="Wiki root path")
    p.add_argument("--self-check", action="store_true", help="Run schema check before printing")
    p.add_argument("--json-out", default=None, help="Optional output JSON path; default = stdout")
    args = p.parse_args(argv)

    wiki_root = Path(args.wiki).expanduser()
    if not wiki_root.exists():
        print(f"ERROR: wiki root not found: {wiki_root}", file=sys.stderr)
        return 2

    payload = run(wiki_root)

    if args.self_check:
        ok, failures = self_check(payload)
        if not ok:
            print(json.dumps({"ok": False, "failures": failures}, indent=2))
            return 1
        print(json.dumps({"ok": True, "failures": []}))

    out_text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.json_out:
        out_p = Path(args.json_out).expanduser()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(out_text, encoding="utf-8")
        print(f"wrote {out_p}")
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
