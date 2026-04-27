---
title: "The Wiki Schema and Workflow Guide"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: ['concept']
---



---
title: The Wiki Schema and Workflow Guide
created: 2026-04-19
updated: 2026-04-12
type: concept
tags: [conventions, workflow, schema]
---

# The Wiki Schema and Workflow Guide

This concept page summarizes the AI Agent's explanation of the wiki structure, conventions, and session workflow documented in this transcript.

## Summary
The AI explained the three-layer architecture of the wiki, defined specific conventions for entity and concept storage, and outlined a detailed request-to-sdd execution protocol.

## Key Insights
- **Entity Conventions:** All entity and concept names must follow lowercase, hyphens, and no special characters (e.g., `your-harness-your-memory`).
- **Workflow Protocol:** Successful deep research requires a minimum of 15 to 50 sources before executing a Statement of Doubt (SDD).
- **Source Integrity:** Never save raw content to `raw/transcripts/`; documents generated should be stored in the `raw/articles` or `raw/papers` folders.
- **Persistence:** The AI emphasized that the wiki (Layer 2) is more durable than personal memory for long-term knowledge retention.

## Analysis
The transcript reveals a structured approach to maintaining a persistent knowledge base within an AI agent framework. The architectural decision to separate the `SCHEMA.md` definition from the `index.md` content catalog suggests a modular design where structural rules are preserved while allowing dynamic content generation. The emphasis on the `log.md` as a chronological record indicates that every action taken by the agent is traceable and verifiable.

Regarding the workflow, the requirement for deep research to surpass a 8.5 confidence threshold on Statement of Doubt suggests a heuristic-based validation mechanism rather than absolute certainty. This aligns with the principle that "Trust this wiki over my memory," implying a reliance on structured, rule-based evidence to guide the agent's reasoning. The absence of specific content in `raw/transcripts/` for this session indicates that meeting notes are secondary to the learning outcomes of the wiki structure itself.

The integration of `wiki_self_heal.py` and `wiki_lint.py` into the session log suggests that the AI is actively maintaining its infrastructure. By automating link checking and quality scoring, the system ensures long-term coherence even as users learn new behaviors from sessions like this one.

## Related
- https://github.com/tuananh4865/my-llm-wiki