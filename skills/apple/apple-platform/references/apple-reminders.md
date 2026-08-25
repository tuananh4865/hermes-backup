# Apple Reminders Reference

Formerly a standalone skill. Content absorbed into `apple-platform`.

## CLI: `remindctl`

```bash
remindctl list                    # List reminders
remindctl add "Task"             # Add reminder
remindctl complete <id>          # Mark complete
remindctl delete <id>            # Delete
```

## AppleScript Fallback

```applescript
tell application "Reminders"
  tell list "Reminders"
    make new reminder at end with properties {name:"Task"}
  end tell
end tell
```
