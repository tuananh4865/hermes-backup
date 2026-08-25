#!/usr/bin/env python3
"""find_target_folder.py — route a free-text snippet to the right wiki note/folder.

Part of the `vault-update` skill (EP @eptwts Post A Prompt 2, post 2080342488728904164).

Given a snippet of something Tuan Anh said, rank existing wiki notes that may already
cover the same subject, so the agent can SEARCH BEFORE CREATE (EP P2 hard rule #6) and
detect contradictions instead of silently adding note #150.

Lexical only — ripgrep/grep over the vault. No vector DB, no embeddings, no network.

Usage
-----
    python3 find_target_folder.py "anh chot gia booking 3 trieu moi video"
    python3 find_target_folder.py "studio moved to Kon Tum" --json
    python3 find_target_folder.py "gear mic Rode" --top 5 --vault /path/to/wiki

Output
------
Ranked candidates, each: (folder, file_path, match_score 0.0-1.0, rationale)
plus a suggested folder for a NEW note when nothing scores well.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

DEFAULT_VAULT = Path("/Volumes/Storage-1/Hermes/wiki")
SEARCH_DIRS = ("concepts", "entities", "projects", "comparisons")

# Weights: a token hit in the title is worth far more than a hit in the body.
W_TITLE = 5.0
W_TAG = 3.0
W_SLUG = 2.5
W_BODY = 1.0

# Volatile subjects from EP P2 ("what i charge, where i live, what i'm working on,
# who i'm working with"), mapped to this vault's vocabulary. A snippet touching one of
# these MUST end with exactly one live note, so conflicts matter more here.
# Hints are matched on WORD BOUNDARIES (see volatile_subjects) — substring matching gave
# false positives, e.g. "kontum" contains "o" and used to trip the location subject.
VOLATILE_HINTS: dict[str, tuple[str, ...]] = {
    "rate": ("gia", "price", "rate", "booking", "charge", "trieu", "ratecard", "phi", "bao nhieu"),
    "location": ("song", "chuyen", "location", "studio", "move", "moved", "base", "quay", "o tai"),
    "active_work": ("dang lam", "working", "project", "du an", "channel", "kenh"),
    "collaborators": ("hop tac", "partner", "brand", "agency", "client", "khach", "lien he", "team"),
    "gear": ("mic", "camera", "may", "gear", "thiet bi", "lens", "gimbal", "laptop", "macbook"),
    "pricing_tool": ("subscription", "plan", "goi", "pricing", "tra phi", "monthly"),
}

# Archived / backup material is history, not the current note — never routed to.
EXCLUDE_PARTS = ("_archive", "_backup", "_template", ".obsidian")
EXCLUDE_SUFFIXES = (".audit-backup", ".backup")

STOPWORDS = {
    # Vietnamese
    "anh", "em", "la", "co", "khong", "cua", "va", "cho", "voi", "nay", "do", "roi",
    "duoc", "moi", "nua", "thi", "ma", "de", "tu", "gio", "minh", "ban", "the", "nhe",
    "giup", "luon", "cai", "con", "chi", "hay", "se", "da", "bi", "ra", "vao", "len",
    "xuong", "tren", "duoi", "khi", "neu", "vi", "nhung", "cung", "chua", "toi", "lai",
    # English
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "be", "been",
    "to", "of", "in", "on", "at", "for", "with", "from", "by", "that", "this", "it",
    "i", "you", "we", "he", "she", "they", "my", "our", "his", "her", "their", "just",
    "now", "new", "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "about", "into", "than", "then", "there", "also", "not", "no", "yes", "am",
}


def deaccent(text: str) -> str:
    """Fold Vietnamese diacritics so 'giá' matches 'gia'."""
    nfkd = unicodedata.normalize("NFD", text)
    stripped = "".join(ch for ch in nfkd if not unicodedata.combining(ch))
    return stripped.replace("đ", "d").replace("Đ", "D")


def tokenize(snippet: str, min_len: int = 3) -> list[str]:
    folded = deaccent(snippet.lower())
    raw = re.findall(r"[a-z0-9]+", folded)
    seen: list[str] = []
    for tok in raw:
        if len(tok) < min_len or tok in STOPWORDS or tok.isdigit():
            continue
        if tok not in seen:
            seen.append(tok)
    return seen


def volatile_subjects(snippet: str) -> list[str]:
    """Word-boundary match so multi-word hints work and short hints don't over-fire."""
    folded = deaccent(snippet.lower())
    hits = []
    for subject, needles in VOLATILE_HINTS.items():
        for n in needles:
            if re.search(rf"(?<![a-z0-9]){re.escape(n)}(?![a-z0-9])", folded):
                hits.append(subject)
                break
    return hits


