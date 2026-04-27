#!/bin/bash
# Monitor agents in tmux session
# Usage: monitor-agents.sh <session-name> [pane-index]
# Example: monitor-agents.sh orchestrator-12345
#          monitor-agents.sh orchestrator-12345 2

SESSION="$1"
PANE="$2"

if [ -z "$SESSION" ]; then
    echo "Usage: monitor-agents.sh <session-name> [pane-index]"
    echo ""
    echo "Examples:"
    echo "  monitor-agents.sh orchestrator-12345      # Monitor all panes"
    echo "  monitor-agents.sh orchestrator-12345 2   # Monitor specific pane"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  AGENT MONITOR                                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo "Session: $SESSION"
echo ""

# If specific pane requested
if [ -n "$PANE" ]; then
    echo "=== Pane $PANE ==="
    tmux capture-pane -p -t "${SESSION}:${PANE}" | tail -20
    exit 0
fi

# Monitor all panes
echo "=== All Panes ==="
PANE_INDICES=$(tmux list-panes -t "${SESSION}" -F '#{pane_index}' 2>/dev/null)

if [ -z "$PANE_INDICES" ]; then
    echo "Session not found: $SESSION"
    exit 1
fi

for pane in $PANE_INDICES; do
    TITLE=$(tmux list-panes -t "${SESSION}" -F '#{pane_title}' 2>/dev/null | head -1)
    echo ""
    echo "--- Pane $pane ---"
    tmux capture-pane -p -t "${SESSION}:${pane}" | tail -15
done

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  QUICK COMMANDS                                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Attach to session:   tmux attach -t ${SESSION}"
echo "Switch panes:       Ctrl+b q (press number)"
echo "Capture pane N:      tmux capture-pane -p -t ${SESSION}:N"
echo "Send message:       tmux send-keys -t ${SESSION}:N 'message' Enter"
echo ""
echo "Cleanup all panes:"
echo "  for p in \$(tmux list-panes -t ${SESSION} -F '#\{pane_index\}' | grep -v '^0'); do tmux kill-pane -t ${SESSION}:\$p; done"
