#!/usr/bin/env python3
"""
ByteRover Knowledge Sync — Agentic Memory Manager

Tự động:
1. Đọc session logs từ ngày chỉ định
2. Trích xuất: facts, preferences, learnings, user info, decisions, errors
3. Curate vào ByteRover với --detach
4. Report tóm tắt

Usage: python3 byterover_knowledge_sync.py [--days-ago N]
"""

import json
import re
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

HERMES_SESSIONS = Path.home() / ".hermes" / "sessions"
HERMES_MEMORIES = Path.home() / ".hermes" / "memories"


def find_sessions(days_ago=1):
    """Tìm session files từ N ngày trước"""
    sessions_dir = HERMES_SESSIONS
    target_date = datetime.now() - timedelta(days=days_ago)
    date_prefix = target_date.strftime("%Y%m%d")
    
    sessions = []
    for f in sessions_dir.glob("session_*.json"):
        if date_prefix in f.name:
            sessions.append(f)
    
    # Fallback: tìm session gần nhất nếu không có session theo ngày
    if not sessions:
        sessions = sorted(sessions_dir.glob("session_*.json"), 
                        key=lambda f: f.stat().st_mtime, reverse=True)[:3]
    
    return sessions


def extract_knowledge(session_path):
    """Trích xuất knowledge từ session file"""
    try:
        with open(session_path) as f:
            data = json.load(f)
    except Exception as e:
        return {}
    
    knowledge = {
        "user_facts": [],
        "preferences": [],
        "learnings": [],
        "tasks_completed": [],
        "decisions": [],
        "entities": [],
        "skills_created": [],
        "errors_fixed": [],
        "session_summary": None,
    }
    
    # Get session metadata
    if isinstance(data, dict):
        messages = data.get("messages", [])
        knowledge["session_summary"] = f"Session with {len(messages)} messages"
        
        # Extract from messages
        text = json.dumps(data, ensure_ascii=False)
        
        # Extract user identity patterns
        name_patterns = [
            r'(?:anh|mr|user|user_name)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'Tu[uần\s]+[A-Z][a-z]+',
        ]
        for pattern in name_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            knowledge["entities"].extend(set(matches[:5]))
        
        # Extract Vietnamese preferences (common patterns)
        pref_patterns = [
            r'(?:prefers|preference|thích|ưa)[:\s]+([^\n.]{5,150})',
            r'(?:muốn|want|wants)[:\s]+([^\n.]{5,150})',
            r'(?:không thích|dislike|hate)[:\s]+([^\n.]{5,150})',
            r'(?:luôn luôn|always|không bao giờ|never)[:\s]+([^\n.]{5,150})',
        ]
        for pattern in pref_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches[:10]:
                if isinstance(m, tuple):
                    knowledge["preferences"].append(" ".join(m).strip())
                else:
                    knowledge["preferences"].append(m.strip())
        
        # Extract learnings (approaches that worked)
        learning_patterns = [
            r'(?:learned|học được|rút kinh nghiệm)[:\s]+([^\n.]{10,250})',
            r'(?:approach|phương pháp|cách)[:\s]+work.*?[:\s]+([^\n.]{10,250})',
            r'(?:fixed|solved|đã fix)[:\s]+([^\n.]{10,250})',
            r'work.*?by[:\s]+([^\n.]{10,250})',
        ]
        for pattern in learning_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches[:10]:
                if isinstance(m, tuple):
                    knowledge["learnings"].append(" ".join(m).strip())
                else:
                    knowledge["learnings"].append(m.strip())
        
        # Extract errors and solutions
        error_patterns = [
            r'error[:\s]+([^\n.]{10,200})',
            r'bug[:\s]+([^\n.]{10,200})',
            r'lỗi[:\s]+([^\n.]{10,200})',
        ]
        for pattern in error_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            knowledge["errors_fixed"].extend(matches[:10])
        
        # Extract decisions
        decision_patterns = [
            r'(?:chose|decided|quyết định|đã chọn)[:\s]+([^\n.]{10,250})',
            r'(?:decision|ra quyết định)[:\s]+([^\n.]{10,250})',
            r'use.*?instead.*?because[:\s]+([^\n.]{10,250})',
        ]
        for pattern in decision_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches[:10]:
                if isinstance(m, tuple):
                    knowledge["decisions"].append(" ".join(m).strip())
                else:
                    knowledge["decisions"].append(m.strip())
        
        # Extract task completions
        task_patterns = [
            r'(?:completed|done|hoàn thành|xong)[:\s]+([^\n.]{10,200})',
            r'(?:task|job|work)[:\s]+([^\n.]{10,200})',
        ]
        for pattern in task_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            knowledge["tasks_completed"].extend(matches[:10])
        
        # Extract skill creations
        skill_patterns = [
            r'(?:skill|created|new skill)[:\s]+([^\n.]{10,200})',
            r'wrote.*?skill.*?to[:\s]+([^\n.]{10,200})',
        ]
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            knowledge["skills_created"].extend(matches[:10])
    
    return knowledge


