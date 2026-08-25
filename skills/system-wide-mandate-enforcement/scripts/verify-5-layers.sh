#!/bin/bash
# 5-Layer System-Wide Mandate Verification
# Usage: bash verify-5-layers.sh [mandate-name]
# Example: bash verify-5-layers.sh fable5
#
# Verifies the FULL 5-layer matrix for a system-wide mandate:
# 1. SOUL.md coverage
# 2. Cron job prompts
# 3. Hook registration
# 4. Shared reference file
# 5. Compliance scripts
#
# Returns exit 0 if all 5 layers PASS, exit 1 if any layer FAILS.
# Prints numbered report with evidence (per self-verify-after-workaround recipe).

set -e

HERMES_ROOT="${HERMES_HOME:-$HOME/.hermes}"
MANDATE="${1:-fable5}"  # Default to fable5; pass another name for different mandate

# Marker string used in cron job prompts to detect mandate presence
CRON_MARKER="${MANDATE^^} MANDATE"  # uppercase for case-insensitive match

# Compliance script names (try common patterns)
COMPLIANCE_SCRIPT="$HERMES_ROOT/scripts/check-${MANDATE}-compliance.sh"
INJECTOR_SCRIPT="$HERMES_ROOT/scripts/add-${MANDATE}-to-soul.sh"
HOOK_DIR="$HERMES_ROOT/hooks/${MANDATE}-compliance-check"
HOOK_HANDLER="$HOOK_DIR/handler.py"
HOOK_LOG="$HERMES_ROOT/logs/gateway.log"
SHARED_REF="$HERMES_ROOT/profiles/_shared/${MANDATE}-patterns.md"

PASS=0
FAIL=0
TOTAL=5

print_result() {
  local num="$1"
  local layer="$2"
  local status="$3"
  local evidence="$4"
  if [ "$status" = "PASS" ]; then
    echo "[$num/5] ✅ PASS  $layer"
    PASS=$((PASS+1))
  else
    echo "[$num/5] ❌ FAIL  $layer"
    FAIL=$((FAIL+1))
  fi
  if [ -n "$evidence" ]; then
    echo "         Evidence: $evidence"
  fi
}

echo "=" * 70
echo "🔍 5-LAYER SYSTEM-WIDE MANDATE VERIFICATION: $MANDATE"
echo "=" * 70
echo ""

# Layer 1: SOUL.md coverage
echo "[1/5] Checking SOUL.md coverage..."
SOUL_TOTAL=0
SOUL_PASS=0
SOUL_EVIDENCE=""
for soul in $(find "$HERMES_ROOT" -name "SOUL.md" -not -path "*/docker/*" 2>/dev/null); do
  SOUL_TOTAL=$((SOUL_TOTAL+1))
  # Check 4 standard patterns (customize per mandate)
  HAS_ALL=true
  for pattern in "MCP CONNECTOR" "PERSISTENT STORAGE" "SKILLS-FIRST" "SEARCH DISCIPLINE"; do
    if ! grep -q "$pattern" "$soul" 2>/dev/null; then
      HAS_ALL=false
      break
    fi
  done
  if $HAS_ALL; then
    SOUL_PASS=$((SOUL_PASS+1))
  else
    SOUL_EVIDENCE="$SOUL_EVIDENCE$soul missing patterns; "
  fi
done
if [ "$SOUL_PASS" -eq "$SOUL_TOTAL" ] && [ "$SOUL_TOTAL" -gt 0 ]; then
  print_result 1 "SOUL.md coverage" "PASS" "$SOUL_PASS/$SOUL_TOTAL files have all patterns"
else
  print_result 1 "SOUL.md coverage" "FAIL" "$SOUL_PASS/$SOUL_TOTAL files compliant. Failures: $SOUL_EVIDENCE"
fi
echo ""

