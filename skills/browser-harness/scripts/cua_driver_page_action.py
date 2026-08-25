#!/usr/bin/env python3
"""
cua_driver_page_action.py — Safe wrapper for cua-driver page tool.

Eliminates the 5 most common pitfalls when driving user's real Chrome:
1. JSON escaping hell (use Python json.dumps, not inline bash)
2. Wrong action spelling (Slate inserts via insert_text, NOT execute_javascript)
3. Pixel click on Slate-disabled button (use JS .click() instead)
4. Trusting tool return value (poll + verify state actually changed)
5. Prompt-in-DOM ≠ generation triggered — verify prompt was the one submitted
   (lesson learned 2026-07-13: em báo success khi chưa click thật)

Usage:
    from cua_driver_page_action import (
        page_execute_js, page_insert_text, page_click_button,
        find_chrome_window, poll_for_change, verify_generation,
        get_button_state, get_media_count
    )

    chrome = find_chrome_window(title_contains="Google Flow")
    pid, wid = chrome["pid"], chrome["window_id"]

    # Focus + insert via Slate-safe method
    page_execute_js(pid, wid, 'document.querySelector("[contenteditable=true]")?.focus()')
    page_insert_text(pid, wid, "Your prompt here (>= 90 chars)")

    # Verify button ENABLED before clicking (bg should be white, not gray)
    state = get_button_state(pid, wid, "Tạo")
    if not state.get("isEnabled"):
        print("Button still disabled — Slate state not synced, retry insert_text")
        sys.exit(1)

    # Click via JS .click() to bypass React pointer-events on submit button
    result = page_click_button(pid, wid, "Tạo")

    # Poll for generation result (45s timeout, 5s intervals)
    before = get_media_count(pid, wid)
    new_state = poll_for_change(pid, wid, before, timeout=45)
    if not new_state:
        print("Generation timeout — verify prompt was actually submitted")
        # CRITICAL: verify prompt is still in DOM and matches what we set
        check = verify_generation_triggered(pid, wid, expected_prompt)
        print(f"Prompt verification: {check}")

CLI mode:
    cua_driver_page_action.py find-window "Google Flow"
    cua_driver_page_action.py exec 85715 3489 'JSON.stringify({url: location.href})'
    cua_driver_page_action.py insert 85715 3489 "Your text"
    cua_driver_page_action.py click-btn 85715 3489 "Tạo"
"""

import json
import subprocess
import sys
import time
import re
from typing import Optional, Dict, Any, List


CUA_DRIVER = "/Users/tuananh4865/.local/bin/cua-driver"


def _call_cua(payload: Dict[str, Any], timeout: int = 30) -> str:
    """Call cua-driver with JSON payload. Returns stdout."""
    try:
        result = subprocess.run(
            [CUA_DRIVER, "call", "page"],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            print(f"[cua_driver_page_action] non-zero exit: {result.stderr[:200]}", file=sys.stderr)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"[cua_driver_page_action] timeout after {timeout}s", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"[cua_driver_page_action] error: {e}", file=sys.stderr)
        return ""


def page_execute_js(pid: int, window_id: int, javascript: str) -> str:
    """Run JavaScript in user's real Chrome via cua-driver page tool.

    Returns stdout from JS. Use this for DOM queries, state checks,
    and .click() calls that need to bypass React pointer-events.
    """
    return _call_cua({
        "pid": pid,
        "window_id": window_id,
        "action": "execute_javascript",
        "javascript": javascript,
    })


def page_insert_text(pid: int, window_id: int, text: str) -> str:
    """Insert text via CDP Input.insertText. Works on Slate.js editors.

    THIS IS THE ONLY METHOD that syncs Slate.js internal state model.
    Methods that FAIL on Slate (verified 2026-07-13):
    - ce.innerText = ... + InputEvent
    - document.execCommand('insertText')
    - type_keystrokes (may crash React app)
    - Enter/Cmd+Enter hotkey

    Tip: prompt length >= 90 chars usually needed for button enable.
    """
    return _call_cua({
        "pid": pid,
        "window_id": window_id,
        "action": "insert_text",
        "text": text,
    })


