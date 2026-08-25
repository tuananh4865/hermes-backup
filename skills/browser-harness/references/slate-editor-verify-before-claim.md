---
title: React Slate editor — verify before claiming "generated"
created: 2026-07-14
type: reference
parent_skill: browser-harness
tags: [react-slate, contenteditable, insert_text, verification, before-after-diff, fake-success, js-click, evidence-first-delivery, tRPC]
confidence: high
relationships: [browser-harness, evidence-first-delivery, cua-driver-page-tool-for-real-chrome, adversarial-subagent-verifier]
---

# React Slate editor — verify before claiming "generated" (2026-07-14)

> **Context:** Session "Learn Google Flow" day 2. Anh Tuấn Anh asked em to click "Tạo" button to generate test image. Em successfully: set prompt via `cua-driver page insert_text`, verified button enabled (bg white), clicked via JS `.click()`, waited 36s. Em then reported "✅ 10 ảnh mới được generate" — TWICE. Anh pushed back: *"Anh thấy em chưa gửi prompt đi mà"* (anh caught it first time), then *"Em vẫn chưa tạo được bất cứ hình ảnh mới nào, làm lại"* (anh caught it second time). Root cause: em used `image count delta` as proof of generation, without diffing unique media IDs.

## Why this skill section exists

**The recurring failure pattern (3rd time in same project):**

| Time | What em did | What em reported | Actual state |
|------|-------------|------------------|--------------|
| 1st | Set prompt + click + saw `images: 41` (was 15) | "✅ 10 ảnh mới được tạo" | Stale generation from earlier queued submit |
| 2nd | Set prompt + click + saw "26%" and "36%" progress | "✅ Generation đang chạy" | Progress UI was for stale queued job, NOT em's submit |
| 3rd (after anh pushback) | Snapshot unique media IDs before/after | "❌ NO NEW IDs, 0 TRPC calls" | Em had been reporting success on stale data |

**Lesson:** When the user can see your work (e.g. image generation in their own browser), `image count delta` is NOT proof. Only `unique ID diff before/after` proves the action came from YOUR submit.

## The 3 forms of false "success" on Slate editors

### Form 1: Image count delta ≠ MY submit

**Symptom:** `document.querySelectorAll("img").length` increases after click → "đã generate N ảnh".

**Reality:** Count delta could be from:
1. A queued old prompt from a previous click (cached submission by user)
2. Background generation triggered by app-side state change (e.g. user navigated away and back)
3. The submit used a partially-stale prompt (React state + DOM text both stale)
4. Lazy-loaded images that were already in DOM but not rendered

**Fix:** Diff unique IDs, not counts. Save `before_ids` set → click → save `after_ids` set → compute `new_ids = after - before`.

### Form 2: Progress % UI indicators ≠ MY submit

**Symptom:** See "26%", "36%", "Generating...", or progress bar after click → "generation đang chạy".

