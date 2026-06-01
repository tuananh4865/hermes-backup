"""
Session Resume Injector Hook

Fires on: session:start, session:reset
Action:   On session:start, reads the most recent transcript file(s) and
          injects recent session summary + last 5 messages into the
          session context file for the agent to resume seamlessly.

What it injects:
  1. Recent session summary (from previous session's last transcript)
  2. Last 5 messages from previous session (if available)
  3. Current task/intent context (if stored in TASK_STATE.md)

The context file is read by session.py and prepended to the system prompt.
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

# Path constants
WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
TRANSCRIPTS_DIR = WIKI_ROOT / "raw" / "transcripts"
MEMORIES_DIR = Path.home() / ".hermes" / "memories"
CONTEXT_FILE = Path.home() / ".hermes" / ".recent_session_context.txt"


def get_most_recent_transcript_dir():
    """Find the most recent transcript directory."""
    if not TRANSCRIPTS_DIR.exists():
        return None
    
    # Get directories sorted by name (date) descending
    dirs = [d for d in TRANSCRIPTS_DIR.iterdir() if d.is_dir()]
    if not dirs:
        return None
    
    dirs.sort(key=lambda x: x.name, reverse=True)
    return dirs[0]


def get_recent_transcript_files(limit=3):
    """Get the most recent transcript files across all dates."""
    if not TRANSCRIPTS_DIR.exists():
        return []
    
    all_files = []
    for d in TRANSCRIPTS_DIR.iterdir():
        if d.is_dir():
            for f in d.glob("*.md"):
                all_files.append(f)
    
    # Sort by modification time, newest first
    all_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return all_files[:limit]


def parse_transcript_for_summary(filepath):
    """
    Parse a transcript file and extract:
    1. Session summary (title/topic)
    2. Last 5 messages (user + assistant alternating)
    """
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        messages = []
        current_role = None
        current_content = []
        
        for line in lines:
            if line.startswith("## User Message"):
                if current_role and current_content:
                    messages.append({"role": current_role, "content": "\n".join(current_content)})
                current_role = "user"
                current_content = []
            elif line.startswith("## Assistant Response"):
                if current_role and current_content:
                    messages.append({"role": current_role, "content": "\n".join(current_content)})
                current_role = "assistant"
                current_content = []
            elif line.startswith("---") or line.startswith("title:") or line.startswith("created:") or line.startswith("platform:") or line.startswith("user_id:") or line.startswith("session_id:") or line.startswith("timestamp:") or line.startswith("type:") or line.startswith("tags:") or line.startswith("_Saved"):
                continue
            else:
                if current_role:
                    current_content.append(line)
        
        # Add last message block
        if current_role and current_content:
            messages.append({"role": current_role, "content": "\n".join(current_content)})
        
        # Take last 5 messages
        last_5 = messages[-5:] if len(messages) > 5 else messages
        
        # Extract session topic from filename or first user message
        session_topic = filepath.stem
        if last_5 and last_5[0].get("role") == "user":
            # Use first user message as topic indicator
            first_msg = last_5[0]["content"][:80]
            session_topic = f"Previous session: {first_msg}..."
        
        return {
            "topic": session_topic,
            "messages": last_5
        }
        
    except Exception as e:
        return {"topic": f"Error reading transcript: {e}", "messages": []}


def read_task_state():
    """Read current task state from TASK_STATE.md."""
    task_state_file = MEMORIES_DIR / "TASK_STATE.md"
    if not task_state_file.exists():
        return None
    
    try:
        content = task_state_file.read_text(encoding="utf-8").strip()
        if content and "not started" not in content.lower() and "none yet" not in content.lower():
            return content
        return None
    except Exception:
        return None


def read_decision_log():
    """Read recent decisions from DECISION_LOG.md."""
    decision_log_file = MEMORIES_DIR / "DECISION_LOG.md"
    if not decision_log_file.exists():
        return None
    
    try:
        content = decision_log_file.read_text(encoding="utf-8").strip()
        if content and "none yet" not in content.lower():
            lines = content.splitlines()
            # Get last 10 lines
            recent = lines[-10:] if len(lines) > 10 else lines
            return "\n".join(recent)
        return None
    except Exception:
        return None


def build_context_summary():
    """Build the full context summary for session resume."""
    parts = []
    
    # Header
    parts.append("=" * 60)
    parts.append("SESSION RESUME CONTEXT (Auto-injected after context overflow)")
    parts.append("=" * 60)
    parts.append("")
    
    # Get most recent transcripts
    recent_files = get_recent_transcript_files(limit=3)
    
    if recent_files:
        parts.append("## RECENT SESSIONS:")
        parts.append("")
        
        for i, filepath in enumerate(recent_files):
            transcript_data = parse_transcript_for_summary(filepath)
            parts.append(f"### [{i+1}] {filepath.parent.name}/{filepath.name}")
            parts.append(f"Topic: {transcript_data['topic']}")
            parts.append("")
            
            # Add last 5 messages
            if transcript_data['messages']:
                parts.append("Last messages:")
                for msg in transcript_data['messages']:
                    role_label = "👤 User" if msg['role'] == 'user' else "🤖 Assistant"
                    # Truncate each message to 300 chars for context size
                    msg_content = msg['content'][:300]
                    if len(msg['content']) > 300:
                        msg_content += "..."
                    parts.append(f"  {role_label}: {msg_content}")
                parts.append("")
    else:
        parts.append("## No recent transcript files found.")
        parts.append("")
    
    # Add task state if available
    task_state = read_task_state()
    if task_state:
        parts.append("## CURRENT TASK STATE:")
        parts.append(task_state)
        parts.append("")
    
    # Add decision log if available
    decision_log = read_decision_log()
    if decision_log:
        parts.append("## RECENT DECISIONS:")
        parts.append(decision_log)
        parts.append("")
    
    # Footer
    parts.append("=" * 60)
    parts.append("END OF RESUME CONTEXT")
    parts.append("=" * 60)
    
    return "\n".join(parts)


def handle(event_type: str, context: dict) -> None:
    """
    Handler for session:start and session:reset events.
    Builds and writes session resume context to .recent_session_context.txt.
    """
    platform = context.get("platform", "unknown")
    user_id = context.get("user_id", "unknown")
    session_key = context.get("session_key", "unknown")[:20]
    
    print(
        f"[session-resume-injector] Event={event_type} "
        f"platform={platform} user={user_id} session={session_key}",
        flush=True
    )
    
    try:
        # Build the context summary
        context_content = build_context_summary()
        
        # Write to context file
        CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONTEXT_FILE.write_text(context_content, encoding="utf-8")
        
        print(
            f"[session-resume-injector] Wrote {len(context_content)} chars "
            f"resume context to {CONTEXT_FILE}",
            flush=True
        )
        
    except Exception as e:
        print(f"[session-resume-injector] Error building session context: {e}", flush=True)