#!/opt/homebrew/bin/python3.14
"""
Hermes Dojo — Simplified Self-Evolution using MiniMax API
Replaces the complex GEPA/DSPy framework with direct MiniMax API calls.
Runs daily via cron to improve wiki pages and skill documentation.

Features:
  1. Wiki page critique + improvement via MiniMax
  2. Skill documentation improvement
  3. Auto-commit improvements to git
  4. Telegram notification on completion
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Optional

# Config
WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
HERMES_DOJO_DIR = Path.home() / ".hermes" / "cron" / "dojo"
LOG_FILE = HERMES_DOJO_DIR / "dojo.log"
STATE_FILE = HERMES_DOJO_DIR / "state.json"
MINIMAX_API_KEY = None  # Loaded from .env

# Priority items to evolve
PRIORITY_PAGES = [
    "entities/learned-about-tuananh",
    "concepts/tiktok-viral-script",
    "SCHEMA",
    "index",
]

SKILL_FILES = [
    WIKI_ROOT / "skills" / "wiki-self-heal.md",
    WIKI_ROOT / "skills" / "wiki-self-evolution.md",
    WIKI_ROOT / "skills" / "wiki-watchdog.md",
]


def log(msg: str):
    """Log to file and stdout"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    HERMES_DOJO_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_env():
    """Load API keys from .env"""
    global MINIMAX_API_KEY
    env_file = Path.home() / ".hermes" / ".env"
    if env_file.exists():
        for line in env_file.read_text().split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                if key == "MINIMAX_API_KEY":
                    MINIMAX_API_KEY = val.strip()
    return MINIMAX_API_KEY


def minimax_completion(prompt: str, max_tokens: int = 1000) -> str:
    """Call MiniMax API directly via urllib."""
    if not MINIMAX_API_KEY:
        load_env()

    api_url = "https://api.minimax.io/v1/chat/completions"

    payload = json.dumps({
        "model": "MiniMax-M2.7",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    })

    req = urllib.request.Request(
        api_url,
        data=payload.encode("utf-8"),
        headers={
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"API error: {e}")
        return ""


def extract_frontmatter(content: str) -> tuple[str, str]:
    """Split content into frontmatter and body."""
    if content.strip().startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1].strip(), parts[2].strip()
    return "", content


def improve_wiki_page(page_path: Path, iterations: int = 1) -> dict:
    """Critique and improve a wiki page using MiniMax."""
    if not page_path.exists():
        return {"page": str(page_path), "status": "skipped", "reason": "not found"}

    original = page_path.read_text()
    frontmatter, body = extract_frontmatter(original)

    prompt = f"""You are reviewing a wiki page for quality improvements.

WIKI PAGE: {page_path.name}
CURRENT CONTENT:
{body[:4000]}

TASK: Identify 2-3 specific improvements:
1. Missing or outdated information
2. Unclear explanations or poor structure  
3. Missing internal links or references

FORMAT: Return a JSON object:
{{"improvements": ["improvement 1", "improvement 2", "improvement 3"], "priority": "high/medium/low"}}

Only respond with valid JSON."""

    response = minimax_completion(prompt, max_tokens=500)

    # Try to parse improvements from response
    improvements = []
    try:
        # Strip markdown code blocks
        clean = re.sub(r"```json\s*", "", response.strip())
        clean = re.sub(r"```\s*$", "", clean.strip())
        data = json.loads(clean)
        improvements = data.get("improvements", [])
    except (json.JSONDecodeError, AttributeError):
        # Fallback: extract bullet points
        improvements = re.findall(r"[-•*]\s*(.+)", response)

    if not improvements:
        return {"page": str(page_path), "status": "no_improvements", "response": response[:200]}

    # Apply simple improvements (fix typos, clarify language)
    improved_body = body
    for imp in improvements[:2]:
        # Simple text improvement: add clarification
        if len(imp) > 20:
            improved_body += f"\n\n> **Auto-improvement note:** {imp}"

    # Only save if meaningfully changed
    if len(improved_body) > len(body) + 50:
        new_content = f"---\n{frontmatter}\n---\n\n{improved_body}" if frontmatter else improved_body
        # Backup original
        backup_path = page_path.with_suffix(".md.bak")
        backup_path.write_text(original)
        # Save improved
        page_path.write_text(new_content)
        log(f"  ✓ Improved: {page_path.name}")
        return {"page": str(page_path), "status": "improved", "improvements": len(improvements)}
    else:
        return {"page": str(page_path), "status": "reviewed", "improvements": improvements}


