---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
platforms: [linux, macos, windows]
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

Extract transcripts from YouTube videos and convert them into useful formats.

## Setup

```bash
# If pip not found, use python3 -m pip
python3 -m pip install youtube-transcript-api
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

## Workflow

1. **Fetch** the transcript using the helper script with `--text-only --timestamps`.
2. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.
6. **For advice/learning videos**: Save to wiki as concept page + add key strategies to `references/youtube-growth-strategies.md`

### Deep Research Mode (When User Asks for Research/Học hỏi)

When the user explicitly asks for research or learning (not just summary), treat it as knowledge capture. **IMPORTANT: YouTube-only format — do NOT mix in TikTok, Instagram, or other platform content.**

1. **Extract full transcript** with timestamps
2. **Identify core themes** from transcript
3. **Do additional web research** on the topic (use exa or web search) to supplement video content
4. **Create dedicated wiki pages** for each sub-topic as SEPARATE files (NOT mixed together)
5. **Update index.md** with each new page
6. **Report**: List all created wiki pages with key takeaways

**Complete YouTube Success Formula — 6 Core Sub-topics:**

| # | Topic | Content |
|---|-------|---------|
| 1 | **Hook Formula** | First 5 seconds, 6 hook types (shock/stakes/question/visual/bold/proof), 5-second structure, psychology |
| 2 | **Script Structure** | 4-part framework (Hook→Context→Payload→Payoff), retention optimization, micro-hooks |
| 3 | **Title Writing** | 25 CTR formulas, curiosity gap patterns, A/B testing, <50 chars rule |
| 4 | **Thumbnail Design** | Face expression +20-30% CTR, 15 formulas, color psychology, 3-layer composition |
| 5 | **Video Editing** | Pacing (3 levels), cut every 3s, B-roll placement, audio mixing, tension building |
| 6 | **Niche Bending** | Format + Market = new niche, empty squares = blue ocean, mapping method |

**Deep research deliverables for YouTube advice videos:**
- Each sub-topic → separate `concepts/youtube-{topic-name}.md` wiki page
- Each page should be comprehensive (5,000+ chars) with psychology, formulas, examples, templates
- Create `references/` sub-folder for session-specific research findings
- Update index.md under "Concepts" section

When user says "nghiên cứu sâu", "tách nhỏ từng phần", "xây dựng bộ công thức" → activate deep research mode

## Saving Advice Videos to Wiki

When the user asks to "learn from" or "học hỏi" a video (not just summarize), treat it as a knowledge capture task:

1. **Create concept page** at `wiki/concepts/[descriptive-name].md`
2. **Frontmatter**: title, created, updated, type=concept, tags=[youtube, advice], sources=[video URL], confidence=high, relationships=[related concepts]
3. **Structure**:
   - Core message / thesis (1-2 sentences)
   - Numbered key lessons with quotes
   - Action items for the user
   - Related quotes
   - Link to related wiki pages
4. **Update navigation**: Add to `wiki/index.md` under Concepts, append to `wiki/log.md`
5. **Report**: List created files + key takeaways to user

### Example Structure for Advice Videos

```markdown
# [Video Title]

> **Source:** [Channel] ([Date])
> **Link:** [URL]
> **Core message:** [1-2 sentence thesis]

## N Key Lessons

### 1. [Lesson Name]
> "[Key quote]"
- [Supporting detail or context]

### 2. ...

## ACTION ITEMS

1. [Specific action for user]
2. ...

## RELATED
- [[related-wiki-page]]
```

## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing / pip not found**: run `python3 -m pip install youtube-transcript-api` (use python3 -m pip instead of bare pip).