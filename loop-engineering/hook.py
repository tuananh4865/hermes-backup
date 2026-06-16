"""
Loop Engineering Gateway Hook
=============================

Auto-trigger pattern: Maker → Checker → Orchestrator → User
HERMES_HOME-aware: detect active profile via env var.

Hooks:
- agent:end: run quality-checker if output is content/research/build
- agent:end: run /goal loop if /goal tag detected
- cron:job:done: update state file
- session:start: load state file of active profile
"""
import os
import sys
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

# HERMES_HOME-aware
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
PROFILE = os.environ.get("HERMES_PROFILE", "default")

# Add helpers to path
sys.path.insert(0, str(HERMES_HOME / "loop-engineering"))
import profile_state  # noqa: E402

TZ_VN = timezone(timedelta(hours=7))


def now_str() -> str:
    return datetime.now(TZ_VN).strftime("%Y-%m-%d %H:%M:%S %z")


# === Task type detection ===
CONTENT_KEYWORDS = [
    "report", "script", "research", "analysis", "tổng hợp", "phân tích",
    "trend", "review", "summary", "findings", "kết quả", "báo cáo",
]

SKIP_KEYWORDS = [
    "?", "what is", "how do you", "tell me about", "explain",
]


def detect_task_type(output: str) -> str:
    """Detect task type from output content."""
    output_lower = output.lower()

    # Skip if it's a question/chat
    if any(kw in output_lower for kw in SKIP_KEYWORDS) and len(output) < 500:
        return "qa"

    # Check for content/research keywords
    if any(kw in output_lower for kw in CONTENT_KEYWORDS):
        if "research" in output_lower or "nguồn" in output_lower or "url" in output_lower:
            return "research"
        if "script" in output_lower or "hook" in output_lower:
            return "script"
        if "report" in output_lower or "tổng hợp" in output_lower:
            return "report"
        return "content"

    # Check for code patterns
    if "```python" in output or "```bash" in output or "def " in output or "import " in output:
        return "code"

    return "other"


# === Quality Checker invocation ===
def run_quality_checker(output: str, task_type: str) -> dict:
    """
    Run quality-checker logic on output.
    Returns verdict dict.
    """
    issues = []
    scores = {
        "format": 10,
        "voice": 10,
        "sources": 10,
        "quality": 10,
        "project_specific": 10,
        "actionability": 10,
    }

    output_lower = output.lower()

    # === Format check ===
    if "```" in output and not any(f"```{lang}" for lang in ["python", "yaml", "json", "bash", "yaml", "markdown"]):
        scores["format"] -= 1
        issues.append({
            "category": "format", "severity": "minor",
            "description": "Code block không có language tag"
        })

    # === Voice check (per profile) ===
    if PROFILE in ("content-director", "default"):
        # Content scripts: cấm "mấy con vợ", etc.
        banned = ["mấy con vợ", "mấy đứa", "mấy chị", "quất một phát", "đỉnh nóc kịch trần"]
        for pattern in banned:
            count = output_lower.count(pattern)
            if count > 0:
                scores["voice"] -= 2 * count
                issues.append({
                    "category": "voice", "severity": "critical",
                    "description": f"Dùng '{pattern}' {count} lần (cấm)",
                })
    else:
        # Hermes general: cấm "anh ơi" lặp, mấy con vợ
        banned = ["mấy con vợ", "mấy đứa", "mấy chị"]
        for pattern in banned:
            count = output_lower.count(pattern)
            if count > 0:
                scores["voice"] -= 2 * count
                issues.append({
                    "category": "voice", "severity": "critical",
                    "description": f"Dùng '{pattern}' {count} lần",
                })

    # === Sources check (research) ===
    if task_type == "research":
        urls = re.findall(r'https?://[^\s\)]+', output)
        n_urls = len(urls)
        if n_urls == 0:
            scores["sources"] = 0
            issues.append({
                "category": "sources", "severity": "critical",
                "description": "Research output không có URL nguồn"
            })
        elif n_urls < 5:
            scores["sources"] = max(0, n_urls * 2)
            issues.append({
                "category": "sources", "severity": "warning",
                "description": f"Chỉ có {n_urls} URLs, cần ≥5 cho research"
            })

    # === Quality bar (no chung chung) ===
    banned_quality = [
        ("có thể là", "chung chung"),
        ("thường thì", "chung chung"),
        ("nhiều khi", "chung chung"),
        ("khá nhiều", "chung chung"),
    ]
    for phrase, issue_type in banned_quality:
        count = output_lower.count(phrase)
        if count > 0:
            scores["quality"] -= count
            # Research tasks: chung chung = critical (no data = no research)
            severity = "critical" if task_type == "research" else ("warning" if count == 1 else "critical")
            issues.append({
                "category": "quality", "severity": severity,
                "description": f"Dùng '{phrase}' {count} lần — {issue_type}"
            })

    # === Compute final score ===
    weights = {
        "format": 0.10, "voice": 0.15, "sources": 0.25,
        "quality": 0.25, "project_specific": 0.15, "actionability": 0.10,
    }
    final_score = sum(scores[k] * weights[k] for k in weights)

    # === Verdict ===
    has_critical = any(i.get("severity") == "critical" for i in issues)
    if has_critical:
        verdict = "FAIL"
    elif final_score >= 9.0:
        verdict = "PASS"
    elif final_score >= 7.0:
        verdict = "WARN"
    else:
        verdict = "FAIL"

    return {
        "verdict": verdict,
        "score": round(final_score, 1),
        "scores": scores,
        "issues": issues,
        "task_type": task_type,
        "profile": PROFILE,
        "timestamp": now_str(),
    }