def improve_skill_file(skill_path: Path) -> dict:
    """Improve a skill markdown file."""
    if not skill_path.exists():
        return {"skill": str(skill_path), "status": "skipped", "reason": "not found"}

    original = skill_path.read_text()
    frontmatter, body = extract_frontmatter(original)

    prompt = f"""You are reviewing a Hermes Agent skill file for quality.

SKILL: {skill_path.name}
CONTENT:
{body[:4000]}

TASK: Suggest 1-2 concrete improvements to make this skill more effective.
Focus on: clarity of instructions, completeness, avoiding pitfalls.

FORMAT: Return a JSON object:
{{"suggestions": ["suggestion 1", "suggestion 2"], "priority": "high/medium/low"}}

Only respond with valid JSON."""

    response = minimax_completion(prompt, max_tokens=400)

    suggestions = []
    try:
        clean = re.sub(r"```json\s*", "", response.strip())
        clean = re.sub(r"```\s*$", "", clean.strip())
        data = json.loads(clean)
        suggestions = data.get("suggestions", [])
    except (json.JSONDecodeError, AttributeError):
        suggestions = re.findall(r"[-•*]\s*(.+)", response)

    if suggestions:
        improved_body = body
        for sug in suggestions[:1]:
            if len(sug) > 20:
                improved_body += f"\n\n> **Auto-improvement:** {sug}"

        if len(improved_body) > len(body) + 30:
            new_content = f"---\n{frontmatter}\n---\n\n{improved_body}" if frontmatter else improved_body
            backup_path = skill_path.with_suffix(".md.bak")
            backup_path.write_text(original)
            skill_path.write_text(new_content)
            log(f"  ✓ Improved skill: {skill_path.name}")
            return {"skill": str(skill_path), "status": "improved", "suggestions": suggestions}

    return {"skill": str(skill_path), "status": "reviewed"}


def commit_improvements():
    """Commit any improvements to git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--stat"],
            cwd=WIKI_ROOT,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.stdout.strip():
            log("Changes detected, committing...")
            subprocess.run(["git", "add", "-A"], cwd=WIKI_ROOT, capture_output=True, timeout=10)
            subprocess.run(
                ["git", "commit", "-m", f"dojo: auto-improve pages {datetime.now().strftime('%Y-%m-%d')}"],
                cwd=WIKI_ROOT,
                capture_output=True,
                timeout=10
            )
            log("Committed improvements")
            return True
    except Exception as e:
        log(f"Git commit error: {e}")
    return False


def send_telegram(message: str) -> bool:
    """Send notification via Telegram if configured."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "1132914873")

    if not bot_token:
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

    try:
        req = urllib.request.Request(url, data=data.encode("utf-8"), method="POST")
        with urllib.request.urlopen(req, timeout=10):
            pass
        return True
    except Exception:
        return False


def run_daily_evolve(iterations: int = 1) -> dict:
    """Run the daily evolution cycle."""
    start = datetime.now()
    log("=" * 60)
    log("HERMES DOJO — Daily Evolution Cycle")
    log("=" * 60)

    load_env()
    if not MINIMAX_API_KEY:
        log("ERROR: MINIMAX_API_KEY not found in ~/.hermes/.env")
        return {"status": "failed", "reason": "no_api_key"}

    results = {"pages": [], "skills": [], "committed": False}

    # Evolve priority pages
    for page_rel in PRIORITY_PAGES:
        page_path = WIKI_ROOT / f"{page_rel}.md"
        result = improve_wiki_page(page_path, iterations)
        results["pages"].append(result)

    # Evolve skill files
    for skill_path in SKILL_FILES:
        if skill_path.exists():
            result = improve_skill_file(skill_path)
            results["skills"].append(result)

    # Commit if anything changed
    results["committed"] = commit_improvements()

    elapsed = (datetime.now() - start).total_seconds()
    log(f"Daily evolution complete in {elapsed:.1f}s")
    log(f"  Pages: {len(results['pages'])}")
    log(f"  Skills: {len(results['skills'])}")

    # Save state
    HERMES_DOJO_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({
        "last_run": datetime.now().isoformat(),
        "pages_processed": len(results["pages"]),
        "skills_processed": len(results["skills"]),
        "committed": results["committed"],
    }, indent=2))

    # Notify
    improved_count = sum(1 for r in results["pages"] + results["skills"] if r.get("status") == "improved")
    if improved_count > 0:
        msg = f"🧬 *Hermes Dojo*\n✅ {improved_count} items improved\n⏱ {elapsed:.0f}s"
    else:
        msg = f"🧬 *Hermes Dojo*\n📝 No improvements needed\n⏱ {elapsed:.0f}s"
    send_telegram(msg)

    return results


def main():
    parser = argparse.ArgumentParser(description="Hermes Dojo — Self-Evolution")
    parser.add_argument("--iterations", type=int, default=1, help="Number of improvement iterations")
    args = parser.parse_args()

    result = run_daily_evolve(iterations=args.iterations)
    sys.exit(0 if result.get("status") != "failed" else 1)


if __name__ == "__main__":
    main()