def is_excluded(path: Path) -> bool:
    """Archives, backups and templates are never routing targets."""
    if any(part in EXCLUDE_PARTS or part.startswith("_archive") for part in path.parts):
        return True
    return any(str(path).endswith(sfx) for sfx in EXCLUDE_SUFFIXES)


def searcher() -> list[str]:
    """Prefer ripgrep; fall back to grep -r. Both are lexical, per EP P2."""
    if shutil.which("rg"):
        return ["rg", "--no-messages", "-l", "-i", "--fixed-strings", "--glob", "*.md"]
    return ["grep", "-r", "-l", "-i", "-F", "--include=*.md"]


def files_matching(token: str, roots: Iterable[Path]) -> set[Path]:
    roots = [r for r in roots if r.exists()]
    if not roots:
        return set()
    cmd = searcher() + [token] + [str(r) for r in roots]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (subprocess.TimeoutExpired, OSError):
        return set()
    out: set[Path] = set()
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.endswith(".md"):
            p = Path(line)
            if not is_excluded(p):
                out.add(p)
    return out


FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def read_frontmatter(path: Path) -> dict[str, str]:
    """Minimal, dependency-free frontmatter reader (top-level scalars only)."""
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:6000]
    except OSError:
        return {}
    m = FM_RE.match(head)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if line.startswith((" ", "\t", "#")) or ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


@dataclass
class Candidate:
    folder: str
    file_path: str
    match_score: float
    rationale: str
    title: str = ""
    tags: str = ""
    as_of: str = ""
    superseded: bool = False
    likely_conflict: bool = False


def rank(snippet: str, vault: Path, top: int) -> tuple[list[Candidate], list[str], dict]:
    tokens = tokenize(snippet)
    vols = volatile_subjects(snippet)
    roots = [vault / d for d in SEARCH_DIRS]

    hits: dict[Path, list[str]] = {}
    for tok in tokens:
        for path in files_matching(tok, roots):
            hits.setdefault(path, []).append(tok)

    scored: list[Candidate] = []
    for path, toks in hits.items():
        fm = read_frontmatter(path)
        title = fm.get("title", "")
        tags = fm.get("tags", "")
        title_f = deaccent(title.lower())
        tags_f = deaccent(tags.lower())
        slug_f = deaccent(path.stem.lower())

        raw = 0.0
        where: list[str] = []
        for tok in toks:
            # Word-boundary match: "phi" must not score on "phiên", "mic" not on "atomic".
            pat = rf"(?<![a-z0-9]){re.escape(tok)}(?![a-z0-9])"
            if re.search(pat, title_f):
                raw += W_TITLE
                where.append(f"title:{tok}")
            elif re.search(pat, tags_f):
                raw += W_TAG
                where.append(f"tag:{tok}")
            elif re.search(pat, slug_f):
                raw += W_SLUG
                where.append(f"slug:{tok}")
            else:
                raw += W_BODY
                where.append(f"body:{tok}")

        # Normalise: perfect score = every query token matched in a title.
        ceiling = max(len(tokens), 1) * W_TITLE
        score = min(raw / ceiling, 1.0)

        superseded = fm.get("superseded", "").lower() in {"true", "yes"}
        if superseded:
            score *= 0.4  # history, not the current note

        try:
            rel = path.relative_to(vault)
        except ValueError:
            rel = path
        folder = rel.parts[0] if len(rel.parts) > 1 else "."
        if folder == "projects" and len(rel.parts) > 2:
            folder = f"projects/{rel.parts[1]}"

        conflict = bool(vols) and not superseded and score >= 0.30

        bits = [f"matched {len(toks)}/{len(tokens)} tokens", ", ".join(where[:6])]
        if superseded:
            bits.append("already superseded (down-weighted)")
        if conflict:
            bits.append(f"volatile subject ({'/'.join(vols)}) - check for contradiction")

        scored.append(
            Candidate(
                folder=folder,
                file_path=str(rel),
                match_score=round(score, 3),
                rationale="; ".join(b for b in bits if b),
                title=title,
                tags=tags,
                as_of=fm.get("as_of", ""),
                superseded=superseded,
                likely_conflict=conflict,
            )
        )

    scored.sort(key=lambda c: (-c.match_score, c.file_path))
    return scored[:top], tokens, {"volatile_subjects": vols}


