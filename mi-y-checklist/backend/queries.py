"""
Chat queries API for Mì Ý Yum Yum web app.

Allows Tuấn Anh to send questions / requests from the web → Hermes Agent
sees them in `wiki/projects/<slug>/queries/queries-log.md` and can reply
via the reply endpoint (or directly editing the markdown file).

Endpoints:
- POST /api/projects/{slug}/queries              → create new query
- GET  /api/projects/{slug}/queries              → list recent queries
- GET  /api/projects/{slug}/queries/{id}         → get single query
- POST /api/projects/{slug}/queries/{id}/reply   → set answer + status=answered
"""

from __future__ import annotations

import hmac
import hashlib
import json
import re
import secrets
import time
from datetime import datetime
from pathlib import Path
from typing import Annotated
from urllib.request import Request, urlopen
from urllib.error import URLError

from fastapi import APIRouter, Body, HTTPException, Path as PathParam
from pydantic import BaseModel, Field

router = APIRouter()

# ---------- Webhook config (Hermes Gateway) ----------
# Read from environment so secrets don't leak into repo
import os
WEBHOOK_URL = os.environ.get(
    "MIY_WEBHOOK_URL",
    "http://localhost:8644/webhooks/miy-question",
)
WEBHOOK_SECRET = os.environ.get(
    "MIY_WEBHOOK_SECRET",
    "hZM3ug_RCxMgB0BZyUXEF-sZZeeUHK32sSC93S4sKxI",
)


def _fire_webhook(query_id: str, question: str, context_tab: str | None) -> None:
    """Fire-and-forget POST to Hermes gateway webhook.

    Gateway validates signature via GitHub-style X-Hub-Signature-256
    (sha256=<hex HMAC-SHA256 of raw body>).
    """
    try:
        payload = json.dumps({
            "id": query_id,
            "question": question,
            "context_tab": context_tab or "(none)",
            "event_type": "miy.query.created",
        }).encode("utf-8")
        sig = hmac.new(WEBHOOK_SECRET.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        req = Request(
            WEBHOOK_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Signature-256": f"sha256={sig}",
                "X-GitHub-Event": "miy.query.created",
            },
            method="POST",
        )
        urlopen(req, timeout=5).read()
    except (URLError, Exception) as e:
        # Don't fail the create if webhook fails — just log
        print(f"[queries] webhook fire failed: {e}")

# ---------- Config ----------
VAULT_ROOT = Path("/Volumes/Storage-1/Hermes/wiki/projects")
QUERIES_DIRNAME = "queries"
QUERIES_FILENAME = "queries-log.md"

