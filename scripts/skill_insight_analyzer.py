#!/usr/bin/env python3
"""
skill_insight_analyzer.py — Self-improvement engine for Hermes skills.

Garry Tan: "The system will improve itself as skills compound."
This script analyzes _usage_log.jsonl to find:
  1. Missing skills — tasks with no good recommendation match
  2. Weak skills — selected but consistently poor outcomes
  3. Over-recommended skills — frequently recommended but never selected
  4. Workflow gaps — repeated task patterns without proper skill coverage
  5. trigger_conditions improvements — suggestions to sharpen skill metadata

Run: python3 skill_insight_analyzer.py [--min-entries 5] [--json]
"""

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# ─── Paths ────────────────────────────────────────────────────────────────────

def _get_skills_dir() -> Path:
    return Path.home() / ".hermes" / "skills"

SKILLS_DIR = _get_skills_dir()
USAGE_LOG = SKILLS_DIR / "_usage_log.jsonl"
INDEX_PATH = SKILLS_DIR / "_index.json"
SKINS_DIR = Path.home() / ".hermes" / "skins"

# ─── Log Parsing ─────────────────────────────────────────────────────────────

def load_usage_log(min_entries: int = 0) -> list[dict]:
    """Load all entries from usage log."""
    if not USAGE_LOG.exists():
        return []
    entries = []
    with open(USAGE_LOG, encoding="utf-8") as f:
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    # Filter by min_entries if specified
    if min_entries > 0 and len(entries) < min_entries:
        print(f"⚠️  Only {len(entries)} entries in log (need {min_entries} for meaningful analysis).")
        print(f"   Run skill_recommend a few more times first, then re-run this analyzer.")
    return entries

def load_skill_index() -> dict:
    """Load the skill index."""
    if not INDEX_PATH.exists():
        return {}
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))

# ─── Analysis Modules ─────────────────────────────────────────────────────────

def analyze_missing_skills(entries: list[dict]) -> list[dict]:
    """
    Find tasks where:
    - No skill was recommended with score > 5 (weak match)
    - OR no skill was selected (no_match outcome)
    These represent gaps where new skills should exist.
    """
    gaps = []
    for entry in entries:
        recs = entry.get("recommended_skills", [])
        top_score = recs[0]["score"] if recs else 0
        selected = entry.get("selected_skill")
        outcome = entry.get("outcome", "unknown")

        if not selected or outcome == "no_match":
            gaps.append({
                "task": entry["task"],
                "task_hash": entry["task_hash"],
                "top_score": top_score,
                "top_skill": recs[0]["name"] if recs else None,
                "outcome": outcome,
                "timestamp": entry["timestamp"],
            })
    return gaps

def analyze_skill_effectiveness(entries: list[dict], skill_index: dict) -> list[dict]:
    """
    For each skill that was actually selected, track outcomes.
    Skills with low success rates need trigger_conditions improvements.
    """
    skill_stats: dict[str, dict] = defaultdict(lambda: {
        "selected": 0, "success": 0, "partial": 0, "failed": 0, "unknown": 0,
        "avg_top_score": 0, "total_top_score": 0
    })

    for entry in entries:
        selected = entry.get("selected_skill")
        outcome = entry.get("outcome", "unknown")
        top_score = entry.get("recommended_skills", [{}])[0].get("score", 0) if entry.get("recommended_skills") else 0
        if selected:
            stats = skill_stats[selected]
            stats["selected"] += 1
            stats["total_top_score"] += top_score
            if outcome in ("success", "partial", "failed", "unknown"):
                stats[outcome] += 1

    effectiveness = []
    for name, stats in sorted(skill_stats.items(), key=lambda x: x[1]["selected"], reverse=True):
        if stats["selected"] < 2:
            continue  # Need minimum sample size
        stats["avg_top_score"] = round(stats["total_top_score"] / stats["selected"], 1)
        success_rate = stats["success"] / stats["selected"]
        # Flag if success rate is low despite high avg score (bad trigger_conditions)
        stats["success_rate"] = round(success_rate * 100, 1)
        stats["name"] = name
        # Skill quality: high score but low success = needs better trigger_conditions
        if stats["avg_top_score"] > 10 and success_rate < 0.5:
            stats["flag"] = "weak_trigger"
        elif success_rate < 0.3:
            stats["flag"] = "low_success"
        else:
            stats["flag"] = "ok"
        effectiveness.append(stats)

    return effectiveness

