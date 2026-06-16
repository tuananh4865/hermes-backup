# Idempotent Script QA Protocol — Bugs, Fixes, Templates

> **Date:** 2026-06-16
> **Source:** Real bugs caught during fable5-injector verification (Fable-5 mandate session)
> **Use this reference when:** writing/auditing any script that modifies files (injector, refactor, batch, sync)

## Why this exists

Tuấn Anh's QA mindset caught em "claiming done quá sớm" 2 lần trong 1 session. The compliance gate showed PASS, but the actual injector had 2 latent bugs that would have caused double-injection on every re-run. This reference documents those bugs and the 3-tier QA protocol that catches them.

## The 2 real bugs

### Bug #1: Section name mismatch → false-positive skip detection

**Scenario:** Injector uses `grep "FABLE-5 PATTERNS"` to detect if section already exists. But the main SOUL.md uses different wording: "🆕 PATTERNS ADAPTED FROM CLAUDE FABLE 5".

**Symptom:** Re-run on main SOUL.md → re-injects → 419 → 457 lines (38 lines added that shouldn't have been).

**Root cause:** Keyword-only check is too permissive. A more robust check requires BOTH:
1. Section name matches (e.g. `FABLE-5 PATTERNS` exact case)
2. Shared-ref link is present (e.g. `fable5-patterns.md`)

**Fix:**
```bash
# BAD — keyword only
if grep -q "FABLE-5" "$file"; then SKIP; fi

# GOOD — keyword AND structural element
if grep -q "FABLE-5 PATTERNS" "$file" && grep -q "fable5-patterns.md" "$file"; then SKIP; fi
```

### Bug #2: Case-insensitive grep matches partial content → false-positive re-inject

**Scenario:** Fresh file has "Fable-5" mentioned in an "Identity" section, but no actual Fable-5 section. Injector's case-insensitive grep matches → re-injects.

**Symptom:** First run injects 27 lines. Second run injects ANOTHER 38 lines (because the file now has 27 lines of new content with the right keyword, but `grep -i` still matches).

**Root cause:** `grep -i "Fable-5"` matches anywhere, even in unrelated sections. Need case-sensitive grep for the EXACT section name AND check that the section is in the right place (e.g. near the end, not buried in Identity).

**Fix:**
```bash
# BAD — case-insensitive
grep -qi "fable-5" "$file"

# GOOD — case-sensitive exact match
grep -q "FABLE-5 PATTERNS" "$file"
```

## The 3-Tier QA Protocol

**Every idempotent script MUST pass these 3 tiers before being declared "done":**

| Tier | Input | Expected output | Catches |
|------|-------|-----------------|---------|
| **Tier 1: Fresh file** | Empty file or file WITHOUT target content | Injector ADDS content (1+ lines added) | Happy path broken? |
| **Tier 2: Re-run on modified file** | File with target content already | Injector SKIPS (0 lines added) | Idempotency broken (Bug #1, #2) |
| **Tier 3: Edge case (partial content)** | File with PARTIAL content (e.g. only 1 of 2 markers) | Injector ADDS the missing parts | Robustness broken |

**Why 3 tiers:** Tier 1 alone misses idempotency bugs. Tier 2 alone misses fresh-file bugs. Tier 3 catches both happy-path AND idempotency in the same test.

## 8-Point QA Checklist (for "system-wide mandate applied" reports)

**Use this checklist before writing "DONE" to Tuấn Anh:**

| # | Check | Evidence format | Example |
|---|-------|-----------------|---------|
| 1 | List of files updated | Full path + line count before/after | `~/.hermes/SOUL.md: 419→457 lines` |
| 2 | File mtime | `YYYY-MM-DD HH:MM` | `mtime: 2026-06-16 18:48` |
| 3 | File size | Bytes | `5,506 bytes` |
| 4 | Compliance check | Exit code + output | `bash check-X.sh; echo $? → 0` |
| 5 | Hook test | Exit code + WARN-only | `bash handler.py; echo $? → 0` |
| 6 | Idempotent script QA | All 3 tiers PASS | Tier 1: 0→27, Tier 2: 27→27, Tier 3: 1→28 |
| 7 | MD5 (for binaries/originals) | `md5sum file` | `md5: abc123...` |
| 8 | Diff (for refactors) | `-X +Y` | `git diff --stat` |

**Self-audit:** If you can't fill in 7/8 of these, you're "claiming done quá sớm".

## Idempotent script QA template

```bash
#!/bin/bash
# qa-injector.sh — 3-tier QA for idempotent scripts
# Usage: bash qa-injector.sh <path-to-injector.sh> [test args]
set -e
INJECTOR="${1:?Usage: qa-injector.sh <injector> [args]}"
TESTDIR=$(mktemp -d)
trap "rm -rf $TESTDIR" EXIT

PASS=0
FAIL=0

check() {
  local name="$1" actual="$2" expected="$3"
  if [ "$actual" = "$expected" ]; then
    echo "✅ $name: $actual"
    PASS=$((PASS+1))
  else
    echo "❌ $name: got $actual, expected $expected"
    FAIL=$((FAIL+1))
  fi
}

# Tier 1: Fresh file
echo "=== Tier 1: Fresh file ==="
TESTFILE="$TESTDIR/fresh.md"
echo "" > "$TESTFILE"
LBEFORE=$(wc -l < "$TESTFILE")
bash "$INJECTOR" "$TESTFILE" >/dev/null 2>&1 || true
LAFTER=$(wc -l < "$TESTFILE")
[ "$LAFTER" -gt "$LBEFORE" ] && check "tier1_content_added" "added" "added" || check "tier1_content_added" "not_added" "added"

# Tier 2: Re-run on modified file
echo "=== Tier 2: Re-run on modified ==="
LBEFORE=$(wc -l < "$TESTFILE")
bash "$INJECTOR" "$TESTFILE" >/dev/null 2>&1 || true
LAFTER=$(wc -l < "$TESTFILE")
[ "$LAFTER" -eq "$LBEFORE" ] && check "tier2_idempotent" "stable" "stable" || check "tier2_idempotent" "re-injected" "stable"

# Tier 3: Edge case
echo "=== Tier 3: Partial content edge case ==="
TESTFILE="$TESTDIR/partial.md"
echo "## Section mentioning target keyword but no actual section" > "$TESTFILE"
LBEFORE=$(wc -l < "$TESTFILE")
bash "$INJECTOR" "$TESTFILE" >/dev/null 2>&1 || true
LAFTER=$(wc -l < "$TESTFILE")
[ "$LAFTER" -gt "$LBEFORE" ] && check "tier3_partial_robust" "added" "added" || check "tier3_partial_robust" "not_added" "added"

echo ""
echo "=========================="
echo "PASS: $PASS  FAIL: $FAIL"
[ "$FAIL" -eq 0 ] && echo "✅ SCRIPT IS TRULY IDEMPOTENT" && exit 0 || (echo "❌ SCRIPT HAS BUGS" && exit 1)
```

## How to use this reference

1. **Before writing a new idempotent script** — read this reference, understand the 2 bug types
2. **After writing the script** — run the 3-tier QA template above
3. **If QA fails** — debug with `bash -x injector.sh testfile` to see where re-inject happens
4. **Before reporting "DONE"** — fill out 8-point QA checklist, attach evidence

## Real example: fable5-injector bugs

**Injector:** `~/.hermes/scripts/add-fable5-to-soul.sh`
**Date:** 2026-06-16

**Bug #1 fix:**
```diff
- if grep -q "FABLE-5 PATTERNS" "$SOUL_FILE"; then
+ if grep -q "FABLE-5 PATTERNS" "$SOUL_FILE" && grep -q "fable5-patterns.md" "$SOUL_FILE"; then
```

**Bug #2 fix:**
```diff
- if grep -qi "Fable-5" "$SOUL_FILE"; then
+ if grep -q "FABLE-5 PATTERNS" "$SOUL_FILE"; then
```

**QA after fix:**
- Tier 1: Fresh file → 0 → 27 lines ✅
- Tier 2: Re-run → 27 → 27 lines ✅
- Tier 3: Partial file → 1 → 28 lines ✅

## Anti-patterns to avoid

| Anti-pattern | Why bad | Fix |
|--------------|---------|-----|
| `grep -i` for section detection | Matches anywhere, false positives | Use case-sensitive grep for exact section name |
| Keyword-only check | Permissive, misses structural changes | Add structural checks (link presence, section position) |
| No 3-tier test | "It worked once" ≠ idempotent | Always run fresh + re-run + edge case |
| "Done" without evidence | Tuấn Anh catches this in QA | Always attach mtime, size, exit code |
| Claiming "perfect score" | Conceals caveats | Honest report: "37/40, 2 caveats noted" |

## Related
- `templates/injector-script.sh` — base template that needs 3-tier QA
- `templates/ci-gate-script.sh` — CI gate template
- SKILL.md Step 8 (Idempotent Script QA Protocol)
- SKILL.md Step 9 (Evidence-Based Reporting Template)
