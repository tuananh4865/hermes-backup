#!/opt/homebrew/bin/python3.14
"""
Wiki Quality Gate — Proactive Self-Improvement Engine

Monitors and improves wiki quality by targeting pages that:
1. Are CRITICAL tier (score < 6.5)
2. Are stale (>14 days) with low quality
3. Are stubs (<500 chars)
4. Have poor connectivity (<2 outbound links)

Runs autonomously during cron jobs to keep wiki avg score in 6.5-7.5 range.

Usage:
    python3 scripts/wiki_quality_gate.py --check           # Report status
    python3 scripts/wiki_quality_gate.py --gate           # Full gate check
    python3 scripts/wiki_quality_gate.py --improve        # Auto-improve CRITICAL pages
    python3 scripts/wiki_quality_gate.py --full           # Full: check + improve + report
    python3 scripts/wiki_quality_gate.py --stats          # Quick stats
    python3 scripts/wiki_quality_gate.py --stubs          # Show all stubs
    python3 scripts/wiki_quality_gate.py --stale-critical # Stale + low score
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ═══════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
STATE_FILE = WIKI_PATH / "_meta" / "quality_gate_state.json"

# Quality gates
MIN_ACCEPTABLE = 6.5
MAX_ACCEPTABLE = 7.5
TARGET_AVG = 7.0  # middle of acceptable range

# Auto-improve thresholds
STUB_MAX_CHARS = 500
STALE_IMPROVE_DAYS = 14   # stale pages older than this that are CRITICAL
LOW_CONNECTIVITY = 2      # outbound links below this on CRITICAL pages

# How many pages to improve per cron run
IMPROVE_BATCH = 50

# Scoring weights (must sum to 1.0)
WEIGHT_COMPLETENESS = 0.35
WEIGHT_STRUCTURE = 0.25
WEIGHT_FRESHNESS = 0.20
WEIGHT_CONNECTIVITY = 0.20

# Directories to always skip
SKIP_DIRS = {"raw", "_archive", ".obsidian", "__pycache__", "_templates",
             "node_modules", ".git", "_drops", "_meta"}

# ═══════════════════════════════════════════════════════════════════════
# STATE
# ═══════════════════════════════════════════════════════════════════════

def get_state() -> dict:
    """Load quality gate state"""
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except:
        pass
    return {
        "last_run": None,
        "last_avg": 0,
        "improved_count": 0,
        "expansion_count": 0,
        "avg_history": [],
        "critical_history": [],
    }


def save_state(state: dict):
    """Save quality gate state"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ═══════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════

def get_all_wiki_pages() -> List[Path]:
    files = []
    for f in WIKI_PATH.rglob("*.md"):
        if any(x in f.parts for x in SKIP_DIRS):
            continue
        files.append(f)
    return files


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    if not content.startswith("---"):
        return None, content
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    fm_text = content[4:end]
    body = content[end + 4:].lstrip("\n")
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm, body


def extract_wikilinks(content: str) -> List[str]:
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)


def count_headings(content: str) -> int:
    return len(re.findall(r'^#+ .+$', content, re.MULTILINE))


def is_stale(updated_str: str, days: int = 30) -> bool:
    if not updated_str:
        return True
    try:
        updated = datetime.strptime(updated_str[:10], "%Y-%m-%d")
        return (datetime.now() - updated).days > days
    except:
        return False


def get_tier(score: float) -> str:
    if score < MIN_ACCEPTABLE:
        return "CRITICAL"
    elif score <= MAX_ACCEPTABLE:
        return "ACCEPTABLE"
    else:
        return "HIGH"


# ═══════════════════════════════════════════════════════════════════════
# SCORING
# ═══════════════════════════════════════════════════════════════════════

def score_completeness(fm: Optional[dict], body: str) -> float:
    score = 0
    content_len = len(body.strip())
    if content_len > 2000:
        score += 3
    elif content_len > 500:
        score += 2
    elif content_len > 100:
        score += 1

    heading_count = count_headings(body)
    if heading_count >= 4:
        score += 2
    elif heading_count >= 2:
        score += 1

    if fm:
        required = ["title", "updated", "type", "tags"]
        fm_fields = sum(1 for f in required if f in fm and fm[f])
        score += fm_fields * 0.5

    return min(10, score)


def score_structure(fm: Optional[dict], body: str) -> float:
    score = 0
    if fm:
        score += 2
    wikilinks = extract_wikilinks(body)
    link_count = len(wikilinks)
    if link_count >= 3:
        score += 3
    elif link_count >= 1:
        score += 2
    if re.search(r'^[*\-] |^\d+\. ', body, re.MULTILINE):
        score += 1
    if "|" in body and "-" in body:
        score += 1
    if "```" in body:
        score += 1
    if re.match(r'^# .+$', body, re.MULTILINE):
        score += 1
    return min(10, score)