**Reality:**
1. Progress may be from a STALE queued job (queued by user's earlier manual click, not by you)
2. Progress may be CLIENT-SIDE estimate (React component animating numbers, no backend hit)
3. Progress may NEVER complete — backend may have already failed but UI hasn't updated yet

**Fix:** Intercept `window.fetch` calls and confirm a POST to `/trpc/...generate...` (or equivalent backend endpoint) was made within 5-10s of your click. Zero fetches = zero generation.

### Form 3: JS `.click()` returned "clicked" ≠ API call fired

**Symptom:** `btn.click()` returned `"clicked"`, no exception → "đã click Tạo thành công".

**Reality:** Click event dispatched, but React's synthetic event handler may have:
1. Used stale state (React state at click time ≠ state at insert_text time)
2. Failed silently in the handler (try/catch swallowed error)
3. Hit a guard that prevented API call (e.g. prompt contains banned words, credits exhausted)

**Fix:** After click, check for:
- Network activity (window.fetch interception)
- Error toast/banner in DOM (`document.body.innerText.includes("lỗi") || ...`)
- State changes in UI (loading indicator, button text changes to "Đang tạo...")
- Server response (check for new media ID within 10s)

## The 4-step verification recipe (MANDATORY before any "generated" claim)

### Step 1: Snapshot unique media IDs BEFORE

```python
import json, subprocess

def snapshot_media_ids(pid, wid):
    """Capture all media UUIDs visible in DOM (attributes + innerHTML)."""
    js = '''(function() {
        const urls = new Set();
        document.querySelectorAll("*").forEach(el => {
            for (const attr of el.attributes) {
                if (attr.value?.includes("getMediaUrlRedirect")) {
                    const m = attr.value.match(/name=([a-f0-9-]+)/);
                    if (m) urls.add(m[1]);
                }
            }
        });
        const html = document.body.innerHTML;
        const matches = html.match(/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/g) || [];
        matches.forEach(id => urls.add(id));
        return JSON.stringify([...urls]);
    })()'''
    payload = {"pid": pid, "window_id": wid, "action": "execute_javascript", "javascript": js}
    result = subprocess.run(['/Users/tuananh4865/.local/bin/cua-driver', 'call', 'page'],
        input=json.dumps(payload), capture_output=True, text=True, timeout=15)
    return set(json.loads(result.stdout.strip()))

before_ids = snapshot_media_ids(PID, WID)
print(f"📸 BEFORE: {len(before_ids)} unique media IDs")
# Save to file for cross-check
import json as json_mod
with open('/tmp/before_ids.json', 'w') as f:
    json_mod.dump(list(before_ids), f)
```

### Step 2: Set prompt + click submit (the actual work)

```python
# Focus prompt input
subprocess.run(['/Users/tuananh4865/.local/bin/cua-driver', 'call', 'page'],
    input=json.dumps({"pid": PID, "window_id": WID, "action": "execute_javascript",
                       "javascript": 'document.querySelector("[contenteditable=true]")?.focus(); "focused"'}),
    capture_output=True, text=True, timeout=15)

# Insert prompt via CDP Input.insertText (the only method that syncs Slate state)
subprocess.run(['/Users/tuananh4865/.local/bin/cua-driver', 'call', 'page'],
    input=json.dumps({"pid": PID, "window_id": WID, "action": "insert_text",
                       "text": "Your full prompt here"}),
    capture_output=True, text=True, timeout=30)

# Click submit button
result = subprocess.run(['/Users/tuananh4865/.local/bin/cua-driver', 'call', 'page'],
    input=json.dumps({"pid": PID, "window_id": WID, "action": "execute_javascript",
                       "javascript": '(function(){const b=Array.from(document.querySelectorAll("button")).find(x=>(x.innerText||"").includes("arrow_forward"));if(b)b.click();})()'}),
    capture_output=True, text=True, timeout=15)
```

### Step 3: Intercept network activity (proves backend was called)

```python
# Install fetch interceptor BEFORE click if possible, or right after
js_install = '''
window.__trpcCalls = [];
const origFetch = window.fetch;
window.fetch = function(...args) {
    const url = typeof args[0] === 'string' ? args[0] : args[0].url;
    if (url.includes('trpc') || url.includes('generate')) {
        window.__trpcCalls.push({url, method: args[1]?.method || "GET", time: Date.now()});
    }
    return origFetch.apply(this, args);
};
"installed"
'''

# Wait for generation (15-30s)
import time
time.sleep(15)

# Check captured tRPC calls
js_check = '''
(function() {
    const calls = window.__trpcCalls || [];
    return JSON.stringify({
        count: calls.length,
        samples: calls.slice(-5).map(c => c.url.slice(0, 120))
    });
})()
'''
result = subprocess.run(['/Users/tuananh4865/.local/bin/cua-driver', 'call', 'page'],
    input=json.dumps({"pid": PID, "window_id": WID, "action": "execute_javascript", "javascript": js_check}),
    capture_output=True, text=True, timeout=15)
trpc_data = json.loads(result.stdout.strip())
print(f"📡 TRPC calls captured: {trpc_data['count']}")
```

### Step 4: Snapshot unique media IDs AFTER + diff

```python
import json as json_mod
time.sleep(5)  # extra buffer for image to render
after_ids = snapshot_media_ids(PID, WID)
print(f"📸 AFTER: {len(after_ids)} unique media IDs")

with open('/tmp/before_ids.json') as f:
    before_ids = set(json_mod.load(f))

new_ids = after_ids - before_ids
print(f"🆕 NEW IDs from MY submit: {len(new_ids)}")
if new_ids:
    for nid in list(new_ids)[:10]:
        print(f"   + {nid}")
else:
    print("   ❌ NO NEW IDs - my submit did NOT trigger generation")
```

### Decision rule

```python
if trpc_data['count'] == 0:
    print("❌ FAIL: No backend call was made. Submit did not fire API.")
elif len(new_ids) == 0:
    print("❌ FAIL: Backend was called but no new media IDs appeared.")
    print("    Possible: queued stale job, prompt ignored, credits exhausted")
elif len(new_ids) > 0:
    print(f"✅ PASS: {len(new_ids)} new IDs confirmed from my submit")
```

## Anti-patterns (DON'T)

| Anti-pattern | Why it fails |
|--------------|--------------|
| Report "generated N images" based on count delta only | Stale queued jobs + lazy-loaded images inflate the count |
| Report "generation đang chạy" based on progress % UI | Progress may be from stale queued job, or client-side estimate |
| Trust JS `.click()` returning "clicked" without network check | React synthetic event handler may fail silently |
| Skip the BEFORE snapshot | Can't compute diff without it; agent overwrites state |
| Wait < 15s for "completion" | AI generation typically takes 10-30s; 36s is not too long |

## Workflow summary

```
[1] Snapshot BEFORE media IDs → save to /tmp/before_ids.json
[2] Install fetch interceptor (optional but recommended)
[3] Set prompt via cua-driver page insert_text
[4] Verify button enabled (bg = rgb(255,255,255), not gray)
[5] Click submit via JS .click()
[6] Wait 15-30s
[7] Check tRPC call count (must be > 0)
[8] Snapshot AFTER media IDs → diff with BEFORE
[9] Only report "generated N" if new_ids > 0 AND trpc_calls > 0
[10] If either fails, report honestly: "submit fired but no new content generated"
```

## Pitfall — Click via JS may use stale React state

**Symptom:** After `insert_text`, prompt is visible in DOM. After `JS .click()`, button click event fires. But backend still uses an old/empty prompt.

**Possible cause:** React's onClick handler reads state via `useState` hook. If React state was set by `insert_text` but a later state update (e.g. from `blur` event, or from a separate `dispatchEvent`) overwrites it to empty, the click handler sees empty state.

**Workaround:** Re-set the prompt IMMEDIATELY before click, and add a small delay:

```python
# Right before click, re-verify state
verify_js = '''
(function() {
    const ce = document.querySelector("[contenteditable=true]");
    const btn = Array.from(document.querySelectorAll("button")).find(b => (b.innerText || "").includes("arrow_forward"));
    return JSON.stringify({
        promptText: ce?.innerText,
        promptLength: ce?.innerText?.length,
        btnBg: btn ? getComputedStyle(btn).backgroundColor : "no btn",
        btnDisabled: btn?.disabled
    });
})()
'''
# Run, verify promptLength > 0 AND btnBg = "rgb(255, 255, 255)"
# If good, click within 1s
```

If state desync keeps happening → escalate to `computer_use` for real cursor + keyboard simulation (this is the only truly synchronous path).

## Google Flow carousel layout (added 2026-07-24)

The verify-before-claim recipe was first written assuming vertical scroll. **As of 2026-07-24, Google Flow's project editor uses HORIZONTAL CAROUSEL layout, not vertical scroll.**

Symptoms that scream "this is a horizontal carousel":
- `document.body.scrollHeight === document.body.clientHeight` (no vertical scroll possible)
- Multiple media items at the same `y` coordinate but increasing `x` (e.g. `x=80, 574, 1069, 1569, 2058`)
- Items positioned via CSS `transform: matrix(...)` rather than scroll position
- "Scroll xuống tìm X" instruction from user = scroll the carousel right, NOT scroll page down

To enumerate ALL items in a Flow project carousel:

```python
js = '''
(function() {
    const carousel = Array.from(document.querySelectorAll("*")).find(el => {
        const cs = getComputedStyle(el);
        return (cs.overflowX === "auto" || cs.overflowX === "scroll") && el.scrollWidth > el.clientWidth + 100;
    });
    if (!carousel) return JSON.stringify({error: "no horizontal carousel found"});
    const items = Array.from(carousel.children).map((child, i) => {
        const r = child.getBoundingClientRect();
        return {
            index: i,
            x: Math.round(r.x), y: Math.round(r.y),
            w: Math.round(r.width), h: Math.round(r.height),
            visible: r.x < window.innerWidth && r.x + r.width > 0
        };
    });
    return JSON.stringify({count: items.length, items});
})()
'''
```

For Flow projects where you can't see all items in one viewport, use the Chrome tab list (`curl http://localhost:9222/json`) — the tab title often IS the project name (e.g. "Google Flow - YouTube" = the project named "YouTube").

## Related skills / files

- `browser-harness/SKILL.md` § "NEW (2026-07-13) — Image count delta ≠ Generation triggered from MY prompt" — sibling pitfall (image count delta)
- `browser-harness/SKILL.md` § "NEW (2026-07-13) — Better fallback when computer_use fails: cua-driver call page" — cua-driver recipe
- `references/cua-driver-page-tool-for-real-chrome.md` § "Pitfall — React Slate editor + button enabled state" — Slate editor diagnosis
- `evidence-first-delivery/SKILL.md` § "5 documented fail cases" — case #6 (this case) added
- `multi-agent-orchestrator` — orchestrator rule "không tin agent claims, verify trước khi mark complete"

## Lessons for future sessions

1. **Always diff before claiming generation/creation/upload.** Save `before_state`, do the action, save `after_state`, compute diff. Numbers like counts can lie; unique IDs can't.
2. **Never trust progress UI.** It's client-side estimate. Confirm with backend traffic.
3. **JS `.click()` is necessary but not sufficient.** Always confirm with a network call or a state change that the handler fired.
4. **Anh's escalation pattern (3 times in same project):** 1st catch is "are you sure?" (verification), 2nd catch is "this is wrong, redo" (correction), 3rd catch is "stop saying success when it's not" (trust repair). After 3rd catch, MUST do the actual before/after verification or admit failure.