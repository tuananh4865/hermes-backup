"""
Wiki Memory Provider — Active Write Loop for Hermes Agent

Enhancements (2026-05-06):
  - sync_turn(): accumulate conversation, write rolling checkpoint every N turns
  - on_session_end(): extract session summary → wiki/log.md + TASK_STATE.md
  - on_pre_compress(): write structured checkpoint BEFORE compression
  - Rolling checkpoint → ~/.hermes/checkpoints/session_state_<id>.md
  - Auto-extract to MEMORY.md via BuiltinMemoryStore mirroring

Wiki path: /Volumes/Storage-1/Hermes/wiki (configurable via WIKI_ROOT env var)
"""

from __future__ import annotations

import json
import logging
import os
import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Default wiki root
DEFAULT_WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
DEFAULT_HERMES_HOME = Path.home() / ".hermes"

# Structured USER.md format — Phase 1: Mem0-style entity memory
USER_PROFILE_TEMPLATE = """§ [PREFERENCES] — explicit preferences discovered over sessions
[PREFERENCES]
- communication: Vietnamese casual
- response_style: concise, no fluff
- tiktok_script_style: "anh" + "mấy con vợ"
§ [PROJECTS] — ongoing work
[PROJECTS]
§ [FACTS] — durable facts about user, environment, tools
[FACTS]
§ [SESSIONS] — session history summaries
[SESSIONS]
§ [ENTITY_INDEX] — cross-session entity tracking (Phase 5)
[ENTITY_INDEX]
§ [GROWTH_LOG] — how user/agent improved
[GROWTH_LOG]
"""

# Files to read at session start (in order)
WIKI_STARTUP_FILES = [
    ("_meta/start-here.md", False),
    ("SCHEMA.md", False),
    ("index.md", False),
    ("log.md", True),  # last 20 lines only
    ("entities/learned-about-tuananh.md", False),
]

# Checkpoint settings
CHECKPOINT_DIR = DEFAULT_HERMES_HOME / "checkpoints"
CHECKPOINT_EVERY_N_TURNS = 5  # Write checkpoint every N turns


def _get_wiki_root() -> Path:
    return Path(os.environ.get("WIKI_ROOT", str(DEFAULT_WIKI_ROOT)))


def _get_hermes_home() -> Path:
    from hermes_constants import get_hermes_home
    return Path(get_hermes_home())


