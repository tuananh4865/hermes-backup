#!/opt/homebrew/bin/python3.14
"""
Proactive Research Cron — Daily autonomous research on top interest areas
Runs BEFORE daily digest to enrich wiki with proactive findings

Cron: 0 7 * * * cd ~/wiki && python3 scripts/proactive_research_cron.py >> logs/proactive_research.log 2>&1
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
FRONTBOOT_FILE = WIKI_ROOT / "_meta" / "frontboot.json"
STATE_DIR = Path.home() / ".hermes" / "cron"
PROACTIVE_STATE = STATE_DIR / "proactive_research.json"

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

def get_frontboot() -> Dict:
    if FRONTBOOT_FILE.exists():
        return json.loads(FRONTBOOT_FILE.read_text())
    return {"proactive_research": {"enabled": True, "topics": []}}

def load_state() -> Dict:
    if PROACTIVE_STATE.exists():
        return json.loads(PROACTIVE_STATE.read_text())
    return {"last_run": None, "findings": [], "topics_researched": []}

def save_state(state: Dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    PROACTIVE_STATE.write_text(json.dumps(state, indent=2))

def get_top_interest_topics() -> List[str]:
    """Get top topics from interest signal tracker."""
    signals_file = WIKI_ROOT / "scripts" / ".interest_signals.json"
    if not signals_file.exists():
        return []

    try:
        signals = json.loads(signals_file.read_text())
    except Exception:
        return []

    topic_freq = signals.get("topic_frequency", {})
    if not topic_freq:
        return []

    # Boost certain topics based on frontboot config
    fb = get_frontboot()
    boost = fb.get("interest_boost", {})

    scored = []
    for topic, freq in topic_freq.items():
        boost_val = boost.get(topic.lower(), 1)
        score = min(freq * 5, 40) + (boost_val * 5)
        scored.append((topic, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [t[0] for t in scored[:5]]

def research_topic(topic: str) -> Optional[Dict]:
    """Run a quick research on a topic using ddgs via python3.14."""
    import tempfile, stat
    search_code = f"""
from ddgs import DDGS
import json, sys
results = []
q = "{topic} 2026 latest"
try:
    with DDGS() as d:
        r = list(d.text(q, max_results=3))
        for item in r:
            results.append({{
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "content": item.get("body", "")[:200]
            }})
except Exception as e:
    sys.stderr.write(str(e))
    sys.exit(1)
print(json.dumps(results))
"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(search_code)
        script_path = f.name
        os.chmod(script_path, stat.S_IRWXU)
        result = subprocess.run(
            ["python3.14", script_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
    finally:
        try:
            os.unlink(script_path)
        except Exception:
            pass

    try:
        findings = json.loads(result.stdout.strip()) if result.stdout.strip() else []
        if findings:
            return {"topic": topic, "status": "success", "findings": findings[:3]}
    except Exception:
        pass
    return {"topic": topic, "status": "no_results", "findings": []}

def main():
    log("=== Proactive Research Cron Started ===")

    state = load_state()
    fb = get_frontboot()

    # Check if enabled
    proactive_config = fb.get("proactive_research", {})
    if not proactive_config.get("enabled", True):
        log("Proactive research disabled in frontboot.json")
        return

    # Get topics to research
    # Priority: frontboot topics FIRST, then interest signals as supplement
    configured_topics = proactive_config.get("topics", [])
    interest_topics = get_top_interest_topics()

    # Frontboot topics get priority (take up to 5)
    frontboot_slice = configured_topics[:5]
    # Fill remaining slots from interest signals (avoiding duplicates)
    existing = set(t.lower() for t in frontboot_slice)
    supplement = [t for t in interest_topics if t.lower() not in existing][:5 - len(frontboot_slice)]
    all_topics = frontboot_slice + supplement

    if not all_topics:
        log("No topics to research")
        return

    log(f"Researching {len(all_topics)} topics: {all_topics}")

    findings = []
    for topic in all_topics:
        result = research_topic(topic)
        if result and result.get("status") == "success":
            findings.append(result)
            log(f"  [success] {topic}: {len(result.get('findings', []))} findings")
        else:
            log(f"  [{result.get('status', 'error')}] {topic}")

    # Update state
    state["last_run"] = datetime.now().isoformat()
    state["findings"] = findings[-10:]
    state["topics_researched"] = all_topics
    save_state(state)

    log(f"=== Proactive Research Complete: {len(findings)} topics with results ===")

if __name__ == "__main__":
    main()
