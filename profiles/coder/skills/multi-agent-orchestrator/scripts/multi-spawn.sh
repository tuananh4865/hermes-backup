#!/bin/bash
# Spawn MULTIPLE agents in split panes
# BẮT BUỘC: Pre-spawn check trước khi spawn
# Usage: multi-spawn.sh <workspace> "<task>" <agent1:type:role> <agent2:type:role> ...
# Example: multi-spawn.sh "~/wiki" "Build e-commerce API" "claude-code:architect" "claude-code:coder" "claude-code:reviewer"

set -e

WORKSPACE="$1"
TASK="$2"
shift 2
AGENTS=("$@")

if [ -z "$WORKSPACE" ] || [ -z "$TASK" ] || [ ${#AGENTS[@]} -eq 0 ]; then
    echo "Usage: multi-spawn.sh <workspace> <task> <agent1:type:role> <agent2:type:role> ..."
    echo ""
    echo "Example:"
    echo '  multi-spawn.sh "~/wiki" "Research AI trends" "claude-code:researcher" "claude-code:coder"'
    exit 1
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

# 2. Check parent process
INSIDE_AGENT=false
PARENT_PID=$$
while [ $PARENT_PID -ne 1 ]; do
    PARENT_PID=$(ps -p $PARENT_PID -o ppid= 2>/dev/null | tr -d ' ')
    if [ -z "$PARENT_PID" ] || [ "$PARENT_PID" = "1" ]; then
        break
    fi
    PARENT_NAME=$(ps -p $PARENT_PID -o comm= 2>/dev/null)
    if echo "$PARENT_NAME" | grep -qiE "hermes|claude|gemini|codex|agent" 2>/dev/null; then
        echo "[WARN] Parent is AI agent: $PARENT_NAME"
        INSIDE_AGENT=true
        break
    fi
done

if [ "$INSIDE_AGENT" = false ]; then
    echo "[OK] Not inside AI agent runtime"
fi

# 3. Decision
if [ "$IN_TMUX" = true ] && [ "$INSIDE_AGENT" = false ]; then
    SESSION_NAME=$(echo "$TMUX" | cut -d',' -f1)
    echo ""
    echo "=== DECISION: Spawn directly in current tmux session ==="
elif [ "$IN_TMUX" = true ] && [ "$INSIDE_AGENT" = true ]; then
    SESSION_NAME="orchestrator-$$"
    tmux new-session -d -s "${SESSION_NAME}" -c "${WORKSPACE}"
    echo ""
    echo "=== DECISION: Create NEW session for user visibility ==="
    echo ">>> User: tmux attach -t ${SESSION_NAME}"
elif [ "$IN_TMUX" = false ]; then
    SESSION_NAME="orchestrator-$$"
    tmux new-session -d -s "${SESSION_NAME}" -c "${WORKSPACE}"
    echo ""
    echo "=== DECISION: Create NEW tmux session ==="
    echo ">>> User: tmux attach -t ${SESSION_NAME}"
else
    SESSION_NAME="orchestrator-$$"
    tmux new-session -d -s "${SESSION_NAME}" -c "${WORKSPACE}"
fi

echo "Will spawn agents into: $SESSION_NAME"
echo ""

# ============================================================================
# SPAWN AGENTS
# ============================================================================
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  MULTI-AGENT SPAWN                                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Workspace: $WORKSPACE"
echo "Task: $TASK"
echo "Agents: ${#AGENTS[@]}"
echo ""

PANE_NUM=1
for agent_spec in "${AGENTS[@]}"; do
    AGENT_TYPE="${agent_spec%%:*}"
    ROLE="${agent_spec##*:}"
    
    echo "[$PANE_NUM] Spawning $AGENT_TYPE as $ROLE..."
    
    case "$AGENT_TYPE" in
        claude-code) AGENT_CMD="claude"; INIT_WAIT=6 ;;
        gemini) AGENT_CMD="gemini"; INIT_WAIT=4 ;;
        hermes) AGENT_CMD="hermes-agent"; INIT_WAIT=3 ;;
        codex) AGENT_CMD="codex"; INIT_WAIT=3 ;;
        *) echo "Unknown agent type: $AGENT_TYPE"; continue ;;
    esac
    
    # Split pane
    tmux split-window -h -t "${SESSION_NAME}:0"
    
    # Get new pane index
    NEW_PANE=$(tmux list-panes -t "${SESSION_NAME}:0" -F '#{pane_index}' | tail -1)
    
    # Start agent
    tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "cd $WORKSPACE && $AGENT_CMD" Enter
    
    # Wait for init
    echo "      Waiting ${INIT_WAIT}s..."
    sleep $INIT_WAIT
    
    # Set role
    tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "You are the **$ROLE** agent on this team." Enter
    sleep 1
    
    # Set task
    tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Task: $TASK" Enter
    sleep 1
    
    # Role-specific
    case "$ROLE" in
        architect)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Design architecture, DB schema, API structure." Enter
            ;;
        researcher)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Research best practices, compare options." Enter
            ;;
        coder)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Implement code based on specifications." Enter
            ;;
        reviewer)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Review code for bugs, security, best practices." Enter
            ;;
        tester)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Write and run tests." Enter
            ;;
        designer)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Design UI/UX, wireframes, mockups." Enter
            ;;
    esac
    sleep 1
    
    # Verification instruction
    tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "IMPORTANT: Verify each criterion before reporting done.
[REPORT] Status: done/issue/need-help | Evidence: <what you verified>" Enter
    
    echo "      Spawned in pane $NEW_PANE"
    PANE_NUM=$((PANE_NUM + 1))
    
    if [ $PANE_NUM -ge 4 ]; then
        echo "Max 4 agents reached."
        break
    fi
done

echo ""
echo "=== Even layout ==="
tmux select-layout -t "${SESSION_NAME}:0" even-horizontal 2>/dev/null || true

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ALL AGENTS SPAWNED                                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Session: $SESSION_NAME"
echo "Agents: $((PANE_NUM - 1))"
echo ""
echo "VIEW: tmux attach -t ${SESSION_NAME}"
echo "CLEANUP: tmux kill-session -t ${SESSION_NAME}"
