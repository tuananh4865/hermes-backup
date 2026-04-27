#!/bin/bash
# Orchestrator workflow - orchestrate multi-agent task
# Usage: orchestrate.sh <workspace> "<task-name>" "<task-description>" <agent1:type:role> <agent2:type:role> ...
# Example: orchestrate.sh "/path/to/repo" "Build Auth" "Build a complete auth system" "claude-code:architect" "claude-code:coder"

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
    echo '  orchestrate.sh "/path/to/repo" "Auth System" "Build complete JWT auth" "claude-code:architect" "claude-code:coder" "claude-code:tester"'
    exit 1
fi

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  HERMES ORCHESTRATOR                                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Task: $TASK_NAME"
echo "Description: $TASK_DESC"
echo "Workspace: $WORKSPACE"
echo "Agents: ${AGENTS[*]}"
echo ""

# Step 1: Create tmux session if not exists
SESSION_NAME="hermes-orchestrator"
if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "[1/5] Creating tmux session..."
    tmux new-session -d -s "$SESSION_NAME" -c "$WORKSPACE"
    tmux send-keys -t "$SESSION_NAME" "cd $WORKSPACE && hermes-agent" Enter
    sleep 3
fi

echo "[2/5] Spawning agents..."
PANE=1
for agent_spec in "${AGENTS[@]}"; do
    AGENT_TYPE="${agent_spec%%:*}"
    ROLE="${agent_spec##*:}"
    
    echo "  [$PANE] $AGENT_TYPE as $ROLE"
    
    case "$AGENT_TYPE" in
        claude-code) AGENT_CMD="claude" ;;
        gemini) AGENT_CMD="gemini" ;;
        hermes) AGENT_CMD="hermes-agent" ;;
    esac
    
    tmux split-window -h -d -c "$WORKSPACE"
    NEW_PANE=$(tmux list-panes -F '#{pane_index}' | tail -1)
    
    tmux send-keys -t "$NEW_PANE" "cd $WORKSPACE && $AGENT_CMD" Enter
    sleep 5
    
    tmux send-keys -t "$NEW_PANE" "You are the **$ROLE** agent. Task: $TASK_DESC" Enter
    
    PANE=$((PANE + 1))
    [ $PANE -ge 4 ] && break
done

echo ""
echo "[3/5] Distributing panes evenly..."
tmux select-layout -t "$SESSION_NAME" even-horizontal 2>/dev/null || true

echo "[4/5] Ready for multi-agent execution"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  AGENTS RUNNING                                           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Session: $SESSION_NAME"
echo "Agents: ${#AGENTS[@]}"
echo ""
echo "To view session: tmux attach -t $SESSION_NAME"
echo "Switch panes: Ctrl+b q → press number"
echo "Layout: tmux select-layout even-horizontal"
echo ""
echo "[5/5] Monitoring for completion..."
echo "Use collect-results.sh to gather outputs when done."
