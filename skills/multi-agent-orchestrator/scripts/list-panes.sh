#!/bin/bash
# List all panes in a tmux session with details
# Usage: list-panes.sh <session-name>
# Example: list-panes.sh orchestrator-12345

SESSION="$1"

if [ -z "$SESSION" ]; then
    echo "Usage: list-panes.sh <session-name>"
    echo ""
    echo "Active sessions:"
    tmux list-sessions 2>/dev/null || echo "  No sessions"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  PANES IN SESSION: $SESSION                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Header
printf "%-6s %-6s %-50s %s\n" "INDEX" "WIDTH" "TITLE" "STATUS"
printf "%-6s %-6s %-50s %s\n" "------" "------" "-----" "------"

tmux list-panes -t "${SESSION}" -F '#{pane_index}|#{pane_width}|#{pane_title}|#{pane_active}' 2>/dev/null | while IFS='|' read -r idx width title active; do
    STATUS=""
    if [ "$active" = "1" ]; then
        STATUS="[ACTIVE]"
    fi
    # Truncate title if too long
    title=$(echo "$title" | cut -c1-48)
    printf "%-6s %-6s %-50s %s\n" "$idx" "$width" "$title" "$STATUS"
done

echo ""
echo "Quick commands:"
echo "  Attach:              tmux attach -t ${SESSION}"
echo "  Monitor pane N:     tmux capture-pane -p -t ${SESSION}:N"
echo "  Kill pane N:        tmux kill-pane -t ${SESSION}:N"
echo "  Kill session:       tmux kill-session -t ${SESSION}"
echo "  Layout even:        tmux select-layout -t ${SESSION} even-horizontal"