class WikiMemoryProvider:
    """Memory provider that injects wiki context AND actively writes session state."""

    name = "wiki"

    def __init__(self) -> None:
        # System prompt / wiki context
        self._system_prompt_block: str = ""
        self._session_id: str = ""
        self._session_cache: Dict[str, str] = {}

        # Active write loop state
        self._conversation_buffer: List[Dict[str, str]] = []
        self._turn_count: int = 0
        self._tool_call_count: int = 0
        self._checkpoint_lock = threading.Lock()
        self._last_checkpoint_turn: int = 0
        self._current_task: str = ""
        self._files_modified: List[str] = []
        self._decisions: List[str] = []
        self._blocked: List[str] = []
        self._next_steps: List[str] = []
        self._session_start_time: Optional[datetime] = None
        self._checkpoint_thread: Optional[threading.Thread] = None

    def is_available(self) -> bool:
        wiki_root = _get_wiki_root()
        available = wiki_root.exists() and wiki_root.is_dir()
        logger.info("[wiki] is_available=%s (root=%s)", available, wiki_root)
        return available

    def initialize(self, session_id: str, **kwargs) -> None:
        self._session_id = session_id
        self._session_start_time = datetime.now()
        self._turn_count = 0
        self._tool_call_count = 0
        self._last_checkpoint_turn = 0
        self._conversation_buffer = []
        self._current_task = ""
        self._files_modified = []
        self._decisions = []
        self._blocked = []
        self._next_steps = []
        self._session_cache = {}

        # Ensure checkpoint directory exists
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

        # Ensure memories directory and structured USER.md exist (Phase 1)
        mem_dir = Path.home() / ".hermes" / "memories"
        mem_dir.mkdir(parents=True, exist_ok=True)
        user_file = mem_dir / "USER.md"
        if not user_file.exists():
            user_file.write_text(USER_PROFILE_TEMPLATE, encoding="utf-8")
            logger.info("[wiki] Created structured USER.md")

        self._load_wiki_context()
        self._load_project_summary()
        self._warm_session_search()

    # ─── Original Methods ───────────────────────────────────────────

    def _load_wiki_context(self) -> None:
        wiki_root = _get_wiki_root()
        parts = ["## Wiki Knowledge Base\n"]

        for rel_path, last_lines_only in WIKI_STARTUP_FILES:
            full_path = wiki_root / rel_path
            if not full_path.exists():
                logger.debug("[wiki] skipping missing: %s", full_path)
                continue

            try:
                if last_lines_only:
                    lines = full_path.read_text(encoding="utf-8").splitlines()
                    content = "\n".join(lines[-20:])
                else:
                    content = full_path.read_text(encoding="utf-8")
            except Exception as e:
                logger.debug("[wiki] could not read %s: %s", full_path, e)
                continue

            if content.strip():
                label = rel_path.replace(".md", "").replace("_meta/", "").replace("entities/", "")
                label = label.replace("-", " ").replace("_", " ").title()
                parts.append(f"### {label}\n{content.strip()}\n\n")

        self._system_prompt_block = "\n".join(parts)
        logger.info("[wiki] Loaded %d wiki files, block size=%d chars",
                    len(WIKI_STARTUP_FILES), len(self._system_prompt_block))

    def _warm_session_search(self) -> None:
        try:
            from hermes_state import SessionDB
            from hermes_cli.config import get_hermes_home
            db_path = get_hermes_home() / "state.db"
            db = SessionDB(db_path=db_path)
            from tools.session_search_tool import session_search as _ss
            result = _ss(query="Tuấn Anh", limit=3, db=db)
            try:
                parsed = json.loads(result)
                if parsed.get("success"):
                    self._session_cache["recent_sessions"] = result
                    logger.info("[wiki] session_search warm-up done, got %d chars", len(result))
                else:
                    logger.warning("[wiki] session_search returned success=false")
                    self._session_cache["recent_sessions"] = ""
            except (json.JSONDecodeError, TypeError):
                self._session_cache["recent_sessions"] = result
                logger.info("[wiki] session_search warm-up done, got %d chars", len(result))
        except Exception as e:
            logger.warning("[wiki] session_search warm-up failed: %s", e)
            self._session_cache["recent_sessions"] = ""

    def _load_project_summary(self) -> None:
        """Scan projects/ directory and append active project summary to system_prompt_block."""
        try:
            wiki_root = _get_wiki_root()
            projects_dir = wiki_root / "projects"
            if not projects_dir.exists():
                return

            active = []
            for subdir in sorted(projects_dir.iterdir()):
                if not subdir.is_dir() or subdir.name.startswith("_"):
                    continue
                hub = subdir / "hub.md"
                if hub.exists():
                    content = hub.read_text(encoding="utf-8", errors="replace")
                    # Extract key metadata
                    title = subdir.name.replace("-", " ").replace("_", " ").title()
                    status = ""
                    phase = ""
                    updated = ""
                    for line in content.split("\n")[:30]:
                        if line.startswith("**Status**:"):
                            status = line.split("**Status**:")[1].strip()
                        elif line.startswith("**Phase**:"):
                            phase = line.split("**Phase**:")[1].strip()
                        elif line.startswith("updated:"):
                            updated = line.replace("updated:", "").strip()
                    entry = f"- `{subdir.name}`"
                    if status:
                        entry += f" [{status}]"
                    if phase:
                        entry += f" — {phase}"
                    active.append(entry)

            if active:
                projects_block = "\n### Projects\n" + "\n".join(active) + "\n"
                self._system_prompt_block += projects_block
                logger.info("[wiki] Scanned %d active projects", len(active))
        except Exception as e:
            logger.debug("[wiki] _load_project_summary failed: %s", e)

    def _git_push_async(self) -> None:
        """
        Non-blocking git add + push to my-llm-wiki.
        Runs in background thread so it never blocks the agent.
        """
        import subprocess
        try:
            wiki_root = _get_wiki_root()
            result = subprocess.run(
                ["git", "add", "-A"],
                cwd=str(wiki_root),
                capture_output=True,
                timeout=30,
            )
            if result.returncode != 0:
                logger.warning("[wiki] git add failed: %s", result.stderr.decode())
                return
            result = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                cwd=str(wiki_root),
                capture_output=True,
                timeout=10,
            )
            if not result.stdout.strip():
                logger.debug("[wiki] No changes to push")
                return
            result = subprocess.run(
                ["git", "commit", "-m", f"[auto] Wiki sync {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
                cwd=str(wiki_root),
                capture_output=True,
                timeout=30,
                env={**__import__("os").environ, "GIT_AUTHOR_NAME": "HermesAgent", "GIT_AUTHOR_EMAIL": "hermes@tuananh.local"},
            )
            result = subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=str(wiki_root),
                capture_output=True,
                timeout=60,
            )
            if result.returncode == 0:
                logger.info("[wiki] Auto-push to GitHub succeeded")
            else:
                logger.warning("[wiki] git push failed: %s", result.stderr.decode())
        except Exception as e:
            logger.debug("[wiki] _git_push_async failed: %s", e)

    def _trigger_git_push(self) -> None:
        """Trigger non-blocking git push (for on_session_end)."""
        t = threading.Thread(target=self._git_push_async, daemon=True, name="wiki-git-push")
        t.start()

    _last_push_time: float = 0.0

    def _maybe_git_push(self) -> None:
        """Rate-limited: only push if 5+ minutes since last push."""
        import time
        now = time.monotonic()
        if now - self._last_push_time < 300:  # 5 minutes
            return
        self._last_push_time = now
        t = threading.Thread(target=self._git_push_async, daemon=True, name="wiki-git-push-rate-limited")
        t.start()

    def system_prompt_block(self) -> str:
        return self._system_prompt_block

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        """
        Called by AIAgent to get relevant memory context for the current query.
        Uses hybrid BM25+semantic retrieval + Phase 3 smart topic parsing.
        """
        parts = []
        
        # Phase 3: Smart topic parsing — extract topics from query
        if query:
            topics = self._parse_session_start_topics(query)
            if topics:
                # Fetch memories for each topic
                topic_memories = self._fetch_session_start_memories(topics)
                if topic_memories:
                    parts.append(topic_memories)
            else:
                # Fallback to hybrid retrieval
                retrieved = self.retrieve_relevant_memory(query, k=8)
                if retrieved:
                    parts.append(retrieved)
        
        # Get recent sessions cache
        cached = self._session_cache.get("recent_sessions", "")
        if cached:
            parts.append(f"### Recent Session Context\n{cached}\n")

        # Proactive retrieval: if we have cached context from on_post_compress,
        # inject it here so the next turn continues seamlessly after compression
        if self._session_cache.get("has_proactive_context"):
            proactive_topics = self._session_cache.get("proactive_topics", [])
            for topic in proactive_topics:
                cached_proactive = self._session_cache.get(f"proactive_{topic}", "")
                if cached_proactive:
                    parts.append(cached_proactive)

        return "\n\n".join(parts) if parts else ""

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        return []

    # ─── NEW: Active Write Loop ─────────────────────────────────────

    def sync_turn(self, user_content: str, assistant_content: str, *, session_id: str = "") -> None:
        """
        Called after each completed turn. Accumulates conversation and triggers
        rolling checkpoint every N tool calls. Non-blocking.
        """
        self._turn_count += 1

        # Accumulate conversation
        self._conversation_buffer.append({
            "role": "user",
            "content": user_content[:500] if user_content else "",
            "turn": self._turn_count,
        })
        self._conversation_buffer.append({
            "role": "assistant",
            "content": assistant_content[:1000] if assistant_content else "",
            "turn": self._turn_count,
        })

        # Parse task from first user message
        if self._turn_count == 1 and user_content:
            self._current_task = self._parse_intent(user_content)

        # Track tool calls in assistant response
        if assistant_content:
            self._track_tool_calls(assistant_content)
            self._track_decisions(assistant_content)

        # Trigger rolling checkpoint every N turns
        if self._turn_count - self._last_checkpoint_turn >= CHECKPOINT_EVERY_N_TURNS:
            self._trigger_rolling_checkpoint()

        # REAL-TIME: Write quick fact to MEMORY.md every turn
        self._sync_fact_realtime()

    def _sync_fact_realtime(self) -> None:
        """
        REAL-TIME memory sync — writes key facts to MEMORY.md after EVERY turn.
        
        This ensures that even if context compresses or session ends abruptly,
        the most important facts are already persisted.
        
        Strategy:
        - Read existing MEMORY.md
        - If current task/decisions are NOT already present, add them
        - Keep only last 20 entries (bounded)
        - Fast path: no LLM, just file I/O
        """
        try:
            memory_file = self.MEMORY_FILE
            memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            existing = self._read_memory_entries(memory_file)
            
            # Check if current task is already recorded (avoid duplicates)
            new_fact = None
            if self._current_task:
                task_preview = self._current_task[:120].replace("\n", " ").strip()
                # Look for similar entry (first 60 chars should match)
                already_recorded = any(
                    e.startswith(f"Task '{task_preview[:60]}") for e in existing
                )
                if not already_recorded:
                    new_fact = f"Task '{task_preview}' — {self._turn_count} turns"
            
            # Also check if recent decisions need recording
            if not new_fact and self._decisions:
                last_decision = self._decisions[-1][:100]
                already_recorded = any(last_decision in e for e in existing)
                if not already_recorded:
                    new_fact = f"Decision: {last_decision}"
            
            if new_fact:
                all_entries = existing + [new_fact]
                trimmed = all_entries[-20:]
                content = self.ENTRY_DELIMITER.join(trimmed)
                if not content.endswith("\n"):
                    content += "\n"
                memory_file.write_text(content, encoding="utf-8")
                logger.debug("[wiki] Real-time fact: %s", new_fact[:80])
                
        except Exception as e:
            logger.warning("[wiki] Real-time sync failed: %s", e)

    def _parse_intent(self, user_message: str) -> str:
        """Extract task intent from first user message."""
        intent = user_message[:200].strip()
        if len(user_message) > 200:
            intent += "..."
        return intent

    def _track_tool_calls(self, assistant_content: str) -> None:
        """Extract file modifications from assistant responses."""
        patterns = [
            r"(?:wrote|modified|created|updated|edited)\s+(?:to\s+)?[`\"']?([\w\-./]+)[`\"']?",
            r"([\w\-./]+\.py)[\"']?\s",
            r"([\w\-./]+\.md)[\"']?\s",
            r"([\w\-./]+\.json)[\"']?\s",
            r"([\w\-./]+\.yaml)[\"']?\s",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, assistant_content, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 3 and match not in self._files_modified:
                    self._files_modified.append(match)

    def _track_decisions(self, assistant_content: str) -> None:
        """Extract decisions from assistant responses."""
        decision_patterns = [
            r"(?:decided|chose|selected|chosen|opting)\s+(?:to\s+)?(.+?)(?:\.|,|$)",
            r"(?:approach|strategy|method):\s*(.+?)(?:\.|,|$)",
        ]
        for pattern in decision_patterns:
            matches = re.findall(pattern, assistant_content, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 5:
                    decision = match.strip()[:150]
                    if decision not in self._decisions:
                        self._decisions.append(decision)

    def _write_rolling_checkpoint(self) -> None:
        """Write rolling checkpoint to disk. Thread-safe, blocking."""
        try:
            checkpoint_path = CHECKPOINT_DIR / f"session_state_{self._session_id}.md"
            content = self._build_checkpoint_content()

            tmp_path = checkpoint_path.with_suffix(".tmp")
            tmp_path.write_text(content, encoding="utf-8")
            os.replace(tmp_path, checkpoint_path)

            logger.info("[wiki] Rolling checkpoint written: %s (turn %d)",
                        checkpoint_path, self._turn_count)
            # Rate-limited git push (only if 5+ minutes since last)
            self._maybe_git_push()
        except Exception as e:
            logger.warning("[wiki] Failed to write rolling checkpoint: %s", e)

    def _trigger_rolling_checkpoint(self) -> None:
        """Trigger async rolling checkpoint write. Safe to call from sync context."""
        # Wait briefly if a previous write is still in progress
        # (daemon thread may be writing from a prior trigger)
        if self._checkpoint_thread and self._checkpoint_thread.is_alive():
            self._checkpoint_thread.join(timeout=2.0)  # wait up to 2s

        self._checkpoint_thread = threading.Thread(
            target=self._write_rolling_checkpoint,
            daemon=True,
            name=f"wiki-checkpoint-{self._session_id}"
        )
        self._checkpoint_thread.start()
        self._last_checkpoint_turn = self._turn_count

    def _build_checkpoint_content(self) -> str:
        """Build structured checkpoint content."""
        timestamp = datetime.now().isoformat()
        session_duration = ""
        if self._session_start_time:
            delta = datetime.now() - self._session_start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            session_duration = f"{hours}h {minutes}m {seconds}s"

        files = "\n".join(f"- `{f}`" for f in self._files_modified[-10:]) or "_None yet_"
        decisions = "\n".join(f"- {d}" for d in self._decisions[-5:]) or "_None yet_"
        blocked = "\n".join(f"- {b}" for b in self._blocked) or "_None_"
        next_steps = "\n".join(f"- {n}" for n in self._next_steps[-5:]) or "_None yet_"

        return f"""---
title: Session Checkpoint
session_id: {self._session_id}
turn: {self._turn_count}
timestamp: {timestamp}
---

# Session Checkpoint — Turn {self._turn_count}

**Session:** {self._session_id}
**Time:** {timestamp}
**Duration:** {session_duration}
**Turn:** {self._turn_count}

## Current Task / Intent
{self._current_task or "_Not set_"}

## State

### Files Modified (recent 10)
{files}

### Decisions Made (recent 5)
{decisions}

## Status

### Blocked / Pending
{blocked}

### Next Steps (recent 5)
{next_steps}

## Recent Conversation (last 3 turns)
"""

    def on_session_end(self, messages: List[Dict[str, Any]]) -> None:
        """
        Called when session ends. Extract session summary and write to:
        - wiki/log.md
        - ~/.hermes/checkpoints/TASK_STATE.md
        - ~/.hermes/checkpoints/DECISION_LOG.md
        - ~/.hermes/checkpoints/session_state_<id>.md (SYNC, not thread)
        """
        try:
            # SYNC write — do NOT use thread here (kills on process exit)
            self._write_rolling_checkpoint()

            summary = self._build_session_summary(messages)

            self._append_to_wiki_log(summary)
            self._write_task_state(summary)
            self._write_decision_log()
            self._auto_extract_to_memory(summary)

            logger.info("[wiki] on_session_end completed, %d turns processed", self._turn_count)
        except Exception as e:
            logger.warning("[wiki] on_session_end failed: %s", e)

    def _build_session_summary(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build structured session summary from messages."""
        duration = ""
        if self._session_start_time:
            delta = datetime.now() - self._session_start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            duration = f"{hours}h {minutes}m"

        outcomes = []
        for msg in messages[-5:]:
            content = msg.get("content", "")
            if isinstance(content, str) and len(content) > 20:
                outcomes.append(content[:300])

        return {
            "session_id": self._session_id,
            "turn_count": self._turn_count,
            "tool_call_count": self._tool_call_count,
            "duration": duration,
            "current_task": self._current_task,
            "files_modified": self._files_modified.copy(),
            "decisions": self._decisions.copy(),
            "blocked": self._blocked.copy(),
            "next_steps": self._next_steps.copy(),
            "outcomes": outcomes,
            "timestamp": datetime.now().isoformat(),
        }

    def _append_to_wiki_log(self, summary: Dict[str, Any]) -> None:
        """Append session summary to wiki log.md."""
        try:
            wiki_root = _get_wiki_root()
            log_path = wiki_root / "log.md"

            if not log_path.exists():
                logger.warning("[wiki] log.md not found, skipping")
                return

            log_lines = [
                "",
                f"## [{datetime.now().strftime('%Y-%m-%d')}] session | {summary['session_id']}",
                f"- Turns: {summary['turn_count']}, Duration: {summary['duration']}",
                f"- Task: {summary['current_task'][:100] if summary['current_task'] else 'N/A'}",
                f"- Files: {', '.join(summary['files_modified'][-5:]) if summary['files_modified'] else 'None'}",
                f"- Decisions: {len(summary['decisions'])} made",
            ]

            existing = log_path.read_text(encoding="utf-8")
            lines = existing.split("\n")

            insert_idx = min(15, len(lines))
            for i, line in enumerate(lines):
                if line.startswith("## [20") and i > 10:
                    insert_idx = i
                    break

            new_log = "\n".join(lines[:insert_idx]) + "\n" + "\n".join(log_lines) + "\n" + "\n".join(lines[insert_idx:])

            tmp_path = log_path.with_suffix(".tmp")
            tmp_path.write_text(new_log, encoding="utf-8")
            os.replace(tmp_path, log_path)

            logger.info("[wiki] Appended session to log.md")
            self._trigger_git_push()  # Non-blocking auto-push
        except Exception as e:
            logger.warning("[wiki] Failed to append to log.md: %s", e)

    def _write_task_state(self, summary: Dict[str, Any]) -> None:
        """Write session summary to TASK_STATE.md."""
        try:
            task_state_path = CHECKPOINT_DIR / "TASK_STATE.md"

            files = "\n".join(f"- [x] `{f}`" for f in summary["files_modified"])
            decisions = "\n".join(f"- {d}" for d in summary["decisions"])
            blocked = "\n".join(f"- {b}" for b in summary["blocked"])
            next_steps = "\n".join(f"- [ ] {n}" for n in summary["next_steps"])

            content = f"""---
title: Task State
session_id: {summary['session_id']}
updated: {datetime.now().isoformat()}
---

# Task State — {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Current Task
**Status:** {'Completed' if not summary['blocked'] else 'In Progress / Blocked'}
**Session:** {summary['session_id']}
**Duration:** {summary['duration']}
**Turns:** {summary['turn_count']}

### Task Description
{summary['current_task'] or '_No task description_'}

## Progress

### Files Modified
{files or '_None_'}

### Decisions Made
{decisions or '_None_'}

## Blockers
{blocked or '_None_'}

## Next Steps
{next_steps or '_None_'}

## Outcomes (from session)
"""
            for i, outcome in enumerate(summary.get("outcomes", [])[-3:], 1):
                content += f"\n### Outcome {i}\n{outcome}\n"

            task_state_path.write_text(content, encoding="utf-8")
            logger.info("[wiki] Wrote TASK_STATE.md")
        except Exception as e:
            logger.warning("[wiki] Failed to write TASK_STATE.md: %s", e)

    def _write_decision_log(self) -> None:
        """Append decisions to DECISION_LOG.md."""
        try:
            decision_log_path = CHECKPOINT_DIR / "DECISION_LOG.md"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            existing = ""
            if decision_log_path.exists():
                existing = decision_log_path.read_text(encoding="utf-8")

            entries = []
            for decision in self._decisions:
                entries.append(f"| {timestamp} | {decision[:80]} | Session end extraction |")

            new_content = existing
            if entries:
                if not existing.strip():
                    new_content = "| Timestamp | Decision | Source |\n|---|---|---|\n"
                new_content += "\n".join(entries) + "\n"

            decision_log_path.write_text(new_content, encoding="utf-8")
            logger.info("[wiki] Updated DECISION_LOG.md with %d entries", len(entries))
        except Exception as e:
            logger.warning("[wiki] Failed to write DECISION_LOG.md: %s", e)

    # ─── Memory File Paths ──────────────────────────────────────────────
    MEMORY_FILE = Path.home() / ".hermes" / "memories" / "MEMORY.md"
    USER_FILE = Path.home() / ".hermes" / "memories" / "USER.md"
    ENTRY_DELIMITER = "\n§\n"

    def _auto_extract_to_memory(self, summary: Dict[str, Any]) -> None:
        """
        DIRECT write to memories/MEMORY.md — no dependencies on tools/memory_tool.
        
        Extracts key facts from session:
        - Files modified
        - Key decisions
        - Current task outcomes
        - Tool results / model performance data
        """
        try:
            Path.home() / ".hermes" / "memories"
            mem_dir = Path.home() / ".hermes" / "memories"
            mem_dir.mkdir(parents=True, exist_ok=True)
            memory_file = self.MEMORY_FILE
            user_file = self.USER_FILE

            # Load existing entries
            existing_memory = self._read_memory_entries(memory_file)
            existing_user = self._read_memory_entries(user_file)

            new_entries = []

            # 1. Task outcome entries (HIGH PRIORITY — always add)
            if summary.get("current_task"):
                task_preview = summary["current_task"][:150].replace("\n", " ").strip()
                new_entries.append(f"Task '{task_preview}' — session {summary['session_id'][:8]}, {summary['turn_count']} turns")

            # 2. Files modified (HIGH PRIORITY)
            if summary.get("files_modified"):
                files = summary["files_modified"]
                unique_files = list(dict.fromkeys(files))[-5:]  # dedupe, keep last 5
                new_entries.append(f"Modified files: {', '.join(unique_files)}")

            # 3. Key decisions (HIGH PRIORITY)
            if summary.get("decisions"):
                decisions = summary["decisions"]
                if len(decisions) >= 1:
                    recent = "; ".join(decisions[-3:])
                    new_entries.append(f"Decisions: {recent[:150]}")

            # 4. Blocked/issue resolutions
            if summary.get("blocked"):
                new_entries.append(f"Resolved blockers: {', '.join(summary['blocked'][-3:])}")

            # 5. Tool call count (useful for memory optimization)
            tool_count = summary.get("tool_call_count", 0)
            if tool_count > 0:
                new_entries.append(f"Session {summary['session_id'][:8]}: {summary['turn_count']} turns, {tool_count} tool calls")

            # Write to MEMORY.md if we have new entries
            if new_entries:
                # Keep only last 20 entries to stay within char limits
                all_entries = existing_memory + new_entries
                trimmed_entries = all_entries[-20:]
                
                content = self.ENTRY_DELIMITER.join(trimmed_entries)
                if not content.endswith("\n"):
                    content += "\n"
                
                memory_file.parent.mkdir(parents=True, exist_ok=True)
                memory_file.write_text(content, encoding="utf-8")
                logger.info("[wiki] Memory auto-extract: wrote %d entries to MEMORY.md", len(new_entries))

            # 6. Structured USER.md updates (Phase 1: Mem0-style entity memory)
            self._write_structured_user_profile(summary)
            self._consolidate_memory()

            logger.info("[wiki] Memory auto-extract complete")
        except Exception as e:
            logger.warning("[wiki] Memory auto-extract failed (NON-SILENT): %s", e)
            import traceback
            logger.warning("[wiki] Traceback: %s", traceback.format_exc())

    def _read_memory_entries(self, path: Path) -> List[str]:
        """Read existing memory entries, handling empty/missing files."""
        if not path.exists():
            return []
        content = path.read_text(encoding="utf-8")
        entries = [e.strip() for e in content.split(self.ENTRY_DELIMITER) if e.strip()]
        return entries

    # ─── Retrieval System (Phase 2: Hybrid BM25 + Semantic) ─────────────────

    def retrieve_relevant_memory(self, query: str, k: int = 8) -> str:
        """
        HYBRID retrieval: BM25 keyword + semantic similarity.
        
        Called at session start OR when agent needs to recall something.
        Returns formatted memory context for injection into prompt.
        """
        if not query or len(query.strip()) < 2:
            return ""
        
        try:
            entries = self._collect_all_memory_entries()
            if not entries:
                return ""
            
            bm25_scores = self._bm25_search(query, entries)
            semantic_scores = self._semantic_search(query, entries)
            combined = self._rrf_fusion(bm25_scores, semantic_scores, k=k)
            
            if not combined:
                return ""
            
            result_parts = ["## Retrieved Memory Context\n"]
            for entry, score in combined:
                # Phase 2: Apply importance scoring boost
                entry_dict = {"text": entry, "score": score}
                boosted_score = self._score_by_importance(entry_dict, query)
                preview = entry[:200].replace("\n", " ")
                result_parts.append(f"- [{boosted_score:.2f}] {preview}")
            
            result = "\n".join(result_parts)
            logger.info("[wiki] retrieve: query='%s' → %d entries, top=%.2f", 
                        query[:50], len(entries), combined[0][1] if combined else 0)
            return result
            
        except Exception as e:
            logger.warning("[wiki] retrieve_relevant_memory failed: %s", e)
            return ""

    def _collect_all_memory_entries(self) -> List[Dict[str, str]]:
        """Collect ALL memory entries from MEMORY.md, USER.md, EPISODES.md, checkpoints."""
        entries = []
        seen = set()
        
        for memory_file in [self.MEMORY_FILE, self.USER_FILE]:
            for entry in self._read_memory_entries(memory_file):
                key = entry[:80].lower()
                if key not in seen:
                    seen.add(key)
                    entries.append({"text": entry, "source": memory_file.name})
        
        episodes_file = Path.home() / ".hermes" / "memories" / "EPISODES.md"
        if episodes_file.exists():
            try:
                content = episodes_file.read_text(encoding="utf-8")
                sessions = re.split(r'\n(?=## Session |\n Session |\n\d{4}-\d{2}-\d{2})', content)
                for s in sessions:
                    s = s.strip()
                    if s and len(s) > 20:
                        key = s[:80].lower()
                        if key not in seen:
                            seen.add(key)
                            entries.append({"text": s, "source": "EPISODES.md"})
            except Exception:
                pass
        
        if CHECKPOINT_DIR.exists():
            for cp_file in sorted(CHECKPOINT_DIR.glob("session_state_*.md"), 
                                  key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
                try:
                    content = cp_file.read_text(encoding="utf-8")
                    lines = [l for l in content.split("\n") 
                             if l.startswith(("## ", "**")) and len(l) > 15]
                    summary = " | ".join(l.strip() for l in lines[:6])
                    if summary and len(summary) > 30:
                        key = summary[:80].lower()
                        if key not in seen:
                            seen.add(key)
                            entries.append({"text": summary, "source": cp_file.name})
                except Exception:
                    pass
        
        return entries

    def _bm25_search(self, query: str, entries: List[Dict[str, str]], k: int = 10) -> List[tuple]:
        """BM25-style keyword search using sklearn TF-IDF."""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            
            texts = [e["text"] for e in entries]
            vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), max_features=5000)
            corpus_tfidf = vectorizer.fit_transform(texts)
            query_tfidf = vectorizer.transform([query.lower()])
            scores = cosine_similarity(query_tfidf, corpus_tfidf).flatten()
            
            top_indices = scores.argsort()[::-1][:k]
            return [(entries[i]["text"], float(scores[i])) for i in top_indices if scores[i] > 0]
        except Exception as e:
            logger.debug("[wiki] BM25 failed, fallback: %s", e)
            return self._keyword_match_fallback(query, entries, k)

    def _keyword_match_fallback(self, query: str, entries: List[Dict[str, str]], k: int = 10) -> List[tuple]:
        """Fallback: simple keyword overlap scoring."""
        keywords = set(query.lower().split())
        results = []
        for entry in entries:
            text_lower = entry["text"].lower()
            score = sum(1 for kw in keywords if kw in text_lower)
            if query.lower() in text_lower:
                score += 5
            if score > 0:
                results.append((entry["text"], float(score)))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def _semantic_search(self, query: str, entries: List[Dict[str, str]], k: int = 10) -> List[tuple]:
        """Lightweight semantic similarity using character n-gram fingerprinting (numpy)."""
        try:
            import numpy as np
            
            def get_ngram_fingerprint(text: str, n: int = 3) -> np.ndarray:
                text = text.lower()
                ngrams = [text[i:i+n] for i in range(max(0, len(text)-n+1))]
                vec = np.zeros(1000)
                for ng in ngrams:
                    vec[hash(ng) % 1000] += 1
                norm = np.linalg.norm(vec)
                return vec / norm if norm > 0 else vec
            
            query_fp = get_ngram_fingerprint(query)
            scores = []
            for entry in entries:
                entry_fp = get_ngram_fingerprint(entry["text"])
                sim = float(np.dot(query_fp, entry_fp))
                if sim > 0.05:
                    scores.append((entry["text"], sim))
            
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[:k]
        except Exception as e:
            logger.debug("[wiki] Semantic search failed: %s", e)
            return []

    def _rrf_fusion(self, bm25_results: List[tuple], semantic_results: List[tuple], 
                    k: int = 60, top_k: int = 8) -> List[tuple]:
        """Reciprocal Rank Fusion: combine ranked lists. RRF_score = weight * (1 / (k + rank + 1))."""
        try:
            combined_scores: Dict[str, float] = {}
            entry_map: Dict[str, str] = {}
            
            for rank, (text, score) in enumerate(bm25_results):
                key = text[:80]
                entry_map[key] = text
                combined_scores[key] = combined_scores.get(key, 0) + 0.6 * (1 / (k + rank + 1))
            
            for rank, (text, score) in enumerate(semantic_results):
                key = text[:80]
                entry_map[key] = text
                combined_scores[key] = combined_scores.get(key, 0) + 0.4 * (1 / (k + rank + 1))
            
            sorted_keys = sorted(combined_scores.keys(), key=lambda k: combined_scores[k], reverse=True)
            return [(entry_map[k], combined_scores[k]) for k in sorted_keys[:top_k]]
        except Exception as e:
            logger.debug("[wiki] RRF fusion failed: %s", e)
            return bm25_results[:top_k]

    # ─── End Retrieval System ───────────────────────────────────────────────

    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 1: Structured Entity Extraction (Mem0-style)
    # ═══════════════════════════════════════════════════════════════════════

    ENTITY_PATTERNS = {
        "project": [
            r"(?i)(project|codebase|repo)[:\s]+([a-zA-Z0-9_-]+)",
            r"(?i)(đang làm|working on|running)[:\s]*([a-zA-Z0-9_-]+)",
        ],
        "tool": [
            r"(?i)(using|via|thông qua)[:\s]+([a-zA-Z0-9_-]+)",
            r"(?i)(tool|CLI|command)[:\s]+([a-zA-Z0-9_-]+)",
        ],
        "model": [
            r"(?i)(model|LLM)[:\s]+([a-zA-Z0-9_./-]+)",
            r"gemma|qwen|claude|gpt|llama",
        ],
        "file": [
            r"(?:file|path)[:\s]+([^\s]+)",
            r"~/.hermes/[^\s]+",
            r"/[^\s]+\.(py|md|json|yaml|sh)",
        ],
        "preference": [
            r"(?i)(muốn|want|prefer|thích|like)[:\s]+(.+)",
            r"(?i)(không|don't|don't)[:\s]+(.+)",
        ],
    }

    def _extract_entity_facts(self, messages: List[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """
        Phase 1: Extract structured entity facts from conversation.
        Returns list of {type, value, source, priority} dicts.
        User corrections → HIGH priority. Repeated facts → SEMANTIC.
        """
        facts = []
        seen = set()
        conversation = messages if messages else self._conversation_buffer
        
        for msg in conversation:
            content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
            if not content:
                continue
            
            # Extract by type
            for entity_type, patterns in self.ENTITY_PATTERNS.items():
                for pattern in patterns:
                    for match in re.finditer(pattern, content):
                        if len(match.groups()) >= 2:
                            value = match.group(2).strip()
                        else:
                            value = match.group(1).strip() if match.groups() else match.group(0).strip()
                        
                        if len(value) < 2 or len(value) > 200:
                            continue
                        
                        key = f"{entity_type}:{value[:50].lower()}"
                        if key in seen:
                            continue
                        seen.add(key)
                        
                        # Priority: user corrections are HIGH
                        priority = "normal"
                        if any(correct_word in content.lower() for correct_word in 
                               ["không phải", "not", "wrong", "sai", "incorrect", "đừng", "don't"]):
                            priority = "high"
                        
                        facts.append({
                            "type": entity_type,
                            "value": value,
                            "source": f"turn_{self._turn_count}",
                            "priority": priority,
                        })
        
        # Deduplicate by value
        unique_facts = []
        seen_values = set()
        for f in facts:
            val_key = f["value"][:30].lower()
            if val_key not in seen_values:
                seen_values.add(val_key)
                unique_facts.append(f)
        
        return unique_facts

    def _write_structured_user_profile(self, session_summary: Dict[str, Any]) -> None:
        """
        Phase 1: Write structured USER.md with sections.
        Replaces flat § delimiter with structured [SECTION] format.
        """
        try:
            user_file = self.USER_FILE
            user_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Read existing profile
            existing_content = ""
            if user_file.exists():
                existing_content = user_file.read_text(encoding="utf-8")
            
            # Parse existing sections
            sections = {"PREFERENCES": [], "PROJECTS": [], "FACTS": [], "SESSIONS": [], "ENTITY_INDEX": [], "GROWTH_LOG": []}
            current_section = "FACTS"
            
            for line in existing_content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("[") and stripped.endswith("]"):
                    tag = stripped[1:-1].upper()
                    if tag in sections:
                        current_section = tag
                        continue
                if stripped.startswith("§"):
                    continue  # Skip old-style delimiters
                if stripped and not stripped.startswith("#"):
                    sections[current_section].append(stripped)
            
            # Extract new facts from this session
            new_facts = self._extract_entity_facts()
            for fact in new_facts:
                fact_line = f"- [{fact['type']}] {fact['value']}"
                if fact["priority"] == "high":
                    fact_line += " [HIGH]"
                sections["FACTS"] = [f for f in sections["FACTS"] 
                                     if f"[{fact['type']}] {fact['value'][:30]}" not in f]
                sections["FACTS"].append(fact_line)
            
            # Add session summary to SESSIONS
            session_date = datetime.now().strftime("%Y-%m-%d")
            session_task = session_summary.get("current_task", self._current_task or "unknown")
            session_str = f"- {session_date}: {session_task[:100]}"
            sections["SESSIONS"] = [s for s in sections["SESSIONS"] if session_date not in s]
            sections["SESSIONS"].append(session_str)
            
            # Keep only last 20 sessions
            sections["SESSIONS"] = sections["SESSIONS"][-20:]
            
            # Build new content
            output_parts = ["§ [PREFERENCES] — explicit preferences discovered over sessions"]
            if sections["PREFERENCES"]:
                output_parts.extend(sections["PREFERENCES"])
            else:
                output_parts.append("- communication: Vietnamese casual")
                output_parts.append("- response_style: concise, no fluff")
                output_parts.append('- tiktok_script_style: "anh" + "mấy con vợ"')
            
            output_parts.append("§ [PROJECTS] — ongoing work")
            output_parts.extend(sections["PROJECTS"] or ["- tiktok-content: active", "- hermes-agent: memory-optimizing"])
            
            output_parts.append("§ [FACTS] — durable facts about user, environment, tools")
            output_parts.extend(sections["FACTS"][-30:] or [])
            
            output_parts.append("§ [SESSIONS] — session history summaries")
            output_parts.extend(sections["SESSIONS"])
            
            output_parts.append("§ [ENTITY_INDEX] — cross-session entity tracking")
            output_parts.extend(sections["ENTITY_INDEX"] or [])
            
            output_parts.append("§ [GROWTH_LOG] — how user/agent improved")
            output_parts.extend(sections["GROWTH_LOG"] or [])
            
            new_content = "\n".join(output_parts) + "\n"
            user_file.write_text(new_content, encoding="utf-8")
            logger.info("[wiki] Structured USER.md written with %d facts", len(new_facts))
            
        except Exception as e:
            logger.warning("[wiki] _write_structured_user_profile failed: %s", e)

    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 2: Importance Scoring in Retrieval
    # ═══════════════════════════════════════════════════════════════════════

    def _score_by_importance(self, entry: Dict[str, str], query: str) -> float:
        """
        Phase 2: Score entry by importance signals.
        Factors: recency, frequency, user correction, domain match.
        """
        score = entry.get("score", 0.5)
        text = entry.get("text", "")
        
        # Boost for recent mentions
        import time
        try:
            # Check if this session's checkpoint mentions it
            if CHECKPOINT_DIR.exists():
                recent_checkpoints = sorted(
                    CHECKPOINT_DIR.glob("session_state_*.md"),
                    key=lambda p: p.stat().st_mtime, reverse=True
                )[:3]
                for cp in recent_checkpoints:
                    if text[:50] in cp.read_text():
                        score *= 1.3  # 30% boost for being mentioned recently
        except Exception:
            pass
        
        # Boost for HIGH priority markers (user corrections)
        if "[HIGH]" in text or "[CORRECTION]" in text:
            score *= 1.5
        
        # Boost for exact query matches in key positions (title, first line)
        text_lower = text.lower()
        query_words = query.lower().split()
        first_line = text_lower.split("\n")[0] if "\n" in text else text_lower
        for word in query_words:
            if len(word) > 3 and word in first_line:
                score *= 1.2
                break
        
        return min(score, 2.0)  # Cap at 2x

    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 3: Smart Session-Start Query Parsing
    # ═══════════════════════════════════════════════════════════════════════

    def _parse_session_start_topics(self, initial_message: str = "") -> List[str]:
        """
        Phase 3: Parse user greeting/message to extract topics for retrieval.
        Returns list of topic queries to fetch relevant memories.
        """
        topics = []
        if not initial_message:
            return topics
        
        # Extract keywords/phrases
        message_lower = initial_message.lower()
        
        # Vietnamese topic patterns
        topic_patterns = [
            r"(?i)lần trước[:\s]*(.+)",
            r"(?i)hôm (qua|nay|trước)[:\s]*(.+)",
            r"(?i)project[:\s]*([a-zA-Z0-9_-]+)",
            r"(?i)(code|script|tiktok|wiki|memory)[:\s]*(.+)",
            r"(?i)(làm|lam|chỉnh sửa|fix|debug)[:\s]*(.+)",
            r"(?i)thg ([a-zA-Z0-9_-]+)",
        ]
        
        for pattern in topic_patterns:
            for match in re.finditer(pattern, message_lower):
                topic = match.group(0).strip()
                if len(topic) > 3:
                    topics.append(topic)
        
        # Add individual important words
        important_words = ["tiktok", "script", "memory", "hermes", "agent", 
                          "wiki", "project", "code", "lm studio", "byteRover"]
        for word in important_words:
            if word in message_lower and len(word) > 3:
                topics.append(word)
        
        # Deduplicate
        seen = set()
        unique = []
        for t in topics:
            t_clean = t[:40].lower()
            if t_clean not in seen:
                seen.add(t_clean)
                unique.append(t)
        
        return unique[:5]  # Max 5 topics

    def _fetch_session_start_memories(self, topics: List[str]) -> str:
        """
        Phase 3: Fetch relevant memories for each topic and combine.
        Called at session start via prefetch() with topics from greeting.
        """
        if not topics:
            return ""
        
        all_results = []
        for topic in topics:
            result = self.retrieve_relevant_memory(topic, k=5)
            if result:
                all_results.append(f"### Topic: {topic}\n{result}")
        
        return "\n\n".join(all_results) if all_results else ""

    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 4: Memory Consolidation (Forgetting/Eviction)
    # ═══════════════════════════════════════════════════════════════════════

    def _consolidate_memory(self, force: bool = False) -> Dict[str, Any]:
        """
        Phase 4: Consolidate memory — evict low-importance, merge duplicates.
        Called weekly or every 50 sessions.
        
        Signals:
        - User correction → HIGH priority, never evicted
        - Repeated 3x+ → promote to SEMANTIC
        - 30 days unused → decay
        - 90 days unused → archive (not delete)
        """
        try:
            stats = {"before": 0, "after": 0, "archived": 0, "merged": 0, "decayed": 0}
            
            user_file = self.USER_FILE
            if not user_file.exists():
                return {"status": "no_user_file", "stats": stats}
            
            entries = self._read_memory_entries(user_file)
            stats["before"] = len(entries)
            
            if len(entries) < 50 and not force:
                return {"status": "below_threshold", "stats": stats}
            
            # Score each entry
            scored = []
            import time
            now = time.time()
            
            for entry in entries:
                score = 0.5
                entry_lower = entry.lower()
                
                # High priority markers
                if "[HIGH]" in entry or "[CORRECTION]" in entry:
                    score = 2.0
                elif "[PREFERENCE]" in entry:
                    score = 1.5
                
                # Age decay (simple: 1 point per 30 days)
                age_marker = re.search(r"(\d{4}-\d{2}-\d{2})", entry)
                if age_marker:
                    try:
                        from datetime import datetime as dt
                        entry_date = dt.strptime(age_marker.group(1), "%Y-%m-%d")
                        days_old = (dt.now() - entry_date).days
                        score += max(0, (30 - days_old) / 30) * 0.5
                    except Exception:
                        pass
                
                scored.append((entry, score))
            
            # Keep top 50 entries, archive rest
            scored.sort(key=lambda x: x[1], reverse=True)
            kept = [e for e, s in scored[:50]]
            archived = [e for e, s in scored[50:]]
            
            stats["after"] = len(kept)
            stats["archived"] = len(archived)
            stats["merged"] = 0  # Simplified for now
            
            # Archive to memories/ARCHIVE/
            if archived:
                archive_dir = Path.home() / ".hermes" / "memories" / "ARCHIVE"
                archive_dir.mkdir(parents=True, exist_ok=True)
                
                archive_file = archive_dir / f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                archive_content = f"""# Memory Archive — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Consolidated Entries ({len(archived)})

""" + "\n".join(f"- {e}" for e in archived) + "\n"
                archive_file.write_text(archive_content, encoding="utf-8")
                logger.info("[wiki] Archived %d memory entries to %s", len(archived), archive_file)
            
            # Rewrite USER.md with kept entries
            new_content = "\n".join(kept) + "\n"
            if not new_content.endswith("\n"):
                new_content += "\n"
            user_file.write_text(new_content, encoding="utf-8")
            
            logger.info("[wiki] Consolidation done: %s", stats)
            return {"status": "consolidated", "stats": stats}
            
        except Exception as e:
            logger.warning("[wiki] _consolidate_memory failed: %s", e)
            return {"status": "error", "error": str(e)}

    # ═══════════════════════════════════════════════════════════════════════
    # PHASE 5: Cross-Session Entity Tracking
    # ═══════════════════════════════════════════════════════════════════════

    def _track_cross_session_entity(self, entity_type: str, name: str, 
                                    fact: str, session_id: str = "") -> None:
        """
        Phase 5: Track entities across sessions.
        Updates ENTITY_INDEX in USER.md with session history.
        """
        try:
            user_file = self.USER_FILE
            if not user_file.exists():
                return
            
            content = user_file.read_text(encoding="utf-8")
            
            # Find ENTITY_INDEX section
            entity_marker = f"[{entity_type.upper()}] {name}"
            session_marker = f"{session_id or self._session_id}: {fact[:80]}"
            
            # Check if entity already exists
            if entity_marker in content:
                # Append new session fact
                lines = content.split("\n")
                in_section = False
                for i, line in enumerate(lines):
                    if line.strip() == entity_marker:
                        in_section = True
                    elif in_section and line.strip().startswith("§ ["):
                        # Next section, insert before
                        lines.insert(i, f"  - {session_marker}")
                        break
                    elif in_section and not line.strip().startswith("  -"):
                        # Non-list item in entity section
                        lines.insert(i, f"  - {session_marker}")
                        break
                content = "\n".join(lines)
            else:
                # Add new entity
                entity_line = f"§ [ENTITY_INDEX]\n- {entity_marker}\n  - {session_marker}\n"
                if "§ [ENTITY_INDEX]" in content:
                    content = content.replace(
                        "§ [ENTITY_INDEX]",
                        entity_line.replace("§ [ENTITY_INDEX]\n", "")
                    )
                else:
                    content += "\n" + entity_line
            
            user_file.write_text(content, encoding="utf-8")
            logger.info("[wiki] Tracked entity: %s/%s", entity_type, name)
            
        except Exception as e:
            logger.warning("[wiki] _track_cross_session_entity failed: %s", e)

    def _update_growth_log(self, improvement: str) -> None:
        """
        Phase 5: Log how user/agent improved this session.
        """
        try:
            user_file = self.USER_FILE
            if not user_file.exists():
                return
            
            content = user_file.read_text(encoding="utf-8")
            date = datetime.now().strftime("%Y-%m-%d")
            entry = f"- [{date}] {improvement[:150]}"
            
            # Append to GROWTH_LOG section
            if "§ [GROWTH_LOG]" in content:
                content = content.replace(
                    "§ [GROWTH_LOG]",
                    f"§ [GROWTH_LOG]\n{entry}"
                )
            else:
                content += f"\n§ [GROWTH_LOG]\n{entry}\n"
            
            # Keep last 20 entries
            lines = content.split("\n")
            growth_lines = []
            in_growth = False
            for line in lines:
                if "§ [GROWTH_LOG]" in line:
                    in_growth = True
                    growth_lines = [line]
                elif in_growth and line.startswith("§ ["):
                    in_growth = False
                elif in_growth:
                    growth_lines.append(line)
            
            if len(growth_lines) > 21:
                growth_lines = growth_lines[:21]
            
            # Rebuild
            other_lines = [l for l in lines if l not in growth_lines or not in_growth]
            content = "\n".join(other_lines) + "\n" + "\n".join(growth_lines) + "\n"
            
            user_file.write_text(content, encoding="utf-8")
            logger.info("[wiki] Growth log updated: %s", improvement[:50])
            
        except Exception as e:
            logger.warning("[wiki] _update_growth_log failed: %s", e)

    # ═══════════════════════════════════════════════════════════════════════
    # Legacy: Update USER.md (Phase 1 transitional)
    # ═══════════════════════════════════════════════════════════════════════

    def _update_user_profile(self, summary: Dict[str, Any]) -> None:
        """
        Update USER.md with inferred user preferences from this session.
        Looks for:
        - New tool preferences (which tools were used heavily)
        - Platform usage (Telegram, CLI, etc.)
        - New conventions/preferences expressed by user
        """
        try:
            user_file = self.USER_FILE
            user_file.parent.mkdir(parents=True, exist_ok=True)
            
            existing = self._read_memory_entries(user_file)
            
            # Infer from conversation buffer
            inferred = []
            
            # Check for preferred pronouns/style
            for msg in self._conversation_buffer[-10:]:
                content = msg.get("content", "")
                if not isinstance(content, str):
                    continue
                # Detect Vietnamese content style
                if any(word in content for word in ["mấy con vợ", "anh ơi", "em ơi"]):
                    if not any("Vietnamese" in e for e in existing + inferred):
                        inferred.append("User communicates in Vietnamese (Tiếng Việt)")
                # Detect model preference from tool results
                if "gemma" in content.lower() or "lm studio" in content.lower():
                    if not any("LM Studio" in e for e in existing + inferred):
                        inferred.append("Prefers local models via LM Studio")
            
            if inferred:
                all_entries = existing + inferred
                trimmed = all_entries[-15:]  # Keep user profile lean
                content = self.ENTRY_DELIMITER.join(trimmed)
                if not content.endswith("\n"):
                    content += "\n"
                user_file.write_text(content, encoding="utf-8")
                logger.info("[wiki] User profile updated with: %s", inferred)
        except Exception as e:
            logger.warning("[wiki] User profile update failed: %s", e)

    def on_pre_compress(self, messages: List[Dict[str, Any]]) -> str:
        """
        Called BEFORE context compression. Write a structured checkpoint
        that will survive compression. Returns context for the compression
        summary prompt.
        """
        try:
            checkpoint_path = CHECKPOINT_DIR / f"pre_compact_{self._session_id}.md"

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            files = "\n".join(f"- `{f}`" for f in self._files_modified[-10:]) or "_None_"
            decisions = "\n".join(f"- {d}" for d in self._decisions[-5:]) or "_None_"
            next_steps = "\n".join(f"- {n}" for n in self._next_steps[-5:]) or "_Continue from checkpoint_"

            content = f"""---
title: Pre-Compact Checkpoint
session_id: {self._session_id}
timestamp: {timestamp}
trigger: context_compression
---

# Pre-Compact Checkpoint — {timestamp}

**CRITICAL: This session is about to be compressed. All work-in-progress below must be preserved.**

## Current Task
{self._current_task or '_No task description_'}

## Intent (Original Goal)
_Above is the current task intent from session start_

## State

### Files Modified (do NOT lose these)
{files}

### Decisions Made
{decisions}

### Blocked / Pending Issues
{self._blocked or '_None_'}

## Next Steps — DO NOT LOSE
{next_steps}

## Session Metadata
- Session ID: {self._session_id}
- Total turns: {self._turn_count}
- Tool calls tracked: {self._tool_call_count}

---
_This checkpoint was written automatically by WikiMemoryProvider before context compression._
"""

            tmp_path = checkpoint_path.with_suffix(".tmp")
            tmp_path.write_text(content, encoding="utf-8")
            os.replace(tmp_path, checkpoint_path)

            logger.info("[wiki] Pre-compact checkpoint written: %s", checkpoint_path)

            return (f"[PRE-COMPACT CHECKPOINT] Session {self._session_id} has {self._turn_count} turns. "
                    f"Current task: {self._current_task[:100] if self._current_task else 'N/A'}. "
                    f"Files modified: {', '.join(self._files_modified[-5:]) if self._files_modified else 'None'}. "
                    f"Next steps: {', '.join(self._next_steps[-3:]) if self._next_steps else 'Continue normally'}. "
                    f"Full checkpoint: {checkpoint_path}")

        except Exception as e:
            logger.warning("[wiki] on_pre_compress failed: %s", e)
            return ""

        # CRITICAL: Also extract to memory on pre-compress (before compression kills context)
        try:
            summary = {
                "session_id": self._session_id,
                "turn_count": self._turn_count,
                "tool_call_count": self._tool_call_count,
                "current_task": self._current_task,
                "files_modified": self._files_modified,
                "decisions": self._decisions,
                "blocked": self._blocked,
                "next_steps": self._next_steps,
            }
            self._auto_extract_to_memory(summary)
        except Exception as e:
            logger.warning("[wiki] on_pre_compress memory extract failed: %s", e)

    def on_session_switch(
        self,
        new_session_id: str,
        *,
        parent_session_id: str = "",
        reset: bool = False,
        **kwargs,
    ) -> None:
        """
        Called when session_id rotates (context compression, /new, /resume, /branch).
        Reset per-session state and flush pending writes to the old session_id.
        """
        try:
            logger.info(
                "[wiki] on_session_switch: %s → %s (parent=%s, reset=%s)",
                self._session_id, new_session_id, parent_session_id, reset,
            )

            # Flush any pending writes for the old session
            if self._conversation_buffer:
                self._write_rolling_checkpoint()

            # Reset per-session state for new session
            old_session_id = self._session_id
            self._session_id = new_session_id
            self._turn_count = 0
            self._tool_call_count = 0
            self._last_checkpoint_turn = 0
            self._current_task = ""
            self._files_modified = []
            self._decisions = []
            self._blocked = []
            self._next_steps = []
            self._conversation_buffer = []
            self._session_start_time = datetime.now()

            # If reset=True (user-initiated /new or /reset), also clear cached
            # context so old session's data doesn't leak into new session
            if reset:
                self._session_cache.clear()
                logger.info("[wiki] Session switch with reset=True — cache cleared")

        except Exception as e:
            logger.warning("[wiki] on_session_switch failed: %s", e)

    def on_post_compress(
        self,
        old_session_id: str,
        compressed_messages: List[Dict[str, Any]],
    ) -> str:
        """
        Called AFTER context compression completes.
        Reads the pre-compact checkpoint and returns structured context
        to be injected into the new session's memory context.

        This is the recovery path — the compressed context loses fine-grained
        task state, so we restore it from the checkpoint file.
        """
        try:
            checkpoint_path = CHECKPOINT_DIR / f"pre_compact_{old_session_id}.md"
            if not checkpoint_path.exists():
                logger.debug("[wiki] on_post_compress: no checkpoint found for %s", old_session_id)
                return ""

            content = checkpoint_path.read_text(encoding="utf-8")

            # Parse task state from checkpoint
            task_match = re.search(r"## Current Task\s*\n(.+?)(?=\n##|\n---\n|$)", content, re.DOTALL)
            decisions_match = re.search(r"### Decisions Made\s*\n(.+?)(?=\n###|\n---\n|$)", content, re.DOTALL)
            next_steps_match = re.search(r"## Next Steps — DO NOT LOSE\s*\n(.+?)(?=\n##|\n---\n|$)", content, re.DOTALL)
            files_match = re.search(r"### Files Modified.*?\n(.+?)(?=\n###|\n---\n|$)", content, re.DOTALL)

            current_task = task_match.group(1).strip() if task_match else ""
            decisions = decisions_match.group(1).strip() if decisions_match else ""
            next_steps = next_steps_match.group(1).strip() if next_steps_match else ""
            files = files_match.group(1).strip() if files_match else ""

            # Build structured recovery context
            recovery = []
            if current_task:
                recovery.append(f"**Continuing task:** {current_task}")
            if decisions and decisions != "_None_":
                recovery.append(f"**Prior decisions:** {decisions}")
            if next_steps and next_steps != "_Continue normally_":
                recovery.append(f"**Next steps:** {next_steps}")
            if files and files != "_None_":
                recovery.append(f"**Files modified:** {files}")

            result = "\n".join(recovery)
            if result:
                logger.info("[wiki] on_post_compress: restored context for %s", old_session_id)

            # Also trigger proactive retrieval to warm up cache for new session
            self._proactive_retrieve_from_checkpoint(checkpoint_path)

            return result

        except Exception as e:
            logger.warning("[wiki] on_post_compress failed: %s", e)
            return ""

    def _proactive_retrieve_from_checkpoint(self, checkpoint_path: Path) -> None:
        """
        Read a pre-compact checkpoint and proactively query wiki for
        relevant context, caching results for the next prefetch() call.
        """
        try:
            content = checkpoint_path.read_text(encoding="utf-8")

            # Extract task from checkpoint
            task_match = re.search(r"## Current Task\s*\n(.+?)(?=\n##|\n---\n|$)", content, re.DOTALL)
            current_task = task_match.group(1).strip() if task_match else ""

            if not current_task:
                return

            # Parse decisions and next steps for additional topics
            decisions_match = re.search(r"### Decisions Made\s*\n(.+?)(?=\n###|\n---\n|$)", content, re.DOTALL)
            next_steps_match = re.search(r"## Next Steps — DO NOT LOSE\s*\n(.+?)(?=\n##|\n---\n|$)", content, re.DOTALL)

            topics = []
            if current_task:
                topics.append(current_task[:200])
            if decisions_match:
                # Extract individual decisions as topics
                decisions = decisions_match.group(1)
                for line in decisions.split("\n"):
                    line = line.strip().lstrip("-*")
                    if line and line != "_None_" and len(line) > 5:
                        topics.append(line[:100])
            if next_steps_match:
                next_steps = next_steps_match.group(1)
                for line in next_steps.split("\n"):
                    line = line.strip().lstrip("-*")
                    if line and line != "_Continue normally_" and len(line) > 5:
                        topics.append(line[:100])

            # Deduplicate and limit
            seen = set()
            unique_topics = []
            for t in topics:
                norm = t.lower()[:50]
                if norm not in seen and t:
                    seen.add(norm)
                    unique_topics.append(t)
            unique_topics = unique_topics[:8]  # Max 8 queries

            # Retrieve and cache
            cached_results = []
            for topic in unique_topics:
                result = self.retrieve_relevant_memory(topic, k=3)
                if result:
                    self._session_cache[f"proactive_{topic[:50]}"] = result
                    cached_results.append(topic[:50])

            if cached_results:
                self._session_cache["has_proactive_context"] = True
                self._session_cache["proactive_topics"] = cached_results
                logger.info(
                    "[wiki] Proactive retrieval: %d topics cached for next prefetch",
                    len(cached_results),
                )

        except Exception as e:
            logger.debug("[wiki] _proactive_retrieve_from_checkpoint failed: %s", e)

    def shutdown(self) -> None:
        """Clean shutdown — write final checkpoint."""
        try:
            if self._conversation_buffer:
                self._write_rolling_checkpoint()
        except Exception:
            pass


# ─── Plugin registration ─────────────────────────────────────────────────────

def register(collector) -> None:
    """Top-level register() function for plugin discovery."""
    collector.register_memory_provider(WikiMemoryProvider())
