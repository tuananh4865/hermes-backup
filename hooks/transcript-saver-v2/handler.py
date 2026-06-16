"""
Transcript Saver Hook v2.0 — Entity-based wiki with backlinks + Obsidian mirror

Pattern (Loop Engineering):
  Real-time: Telegram msg → handler.py → write wiki/raw/transcripts/{date}/*.md
  Auto: Extract entities, generate wikilinks, mirror to Obsidian
  Backward compatible: v1.0 format still works

Events:
- agent:end: Save transcript to wiki + Obsidian

Output:
- Primary: /Volumes/Storage-1/Hermes/wiki/raw/transcripts/{YYYY-MM-DD}/{HH-MM-SS}_{session_id}_{slug}.md
- Mirror:  ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/transcripts/{YYYY-MM-DD}/{same}.md
"""

import os
import re
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta


# === Paths ===
WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
WIKI_TRANSCRIPTS = WIKI_ROOT / "raw" / "transcripts"
WIKI_ENTITIES = WIKI_ROOT / "entities"
WIKI_CONCEPTS = WIKI_ROOT / "concepts"

OBSIDIAN_ROOT = Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents" / "My-Brain"
OBSIDIAN_TRANSCRIPTS = OBSIDIAN_ROOT / "transcripts"

TZ_VN = timezone(timedelta(hours=7))


# === Utilities ===

def now_vn() -> datetime:
    return datetime.now(TZ_VN)


def now_str() -> str:
    return now_vn().strftime("%Y-%m-%d %H:%M:%S %z")


def sanitize_slug(text: str, max_len: int = 40) -> str:
    """Sanitize text for filename: lowercase, hyphens, no special chars."""
    text = re.sub(r'[^\w\s\-àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]', '', text.lower())
    text = re.sub(r'\s+', '-', text.strip())
    text = re.sub(r'-+', '-', text)
    return text[:max_len] if text else "untitled"


def extract_title(user_message: str, timestamp: datetime) -> str:
    """Extract title from user message (first sentence/question, max 60 chars)."""
    # Strip sender prefix [Tuấn Anh]
    msg = re.sub(r'^\s*\[[^\]]+\]\s*', '', user_message).strip()
    # First sentence
    first = re.split(r'[.!?\n]', msg)[0].strip()
    if len(first) > 50:
        first = first[:47] + "..."
    time_str = timestamp.strftime("%H:%M")
    return f"{time_str} - {first}" if first else f"Transcript {time_str}"


def extract_goal(user_message: str) -> str:
    """Extract goal/intent from user message."""
    msg = re.sub(r'^\s*\[[^\]]+\]\s*', '', user_message).strip()
    # Remove greetings
    msg = re.sub(r'^(alo|hi|hello|hey)\s*', '', msg, flags=re.IGNORECASE).strip()
    return msg[:100] if msg else ""


def extract_tags(user_message: str, response: str) -> list[str]:
    """Auto-extract tags from message + response content."""
    tags = ["transcript"]
    text = (user_message + " " + response).lower()
    
    # Domain keywords
    domain_map = {
        "tiktok": ["tiktok", "tiktok shop", "affiliate"],
        "youtube": ["youtube", "video", "short"],
        "wiki": ["wiki", "transcript"],
        "hermes": ["hermes", "agent", "hook"],
        "research": ["research", "nghiên cứu", "phân tích"],
        "code": ["code", "python", "javascript", "function", "def "],
        "telegram": ["telegram"],
        "obsidian": ["obsidian", "icloud"],
    }
    for tag, keywords in domain_map.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    
    # Action keywords
    action_map = {
        "setup": ["setup", "cài đặt", "configure"],
        "review": ["review", "đánh giá"],
        "fix": ["fix", "sửa", "lỗi"],
        "plan": ["plan", "kế hoạch", "lộ trình"],
        "analysis": ["phân tích", "analyze"],
    }
    for tag, keywords in action_map.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    
    return list(set(tags))[:6]  # max 6 tags


def find_related_entities(user_message: str, response: str) -> list[str]:
    """Find related entities/concepts in wiki by name matching."""
    text = (user_message + " " + response).lower()
    related = []
    
    # Scan entities folder
    if WIKI_ENTITIES.exists():
        for f in WIKI_ENTITIES.glob("*.md"):
            if f.name.startswith("."):
                continue
            name = f.stem
            # Check if name (or key parts) appears in text
            name_parts = name.replace("-", " ").split()
            if any(part in text for part in name_parts if len(part) > 3):
                related.append(f"[[{name}]]")
    
    # Scan concepts folder (top-level only, not sub-dirs)
    if WIKI_CONCEPTS.exists():
        for f in WIKI_CONCEPTS.glob("*.md"):
            if f.name.startswith(".") or f.name.endswith(".bak"):
                continue
            name = f.stem
            name_parts = name.replace("-", " ").split()
            if any(part in text for part in name_parts if len(part) > 4):
                related.append(f"[[{name}]]")
    
    return related[:5]  # max 5 relationships