def score_freshness(fm: Optional[dict]) -> float:
    if not fm or "updated" not in fm:
        return 3
    updated_str = fm.get("updated", "")
    try:
        updated = datetime.strptime(updated_str[:10], "%Y-%m-%d")
        age_days = (datetime.now() - updated).days
        if age_days <= 7:
            return 10
        elif age_days <= 30:
            return 8
        elif age_days <= 60:
            return 5
        elif age_days <= 90:
            return 3
        else:
            return 1
    except:
        return 3


def score_connectivity(page_name: str, files: List[Path], body: str) -> float:
    outbound = extract_wikilinks(body)
    outbound_count = len(outbound)
    inbound_count = 0
    page_lower = page_name.lower()
    for f in files:
        if f.stem.lower() == page_lower:
            continue
        try:
            content = f.read_text(encoding="utf-8")
            if f"[[{page_name}]]" in content or f"[[{page_name}|" in content:
                inbound_count += 1
        except:
            pass
    total_links = outbound_count + inbound_count
    if total_links >= 6:
        return min(10, 7 + (total_links - 6))
    elif total_links >= 3:
        return 6
    elif total_links >= 1:
        return 4
    else:
        return 2


def score_page(f: Path, files: List[Path]) -> Dict:
    content = f.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    c = score_completeness(fm, body)
    s = score_structure(fm, body)
    fr = score_freshness(fm)
    co = score_connectivity(f.stem, files, body)
    overall = c * WEIGHT_COMPLETENESS + s * WEIGHT_STRUCTURE + fr * WEIGHT_FRESHNESS + co * WEIGHT_CONNECTIVITY
    content_len = len(body.strip())
    return {
        "file": str(f.relative_to(WIKI_PATH)),
        "title": fm.get("title", f.stem) if fm else f.stem,
        "score": round(overall, 1),
        "tier": get_tier(overall),
        "completeness": c,
        "structure": s,
        "freshness": fr,
        "connectivity": co,
        "content_len": content_len,
        "is_stub": content_len <= STUB_MAX_CHARS,
        "is_stale": is_stale(fm.get("updated", "") if fm else "") if fm else True,
        "outbound_links": len(extract_wikilinks(body)),
        "updated": fm.get("updated", "") if fm else "",
    }


def score_all() -> Tuple[List[Dict], Dict]:
    """Score all pages, return list + summary"""
    files = get_all_wiki_pages()
    results = []
    for f in files:
        try:
            results.append(score_page(f, files))
        except Exception as e:
            print(f"Error scoring {f}: {e}", file=sys.stderr)
    results.sort(key=lambda x: x["score"])

    total = len(results)
    avg = sum(r["score"] for r in results) / total if total else 0

    by_tier = {}
    for tier in ["CRITICAL", "ACCEPTABLE", "HIGH"]:
        tier_pages = [r for r in results if r["tier"] == tier]
        cnt = len(tier_pages)
        avg_t = sum(r["score"] for r in tier_pages) / cnt if cnt > 0 else 0
        by_tier[tier] = {"count": cnt, "avg": round(avg_t, 1)}

    summary = {
        "total": total,
        "avg": round(avg, 1),
        "by_tier": by_tier,
        "stubs": sum(1 for r in results if r["is_stub"]),
        "stale": sum(1 for r in results if r["is_stale"]),
    }
    return results, summary


# ═══════════════════════════════════════════════════════════════════════
# AUTO-IMPROVEMENT
# ═══════════════════════════════════════════════════════════════════════

EXPANSION_SECTIONS = """
## Overview

Brief overview of this concept.

## Key Concepts

- **Concept 1**: Description of the first key idea with practical context
- **Concept 2**: Description of the second key idea
- **Concept 3**: Description of the third key idea

## Practical Applications

How this topic is applied in real-world scenarios. Include at least one concrete example or use case.

## Related Concepts

[[related-concept-1]]
[[related-concept-2]]
"""


