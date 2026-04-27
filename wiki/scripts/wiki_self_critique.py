#!/opt/homebrew/bin/python3.14
"""
Wiki Self-Critique Script v2

Quality scoring with tier gates:
- CRITICAL: score < 6.5 → auto-expand stubs, flag for human review
- ACCEPTABLE: 6.5 ≤ score ≤ 7.5 → monitor, improve when time
- HIGH QUALITY: score > 7.5 → use as reference

Scoring dimensions (heuristic, fast, cron-compatible):
1. Completeness - substantial content + structure
2. Structure - frontmatter + wikilinks + markdown elements
3. Freshness - recency of update
4. Connectivity - inbound + outbound links

Usage:
    python3 scripts/wiki_self_critique.py --all
    python3 scripts/wiki_self_critique.py --file path
    python3 scripts/wiki_self_critique.py --min-score 6.5  # only CRITICAL pages
    python3 scripts/wiki_self_critique.py --tier critical  # only CRITICAL tier
    python3 scripts/wiki_self_critique.py --tier acceptable --below  # acceptable but needs attention
    python3 scripts/wiki_self_critique.py --json
    python3 scripts/wiki_self_critique.py --expand-stubs  # auto-expand stubs
"""

import re
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
import argparse

# ═══════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
DAYS_STALE_THRESHOLD = 30
MIN_CONTENT_LENGTH = 100

# Quality gates
MIN_ACCEPTABLE_SCORE = 6.5
MAX_ACCEPTABLE_SCORE = 7.5

# Scoring weights (must sum to 1.0)
WEIGHT_COMPLETENESS = 0.35
WEIGHT_STRUCTURE = 0.25
WEIGHT_FRESHNESS = 0.20
WEIGHT_CONNECTIVITY = 0.20

# Stub expansion thresholds
STUB_MAX_CHARS = 500
STUB_MIN_HEADINGS = 2
EXPAND_MIN_SCORE = 6.5  # expand stubs below this

# ═══════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════

def get_all_wiki_pages(path: Path) -> List[Path]:
    """Get all .md files, excluding raw/, _archive/, .obsidian/, _templates/"""
    SKIP_DIRS = {"raw", "_archive", ".obsidian", "__pycache__", "_templates",
                 "node_modules", ".git"}
    files = []
    for f in path.rglob("*.md"):
        if any(x in f.parts for x in SKIP_DIRS):
            continue
        files.append(f)
    return files


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    """Parse YAML frontmatter. Returns (fm_dict, body)"""
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
    """Extract all [[wikilinks]] from content"""
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)


def count_headings(content: str) -> int:
    """Count # headings in content"""
    return len(re.findall(r'^#+ .+$', content, re.MULTILINE))


def is_stale(updated_str: str, days: int = DAYS_STALE_THRESHOLD) -> bool:
    """Check if page is stale (>N days since update)"""
    if not updated_str:
        return True
    try:
        updated = datetime.strptime(updated_str[:10], "%Y-%m-%d")
        return (datetime.now() - updated).days > days
    except:
        return False


def get_tier(score: float) -> str:
    """Classify score into quality tier"""
    if score < MIN_ACCEPTABLE_SCORE:
        return "CRITICAL"
    elif score <= MAX_ACCEPTABLE_SCORE:
        return "ACCEPTABLE"
    else:
        return "HIGH"


def get_tier_emoji(tier: str) -> str:
    return {"CRITICAL": "🔴", "ACCEPTABLE": "🟡", "HIGH": "🟢"}.get(tier, "⚪")


def get_tier_advice(tier: str) -> str:
    return {
        "CRITICAL": "Auto-expand stub OR flag for human review",
        "ACCEPTABLE": "Monitor, improve when time permits",
        "HIGH": "Use as quality reference, link heavily",
    }.get(tier, "")


# ═══════════════════════════════════════════════════════════════════════
# DIMENSION SCORING
# ═══════════════════════════════════════════════════════════════════════

def score_completeness(fm: Optional[dict], body: str) -> Tuple[float, str]:
    """Score 1-10 based on content completeness"""
    score = 0
    reasons = []

    content_len = len(body.strip())
    if content_len > 2000:
        score += 3
        reasons.append(f"substantial ({content_len} chars)")
    elif content_len > 500:
        score += 2
        reasons.append(f"good ({content_len} chars)")
    elif content_len > MIN_CONTENT_LENGTH:
        score += 1
        reasons.append(f"minimal ({content_len} chars)")
    else:
        reasons.append(f"stub ({content_len} chars)")

    heading_count = count_headings(body)
    if heading_count >= 4:
        score += 2
        reasons.append(f"well-structured ({heading_count} headings)")
    elif heading_count >= 2:
        score += 1
        reasons.append(f"has structure ({heading_count} headings)")

    if fm:
        required = ["title", "updated", "type", "tags"]
        fm_fields = sum(1 for f in required if f in fm and fm[f])
        score += fm_fields * 0.5
        if fm_fields == 4:
            reasons.append("complete frontmatter")

    score = min(10, score)
    return score, ", ".join(reasons) if reasons else "no content"


