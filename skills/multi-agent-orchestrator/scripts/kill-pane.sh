#!/bin/bash
# Kill a specific tmux pane
# Usage: kill-pane.sh <pane-index>

PANE="$1"

if [ -z "$PANE" ]; then
    echo "Usage: kill-pane.sh <pane-index>"
    echo "Run list-panes.sh to see available panes"
    exit 1
fi

echo "Killing pane $PANE"
tmux kill-pane -t "$PANE"
echo "Pane $PANE killed"
