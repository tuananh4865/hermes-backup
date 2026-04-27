#!/usr/bin/env python3
"""
nudge_trigger.py

Triggers self-reflection at key moments:
- Every N tool calls
- On error
- On user correction
- On task completion
- On session end
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class NudgeTrigger:
    """
    Determines when to trigger self-reflection nudges.
    """
    
    DEFAULT_TRIGGERS = {
        "every_10_tool_calls": {
            "condition": "tool_calls_since_nudge >= 10",
            "message": "Review recent actions. What is worth saving?",
        },
        "on_error": {
            "condition": "last_action_was_error == True",
            "message": "Analyze what went wrong. How to prevent?",
        },
        "on_user_correction": {
            "condition": "user_corrected == True",
            "message": "Document the correct approach.",
        },
        "on_complex_task_complete": {
            "condition": "task_complexity > 5 and task_complete == True",
            "message": "Extract reusable pattern from this task?",
        },
        "on_session_end": {
            "condition": "session_ending == True",
            "message": "Update memory with learnings from this session.",
        },
    }
    
    def __init__(self, config_path: str = None):
        self.triggers = self.DEFAULT_TRIGGERS.copy()
        if config_path and Path(config_path).exists():
            with open(config_path) as f:
                self.triggers.update(json.load(f))
                
    def should_nudge(self, state: dict) -> tuple[bool, str]:
        """
        Check if a nudge should fire.
        
        Args:
            state: Dictionary with agent state:
                - tool_calls_since_nudge: int
                - last_action_was_error: bool
                - user_corrected: bool
                - task_complexity: int
                - task_complete: bool
                - session_ending: bool
                
        Returns:
            (should_nudge, nudge_type)
        """
        if state.get("tool_calls_since_nudge", 0) >= 10:
            return True, "periodic_review"
        if state.get("last_action_was_error", False):
            return True, "error_analysis"
        if state.get("user_corrected", False):
            return True, "correction_capture"
        if state.get("task_complexity", 0) > 5 and state.get("task_complete", False):
            return True, "pattern_extraction"
        if state.get("session_ending", False):
            return True, "session_summary"
        return False, None
        
    def get_message(self, nudge_type: str) -> str:
        """Get the nudge message for a trigger type."""
        return self.triggers.get(nudge_type, {}).get(
            "message", 
            "Review recent actions. What is worth saving?"
        )
        
    def format_nudge(self, state: dict) -> str:
        """
        Format a nudge prompt for the agent.
        """
        should_nudge, nudge_type = self.should_nudge(state)
        if not should_nudge:
            return ""
            
        message = self.get_message(nudge_type)
        
        prompt = f"""
[NUDGE - Self-Reflection Triggered: {nudge_type}]

{message}

## Recent Activity Summary
- Tool calls: {state.get('tool_calls_since_nudge', 0)}
- Last error: {state.get('last_error', 'None')}
- User corrections: {state.get('user_corrections', 0)}

## Reflection Questions
1. What worked well in recent actions?
2. What could be improved?
3. Is there a pattern worth documenting as a skill?
4. Should any new information be added to memory?

## Actions Available
- Add to MEMORY.md
- Create new skill
- Update existing skill
- Log mistake to mistakes/
- Update PROJECT_STATE.md
"""
        return prompt


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Nudge trigger")
    parser.add_argument("--tool-calls", type=int, default=0)
    parser.add_argument("--error", action="store_true")
    parser.add_argument("--correction", action="store_true")
    parser.add_argument("--complexity", type=int, default=0)
    parser.add_argument("--complete", action="store_true")
    parser.add_argument("--session-end", action="store_true")
    parser.add_argument("--state", help="JSON state file")
    
    args = parser.parse_args()
    
    if args.state:
        with open(args.state) as f:
            state = json.load(f)
    else:
        state = {
            "tool_calls_since_nudge": args.tool_calls,
            "last_action_was_error": args.error,
            "user_corrected": args.correction,
            "task_complexity": args.complexity,
            "task_complete": args.complete,
            "session_ending": args.session_end,
        }
        
    trigger = NudgeTrigger()
    should_nudge, nudge_type = trigger.should_nudge(state)
    
    print(f"Should nudge: {should_nudge}")
    print(f"Nudge type: {nudge_type}")
    
    if should_nudge:
        print("\n" + trigger.format_nudge(state))


if __name__ == "__main__":
    main()
