"""
Local API backend for Mì Ý Yum Yum project — multi-file support.

Supported files per project:
- checklist.md   (default — launch checklist with - [ ] / - [x] tasks)
- ingredients.md (bảng nguyên phụ liệu + link Shopee, cùng format checklist)
- recipes.md     (công thức 5 món + test tasks)
- budget.md      (ngân sách + KPI)
- calendar.md    (TikTok content calendar)

Cùng parser + serializer cho tất cả 5 file (markdown checklist format).
"""

from __future__ import annotations

import re
import secrets
import time
from pathlib import Path
from typing import Annotated, Literal

from fastapi import Body, FastAPI, HTTPException, Path as PathParam
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from queries import router as queries_router
from pos import router as pos_router

# ---------- Config ----------
VAULT_ROOT = Path("/Volumes/Storage-1/Hermes/wiki/projects")
ALLOWED_FILES = (
    "checklist",
    "ingredients",
    "recipes",
    "budget",
    "calendar",
    "cost",
    "orders",
    "sales",
)

app = FastAPI(title="Mi-Y Project API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount chat-queries API (chat widget → Hermes Agent inbox)
app.include_router(queries_router)
app.include_router(pos_router)


# ---------- Helpers ----------
def file_path(slug: str, file: str) -> Path:
    if file not in ALLOWED_FILES:
        raise HTTPException(400, f"file must be one of {ALLOWED_FILES}")
    project_dir = VAULT_ROOT / slug
    if not project_dir.exists():
        raise HTTPException(404, f"Project '{slug}' not found")
    return project_dir / f"{file}.md"


def parse_checklist(text: str) -> dict:
    lines = text.splitlines()
    frontmatter: dict[str, str] = {}
    body_start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                for raw in lines[1:i]:
                    if ":" in raw:
                        k, _, v = raw.partition(":")
                        frontmatter[k.strip()] = v.strip()
                body_start = i + 1
                break

    body = "\n".join(lines[body_start:]).lstrip("\n")
    sections: list[dict] = []
    current: dict | None = None
    for raw in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", raw)
        if m:
            if current:
                sections.append(current)
            current = {"title": m.group(1).strip(), "tasks": []}
            continue
        m = re.match(r"^-\s+\[(?P<done>[ xX])\]\s+(?P<rest>.*)$", raw)
        if m and current is not None:
            rest = m.group("rest").strip()
            task_id_match = re.search(r"`id:\s*([A-Za-z0-9_-]+)`", rest)
            task_id = task_id_match.group(1) if task_id_match else secrets.token_hex(4)
            display = re.sub(r"\s*`id:\s*[A-Za-z0-9_-]+`\s*$", "", rest).strip()
            current["tasks"].append(
                {"id": task_id, "text": display, "done": m.group("done").lower() == "x"}
            )
        elif current is not None and raw.strip():
            current.setdefault("notes", []).append(raw.rstrip())

    if current:
        sections.append(current)

    return {"frontmatter": frontmatter, "sections": sections}


def serialize_checklist(parsed: dict) -> str:
    fm = parsed.get("frontmatter", {})
    out: list[str] = ["---"]
    for k, v in fm.items():
        out.append(f"{k}: {v}")
    out.append("---")
    out.append("")
    for sec in parsed.get("sections", []):
        out.append(f"## {sec['title']}")
        out.append("")
        for task in sec.get("tasks", []):
            mark = "x" if task.get("done") else " "
            task_id = task.get("id") or secrets.token_hex(4)
            out.append(f"- [{mark}] {task['text']} `id:{task_id}`")
        for note in sec.get("notes", []):
            out.append(note)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def find_task(parsed: dict, task_id: str) -> tuple[int, int]:
    for si, sec in enumerate(parsed.get("sections", [])):
        for ti, t in enumerate(sec.get("tasks", [])):
            if t["id"] == task_id:
                return si, ti
    raise HTTPException(404, f"Task '{task_id}' not found in {parsed.get('frontmatter', {}).get('title', '?')}")


def find_section(parsed: dict, phase: str) -> int:
    for si, sec in enumerate(parsed.get("sections", [])):
        if sec["title"].lower() == phase.lower() or sec["title"].lower().startswith(phase.lower()):
            return si
    raise HTTPException(404, f"Phase '{phase}' not found")


def load_parsed(slug: str, file: str) -> dict:
    p = file_path(slug, file)
    if not p.exists():
        seed = {
            "frontmatter": {
                "title": f"{file} for {slug}",
                "project": slug,
                "type": file,
                "last_modified": time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "sections": [{"title": "Empty", "tasks": []}],
        }
        p.write_text(serialize_checklist(seed))
        return seed
    return parse_checklist(p.read_text())


def save_parsed(slug: str, file: str, parsed: dict) -> None:
    parsed.setdefault("frontmatter", {})["last_modified"] = time.strftime("%Y-%m-%d %H:%M:%S")
    file_path(slug, file).write_text(serialize_checklist(parsed))


# ---------- Schemas ----------
class TaskPatch(BaseModel):
    done: bool


class NewTask(BaseModel):
    phase: str
    text: str
    done: bool = False


class NoteAppend(BaseModel):
    phase: str
    text: str


# ---------- Routes ----------
@app.get("/healthz")
def healthz():
    return {
        "ok": True,
        "ts": int(time.time()),
        "vault": str(VAULT_ROOT),
        "files": ALLOWED_FILES,
    }


@app.get("/api/projects")
def list_projects():
    if not VAULT_ROOT.exists():
        raise HTTPException(500, f"Vault root missing: {VAULT_ROOT}")
    out = []
    for p in sorted(VAULT_ROOT.iterdir()):
        if p.is_dir():
            files = [f.stem for f in p.glob("*.md") if f.stem in ALLOWED_FILES]
            if files:
                out.append({"slug": p.name, "files": files})
    return {"projects": out}


@app.get("/api/projects/{slug}/files/{file}")
def get_file(
    slug: Annotated[str, PathParam(min_length=1, max_length=64, regex=r"^[A-Za-z0-9_-]+$")],
    file: str,
):
    return load_parsed(slug, file)


@app.put("/api/projects/{slug}/files/{file}/tasks/{task_id}")
def patch_task(slug: str, file: str, task_id: str, body: TaskPatch):
    parsed = load_parsed(slug, file)
    si, ti = find_task(parsed, task_id)
    parsed["sections"][si]["tasks"][ti]["done"] = body.done
    save_parsed(slug, file, parsed)
    return {"ok": True, "file": file, "task_id": task_id, "done": body.done}


@app.post("/api/projects/{slug}/files/{file}/tasks")
def add_task(slug: str, file: str, body: NewTask):
    parsed = load_parsed(slug, file)
    si = find_section(parsed, body.phase)
    new_id = secrets.token_hex(4)
    parsed["sections"][si].setdefault("tasks", []).append(
        {"id": new_id, "text": body.text, "done": body.done}
    )
    save_parsed(slug, file, parsed)
    return {"ok": True, "file": file, "task_id": new_id}


@app.delete("/api/projects/{slug}/files/{file}/tasks/{task_id}")
def delete_task(slug: str, file: str, task_id: str):
    parsed = load_parsed(slug, file)
    si, ti = find_task(parsed, task_id)
    deleted = parsed["sections"][si]["tasks"].pop(ti)
    save_parsed(slug, file, parsed)
    return {"ok": True, "file": file, "deleted": deleted}


@app.post("/api/projects/{slug}/files/{file}/notes")
def append_note(slug: str, file: str, body: NoteAppend):
    parsed = load_parsed(slug, file)
    si = find_section(parsed, body.phase)
    parsed["sections"][si].setdefault("notes", []).append(f"- {body.text}")
    save_parsed(slug, file, parsed)
    return {"ok": True, "file": file}


# ---------- Main ----------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=7891, log_level="info")
