#!/opt/homebrew/bin/python3.14
"""
Wiki Self-Evolution Agent
Orchestrates the full self-evolution cycle:
1. Gap Analysis — what should exist but doesn't?
2. Content Generation — create new pages for high-priority gaps
3. Self-Critique — score all pages, flag low-quality ones
4. Staleness Detection — find and refresh old content
5. Duplicate Detection — find and merge redundant pages
6. Checkpoint — record what was done

Usage:
    python3 scripts/wiki_self_evolution_agent.py [--dry-run] [--min-gap-score N]
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WIKI_DIR = Path("/Volumes/Storage-1/Hermes/wiki")
REPORT_FILE = WIKI_DIR / "scripts" / "self_evolution_report.json"
LOG_FILE = WIKI_DIR / "scripts" / "self_evolution.log"


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def run_script(script_name: str, args: list = None) -> dict:
    """Run a wiki script and return parsed output."""
    cmd = ["python3", str(WIKI_DIR / "scripts" / script_name)]
    if args:
        cmd.extend(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=str(WIKI_DIR))
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def step_gap_analysis(min_score: float = 8.0, priority_weighted: bool = False) -> dict:
    """Find missing topics."""
    log("STEP: Gap Analysis")
    
    if priority_weighted:
        # Use priority-weighted gap analyzer
        result = run_script("priority_gap_analyzer.py", ["--threshold", "10"])
        gaps = []
        if result["success"]:
            output = result["stdout"]
            import re
            # Parse priority gaps
            for line in output.split("\n"):
                m = re.match(r"\s*\d+\.\s+(\S+)\s+([\d.]+)\s+(\d+)\s+(\d+)", line)
                if m:
                    gaps.append({
                        "topic": m.group(1),
                        "score": float(m.group(2)),
                        "user_interest": int(m.group(3)),
                        "connections": int(m.group(4))
                    })
        log(f"  Found {len(gaps)} priority gaps (weighted by user interest)")
        return {"gaps": gaps, "raw": result.get("stdout", "") if result["success"] else "", "priority": True}
    else:
        # Use standard gap analyzer
        result = run_script("wiki_gap_analyzer.py", ["--min-score", str(min_score)])
        gaps = []
        if result["success"]:
            output = result["stdout"]
            for line in output.split("\n"):
                if line.strip().startswith("[["):
                    import re
                    m = re.match(r"\s+\[\[([^\]]+)\]\]\s+\(score:\s+([\d.]+)\)", line)
                    if m:
                        gaps.append({"topic": m.group(1), "score": float(m.group(2))})
        log(f"  Found {len(gaps)} gaps")
        return {"gaps": gaps, "raw": result.get("stdout", "") if result["success"] else "", "priority": False}


def step_auto_improve(min_gap_score: float = 8.0) -> dict:
    """Generate content for high-priority gaps."""
    log("STEP: Auto-Improve (Content Generation)")
    result = run_script("wiki_auto_improve.py", ["--min-score", str(min_gap_score)])
    created = []
    if result["success"]:
        output = result["stdout"]
        for line in output.split("\n"):
            if "Created:" in line:
                created.append(line.strip())
        log(f"  Created {len(created)} new pages")
        return {"created": created, "raw": output}
    return {"created": [], "error": result.get("stderr", "unknown")}


def step_self_critique() -> dict:
    """Score all pages."""
    log("STEP: Self-Critique")
    result = run_script("wiki_self_critique.py", ["--json"])
    scores = []
    low_quality = []
    if result["success"]:
        try:
            data = json.loads(result["stdout"])
            # Handle both list format and dict format
            pages = data if isinstance(data, list) else data.get("pages", [])
            for page in pages:
                total = page.get("overall_score", 0) or page.get("total_score", 0)
                scores.append(total)
                if total < 6:
                    low_quality.append(page.get("file", "unknown"))
        except (json.JSONDecodeError, KeyError) as e:
            pass
    avg = sum(scores) / len(scores) if scores else 0
    log(f"  Average score: {avg:.1f}/10, {len(low_quality)} low-quality pages")
    return {"avg_score": avg, "low_quality": low_quality, "raw": result.get("stdout", "")}


def step_freshness() -> dict:
    """Find stale pages."""
    log("STEP: Freshness Check")
    result = run_script("freshness_score.py", ["--stale-only"])
    stale = []
    if result["success"]:
        for line in result["stdout"].split("\n"):
            if "Stale" in line or "[[" in line:
                stale.append(line.strip())
    log(f"  Found {len(stale)} stale pages")
    return {"stale": stale}


def step_duplicate() -> dict:
    """Find duplicate pages."""
    log("STEP: Duplicate Detection")
    result = run_script("duplicate_detector.py", ["--find-merges"])
    duplicates = []
    if result["success"]:
        output = result["stdout"]
        import re
        for m in re.finditer(r"(\S+)\s+↔\s+(\S+)\s+\(([\d.]+)%\)", output):
            duplicates.append({
                "page1": m.group(1),
                "page2": m.group(2),
                "similarity": float(m.group(3))
            })
    log(f"  Found {len(duplicates)} potential duplicates")
    return {"duplicates": duplicates}


def build_report(phases: dict) -> dict:
    """Build evolution report."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "phases": phases,
        "summary": {
            "gaps_found": len(phases["gap_analysis"].get("gaps", [])),
            "pages_created": len(phases["auto_improve"].get("created", [])),
            "avg_quality": phases["self_critique"].get("avg_score", 0),
            "low_quality_pages": len(phases["self_critique"].get("low_quality", [])),
            "stale_pages": len(phases["freshness"].get("stale", [])),
            "duplicates": len(phases["duplicate"].get("duplicates", []))
        },
        "recommendations": []
    }

    # Generate recommendations
    if report["summary"]["low_quality_pages"] > 0:
        report["recommendations"].append({
            "priority": "high",
            "action": "refresh_pages",
            "pages": phases["self_critique"]["low_quality"]
        })
    if report["summary"]["stale_pages"] > 3:
        report["recommendations"].append({
            "priority": "medium",
            "action": "update_stale_pages"
        })
    if report["summary"]["duplicates"] > 0:
        report["recommendations"].append({
            "priority": "medium",
            "action": "merge_duplicates",
            "pairs": phases["duplicate"]["duplicates"]
        })
    if report["summary"]["gaps_found"] > 0 and report["summary"]["pages_created"] == 0:
        report["recommendations"].append({
            "priority": "medium",
            "action": "check_lm_studio_connection"
        })

    return report


