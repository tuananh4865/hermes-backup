---
name: apple-platform
description: Apple platform automation — Notes, Reminders, iMessage, and FindMy. Covers Apple Script / osascript workflows for macOS.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [apple, macos, notes, reminders, imessage, sms, findmy, device-tracking]
    related_skills: [apple-notes, apple-reminders, imessage, findmy]
---

# Apple Platform Automation

Automate Apple native apps on macOS via `osascript` / AppleScript and native CLIs.

## Umbrella Note

This skill absorbs four formerly separate skills covering Apple ecosystem apps. Each app gets a labeled subsection:

- `apple-notes` — Apple Notes via `memo` CLI
- `apple-reminders` — Apple Reminders via `remindctl`
- `imessage` — iMessage/SMS via `imsg` CLI
- `findmy` — FindMy device/AirTag tracking

---

## Section: Apple Notes (`apple-notes`)

### CLI: `memo`

```bash
memo list                    # List all notes
memo find "query"            # Search notes
memo new "Title" "Content"  # Create note
memo read <id>              # Read note
memo edit <id> "Content"    # Edit note
```

### AppleScript Fallback

```applescript
tell application "Notes"
  tell account "iCloud"
    make note at folder "Notes" with properties {name:"Title", body:"Content"}
  end tell
end tell
```

---

## Section: Apple Reminders (`apple-reminders`)

### CLI: `remindctl`

```bash
remindctl list                    # List reminders
remindctl add "Task"             # Add reminder
remindctl complete <id>          # Mark complete
remindctl delete <id>            # Delete
```

### AppleScript Fallback

```applescript
tell application "Reminders"
  tell list "Reminders"
    make new reminder at end with properties {name:"Task"}
  end tell
end tell
```

---

## Section: iMessage (`imessage`)

### CLI: `imsg`

```bash
imsg send "Name" "Message"     # Send message
imsg list contacts            # List contacts
imsg search "query"           # Search messages
```

### AppleScript Fallback

```applescript
tell application "Messages"
  send "Message" to buddy "Name" of service "E:jabber.org"
end tell
```

---

## Section: FindMy (`findmy`)

### AppleScript via osascript

```bash
# Get FindMy device locations
osascript -e 'tell application "FindMy" to get name of every device'
```

### Notes

- Requires macOS FindMy to be signed into iCloud
- AirTags appear as "Accessory" items
- Location data requires iCloud authentication

---

## References

Former standalone skill content:
- `references/apple-notes.md` — full notes reference
- `references/apple-reminders.md` — full reminders reference
- `references/imessage.md` — full iMessage reference
- `references/findmy.md` — full FindMy reference
