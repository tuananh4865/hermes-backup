#!/bin/bash
# Spawn an agent in a tmux pane
# BẮT BUỘC: Pre-spawn check trước khi tạo pane
# Usage: spawn-pane.sh <agent-type> <workspace> "<role>" "<task>" "<acceptance-criteria>"
# Example: spawn-pane.sh "claude-code" "~/wiki" "researcher" "Research AI trends" "1. Cover X 2. Cover Y 3. File saved"

set -e

AGENT_TYPE="$1"
WORKSPACE="$2"
ROLE="$3"
TASK="$4"
ACCEPTANCE="$5"

if [ -z "$AGENT_TYPE" ] || [ -z "$WORKSPACE" ] || [ -z "$ROLE" ] || [ -z "$TASK" ]; then
    echo "Usage: spawn-pane.sh <type> <workspace> <role> <task> [acceptance-criteria]"
    echo ""
    echo "Types: claude-code, gemini, hermes, codex, opencode"
    echo "Roles: pm, designer, researcher, architect, coder, reviewer, tester, docs-writer"
    exit 1
fi

# Default acceptance if not provided
if [ -z "$ACCEPTANCE" ]; then
    ACCEPTANCE="1. Task completed as described 2. No errors 3. Code is functional"
fi

# ============================================================================
# PRE-SPAWN CHECK - BẮT BUỘC
# ============================================================================
echo "=== Pre-Spawn Terminal Check ==="

# 1. Check if in tmux
if [ -z "$TMUX" ]; then
    echo "[WARN] Not in tmux session"
    IN_TMUX=false
else
    echo "[OK] In tmux session: $TMUX"
    IN_TMUX=true
    CURRENT_SESSION="$TMUX"
fi

# 2. Check parent process (are we inside an AI agent?)
INSIDE_AGENT=false
PARENT_PID=$$
while [ $PARENT_PID -ne 1 ]; do
    PARENT_PID=$(ps -p $PARENT_PID -o ppid= 2>/dev/null | tr -d ' ')
    if [ -z "$PARENT_PID" ] || [ "$PARENT_PID" = "1" ]; then
        break
    fi
    PARENT_NAME=$(ps -p $PARENT_PID -o comm= 2>/dev/null)
    if echo "$PARENT_NAME" | grep -qiE "hermes|claude|gemini|codex|agent" 2>/dev/null; then
        echo "[WARN] Parent is AI agent: $PARENT_NAME (PID: $PARENT_PID)"
        INSIDE_AGENT=true
        break
    fi
done

if [ "$INSIDE_AGENT" = false ]; then
    echo "[OK] Not inside AI agent runtime"
fi

# 3. Decision: Where to spawn?
if [ "$IN_TMUX" = true ] && [ "$INSIDE_AGENT" = false ]; then
    # Safe: we're in tmux and not inside an AI agent - user can see
    SPAWN_SESSION=$(echo "$TMUX" | cut -d',' -f1)
    echo ""
    echo "=== DECISION: Spawn directly in current tmux session ==="
    echo "Session: $SPAWN_SESSION"
elif [ "$IN_TMUX" = true ] && [ "$INSIDE_AGENT" = true ]; then
    # We're inside an AI agent running in tmux - MUST create new session
    SPAWN_SESSION="orchestrator-$$"
    tmux new-session -d -s "${SPAWN_SESSION}" -c "${WORKSPACE}"
    echo ""
    echo "=== DECISION: Create NEW session for user visibility ==="
    echo "Session: $SPAWN_SESSION"
    echo ">>> User: Open Terminal and run: tmux attach -t ${SPAWN_SESSION}"
    echo ""
elif [ "$IN_TMUX" = false ]; then
    # Not in tmux at all - create new session
    SPAWN_SESSION="orchestrator-$$"
    tmux new-session -d -s "${SPAWN_SESSION}" -c "${WORKSPACE}"
    echo ""
    echo "=== DECISION: Create NEW tmux session ==="
    echo "Session: $SPAWN_SESSION"
    echo ">>> User: tmux attach -t ${SPAWN_SESSION}"
    echo ""
else
    # Fallback
    SPAWN_SESSION="orchestrator-$$"
    tmux new-session -d -s "${SPAWN_SESSION}" -c "${WORKSPACE}"
    echo ""
    echo "=== DECISION: Fallback - create NEW session ==="
    echo "Session: $SPAWN_SESSION"
