# Apple Notes Reference

Formerly a standalone skill. Content absorbed into `apple-platform`.

## CLI: `memo`

```bash
memo list                    # List all notes
memo find "query"           # Search notes
memo new "Title" "Content"  # Create note
memo read <id>              # Read note
memo edit <id> "Content"    # Edit note
```

## AppleScript Fallback

```applescript
tell application "Notes"
  tell account "iCloud"
    make note at folder "Notes" with properties {name:"Title", body:"Content"}
  end tell
end tell
```
