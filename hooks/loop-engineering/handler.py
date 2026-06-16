"""
Loop Engineering Hook — Auto quality-check + /goal loop + state persistence

Pattern: Maker (subagent/profile) → Checker (this hook) → Orchestrator (em) → User (anh)

Events:
- agent:end: Run quality-checker on agent output, log to state file
- cron:job:done: Log cron run to state file
- session:start: Load state file of active profile
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

# Add profile_state helper to path
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
SKIP_KEYWORDS = ["?", "what is", "how do you", "tell me about", "explain"]


def detect_task_type(output: str) -> str:
    """Detect task type from output content."""
    output_lower = output.lower()
    if any(kw in output_lower for kw in SKIP_KEYWORDS) and len(output) < 500:
        return "qa"
    if any(kw in output_lower for kw in CONTENT_KEYWORDS):
        if "research" in output_lower or "nguồn" in output_lower or "url" in output_lower:
            return "research"
        if "script" in output_lower or "hook" in output_lower:
            return "script"
        if "report" in output_lower or "tổng hợp" in output_lower:
            return "report"
        return "content"
    if "```python" in output or "```bash" in output or "def " in output or "import " in output:
        return "code"
    return "other"


# === Quality Checker (embedded lightweight version) ===
def run_quality_checker(output: str, task_type: str) -> dict:
    """Run quality-checker logic on output. Returns verdict dict."""
    issues = []
    scores = {
        "format": 10, "voice": 10, "sources": 10, "quality": 10,
        "project_specific": 10, "actionability": 10,
    }
    output_lower = output.lower()

    # Format check
    if "```" in output and not any(f"```{lang}" for lang in ["python", "yaml", "json", "bash", "yaml", "markdown"]):
        scores["format"] -= 1
        issues.append({"category": "format", "severity": "minor", "description": "Code block không có language tag"})

    # Voice check (per profile)
    if PROFILE in ("content-director", "default"):
        banned = ["mấy con vợ", "mấy đứa", "mấy chị", "quất một phát", "đỉnh nóc kịch trần"]
    else:
        banned = ["mấy con vợ", "mấy đứa", "mấy chị"]
    for pattern in banned:
        count = output_lower.count(pattern)
        if count > 0:
            scores["voice"] -= 2 * count
            issues.append({
                "category": "voice", "severity": "critical",
                "description": f"Dùng '{pattern}' {count} lần (cấm)",
            })

    # Sources check (research)
    if task_type == "research":
        urls = re.findall(r'https?://[^\s\)]+', output)
        n_urls = len(urls)
        if n_urls == 0:
            scores["sources"] = 0
            issues.append({"category": "sources", "severity": "critical", "description": "Research output không có URL nguồn"})
        elif n_urls < 5:
            scores["sources"] = max(0, n_urls * 2)
            issues.append({"category": "sources", "severity": "warning", "description": f"Chỉ có {n_urls} URLs, cần ≥5 cho research"})

    # Quality bar
    banned_quality = [("có thể là", "chung chung"), ("thường thì", "chung chung"),
                      ("nhiều khi", "chung chung"), ("khá nhiều", "chung chung")]
    for phrase, issue_type in banned_quality:
        count = output_lower.count(phrase)
        if count > 0:
            scores["quality"] -= count
            severity = "critical" if task_type == "research" else ("warning" if count == 1 else "critical")
            issues.append({"category": "quality", "severity": severity,
                          "description": f"Dùng '{phrase}' {count} lần — {issue_type}"})

    # Final score
    weights = {"format": 0.10, "voice": 0.15, "sources": 0.25,
               "quality": 0.25, "project_specific": 0.15, "actionability": 0.10}
    final_score = sum(scores[k] * weights[k] for k in weights)

    has_critical = any(i.get("severity") == "critical" for i in issues)
    if has_critical:
        verdict = "FAIL"
    elif final_score >= 9.0:
        verdict = "PASS"
    elif final_score >= 7.0:
        verdict = "WARN"
    else:
        verdict = "FAIL"

    return {"verdict": verdict, "score": round(final_score, 1), "scores": scores,
            "issues": issues, "task_type": task_type, "profile": PROFILE, "timestamp": now_str()}


# === Hook entry point (Hermes format) ===
def handle(event_type: str, context: dict) -> None:
    """
    Main hook entry point. Called by Hermes gateway on each event.

    Context varies by event:
    - agent:end: {platform, user_id, session_id, response, message}
    - cron:job:done: {job_id, job_name, status, output}
    - session:start: {session_id, profile, platform}
    """
    try:
        if event_type == "agent:end":
            handle_agent_end(context)
        elif event_type == "cron:job:done":
            handle_cron_done(context)
        elif event_type == "session:start":
            handle_session_start(context)
        else:
            print(f"[loop-engineering] Unknown event: {event_type}", flush=True)
    except Exception as e:
        # Never let errors break the main pipeline
        print(f"[loop-engineering] Error: {e}", flush=True)


def handle_agent_end(context: dict) -> None:
    """Run quality-checker on agent output."""
    output = context.get("response", "") or context.get("output", "")
    if not output or len(output) < 100:
        print(f"[loop-engineering] SKIP: output too short ({len(output)} chars)", flush=True)
        return

    task_type = detect_task_type(output)
    if task_type in ("qa", "other"):
        print(f"[loop-engineering] SKIP: task type {task_type}", flush=True)
        return

    verdict = run_quality_checker(output, task_type)
    print(f"[loop-engineering] Verdict: {verdict['verdict']} (score: {verdict['score']}) | type: {task_type} | profile: {PROFILE}", flush=True)
    if verdict.get("issues"):
        for issue in verdict["issues"][:3]:
            print(f"[loop-engineering]   - [{issue['severity']}] {issue['description']}", flush=True)

    # Log to state file
    try:
        profile_state.append_verdict(
            profile=PROFILE,
            verdict=verdict["verdict"],
            score=verdict["score"],
            issues=verdict["issues"],
            goal=context.get("goal", ""),
            worker=PROFILE,
        )
    except Exception as e:
        print(f"[loop-engineering] Failed to log verdict: {e}", flush=True)


def handle_cron_done(context: dict) -> None:
    """Log cron run to state file."""
    try:
        profile_state.append_run(
            profile=PROFILE,
            goal=context.get("job_name", "cron task"),
            runs=1,
            result=context.get("status", "PASS"),
            score=0.0,
        )
        print(f"[loop-engineering] Logged cron run: {context.get('job_name', '?')}", flush=True)
    except Exception as e:
        print(f"[loop-engineering] Failed to log cron: {e}", flush=True)


def handle_session_start(context: dict) -> None:
    """Load state file of active profile."""
    try:
        state = profile_state.read_state(PROFILE)
        n_verdicts = state.count("| PASS |") + state.count("| FAIL |") + state.count("| WARN |")
        n_runs = state.count("## Run History")
        print(f"[loop-engineering] Session start | profile: {PROFILE} | verdicts: {n_verdicts} | runs: {n_runs}", flush=True)
    except Exception as e:
        print(f"[loop-engineering] Failed to load state: {e}", flush=True)
