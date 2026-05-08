"""
Wiki Session Start Hook — inject wiki context at new session start.

Fires on: session:start, gateway:startup
Action:   Reads wiki files and writes context to ~/.hermes/.wiki_session_context.txt
          for injection into the main agent's system prompt.

Wiki files read (in order):
  1. _meta/start-here.md
  2. SCHEMA.md
  3. index.md
  4. log.md (last 20 lines)
  5. entities/learned-about-{user}.md
  6. memories/TASK_STATE.md (if exists and has content)
  7. memories/DECISION_LOG.md (if exists and has content)

The combined context is read by session.py and run_agent.py during
system prompt assembly.
"""

import logging
from pathlib import Path

logger = logging.getLogger("hooks.wiki-session-start")

WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
CONTEXT_FILE = Path.home() / ".hermes" / ".wiki_session_context.txt"
MEMORIES_DIR = Path.home() / ".hermes" / "memories"


def _read_wiki_files() -> str:
    """Read all wiki session-start files and return combined content."""
    files_to_read = [
        (WIKI_ROOT / "_meta" / "start-here.md", False, "start-here.md"),
        (WIKI_ROOT / "SCHEMA.md", False, "SCHEMA.md"),
        (WIKI_ROOT / "index.md", False, "index.md"),
        (WIKI_ROOT / "log.md", True, "log.md (last 20 lines)"),  # tail only
        (WIKI_ROOT / "entities" / "learned-about-tuananh.md", False, "learned-about-tuananh.md"),
    ]

    parts = []
    for f, tail_only, label in files_to_read:
        if not f.exists():
            logger.warning(f"[wiki-session-start] Wiki file not found: {f}")
            continue
        try:
            if tail_only:
                lines = f.read_text(encoding="utf-8").splitlines()
                content = "\n".join(lines[-20:])
            else:
                content = f.read_text(encoding="utf-8")
            parts.append(f"=== {label} ===\n{content}")
        except Exception as e:
            logger.warning(f"[wiki-session-start] Failed to read {f}: {e}")

    return "\n\n".join(parts)


def _read_memory_files() -> str:
    """Read TASK_STATE.md and DECISION_LOG.md from memories/ directory."""
    parts = []
    
    # TASK_STATE.md — task progress checkpoint
    task_state = MEMORIES_DIR / "TASK_STATE.md"
    if task_state.exists():
        try:
            content = task_state.read_text(encoding="utf-8").strip()
            # Only include if it has actual content (not just template)
            if content and "not started" not in content.lower():
                parts.append(f"=== TASK_STATE.md (from memories/) ===\n{content}")
        except Exception as e:
            logger.warning(f"[wiki-session-start] Failed to read TASK_STATE.md: {e}")

    # DECISION_LOG.md — session decisions
    decision_log = MEMORIES_DIR / "DECISION_LOG.md"
    if decision_log.exists():
        try:
            content = decision_log.read_text(encoding="utf-8").strip()
            if content and "none yet" not in content.lower():
                parts.append(f"=== DECISION_LOG.md (from memories/) ===\n{content}")
        except Exception as e:
            logger.warning(f"[wiki-session-start] Failed to read DECISION_LOG.md: {e}")

    return "\n\n".join(parts)


def handle(event_type: str, context: dict) -> None:
    """
    Sync handler for session:start and gateway:startup events.
    Reads wiki files and writes context to .wiki_session_context.txt.
    """
    platform = context.get("platform", "unknown")
    user_id = context.get("user_id", "unknown")
    session_key = context.get("session_key", "")[:20]

    logger.info(
        f"[wiki-session-start] Event={event_type} platform={platform} user={user_id} session={session_key}"
    )

    if not WIKI_ROOT.exists():
        logger.warning(f"[wiki-session-start] Wiki root not found: {WIKI_ROOT}")
        return

    try:
        # Build wiki context
        wiki_content = _read_wiki_files()
        
        # Append memory files (task state, decision log)
        memory_content = _read_memory_files()
        
        # Combine
        if wiki_content and memory_content:
            combined_content = wiki_content + "\n\n" + memory_content
        elif wiki_content:
            combined_content = wiki_content
        elif memory_content:
            combined_content = memory_content
        else:
            combined_content = ""
            
        if combined_content:
            CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
            CONTEXT_FILE.write_text(combined_content, encoding="utf-8")
            logger.info(
                f"[wiki-session-start] Wrote {len(combined_content)} chars to {CONTEXT_FILE}"
            )
        else:
            logger.warning("[wiki-session-start] No wiki content to write")
    except Exception as e:
        logger.error(f"[wiki-session-start] Failed to write wiki context: {e}")
