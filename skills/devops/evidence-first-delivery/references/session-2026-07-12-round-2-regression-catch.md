# Session 2026-07-12 — Round 2 Verifier Caught Agent's Own Regression

> Companion to `session-2026-07-12-four-case-validation.md`. Documents the 5th verifier case: catching a regression introduced by the AUTHOR's own fix attempt.

## What happened

After SOUL.md 3-fix batch applied (Karpathy #1 conflict → state-assumption; 4 outdated paths cleaned; 🎯 consolidated to 1 line per task), author dispatched a **round 2 verifier** to confirm.

**Verifier verdict:** `PARTIAL_PASS` (2/3 fix pass, 1 partial).

## What the verifier caught

The author's "4 outdated paths cleaned" fix had **missed one**:

- ✅ Line 215: `universal-verify/SKILL.md` reference → removed
- ✅ Line 216: `wiki/concepts/universal-verify-protocol-...` reference → marked TODO
- ✅ Line 192 example: `Hermes-Edit/clip_0704_V5_troncau.mp4` → generic `/path/to/output/clip.mp4`
- ✅ Line 323: `restart_gateway.sh` → `restart-hermes-gateway.sh`
- ❌ **MISSED at line 319**: still referenced `~/.hermes/restart_gateway.sh` (the old broken path)

The duplicate reference was easy to miss because line 323 had been patched correctly — author assumed "the gateway section is fixed" without scanning the OTHER table row that mentioned the same script.

## Outcome

Author patched line 319 → `~/.hermes/restart-gateway-telegram-fix.sh` (verified file exists on disk via `ls -la`). Final grep confirmed 0 stale gateway script references.

## Why this matters (the durable lesson)

**The verifier caught a regression introduced by the AUTHOR's own fix attempt.** Without round 2 verify:

- SOUL.md would have shipped with one stale reference intact
- The "cleanup outdated paths" fix would have been only 75% effective (3/4, not 4/4)
- User would eventually hit the stale path, lose trust in "verified" claims

This validates the **always-run-r2** rule: **first round verifies claims, second round verifies the fix**.

## Apply rule (general)

After any **non-trivial fix batch on a system prompt or policy file** (SOUL.md, SKILL.md, agent-rules.yaml, etc.), ALWAYS dispatch a round 2 verifier subagent with the original 5-dim audit prompt (or its equivalent for that file type).

**Single-round verify is insufficient when:**

- Fix touches multiple paths/sections (easy to miss a duplicate)
- Fix involves renaming/relocating references (typo-prone)
- Fix changes structure, not just content (regression surface > 1)
- Author has time pressure (skim-mode = miss mode)

**Round 2 prompt template (adapt from the original 5-dim audit):**

```
You are INDEPENDENT ADVERSARIAL VERIFIER. Verify the FIX (not the original claim).
- Run diff [backup] [current] | head -100
- For each claimed fix, run grep to confirm it landed
- For each claimed fix, ALSO check nearby lines for the same pattern (catch duplicates)
- Verdict: PASS (all fixes landed + no regressions) / FAIL (any fix missing OR new issue)
```

## Cost-benefit

- Round 2 cost: ~30-60 seconds (single subagent, focused diff + grep prompt)
- Cost of shipping with stale fix: 5-30 min user-debug time + 1 trust hit
- ROI: round 2 is essentially free if there's any chance of regression

## Cross-reference

- `references/session-2026-07-12-four-case-validation.md` — original 4-case validation
- `references/adversarial-subagent-2026-07-12.md` — base prompt template + 5 self-questions
- SKILL.md § "Round 2 verifier pattern" — short inline mention