#!/usr/bin/env python3
"""Auto-reply pending queries with placeholder + notify user via Telegram.

Chạy mỗi 1 phút qua cron. Logic:
1. GET /queries?pending_only=true từ backend
2. Với mỗi pending query:
   - Gọi POST /queries/{id}/reply với placeholder text + link tới web
   - Skip nếu đã có reply
3. Notify anh Tuấn Anh qua Telegram với danh sách câu hỏi mới
"""

import json
import subprocess
import sys
import time
import urllib.request
from urllib.error import URLError

API_BASE = "https://tuananhs-mac-mini.taila86c48.ts.net"
SLUG = "mi-y-kontum-research"


def fetch_pending() -> list:
    try:
        req = urllib.request.Request(f"{API_BASE}/api/projects/{SLUG}/queries?pending_only=true&limit=10")
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
            return data.get("queries", [])
    except (URLError, Exception) as e:
        print(f"[auto-reply] fetch failed: {e}", file=sys.stderr)
        return []


def post_reply(query_id: str, answer: str) -> bool:
    try:
        body = json.dumps({"answer": answer}).encode("utf-8")
        req = urllib.request.Request(
            f"{API_BASE}/api/projects/{SLUG}/queries/{query_id}/reply",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status == 200
    except (URLError, Exception) as e:
        print(f"[auto-reply] post reply failed for {query_id}: {e}", file=sys.stderr)
        return False


def notify_telegram(text: str) -> bool:
    """Send notification via hermes CLI to current Telegram Company topic 3 session.

    Uses explicit chat_id from running gateway session (group -1004366612538 thread 3)
    so it lands in the SAME conversation anh Tuấn Anh is chatting with em in.
    """
    try:
        result = subprocess.run(
            ["hermes", "send", "--to", "telegram:-1004366612538:3", text],
            timeout=15,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[auto-reply] telegram notify failed: {e}", file=sys.stderr)
        return False


def main():
    pending = fetch_pending()
    if not pending:
        return  # no work

    print(f"[auto-reply] found {len(pending)} pending queries")

    # Auto-reply each + notify user
    notif_lines = ["📨 Câu hỏi mới từ web Mì Ý Yum Yum:"]
    for q in pending:
        qid = q["id"]
        tab = q.get("tab") or "?"
        question = q["question"][:80]
        answer = (
            f"⏳ Em (Hermes) đang xử lý câu hỏi tab `{tab}` của anh. "
            f"Em sẽ reply chi tiết trong session kế tiếp. "
            f"Anh có thể xem tại: https://miy-yum-yum.vercel.app (click 💬 góc phải dưới).\n\n"
            f"Câu hỏi: _{question}_"
        )
        ok = post_reply(qid, answer)
        if ok:
            notif_lines.append(f"• `{qid}` [{tab}]: {question}...")
            print(f"[auto-reply] replied to {qid}")

    if len(notif_lines) > 1:
        notify_telegram("\n".join(notif_lines))


if __name__ == "__main__":
    main()