def read_verdict_from_state(session_id: str) -> str:
    """Read loop-engineering verdict for this session from state file."""
    try:
        profile = os.environ.get("HERMES_PROFILE", "default")
        state_file = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")) / "profiles" / profile / "state.md"
        if not state_file.exists():
            return "null"
        # Search for session_id in state file
        content = state_file.read_text(encoding="utf-8")
        if session_id in content:
            # Find verdict near session_id
            idx = content.find(session_id)
            window = content[max(0, idx-200):idx+500]
            if "| PASS |" in window:
                return "PASS"
            elif "| WARN |" in window:
                return "WARN"
            elif "| FAIL |" in window:
                return "FAIL"
        return "null"
    except Exception:
        return "null"


def count_words(text: str) -> int:
    """Count words in mixed Vietnamese/English text."""
    return len(re.findall(r'\b\w+\b', text))


def write_obsidian_mirror(filepath: Path, content: str) -> bool:
    """Mirror transcript to Obsidian iCloud folder.
    
    Tries 2 strategies:
    1. If OBSIDIAN_ROOT exists → mirror normally
    2. If not → try creating parent dirs (for test environments)
    """
    try:
        # Strategy 1: Mirror to real Obsidian if available
        if OBSIDIAN_ROOT.exists():
            mirror_path = OBSIDIAN_TRANSCRIPTS / filepath.relative_to(WIKI_TRANSCRIPTS)
            mirror_path.parent.mkdir(parents=True, exist_ok=True)
            mirror_path.write_text(content, encoding="utf-8")
            return True
        
        # Strategy 2: Auto-create Obsidian path (first run, or test env)
        # Only if we're in test mode (parent dir was monkey-patched)
        try:
            mirror_path = OBSIDIAN_TRANSCRIPTS / filepath.relative_to(WIKI_TRANSCRIPTS)
            mirror_path.parent.mkdir(parents=True, exist_ok=True)
            mirror_path.write_text(content, encoding="utf-8")
            return True
        except Exception:
            pass
        
        print(f"[transcript-saver-v2] Obsidian root not found, mirror skipped: {OBSIDIAN_ROOT}", flush=True)
        return False
    except Exception as e:
        print(f"[transcript-saver-v2] Obsidian mirror failed: {e}", flush=True)
        return False


# === Main entry point ===

