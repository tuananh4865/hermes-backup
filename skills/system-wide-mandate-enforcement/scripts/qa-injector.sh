#!/bin/bash
# qa-injector.sh — 3-tier QA for idempotent scripts
# Usage: bash qa-injector.sh <path-to-injector.sh> [test args]
#
# Tests:
#   Tier 1: Fresh file → expect content ADDED
#   Tier 2: Re-run on modified file → expect SKIP (idempotent)
#   Tier 3: Partial content edge case → expect content ADDED
#
# Exits 0 on all-pass, 1 on any failure.

set -e
INJECTOR="${1:?Usage: qa-injector.sh <injector> [args]}"
TESTDIR=$(mktemp -d)
trap "rm -rf $TESTDIR" EXIT

PASS=0
FAIL=0

check() {
  local name="$1" actual="$2" expected="$3"
  if [ "$actual" = "$expected" ]; then
    echo "  ✅ $name: $actual"
    PASS=$((PASS+1))
  else
    echo "  ❌ $name: got '$actual', expected '$expected'"
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
if [ "$LAFTER" -gt "$LBEFORE" ]; then
  check "tier1_content_added" "added" "added"
else
  check "tier1_content_added" "not_added" "added"
fi

# Tier 2: Re-run on modified file
echo "=== Tier 2: Re-run on modified ==="
LBEFORE=$(wc -l < "$TESTFILE")
bash "$INJECTOR" "$TESTFILE" >/dev/null 2>&1 || true
LAFTER=$(wc -l < "$TESTFILE")
if [ "$LAFTER" -eq "$LBEFORE" ]; then
  check "tier2_idempotent" "stable" "stable"
else
  check "tier2_idempotent" "re-injected" "stable"
fi

# Tier 3: Edge case (partial content)
echo "=== Tier 3: Partial content edge case ==="
TESTFILE="$TESTDIR/partial.md"
echo "## Identity section mentioning target keyword" > "$TESTFILE"
LBEFORE=$(wc -l < "$TESTFILE")
bash "$INJECTOR" "$TESTFILE" >/dev/null 2>&1 || true
LAFTER=$(wc -l < "$TESTFILE")
if [ "$LAFTER" -gt "$LBEFORE" ]; then
  check "tier3_partial_robust" "added" "added"
else
  check "tier3_partial_robust" "not_added" "added"
fi

echo ""
echo "=========================="
echo "PASS: $PASS  FAIL: $FAIL"
if [ "$FAIL" -eq 0 ]; then
  echo "✅ SCRIPT IS TRULY IDEMPOTENT"
  exit 0
else
  echo "❌ SCRIPT HAS BUGS — review the failing tier above"
  exit 1
fi