def score_structure(fm: Optional[dict], body: str) -> Tuple[float, str]:
    """Score 1-10 based on structure"""
    score = 0
    reasons = []

    if fm:
        score += 2
        reasons.append("has frontmatter")

    wikilinks = extract_wikilinks(body)
    link_count = len(wikilinks)
    if link_count >= 3:
        score += 3
        reasons.append(f"well-linked ({link_count} links)")
    elif link_count >= 1:
        score += 2
        reasons.append(f"has links ({link_count})")
    else:
        reasons.append("no wikilinks")

    if re.search(r'^[*\-] |^\d+\. ', body, re.MULTILINE):
        score += 1
        reasons.append("has lists")
    if "|" in body and "-" in body:
        score += 1
        reasons.append("has tables")
    if "```" in body:
        score += 1
        reasons.append("has code blocks")
    if re.match(r'^# .+$', body, re.MULTILINE):
        score += 1
        reasons.append("proper H1 title")

    score = min(10, score)
    return score, ", ".join(reasons) if reasons else "poor structure"


def score_freshness(fm: Optional[dict]) -> Tuple[float, str]:
    """Score 1-10 based on freshness"""
    if not fm or "updated" not in fm:
        return 3, "no update date"

    updated_str = fm.get("updated", "")
    try:
        updated = datetime.strptime(updated_str[:10], "%Y-%m-%d")
        age_days = (datetime.now() - updated).days

        if age_days <= 7:
            return 10, f"fresh ({age_days}d)"
        elif age_days <= 30:
            return 8, f"recent ({age_days}d)"
        elif age_days <= 60:
            return 5, f"aging ({age_days}d)"
        elif age_days <= 90:
            return 3, f"stale ({age_days}d)"
        else:
            return 1, f"very stale ({age_days}d)"
    except:
        return 3, "invalid date format"


def score_connectivity(page_name: str, files: List[Path], body: str) -> Tuple[float, str]:
    """Score 1-10 based on connectivity"""
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
        score = min(10, 7 + (total_links - 6))
        reason = f"highly connected ({outbound_count} out, {inbound_count} in)"
    elif total_links >= 3:
        score = 6
        reason = f"connected ({outbound_count} out, {inbound_count} in)"
    elif total_links >= 1:
        score = 4
        reason = f"weak ({outbound_count} out, {inbound_count} in)"
    else:
        score = 2
        reason = "isolated (no links)"

    return score, reason


def evaluate_page(f: Path, files: List[Path]) -> Dict:
    """Evaluate a single page and return all scores"""
    content = f.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    c_score, c_reason = score_completeness(fm, body)
    s_score, s_reason = score_structure(fm, body)
    f_score, f_reason = score_freshness(fm)

    page_name = f.stem
    con_score, con_reason = score_connectivity(page_name, files, body)

    overall = (
        c_score * WEIGHT_COMPLETENESS +
        s_score * WEIGHT_STRUCTURE +
        f_score * WEIGHT_FRESHNESS +
        con_score * WEIGHT_CONNECTIVITY
    )

    overall = round(overall, 1)
    tier = get_tier(overall)
    content_len = len(body.strip())

    return {
        "file": str(f.relative_to(WIKI_PATH)),
        "title": fm.get("title", page_name) if fm else page_name,
        "overall_score": overall,
        "tier": tier,
        "tier_emoji": get_tier_emoji(tier),
        "completeness": {"score": c_score, "reason": c_reason},
        "structure": {"score": s_score, "reason": s_reason},
        "freshness": {"score": f_score, "reason": f_reason},
        "connectivity": {"score": con_score, "reason": con_reason},
        "is_stale": is_stale(fm.get("updated", "")) if fm else True,
        "content_len": content_len,
        "is_stub": content_len <= STUB_MAX_CHARS,
        "updated": fm.get("updated", "") if fm else "",
    }


# ═══════════════════════════════════════════════════════════════════════
# STUB EXPANSION
# ═══════════════════════════════════════════════════════════════════════

EXPANSION_TEMPLATE = """
## Overview

Brief introduction to {title}.

## Key Concepts

- Concept 1: Description of the first key idea
- Concept 2: Description of the second key idea
- Concept 3: Description of the third key idea

## Practical Applications

How this topic is applied in real-world scenarios.

## Related Topics

[[related-concept-1]]
[[related-concept-2]]
"""


