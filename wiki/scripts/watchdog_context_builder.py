#!/opt/homebrew/bin/python3.14
"""
Wiki Context Builder
Gathers current wiki state for agent consumption.
Used by watchdog-triggered agents to quickly understand context.
Output: JSON with wiki health, recent changes, active projects.
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

WIKI_DIR = Path("/Volumes/Storage-1/Hermes/wiki")
EVENT_FILE = WIKI_DIR / "scripts" / "watchdog_event.json"
OUTPUT_FILE = WIKI_DIR / "scripts" / "watchdog_context.json"


def get_recent_transcripts(days=7):
    """Get recent transcript summaries."""
    transcripts_dir = WIKI_DIR / "raw" / "transcripts"
    recent = []
    if transcripts_dir.exists():
        cutoff = datetime.now() - timedelta(days=days)
        for date_dir in sorted(transcripts_dir.iterdir(), reverse=True):
            if date_dir.is_dir():
                for md_file in date_dir.iterdir():
                    if md_file.suffix == ".md":
                        mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
                        if mtime > cutoff:
                            content = md_file.read_text()
                            recent.append({
                                "file": str(md_file.relative_to(WIKI_DIR)),
                                "preview": content[:500],
                                "size": len(content)
                            })
    return recent


def get_watchdog_event():
    """Read watchdog event file."""
    if EVENT_FILE.exists():
        try:
            return json.loads(EVENT_FILE.read_text())
        except Exception:
            return None
    return None


def get_concept_stats():
    """Quick stats on concepts directory."""
    concepts_dir = WIKI_DIR / "concepts"
    if not concepts_dir.exists():
        return {"count": 0}

    md_files = list(concepts_dir.glob("*.md"))
    return {
        "count": len(md_files),
        "files": [f.name for f in md_files[:10]]
    }


def get_project_state():
    """Read current project state if exists."""
    project_file = WIKI_DIR / "concepts" / "project-tracker.md"
    if project_file.exists():
        content = project_file.read_text()
        return {"exists": True, "preview": content[:1000]}
    return {"exists": False}


def build_context():
    """Build full wiki context."""
    event = get_watchdog_event()
    context = {
        "generated_at": datetime.now().isoformat(),
        "wiki_dir": str(WIKI_DIR),
        "watchdog_event": event,
        "triggered_by_watchdog": event is not None,
        "concepts": get_concept_stats(),
        "project_state": get_project_state(),
        "recent_transcripts": get_recent_transcripts(days=7),
    }
    return context


def main():
    context = build_context()
    with open(OUTPUT_FILE, "w") as f:
        json.dump(context, f, indent=2)
    print(json.dumps(context, indent=2))


if __name__ == "__main__":
    main()