def suggest_new(snippet: str, vault: Path) -> dict[str, str]:
    """Where a NEW note should go when nothing existing fits (SKILL.md Step 3)."""
    folded = deaccent(snippet.lower())
    projects_dir = vault / "projects"
    if projects_dir.exists():
        for child in sorted(projects_dir.iterdir()):
            if not child.is_dir() or child.name.startswith("_"):
                continue
            words = [w for w in child.name.split("-") if len(w) > 3]
            if words and any(w in folded for w in words):
                return {
                    "folder": f"projects/{child.name}",
                    "reason": f"snippet mentions project '{child.name}'",
                }
    # Person / brand / company signals. Bare pronouns ("anh ", "ban ") are deliberately
    # excluded — they appear in almost every Vietnamese sentence and misrouted gear and
    # rate facts into entities/ during testing.
    person_hints = ("brand", "agency", "company", "shopee", "tiktok shop", "partner",
                    "hop tac", "lien he", "client", "khach hang", "chi ", "ceo", "founder")
    if any(h in folded for h in person_hints):
        return {"folder": "entities", "reason": "snippet looks person/brand/company-scoped"}
    return {"folder": "concepts", "reason": "default flat folder for facts, decisions, gear, rates, locations"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Rank existing wiki notes for a snippet (vault-update Step 2).")
    ap.add_argument("snippet", help="free text the user said")
    ap.add_argument("--vault", default=os.environ.get("HERMES_WIKI", str(DEFAULT_VAULT)))
    ap.add_argument("--top", type=int, default=3, help="candidates to return (default 3)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    vault = Path(args.vault).expanduser()
    if not vault.exists():
        print(f"ERROR: vault not found: {vault}", file=sys.stderr)
        return 2

    cands, tokens, meta = rank(args.snippet, vault, max(args.top, 1))
    new_note = suggest_new(args.snippet, vault)
    payload = {
        "snippet": args.snippet,
        "vault": str(vault),
        "tokens": tokens,
        "volatile_subjects": meta["volatile_subjects"],
        "candidates": [asdict(c) for c in cands],
        "suggested_new_note": new_note,
        "verdict": (
            "no_candidates_create_new" if not cands
            else "likely_conflict_check_supersede" if any(c.likely_conflict for c in cands)
            else "possible_existing_note_read_before_create" if cands[0].match_score >= 0.30
            else "weak_matches_probably_create_new"
        ),
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"snippet : {args.snippet}")
    print(f"tokens  : {', '.join(tokens) or '(none)'}")
    if meta["volatile_subjects"]:
        print(f"volatile: {', '.join(meta['volatile_subjects'])}  -> only ONE note may stay current")
    print(f"verdict : {payload['verdict']}")
    print()
    if not cands:
        print("no existing note matched.")
    for i, c in enumerate(cands, 1):
        flag = "  ⚠ CONFLICT?" if c.likely_conflict else ""
        print(f"{i}. [{c.match_score:.2f}] {c.folder}/  ->  {c.file_path}{flag}")
        if c.title:
            print(f"     title : {c.title}")
        if c.as_of:
            print(f"     as_of : {c.as_of}")
        print(f"     why   : {c.rationale}")
    print()
    print(f"new note would go to: {new_note['folder']}/   ({new_note['reason']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