def deduplicate_items(items, min_length=15):
    """Remove duplicates and short items"""
    seen = set()
    result = []
    for item in items:
        if not item or len(item.strip()) < min_length:
            continue
        item_clean = item.strip().lower()[:100]
        if item_clean not in seen:
            seen.add(item_clean)
            result.append(item.strip())
    return result


def curate_to_byterover(knowledge):
    """Curate extracted knowledge to ByteRover"""
    results = []
    
    # Deduplicate all lists
    for key in knowledge:
        if isinstance(knowledge[key], list):
            knowledge[key] = deduplicate_items(knowledge[key])
    
    # Curate user facts
    for fact in knowledge.get("user_facts", [])[:15]:
        if len(fact) > 15:
            result = subprocess.run(
                ["brv", "curate", f"fact: {fact}", "--detach"],
                capture_output=True, text=True, timeout=8
            )
            results.append(("fact", fact[:80], result.returncode == 0))
    
    # Curate preferences
    for pref in knowledge.get("preferences", [])[:15]:
        if len(pref) > 15:
            result = subprocess.run(
                ["brv", "curate", f"preference: {pref}", "--detach"],
                capture_output=True, text=True, timeout=8
            )
            results.append(("pref", pref[:80], result.returncode == 0))
    
    # Curate learnings
    for learning in knowledge.get("learnings", [])[:15]:
        if len(learning) > 15:
            result = subprocess.run(
                ["brv", "curate", f"learning: {learning}", "--detach"],
                capture_output=True, text=True, timeout=8
            )
            results.append(("learning", learning[:80], result.returncode == 0))
    
    # Curate errors fixed
    for error in knowledge.get("errors_fixed", [])[:10]:
        if len(error) > 15:
            result = subprocess.run(
                ["brv", "curate", f"error_fix: {error}", "--detach"],
                capture_output=True, text=True, timeout=8
            )
            results.append(("error", error[:80], result.returncode == 0))
    
    # Curate decisions
    for decision in knowledge.get("decisions", [])[:10]:
        if len(decision) > 15:
            result = subprocess.run(
                ["brv", "curate", f"decision: {decision}", "--detach"],
                capture_output=True, text=True, timeout=8
            )
            results.append(("decision", decision[:80], result.returncode == 0))
    
    # Curate tasks completed
    for task in knowledge.get("tasks_completed", [])[:10]:
        if len(task) > 15:
            result = subprocess.run(
                ["brv", "curate", f"task_completed: {task}", "--detach"],
                capture_output=True, text=True, timeout=8
            )
            results.append(("task", task[:80], result.returncode == 0))
    
    # Curate skills created
    for skill in knowledge.get("skills_created", [])[:10]:
        if len(skill) > 15:
            result = subprocess.run(
                ["brv", "curate", f"skill_created: {skill}", "--detach"],
                capture_output=True, text=True, timeout=8
            )
            results.append(("skill", skill[:80], result.returncode == 0))
    
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ByteRover Knowledge Sync")
    parser.add_argument("--days-ago", type=int, default=1,
                        help="Sync sessions from N days ago (default: 1)")
    args = parser.parse_args()
    
    print(f"[ByteRover Knowledge Sync] Running for {args.days_ago} day(s) ago...")
    
    # Find sessions
    sessions = find_sessions(args.days_ago)
    print(f"Found {len(sessions)} sessions")
    
    if not sessions:
        print("No sessions found. Exiting.")
        return
    
    # Extract knowledge from all sessions
    all_knowledge = defaultdict(list)
    total_messages = 0
    
    for session in sessions:
        print(f"  Processing: {session.name}")
        k = extract_knowledge(session)
        total_messages += k.get("session_summary", "").count("messages")
        for key, vals in k.items():
            if isinstance(vals, list):
                all_knowledge[key].extend(vals)
    
    total_items = sum(len(v) for v in all_knowledge.values())
    print(f"Extracted: {total_items} items from {len(sessions)} session(s)")
    
    # Deduplicate
    for key in all_knowledge:
        all_knowledge[key] = deduplicate_items(all_knowledge[key])
    
    # Curate to ByteRover
    print("Curating to ByteRover...")
    results = curate_to_byterover(all_knowledge)
    
    success = sum(1 for _, _, ok in results if ok)
    failed = sum(1 for _, _, ok in results if not ok)
    
    print(f"Curated {success}/{len(results)} items (failed: {failed})")
    
    # Summary by type
    by_type = defaultdict(list)
    for t, _, ok in results:
        if ok:
            by_type[t].append(t)
    
    for t, items in sorted(by_type.items()):
        print(f"  - {t}: {len(items)} items")
    
    print("\n[ByteRover Knowledge Sync] Complete!")


if __name__ == "__main__":
    main()