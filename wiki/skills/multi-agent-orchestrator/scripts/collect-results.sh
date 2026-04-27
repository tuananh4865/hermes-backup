#!/bin/bash
# Collect results from all agent panes
# Usage: collect-results.sh [pane-index...]

PANE="$1"

if [ -z "$PANE" ]; then
    echo "Usage: collect-results.sh <pane-index>"
    echo "Run list-panes.sh to see pane indices"
    exit 1
fi

echo "=== Collecting from Pane $PANE ==="
echo ""
tmux capture-pane -p -t "$PANE" | tail -100
