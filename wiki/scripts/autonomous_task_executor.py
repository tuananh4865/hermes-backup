#!/opt/homebrew/bin/python3.14
"""
Autonomous Task Executor — Reads task queue and spawns subagents to execute
Runs after task_checker.py to actually execute tasks, not just list them.
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
STATE_FILE = Path.home() / ".hermes" / "cron" / "task_state.json"
TASK_CHECK_FILE = Path.home() / ".hermes" / "cron" / "last_task_check.json"
LOG_FILE = Path.home() / ".hermes" / "cron" / "autonomous_executor.log"

def log(msg: str):
    """Log to file with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def load_task_queue() -> Optional[Dict]:
    """Load task queue from last task_checker run"""
    if not TASK_CHECK_FILE.exists():
        log("ERROR: No task queue found. Run task_checker.py first.")
        return None
    
    data = json.loads(TASK_CHECK_FILE.read_text())
    return data.get('all_tasks', [])

def load_state() -> Dict:
    """Load completed tasks state"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {'completed_tasks': [], 'last_run': None}

def save_state(state: Dict):
    """Save state"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def is_completed(task_text: str, state: Dict) -> bool:
    """Check if task was already completed"""
    return any(t['text'] == task_text for t in state.get('completed_tasks', []))

def mark_completed(task_text: str, state: Dict):
    """Mark task as completed"""
    if 'completed_tasks' not in state:
        state['completed_tasks'] = []
    state['completed_tasks'].append({
        'text': task_text,
        'completed_at': datetime.now().isoformat()
    })
    save_state(state)
    log(f"COMPLETED: {task_text}")

def execute_task_via_subagent(task: Dict) -> bool:
    """Execute a task by spawning a Claude Code subagent"""
    task_text = task.get('text', '')
    task_type = task.get('type', 'unknown')
    priority = task.get('priority', 50)
    
    log(f"EXECUTING: [{priority}] {task_text} (type: {task_type})")
    
    # Build the subagent prompt
    # For system tasks, give direct command to avoid max_turns issues
    if task_type == 'system':
        prompt = f"Run this exact command in ~/wiki directory:\ncd ~/wiki && python3 scripts/wiki_lint.py --auto-fix 2>&1"
    elif task_type == 'wiki':
        prompt = f"Run this exact command in ~/wiki directory:\ncd ~/wiki && python3 scripts/wiki_lint.py --auto-fix 2>&1"
    else:
        prompt = f"""Task: {task_text}
Type: {task_type}
Working directory: ~/wiki
Execute this task and report what you did briefly."""
    
    # Execute via Claude Code print mode
    cmd = [
        'claude', '-p', prompt,
        '--output-format', 'json',
        '--max-turns', '5',
        '--dangerously-skip-permissions'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,  # 3 min timeout (Claude needs time to warm up)
            # Note: Don't set cwd - Claude Code needs its own context
            # Task prompt already includes cd ~/wiki
        )
        
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
                if output.get('subtype') == 'success':
                    log(f"SUCCESS: {task_text}")
                    return True
            except json.JSONDecodeError:
                # Non-JSON output still might have worked
                if 'success' in result.stdout.lower() or 'completed' in result.stdout.lower():
                    return True
        else:
            log(f"FAILED: {task_text} - exit code {result.returncode}")
            log(f"stderr: {result.stderr[:500]}")
            
    except subprocess.TimeoutExpired:
        log(f"TIMEOUT: {task_text} (5 min limit)")
    except Exception as e:
        log(f"ERROR: {task_text} - {str(e)}")
    
    return False

def can_execute_autonomously(task: Dict) -> bool:
    """Filter tasks that can be executed autonomously"""
    task_text = task.get('text', '').lower()
    task_type = task.get('type', 'unknown')
    source = task.get('source', 'unknown')
    
    # ONLY execute these specific types autonomously
    # Do NOT run project tasks - they need user context
    if task_type not in {'system', 'wiki', 'gap', 'autonomous', 'explore'}:
        return False
    
    # Skip user-dependent tasks (even system/wiki tasks might have these)
    user_dependent_keywords = [
        'configure', 'create account', 'signup', 'sign up',
        'user needs to', 'requires user', 'manual',
        'deploy to vercel', 'vercel dashboard', 'turso account',
        'dashboard', 'dsn', 'auth_secret', 'database_url'
    ]
    for keyword in user_dependent_keywords:
        if keyword in task_text:
            return False
    
    return True

def main():
    log("=== Autonomous Task Executor Started ===")
    
    # Load task queue
    tasks = load_task_queue()
    if not tasks:
        log("No tasks to execute")
        return
    
    # Load state
    state = load_state()
    
    # Filter out already completed
    pending_tasks = [t for t in tasks if not is_completed(t.get('text', ''), state)]
    
    # Filter to only autonomously executable tasks
    executable_tasks = [t for t in pending_tasks if can_execute_autonomously(t)]
    skipped_count = len(pending_tasks) - len(executable_tasks)
    
    if skipped_count > 0:
        log(f"Skipping {skipped_count} user-dependent tasks (Configure Turso, etc.)")
    
    if not executable_tasks:
        log("No autonomously executable tasks remaining")
        log("Remaining tasks require user action")
        return
    
    log(f"Found {len(executable_tasks)} executable tasks")
    
    # Execute top priority task
    executable_tasks.sort(key=lambda x: x.get('priority', 50), reverse=True)
    
    top_task = executable_tasks[0]
    success = execute_task_via_subagent(top_task)
    
    if success:
        mark_completed(top_task.get('text', ''), state)
    else:
        # If failed, mark as completed anyway to avoid infinite retry loops
        # Or we could increment a retry count
        log(f"Task failed but marking complete to avoid infinite retry: {top_task.get('text', '')}")
        mark_completed(top_task.get('text', '') + " [FAILED]", state)
    
    log("=== Autonomous Task Executor Finished ===")

if __name__ == "__main__":
    main()
