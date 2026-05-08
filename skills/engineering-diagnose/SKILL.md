---
name: diagnose
description: Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says "diagnose this" / "debug this", reports a bug, says something is broken/throwing/failing, or describes a performance regression.
---

# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring the codebase, use the project's domain glossary to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a fast, deterministic, agent-runnable pass/fail signal for the bug, you will find the cause — bisection, hypothesis-testing, and instrumentation all just consume that signal. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one — try them in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Iterate on the loop itself

Treat the loop as a product. Once you have _a_ loop, ask:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

Do not proceed to Phase 2 until you have a loop you believe in.

## Phase 2 — Reproduce

Run the loop. Watch the bug appear.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

Do not proceed until you reproduce the bug.

## Phase 3 — Hypothesise

Generate **3–5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix + regression test

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling) hand off to the `/improve-codebase-architecture` skill with the specifics. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.

## Examples

### Example: Diagnosing a Flask API crash

**Symptom**: POST /api/checkout returns 500 on production but not locally.

**Phase 1 — Build feedback loop**:
```python
# Replay the exact request that failed
import requests
resp = requests.post('http://localhost:5000/api/checkout', json={
  "cart_id": "abc123",
  "payment_method": "card",
  "amount": 99000
})
print(resp.status_code, resp.json())
```
Loop works: reproduces 500 locally.

**Phase 2 — Reproduce**: Run the loop. Error: `KeyError: 'user_id'` in `checkout.py:47`.

**Phase 3 — Hypothesise**:
1. If `cart_id` not found in DB → should return 404 not 500 (rank #1)
2. If `user_id` missing from cart object → null reference at line 47 (rank #2)
3. If race condition in DB → intermittent, not 100% (rank #3)

**Phase 4 — Instrument**: Add log at line 47: `logger.debug(f"[DEBUG-a4f2] cart object: {cart}")`. Rerun. Output shows `cart` has no `user_id` key.

**Phase 5 — Fix**: The cart lookup returns a partial object when cart exists but user_id not populated. Add null check: `cart.get('user_id')` instead of `cart['user_id']`. Write regression test.

**Phase 6 — Cleanup**: Remove `[DEBUG-a4f2]` logs. Commit with message: "Fix: KeyError in checkout when cart.user_id not populated — add .get() with fallback".

### Example: Performance regression in list query

**Symptom**: `/api/orders` takes 8s, was <1s last week.

**Phase 1 — Build feedback loop**:
```python
import time, requests
for _ in range(3):
    start = time.time()
    resp = requests.get('http://localhost:5000/api/orders?limit=100')
    print(f"{time.time()-start:.2f}s — {resp.status_code}")
```
Baseline: 0.9s. Production: 8s.

**Phase 3 — Hypothesise**:
1. If missing database index on `orders.user_id` → full table scan (rank #1)
2. If N+1 query problem → orders × items = many queries (rank #2)
3. If new serializer slowness → JSON overhead (rank #3)

**Phase 4 — Instrument**: Run `EXPLAIN QUERY PLAN` on the orders query. Output shows `SCAN TABLE orders` — no index used.

**Phase 5 — Fix**: Add index: `CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)`. Re-run loop: 0.95s.

### Common Pitfalls

1. **Skip Phase 1 (no loop)** — debugging without a feedback loop is guessing.
2. **Fix before understanding** — "obvious" fixes often miss the real cause.
3. **Change multiple variables** — instrument one thing at a time.
4. **Forget to clean debug logs** — `[DEBUG-xxx]` tags left behind pollute production logs.
5. **Skip regression test** — the bug WILL come back without a test.
