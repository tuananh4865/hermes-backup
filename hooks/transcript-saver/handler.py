"""
Transcript Saver Hook

Lưu transcript từng message (user + assistant) vào wiki/raw/transcripts
theo thời gian thực sau mỗi agent:end event.

Format lưu: wiki/raw/transcripts/{YYYY-MM-DD}/{HH}-{session_id}.md
"""

import os
import re
from datetime import datetime
from pathlib import Path


def sanitize_filename(text: str) -> str:
    """Remove characters that are unsafe for filenames."""
    # Remove anything that's not alphanumeric, space, hyphen, or underscore
    text = re.sub(r'[^\w\s\-]', '', text)
    # Replace spaces with dashes
    text = text.replace(' ', '-')
    # Truncate to 50 chars
    return text[:50] if text else "untitled"


def handle(event_type: str, context: dict) -> None:
    """
    Called on agent:end event.
    
    Context expected:
      - platform: str (telegram, discord, etc.)
      - user_id: str
      - session_id: str
      - message: str (user message, first 500 chars)
      - response: str (assistant response, first 500 chars)
    """
    try:
        platform = context.get("platform", "unknown")
        user_id = context.get("user_id", "unknown")
        session_id = context.get("session_id", "unknown")
        user_message = context.get("message", "")
        assistant_response = context.get("response", "")
        
        # Skip if no meaningful content
        if not user_message and not assistant_response:
            return
        
        # Create timestamp-based filename
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")
        
        # Wiki path: /Volumes/Storage-1/Hermes/wiki/raw/transcripts/{date}/
        wiki_root = Path("/Volumes/Storage-1/Hermes/wiki")
        transcript_dir = wiki_root / "raw" / "transcripts" / date_str
        transcript_dir.mkdir(parents=True, exist_ok=True)
        
        # Filename: {HH-MM-SS}_{platform}_{sanitized_user_msg}.md
        user_preview = sanitize_filename(user_message[:30]) if user_message else "no-message"
        filename = f"{time_str}_{platform}_{user_preview}.md"
        filepath = transcript_dir / filename
        
        # Build transcript content
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        content_lines = [
            "---",
            f"title: Transcript {timestamp}",
            f"created: {date_str}",
            f"platform: {platform}",
            f"user_id: {user_id}",
            f"session_id: {session_id}",
            f"timestamp: {timestamp}",
            "type: transcript",
            "tags: [transcript]",
            "---",
            "",
            f"## User Message ({timestamp})",
            "",
            user_message or "_[no message]_",
            "",
            "---",
            "",
            f"## Assistant Response",
            "",
            assistant_response or "_[no response]_",
            "",
            "---",
            f"_Saved by transcript-saver hook at {timestamp}_",
        ]
        
        content = "\n".join(content_lines)
        filepath.write_text(content, encoding="utf-8")
        
        print(f"[transcript-saver] Saved: {filepath}", flush=True)
        
    except Exception as e:
        # Never let errors break the main pipeline
        print(f"[transcript-saver] Error: {e}", flush=True)
