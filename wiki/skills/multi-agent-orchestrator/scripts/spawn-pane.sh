#!/bin/bash
# Spawn an agent in a NEW SPLIT PANE (side by side)
# Flow: split pane → start agent → wait → set role → task + ACCEPTANCE CRITERIA → VERIFY instruction
# Usage: spawn-pane.sh <agent-type> <workspace> "<role>" "<task>" "<acceptance-criteria>"
# Example: spawn-pane.sh "claude-code" "/path/repo" "coder" "Implement JWT auth" "1. Login works 2. Token persisted 3. Logout clears token"

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
    echo "Roles: pm, designer, researcher, architect, coder, reviewer, tester, docs-writer, coordinator"
    echo ""
    echo "Example:"
    echo '  spawn-pane.sh "claude-code" "/path/repo" "coder" "Implement JWT auth" "1. Login works 2. Token persisted 3. Logout clears token"'
    exit 1
fi

# Default acceptance if not provided
if [ -z "$ACCEPTANCE" ]; then
    ACCEPTANCE="1. Task completed as described 2. No errors 3. Code is functional"
fi

# Determine agent command
case "$AGENT_TYPE" in
    claude-code) AGENT_CMD="claude" ;;
    gemini) AGENT_CMD="gemini" ;;
    hermes) AGENT_CMD="hermes-agent" ;;
    codex) AGENT_CMD="codex" ;;
    opencode) AGENT_CMD="opencode" ;;
    *) echo "Unknown agent type: $AGENT_TYPE" && exit 1 ;;
esac

PANE_ID="${AGENT_TYPE}-${ROLE}-$(date +%s)"

echo "=== Spawning $AGENT_TYPE Agent ==="
echo "Role: $ROLE"
echo "Workspace: $WORKSPACE"
echo ""

# Step 1: Split current pane horizontally
echo "[1/7] Creating split pane..."
tmux split-window -h -d -c "$WORKSPACE"

NEW_PANE_INDEX=$(tmux list-panes -F '#{pane_index}' | tail -1)
echo "      Pane created: $NEW_PANE_INDEX"

# Step 2: Start the agent
echo "[2/7] Starting agent: $AGENT_CMD"
tmux send-keys -t "$NEW_PANE_INDEX" "cd $WORKSPACE && $AGENT_CMD" Enter

# Step 3: Wait for agent to initialize
echo "[3/7] Waiting for agent to initialize..."
case "$AGENT_TYPE" in
    claude-code) sleep 5 ;;
    gemini) sleep 4 ;;
    hermes|codex|opencode) sleep 3 ;;
esac

# Step 4: Set role
echo "[4/7] Assigning role: $ROLE"
tmux send-keys -t "$NEW_PANE_INDEX" "You are the **$ROLE** agent on this team." Enter

# Step 5: Send task with acceptance criteria
echo "[5/7] Sending task with acceptance criteria..."
TASK_MSG="[AGENT TASK]
Task: $TASK

Acceptance Criteria (MUST satisfy ALL):
$ACCEPTANCE

Context: Working directory is $WORKSPACE"

tmux send-keys -t "$NEW_PANE_INDEX" "$TASK_MSG" Enter

# Step 6: VERIFY instruction - critical for active verification
echo "[6/7] Adding verification instruction..."
VERIFY_MSG="IMPORTANT - VERIFY before reporting done:
1. Verify EACH acceptance criterion is met
2. Include EVIDENCE in your report (file paths, test output, etc)
3. Do NOT claim done until you have verified

Report format:
[REPORT] Task: $TASK | Status: done/issue/need-help | Evidence: <what you verified>"

tmux send-keys -t "$NEW_PANE_INDEX" "$VERIFY_MSG" Enter

# Step 7: Final instruction
echo "[7/7] Final instructions..."
FINAL_MSG="Report back to Orchestrator (Hermes) when:
- Task complete (with VERIFIED evidence)
- Found a problem (describe clearly)
- Need a decision (ask explicitly)
- Stuck for more than 2 minutes

Do NOT make up answers. If unsure, ask."
tmux send-keys -t "$NEW_PANE_INDEX" "$FINAL_MSG" Enter

echo ""
echo "=== Agent Spawned ==="
echo "Pane: $NEW_PANE_INDEX"
echo "Role: $ROLE"
echo "Agent: $AGENT_CMD"
echo ""
echo "Switch between panes:"
echo "  Ctrl+b q (shows pane numbers) → press number"
echo "  Ctrl+b Alt+Left/Right (cycle panes)"
echo ""
echo "Monitor this pane:"
echo "  tmux capture-pane -p -t $NEW_PANE_INDEX"
echo ""
echo "Layout evenly:"
echo "  tmux select-layout even-horizontal"