def analyze_over_recommended(entries: list[dict]) -> list[dict]:
    """
    Skills that are recommended frequently but rarely selected.
    This means the trigger_conditions/use_case_keywords are too broad.
    """
    recommended_counter = Counter()
    selected_counter = Counter()

    for entry in entries:
        for rec in entry.get("recommended_skills", [])[:3]:  # top-3
            recommended_counter[rec["name"]] += 1
        if entry.get("selected_skill"):
            selected_counter[entry["selected_skill"]] += 1

    over_recommended = []
    for skill_name, rec_count in recommended_counter.most_common(20):
        sel_count = selected_counter.get(skill_name, 0)
        if rec_count >= 3 and sel_count == 0:
            over_recommended.append({
                "skill": skill_name,
                "recommended_count": rec_count,
                "selected_count": sel_count,
                "selection_rate": 0.0,
                "issue": "Never selected despite top-3 recommendation",
            })
        elif rec_count >= 5 and sel_count / rec_count < 0.2:
            over_recommended.append({
                "skill": skill_name,
                "recommended_count": rec_count,
                "selected_count": sel_count,
                "selection_rate": round(sel_count / rec_count * 100, 1),
                "issue": f"Only {sel_count}/{rec_count} selected ({round(sel_count/rec_count*100)}%)",
            })
    return over_recommended

def analyze_workflow_patterns(entries: list[dict]) -> list[dict]:
    """
    Detect task_hash repetitions — same task done multiple times.
    If repeated > 3x without good outcome, suggests automation opportunity.
    """
    task_runs: dict[str, list] = defaultdict(list)
    for entry in entries:
        task_runs[entry["task_hash"]].append(entry)

    patterns = []
    for task_hash, runs in sorted(task_runs.items(), key=lambda x: len(x[1]), reverse=True):
        if len(runs) < 2:
            continue
        outcomes = [r.get("outcome", "unknown") for r in runs]
        success_count = outcomes.count("success")
        latest = runs[-1]
        patterns.append({
            "task_hash": task_hash,
            "task": runs[0]["task"][:100],
            "repeat_count": len(runs),
            "success_count": success_count,
            "success_rate": round(success_count / len(runs) * 100, 1),
            "last_outcome": latest.get("outcome"),
            "last_timestamp": latest["timestamp"],
            "opportunity": "workflow_automation" if len(runs) >= 3 and success_count < len(runs) * 0.5 else None,
        })
    return patterns

def analyze_trigger_gaps(entries: list[dict], skill_index: dict) -> list[dict]:
    """
    For tasks with low match scores, extract key phrases that could become
    new trigger_conditions for existing skills or new skills entirely.
    """
    skill_map = {s["name"]: s for s in skill_index.get("skills", [])}
    gaps = analyze_missing_skills(entries)

    suggestions = []
    for gap in gaps[:20]:  # Top 20 gaps
        task = gap["task"]
        # Extract meaningful keywords from task
        words = re.findall(r"[a-z0-9]{3,}", task.lower())
        significant = [w for w in words if w not in {
            "what", "how", "when", "where", "why", "make", "build",
            "create", "fix", "update", "add", "remove", "delete",
            "task", "use", "using", "need", "want", "get", "got",
        }]
        if significant:
            suggestions.append({
                "task": task[:150],
                "task_hash": gap["task_hash"],
                "key_phrases": significant[:5],
                "current_best_skill": gap["top_skill"],
                "current_best_score": gap["top_score"],
                "suggestion": f"Consider adding trigger_conditions matching: {', '.join(significant[:5])}",
            })
    return suggestions

# ─── Report Generation ─────────────────────────────────────────────────────────