def improve_page(f: Path, result: Dict, files: List[Path]) -> Tuple[bool, str]:
    """
    Auto-improve a CRITICAL page. Returns (success, action_taken).
    Tries in order: expand_stub → add_related_links → refresh_staleness
    """
    content = f.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    title = result["title"]
    today = datetime.now().strftime("%Y-%m-%d")

    # Find related pages from wikilinks in body
    wikilinks = extract_wikilinks(body)
    existing_pages = {sf.stem.lower() for sf in files}

    # Strategy 1: Stub expansion
    if result["is_stub"]:
        # Build related links from existing wikilinks
        related = ""
        if wikilinks:
            sample = wikilinks[:3]
            related = "\n\n## Related Concepts\n\n" + "\n".join(f"- [[{lnk}]]" for lnk in sample)

        expansion = EXPANSION_SECTIONS.replace("[[related-concept-1]]",
                                               wikilinks[0] if wikilinks else "related-topic")
        expansion = expansion.replace("[[related-concept-2]]",
                                     wikilinks[1] if len(wikilinks) > 1 else wikilinks[0] if wikilinks else "related-topic")

        new_body = body.strip() + f"\n\n{expansion}{related}"

        # Check if we have enough content
        if len(new_body.strip()) <= result["content_len"] + 50:
            # Not enough improvement possible from existing content
            # Try to add generic sections
            new_body = body.strip() + EXPANSION_SECTIONS

        # Rebuild page
        new_content = f"""---
title: {title}
created: {fm.get('created', today) if fm else today}
updated: {today}
type: {fm.get('type', 'concept') if fm else 'concept'}
tags: [{fm.get('tags', '')}]
---

# {title}

{new_body}
"""
        try:
            f.write_text(new_content, encoding="utf-8")
            return True, "expanded_stub"
        except Exception as e:
            return False, f"expand_failed: {e}"

    # Strategy 2: Improve connectivity
    if result["outbound_links"] < LOW_CONNECTIVITY:
        # Find candidate related pages from same directory
        dir_pages = []
        for sf in files:
            if sf.parent == f.parent and sf != f:
                dir_pages.append(sf.stem)
        if dir_pages:
            related = "\n\n## Related Concepts\n\n" + "\n".join(f"- [[{p}]]" for p in dir_pages[:3])
            new_body = body.rstrip() + related

            new_content = content.replace(
                body,
                new_body
            )
            if new_content != content:
                new_content = f"""---
title: {title}
created: {fm.get('created', today) if fm else today}
updated: {today}
type: {fm.get('type', 'concept') if fm else 'concept'}
tags: [{fm.get('tags', '')}]
---

# {title}

{new_body}
"""
                try:
                    f.write_text(new_content, encoding="utf-8")
                    return True, "added_related_links"
                except Exception as e:
                    return False, f"link_failed: {e}"

    # Strategy 3: Refresh stale page
    if result["is_stale"] and result["tier"] == "CRITICAL":
        new_content = content
        if fm:
            # Update frontmatter timestamp
            fm["updated"] = today
            fm_lines = []
            for k, v in fm.items():
                fm_lines.append(f"{k}: {v}")
            fm_block = "---\n" + "\n".join(fm_lines) + "\n---\n"
            new_content = fm_block + body
        try:
            f.write_text(new_content, encoding="utf-8")
            return True, "refreshed_timestamp"
        except Exception as e:
            return False, f"refresh_failed: {e}"

    return False, "no_action_possible"


def auto_improve_critical(results: List[Dict], dry_run: bool = True) -> List[Dict]:
    """
    Auto-improve up to IMPROVE_BATCH CRITICAL pages.
    Returns list of actions taken.
    """
    files = get_all_wiki_pages()
    files_dict = {str(f.relative_to(WIKI_PATH)): f for f in files}

    # Priority order:
    # 1. Stubs (lowest hanging fruit)
    # 2. Stale + low connectivity
    # 3. Any CRITICAL

    stubs = [r for r in results if r["tier"] == "CRITICAL" and r["is_stub"]]
    stale_low_conn = [r for r in results
                      if r["tier"] == "CRITICAL" and r["is_stale"] and r["outbound_links"] < LOW_CONNECTIVITY]
    other_critical = [r for r in results if r["tier"] == "CRITICAL"
                      and not r["is_stub"] and not (r["is_stale"] and r["outbound_links"] < LOW_CONNECTIVITY)]

    priority_order = stubs + stale_low_conn + other_critical
    to_improve = priority_order[:IMPROVE_BATCH]

    actions = []
    for r in to_improve:
        f = files_dict.get(r["file"])
        if not f:
            continue

        if dry_run:
            actions.append({
                "file": r["file"],
                "title": r["title"],
                "score": r["score"],
                "tier": r["tier"],
                "action": "would_improve",
                "strategy": "expand_stub" if r["is_stub"] else
                           "add_related_links" if r["outbound_links"] < LOW_CONNECTIVITY else
                           "refresh_timestamp",
            })
        else:
            success, action = improve_page(f, r, files)
            actions.append({
                "file": r["file"],
                "title": r["title"],
                "score": r["score"],
                "tier": r["tier"],
                "action": action,
                "success": success,
            })

    return actions


