#!/usr/bin/env python3
"""
weekly_review.py — Read-only weekly review generator for life-review skill.

Inspect the wiki vault and emit a JSON report covering:
    - completed_projects (status: archived/completed)
    - stalled_goals    (active hubs whose next_action mtime > 7 days old)
    - superseded_count (entries tagged supersedes: true)
    - notes_missing_date (frontmatter without `updated:`)
    - broken_link_candidates (top 5 wikilinks to missing files; opportunistic)
    - habit_consistency  (per-habit done vs total in last 7d)

Output schema:
    {
      "week_start": "YYYY-MM-DD",
      "completed_projects": [str],
      "stalled_goals": [{file, hub_path, days_since_update, next_action}],
      "habit_consistency": [{name, done_7d, total_7d}],
      "superseded_count": int,
      "missing_date_count": int,
      "broken_link_candidates": [str],
      "telegram_message": "<=500 word compact brief"
    }

Usage:
    python3 weekly_review.py --wiki /Volumes/Storage-1/Hermes/wiki \
                             [--week-start YYYY-MM-DD] [--json-out PATH] [--self-check]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

WORD_LIMIT = 500
STALL_DAYS = 7
COMPLETED_STATUS = {"archived", "completed", "done", "shipped"}
WIKILINK_RE = re.compile(r"\[\[(?P<target>[^\[\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_UPDATED_RE = re.compile(r"^updated\s*:\s*", re.MULTILINE)
SUPERSEDES_RE = re.compile(r"^supersedes\s*:\s*true", re.MULTILINE | re.IGNORECASE)


def last_monday(today: dt.date) -> dt.date:
    return today - dt.timedelta(days=today.weekday())


def project_hubs(projects_dir: Path) -> list[Path]:
    if not projects_dir.exists():
        return []
    hubs: list[Path] = []
    for hub in projects_dir.glob("*/HUB.md"):
        if hub.parts[-2].startswith("_"):
            continue
        hubs.append(hub)
    return hubs


def read_hub_status_and_next(hub: Path) -> tuple[str | None, str | None, float]:
    """Return (status, next_action, mtime) for a hub file."""
    try:
        mtime = hub.stat().st_mtime
    except OSError:
        mtime = 0.0
    if not hub.exists():
        return None, None, mtime
    text = hub.read_text(encoding="utf-8", errors="replace")
    status_m = re.search(r"^status\s*:\s*(\S+)", text, re.MULTILINE)
    na_m = re.search(r"^next_action\s*:\s*(.+?)\s*$", text, re.MULTILINE)
    status = status_m.group(1) if status_m else None
    next_action = na_m.group(1) if na_m else None
    return status, next_action, mtime


def completed_projects(hubs: list[Path]) -> list[str]:
    out = []
    for h in hubs:
        status, _, _ = read_hub_status_and_next(h)
        if status and status.lower() in COMPLETED_STATUS:
            out.append(f"wiki/projects/{h.parts[-2]}/HUB.md")
    return out


def stalled_goals(hubs: list[Path], today: dt.date) -> list[dict[str, object]]:
    out = []
    for h in hubs:
        status, na, mtime = read_hub_status_and_next(h)
        if status and status.lower() in COMPLETED_STATUS:
            continue
        if mtime <= 0:
            continue
        delta_days = (today - dt.date.fromtimestamp(mtime)).days
        if delta_days >= STALL_DAYS:
            out.append({
                "file": f"wiki/projects/{h.parts[-2]}/HUB.md",
                "hub_path": str(h),
                "days_since_update": delta_days,
                "next_action": na,
            })
    out.sort(key=lambda x: x["days_since_update"], reverse=True)
    return out


def habit_consistency(wiki_root: Path, habits_md: Path | None = None) -> list[dict[str, object]]:
    candidates = [wiki_root / "habits.md", wiki_root / "projects" / "_meta" / "habits.md"]
    p = habits_md or next((c for c in candidates if c.exists()), None)
    if not p:
        return []
    text = p.read_text(encoding="utf-8", errors="replace")
    out = []
    current: str | None = None
    rows: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current and rows:
                done = sum(1 for r in rows[-7:] if "[x]" in r.lower())
                out.append({"name": current, "done_7d": done, "total_7d": 7})
            current = line[3:].strip()
            rows = []
        elif current:
            rows.append(line)
    if current and rows:
        done = sum(1 for r in rows[-7:] if "[x]" in r.lower())
        out.append({"name": current, "done_7d": done, "total_7d": 7})
    return out


def count_superseded(wiki_root: Path) -> int:
    count = 0
    for md in wiki_root.rglob("*.md"):
        if "/_disabled_" in str(md) or "/_archive" in str(md):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if SUPERSEDES_RE.search(text):
            count += 1
    return count


def count_missing_dates(wiki_root: Path) -> int:
    """Heuristic: frontmatter has no `updated:` line and is clearly frontmatter-delimited."""
    count = 0
    for md in wiki_root.rglob("*.md"):
        if "/_disabled_" in str(md) or "/_archive" in str(md):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---\n", 4)
        if end == -1:
            continue
        fm = text[4:end]
        if not FRONTMATTER_UPDATED_RE.search(fm):
            count += 1
    return count


def broken_link_candidates(wiki_root: Path, limit: int = 5) -> list[str]:
    """Opportunistic scan: detect wikilinks whose target file does not exist."""
    missing: list[str] = []
    for md in wiki_root.rglob("*.md"):
        if "/_disabled_" in str(md):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in WIKILINK_RE.finditer(text):
            target = m.group("target").strip()
            # Skip URL-ish and section-only anchors.
            if target.startswith(("http", "#")):
                continue
            candidate = (md.parent / f"{target}.md").resolve()
            if not candidate.exists():
                missing.append(f"{md.name} → [[{target}]]")
                if len(missing) >= limit:
                    return missing
    return missing


def build_telegram_message(payload: dict[str, object]) -> str:
    lines: list[str] = []
    lines.append(f"📅 Weekly Review — week of {payload['week_start']}")
    lines.append("")
    completed = payload.get("completed_projects") or []
    if completed:
        lines.append(f"✅ Completed ({len(completed)}):")
        for p in completed[:5]:
            lines.append(f"  - {p.split('/')[-2]}")
    else:
        lines.append("✅ Completed: none archived this week")
    lines.append("")
    stalled = payload.get("stalled_goals") or []
    if stalled:
        lines.append(f"⚠️ Stalled ({len(stalled)}):")
        for s in stalled[:5]:
            lines.append(f"  - {Path(str(s['hub_path'])).parts[-2]} — {s['days_since_update']}d stale; next: {s.get('next_action') or '(blank)'}")
    else:
        lines.append("⚠️ Stalled: none >7d")
    lines.append("")
    habits = payload.get("habit_consistency") or []
    if habits:
        for h in habits:
            lines.append(f"🔁 {h['name']}: {h['done_7d']}/{h['total_7d']} (7d)")
    else:
        lines.append("🔁 Habits: not tracked")
    lines.append("")
    lines.append(f"📚 Superseded entries: {payload.get('superseded_count', 0)}")
    lines.append(f"📅 Missing `updated:` frontmatter: {payload.get('missing_date_count', 0)}")
    broken = payload.get("broken_link_candidates") or []
    if broken:
        lines.append("🔗 Broken link candidates:")
        for b in broken:
            lines.append(f"  - {b}")
    text = "\n".join(lines).strip()
    words = text.split()
    if len(words) > WORD_LIMIT:
        words = words[:WORD_LIMIT]
    return " ".join(words)


def run(wiki_root: Path, week_start: dt.date) -> dict[str, object]:
    projects_dir = wiki_root / "projects"
    hubs = project_hubs(projects_dir)
    today = dt.date.today()

    payload: dict[str, object] = {
        "week_start": week_start.isoformat(),
        "completed_projects": completed_projects(hubs),
        "stalled_goals": stalled_goals(hubs, today),
        "habit_consistency": habit_consistency(wiki_root),
        "superseded_count": count_superseded(wiki_root),
        "missing_date_count": count_missing_dates(wiki_root),
        "broken_link_candidates": broken_link_candidates(wiki_root),
        "source_paths": [str(wiki_root)],
        "data_quality": "ok",
    }
    payload["telegram_message"] = build_telegram_message(payload)
    return payload


def self_check(payload: dict[str, object]) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if "week_start" not in payload:
        failures.append("missing week_start")
    if "telegram_message" not in payload:
        failures.append("missing telegram_message")
    elif len(payload["telegram_message"].split()) > WORD_LIMIT + 5:
        failures.append("telegram_message overflow")
    return (len(failures) == 0, failures)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="life-review weekly review generator")
    p.add_argument("--wiki", default="/Volumes/Storage-1/Hermes/wiki")
    p.add_argument("--week-start", default=None, help="ISO date; default = Monday of current week")
    p.add_argument("--json-out", default=None)
    p.add_argument("--self-check", action="store_true")
    args = p.parse_args(argv)

    wiki_root = Path(args.wiki).expanduser()
    if not wiki_root.exists():
        print(f"ERROR: wiki root not found: {wiki_root}", file=sys.stderr)
        return 2

    if args.week_start:
        week_start = dt.date.fromisoformat(args.week_start)
    else:
        week_start = last_monday(dt.date.today())

    payload = run(wiki_root, week_start)

    if args.self_check:
        ok, failures = self_check(payload)
        if not ok:
            print(json.dumps({"ok": False, "failures": failures}, indent=2))
            return 1
        print(json.dumps({"ok": True}))

    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.json_out:
        out = Path(args.json_out).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