def generate_report(entries: list[dict], args) -> dict:
    """Generate full self-improvement report."""
    skill_index = load_skill_index()

    missing = analyze_missing_skills(entries)
    effectiveness = analyze_skill_effectiveness(entries, skill_index)
    over_rec = analyze_over_recommended(entries)
    patterns = analyze_workflow_patterns(entries)
    trigger_gaps = analyze_trigger_gaps(entries, skill_index)

    # Summary stats
    total_entries = len(entries)
    tasks_with_match = sum(1 for e in entries if e.get("selected_skill"))
    tasks_no_match = sum(1 for e in entries if not e.get("selected_skill") or e.get("outcome") == "no_match")
    skills_used = len(set(e.get("selected_skill") for e in entries if e.get("selected_skill")))

    # Actionable items
    actions = []

    # Critical: missing skills
    if missing:
        actions.append({
            "priority": "high",
            "type": "new_skill_needed",
            "count": len(missing),
            "description": f"{len(missing)} tasks had no matching skill",
            "examples": [m["task"][:80] for m in missing[:3]],
        })

    # Weak trigger_conditions
    weak = [s for s in effectiveness if s.get("flag") == "weak_trigger"]
    if weak:
        actions.append({
            "priority": "medium",
            "type": "improve_trigger_conditions",
            "count": len(weak),
            "description": f"{len(weak)} skills recommended often but rarely succeed",
            "skills": [s["name"] for s in weak[:5]],
        })

    # Over-recommended
    if over_rec:
        actions.append({
            "priority": "low",
            "type": "sharpen_keywords",
            "count": len(over_rec),
            "description": f"{len(over_rec)} skills too broad — getting recommended for wrong tasks",
            "skills": [o["skill"] for o in over_rec[:5]],
        })

    # Workflow automation
    automatable = [p for p in patterns if p.get("opportunity") == "workflow_automation"]
    if automatable:
        actions.append({
            "priority": "medium",
            "type": "workflow_automation",
            "count": len(automatable),
            "description": f"{len(automatable)} repeated tasks with low success — candidates for automation",
            "examples": [p["task"][:80] for p in automatable[:3]],
        })

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_entries": total_entries,
        "tasks_with_match": tasks_with_match,
        "tasks_no_match": tasks_no_match,
        "match_rate": round(tasks_with_match / total_entries * 100, 1) if total_entries else 0,
        "unique_skills_used": skills_used,
        "actions": actions,
        "missing_skills": missing[:10],
        "skill_effectiveness": effectiveness[:15],
        "over_recommended": over_rec[:10],
        "workflow_patterns": patterns[:10],
        "trigger_gap_suggestions": trigger_gaps[:10],
    }

    return report

def print_report(report: dict) -> None:
    """Pretty-print the report to console."""
    print("\n" + "=" * 60)
    print("  HERMES SKILL SELF-IMPROVEMENT REPORT")
    print("=" * 60)
    print(f"\n📊 OVERVIEW")
    print(f"   Total entries:     {report['total_entries']}")
    print(f"   Match rate:        {report['match_rate']}%")
    print(f"   Skills used:       {report['unique_skills_used']}")

    print(f"\n📋 ACTION ITEMS ({len(report['actions'])})")
    for action in report["actions"]:
        emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(action["priority"], "⚪")
        print(f"\n   {emoji} [{action['priority'].upper()}] {action['description']}")
        if "examples" in action:
            for ex in action["examples"][:2]:
                print(f"      → {ex}")
        if "skills" in action:
            print(f"      → {', '.join(action['skills'][:3])}")

    # Missing skills
    if report["missing_skills"]:
        print(f"\n⚠️  MISSING SKILLS ({len(report['missing_skills'])} tasks with no good match)")
        for m in report["missing_skills"][:5]:
            score_str = f"(score {m['top_score']})" if m['top_score'] > 0 else "(no match)"
            print(f"   • {m['task'][:70]}... {score_str}")

    # Skill effectiveness
    weak = [s for s in report["skill_effectiveness"] if s.get("flag") != "ok"]
    if weak:
        print(f"\n📉 SKILLS NEEDING IMPROVEMENT")
        for s in weak[:5]:
            print(f"   • {s['name']}: {s['selected']} uses, {s['success_rate']}% success, flag={s['flag']}")

    # Workflow patterns
    auto = [p for p in report["workflow_patterns"] if p.get("opportunity")]
    if auto:
        print(f"\n🔄 WORKFLOW AUTOMATION OPPORTUNITIES")
        for p in auto[:3]:
            print(f"   • [{p['repeat_count']}x] {p['task'][:60]}... (success: {p['success_rate']}%)")

    # Trigger gap suggestions
    if report["trigger_gap_suggestions"]:
        print(f"\n💡 TRIGGER_CONDITIONS SUGGESTIONS")
        for g in report["trigger_gap_suggestions"][:3]:
            print(f"   Task: {g['task'][:60]}")
            print(f"   Phrases: {', '.join(g['key_phrases'])}")
            if g['current_best_skill']:
                print(f"   Current best: {g['current_best_skill']} (score {g['current_best_score']})")
            print()

    print("=" * 60)
    print(f"  Report generated: {report['generated_at']}")
    print("=" * 60)

# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Analyze skill usage for self-improvement")
    parser.add_argument("--min-entries", type=int, default=5, help="Minimum log entries needed")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--days", type=int, default=None, help="Only analyze last N days")
    args = parser.parse_args()

    entries = load_usage_log(args.min_entries)
    if not entries:
        print("📭 No usage data yet. Use skill_recommend a few times, then run this analyzer.")
        return

    # Filter by days if specified
    if args.days:
        cutoff = datetime.now() - timedelta(days=args.days)
        entries = [
            e for e in entries
            if datetime.fromisoformat(e["timestamp"]) >= cutoff
        ]
        print(f"📅 Filtered to last {args.days} days: {len(entries)} entries")

    report = generate_report(entries, args)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)

if __name__ == "__main__":
    main()
