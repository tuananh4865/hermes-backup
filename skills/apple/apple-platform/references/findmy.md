# FindMy Reference

Formerly a standalone skill. Content absorbed into `apple-platform`.

## AppleScript via osascript

```bash
# Get FindMy device locations
osascript -e 'tell application "FindMy" to get name of every device'
```

## Notes

- Requires macOS FindMy to be signed into iCloud
- AirTags appear as "Accessory" items
- Location data requires iCloud authentication
