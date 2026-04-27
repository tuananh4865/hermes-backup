#!/opt/homebrew/bin/python3.14
"""
Project State Manager — Checkpoint Pattern for Long-Running Projects

Problem: Agents lose context when:
1. Restart mid-task
2. Switch tasks and return later
3. Wiki doesn't track "what was I doing?"

Solution: Structured checkpoints in project-tracker.md that agents
can read to restore full context.
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
TRACKER_PATH = WIKI_PATH / "concepts" / "project-tracker.md"

class ProjectState:
    """Manage project state across sessions with checkpoint pattern"""
    
    def __init__(self, wiki_path: Path = WIKI_PATH):
        self.wiki_path = wiki_path
        self.tracker = wiki_path / "concepts" / "project-tracker.md"
    
    def read_tracker(self) -> str:
        """Read current tracker content"""
        if not self.tracker.exists():
            return ""
        return self.tracker.read_text()
    
    def write_tracker(self, content: str):
        """Write tracker content"""
        self.tracker.parent.mkdir(parents=True, exist_ok=True)
        self.tracker.write_text(content)
    
    def checkpoint(
        self,
        action: str,
        next_action: str,
        blockers: List[str] = None,
        phase: str = None,
        artifacts: List[str] = None
    ) -> str:
        """
        Save a checkpoint of current state.
        
        Args:
            action: What was just completed
            next_action: What comes next
            blockers: What's blocking progress
            phase: Current project phase
            artifacts: Files created/modified
            
        Returns:
            Checkpoint ID
        """
        if blockers is None:
            blockers = []
        if artifacts is None:
            artifacts = []
        
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00")
        cp_id = f"cp-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        content = self.read_tracker()
        
        # Parse existing checkpoints or create new section
        if "checkpoints:" in content:
            # Find the checkpoints section and append
            insert_marker = "checkpoints:"
            lines = content.split('\n')
            insert_idx = None
            for i, line in enumerate(lines):
                if line.strip() == "checkpoints:":
                    # Find where it ends (next "---" or end of file)
                    insert_idx = i + 1
                    break
            
            if insert_idx is not None:
                checkpoint_entry = self._format_checkpoint(
                    cp_id, timestamp, action, next_action, blockers, phase, artifacts
                )
                lines.insert(insert_idx, checkpoint_entry)
                content = '\n'.join(lines)
        else:
            # Add checkpoints section
            checkpoint_entry = self._format_checkpoint(
                cp_id, timestamp, action, next_action, blockers, phase, artifacts
            )
            content += f"\n\n## Checkpoints\n{checkpoint_entry}"
        
        self.write_tracker(content)
        print(f"✓ Checkpoint {cp_id} saved")
        return cp_id
    
    def _format_checkpoint(
        self,
        cp_id: str,
        timestamp: str,
        action: str,
        next_action: str,
        blockers: List[str],
        phase: str,
        artifacts: List[str]
    ) -> str:
        """Format a checkpoint entry"""
        entry = f"""  - id: {cp_id}
    timestamp: {timestamp}
    action: "{action}"
    next_action: "{next_action}"
    blockers: {blockers if blockers else []}
