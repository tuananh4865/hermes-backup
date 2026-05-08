#!/bin/bash
# Orchestrator workflow - orchestrate multi-agent task
# BẮT BUỘC: Pre-spawn check trước khi spawn
# Usage: orchestrate.sh <workspace> "<task-name>" "<task-description>" <agent1:type:role> <agent2:type:role> ...
# Example: orchestrate.sh "~/wiki" "Research" "Research AI agent trends" "claude-code:researcher" "claude-code:coder"

set -e

WORKSPACE="$1"
TASK_NAME="$2"
TASK_DESC="$3"
shift 3
AGENTS=("$@")

if [ -z "$WORKSPACE" ] || [ -z "$TASK_NAME" ] || [ -z "$TASK_DESC" ]; then
    echo "Usage: orchestrate.sh <workspace> <task-name> <task-desc> <agent1:type:role> ..."
    echo ""
    echo "Example:"
    echo '  orchestrate.sh "~/wiki" "Research" "Research AI trends" "claude-code:researcher" "claude-code:coder"'
    exit 1
fi

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  HERMES ORCHESTRATOR v4                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Task: $TASK_NAME"
echo "Description: $TASK_DESC"
echo "Workspace: $WORKSPACE"
echo "Agents: ${#AGENTS[@]}"
echo ""

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
        echo "[WARN] Parent is AI agent: $PARENT_NAME"
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
    SESSION_NAME=$(echo "$TMUX" | cut -d',' -f1)
    echo ""
    echo "=== DECISION: Spawn directly in current tmux session ==="
    echo "Session: $SESSION_NAME"
elif [ "$IN_TMUX" = true ] && [ "$INSIDE_AGENT" = true ]; then
    # We're inside an AI agent running in tmux - MUST create new session
    SESSION_NAME="orchestrator-$$"
    tmux new-session -d -s "${SESSION_NAME}" -c "${WORKSPACE}"
    echo ""
    echo "=== DECISION: Create NEW session for user visibility ==="
    echo "Session: $SESSION_NAME"
    echo ">>> User: Open Terminal and run: tmux attach -t ${SESSION_NAME}"
    echo ""
elif [ "$IN_TMUX" = false ]; then
    # Not in tmux at all - create new session
    SESSION_NAME="orchestrator-$$"
    tmux new-session -d -s "${SESSION_NAME}" -c "${WORKSPACE}"
    echo ""
    echo "=== DECISION: Create NEW tmux session ==="
    echo "Session: $SESSION_NAME"
    echo ">>> User: tmux attach -t ${SESSION_NAME}"
    echo ""
else
    # Fallback
    SESSION_NAME="orchestrator-$$"
    tmux new-session -d -s "${SESSION_NAME}" -c "${WORKSPACE}"
    echo ""
    echo "=== DECISION: Fallback - create NEW session ==="
    echo "Session: $SESSION_NAME"
fi

echo "Will spawn agents into: $SESSION_NAME"
echo ""

# ============================================================================
# SPAWN AGENTS
# ============================================================================
echo "=== Spawning Agents ==="
PANE_NUM=1

for agent_spec in "${AGENTS[@]}"; do
    AGENT_TYPE="${agent_spec%%:*}"
    ROLE="${agent_spec##*:}"
    
    echo ""
    echo "[$PANE_NUM] Spawning $AGENT_TYPE as $ROLE..."
    
    # Determine agent command and init time
    case "$AGENT_TYPE" in
        claude-code) AGENT_CMD="claude"; INIT_WAIT=6 ;;
        gemini) AGENT_CMD="gemini"; INIT_WAIT=4 ;;
        hermes) AGENT_CMD="hermes-agent"; INIT_WAIT=3 ;;
        codex) AGENT_CMD="codex"; INIT_WAIT=3 ;;
        opencode) AGENT_CMD="opencode"; INIT_WAIT=3 ;;
        *) echo "Unknown agent type: $AGENT_TYPE"; continue ;;
    esac
    
    # Split pane
    tmux split-window -h -t "${SESSION_NAME}:0"
    
    # Get new pane index
    NEW_PANE=$(tmux list-panes -t "${SESSION_NAME}:0" -F '#{pane_index}' | tail -1)
    
    # Start agent
    tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "cd $WORKSPACE && $AGENT_CMD" Enter
    
    # Wait for init
    echo "      Waiting ${INIT_WAIT}s for init..."
    sleep $INIT_WAIT
    
    # Set role
    tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "You are the **$ROLE** agent on this team." Enter
    sleep 1
    
    # Send task
    tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Main task: $TASK_NAME - $TASK_DESC" Enter
    sleep 1
    
    # Role-specific focus
    case "$ROLE" in
        architect)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Design the architecture, DB schema, API structure." Enter
            ;;
        researcher)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Research best practices, compare options, provide recommendations." Enter
            ;;
        coder)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Implement the code based on specifications." Enter
            ;;
        reviewer)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Review code for bugs, security, best practices." Enter
            ;;
        tester)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Write and run tests to validate functionality." Enter
            ;;
        designer)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Design UI/UX, create wireframes, mockups." Enter
            ;;
        pm)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Project management, timeline, coordination." Enter
            ;;
        docs-writer)
            tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "Your focus: Write documentation for the project." Enter
            ;;
    esac
    sleep 1
    
    # Verification instruction
    tmux send-keys -t "${SESSION_NAME}:${NEW_PANE}" "IMPORTANT: Verify each criterion before reporting done. Include evidence.
[REPORT] Task: $TASK_NAME | Status: done/issue/need-help | Evidence: <what you verified>" Enter
    
    echo "      Spawned in pane $NEW_PANE"
    PANE_NUM=$((PANE_NUM + 1))
    
    # Max 4 agents
    if [ $PANE_NUM -ge 4 ]; then
        echo "Max 4 agents reached."
        break
    fi
done

echo ""
echo "=== Distributing panes evenly ==="
tmux select-layout -t "${SESSION_NAME}:0" even-horizontal 2>/dev/null || true

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  AGENTS RUNNING                                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Session: $SESSION_NAME"
echo "Agents spawned: $((PANE_NUM - 1))"
echo ""
echo "To VIEW (Anh nhìn thấy agents):"
echo "  tmux attach -t ${SESSION_NAME}"
echo ""
echo "To MONITOR a specific pane:"
echo "  tmux capture-pane -p -t ${SESSION_NAME}:<pane-index>"
echo ""
echo "Navigation in tmux:"
echo "  Ctrl+b q         Show pane numbers"
echo "  Ctrl+b o         Next pane"
echo "  Ctrl+b <number>  Go to pane <number>"
echo ""
echo "To CLEANUP when done:"
echo "  # Kill all agent panes (keep pane 0):"
echo "  for p in \$(tmux list-panes -t ${SESSION_NAME} -F '#\{pane_index\}' | grep -v '^0'); do"
echo "    tmux kill-pane -t ${SESSION_NAME}:\$p 2>/dev/null; done"
echo ""
echo "  # Or kill entire session:"
echo "  tmux kill-session -t ${SESSION_NAME}"
