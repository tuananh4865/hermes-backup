#!/opt/homebrew/bin/python3.14
"""
Wiki Agent Coordinator
Multi-agent task coordination system.

Workflow:
1. DECOMPOSE — Break complex task into parallel sub-tasks
2. DISPATCH — Spawn agents to work on sub-tasks
3. AGGREGATE — Collect and merge results
4. RESOLVE — Handle conflicts between agent outputs

Usage:
    python3 agent_coordinator.py --task "Build project tracker" --parallel 3
    python3 agent_coordinator.py --status
    python3 agent_coordinator.py --results TASK_ID
"""

import json
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

WIKI_DIR = Path("/Volumes/Storage-1/Hermes/wiki")
TASK_QUEUE_DIR = WIKI_DIR / ".agent_tasks"
RESULTS_DIR = WIKI_DIR / ".agent_results"


def ensure_dirs():
    TASK_QUEUE_DIR.mkdir(exist_ok=True, parents=True)
    RESULTS_DIR.mkdir(exist_ok=True, parents=True)


def create_task(task_name: str, description: str, sub_tasks: List[Dict]) -> str:
    """Create a new coordination task."""
    ensure_dirs()
    task_id = f"task-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    task = {
        "id": task_id,
        "name": task_name,
        "description": description,
        "sub_tasks": sub_tasks,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "started_at": None,
        "completed_at": None,
        "results": {},
        "conflicts": []
    }

    task_file = TASK_QUEUE_DIR / f"{task_id}.json"
    task_file.write_text(json.dumps(task, indent=2))
    return task_id


def decompose_task(task_name: str) -> List[Dict]:
    """
    Decompose a complex task into parallelizable sub-tasks.
    Each sub-task has: id, description, priority, dependencies
    """
    # This is a simple rule-based decomposer
    # For complex tasks, could integrate with LLM
    sub_tasks = []

    # Common decomposition patterns
    if "research" in task_name.lower():
        sub_tasks = [
            {"id": "web_search", "description": "Search web for information", "priority": 1, "deps": []},
            {"id": "wiki_review", "description": "Review existing wiki content", "priority": 1, "deps": []},
            {"id": "synthesize", "description": "Synthesize findings", "priority": 2, "deps": ["web_search", "wiki_review"]}
        ]
    elif "build" in task_name.lower() or "create" in task_name.lower():
        sub_tasks = [
            {"id": "research_req", "description": "Research requirements", "priority": 1, "deps": []},
            {"id": "write_code", "description": "Write implementation", "priority": 1, "deps": ["research_req"]},
            {"id": "write_tests", "description": "Write tests", "priority": 2, "deps": ["write_code"]},
            {"id": "write_docs", "description": "Write documentation", "priority": 2, "deps": ["write_code"]}
        ]
    elif "improve" in task_name.lower() or "enhance" in task_name.lower():
        sub_tasks = [
            {"id": "analyze_gaps", "description": "Analyze gaps in wiki", "priority": 1, "deps": []},
            {"id": "generate_content", "description": "Generate new content", "priority": 1, "deps": ["analyze_gaps"]},
            {"id": "fix_links", "description": "Fix broken links", "priority": 2, "deps": []},
            {"id": "refresh_stale", "description": "Refresh stale content", "priority": 2, "deps": []}
        ]
    else:
        # Generic single task
        sub_tasks = [
            {"id": "main", "description": task_name, "priority": 1, "deps": []}
        ]

    return sub_tasks


def spawn_agent(sub_task: Dict, parent_task_id: str) -> str:
    """
    Spawn a sub-agent to work on a sub-task.
    Uses Claude Code's ACP mode or falls back to subprocess.
    """
    task_id = sub_task["id"]
    description = sub_task["description"]

    # Write task instructions
    task_file = RESULTS_DIR / f"{parent_task_id}-{task_id}.json"
    task_file.write_text(json.dumps({
        "status": "in_progress",
        "description": description,
        "started_at": datetime.now().isoformat(),
        "output": None,
        "error": None
    }, indent=2))

    # Build agent prompt
    prompt = f"""You are a wiki sub-agent working on task: {description}

Working directory: {WIKI_DIR}
Task ID: {parent_task_id}-{task_id}

Instructions:
1. Complete the task: {description}
2. Write your findings/output to: {task_file}
3. Update the task file with your results when done

If this is a wiki task:
- Check existing content in concepts/
- Create or update pages as needed
- Fix any broken links
- Commit your changes

Start working now. Do not ask for confirmation. Just do it."""

    try:
        # Try using hermes acp mode (Claude Code ACP)
        result = subprocess.run(
            ["claude", "--acp", "--stdio"],
            input=prompt.encode(),
            capture_output=True,
            timeout=120
        )
        return result.returncode == 0
    except FileNotFoundError:
        # Fallback: run in hermes
        try:
            result = subprocess.run(
                ["hermes", "chat", "-y", "--model", "claude-sonnet-4-7-2027"],
                input=prompt.encode(),
                capture_output=True,
                timeout=120
            )
            return result.returncode == 0
        except Exception as e:
            task_file.write_text(json.dumps({
                "status": "failed",
                "error": str(e)
            }, indent=2))
            return False
    except subprocess.TimeoutExpired:
        task_file.write_text(json.dumps({
            "status": "timeout",
            "error": "Agent timed out after 120 seconds"
        }, indent=2))
        return False


