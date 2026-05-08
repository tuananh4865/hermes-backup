---
name: transcript-cleanup
description: Cleanup media files sau khi extract transcript - xóa video/audio để tiết kiệm disk space
category: utility
---

# Transcript Cleanup Skill

Tự động xóa media files (video/audio) sau khi transcript đã được extract thành công.

## Cleanup Rules

### Sau khi extract transcript thành công:
1. **Video files**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` → XÓA
2. **Audio files**: `.m4a`, `.mp3`, `.wav`, `.aac`, `.ogg` → XÓA
3. **Giữ lại**: `.md` transcript, `.vtt` subtitles, `.json` metadata

### Cleanup Locations
- `wiki/learning/tiktok-viral-script/transcripts/`
- `wiki/projects/tiktok-content-strategy/transcripts/`
- `wiki/raw/transcripts/`
- Bất kỳ folder nào chứa transcript từ video

## Cleanup Script

```bash
#!/bin/bash
# Cleanup media files sau transcript extraction

WIKI_PATH="/Volumes/Storage-1/Hermes/wiki"

find "$WIKI_PATH" -type f \( \
  -name "*.mp4" -o -name "*.mov" -o -name "*.avi" \
  -o -name "*.mkv" -o -name "*.webm" -o -name "*.m4a" \
  -o -name "*.mp3" -o -name "*.wav" -o -name "*.aac" \
\) -size +1k -delete 2>/dev/null

echo "Cleanup completed: $(date)"
```

## When to Run

1. **Sau khi extract transcript thành công** - tự động trong pipeline
2. **Định kỳ hàng tuần** - cleanup any leftovers
3. **Trước khi backup** - giảm kích thước backup

## Integration with Transcript Pipeline

```python
# Sau khi transcript extraction hoàn tất:
def on_transcript_extracted(video_path: str, transcript_path: str):
    # Verify transcript was created
    if os.path.exists(transcript_path):
        # Extract file size of video before delete
        video_size = os.path.getsize(video_path)
        
        # Delete video if size > 1MB (to avoid deleting thumbnails)
        if video_size > 1_000_000:
            os.remove(video_path)
            print(f"Deleted {video_path} ({video_size / 1_000_000:.1f}MB)")
```

## Safe Cleanup Thresholds

| File Type | Min Size to Delete | Reason |
|-----------|-------------------|---------|
| Video (.mp4, .mov, etc.) | > 1MB | Skip small previews |
| Audio (.m4a, .mp3, etc.) | > 100KB | Skip sound effects |
| All types | None if transcript.md exists | Transcript is primary artifact |