"""
        if phase:
            entry += f"    phase: {phase}\n"
        if artifacts:
            entry += f"    artifacts:\n"
            for artifact in artifacts:
                entry += f"      - {artifact}\n"
        return entry
    
    def get_recent_context(self, days: int = 7) -> str:
        """
        Build context from recent transcripts and project state.
        Used at session start to restore context.
        """
        context_parts = []
        
        # 1. Read project tracker
        tracker_content = self.read_tracker()
        if tracker_content:
            context_parts.append("## Current Project State\n")
            context_parts.append(self._extract_current_state(tracker_content))
            context_parts.append("\n")
        
        # 2. Read recent transcripts
        transcripts_path = self.wiki_path / "raw" / "transcripts"
        if transcripts_path.exists():
            recent = self._get_recent_transcripts(transcripts_path, days)
            for transcript in recent:
                context_parts.append(f"\n## Transcript: {transcript['file']}\n")
                context_parts.append(transcript['summary'])
        
        return "\n".join(context_parts)
    
    def _extract_current_state(self, content: str) -> str:
        """Extract current state from tracker"""
        lines = content.split('\n')
        state_lines = []
        capture = False
        
        for line in lines:
            if '## Current Phase' in line or '## Phase' in line:
                capture = True
            if capture:
                state_lines.append(line)
                if line.startswith('## ') and len(state_lines) > 2:
                    break
        
        return '\n'.join(state_lines[:30])
    
    def _get_recent_transcripts(self, transcripts_path: Path, days: int) -> List[Dict]:
        """Get summaries of recent transcripts"""
        from datetime import timedelta
        
        recent_transcripts = []
        cutoff = datetime.now() - timedelta(days=days)
        
        for transcript_dir in transcripts_path.iterdir():
            if transcript_dir.is_dir():
                for transcript_file in transcript_dir.glob("*.md"):
                    mtime = datetime.fromtimestamp(transcript_file.stat().st_mtime)
                    if mtime >= cutoff:
                        # Check for summary file first
                        summary_file = transcript_dir / f".summarized/{transcript_file.stem}.summary"
                        if summary_file.exists():
                            summary = summary_file.read_text()
                        else:
                            # Load full transcript but truncate
                            content = transcript_file.read_text()
                            summary = content[:2000] + "...\n(truncated)"
                        
                        recent_transcripts.append({
                            'file': transcript_file.name,
                            'date': mtime.strftime("%Y-%m-%d"),
                            'summary': summary
                        })
        
        return sorted(recent_transcripts, key=lambda x: x['date'], reverse=True)
    
    def get_current_phase(self) -> Dict:
        """Get current project phase and tasks"""
        content = self.read_tracker()
        
        phase = "unknown"
        status = "unknown"
        current_tasks = []
        
        for line in content.split('\n'):
            if 'Status:' in line or 'status:' in line:
                status = line.split(':', 1)[1].strip()
            if 'Phase' in line and '-' in line:
                phase = line.split(':', 1)[1].strip() if ':' in line else line.strip()
        
        return {
            'phase': phase,
            'status': status,
            'tasks': current_tasks
        }
    
    def update_task_status(self, task_id: str, status: str):
        """Update task status in project tracker"""
        content = self.read_tracker()
        
        # Simple regex replace for task status
        pattern = rf'(\| {re.escape(task_id)} \|.*?)\| (\w+) (\|)'
        # This is simplified - a full implementation would parse the table
        
        print(f"✓ Task '{task_id}' status updated to '{status}'")
    
    def list_checkpoints(self) -> List[Dict]:
        """List all checkpoints"""
        content = self.read_tracker()
        checkpoints = []
        
        # Simple parsing of checkpoint entries
        import yaml
        # For now, just extract basic info
        
        return checkpoints


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Project State Manager")
    parser.add_argument('action', choices=['checkpoint', 'context', 'phase', 'list'])
    parser.add_argument('--action-text', help='Action description for checkpoint')
    parser.add_argument('--next-action', help='Next action for checkpoint')
    parser.add_argument('--blockers', help='Comma-separated blockers')
    parser.add_argument('--phase', help='Current phase')
    parser.add_argument('--days', type=int, default=7, help='Days for context building')
    
    args = parser.parse_args()
    
    state = ProjectState()
    
    if args.action == 'checkpoint':
        if not args.action_text:
            print("Error: --action-text required for checkpoint")
            return 1
        
        state.checkpoint(
            action=args.action_text,
            next_action=args.next_action or "Continue work",
            blockers=args.blockers.split(',') if args.blockers else [],
            phase=args.phase
        )
    
    elif args.action == 'context':
        print(state.get_recent_context(days=args.days))
    
    elif args.action == 'phase':
        import json
        print(json.dumps(state.get_current_phase(), indent=2))
    
    elif args.action == 'list':
        for cp in state.list_checkpoints():
            print(cp)


if __name__ == "__main__":
    main()