def aggregate_results(task_id: str) -> Dict:
    """Collect and aggregate results from all sub-tasks."""
    task_file = TASK_QUEUE_DIR / f"{task_id}.json"
    if not task_file.exists():
        return {"error": "Task not found"}

    task = json.loads(task_file.read_text())
    results = {}

    for sub_task in task["sub_tasks"]:
        result_file = RESULTS_DIR / f"{task_id}-{sub_task['id']}.json"
        if result_file.exists():
            results[sub_task["id"]] = json.loads(result_file.read_text())
        else:
            results[sub_task["id"]] = {"status": "not_started"}

    return results


def resolve_conflicts(results: Dict) -> List[Dict]:
    """Detect and resolve conflicts between agent outputs."""
    conflicts = []

    # Simple conflict detection: check for contradictory claims
    # This is a placeholder — real implementation would use LLM
    for task_id, result in results.items():
        if result.get("status") == "completed":
            output = result.get("output", "")
            if output:
                # Check for common conflict patterns
                pass

    return conflicts


def run_task(task_name: str, parallel: int = 3, auto_spawn: bool = False):
    """Run a coordinated task."""
    print(f"🎯 Creating task: {task_name}")

    sub_tasks = decompose_task(task_name)
    print(f"📋 Decomposed into {len(sub_tasks)} sub-tasks:")

    for i, st in enumerate(sub_tasks, 1):
        deps = f" (deps: {', '.join(st['deps'])})" if st['deps'] else ""
        print(f"  {i}. [{st['priority']}] {st['id']}{deps}")

    task_id = create_task(task_name, task_name, sub_tasks)
    print(f"\n📝 Task ID: {task_id}")

    if auto_spawn:
        print(f"\n🚀 Spawning {min(parallel, len(sub_tasks))} agents...")

        # Spawn agents for non-dependent tasks first
        ready_tasks = [st for st in sub_tasks if not st['deps']]
        running = []

        for st in ready_tasks[:parallel]:
            print(f"  → Spawning agent for: {st['id']}")
            success = spawn_agent(st, task_id)
            running.append(st['id'])
            if success:
                print(f"    ✓ Agent started")
            else:
                print(f"    ✗ Agent failed to start")

        # Wait for completion and aggregate
        print(f"\n⏳ Waiting for agents to complete...")
        max_wait = 300  # 5 minutes
        start = time.time()

        while running and time.time() - start < max_wait:
            time.sleep(5)
            remaining = []
            for st_id in running:
                result_file = RESULTS_DIR / f"{task_id}-{st_id}.json"
                if result_file.exists():
                    result = json.loads(result_file.read_text())
                    if result.get("status") in ["completed", "failed", "timeout"]:
                        print(f"  ✓ {st_id}: {result.get('status')}")
                    else:
                        remaining.append(st_id)
                else:
                    remaining.append(st_id)
            running = remaining

        # Aggregate
        print(f"\n📊 Aggregating results...")
        results = aggregate_results(task_id)

        # Resolve conflicts
        conflicts = resolve_conflicts(results)
        if conflicts:
            print(f"\n⚠️  {len(conflicts)} conflicts detected:")
            for c in conflicts:
                print(f"  - {c}")

        print(f"\n✅ Task {task_id} complete!")
        return task_id
    else:
        print(f"\n💡 To run: python3 agent_coordinator.py --run {task_id}")
        print(f"   Or: python3 agent_coordinator.py --auto --task '{task_name}'")
        return task_id


def show_status():
    """Show status of all tasks."""
    ensure_dirs()
    tasks = list(TASK_QUEUE_DIR.glob("*.json"))

    if not tasks:
        print("No tasks found")
        return

    print(f"📋 Active Tasks: {len(tasks)}\n")

    for task_file in sorted(tasks):
        task = json.loads(task_file.read_text())
        status = task.get("status", "unknown")
        created = task.get("created_at", "")[:19]

        print(f"[{status.upper()}] {task['name']}")
        print(f"  ID: {task['id']}")
        print(f"  Created: {created}")
        print(f"  Sub-tasks: {len(task['sub_tasks'])}")
        print()


def main():
    args = sys.argv[1:]

    if "--status" in args or "-s" in args:
        show_status()
        return

    if "--run" in args:
        task_id = args[args.index("--run") + 1] if args.index("--run") + 1 < len(args) else None
        if task_id:
            results = aggregate_results(task_id)
            print(json.dumps(results, indent=2))
        return

    if "--task" in args or "-t" in args:
        task_idx = args.index("--task") if "--task" in args else args.index("-t")
        task_name = args[task_idx + 1] if task_idx + 1 < len(args) else "Unknown"

        parallel = 3
        if "--parallel" in args:
            p_idx = args.index("--parallel")
            parallel = int(args[p_idx + 1])

        auto = "--auto" in args
        run_task(task_name, parallel, auto)
        return

    # Default: show help
    print(__doc__)


if __name__ == "__main__":
    main()
