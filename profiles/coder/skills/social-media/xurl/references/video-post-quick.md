# X Post Video — Quick Reference

## Video File Discovery (2026-05-21)

**Confirmed working locations:**
- `/tmp/google-io-2026-draft.mp4` — Remotion renders go here by default
- `/tmp/*.mp4` — Always check `/tmp/` first for recent video renders

**Check video specs:**
```bash
ffprobe -v quiet -print_format json -show_streams /tmp/google-io-2026-draft.mp4
```

## Caption (Google I/O 2026)
```
🚀 Google I/O 2026 — Gemini 3.5 Flash, Omni, Spark, Universal Cart, Smart Glasses, Antigravity 2.0

The Era of Agentic AI is HERE.

#GoogleIO #AI #Gemini #Tech
```

## xurl Video Post Workflow

```bash
# 1. Upload video (returns media_id)
xurl media upload /tmp/google-io-2026-draft.mp4

# 2. Wait for processing (poll status)
xurl media status MEDIA_ID
# If processing, wait and poll again

# 3. Post with media
xurl post "🚀 Google I/O 2026 — Gemini 3.5 Flash, Omni, Spark, Universal Cart, Smart Glasses, Antigravity 2.0

The Era of Agentic AI is HERE.

#GoogleIO #AI #Gemini #Tech" --media-id MEDIA_ID
```

## Auth Status Check

```bash
xurl auth status
```

If no apps registered → user needs to setup OAuth outside agent session.

## Pitfalls

- Video processing is async — X needs time before tweet button enables after upload
- Browser-harness Chrome session may be logged out while `page_info()` shows authenticated URL
- Always screenshot to verify actual auth state, not just URL