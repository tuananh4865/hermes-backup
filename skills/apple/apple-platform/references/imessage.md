# iMessage Reference

Formerly a standalone skill. Content absorbed into `apple-platform`.

## CLI: `imsg`

```bash
imsg send "Name" "Message"     # Send message
imsg list contacts            # List contacts
imsg search "query"           # Search messages
```

## AppleScript Fallback

```applescript
tell application "Messages"
  send "Message" to buddy "Name" of service "E:jabber.org"
end tell
```
