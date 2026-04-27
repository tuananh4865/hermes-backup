#!/bin/bash
# Spawn MULTIPLE agents in split panes for a large task
# Usage: multi-spawn.sh <workspace> "<task-description>" <agent1-type:role> <agent2-type:role> ...
# Example: multi-spawn.sh "/path/to/repo" "Build e-commerce API" "claude-code:architect" "gemini:coder" "claude-code:reviewer"

set -e

WORKSPACE="$1"
TASK="$2"
shift 2
AGENTS=("$@")

if [ -z "$WORKSPACE" ] || [ -z "$TASK" ] || [ ${#AGENTS[@]} -eq 0 ]; then
    echo "Usage: multi-spawn.sh <workspace> <task> <agent1:type:role> <agent2:type:role> ..."
    echo ""
    echo "Example:"
    echo '  multi-spawn.sh "/path/to/repo" "Build e-commerce API" "claude-code:architect" "gemini:coder" "claude-code:reviewer"'
    exit 1
fi

echo "=== Multi-Agent Spawn ==="
echo "Workspace: $WORKSPACE"
echo "Task: $TASK"
echo "Agents to spawn: ${#AGENTS[@]}"
echo ""

# Check if we have tmux session
if ! tmux list-sessions &>/dev/null; then
    echo "Error: No tmux session found. Start tmux first."
    exit 1
fi

# Spawn each agent in sequence (split for each)
PANE_INDEX=1
for agent_spec in "${AGENTS[@]}"; do
    # Parse type:role
    AGENT_TYPE="${agent_spec%%:*}"
    ROLE="${agent_spec##*:}"
    
    echo "[$PANE_INDEX] Spawning $AGENT_TYPE as $ROLE..."
    
    case "$AGENT_TYPE" in
        claude-code)
            AGENT_CMD="claude"
            ;;
        gemini)
            AGENT_CMD="gemini"
            ;;
        hermes)
            AGENT_CMD="hermes-agent"
            ;;
        *)
            echo "Unknown agent type: $AGENT_TYPE"
            continue
            ;;
    esac
    
    # Split pane
    tmux split-window -h -d -c "$WORKSPACE"
    
    # Get new pane index
    NEW_PANE=$(tmux list-panes -F '#{pane_index}' | tail -1)
    
    # Start agent
    tmux send-keys -t "$NEW_PANE" "cd $WORKSPACE && $AGENT_CMD" Enter
    
    # Wait for init
    sleep 5
    
    # Set role
    tmux send-keys -t "$NEW_PANE" "You are the **$ROLE** agent on this team." Enter
    sleep 1
    
    # Set task context
    tmux send-keys -t "$NEW_PANE" "Main project task: $TASK" Enter
    sleep 1
    
    # Role-specific subtask
    case "$ROLE" in
        architect)
            tmux send-keys -t "$NEW_PANE" "Your focus: Design the system architecture, database schema, and API structure." Enter
            ;;
        coder)
            tmux send-keys -t "$NEW_PANE" "Your focus: Implement the code based on the architecture." Enter
            ;;
        reviewer)
            tmux send-keys -t "$NEW_PANE" "Your focus: Review code for bugs, security issues, and best practices." Enter
            ;;
        tester)
            tmux send-keys -t "$NEW_PANE" "Your focus: Write comprehensive tests." Enter
            ;;
        researcher)
            tmux send-keys -t "$NEW_PANE" "Your focus: Research best practices and provide recommendations." Enter
            ;;
        designer)
            tmux send-keys -t "$NEW_PANE" "Your focus: Design the UI/UX and create wireframes/mockups." Enter
            ;;
        pm)
            tmux send-keys -t "$NEW_PANE" "Your focus: Project management, timeline, and coordination." Enter
            ;;
        docs-writer)
            tmux send-keys -t "$NEW_PANE" "Your focus: Write documentation for the project." Enter
            ;;
    esac
    
    echo "      Spawned in pane $NEW_PANE"
    PANE_INDEX=$((PANE_INDEX + 1))
    
    # Max 4 agents
    if [ $PANE_INDEX -ge 4 ]; then
        echo "Max 4 agents reached. Remaining agents queued."
        break
    fi
done

echo ""
echo "=== All agents spawned ==="
echo "Layout evenly: tmux select-layout even-horizontal"
echo "Switch panes: Ctrl+b q → press number"
