#!/usr/bin/env python3
"""
wiki_hooks.py

Event-driven automation engine for wiki operations.

Hooks:
- on_ingest: fired when new source is added
- on_session_start: fired when session begins
- on_session_end: fired when session ends
- on_schedule: fired on periodic schedule
- on_query: fired when question is asked
- on_memory_write: fired when memory is updated
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional


class WikiHooks:
    """Event-driven automation engine."""
    
    HOOK_TYPES = [
        "on_ingest",         # New source added
        "on_session_start",   # Session begins
        "on_session_end",     # Session ends
        "on_schedule",        # Periodic trigger
        "on_query",           # Question asked
        "on_memory_write",    # Memory updated
    ]
    
    def __init__(self, config_path: str = None):
        self.hooks = {hook_type: [] for hook_type in self.HOOK_TYPES}
        self.config_path = config_path
        self.load_hooks()
        
    def load_hooks(self):
        """Load hook configurations."""
        if self.config_path and Path(self.config_path).exists():
            with open(self.config_path) as f:
                config = json.load(f)
                for hook_type, actions in config.get("hooks", {}).items():
                    if hook_type in self.hooks:
                        self.hooks[hook_type] = actions
                        
    def register(self, hook_type: str, action: str, skill: str = None):
        """
        Register a hook action.
        
        Args:
            hook_type: One of HOOK_TYPES
            action: Description of action to take
            skill: Optional skill to invoke
        """
        if hook_type not in self.hooks:
            raise ValueError(f"Unknown hook type: {hook_type}")
            
        self.hooks[hook_type].append({
            "action": action,
            "skill": skill,
            "registered_at": datetime.now().isoformat()
        })
        
    def trigger(self, hook_type: str, context: dict = None) -> list:
        """
        Trigger all actions for a hook type.
        
        Args:
            hook_type: Hook to trigger
            context: Context data for the hook
            
        Returns:
            List of results from each action
        """
        if hook_type not in self.hooks:
            return []
            
        results = []
        context = context or {}
        context["hook_type"] = hook_type
        context["triggered_at"] = datetime.now().isoformat()
        
        for hook in self.hooks[hook_type]:
            result = {
                "action": hook["action"],
                "skill": hook.get("skill"),
                "context": context,
                "status": "pending"
            }
            
            # Execute the hook action
            # In a full implementation, this would invoke skills or scripts
            result["status"] = "triggered"
            results.append(result)
            
        return results
        
    def list_hooks(self) -> dict:
        """List all registered hooks."""
        return self.hooks
        
    def clear(self, hook_type: str = None):
        """Clear hooks for a type, or all if no type specified."""
        if hook_type:
            self.hooks[hook_type] = []
        else:
            for hook_type in self.hooks:
                self.hooks[hook_type] = []


def on_ingest(wiki_path: str, source_name: str, source_type: str = "unknown") -> dict:
    """
    Triggered when a new source is added to the wiki.
    
    Actions:
    1. Extract entities from source
    2. Update knowledge graph
    3. Update wiki index
    4. Check for contradictions
    """
    print(f"[HOOK] on_ingest: {source_name}")
    
    context = {
        "wiki_path": wiki_path,
        "source_name": source_name,
        "source_type": source_type
    }
    
    # In full implementation:
    # 1. Run entity_extractor.py on the source
    # 2. Run knowledge_graph.py to add entities
    # 3. Update index
    # 4. Check for contradictions
    
    return {
        "hook": "on_ingest",
        "source": source_name,
        "actions_triggered": [
            "entity_extraction",
            "graph_update",
            "index_update",
            "contradiction_check"
        ]
    }


def on_session_start(wiki_path: str, project_name: str = None) -> dict:
    """
    Triggered when a session begins.
    
    Actions:
    1. Load project state if available
    2. Check for in-progress work
    3. Load relevant context
    """
    print(f"[HOOK] on_session_start")
    
    context = {
        "wiki_path": wiki_path,
        "project_name": project_name
    }
    
    # In full implementation:
    # 1. Read PROJECT_STATE.md if exists
    # 2. Load recent session summaries
    # 3. Check for pending tasks
    
    return {
        "hook": "on_session_start",
        "project": project_name,
        "actions_triggered": [
            "load_project_state",
            "check_pending_tasks",
            "load_recent_context"
        ]
    }


def on_session_end(wiki_path: str, summary: str = None) -> dict:
    """
    Triggered when a session ends.
    
    Actions:
    1. Update project state
    2. Compress observations to episodic memory
    3. Log any decisions made
    4. Update memory
    """
    print(f"[HOOK] on_session_end")
    
    context = {
        "wiki_path": wiki_path,
        "summary": summary
    }
    
    # In full implementation:
    # 1. Update PROJECT_STATE.md
    # 2. Create episodic memory in memories/sessions/
    # 3. Log decisions
    # 4. Update MEMORY.md
    
    return {
        "hook": "on_session_end",
        "actions_triggered": [
            "update_project_state",
            "compress_episodic",
            "log_decisions",
            "update_memory"
        ]
    }


def on_schedule(event_type: str = "daily") -> dict:
    """
    Triggered on periodic schedule.
    
    Actions:
    - Daily: Quick health check
    - Weekly: Deep review
    """
    print(f"[HOOK] on_schedule: {event_type}")
    
    if event_type == "daily":
        actions = [
            "quick_lint",
            "stale_check",
            "backup"
        ]
    elif event_type == "weekly":
        actions = [
            "deep_review",
            "skill_updates",
            "consolidation",
            "stats_report"
        ]
    else:
        actions = ["periodic_maintenance"]
        
    return {
        "hook": "on_schedule",
        "event_type": event_type,
        "actions_triggered": actions
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Wiki hooks automation")
    parser.add_argument("--init", action="store_true", help="Initialize hooks config")
    parser.add_argument("--list", action="store_true", help="List all hooks")
    parser.add_argument("--trigger", help="Trigger a hook type")
    parser.add_argument("--config", help="Config file path")
    
    args = parser.parse_args()
    
    hooks = WikiHooks(args.config)
    
    if args.init:
        # Create default config
        config = {
            "hooks": {
                "on_ingest": [],
                "on_session_start": [],
                "on_session_end": [],
                "on_schedule": [],
                "on_query": [],
                "on_memory_write": []
            }
        }
        print(json.dumps(config, indent=2))
        
    if args.list:
        print(json.dumps(hooks.list_hooks(), indent=2))
        
    if args.trigger:
        results = hooks.trigger(args.trigger)
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
