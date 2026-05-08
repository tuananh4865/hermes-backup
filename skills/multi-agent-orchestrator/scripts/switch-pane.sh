#!/bin/bash
# Switch to a specific tmux pane
# Usage: switch-pane.sh <pane-index>

PANE="$1"

if [ -z "$PANE" ]; then
    echo "Usage: switch-pane.sh <pane-index>"
    echo "Run list-panes.sh to see pane indices"
    exit 1
fi

tmux select-pane -t "$PANE"
echo "Switched to pane $PANE"
