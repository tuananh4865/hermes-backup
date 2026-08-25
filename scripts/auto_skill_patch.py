#!/usr/bin/env python3
"""
auto_skill_patch.py — Autonomous skill improvement from usage analysis.

Garry Tan: "The system will improve itself as skills compound."
This script takes insights from skill_insight_analyzer and
AUTO-PATCHES trigger_conditions on skills that are:
  - Recommended often but rarely selected (weak trigger)
  - Selected but have low success rate (imprecise trigger)

Safe auto-patches (LOW RISK):
  - trigger_conditions: add/remove phrases
  - use_case_keywords: sharpen or broaden
  - tags: add missing tags

RISKY — always ask user first:
  - Creating new skills
  - Deleting skills
  - Rewriting description or body content

Run: python3 auto_skill_patch.py --dry-run
     python3 auto_skill_patch.py --apply
     python3 auto_skill_patch.py --skill ios-dev --add-trigger "when building iOS apps with Xcode"
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─── Paths ────────────────────────────────────────────────────────────────────

SKILLS_DIR = Path.home() / ".hermes" / "skills"
USAGE_LOG = SKILLS_DIR / "_usage_log.jsonl"
INDEX_PATH = SKILLS_DIR / "_index.json"
AUTO_PATCH_LOG = SKILLS_DIR / "_auto_patch_log.jsonl"

# ─── Log Analysis Helpers ────────────────────────────────────────────────────

def load_usage_log(limit: int = 500) -> list[dict]:
    if not USAGE_LOG.exists():
        return []
    entries = []
    with open(USAGE_LOG, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return entries

def load_skill_index() -> dict:
    if not INDEX_PATH.exists():
        return {}
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))

def find_weak_triggers(entries: list[dict], skill_index: dict, min_recommendations: int = 3) -> list[dict]:
    """
    Find skills that get recommended frequently but almost never selected.
    This means the trigger_conditions are too broad.
    """
    recommended = {}
    selected = {}

    for entry in entries:
        recs = entry.get("recommended_skills", [])
        for rec in recs[:3]:
            name = rec["name"]
            recommended[name] = recommended.get(name, 0) + 1
        sel = entry.get("selected_skill")
        if sel:
            selected[sel] = selected.get(sel, 0) + 1

    skill_map = {s["name"]: s for s in skill_index.get("skills", [])}
    weak = []

    for name, rec_count in recommended.items():
        if rec_count < min_recommendations:
            continue
        sel_count = selected.get(name, 0)
        selection_rate = sel_count / rec_count if rec_count > 0 else 0
        # Flag: recommended a lot but almost never chosen
        if selection_rate < 0.15 and rec_count >= min_recommendations:
            skill = skill_map.get(name, {})
            weak.append({
                "skill_name": name,
                "skill_path": SKILLS_DIR / skill.get("skill_dir", name) / "SKILL.md",
                "recommended_count": rec_count,
                "selected_count": sel_count,
                "selection_rate": round(selection_rate * 100, 1),
                "current_triggers": skill.get("trigger_conditions", []),
                "current_use_case": skill.get("use_case_keywords", []),
                "issue": "trigger_conditions too broad — matches many tasks but wrong ones selected",
                "fix": "sharpen trigger_conditions to be more specific",
            })
    return weak

def find_low_success_skills(entries: list[dict], skill_index: dict, min_uses: int = 2) -> list[dict]:
    """
    Find skills that ARE selected but produce poor outcomes.
    This means the skill is good but trigger_conditions don't match the right situations.
    """
    skill_outcomes = {}

    for entry in entries:
        sel = entry.get("selected_skill")
        outcome = entry.get("outcome", "unknown")
        if sel:
            if sel not in skill_outcomes:
                skill_outcomes[sel] = {"success": 0, "failed": 0, "partial": 0, "unknown": 0, "total": 0}
            skill_outcomes[sel]["total"] += 1
            if outcome in skill_outcomes[sel]:
                skill_outcomes[sel][outcome] += 1

    skill_map = {s["name"]: s for s in skill_index.get("skills", [])}
    low_success = []

    for name, stats in skill_outcomes.items():
        if stats["total"] < min_uses:
            continue
        success_rate = stats["success"] / stats["total"] if stats["total"] > 0 else 0
        if success_rate < 0.4:  # Less than 40% success
            skill = skill_map.get(name, {})
            low_success.append({
                "skill_name": name,
                "skill_path": SKILLS_DIR / skill.get("skill_dir", name) / "SKILL.md",
                "total_uses": stats["total"],
                "success_rate": round(success_rate * 100, 1),
                "current_triggers": skill.get("trigger_conditions", []),
                "issue": "skill selected but low success rate — trigger_conditions may be misaligned",
                "fix": "refine trigger_conditions to better match successful use cases",
            })
    return low_success

def extract_task_keywords(task: str) -> list[str]:
    """Extract meaningful 2-3 word phrases from task text."""
    # Remove common words
    stopwords = {
        "a", "an", "the", "and", "or", "but", "is", "are", "was", "were",
        "be", "been", "being", "have", "has", "had", "do", "does", "did",
        "will", "would", "could", "should", "may", "might", "must", "can",
        "this", "that", "these", "those", "i", "you", "he", "she", "it",
        "what", "which", "who", "when", "where", "why", "how",
        "all", "each", "every", "both", "few", "more", "most", "other",
        "some", "any", "no", "not", "only", "own", "same", "so", "than",
        "too", "very", "just", "for", "with", "on", "at", "by", "from",
        "up", "down", "out", "off", "over", "under", "again", "once",
        "make", "build", "create", "fix", "update", "add", "remove",
        "delete", "task", "use", "using", "need", "want", "get", "got",
        "run", "running", "setup", "set up", "try", "working", "work",
    }
    words = re.findall(r"[a-z0-9]{3,}", task.lower())
    filtered = [w for w in words if w not in stopwords and len(w) >= 3]
    return filtered

def suggest_improved_triggers(skill_name: str, entries: list[dict], fix_type: str) -> list[str]:
    """
    Analyze recent task entries where this skill was NOT selected
    but the task was similar — to understand what causes mis-matches.
    """
    # Find entries where this skill was top-recommended but NOT selected
    similar_entries = []
    for entry in entries:
        recs = entry.get("recommended_skills", [])
        if recs and recs[0]["name"] == skill_name and not entry.get("selected_skill"):
            similar_entries.append(entry["task"])

    # Also find where it WAS selected but failed
    failed_entries = []
    for entry in entries:
        if entry.get("selected_skill") == skill_name and entry.get("outcome") == "failed":
            failed_entries.append(entry["task"])

    suggested = []

    # Extract key phrases from tasks that matched but weren't selected
    if similar_entries:
        for task in similar_entries[:5]:
            kws = extract_task_keywords(task)
            # Filter to phrases that are 2+ words
            phrases = [kws[i] + " " + kws[i+1] for i in range(len(kws)-1) if kws[i] and kws[i+1]]
            suggested.extend([p for p in phrases if len(p) > 5][:2])

    # Remove duplicates and current triggers
    skill_index = load_skill_index()
    skill_map = {s["name"]: s for s in skill_index.get("skills", [])}
    current = set(skill_map.get(skill_name, {}).get("trigger_conditions", []))

    suggestions = []
    for s in suggested:
        if s.lower() not in current and s not in current:
            suggestions.append(s)
    return list(dict.fromkeys(suggestions))[:4]  # Dedupe, max 4

# ─── Safe Auto-Patch Functions ───────────────────────────────────────────────

def patch_trigger_conditions(skill_path: Path, new_triggers: list[str], dry_run: bool = True) -> dict:
    """
    Safely add new trigger_conditions to a SKILL.md frontmatter.
    Only modifies trigger_conditions — does NOT touch body content.
    """
    if not skill_path.exists():
        return {"success": False, "error": f"Skill file not found: {skill_path}"}

    content = skill_path.read_text(encoding="utf-8")

    # Parse frontmatter
    if not content.startswith("---"):
        return {"success": False, "error": "No frontmatter found"}

    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return {"success": False, "error": "Malformed frontmatter"}

    frontmatter = content[3:end_idx].strip()
    body = content[end_idx + 4:]

    # Parse existing frontmatter as dict
    fm_dict = {}
    for line in frontmatter.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            fm_dict[key.strip()] = val.strip().strip('"\'')

    # Check if trigger_conditions already exists
    existing_triggers = []
    if "trigger_conditions" in fm_dict:
        # Try to extract from frontmatter text
        trigger_match = re.search(r'trigger_conditions:\s*\n((?:\s*-\s*[^\n]+\n)*)', content[:end_idx+3])
        if trigger_match:
            for line in trigger_match.group(1).split("\n"):
                m = re.match(r'\s*-\s*(.+)', line)
                if m:
                    existing_triggers.append(m.group(1).strip().strip('"\''))

    # Merge new triggers (avoid duplicates)
    all_triggers = existing_triggers.copy()
    for t in new_triggers:
        if t.lower() not in [x.lower() for x in all_triggers]:
            all_triggers.append(t)

    if len(all_triggers) <= len(existing_triggers):
        return {"success": True, "message": "No new unique triggers to add", "changes": 0}

    # Rebuild frontmatter with new triggers
    new_trigger_lines = "\n".join(f"  - \"{t}\"" for t in all_triggers)

    # Find and replace trigger_conditions section
    new_content = content
    if "trigger_conditions:" in content:
        # Replace existing
        pattern = r'trigger_conditions:\s*\n((?:\s*-\s*[^\n]+\n)*)'
        new_content = re.sub(pattern, f'trigger_conditions:\n{new_trigger_lines}\n', content)
    else:
        # Add after description line
        if "description:" in new_content:
            new_content = re.sub(
                r'(description:[^\n]+\n)',
                r'\1' + f'trigger_conditions:\n{new_trigger_lines}\n',
                new_content,
                count=1
            )

    changes = len(all_triggers) - len(existing_triggers)

    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "skill": skill_path.parent.name,
            "existing_triggers": existing_triggers,
            "new_triggers_added": new_triggers,
            "all_triggers": all_triggers,
            "changes": changes,
            "message": f"Would add {changes} new trigger_conditions",
        }
    else:
        skill_path.write_text(new_content, encoding="utf-8")
        log_patch(skill_path.parent.name, "trigger_conditions", new_triggers, "applied")
        return {
            "success": True,
            "dry_run": False,
            "skill": skill_path.parent.name,
            "changes": changes,
            "message": f"Added {changes} trigger_conditions",
        }

def log_patch(skill_name: str, patch_type: str, details: list, status: str) -> None:
    """Log all auto-patches for audit trail."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "skill": skill_name,
        "type": patch_type,
        "details": details,
        "status": status,  # applied, skipped, user_approved
    }
    with open(AUTO_PATCH_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# ─── Main Logic ───────────────────────────────────────────────────────────────

def run_auto_improve(dry_run: bool = True, min_recommendations: int = 3) -> list[dict]:
    """Main self-improvement loop."""
    entries = load_usage_log()
    if len(entries) < 3:
        print(f"⚠️  Only {len(entries)} entries — need more data for auto-improvement.")
        print("   Keep using skill_recommend and this will improve automatically.")
        return []

    skill_index = load_skill_index()
    results = []

    # 1. Sharpen overly broad trigger_conditions
    weak_triggers = find_weak_triggers(entries, skill_index, min_recommendations)
    for item in weak_triggers:
        suggested = suggest_improved_triggers(item["skill_name"], entries, "weak_trigger")
        if suggested:
            item["suggested_triggers"] = suggested
            result = patch_trigger_conditions(item["skill_path"], suggested, dry_run=dry_run)
            results.append({**item, "patch_result": result})
        else:
            results.append({**item, "patch_result": {"success": True, "message": "No specific suggestions — needs manual review"}})

    # 2. Refine low-success skill triggers
    low_success = find_low_success_skills(entries, skill_index)
    for item in low_success:
        suggested = suggest_improved_triggers(item["skill_name"], entries, "low_success")
        if suggested:
            item["suggested_triggers"] = suggested
            result = patch_trigger_conditions(item["skill_path"], suggested, dry_run=dry_run)
            results.append({**item, "patch_result": result})

    return results

def print_results(results: list[dict], dry_run: bool) -> None:
    mode = "DRY-RUN" if dry_run else "APPLIED"
    print(f"\n{'='*60}")
    print(f"  AUTO-SKILL-PATCH ({mode})")
    print(f"{'='*60}")

    if not results:
        print("\n✅ No patches needed — skills are well-tuned.")
        return

    applied = [r for r in results if r.get("patch_result", {}).get("success")]
    skipped = [r for r in results if not r.get("patch_result", {}).get("success")]

    print(f"\n📊 Total: {len(results)} skills analyzed")
    print(f"   {'Would apply' if dry_run else 'Applied'}: {len(applied)}")
    print(f"   Skipped: {len(skipped)}")

    for r in applied:
        pr = r["patch_result"]
        print(f"\n🔧 {r['skill_name']}")
        print(f"   Issue: {r['issue']}")
        if "suggested_triggers" in r:
            print(f"   Adding: {', '.join(r['suggested_triggers'][:3])}")
        print(f"   → {pr.get('message', 'OK')}")

    if skipped:
        print(f"\n⚠️  Skipped:")
        for r in skipped:
            print(f"   • {r['skill_name']}: {r['patch_result'].get('message')}")

    if dry_run:
        print(f"\n💡 Run with --apply to actually apply these changes.")
        print(f"   Run with --dry-run=false to apply silently.")

# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Auto-improve skills from usage analysis")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Show what would change (default)")
    parser.add_argument("--apply", action="store_true", help="Actually apply changes")
    parser.add_argument("--min-recs", type=int, default=3, help="Min recommendation count to flag a skill")
    parser.add_argument("--skill", type=str, help="Target a specific skill only")
    parser.add_argument("--add-trigger", type=str, dest="add_trigger", help="Add trigger to specific skill")
    args = parser.parse_args()

    dry_run = not args.apply

    # Single-skill mode
    if args.skill:
        if not args.add_trigger:
            print("--skill requires --add-trigger")
            sys.exit(1)
        skill_index = load_skill_index()
        skill_map = {s["name"]: s for s in skill_index.get("skills", [])}
        if args.skill not in skill_map:
            print(f"Skill '{args.skill}' not found in index")
            sys.exit(1)
        skill = skill_map[args.skill]
        skill_path = SKILLS_DIR / skill.get("skill_dir", args.skill) / "SKILL.md"
        result = patch_trigger_conditions(skill_path, [args.add_trigger], dry_run=dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Full auto-improvement
    results = run_auto_improve(dry_run=dry_run, min_recommendations=args.min_recs)
    print_results(results, dry_run)

if __name__ == "__main__":
    main()
