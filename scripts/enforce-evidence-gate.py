#!/usr/bin/env python3
"""
5-Evidence Gate Enforcer (System-Wide)
========================================

Runs as pre-tool-use hook. When agent claims "done / saved / fixed / shipped",
this script:
  1. Parses the assistant's last message for completion keywords
  2. If detected, scans the conversation/tool history for VERIFY evidence
  3. If NO evidence found → INJECTS warning back to the agent
  4. If evidence found → silently allows

Usage:
  Called by Hermes pre_tool_use hook when tool == 'reply' or final message.

Author: Hermes Agent (post-incident 2026-07-05)
"""

import re
import sys
import json

# Keywords that signal "claim done" — each must be paired with EVIDENCE
COMPLETION_KEYWORDS = [
    r"đã (?:lưu|tạo|sửa|xong|fix|ship|deploy|update|ghi|viết)",
    r"(?:đã|đã làm|đã chạy) xong",
    r"ship(?:ped)? ok",
    r"deploy(?:ed)? (?:to |on )?(?:staging|prod|github|pages)",
    r"(?:file|code|script|config) (?:đã )?(?:được )?(?:tạo|sửa|lưu|update|deploy)",
    r"hoàn thành",
    r"complete[d]?",
    r"finished",
    r"✅",
    r"task done",
    r"(?:v\d+\.\d+\.?\.?\d*) (?:live|shipped|deployed)",
]

# Evidence commands — if these appear in tool history, evidence exists
EVIDENCE_COMMANDS = [
    r"\bls\s+-la\b",
    r"\bwc\s+-c\b",
    r"\bhead\s+-?\d*",
    r"\btail\s+-?\d*",
    r"\bgrep\b",
    r"\bcat\s+\S+\.(?:md|py|js|yaml|json|txt|env)",
    r"\bfind\b",
    r"\bstat\b",
    r"\bfile\s+\S+\s+exists\b",
    r"\bcurl\s+-[sSI]\b",
    r"\bhermes\s+cron\s+list\b",
    r"\bgit\s+(?:status|log|diff|rev-parse)\b",
    r"bytes_written",
    r"'content':",  # write_file successful return
    r"'status':\s*['\"]ok['\"]",  # generic API success
]


def detect_completion_claim(text: str) -> bool:
    """Check if the agent's message claims completion."""
    text_lower = text.lower()
    for pattern in COMPLETION_KEYWORDS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False


def detect_evidence(history: str) -> bool:
    """Check if there's any evidence command in recent tool history."""
    for pattern in EVIDENCE_COMMANDS:
        if re.search(pattern, history, re.IGNORECASE):
            return True
    return False


def main():
    """
    Stdin: JSON with last_assistant_message + tool_history
    Stdout: warning text to inject, or empty if no warning needed
    """
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:
        return  # no payload → silent allow

    last_msg = payload.get("last_assistant_message", "")
    tool_history = payload.get("tool_history", "")

    if not detect_completion_claim(last_msg):
        return  # no completion claim → silent allow

    if detect_evidence(tool_history):
        return  # evidence found → silent allow

    # NO EVIDENCE — inject warning
    warning = """

🚨 **5-EVIDENCE GATE WARNING** 🚨

Bạn vừa nói "đã làm X / đã lưu X / đã fix X" nhưng KHÔNG có evidence nào trong tool history (ls / wc / head / grep / file exists / curl).

**Trước khi gửi reply cho user, PHẢI chạy ít nhất 1 verify command:**

```bash
# Ví dụ — file write:
ls -la <path>           # file tồn tại?
wc -c <path>            # size > 0?
head -5 <path>          # content đúng?
grep -c "<keyword>" <path>  # feature có trong file?
```

**Sau khi có evidence → mới được trả lời user kèm bảng evidence.**

Đây là session 2026-07-05 incident — đã lỗi 1 lần, không được lỗi lần 2.
"""
    print(warning, file=sys.stdout)


if __name__ == "__main__":
    main()
