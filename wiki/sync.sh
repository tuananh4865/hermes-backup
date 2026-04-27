#!/bin/bash
# Sync wiki to GitHub — run this at end of each session

cd ~/wiki

# Check if there are changes to commit
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to push"
    exit 0
fi

git add .
git commit -m "Wiki update — $(date '+%Y-%m-%d %H:%M')"
git push origin main

echo "Wiki synced to GitHub"