fi

echo "Spawning into session: $SPAWN_SESSION"
echo ""

# ============================================================================
# DETERMINE AGENT COMMAND
# ============================================================================
case "$AGENT_TYPE" in
    claude-code) AGENT_CMD="claude"; INIT_WAIT=6 ;;
    gemini) AGENT_CMD="gemini"; INIT_WAIT=4 ;;
    hermes) AGENT_CMD="hermes-agent"; INIT_WAIT=3 ;;
    codex) AGENT_CMD="codex"; INIT_WAIT=3 ;;
    opencode) AGENT_CMD="opencode"; INIT_WAIT=3 ;;
    *) echo "Unknown agent type: $AGENT_TYPE" && exit 1 ;;
esac

# ============================================================================
# SPAWN AGENT
# ============================================================================
echo "=== Spawning $AGENT_TYPE Agent ==="
echo "Role: $ROLE"
echo "Workspace: $WORKSPACE"
echo ""

# Step 1: Split current pane horizontally
echo "[1/7] Creating split pane..."
tmux split-window -h -t "${SPAWN_SESSION}:0"

NEW_PANE_INDEX=$(tmux list-panes -t "${SPAWN_SESSION}:0" -F '#{pane_index}' | tail -1)
echo "      Pane created: $NEW_PANE_INDEX"

# Step 2: Start the agent
echo "[2/7] Starting agent: $AGENT_CMD"
tmux send-keys -t "${SPAWN_SESSION}:${NEW_PANE_INDEX}" "cd $WORKSPACE && $AGENT_CMD" Enter

# Step 3: Wait for agent to initialize
echo "[3/7] Waiting for agent to initialize (${INIT_WAIT}s)..."
sleep $INIT_WAIT

# Step 4: Set role
echo "[4/7] Assigning role: $ROLE"
tmux send-keys -t "${SPAWN_SESSION}:${NEW_PANE_INDEX}" "You are the **$ROLE** agent on this team." Enter

# Step 5: Send task with acceptance criteria
echo "[5/7] Sending task with acceptance criteria..."
TASK_MSG="[AGENT TASK]
Task: $TASK

Acceptance Criteria (MUST satisfy ALL):
$ACCEPTANCE

Context: Working directory is $WORKSPACE"

tmux send-keys -t "${SPAWN_SESSION}:${NEW_PANE_INDEX}" "$TASK_MSG" Enter

# Step 6: VERIFY instruction
echo "[6/7] Adding verification instruction..."
VERIFY_MSG="IMPORTANT - VERIFY before reporting done:
1. Verify EACH acceptance criterion is met
2. Include EVIDENCE in your report (file paths, test output, etc)
3. Do NOT claim done until you have verified

Report format:
[REPORT] Task: $TASK | Status: done/issue/need-help | Evidence: <what you verified>"

tmux send-keys -t "${SPAWN_SESSION}:${NEW_PANE_INDEX}" "$VERIFY_MSG" Enter

# Step 7: Final instruction
echo "[7/7] Final instructions..."
FINAL_MSG="Report back to Orchestrator (Hermes) when:
- Task complete (with VERIFIED evidence)
- Found a problem (describe clearly)
- Need a decision (ask explicitly)
- Stuck for more than 2 minutes

Do NOT make up answers. If unsure, ask."
tmux send-keys -t "${SPAWN_SESSION}:${NEW_PANE_INDEX}" "$FINAL_MSG" Enter

echo ""
echo "=== Agent Spawned ==="
echo "Session: $SPAWN_SESSION"
echo "Pane: ${SPAWN_SESSION}:${NEW_PANE_INDEX}"
echo "Role: $ROLE"
echo "Agent: $AGENT_CMD"
echo ""
echo "Monitor this pane:"
echo "  tmux capture-pane -p -t ${SPAWN_SESSION}:${NEW_PANE_INDEX}"
echo ""
echo "Switch between panes:"
echo "  Ctrl+b q (shows pane numbers) → press number"
echo "  Ctrl+b o (next pane)"
echo ""
echo "Cleanup when done:"
echo "  tmux kill-pane -t ${SPAWN_SESSION}:${NEW_PANE_INDEX}"