# === Hook entry points ===
def on_agent_end(task_result: dict, **kwargs) -> dict:
    """
    Hermes hook: agent:end event.
    Auto-run quality-checker if output is content/research/build.
    """
    output = task_result.get("output", "")
    if not output or len(output) < 100:
        return {"verdict": "SKIP", "reason": "output too short"}

    # Detect task type
    task_type = detect_task_type(output)
    if task_type in ("qa", "other"):
        return {"verdict": "SKIP", "reason": f"task type: {task_type}"}

    # Run checker
    verdict = run_quality_checker(output, task_type)

    # Log to state file
    profile_state.append_verdict(
        profile=PROFILE,
        verdict=verdict["verdict"],
        score=verdict["score"],
        issues=verdict["issues"],
        goal=task_result.get("goal", ""),
        worker=PROFILE,
    )

    return verdict


def on_cron_done(task_result: dict, **kwargs) -> dict:
    """
    Hermes hook: cron:job:done event.
    Log to state file.
    """
    profile_state.append_run(
        profile=PROFILE,
        goal=task_result.get("goal", "cron task"),
        runs=1,
        result=task_result.get("status", "PASS"),
        score=task_result.get("score", 0.0),
    )
    return {"logged": True}


def on_session_start(**kwargs) -> dict:
    """
    Hermes hook: session:start event.
    Load state file of active profile.
    """
    state = profile_state.read_state(PROFILE)
    return {
        "profile": PROFILE,
        "state_loaded": True,
        "state_preview": state[:500],
    }


# === CLI for testing ===
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", choices=[
        "agent:end", "cron:job:done", "session:start",
        "on_session_start", "on_session_end", "post_tool_call",
    ], required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--goal", default="")
    parser.add_argument("--status", default="PASS")
    parser.add_argument("--score", type=float, default=0.0)
    args = parser.parse_args()

    if args.event in ("agent:end", "post_tool_call"):
        result = on_agent_end({"output": args.output, "goal": args.goal})
    elif args.event == "cron:job:done":
        result = on_cron_done({"goal": args.goal, "status": args.status, "score": args.score})
    elif args.event in ("session:start", "on_session_start"):
        result = on_session_start()
    elif args.event == "on_session_end":
        result = on_cron_done({"goal": "session ended", "status": "PASS", "score": 0.0})

    print(json.dumps(result, indent=2, ensure_ascii=False))
