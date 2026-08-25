#!/usr/bin/env python3
"""
Hermes Activity Analyzer — Chase pattern step 2 (video njHuj8OxIVI).

Reads BOTH log layers and extracts skill candidates:
  1. JSONL activity logs  — /Volumes/Storage-1/Hermes/logs/activity/*.jsonl (from hook, forward-looking)
  2. Hermes session DB    — ~/.hermes/state.db messages table (backfill, 132K+ rows of history)

Usage:
    python3 analyze_activity.py                 # last 30 days, both sources
    python3 analyze_activity.py --days 90
    python3 analyze_activity.py --source db     # db | jsonl | both
    python3 analyze_activity.py --json          # machine-readable output
"""

import argparse
import gzip
import json
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ICT = timezone(timedelta(hours=7))
ACTIVITY_DIR = Path("/Volumes/Storage-1/Hermes/logs/activity")
FALLBACK_DIR = Path.home() / ".hermes" / "logs" / "activity"
STATE_DB = Path.home() / ".hermes" / "state.db"


def load_jsonl(days: int) -> list[dict]:
    cutoff = datetime.now(ICT) - timedelta(days=days)
    events = []
    for directory in (ACTIVITY_DIR, FALLBACK_DIR):
        if not directory.is_dir():
            continue
        for path in sorted(list(directory.glob("*.jsonl")) + list(directory.glob("*.jsonl.gz"))):
            try:
                day = datetime.strptime(path.name.split(".")[0], "%Y-%m-%d").replace(tzinfo=ICT)
            except ValueError:
                continue
            if day < cutoff - timedelta(days=1):
                continue
            try:
                if path.suffix == ".gz":
                    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
                        raw = fh.read()
                else:
                    raw = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return events


def load_db(days: int) -> list[dict]:
    """Backfill from Hermes' own message store — tool_name is already a column."""
    if not STATE_DB.exists():
        return []
    cutoff = (datetime.now(ICT) - timedelta(days=days)).timestamp()
    con = sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(
            """
            SELECT session_id, role, tool_name, timestamp, token_count,
                   substr(COALESCE(content, ''), 1, 300) AS snippet
            FROM messages
            WHERE timestamp >= ?
            ORDER BY timestamp
            """,
            (cutoff,),
        ).fetchall()
    finally:
        con.close()

    events = []
    for r in rows:
        events.append(
            {
                "ts": datetime.fromtimestamp(r["timestamp"], ICT).isoformat(timespec="seconds"),
                "_epoch": r["timestamp"],
                "event": "post_tool_call" if r["tool_name"] else f"message:{r['role']}",
                "tool": r["tool_name"] or "",
                "session_id": r["session_id"],
                "role": r["role"],
                "tokens": r["token_count"] or 0,
                "snippet": r["snippet"] or "",
            }
        )
    return events


def epoch_of(ev: dict) -> float:
    if "_epoch" in ev:
        return ev["_epoch"]
    try:
        return datetime.fromisoformat(ev["ts"]).timestamp()
    except Exception:
        return 0.0


def analyze(events: list[dict], top: int = 20) -> dict:
    tools = Counter(e["tool"] for e in events if e.get("tool"))

    # Per-session ordered tool chains
    chains: dict[str, list[str]] = defaultdict(list)
    for ev in sorted(events, key=epoch_of):
        if ev.get("tool"):
            chains[ev.get("session_id", "?")].append(ev["tool"])

    # Repeating n-grams (collapse immediate self-repeats: terminal×20 is one habit, not 20)
    ngrams: dict[int, Counter] = {n: Counter() for n in (2, 3, 4)}
    for chain in chains.values():
        dedup = [t for i, t in enumerate(chain) if i == 0 or t != chain[i - 1]]
        for n in ngrams:
            for i in range(len(dedup) - n + 1):
                ngrams[n][" → ".join(dedup[i : i + n])] += 1

    hours = Counter(datetime.fromtimestamp(epoch_of(e), ICT).hour for e in events if epoch_of(e))
    days = Counter(datetime.fromtimestamp(epoch_of(e), ICT).strftime("%Y-%m-%d") for e in events if epoch_of(e))

    durations = [e["duration_ms"] for e in events if isinstance(e.get("duration_ms"), (int, float))]
    errors = Counter(e["tool"] for e in events if e.get("error_type"))

    # Skill candidates: a chain seen 5+ times across 2+ sessions = a real habit
    chain_sessions: dict[str, set] = defaultdict(set)
    for sid, chain in chains.items():
        dedup = [t for i, t in enumerate(chain) if i == 0 or t != chain[i - 1]]
        for n in (3, 4):
            for i in range(len(dedup) - n + 1):
                chain_sessions[" → ".join(dedup[i : i + n])].add(sid)

    candidates = []
    for n in (4, 3):
        for pattern, count in ngrams[n].most_common(40):
            nsess = len(chain_sessions.get(pattern, ()))
            if count >= 5 and nsess >= 2:
                candidates.append({"pattern": pattern, "count": count, "sessions": nsess, "length": n})
    candidates.sort(key=lambda c: (-c["count"], -c["length"]))

    return {
        "total_events": len(events),
        "tool_calls": sum(tools.values()),
        "sessions": len(chains),
        "active_days": len(days),
        "top_tools": tools.most_common(top),
        "ngrams": {n: c.most_common(12) for n, c in ngrams.items()},
        "hours": sorted(hours.items()),
        "busiest_days": days.most_common(10),
        "avg_duration_ms": round(sum(durations) / len(durations), 1) if durations else None,
        "slowest_tools": Counter(
            {e["tool"]: e["duration_ms"] for e in events if e.get("duration_ms") and e.get("tool")}
        ).most_common(8),
        "errors": errors.most_common(10),
        "skill_candidates": candidates[:15],
    }