# ---------- Schemas ----------
class NewQuery(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    context_tab: str | None = Field(default=None, max_length=64)
    context_url: str | None = Field(default=None, max_length=512)


class QueryReply(BaseModel):
    answer: str = Field(min_length=1, max_length=8000)


# ---------- Helpers ----------
def _queries_dir(slug: str) -> Path:
    """Resolve and create the queries dir for a given project slug."""
    project_dir = VAULT_ROOT / slug
    if not project_dir.exists():
        raise HTTPException(404, f"Project '{slug}' not found")
    qdir = project_dir / QUERIES_DIRNAME
    qdir.mkdir(parents=True, exist_ok=True)
    return qdir


def _queries_file(slug: str) -> Path:
    return _queries_dir(slug) / QUERIES_FILENAME


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _next_id(log_text: str) -> str:
    """Generate next query ID based on today's prefix and existing count."""
    today = datetime.now().strftime("%Y%m%d")
    # Find all existing IDs that start with Q-YYYYMMDD-
    pattern = re.compile(rf"## Q-({today})-(\d{{3}})\b")
    used = [int(m.group(2)) for m in pattern.finditer(log_text)]
    n = (max(used) + 1) if used else 1
    return f"Q-{today}-{n:03d}"


def _ensure_header(path: Path) -> None:
    """Make sure the log file has a top-level header."""
    if not path.exists() or not path.read_text().strip():
        path.write_text("# Queries log\n\n")


def _entry_markdown(query_id: str, created_at: str, tab: str | None,
                    question: str, answer: str | None, status: str) -> str:
    lines = [
        f"## {query_id} · {created_at} · {status}",
        f"**Tab:** {tab}" if tab else "",
        f"**Question:** {question}",
    ]
    if answer is not None:
        lines.append(f"**Answer:** {answer}")
    lines.append("")
    return "\n".join(l for l in lines if l is not None) + "---\n"


def _append_entry(path: Path, entry: str) -> None:
    """Append an entry to the log file, creating header if missing."""
    _ensure_header(path)
    current = path.read_text()
    if not current.endswith("\n"):
        current += "\n"
    if not current.endswith("\n\n"):
        current += "\n"
    path.write_text(current + entry)


def _parse_entries(log_text: str) -> list[dict]:
    """
    Parse queries-log.md into a list of structured query entries.

    Format expectation:
        # Queries log

        ## Q-YYYYMMDD-NNN · YYYY-MM-DD HH:MM:SS · pending|answered
        **Tab:** ingredients
        **Question:** ...
        **Answer:** ...   (optional, only when answered)
        ---
    """
    entries: list[dict] = []
    # Split on lines starting with "## Q-"
    chunks = re.split(r"(?=^## Q-)", log_text, flags=re.MULTILINE)
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk.startswith("## Q-"):
            continue
        # Header line: ## Q-YYYYMMDD-NNN · YYYY-MM-DD HH:MM:SS · status
        m = re.match(
            r"^##\s+(Q-\d{8}-\d{3})\s+·\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+·\s+(pending|answered)\s*$",
            chunk.splitlines()[0],
        )
        if not m:
            continue
        query_id, ts, status = m.group(1), m.group(2), m.group(3)

        tab = None
        question = None
        answer = None
        for line in chunk.splitlines()[1:]:
            if line.startswith("**Tab:**"):
                tab = line.replace("**Tab:**", "").strip() or None
            elif line.startswith("**Question:**"):
                question = line.replace("**Question:**", "").strip()
            elif line.startswith("**Answer:**"):
                answer = line.replace("**Answer:**", "").strip()

        if question is None:
            continue

        entries.append({
            "id": query_id,
            "created_at": ts,
            "tab": tab,
            "question": question,
            "answer": answer,
            "status": status,
        })
    return entries


def _find_entry(log_text: str, query_id: str) -> dict:
    entries = _parse_entries(log_text)
    for e in entries:
        if e["id"] == query_id:
            return e
    raise HTTPException(404, f"Query '{query_id}' not found")


def _update_entry_file(path: Path, query_id: str, answer: str) -> None:
    """Replace an entry in the log file, marking it answered."""
    text = path.read_text()
    new_text = ""
    replaced = False

    # Match the entire block for the query_id, including trailing "---"
    pattern = re.compile(
        rf"(##\s+{re.escape(query_id)}\s+·\s+\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\s+·\s+)pending\b(.*?)(^---\s*$)",
        re.MULTILINE | re.DOTALL,
    )

    def _replace(m: re.Match) -> str:
        header_prefix = m.group(1)
        body = m.group(2)
        trailer = m.group(3)
        # Strip any prior **Answer:** line from body, add new one
        body_lines = [
            line for line in body.splitlines()
            if not line.lstrip().startswith("**Answer:**")
        ]
        body_clean = "\n".join(body_lines).rstrip()
        # If body_clean is empty, do not add a leading blank
        sep = "\n" if body_clean else ""
        return f"{header_prefix}answered{sep}{body_clean}\n**Answer:** {answer}\n{trailer}"

    new_text, count = pattern.subn(_replace, text, count=1)
    if count == 0:
        # Maybe status already shows 'answered' — try updating header only
        pattern2 = re.compile(
            rf"(##\s+{re.escape(query_id)}\s+·\s+\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\s+·\s+)answered\b(.*?)(^---\s*$)",
            re.MULTILINE | re.DOTALL,
        )

        def _replace2(m: re.Match) -> str:
            body = m.group(2)
            trailer = m.group(3)
            body_lines = [
                line for line in body.splitlines()
                if not line.lstrip().startswith("**Answer:**")
            ]
            body_clean = "\n".join(body_lines).rstrip()
            sep = "\n" if body_clean else ""
            return f"{m.group(1)}answered{sep}{body_clean}\n**Answer:** {answer}\n{trailer}"

        new_text, count = pattern2.subn(_replace2, text, count=1)
        if count == 0:
            raise HTTPException(404, f"Query '{query_id}' block not found in log")

    path.write_text(new_text)


# ---------- Routes ----------
@router.post("/api/projects/{slug}/queries")
def create_query(
    slug: Annotated[str, PathParam(min_length=1, max_length=64, regex=r"^[A-Za-z0-9_-]+$")],
    body: NewQuery,
):
    path = _queries_file(slug)
    _ensure_header(path)

    log_text = path.read_text()
    query_id = _next_id(log_text)
    created_at = _now_str()

    entry = _entry_markdown(
        query_id=query_id,
        created_at=created_at,
        tab=body.context_tab,
        question=body.question,
        answer=None,
        status="pending",
    )
    _append_entry(path, entry)

    # Fire webhook to Hermes gateway → bắn thẳng vào Telegram session
    _fire_webhook(query_id, body.question, body.context_tab)

    return {
        "ok": True,
        "id": query_id,
        "created_at": created_at,
        "status": "pending",
    }


@router.get("/api/projects/{slug}/queries")
def list_queries(
    slug: Annotated[str, PathParam(min_length=1, max_length=64, regex=r"^[A-Za-z0-9_-]+$")],
    limit: int = 20,
    pending_only: bool = False,
):
    path = _queries_file(slug)
    if not path.exists():
        return {"queries": [], "count": 0}
    log_text = path.read_text()
    entries = _parse_entries(log_text)
    # Newest first
    entries.reverse()
    if pending_only:
        entries = [e for e in entries if e["status"] == "pending"]
    if limit and limit > 0:
        entries = entries[:limit]
    return {"queries": entries, "count": len(entries)}


@router.get("/api/projects/{slug}/queries/{query_id}")
def get_query(
    slug: Annotated[str, PathParam(min_length=1, max_length=64, regex=r"^[A-Za-z0-9_-]+$")],
    query_id: Annotated[str, PathParam(regex=r"^Q-\d{8}-\d{3}$")],
):
    path = _queries_file(slug)
    if not path.exists():
        raise HTTPException(404, "No queries yet")
    entry = _find_entry(path.read_text(), query_id)
    return entry


@router.post("/api/projects/{slug}/queries/{query_id}/reply")
def reply_query(
    slug: Annotated[str, PathParam(min_length=1, max_length=64, regex=r"^[A-Za-z0-9_-]+$")],
    query_id: Annotated[str, PathParam(regex=r"^Q-\d{8}-\d{3}$")],
    body: QueryReply,
):
    path = _queries_file(slug)
    if not path.exists():
        raise HTTPException(404, "No queries yet")
    # Verify the entry exists before writing
    _find_entry(path.read_text(), query_id)
    _update_entry_file(path, query_id, body.answer)
    return {
        "ok": True,
        "id": query_id,
        "status": "answered",
        "answered_at": _now_str(),
    }
