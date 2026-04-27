#!/opt/homebrew/bin/python3.14
"""
Task Checker — Autonomous wiki + system task checker
Runs every 60 minutes via cron
Fully autonomous: picks highest priority task and executes
"""
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
STATE_FILE = Path.home() / ".hermes" / "cron" / "task_state.json"

def run_cmd(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def load_state() -> Dict:
    """Load previous run state to know what's completed"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {'completed_tasks': [], 'last_run': None}

def save_state(state: Dict):
    """Save state for next run"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def mark_completed(task_text: str, state: Dict):
    """Mark a task as completed"""
    if 'completed_tasks' not in state:
        state['completed_tasks'] = []
    state['completed_tasks'].append({
        'text': task_text,
        'completed_at': datetime.now().isoformat()
    })
    save_state(state)

def get_wiki_tasks(state: Dict) -> Dict:
    """Extract pending tasks from wiki"""
    tasks = {
        'project_tasks': [],
        'wiki_improvements': [],
        'top_gaps': [],
        'empty': True
    }
    
    completed = [t['text'] for t in state.get('completed_tasks', [])]
    
    # Patterns that indicate user-action blocked tasks (skip these — external credentials, demos)
    USER_ACTION_BLOCKED_PATTERNS = [
        'turso', 'vercel', 'auth_secret', 'sentry_dsn', 'database_url',
        'configure', 'create turso', 'add .env', 'environment variable',
        'pending user action', 'mint my-token', 'requires user',
        '--group finance', 'financetracker',  # demo project names
        'NOT tested on iOS', 'needs manual', 'ios testing', 'user action',
    ]

    def is_user_action_blocked(task: str) -> bool:
        task_lower = task.lower()
        return any(p in task_lower for p in USER_ACTION_BLOCKED_PATTERNS)

    # Check phase files for unchecked TODO items
    phase_dir = WIKI_PATH / "projects"
    if phase_dir.exists():
        for phase_file in phase_dir.rglob("phase-*.md"):
            project_name = phase_file.parent.name.lower()

            # Skip entire demo/template projects
            if 'demo' in project_name or 'template' in project_name:
                continue

            content = phase_file.read_text()
            unchecked = re.findall(r'- \[ \] (.+)', content)
            if unchecked:
                for task in unchecked:
                    if task not in completed and not is_user_action_blocked(task):
                        tasks['project_tasks'].append({
                            'text': task,
                            'source': phase_file.stem,
                            'priority': 70,
                            'type': 'project'
                        })
    
    # Check daily-task queue
    task_queue_file = WIKI_PATH / "projects" / "daily-tasks" / "TASK_QUEUE.md"
    if task_queue_file.exists():
        content = task_queue_file.read_text()
        unchecked = re.findall(r'- \[ \] (.+)', content)
        if unchecked:
            for task in unchecked:
                if task not in completed and not is_user_action_blocked(task):
                    tasks['wiki_improvements'].append({
                        'text': task,
                        'source': 'daily-tasks',
                        'priority': 65,  # Slightly higher than default wiki improvements
                        'type': 'wiki'
                    })

    # Check concepts for improvement ideas
    concepts_dir = WIKI_PATH / "concepts"
    improvement_keywords = ['enhancement', 'improvement', 'roadmap']
    
    if concepts_dir.exists():
        for concept_file in concepts_dir.rglob("*.md"):
            if any(kw in concept_file.name.lower() for kw in improvement_keywords):
                content = concept_file.read_text()
                unchecked = re.findall(r'- \[ \] (.+)', content)
                if unchecked:
                    for task in unchecked:
                        if task not in completed and not is_user_action_blocked(task):
                            tasks['wiki_improvements'].append({
                                'text': task,
                                'source': concept_file.stem,
                                'priority': 50,
                                'type': 'wiki'
                            })
    
    # Check for gaps
    gap_file = WIKI_PATH / "scripts" / "priority_gaps.json"
    if gap_file.exists():
        try:
            gaps = json.loads(gap_file.read_text())
            if isinstance(gaps, list):
                for g in gaps[:5]:
                    score = g.get('score', 0)
                    if score >= 40:
                        task_text = f"Explore: {g['topic']}"
                        if task_text not in completed:
                            tasks['top_gaps'].append({
                                'text': task_text,
                                'source': 'gap_analysis',
                                'priority': min(90, int(score + 30)),
                                'score': score,
                                'type': 'gap'
                            })
        except:
            pass
    
    tasks['empty'] = (
        len(tasks['project_tasks']) == 0 and 
        len(tasks['wiki_improvements']) == 0 and 
        len(tasks['top_gaps']) == 0
    )
    
    return tasks

def get_system_tasks(state: Dict) -> List[Dict]:
    """Check for system-level pending items"""
    tasks = []
    completed = [t['text'] for t in state.get('completed_tasks', [])]
    
    # Check watchdog status
    pid_file = WIKI_PATH / "scripts" / "watchdog.pid"
    watchdog_dead = False
    if pid_file.exists():
        pid = pid_file.read_text().strip()
        try:
            result = subprocess.run(['ps', '-p', pid], capture_output=True)
            watchdog_dead = result.returncode != 0
        except:
            watchdog_dead = True
    else:
        watchdog_dead = True
    
    if watchdog_dead:
        task_text = 'Restart watchdog daemon'
        if task_text not in completed:
            tasks.append({
                'text': task_text,
                'source': 'system',
                'priority': 80,
                'type': 'system'
            })
    
    # Check for wiki lint issues
    lint_result = run_cmd(f"cd {WIKI_PATH} && python3 scripts/wiki_lint.py 2>&1")
    
    if 'TOTAL ISSUES:' in lint_result:
        match = re.search(r'TOTAL ISSUES:\s+(\d+)', lint_result)
        if match:
            issue_count = int(match.group(1))
            if issue_count > 0:
                task_text = f'Fix {issue_count} wiki lint issues'
                if task_text not in completed:
                    tasks.append({
                        'text': task_text,
                        'source': 'system',
                        'priority': 65,
                        'type': 'system'
                    })
    
    # Check git status
    git_status = run_cmd(f"cd {WIKI_PATH} && git status --porcelain")
    if git_status:
        lines = [l for l in git_status.strip().split('\n') if l]
        uncommitted = len(lines)
        if uncommitted > 10:
            task_text = f'Commit {uncommitted} uncommitted changes'
            if task_text not in completed:
                tasks.append({
                    'text': task_text,
                    'source': 'system',
                    'priority': 40,
                    'type': 'system'
                })
    
    return tasks

def get_autonomous_tasks(state: Dict) -> List[Dict]:
    """Tasks for autonomous self-improvement when nothing else to do"""
    tasks = []
    completed = [t['text'] for t in state.get('completed_tasks', [])]
    
    # Check if gaps analysis is stale
    gaps_file = WIKI_PATH / "scripts" / "priority_gaps.json"
    if gaps_file.exists():
        mtime = datetime.fromtimestamp(gaps_file.stat().st_mtime)
        days_since = (datetime.now() - mtime).days
        if days_since > 3:
            task_text = f'Refresh priority gaps analysis (stale {days_since} days)'
            if task_text not in completed:
                tasks.append({
                    'text': task_text,
                    'source': 'autonomous',
                    'priority': 60,
                    'type': 'autonomous'
                })
    
    # Check if self-evolution report is stale
    evolution_file = WIKI_PATH / "scripts" / "self_evolution_report.json"
    if evolution_file.exists():
        mtime = datetime.fromtimestamp(evolution_file.stat().st_mtime)
        days_since = (datetime.now() - mtime).days
        if days_since > 7:
            task_text = f'Run self-evolution analysis (stale {days_since} days)'
            if task_text not in completed:
                tasks.append({
                    'text': task_text,
                    'source': 'autonomous',
                    'priority': 55,
                    'type': 'autonomous'
                })
    
    return tasks

def build_proposal(wiki_tasks: Dict, system_tasks: List[Dict], autonomous_tasks: List[Dict], state: Dict) -> str:
    """Build work proposal for autonomous execution"""
    
    # Combine and sort all tasks
    all_tasks = []
    
    for task in wiki_tasks.get('project_tasks', []):
        all_tasks.append(task)
    for task in wiki_tasks.get('wiki_improvements', []):
        all_tasks.append(task)
    for task in wiki_tasks.get('top_gaps', []):
        all_tasks.append(task)
    for task in system_tasks:
        all_tasks.append(task)
    for task in autonomous_tasks:
        all_tasks.append(task)
    
    # Sort by priority (descending)
    all_tasks.sort(key=lambda x: x.get('priority', 50), reverse=True)
    
    # Deduplicate by text
    seen = set()
    unique_tasks = []
    for t in all_tasks:
        if t['text'] not in seen:
            seen.add(t['text'])
            unique_tasks.append(t)
    
    # Limit to top 10
    top_tasks = unique_tasks[:10]
    
    lines = [
        f"🤖 **AUTONOMOUS TASK CHECK — {datetime.now().strftime('%H:%M %d/%m/%Y')}**\n",
        f"**{len(unique_tasks)} pending tasks** | Priority mode: ACTIVE\n",
        "━━━━━━━━━━━━━━━━━━━━"
    ]
    
    if top_tasks:
        lines.append("\n📋 **NEXT UP:**")
        next_task = top_tasks[0]
        lines.append(f"  ▶ [{next_task['priority']}] {next_task['text']}")
        lines.append(f"    Type: {next_task.get('type', 'task')} | Source: {next_task.get('source', 'unknown')}")
        
        lines.append("\n📜 **QUEUE:**")
        for i, task in enumerate(top_tasks[1:6], 2):
            lines.append(f"  {i}. [{task['priority']}] {task['text']}")
        
        remaining = len(unique_tasks) - 6
        if remaining > 0:
            lines.append(f"  ... +{remaining} more")
    
    # Show what was completed recently
    recent_completed = state.get('completed_tasks', [])[-3:]
    if recent_completed:
        lines.append("\n✅ **RECENTLY COMPLETED:**")
        for comp in recent_completed:
            dt = datetime.fromisoformat(comp['completed_at']).strftime('%H:%M')
            lines.append(f"  ✓ {comp['text']} @ {dt}")
    
    lines.append("\n━━━━━━━━━━━━━━━━━━━━")
    lines.append("🤖 **AUTONOMOUS MODE: Executing highest priority task...**")
    
    return "\n".join(lines), unique_tasks, top_tasks

def save_last_check(wiki_tasks: Dict, system_tasks: List[Dict], autonomous_tasks: List[Dict], all_tasks: List[Dict], top_tasks: List[Dict]):
    """Save for next run"""
    output_file = Path.home() / ".hermes" / "cron" / "last_task_check.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps({
        'timestamp': datetime.now().isoformat(),
        'wiki_tasks': wiki_tasks,
        'system_tasks': system_tasks,
        'autonomous_tasks': autonomous_tasks,
        'all_tasks': all_tasks,
        'top_tasks': top_tasks,
        'next_task': top_tasks[0] if top_tasks else None
    }, indent=2, ensure_ascii=False))

def main():
    # Load state
    state = load_state()
    
    # Get all task sources
    wiki_tasks = get_wiki_tasks(state)
    system_tasks = get_system_tasks(state)
    autonomous_tasks = get_autonomous_tasks(state)
    
    # Build proposal
    proposal, all_tasks, top_tasks = build_proposal(wiki_tasks, system_tasks, autonomous_tasks, state)
    
    # Print to stdout
    print(proposal)
    
    # Save for next run
    save_last_check(wiki_tasks, system_tasks, autonomous_tasks, all_tasks, top_tasks)
    
    # Save to autonomous log
    log_file = Path.home() / ".hermes" / "cron" / "autonomous.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if top_tasks:
            f.write(f"[{timestamp}] TASKS: {len(all_tasks)} pending | NEXT: {top_tasks[0]['text']} [{top_tasks[0]['priority']}]\n")
        else:
            f.write(f"[{timestamp}] NO TASKS — autonomous learning mode\n")

if __name__ == "__main__":
    main()