def page_click_element(pid: int, window_id: int, css_selector: str) -> str:
    """Click element by CSS selector with cursor animation.

    Prefer page_click_button() for submit buttons — bypasses React
    pointer-events: none issue.
    """
    return _call_cua({
        "pid": pid,
        "window_id": window_id,
        "action": "click_element",
        "selector": css_selector,
    })


def page_click_button(pid: int, window_id: int, button_text: str) -> str:
    """Click button by innerText match. Uses JS .click() to bypass
    React aria-disabled / pointer-events on submit buttons.

    ALWAYS call get_button_state() first to verify enabled.
    """
    js = f'''
    (function() {{
        const btn = Array.from(document.querySelectorAll("button")).find(b =>
            (b.innerText || "").includes({json.dumps(button_text)}));
        if (!btn) return "no btn";
        if (btn.disabled) return "still disabled";
        btn.click();
        return "clicked";
    }})()
    '''
    return page_execute_js(pid, window_id, js)


def page_query_dom(pid: int, window_id: int, css_selector: str,
                   attributes: Optional[List[str]] = None) -> str:
    """Find elements by CSS selector. Returns JSON array."""
    payload = {
        "pid": pid,
        "window_id": window_id,
        "action": "query_dom",
        "css_selector": css_selector,
    }
    if attributes:
        payload["attributes"] = attributes
    return _call_cua(payload)