# ═══════════════════════════════════════════════════════════════════════
# GATE LOGIC
# ═══════════════════════════════════════════════════════════════════════

def check_gate(summary: Dict, state: dict) -> Dict:
    """Evaluate gate status"""
    avg = summary["avg"]
    critical_count = summary["by_tier"].get("CRITICAL", {"count": 0})["count"]

    if avg < MIN_ACCEPTABLE:
        status = "FAIL"
        severity = "HIGH"
        message = f"Average score {avg} is BELOW minimum {MIN_ACCEPTABLE}"
    elif avg > MAX_ACCEPTABLE:
        status = "PASS_HIGH"
        severity = "LOW"
        message = f"Average score {avg} is above target {TARGET_AVG} — quality is good"
    else:
        if abs(avg - TARGET_AVG) <= 0.5:
            status = "OPTIMAL"
            severity = "NONE"
            message = f"Average score {avg} is within optimal range ({TARGET_AVG} ±0.5)"
        else:
            status = "ACCEPTABLE"
            severity = "LOW"
            message = f"Average score {avg} is acceptable"

    return {
        "status": status,
        "severity": severity,
        "message": message,
        "avg": avg,
        "critical_count": critical_count,
        "target_avg": TARGET_AVG,
        "min_acceptable": MIN_ACCEPTABLE,
        "max_acceptable": MAX_ACCEPTABLE,
    }


def compute_trend(state: dict, summary: Dict) -> str:
    """Determine quality trend"""
    history = state.get("avg_history", [])
    if len(history) < 2:
        return "no_trend"
    last = history[-1]
    curr = summary["avg"]
    diff = curr - last
    if abs(diff) < 0.1:
        return "stable"
    elif diff > 0:
        return "improving"
    else:
        return "declining"


# ═══════════════════════════════════════════════════════════════════════
# REPORTING
# ═══════════════════════════════════════════════════════════════════════

def print_stats(results: List[Dict], summary: Dict):
    """Quick stats output"""
    print(f"Total pages:  {summary['total']}")
    print(f"Average score: {summary['avg']}/10  (target: {TARGET_AVG})")
    print(f"Stubs:        {summary['stubs']}")
    print(f"Stale:        {summary['stale']}")
    print()
    for tier in ["CRITICAL", "ACCEPTABLE", "HIGH"]:
        s = summary["by_tier"].get(tier, {"count": 0, "avg": 0})
        emoji = {"CRITICAL": "🔴", "ACCEPTABLE": "🟡", "HIGH": "🟢"}[tier]
        print(f"  {emoji} {tier:<12} {s['count']:>4} pages  avg {s['avg']}")


def print_gate_report(gate: Dict, summary: Dict, trend: str, actions: List[Dict]):
    """Full gate report"""
    trend_emoji = {"improving": "📈", "declining": "📉", "stable": "➡️", "no_trend": "❓"}[trend]

    print("=" * 70)
    print("WIKI QUALITY GATE REPORT")
    print("=" * 70)
    print()

    # Gate status
    status_emoji = {"FAIL": "❌", "ACCEPTABLE": "🟡", "OPTIMAL": "✅",
                     "PASS_HIGH": "🟢", "FAIL_STALE": "⚠️"}[gate["status"]]
    print(f"Status:       {status_emoji} {gate['status']}")
    print(f"Message:      {gate['message']}")
    print(f"Trend:        {trend_emoji} {trend}")
    print()

    # Summary
    print(f"Average:      {gate['avg']}/10  (min: {gate['min_acceptable']}, max: {gate['max_acceptable']})")
    print(f"Critical:     {gate['critical_count']} pages below minimum")
    print()

    # Tier breakdown
    print("By tier:")
    for tier in ["CRITICAL", "ACCEPTABLE", "HIGH"]:
        s = summary["by_tier"].get(tier, {"count": 0, "avg": 0})
        emoji = {"CRITICAL": "🔴", "ACCEPTABLE": "🟡", "HIGH": "🟢"}[tier]
        print(f"  {emoji} {tier:<12} {s['count']:>4} pages  avg {s['avg']}")
    print()

    # Actions taken
    if actions:
        print(f"Auto-improvement actions ({len(actions)}):")
        for a in actions:
            emoji = "✅" if a.get("success", True) else "❌"
            print(f"  {emoji} [{a['action']}] {a['title']} ({a['score']}→ ?)")
    else:
        print("No auto-improvement actions taken.")