def main():
    dry_run = "--dry-run" in sys.argv
    priority_weighted = "--priority-weighted" in sys.argv
    min_gap_score = 8.0

    for arg in sys.argv[1:]:
        if arg.startswith("--min-gap-score="):
            min_gap_score = float(arg.split("=")[1])

    log("=" * 60)
    log("WIKI SELF-EVOLUTION CYCLE STARTED")
    if priority_weighted:
        log("  Mode: PRIORITY-WEIGHTED (by user interest)")
    log("=" * 60)

    phases = {}

    # Phase 1: Gap Analysis
    phases["gap_analysis"] = step_gap_analysis(min_gap_score, priority_weighted)

    # Phase 2: Auto-Improve (only if not dry run)
    if dry_run:
        log("DRY RUN — skipping content generation")
        phases["auto_improve"] = {"created": []}
    else:
        phases["auto_improve"] = step_auto_improve(min_gap_score)

    # Phase 3: Self-Critique
    phases["self_critique"] = step_self_critique()

    # Phase 4: Freshness
    phases["freshness"] = step_freshness()

    # Phase 5: Duplicate Detection
    phases["duplicate"] = step_duplicate()

    # Build and save report
    report = build_report(phases)
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    log("=" * 60)
    log("SELF-EVOLUTION CYCLE COMPLETE")
    log(f"  Gaps found: {report['summary']['gaps_found']}")
    log(f"  Pages created: {report['summary']['pages_created']}")
    log(f"  Avg quality: {report['summary']['avg_quality']:.1f}/10")
    log(f"  Low quality pages: {report['summary']['low_quality_pages']}")
    log(f"  Stale pages: {report['summary']['stale_pages']}")
    log(f"  Duplicates: {report['summary']['duplicates']}")
    log(f"  Report saved to: {REPORT_FILE}")
    log("=" * 60)

    if report["recommendations"]:
        log("RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            log(f"  [{rec['priority']}] {rec['action']}")

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
