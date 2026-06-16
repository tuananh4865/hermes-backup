#!/usr/bin/env bash
# loop-goal test suite
# Run: ./test.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🧪 /goal Loop Runner — Test Suite"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

PASS=0
FAIL=0

# Test 1: Condition parser passes
echo "Test 1: Condition parser — all unit tests pass"
if python3 condition-parser.py > /dev/null 2>&1; then
    echo "  ✅ PASS"
    ((PASS++))
else
    echo "  ❌ FAIL"
    ((FAIL++))
fi

# Test 2: Condition parser CLI — PASS verdict
echo "Test 2: CLI check — PASS verdict, condition matches"
if python3 condition-parser.py --check PASS 9.3 --condition "checker_verdict == 'PASS' and checker_score >= 9.0" > /dev/null 2>&1; then
    echo "  ✅ PASS (exit 0)"
    ((PASS++))
else
    echo "  ❌ FAIL"
    ((FAIL++))
fi

# Test 3: Condition parser CLI — FAIL verdict
echo "Test 3: CLI check — FAIL verdict, condition does not match"
if ! python3 condition-parser.py --check FAIL 7.5 --condition "checker_score >= 9.0" > /dev/null 2>&1; then
    echo "  ✅ PASS (exit 1 as expected)"
    ((PASS++))
else
    echo "  ❌ FAIL (should have exit 1)"
    ((FAIL++))
fi

# Test 4: Loop runner — succeeds within max_runs
echo "Test 4: Loop runner — achieves PASS within max_runs"
if ./run.sh "Test goal" --condition "checker_score >= 9.0" --max-runs 5 --profile test-profile-runner-$$ > /dev/null 2>&1; then
    echo "  ✅ PASS (loop achieved condition)"
    ((PASS++))
else
    echo "  ❌ FAIL (loop did not achieve condition)"
    ((FAIL++))
fi

# Test 5: Loop runner — exceeds max_runs
echo "Test 5: Loop runner — exceeds max_runs when impossible condition"
if ! ./run.sh "Impossible goal" --condition "checker_score >= 99.0" --max-runs 2 --profile test-profile-runner-impossible-$$ > /dev/null 2>&1; then
    echo "  ✅ PASS (correctly failed when impossible)"
    ((PASS++))
else
    echo "  ❌ FAIL (should have failed)"
    ((FAIL++))
fi

# Test 6: State file is created
echo "Test 6: State file written to worker dir"
STATE_DIR="$HOME/.hermes/profiles/test-profile-runner-$$"
if [[ -d "$STATE_DIR" ]]; then
    echo "  ✅ PASS (state dir: $STATE_DIR)"
    ((PASS++))
else
    echo "  ❌ FAIL"
    ((FAIL++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Results: $PASS passed, $FAIL failed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ $FAIL -eq 0 ]]; then
    exit 0
else
    exit 1
fi