# Layer 2: Cron job prompts
echo "[2/5] Checking cron job prompts..."
if [ -f "$HERMES_ROOT/cron/jobs.json" ]; then
  LLM_JOBS=$(python3 -c "
import json
data = json.load(open('$HERMES_ROOT/cron/jobs.json'))
llm = [j for j in data.get('jobs', []) if not j.get('no_agent') and j.get('prompt')]
print(len(llm))
")
  JOBS_WITH_MARKER=$(python3 -c "
import json
data = json.load(open('$HERMES_ROOT/cron/jobs.json'))
count = 0
for j in data.get('jobs', []):
  if j.get('no_agent') or not j.get('prompt'):
    continue
  if '$CRON_MARKER' in j['prompt'].upper():
    count += 1
print(count)
")
  if [ "$JOBS_WITH_MARKER" -eq "$LLM_JOBS" ] && [ "$LLM_JOBS" -gt 0 ]; then
    print_result 2 "Cron job prompts" "PASS" "$JOBS_WITH_MARKER/$LLM_JOBS LLM jobs have '$CRON_MARKER'"
  else
    print_result 2 "Cron job prompts" "FAIL" "$JOBS_WITH_MARKER/$LLM_JOBS LLM jobs have '$CRON_MARKER'. Run inject-cron-mandate.sh."
  fi
else
  print_result 2 "Cron job prompts" "FAIL" "jobs.json not found"
fi
echo ""

# Layer 3: Hook registration
echo "[3/5] Checking hook registration..."
if [ -f "$HOOK_HANDLER" ]; then
  if grep -q "def handle" "$HOOK_HANDLER"; then
    # Check gateway log
    if [ -f "$HOOK_LOG" ]; then
      HOOK_STATUS=$(tail -100 "$HOOK_LOG" | grep -E "Loaded|Skipping.*${MANDATE}-compliance-check" | tail -1)
      if echo "$HOOK_STATUS" | grep -q "Loaded"; then
        print_result 3 "Hook registration" "PASS" "def handle() present, gateway log: Loaded"
      elif echo "$HOOK_STATUS" | grep -q "Skipping"; then
        print_result 3 "Hook registration" "FAIL" "def handle() present BUT gateway log: Skipping. Check discovery contract."
      else
        print_result 3 "Hook registration" "FAIL" "def handle() present BUT no gateway log line found. Gateway may need reload."
      fi
    else
      print_result 3 "Hook registration" "FAIL" "def handle() present but no gateway.log to verify discovery"
    fi
  else
    print_result 3 "Hook registration" "FAIL" "$HOOK_HANDLER missing 'def handle' function. Rename from main() to handle()."
  fi
else
  print_result 3 "Hook registration" "FAIL" "$HOOK_HANDLER not found"
fi
echo ""

# Layer 4: Shared reference file
echo "[4/5] Checking shared reference file..."
if [ -f "$SHARED_REF" ]; then
  SIZE=$(stat -f "%z" "$SHARED_REF" 2>/dev/null || stat -c "%s" "$SHARED_REF" 2>/dev/null)
  if [ "$SIZE" -gt 1000 ]; then
    print_result 4 "Shared reference file" "PASS" "$SHARED_REF exists, ${SIZE}b"
  else
    print_result 4 "Shared reference file" "FAIL" "$SHARED_REF exists but only ${SIZE}b (expected >1KB)"
  fi
else
  # Try alternate naming
  ALT_REF="$HERMES_ROOT/profiles/_shared/${MANDATE}.md"
  if [ -f "$ALT_REF" ]; then
    SIZE=$(stat -f "%z" "$ALT_REF" 2>/dev/null || stat -c "%s" "$ALT_REF" 2>/dev/null)
    print_result 4 "Shared reference file" "PASS" "$ALT_REF exists (alternate name), ${SIZE}b"
  else
    print_result 4 "Shared reference file" "FAIL" "Neither $SHARED_REF nor $ALT_REF found"
  fi
fi
echo ""

# Layer 5: Compliance scripts
echo "[5/5] Checking compliance scripts..."
SCRIPTS_OK=true
SCRIPT_EVIDENCE=""
if [ ! -x "$COMPLIANCE_SCRIPT" ]; then
  SCRIPTS_OK=false
  SCRIPT_EVIDENCE="$COMPLIANCE_SCRIPT not executable or missing; "
fi
if [ ! -x "$INJECTOR_SCRIPT" ]; then
  SCRIPTS_OK=false
  SCRIPT_EVIDENCE="$SCRIPT_EVIDENCE$INJECTOR_SCRIPT not executable or missing"
fi
if $SCRIPTS_OK; then
  print_result 5 "Compliance scripts" "PASS" "Both $COMPLIANCE_SCRIPT and $INJECTOR_SCRIPT are executable"
else
  print_result 5 "Compliance scripts" "FAIL" "$SCRIPT_EVIDENCE"
fi
echo ""

# Summary
echo "=" * 70
echo "📊 SUMMARY: $PASS/$TOTAL layers PASS"
echo "=" * 70
if [ "$FAIL" -eq 0 ]; then
  echo "✅ Mandate '$MANDATE' is 100% applied system-wide"
  exit 0
else
  echo "❌ Mandate '$MANDATE' is partial: $FAIL layer(s) need attention"
  echo "   Re-run after fixing the failed layers."
  exit 1
fi
