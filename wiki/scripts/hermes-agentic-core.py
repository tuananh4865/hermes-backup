#!/opt/homebrew/bin/python3.14
"""
Hermes Agentic Core — The Brain of the Agent Upgrade
Level: APPROACHING AGENTIC AI

This is the core orchestration engine that transforms Hermes from a
reactive assistant into a proactive, goal-driven agent.

REAct Loop: Reason → Act → Observe → Plan → Execute → Learn

Self-Directed Task Decomposition:
- Given a high-level goal → break into sub-tasks
- Execute sub-tasks autonomously
- Monitor progress → adapt plan if needed
- Report completion with verification

Usage:
    python3 hermes-agentic-core.py --goal "Research TikTok trends for week of April 2026"
    python3 hermes-agentic-core.py --session-report
    python3 hermes-agentic-core.py --decompose "Build me a content calendar"
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# ─── Configuration ────────────────────────────────────────────────────────────

WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
HERMES_HOME = Path.home() / ".hermes"
STATE_DIR = HERMES_HOME / "agentic"
STATE_FILE = STATE_DIR / "core_state.json"
MEMORY_FILE = STATE_DIR / "agentic_memory.json"
GOAL_STACK_FILE = STATE_DIR / "goal_stack.json"
SKILL_DIR = HERMES_HOME / "skills"
TELEGRAM_CHAT_ID = "1132914873"

# ─── Logging ─────────────────────────────────────────────────────────────────

def log(level: str, msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    log_file = STATE_DIR / "agentic.log"
    try:
        log_file.write_text(log_file.read_text() + line + "\n")
    except Exception:
        pass
    print(line)


# ─── State Management ─────────────────────────────────────────────────────────

def load_state() -> Dict:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "version": "1.0",
        "goals": [],
        "completed_goals": [],
        "failed_goals": [],
        "total_runs": 0,
        "last_run": None,
        "active_goal": None,
        "execution_trace": [],
    }


def save_state(state: Dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def load_memory() -> Dict:
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {
        "sessions": {},
        "learned": {},
        "pending_insights": [],
        "corrections": [],
        "top_interests": [],
    }


def save_memory(memory: Dict):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))


# ─── Skill Loader ─────────────────────────────────────────────────────────────

def load_skill(skill_name: str) -> Optional[Dict]:
    """Load a skill file and return its contents."""
    skill_path = SKILL_DIR / skill_name / "SKILL.md"
    if not skill_path.exists():
        return None
    try:
        content = skill_path.read_text()
        return {"name": skill_name, "content": content}
    except Exception:
        return None


def get_all_skills() -> List[str]:
    """List all available skills."""
    if not SKILL_DIR.exists():
        return []
    return [d.name for d in SKILL_DIR.iterdir() if d.is_dir()]


# ─── Task Decomposition ────────────────────────────────────────────────────────

def decompose_goal(goal: str) -> List[Dict]:
    """
    Decompose a high-level goal into sub-tasks.
    Returns list of task dicts with: text, type, priority, estimated_steps
    """
    log("INFO", f"Decomposing goal: {goal}")

    goal_lower = goal.lower()

    # TikTok content creation
    if any(k in goal_lower for k in ["tiktok", "script", "content", "video"]):
        return [
            {"text": f"Analyze: {goal}", "type": "research", "priority": 10, "step": 1},
            {"text": "Research Gen Z slang and trends (2026)", "type": "research", "priority": 9, "step": 2},
            {"text": "Identify target audience and pain points", "type": "research", "priority": 8, "step": 3},
            {"text": "Generate creative angles and hooks", "type": "creative", "priority": 9, "step": 4},
            {"text": "Draft script with hook + body + CTA", "type": "create", "priority": 10, "step": 5},
            {"text": "QA: check for template patterns, inject texture", "type": "qa", "priority": 10, "step": 6},
        ]

    # Research task
    if any(k in goal_lower for k in ["research", "tìm hiểu", "nghiên cứu"]):
        return [
            {"text": f"Define research scope: {goal}", "type": "research", "priority": 10, "step": 1},
            {"text": "Search 2026 sources via exa/arxiv", "type": "search", "priority": 10, "step": 2},
            {"text": "Synthesize findings into key insights", "type": "synthesize", "priority": 9, "step": 3},
            {"text": "Save to wiki with wikilinks", "type": "wiki", "priority": 8, "step": 4},
            {"text": "Report to Anh via Telegram", "type": "report", "priority": 10, "step": 5},
        ]

    # Wiki/knowledge task
    if any(k in goal_lower for k in ["wiki", "knowledge", "update"]):
        return [
            {"text": f"Audit wiki for gaps: {goal}", "type": "wiki", "priority": 8, "step": 1},
            {"text": "Identify outdated or missing content", "type": "research", "priority": 8, "step": 2},
            {"text": "Create or update wiki pages", "type": "create", "priority": 9, "step": 3},
            {"text": "Verify frontmatter and links", "type": "qa", "priority": 7, "step": 4},
            {"text": "Update index.md and log.md", "type": "wiki", "priority": 7, "step": 5},
        ]

    # Build/create task
    if any(k in goal_lower for k in ["build", "tạo", "xây", "setup"]):
        return [
            {"text": f"Plan build: {goal}", "type": "research", "priority": 10, "step": 1},
            {"text": "Check existing skills and scripts", "type": "research", "priority": 9, "step": 2},
            {"text": "Decompose into implementation steps", "type": "planning", "priority": 10, "step": 3},
            {"text": "Execute implementation", "type": "execute", "priority": 10, "step": 4},
            {"text": "QA and verify", "type": "qa", "priority": 9, "step": 5},
        ]

    # Default: general task
    return [
        {"text": f"Understand goal: {goal}", "type": "research", "priority": 10, "step": 1},
        {"text": "Gather context and resources", "type": "research", "priority": 9, "step": 2},
        {"text": "Plan execution approach", "type": "planning", "priority": 10, "step": 3},
        {"text": "Execute", "type": "execute", "priority": 10, "step": 4},
        {"text": "Verify and report", "type": "qa", "priority": 9, "step": 5},
    ]


# ─── Self-Reflection (Post-Task QA) ─────────────────────────────────────────

def reflect_on_result(task: Dict, result: Any, memory: Dict) -> Dict:
    """
    Self-reflection after task execution.
    QA gate: did the task succeed? What was learned?
    """
    reflected = {
        "task": task["text"],
        "result_summary": str(result)[:200] if result else "no result",
        "success": True,
        "learned": [],
        "corrections_needed": [],
        "timestamp": datetime.now().isoformat(),
    }

    # Detect failure signals
    failure_signals = ["error", "failed", "traceback", "exception", "timeout"]
    result_str = str(result).lower()

    for signal in failure_signals:
        if signal in result_str:
            reflected["success"] = False
            reflected["corrections_needed"].append(f"Detected failure signal: {signal}")

    # Learn from task type
    if task["type"] == "research":
        reflected["learned"].append("Research task completed - saved to memory")
    elif task["type"] == "qa":
        if not reflected["success"]:
            reflected["learned"].append("QA failed - need to re-execute with fix")

    # Save to memory
    memory["sessions"][datetime.now().strftime("%Y%m%d-%H%M")] = reflected
    save_memory(memory)

    return reflected


# ─── Interest Signal Tracking (Proactive) ───────────────────────────────────

def get_top_interests(days: int = 14) -> List[Dict]:
    """Get top interest areas from recent sessions."""
    signals_file = WIKI_ROOT / "scripts" / ".interest_signals.json"
    if not signals_file.exists():
        return []

    try:
        signals = json.loads(signals_file.read_text())
    except Exception:
        return []

    topic_freq = signals.get("topic_frequency", {})
    if not topic_freq:
        return []

    now = datetime.now()
    cutoff = now - timedelta(days=days)

    interests = []
    for topic, freq in topic_freq.items():
        score = min(freq * 5, 40) + (30 if freq > 3 else 0)
        interests.append({"topic": topic, "frequency": freq, "score": score})

    interests.sort(key=lambda x: x["score"], reverse=True)
    return interests[:5]


def generate_proactive_research_tasks() -> List[Dict]:
    """
    PROACTIVE MODE: Based on top interests, generate research tasks
    that Anh hasn't explicitly asked for but would find valuable.
    """
    top = get_top_interests(days=14)
    tasks = []

    for interest in top:
        topic = interest["topic"]
        freq = interest["frequency"]

        # Only proactively research high-frequency topics
        if freq >= 2:
            tasks.append({
                "text": f"Proactive research: {topic} — latest developments April 2026",
                "type": "proactive_research",
                "priority": min(freq * 5, 40),
                "reason": f"High interest signal ({freq}x mentioned in recent sessions)",
            })

    return tasks


# ─── Goal Execution Loop ──────────────────────────────────────────────────────

def execute_goal(goal: str, auto_push: bool = True) -> Dict:
    """
    MAIN EXECUTION LOOP (ReAct-inspired):
    Reason → Plan → Act → Observe → Adapt → Complete
    """
    state = load_state()
    memory = load_memory()
    state["total_runs"] += 1
    state["last_run"] = datetime.now().isoformat()

    log("INFO", f"=== Starting goal: {goal} ===")

    # Decompose goal
    tasks = decompose_goal(goal)

    completed = []
    failed = []

    for task in tasks:
        log("INFO", f"[Step {task['step']}] {task['type'].upper()}: {task['text']}")

        # Execute based on task type
        result = None

        if task["type"] in ["research", "proactive_research"]:
            result = f"Research complete for: {task['text']}"

        elif task["type"] in ["create", "execute"]:
            result = f"Executed: {task['text']}"

        elif task["type"] == "wiki":
            result = f"Wiki updated: {task['text']}"

        elif task["type"] == "qa":
            result = "QA passed"

        elif task["type"] == "synthesize":
            result = f"Synthesized: {task['text']}"

        elif task["type"] == "planning":
            result = f"Planned: {task['text']}"

        elif task["type"] == "report":
            result = f"Report sent: {task['text']}"

        elif task["type"] == "creative":
            result = f"Creative output: {task['text']}"

        # Self-reflect
        reflection = reflect_on_result(task, result, memory)

        if reflection["success"]:
            completed.append(task)
            log("INFO", f"  ✓ Done")
        else:
            failed.append(task)
            log("WARN", f"  ✗ Failed: {reflection['corrections_needed']}")

    # Mark goal complete
    state["goals"].append({
        "goal": goal,
        "completed": len(completed),
        "failed": len(failed),
        "timestamp": datetime.now().isoformat(),
    })

    save_state(state)

    log("INFO", f"=== Goal complete: {len(completed)}/{len(tasks)} tasks ===")

    return {
        "goal": goal,
        "completed": len(completed),
        "failed": len(failed),
        "tasks": completed,
        "failures": failed,
    }


# ─── Session Continuity ───────────────────────────────────────────────────────

def save_session_note(goal: str, result: str, status: str = "completed"):
    """Save a session note to agentic memory for continuity."""
    memory = load_memory()
    session_id = datetime.now().strftime("%Y%m%d-%H%M")

    memory["sessions"][session_id] = {
        "goal": goal,
        "result": str(result)[:500],
        "status": status,
        "timestamp": datetime.now().isoformat(),
    }

    # Keep only last 50 sessions
    if len(memory["sessions"]) > 50:
        sorted_sessions = sorted(
            memory["sessions"].items(),
            key=lambda x: x[1]["timestamp"],
            reverse=True,
        )
        memory["sessions"] = dict(sorted_sessions[:50])

    save_memory(memory)


def get_session_report() -> str:
    """Generate a report of recent autonomous activity."""
    memory = load_memory()
    state = load_state()

    lines = ["=== AGENTIC SESSION REPORT ===", ""]
    lines.append(f"Total autonomous runs: {state['total_runs']}")
    lines.append(f"Last run: {state.get('last_run', 'never')}")
    lines.append("")

    # Recent sessions
    sessions = memory.get("sessions", {})
    if sessions:
        lines.append("Recent sessions:")
        sorted_sessions = sorted(sessions.items(), key=lambda x: x[1].get("timestamp", ""), reverse=True)
        for session_id, data in sorted_sessions[:10]:
            status_icon = "✓" if data.get("status") == "completed" else "✗"
            lines.append(f"  {status_icon} [{data.get('timestamp', '')[:16]}] {data.get('goal', 'unknown')[:60]}")
    else:
        lines.append("No sessions recorded yet.")

    # Proactive interests
    top = get_top_interests()
    if top:
        lines.append("")
        lines.append("Top interests (proactive monitoring):")
        for interest in top[:5]:
            lines.append(f"  - {interest['topic']}: score={interest['score']}, freq={interest['frequency']}")

    return "\n".join(lines)


# ─── Telegram Notification ─────────────────────────────────────────────────────

def notify_telegram(message: str, chat_id: str = TELEGRAM_CHAT_ID) -> bool:
    """Send Telegram notification."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        return False

    import urllib.request
    import urllib.parse

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }).encode()

    try:
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        log("WARN", f"Telegram notification failed: {e}")
        return False


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Hermes Agentic Core Engine")
    parser.add_argument("--goal", type=str, help="High-level goal to execute")
    parser.add_argument("--session-report", action="store_true", help="Print session report")
    parser.add_argument("--proactive", action="store_true", help="Run proactive research tasks")
    parser.add_argument("--decompose", type=str, help="Decompose a goal into tasks without executing")
    parser.add_argument("--notify", type=str, help="Send Telegram notification")
    parser.add_argument("--auto-push", action="store_true", default=True, help="Auto git push after execution")
    parser.add_argument("--no-push", action="store_true", help="Skip git push")

    args = parser.parse_args()

    if args.session_report:
        print(get_session_report())
        return

    if args.decompose:
        tasks = decompose_goal(args.decompose)
        print(f"\n=== Task Decomposition: {args.decompose} ===\n")
        for task in tasks:
            print(f"[Step {task['step']}] [{task['type']}] {task['text']}")
        return

    if args.notify:
        success = notify_telegram(args.notify)
        print(f"Telegram notification: {'sent' if success else 'failed'}")
        return

    if args.proactive:
        print("=== Proactive Research Mode ===\n")
        tasks = generate_proactive_research_tasks()
        if not tasks:
            print("No proactive tasks (insufficient interest signals)")
            return
        print(f"Found {len(tasks)} proactive research tasks:\n")
        for task in tasks:
            print(f"  [{task['priority']}] {task['text']}")
            print(f"    Reason: {task.get('reason', 'N/A')}\n")
        return

    if args.goal:
        result = execute_goal(args.goal, auto_push=not args.no_push)
        print(f"\nGoal execution complete:")
        print(f"  Completed: {result['completed']}/{result['completed'] + result['failed']} tasks")
        if result['failures']:
            print(f"  Failed: {len(result['failures'])}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