def render(rep: dict, days: int, source: str) -> str:
    L = []
    L.append("=" * 74)
    L.append(f"  HERMES ACTIVITY ANALYSIS — last {days} days (source: {source})")
    L.append("=" * 74)
    L.append(
        f"\nevents={rep['total_events']:,}  tool_calls={rep['tool_calls']:,}  "
        f"sessions={rep['sessions']:,}  active_days={rep['active_days']}"
    )
    if rep["avg_duration_ms"] is not None:
        L.append(f"avg tool duration: {rep['avg_duration_ms']} ms")

    L.append(f"\n{'─' * 74}\nTOP TOOLS\n{'─' * 74}")
    total = rep["tool_calls"] or 1
    for name, count in rep["top_tools"]:
        bar = "█" * max(1, int(count / total * 44))
        L.append(f"  {name:26s} {count:>7,}  {count/total*100:5.1f}%  {bar}")

    for n in (2, 3, 4):
        rows = [r for r in rep["ngrams"].get(n, []) if r[1] >= 3]
        if not rows:
            continue
        L.append(f"\n{'─' * 74}\nREPEATING SEQUENCES (length {n}, self-repeats collapsed)\n{'─' * 74}")
        for pattern, count in rows:
            L.append(f"  {count:>5,}×  {pattern}")

    if rep["skill_candidates"]:
        L.append(f"\n{'─' * 74}\n🎯 SKILL CANDIDATES (≥5 occurrences, ≥2 sessions)\n{'─' * 74}")
        for i, c in enumerate(rep["skill_candidates"], 1):
            L.append(f"  {i:2d}. {c['count']:>4,}× in {c['sessions']} sessions  |  {c['pattern']}")

    if rep["errors"]:
        L.append(f"\n{'─' * 74}\nTOOLS WITH ERRORS\n{'─' * 74}")
        for name, count in rep["errors"]:
            L.append(f"  {name:26s} {count:>6,} errors")

    if rep["hours"]:
        L.append(f"\n{'─' * 74}\nTIME-OF-DAY (ICT)\n{'─' * 74}")
        peak = max(c for _, c in rep["hours"]) or 1
        for hour, count in rep["hours"]:
            L.append(f"  {hour:02d}:00  {count:>7,}  {'▇' * max(1, int(count / peak * 40))}")

    L.append(f"\n{'─' * 74}\nBUSIEST DAYS\n{'─' * 74}")
    for day, count in rep["busiest_days"]:
        L.append(f"  {day}  {count:>7,} events")

    L.append("\n" + "=" * 74)
    L.append("  NEXT: pick a candidate → run manually → codify skill → cron automation")
    L.append("=" * 74)
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--source", choices=["jsonl", "db", "both"], default="both")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    events = []
    if args.source in ("jsonl", "both"):
        events += load_jsonl(args.days)
    if args.source in ("db", "both"):
        events += load_db(args.days)

    if not events:
        print(f"No events found in last {args.days} days (source={args.source}).")
        return

    rep = analyze(events, top=args.top)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if args.json else render(rep, args.days, args.source))


if __name__ == "__main__":
    main()
