---
name: youtube-transcript-extractor
title: YouTube Transcript Extractor
description: Extract full transcripts from YouTube videos for content creation and research
created: 2026-05-01
updated: 2026-05-01
type: skill
tags: [youtube, content, transcript]
confidence: high
---

# YouTube Transcript Extractor

Extract full transcripts from YouTube videos for content creation/research.

## Tool: youtube-content skill

```bash
skill_view(name="youtube-content")
```

This skill handles fetching YouTube video transcripts.

## Alternative: Direct yt-dlp

```bash
# Install if needed
pip install yt-dlp

# Get transcript
yt-dlp --write-auto-sub --sub-lang en --skip-download -o /tmp/video.%(ext)s https://youtu.be/VIDEO_ID

# Or get subtitles as transcript
yt-dlp --convert-subs srt --skip-download -o /tmp/video.%(ext)s https://youtu.be/VIDEO_ID
```

## Output Format for Tuấn Anh

When Tuấn Anh asks for video transcript:
1. Extract full transcript
2. Break into timestamped sections by topic
3. Create summary table at top (timestamp | section title)
4. Highlight key quotes/insights
5. Offer alternative formats (tweet thread, blog post, chapter-by-chapter)

## Note for Tuấn Anh Content

Tuấn Anh is a TikTok content creator interested in AI/tech topics. He asked for Andrej Karpathy "I've Never Felt More Behind" transcript (2026-05-01). Future requests may include:
- Tech podcast transcripts (Lex Fridman, Huberman, etc.)
- AI/LLM trend videos
- Code agent/agentic engineering content

For TikTok script purposes, focus on:
- Extractable viral hooks or insights
- Controversial/predictive statements
- Actionable advice for developers/founders