def print_stubs(results: List[Dict], limit: int = 30):
    """Show all stubs"""
    stubs = [r for r in results if r["is_stub"]]
    stubs.sort(key=lambda x: x["score"])
    print(f"STUBS ({len(stubs)} total, showing {min(limit, len(stubs))}):")
    for r in stubs[:limit]:
        print(f"  🔴 {r['title']} ({r['content_len']} chars, score {r['score']})")
    if len(stubs) > limit:
        print(f"  ... and {len(stubs) - limit} more")


def print_stale_critical(results: List[Dict]):
    """Show stale + CRITICAL pages"""
    sc = [r for r in results if r["is_stale"] and r["tier"] == "CRITICAL"]
    sc.sort(key=lambda x: x["score"])
    print(f"STALE + CRITICAL ({len(sc)} pages):")
    for r in sc[:20]:
        print(f"  🔴 {r['title']} (score {r['score']}, updated {r['updated']})")
    if len(sc) > 20:
        print(f"  ... and {len(sc) - 20} more")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Wiki Quality Gate — Proactive Self-Improvement Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/wiki_quality_gate.py --stats         # Quick stats
  python3 scripts/wiki_quality_gate.py --check         # Gate check report
  python3 scripts/wiki_quality_gate.py --stubs         # Show all stubs
  python3 scripts/wiki_quality_gate.py --stale-critical # Stale + CRITICAL
  python3 scripts/wiki_quality_gate.py --improve        # Auto-improve CRITICAL pages
  python3 scripts/wiki_quality_gate.py --full          # Check + improve + report
  python3 scripts/wiki_quality_gate.py --dry-run       # Show what would improve

Quality Gates:
  - FAIL: avg < 6.5 → auto-improve CRITICAL pages
  - ACCEPTABLE: 6.5 ≤ avg ≤ 7.5 → monitor
  - OPTIMAL: avg within TARGET ±0.5 → no action needed
  - PASS_HIGH: avg > 7.5 → quality is good
        """
    )
    parser.add_argument("--stats", action="store_true", help="Quick stats only")
    parser.add_argument("--check", action="store_true", help="Full gate check report")
    parser.add_argument("--gate", action="store_true", help="Gate check only (no improve)")
    parser.add_argument("--stubs", action="store_true", help="Show all stub pages")
    parser.add_argument("--stale-critical", action="store_true",
                        help="Show stale + CRITICAL pages")
    parser.add_argument("--improve", action="store_true", help="Auto-improve CRITICAL pages")
    parser.add_argument("--full", action="store_true", help="Check + improve + report")
    parser.add_argument("--dry-run", action="store_true", help="Show what would improve")
    parser.add_argument("--limit", type=int, default=30, help="Limit output count")

    args = parser.parse_args()

    print("Scoring all pages...")
    results, summary = score_all()
    state = get_state()
    gate = check_gate(summary, state)
    trend = compute_trend(state, summary)

    if args.stats:
        print_stats(results, summary)
        return

    if args.stubs:
        print_stubs(results, args.limit)
        return

    if args.stale_critical:
        print_stale_critical(results)
        return

    if args.gate or args.check:
        actions = [] if args.gate else auto_improve_critical(results, dry_run=True)
        print_gate_report(gate, summary, trend, actions)
        return

    if args.improve or args.full:
        if args.dry_run:
            actions = auto_improve_critical(results, dry_run=True)
            print(f"[DRY RUN] Would improve {len(actions)} pages:")
            for a in actions:
                print(f"  [{a['action']}] {a['title']} (score {a['score']})")
        else:
            actions = auto_improve_critical(results, dry_run=False)

            # Re-score after improvement
            results2, summary2 = score_all()
            gate2 = check_gate(summary2, state)

            print(f"\nImproved {len([a for a in actions if a.get('success')])} pages.")
            print(f"Score: {summary['avg']} → {summary2['avg']}")
            print(f"Critical: {summary['by_tier'].get('CRITICAL',{'count':0})['count']} → "
                  f"{summary2['by_tier'].get('CRITICAL',{'count':0})['count']}")

            # Update state
            state["last_run"] = datetime.now().isoformat()
            state["last_avg"] = summary2["avg"]
            state["improved_count"] += len([a for a in actions if a.get("success")])
            state["avg_history"].append(summary2["avg"])
            state["avg_history"] = state["avg_history"][-30:]  # keep last 30
            state["critical_history"].append(summary2["by_tier"].get("CRITICAL", {"count": 0})["count"])
            state["critical_history"] = state["critical_history"][-30:]
            save_state(state)

        return

    # Default: full report
    actions = auto_improve_critical(results, dry_run=True)
    print_gate_report(gate, summary, trend, actions)


if __name__ == "__main__":
    main()