def find_chrome_window(title_contains: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Find Chrome window via cua-driver get_accessibility_tree.

    Returns dict with pid, window_id, title. None if not found.
    Skips menu bar (those are AXApplication "Chrome" without window_id).
    """
    try:
        result = subprocess.run(
            [CUA_DRIVER, "get_accessibility_tree"],
            capture_output=True, text=True, timeout=15,
        )
        windows = []
        # Find all window blocks — match window_id + title + pid triplet
        # Skip menu bar windows (no window_id or "AXMenuBar" title)
        for match in re.finditer(
            r'"window_id":\s*(\d+),\s*"title":\s*"([^"]+)"',
            result.stdout,
        ):
            wid, title = match.groups()
            if "AXMenuBar" in title or "Chrome" == title:
                continue
            # Get pid from context (look back ~200 chars)
            start = max(0, match.start() - 300)
            pid_match = re.search(r'"pid":\s*(\d+)', result.stdout[start:match.start()])
            pid = int(pid_match.group(1)) if pid_match else 0
            windows.append({
                "pid": pid,
                "window_id": int(wid),
                "title": title,
            })
        # Filter
        for w in windows:
            if title_contains and title_contains not in w["title"]:
                continue
            return w
        return None
    except Exception as e:
        print(f"[find_chrome_window] error: {e}", file=sys.stderr)
        return None


def get_button_state(pid: int, window_id: int, button_text: str) -> Dict[str, Any]:
    """Get submit button enabled state via background color check.

    White bg (rgb 255,255,255) = enabled
    Gray bg (rgba 218,220,224,0.05) = disabled (React/Slate state not synced)
    """
    js = f'''
    (function() {{
        const btn = Array.from(document.querySelectorAll("button")).find(b =>
            (b.innerText || "").includes({json.dumps(button_text)}));
        if (!btn) return JSON.stringify({{error: "no btn"}});
        const cs = getComputedStyle(btn);
        return JSON.stringify({{
            disabled: btn.disabled,
            bg: cs.backgroundColor,
            color: cs.color,
            opacity: cs.opacity,
            isEnabled: cs.backgroundColor.includes("255") && parseFloat(cs.opacity) > 0.5
        }});
    }})()
    '''
    raw = page_execute_js(pid, window_id, js)
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw, "parsed": False}


def get_media_count(pid: int, window_id: int) -> Dict[str, int]:
    """Count media elements (images + videos) + media URLs in DOM.

    mediaUrls counts getMediaUrlRedirect occurrences in innerHTML.
    uniqueMediaIds counts unique media IDs (useful to detect NEW media
    vs just re-rendered existing).
    """
    js = '''
    JSON.stringify({
        images: document.querySelectorAll("img").length,
        videos: document.querySelectorAll("video").length,
        mediaUrls: (document.body.innerHTML.match(/getMediaUrlRedirect/g) || []).length,
        uniqueMediaIds: new Set(
            (document.body.innerHTML.match(/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/g) || [])
        ).size
    })
    '''
    raw = page_execute_js(pid, window_id, js)
    try:
        return json.loads(raw)
    except Exception:
        return {"raw": raw}


def poll_for_change(pid: int, window_id: int,
                    before: Dict[str, int],
                    timeout: int = 45,
                    interval: int = 5) -> Optional[Dict[str, int]]:
    """Poll media count until it changes (generation completed).

    Returns new count dict if changed, None if timeout.

    Don't trust first poll — some apps show loading then render in chunks.
    Wait at least 30s for typical image gen, 60s+ for video.
    """
    start = time.time()
    iterations = max(1, timeout // interval)
    for i in range(iterations):
        time.sleep(interval)
        current = get_media_count(pid, window_id)
        changed = any(
            current.get(k, 0) > before.get(k, 0)
            for k in ["images", "videos", "mediaUrls", "uniqueMediaIds"]
        )
        elapsed = int(time.time() - start)
        print(f"[poll T+{elapsed}s] {current}")
        if changed:
            return current
    return None


def verify_generation_triggered(pid: int, window_id: int,
                                expected_prompt: str,
                                min_length: int = 30) -> Dict[str, Any]:
    """Verify the SUBMIT used OUR prompt (not a cached/old one).

    Catches the 2026-07-13 failure mode: em báo "thành công" sau khi thấy
    image count tăng, nhưng thật ra submit đã dùng prompt CŨ trong cache.

    Returns dict with: currentPrompt, expectedSubstr, matches, isCorrect
    """
    expected_substr = expected_prompt[:80]
    expected_strict = expected_prompt[:50]
    js = f'''
    (function() {{
        const ce = document.querySelector("[contenteditable=true]");
        const current = ce?.innerText || "";
        return JSON.stringify({{
            currentPrompt: current,
            expectedSubstr: {json.dumps(expected_substr)},
            promptLength: current.length,
            matches: current.includes({json.dumps(expected_strict)})
        }});
    }})()
    '''
    raw = page_execute_js(pid, window_id, js)
    try:
        data = json.loads(raw)
        data["isCorrect"] = (
            data.get("matches", False)
            and data.get("promptLength", 0) >= min_length
        )
        return data
    except Exception:
        return {"raw": raw, "parsed": False}


# CLI mode
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "find-window":
        title = sys.argv[2] if len(sys.argv) > 2 else None
        w = find_chrome_window(title_contains=title)
        print(json.dumps(w, indent=2, ensure_ascii=False))
    elif cmd == "exec":
        if len(sys.argv) < 5:
            print("Usage: exec <pid> <wid> <js>")
            sys.exit(1)
        pid, wid = int(sys.argv[2]), int(sys.argv[3])
        js = sys.argv[4]
        print(page_execute_js(pid, wid, js))
    elif cmd == "insert":
        if len(sys.argv) < 5:
            print("Usage: insert <pid> <wid> <text>")
            sys.exit(1)
        pid, wid = int(sys.argv[2]), int(sys.argv[3])
        text = sys.argv[4]
        print(page_insert_text(pid, wid, text))
    elif cmd == "click-btn":
        if len(sys.argv) < 5:
            print("Usage: click-btn <pid> <wid> <button_text>")
            sys.exit(1)
        pid, wid = int(sys.argv[2]), int(sys.argv[3])
        text = sys.argv[4]
        print(page_click_button(pid, wid, text))
    elif cmd == "btn-state":
        if len(sys.argv) < 5:
            print("Usage: btn-state <pid> <wid> <button_text>")
            sys.exit(1)
        pid, wid = int(sys.argv[2]), int(sys.argv[3])
        text = sys.argv[4]
        print(json.dumps(get_button_state(pid, wid, text), indent=2, ensure_ascii=False))
    elif cmd == "media-count":
        if len(sys.argv) < 4:
            print("Usage: media-count <pid> <wid>")
            sys.exit(1)
        pid, wid = int(sys.argv[2]), int(sys.argv[3])
        print(json.dumps(get_media_count(pid, wid), indent=2, ensure_ascii=False))
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: find-window, exec, insert, click-btn, btn-state, media-count")
        sys.exit(1)