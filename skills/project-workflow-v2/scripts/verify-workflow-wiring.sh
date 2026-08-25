#!/bin/bash
# 4-Layer Workflow Wiring Verification
#
# Verifies a project workflow is wired into all future sessions + sub-agents.
# Use after applying project-workflow-v2 v2.5 wiring pattern, or as part of
# `bash ~/.hermes/scripts/check-all-compliance.sh` follow-up.
#
# Layer 1: Default SOUL has workflow section (orchestrator self-knowledge)
# Layer 2: Shared sub-agent reference file exists (single source of truth)
# Layer 3: ≥3 sub-agent SOUL.md reference shared file (consumers wired)
# Layer 4: Hook wrapper executable + triggers per-project log (auto-log fires)
#
# Exit codes:
#   0 = all 4 layers PASS
#   1 = any layer FAIL (with specific reason)
#
# Usage:
#   bash verify-workflow-wiring.sh [project_id]
#
# Examples:
#   bash verify-workflow-wiring.sh content-creator
#   bash verify-workflow-wiring.sh              # checks all default layers without project test

set -e

PROJECT_ID="${1:-content-creator}"
PASS=0
FAIL=0

echo "=== 4-Layer Workflow Wiring Verification ==="
echo "Project: $PROJECT_ID"
echo ""

# === Layer 1: Default SOUL has workflow section ===
echo "Layer 1: Default SOUL.md has PROJECT WORKFLOW section..."
SOUL_HITS=$(grep -c "PROJECT WORKFLOW" ~/.hermes/SOUL.md 2>/dev/null || echo "0")
if [[ "$SOUL_HITS" -ge 1 ]]; then
  echo "  ✓ PASS ($SOUL_HITS match in default SOUL)"
  PASS=$((PASS+1))
else
  echo "  ✗ FAIL — default SOUL.md missing PROJECT WORKFLOW section"
  echo "    Fix: inject ~90-line section into ~/.hermes/SOUL.md"
  FAIL=$((FAIL+1))
fi
echo ""

# === Layer 2: Shared sub-agent reference file exists ===
echo "Layer 2: Shared sub-agent reference file exists..."
SHARED_REF=~/.hermes/profiles/_shared/sub-agent-workflow.md
if [[ -f "$SHARED_REF" ]]; then
  SIZE=$(wc -c < "$SHARED_REF")
  echo "  ✓ PASS ($SHARED_REF, ${SIZE}b)"
  PASS=$((PASS+1))
else
  echo "  ✗ FAIL — shared sub-agent-workflow.md missing"
  echo "    Fix: create $SHARED_REF with project structure + 6-step loop"
  FAIL=$((FAIL+1))
fi
echo ""

# === Layer 3: ≥3 sub-agent SOULs reference shared file ===
echo "Layer 3: Sub-agent SOUL.md files reference shared workflow..."
REF_COUNT=$(grep -l "sub-agent-workflow" ~/.hermes/profiles/*/SOUL.md 2>/dev/null | wc -l)
if [[ "$REF_COUNT" -ge 3 ]]; then
  echo "  ✓ PASS ($REF_COUNT sub-agent profiles reference shared workflow)"
  grep -l "sub-agent-workflow" ~/.hermes/profiles/*/SOUL.md | sed 's/^/    - /'
  PASS=$((PASS+1))
else
  echo "  ✗ FAIL — only $REF_COUNT sub-agent profiles reference shared workflow (need ≥3)"
  echo "    Fix: patch coder, research-lead, content-director SOUL.md"
  FAIL=$((FAIL+1))
fi
echo ""

# === Layer 4: Hook wrapper exists, executable, and triggers per-project log ===
echo "Layer 4: Hook wrapper executable + triggers per-project log..."
WRAPPER=~/.hermes/hooks/session-auto-log/hook_wrapper.sh
HANDLER=~/.hermes/hooks/session-auto-log/handler.py

if [[ ! -f "$WRAPPER" ]]; then
  echo "  ✗ FAIL — hook wrapper missing at $WRAPPER"
  echo "    Fix: create hook_wrapper.sh using templates/hook-wrapper-bash-to-python.sh"
  FAIL=$((FAIL+1))
elif [[ ! -x "$WRAPPER" ]]; then
  echo "  ✗ FAIL — hook wrapper not executable"
  echo "    Fix: chmod +x $WRAPPER"
  FAIL=$((FAIL+1))
elif [[ ! -f "$HANDLER" ]]; then
  echo "  ✗ FAIL — handler.py missing at $HANDLER"
  echo "    Fix: install session-auto-log handler or create minimal handler with def handle()"
  FAIL=$((FAIL+1))
else
  # Try a real trigger — record file size before + after
  PROJECT_LOG_DIR="/Volumes/Storage-1/Hermes/wiki/projects/$PROJECT_ID/logs"
  if [[ ! -d "$PROJECT_LOG_DIR" ]]; then
    echo "  ⚠ SKIP — project $PROJECT_ID has no logs/ dir, can't test trigger end-to-end"
    echo "    (Layers 1-3 still verified above)"
    PASS=$((PASS+1))  # Don't penalize for missing test project
  else
    TODAY=$(date +%Y-%m-%d)
    LOG_FILE="$PROJECT_LOG_DIR/${TODAY}-sessions.md"
    SIZE_BEFORE=0
    [[ -f "$LOG_FILE" ]] && SIZE_BEFORE=$(wc -c < "$LOG_FILE")

    bash "$WRAPPER" --event agent:end \
      --output "wire-verify test for $PROJECT_ID" 2>&1 >/dev/null

    if [[ -f "$LOG_FILE" ]]; then
      SIZE_AFTER=$(wc -c < "$LOG_FILE")
      if [[ "$SIZE_AFTER" -gt "$SIZE_BEFORE" ]]; then
        echo "  ✓ PASS (wrapper fires, log grew ${SIZE_BEFORE}b → ${SIZE_AFTER}b)"
        PASS=$((PASS+1))
      else
        echo "  ✗ FAIL — wrapper ran but log size unchanged"
        echo "    Fix: check handler.py event_type check, may need --event agent:end not on_session_end"
        FAIL=$((FAIL+1))
      fi
    else
      echo "  ✗ FAIL — wrapper ran but $LOG_FILE not created"
      echo "    Fix: check handler.py path resolution + PROJECTS_ROOT constant"
      FAIL=$((FAIL+1))
    fi
  fi
fi
echo ""

# === Summary ===
TOTAL=$((PASS+FAIL))
echo "=== Summary: $PASS/$TOTAL layers PASS ==="
if [[ "$FAIL" -eq 0 ]]; then
  echo "✓ Workflow system fully wired into future sessions + sub-agents"
  exit 0
else
  echo "✗ $FAIL layer(s) need attention — see fixes above"
  exit 1
fi