def is_stub_needing_expansion(result: Dict) -> bool:
    """Check if a page is a stub that needs auto-expansion"""
    if result["tier"] != "CRITICAL":
        return False
    if not result["is_stub"]:
        return False
    # Only auto-expand very short stubs that are CRITICAL
    return result["content_len"] <= STUB_MAX_CHARS


def expand_stub(f: Path, result: Dict) -> bool:
    """Auto-expand a stub page. Returns True if expanded."""
    content = f.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    title = result["title"]
    today = datetime.now().strftime("%Y-%m-%d")

    # Build related links suggestion
    wikilinks = extract_wikilinks(body)
    related = ""
    if wikilinks:
        sample_links = wikilinks[:3]
        related = "\n".join(f"- [[{lnk}]]" for lnk in sample_links)

    expansion = EXPANSION_TEMPLATE.format(
        title=title,
        related=related,
    )

    # Check if page already has more than minimal content
    if len(body.strip()) > STUB_MAX_CHARS:
        return False  # Already expanded

    new_body = body.strip() + f"\n\n{expansion}"

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
        return True
    except Exception as e:
        print(f"  ERROR expanding {f.name}: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════
# REPORTING
# ═══════════════════════════════════════════════════════════════════════

def print_report(results: List[Dict], args: argparse.Namespace):
    """Print quality report"""
    if args.json:
        out = {
            "summary": compute_summary(results),
            "pages": results,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print("=" * 80)
    print("WIKI SELF-CRITIQUE REPORT")
    print("=" * 80)
    print()

    summary = compute_summary(results)

    # Tier summary
    print(f"{'Tier':<15} {'Count':>6} {'Avg Score':>10} {'Action'}")
    print("-" * 80)
    for tier in ["CRITICAL", "ACCEPTABLE", "HIGH"]:
        stats = summary["by_tier"].get(tier, {"count": 0, "avg": 0})
        emoji = get_tier_emoji(tier)
        advice = get_tier_advice(tier)
        print(f"{emoji} {tier:<12} {stats['count']:>6} {stats['avg']:>10.1f}  {advice}")

    print()
    print(f"Total pages:     {summary['total']}")
    print(f"Average score:   {summary['avg_score']:.1f}/10")
    print(f"Wiki health:     {'✅ PASS' if summary['avg_score'] >= MIN_ACCEPTABLE_SCORE else '❌ FAIL'} "
          f"(target: {MIN_ACCEPTABLE_SCORE}-{MAX_ACCEPTABLE_SCORE})")
    print()

    # Gate status
    critical = summary["by_tier"].get("CRITICAL", {"count": 0})["count"]
    if critical > 0:
        print(f"⚠️  {critical} pages below minimum score ({MIN_ACCEPTABLE_SCORE}) — needs attention")
    print()

    # Filter and sort
    display = list(results)
    if args.tier:
        display = [r for r in display if r["tier"].upper() == args.tier.upper()]

    if args.below:
        display = [r for r in display if r["overall_score"] < MAX_ACCEPTABLE_SCORE]

    if args.min_score is not None:
        display = [r for r in display if r["overall_score"] >= args.min_score]

    # Sort by score ascending (worst first)
    display.sort(key=lambda x: x["overall_score"])

    count = min(args.top, len(display))
    if count == 0:
        print("No pages match the filter criteria.")
        return

    print("-" * 80)
    tier_mode = args.tier.upper() if args.tier else "CRITICAL"
    print(f"PAGES NEEDING ATTENTION (sorted by score, {count}/{len(display)} shown)")
    print("-" * 80)

    for r in display[:count]:
        emoji = r["tier_emoji"]
        score = r["overall_score"]
        stale = " ⚠️ STALE" if r["is_stale"] else ""
        stub = " 📄 STUB" if r["is_stub"] else ""
        print(f"\n{emoji} {r['title']}")
        print(f"   File:     {r['file']}")
        print(f"   Score:    {score}/10 [{r['tier']}]{stale}{stub}")

        # Show weakest dimension
        scores = {
            "completeness": r["completeness"]["score"],
            "structure": r["structure"]["score"],
            "freshness": r["freshness"]["score"],
            "connectivity": r["connectivity"]["score"],
        }
        weakest = min(scores, key=scores.get)
        print(f"   Weakest:  {weakest} ({scores[weakest]:.0f}/10) — {r[weakest]['reason']}")

    # Excellent pages
    print()
    print("-" * 80)
    print("HIGH QUALITY PAGES (score > 7.5)")
    print("-" * 80)
    high = [r for r in results if r["tier"] == "HIGH"]
    high.sort(key=lambda x: x["overall_score"], reverse=True)
    for r in high[:10]:
        print(f"  🟢 {r['title']} ({r['overall_score']}/10)")
    if len(high) > 10:
        print(f"  ... and {len(high) - 10} more")


def compute_summary(results: List[Dict]) -> Dict:
    """Compute summary statistics"""
    total = len(results)
    if total == 0:
        return {"total": 0, "avg_score": 0, "by_tier": {}}

    avg_score = sum(r["overall_score"] for r in results) / total

    by_tier = {}
    for tier in ["CRITICAL", "ACCEPTABLE", "HIGH"]:
        tier_pages = [r for r in results if r["tier"] == tier]
        count = len(tier_pages)
        avg = sum(r["overall_score"] for r in tier_pages) / count if count > 0 else 0
        by_tier[tier] = {"count": count, "avg": round(avg, 1)}

    stubs = sum(1 for r in results if r["is_stub"])
    stale = sum(1 for r in results if r["is_stale"])

    return {
        "total": total,
        "avg_score": round(avg_score, 1),
        "by_tier": by_tier,
        "stubs": stubs,
        "stale": stale,
    }


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Wiki Self-Critique v2 — Quality scoring with tier gates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/wiki_self_critique.py --all
  python3 scripts/wiki_self_critique.py --min-score 6.5     # only CRITICAL pages
  python3 scripts/wiki_self_critique.py --tier critical     # same as above
  python3 scripts/wiki_self_critique.py --tier acceptable --below  # acceptable but needs work
  python3 scripts/wiki_self_critique.py --expand-stubs      # auto-expand CRITICAL stubs
  python3 scripts/wiki_self_critique.py --json              # machine-readable output
  python3 scripts/wiki_self_critique.py --file concepts/ai-agent.md

Quality Gates:
  CRITICAL  : score < 6.5  → auto-expand stubs, flag for human review
  ACCEPTABLE: 6.5 ≤ s ≤ 7.5 → monitor, improve when time permits
  HIGH      : score > 7.5  → use as reference, link heavily
        """
    )
    parser.add_argument("--all", action="store_true", help="Critique all pages")
    parser.add_argument("--file", type=str, help="Critique specific file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--top", type=int, default=15, help="Show top N issues (default 15)")
    parser.add_argument("--min-score", type=float, dest="min_score",
                        help=f"Show only pages with score >= N (e.g. 6.5)")
    parser.add_argument("--tier", type=str,
                        help="Filter by tier: CRITICAL, ACCEPTABLE, or HIGH")
    parser.add_argument("--below", action="store_true",
                        help="When used with --tier: show pages BELOW that tier's max")
    parser.add_argument("--expand-stubs", action="store_true", dest="expand_stubs",
                        help="Auto-expand CRITICAL stub pages")
    parser.add_argument("--stubs-only", action="store_true", dest="stubs_only",
                        help="Only show stub pages")
    parser.add_argument("--stale-only", action="store_true", dest="stale_only",
                        help="Only show stale pages")
    parser.add_argument("--summary", action="store_true", help="Show only summary, no details")

    args = parser.parse_args()

    files = get_all_wiki_pages(WIKI_PATH)

    # Get target files
    if args.file:
        target = WIKI_PATH / args.file
        if target.exists():
            results = [evaluate_page(target, files)]
        else:
            print(f"File not found: {args.file}")
            return
    else:
        results = [evaluate_page(f, files) for f in files]

    # Apply filters
    if args.stubs_only:
        results = [r for r in results if r["is_stub"]]
    if args.stale_only:
        results = [r for r in results if r["is_stale"]]

    # Auto-expand stubs if requested
    if args.expand_stubs:
        print("=" * 80)
        print("AUTO-EXPANDING CRITICAL STUBS")
        print("=" * 80)
        print()
        expanded = 0
        for r in results:
            if r["tier"] == "CRITICAL" and r["is_stub"]:
                f = WIKI_PATH / r["file"]
                print(f"  Expanding: {r['title']} ({r['content_len']} chars)...")
                if expand_stub(f, r):
                    expanded += 1
                    print(f"    ✅ Expanded — re-scoring...")
                    # Re-score
                    new_result = evaluate_page(f, files)
                    print(f"    New score: {new_result['overall_score']}/10 [{new_result['tier']}]")
                else:
                    print(f"    ❌ Failed")
        print()
        print(f"Expanded {expanded} stubs.")
        print()

        # Re-evaluate all pages
        results = [evaluate_page(f, files) for f in files]

    if args.summary:
        summary = compute_summary(results)
        print(f"Total: {summary['total']} | Avg: {summary['avg_score']:.1f} | "
              f"CRITICAL: {summary['by_tier'].get('CRITICAL',{'count':0})['count']} | "
              f"Stubs: {summary.get('stubs',0)} | Stale: {summary.get('stale',0)}")
        return

    print_report(results, args)


if __name__ == "__main__":
    main()
