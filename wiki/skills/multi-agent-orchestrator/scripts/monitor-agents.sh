#!/bin/bash
# Monitor all agent panes - watch for completion
# Usage: monitor-agents.sh [interval-seconds]

INTERVAL="${1:-10}"

echo "=== Monitoring Agent Panes ==="
echo "Press Ctrl+C to stop"
echo ""

while true; do
    clear
    echo "=== $(date) ==="
    echo ""
    
    # List all panes with recent output
    tmux list-windows -a 2>/dev/null | grep -v "^0:" | while IFS= read -r line; do
        WINDOW=$(echo "$line" | awk '{print $1}' | tr ':' ' ')
        CMD=$(echo "$line" | awk '{print $NF}')
        LAST_LINES=$(tmux capture-pane -p -t "$WINDOW" 2>/dev/null | tail -2 | tr '\n' ' ' | cut -c1-60)
        echo "[$WINDOW] $CMD"
        echo "  $LAST_LINES"
        echo ""
    done
    
    echo "Refresh in ${INTERVAL}s..."
    sleep "$INTERVAL"
done