def handle(event_type: str, context: dict) -> None:
    """
    Called by Hermes gateway on agent:end event.
    
    Context expected:
      - platform: str
      - user_id: str
      - session_id: str
      - message: str (user message)
      - response: str (assistant response)
    """
    try:
        # Accept all "end" events from Hermes shell hooks
        # Hermes uses: on_session_end, on_session_start, post_tool_call
        # We only care about events that fire AFTER agent responds
        END_EVENTS = (
            "agent:end", "agent_end",
            "on_session_end",  # Hermes shell hook event
        )
        if event_type not in END_EVENTS:
            return
        
        platform = context.get("platform", "unknown")
        user_id = context.get("user_id", "unknown")
        session_id = context.get("session_id", "unknown")
        user_message = context.get("message", "")
        assistant_response = context.get("response", "")
        if not user_message and not assistant_response:
            return
    
        # Defensive: skip if message/response are unsubstituted shell vars
        if user_message.startswith("$") or assistant_response.startswith("$"):
            print(f"[transcript-saver-v2] Skip: unsubstituted shell var in message/response", flush=True)
            return
        
        # Build paths
        now = now_vn()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")
        
        date_dir = WIKI_TRANSCRIPTS / date_str
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract fields
        title = extract_title(user_message, now)
        goal = extract_goal(user_message)
        tags = extract_tags(user_message, assistant_response)
        related = find_related_entities(user_message, assistant_response)
        verdict = read_verdict_from_state(session_id)
        word_count = count_words(user_message + assistant_response)
        
        # Build filename: HH-MM-SS_{session_id}_{slug}.md
        slug = sanitize_slug(re.sub(r'^\s*\[[^\]]+\]\s*', '', user_message)[:50] or "transcript")
        short_session = session_id[:8] if session_id != "unknown" else "x"
        filename = f"{time_str}_{short_session}_{slug}.md"
        filepath = date_dir / filename
        
        # Frontmatter
        frontmatter = {
            "title": title,
            "created": date_str,
            "updated": date_str,
            "type": "transcript",
            "tags": tags,
            "confidence": "high",
            "platform": platform,
            "user_id": user_id,
            "session_id": session_id,
            "goal": goal,
            "verdict": verdict,
            "word_count": word_count,
            "relationships": related,
            "source": "transcript-saver-v2",
        }
        
        # Build content
        frontmatter_yaml = "---\n" + "\n".join(
            f"{k}: {json.dumps(v, ensure_ascii=False) if isinstance(v, (list, str)) and k != 'relationships' else v}"
            for k, v in frontmatter.items()
        ) + "\n---\n"
        
        # Fix the frontmatter serialization (manual yaml)
        def fmt_value(v):
            if isinstance(v, list):
                return "[" + ", ".join(str(x) for x in v) + "]"
            return str(v)
        
        frontmatter_yaml = "---\n"
        for k, v in frontmatter.items():
            frontmatter_yaml += f"{k}: {fmt_value(v)}\n"
        frontmatter_yaml += "---\n"
        
        # Build body
        relationships_section = ""
        if related:
            relationships_section = "\n## Related\n\n" + "\n".join(f"- {r}" for r in related) + "\n"
        
        body = f"""
# {title}

**Session:** `{session_id}` | **Platform:** {platform} | **Time:** {now_str()}
**Verdict:** {verdict} | **Words:** {word_count}

## User Message

> {user_message or "_[no message]_"}

## Assistant Response

{assistant_response or "_[no response]_"}
{relationships_section}
## Tags

{', '.join(f'`{t}`' for t in tags)}

---
_Saved by transcript-saver v2.0 at {now_str()}_
"""
        
        content = frontmatter_yaml + body
        
        # Write primary
        filepath.write_text(content, encoding="utf-8")
        print(f"[transcript-saver-v2] Saved: {filepath}", flush=True)
        
        # Mirror to Obsidian
        if write_obsidian_mirror(filepath, content):
            print(f"[transcript-saver-v2] Mirrored to Obsidian", flush=True)
        
        # Log
        print(
            f"[transcript-saver-v2] Title: {title} | Tags: {len(tags)} | "
            f"Related: {len(related)} | Verdict: {verdict}",
            flush=True
        )
    
    except Exception as e:
        print(f"[transcript-saver-v2] Error: {e}", flush=True)


# === CLI entry point (for Hermes shell hook wrapper) ===
if __name__ == "__main__":
    import argparse
    import sys
    import json as json_lib
    
    parser = argparse.ArgumentParser(description="Transcript Saver v2.0 CLI")
    parser.add_argument("--event", default="agent_end", help="Event type")
    parser.add_argument("--output", default="", help="Assistant response")
    parser.add_argument("--response", default="", help="Alias for --output")
    parser.add_argument("--message", default="", help="User message")
    parser.add_argument("--session_id", default="unknown", help="Session ID")
    parser.add_argument("--platform", default="unknown", help="Platform")
    parser.add_argument("--user_id", default="unknown", help="User ID")
    
    args = parser.parse_args()
    
    # Strategy 1: Hermes shell hook passes JSON via stdin
    # Format: {hook_event_name, tool_name, tool_input, session_id, cwd, extra: {response, message, ...}}
    if not sys.stdin.isatty():
        try:
            stdin_data = sys.stdin.read()
            if stdin_data.strip():
                payload = json_lib.loads(stdin_data)
                args.event = payload.get("hook_event_name", args.event)
                args.session_id = payload.get("session_id", args.session_id)
                extra = payload.get("extra", {})
                args.response = extra.get("response", args.response)
                args.message = extra.get("message", args.message)
                args.platform = extra.get("platform", args.platform)
                args.user_id = extra.get("user_id", args.user_id)
        except (json_lib.JSONDecodeError, Exception) as e:
            print(f"[transcript-saver-v2] stdin parse failed: {e}", flush=True)
    
    # Normalize event name
    event = args.event.replace(":", "_") if args.event else "agent_end"  # agent:end → agent_end
    
    # Build context
    context = {
        "platform": args.platform,
        "user_id": args.user_id,
        "session_id": args.session_id,
        "message": args.message,
        "response": args.response or args.output,
    }
    
    handle(event, context)
