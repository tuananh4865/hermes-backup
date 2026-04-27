#!/bin/bash
# Follow/monitor a pane - capture output for review
# Usage: follow-pane.sh <pane-id> [lines]
# Example: follow-pane.sh 1 50

PANE="$1"
LINES="${2:-50}"

if [ -z "$PANE" ]; then
    echo "Usage: follow-pane.sh <pane-id> [lines]"
    echo ""
    echo "Run list-panes.sh to see pane IDs"
    exit 1
fi

echo "=== Following pane $PANE (last $LINES lines) ==="
echo ""

tmux capture-pane -p -t "$PANE" 2>/dev/null | tail -"$LINES"
