---
title: "Wiki Transcript Hook"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [wiki, transcripts, automation, hook]
---

# Wiki Transcript Hook

## Overview

The Wiki Transcript Hook is an automated system that captures and archives conversation transcripts from AI assistant sessions into a structured wiki format. When an AI assistant session concludes, this hook triggers a process that extracts the full conversation history, formats it into readable wiki-style markdown, and saves it to a designated transcripts directory. This creates a persistent, searchable record of all interactions that can be referenced, reviewed, or used for training and analysis purposes.

The hook operates as part of the broader [[hermes-agent-self-evolution]] framework, which aims to enable AI systems to learn and improve from their operational history. By automatically capturing transcripts, the system ensures that valuable conversational context and insights are not lost after sessions end. The transcripts serve as both an audit trail and a knowledge base that can inform future interactions and system improvements.

## How It Works

The Wiki Transcript Hook is triggered by the `session:end` event, which fires automatically when an AI assistant session terminates. This event-driven architecture ensures that transcript capture happens without requiring manual intervention or explicit commands from the user.

When triggered, the hook performs the following sequence of operations. First, it locates and loads the complete session transcript from the stored JSONL file located in `~/.hermes/sessions/*.jsonl`. These JSONL files contain the raw conversation data in a structured format, including timestamps, messages, and metadata for each exchange within the session. Second, the hook parses this JSONL data and transforms it into formatted wiki-style markdown. This transformation includes proper heading structures, message attribution, timestamps, and any code blocks or special formatting preserved from the original conversation. Finally, the hook writes the formatted transcript to the appropriate location in the wiki directory structure: `~/wiki/raw/transcripts/[date]/[topic].md`.

The directory structure organizes transcripts by date and topic, making it easy to locate specific conversations based on when they occurred and what subject matter they covered. This systematic organization supports both human browsing and programmatic access to the transcript archive.

## Use Cases

The Wiki Transcript Hook serves several important purposes within an AI assistant workflow. The primary use case is documentation and knowledge preservation. By automatically capturing all conversations, users build a comprehensive archive of their interactions with the AI assistant. This archive becomes valuable for tracking project history, reviewing past decisions, and找回 previously discussed information.

A second major use case is training and analysis. The captured transcripts provide real-world examples of how the AI assistant was used, what types of questions were asked, and how the assistant responded. This data can inform system improvements, prompt engineering refinements, and better understanding of user needs. Researchers and developers can analyze transcript patterns to identify common tasks, frequent errors, or opportunities for new capabilities.

The hook also supports continuity across sessions. When a user returns to a project after some time, they can review relevant transcripts to refresh their memory about previous discussions, decisions, or work-in-progress. This is particularly valuable for long-term projects where context from past conversations would otherwise need to be re-established from scratch.

Finally, the transcript archive enables collaboration and sharing. Team members can access shared transcripts to understand what was discussed in previous sessions, review shared work, or build upon prior iterations. This transforms individual AI assistant use into a collaborative knowledge resource.

## Related

- [[hermes-agent-self-evolution]] — Self-evolution system that leverages session data for AI improvement
- [[Hermes Agent]] — The broader agent framework this hook operates within
- [[Intelligent Agents]] — General concept of goal-directed AI systems
- [[AI Agents]] — Overview of autonomous AI systems that generate transcripts
- [[Tool Use]] — How agents interact with systems and external tools during sessions
