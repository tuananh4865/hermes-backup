# Transcript Cleanup

Delete video/audio files after transcript extraction to save disk space.

## Cleanup Rules

After transcript extraction succeeds:
1. **Delete video files**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` → DELETE
2. **Delete audio files**: `.m4a`, `.mp3`, `.wav`, `.aac`, `.ogg` → DELETE
3. **Keep**: `.md` transcript, `.vtt` subtitles, `.json` metadata

### Cleanup Locations
- `wiki/learning/tiktok-viral-script/transcripts/`
- `wiki/projects/tiktok-content-strategy/transcripts/`
- `wiki/raw/transcripts/`
- Any folder containing video/audio transcripts

## Cleanup Script

```bash
#!/bin/bash
# Cleanup media files after transcript extraction

WIKI_PATH="/Volumes/Storage-1/Hermes/wiki"

find "$WIKI_PATH" -type f \( \
  -name "*.mp4" -o -name "*.mov" -o -name "*.avi" \
  -o -name "*.mkv" -o -name "*.webm" -o -name "*.m4a" \
  -o -name "*.mp3" -o -name "*.wav" -o -name "*.aac" \
\) -size +1k -delete 2>/dev/null

echo "Cleanup completed: $(date)"
```

## When to Run

1. **After transcript extraction succeeds** — automatic in pipeline
2. **Weekly** — cleanup any leftovers
3. **Before backup** — reduce backup size

## Integration with Transcript Pipeline

```python
# After transcript extraction completes:
def on_transcript_extracted(video_path: str, transcript_path: str):
    # Verify transcript was created
    if os.path.exists(transcript_path):
        video_size = os.path.getsize(video_path)
        
        # Delete video if size > 1MB (to avoid deleting thumbnails)
        if video_size > 1_000_000:
            os.remove(video_path)
            print(f"Deleted {video_path} ({video_size / 1_000_000:.1f}MB)")
```

## Safe Cleanup Thresholds

| File Type | Min Size to Delete | Reason |
|-----------|-------------------|--------|
| Video (.mp4, .mov, etc.) | > 1MB | Skip small previews |
| Audio (.m4a, .mp3, etc.) | > 100KB | Skip sound effects |
| All types | None if transcript.md exists | Transcript is primary artifact |
