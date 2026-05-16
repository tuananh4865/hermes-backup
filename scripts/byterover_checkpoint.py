#!/usr/bin/env python3
"""
ByteRover Agentic Memory Checkpoint

Chạy trước compaction để đảm bảo tất cả kiến thức quan trọng 
trong session hiện tại được lưu vào ByteRover.

Usage: python3 byterover_checkpoint.py [--session-id SID] [--iteration N]
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

HERMES_SESSIONS = Path.home() / ".hermes" / "sessions"
CHECKPOINT_FILE = Path.home() / ".hermes" / "memories" / "session_checkpoint.json"


def get_current_session_state(session_id=None):
    """Đọc session hiện tại và trích xuất state"""
    try:
        # Tìm session file gần nhất
        if not session_id:
            sessions = sorted(HERMES_SESSIONS.glob("session_*.json"), 
                            key=lambda f: f.stat().st_mtime, reverse=True)
            if sessions:
                session_id = sessions[0].stem.replace("session_", "")
        
        session_file = HERMES_SESSIONS / f"session_{session_id}.json"
        if not session_file.exists():
            return None
            
        with open(session_file) as f:
            data = json.load(f)
        
        # Trích xuất thông tin quan trọng
        state = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "turns": len(data.get("messages", [])),
            "pending_tasks": [],
            "decisions": [],
            "learnings": [],
            "active_work": None,
        }
        
        messages = data.get("messages", [])
        
        # Tìm kiếm pending tasks, decisions, learnings
        for msg in messages[-20:]:  # Chỉ check 20 messages gần nhất
            content = ""
            if isinstance(msg, dict):
                content = msg.get("content", "") or msg.get("text", "") or ""
                if isinstance(content, list):
                    content = " ".join(str(c) for c in content)
            
            # Extract patterns
            if "pending" in content.lower() or "đang làm" in content.lower():
                state["active_work"] = content[:200]
            
            if any(kw in content.lower() for kw in ["decided", "chose", "quyết định"]):
                state["decisions"].append(content[:150])
            
            if any(kw in content.lower() for kw in ["learned", "học được", "discovered"]):
                state["learnings"].append(content[:150])
        
        return state
        
    except Exception as e:
        return None


def checkpoint_to_byterover(state):
    """Curate session state vào ByteRover"""
    if not state:
        return False
    
    try:
        # Curate session summary
        session_id = state.get("session_id", "unknown")
        turns = state.get("turns", 0)
        timestamp = state.get("timestamp", "")
        
        cmd = [
            "brv", "curate", 
            f"session_checkpoint: sid={session_id}, turns={turns}, {timestamp}", 
            "--detach"
        ]
        subprocess.run(cmd, capture_output=True, timeout=5)
        
        # Curate active work
        if state.get("active_work"):
            cmd = [
                "brv", "curate",
                f"active_work: {state['active_work'][:200]}",
                "--detach"
            ]
            subprocess.run(cmd, capture_output=True, timeout=5)
        
        # Curate learnings
        for learning in state.get("learnings", [])[:5]:
            if len(learning) > 20:
                cmd = [
                    "brv", "curate",
                    f"learning: {learning[:200]}",
                    "--detach"
                ]
                subprocess.run(cmd, capture_output=True, timeout=5)
        
        # Curate decisions
        for decision in state.get("decisions", [])[:5]:
            if len(decision) > 20:
                cmd = [
                    "brv", "curate",
                    f"decision: {decision[:200]}",
                    "--detach"
                ]
                subprocess.run(cmd, capture_output=True, timeout=5)
        
        return True
        
    except Exception as e:
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--iteration", type=int, default=None)
    args = parser.parse_args()
    
    # Check iteration - if we're past threshold, checkpoint
    if args.iteration and args.iteration < 50:
        print(f"[Checkpoint] Iteration {args.iteration} - skipping (not near compaction)")
        return
    
    print(f"[ByteRover Checkpoint] Saving session state to ByteRover...")
    
    # Get current state
    state = get_current_session_state(args.session_id)
    
    if state:
        # Save checkpoint locally first
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(state, f, indent=2)
        
        # Curate to ByteRover
        success = checkpoint_to_byterover(state)
        
        if success:
            print(f"[Checkpoint] ✓ Saved {state['turns']} turns, {len(state['learnings'])} learnings")
        else:
            print("[Checkpoint] ✗ Failed to curate to ByteRover")
    else:
        print("[Checkpoint] No active session found")


if __name__ == "__main__":
    main()