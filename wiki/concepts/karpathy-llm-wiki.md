---
title: Karpathy LLM Wiki
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [karpathy, llm, wiki, knowledge-base]
relationships:
  - 🔗 karpathy-llm-knowledge-base (extracted)
  - 🔗 karpathy-llm-wiki-architecture (extracted)
  - 🔗 karpathy-llm-knowledge-bases (extracted)
  - 🔗 autonomous-wiki-agent (extracted)
  - 🔗 wiki-self-evolution (extracted)
  - 🔗 self-healing-wiki (extracted)
  - 🔗 andrej-karpathy (extracted)
  - 🔗 llm-wiki (extracted)
  - 🔗 topic-workflow (extracted)
relationship_count: 9
---

# Karpathy LLM Wiki

Andrej Karpathy's approach to building personal knowledge bases using large language models represents a fundamental shift in how we think about AI-assisted knowledge management. Rather than relying on traditional retrieval-augmented generation (RAG) with vector similarity search, Karpathy advocates for maintaining a structured, interlinked markdown wiki that an LLM continuously compiles and maintains from raw source documents. This approach treats the wiki itself as the LLM's memory, creating a compounding knowledge system that grows more valuable over time.

## Overview

The core innovation of Karpathy's wiki approach lies in its simplicity: instead of retrieving relevant document chunks at query time through complex embedding and vector similarity mechanisms, the system maintains a living wiki that compounds over time. At query time, the LLM simply reads relevant wiki pages directly—no retrieval step required. This eliminates the "vector similarity is bad at nuance" problem that plagues traditional RAG implementations.

The wiki functions as a synthesized knowledge layer sitting between raw source materials and the LLM's context window. When you encounter interesting content—meeting transcripts, research papers, article clippings, or code comments—you feed it to the LLM which transforms it into structured markdown with proper frontmatter, summaries, and cross-links to existing pages. Over time, this creates a dense knowledge graph where every piece of information is connected to related concepts through explicit wikilinks.

Karpathy's philosophy emphasizes that knowledge management should feel natural and low-friction. The system isn't about building a perfect database; it's about creating a continuously evolving second brain that an LLM can effectively navigate and query. The key insight is that maintaining explicit relationships between concepts produces better results than trusting embedding-based similarity to capture semantic nuance.

## Key Patterns

### The Four-Phase Cycle

Karpathy's wiki operates on a continuous four-phase cycle that keeps knowledge fresh and interconnected:

**Phase 1 - Ingest**: Raw notes, research, highlights, and transcripts flow into the system from various sources. These include meeting transcripts automatically transcribed from conversations, web articles clipped from browser tabs, research highlights marked during paper reading, code comments extracted from repositories, and any other text-based content worth preserving. The ingestion phase is intentionally low-friction—the goal is to capture content without worrying about organization.

**Phase 2 - Compile**: The LLM transforms raw content into structured markdown with YAML frontmatter containing title, created date, updated date, type classification, and tags. The body of each page synthesizes the source material into coherent summaries with key insights extracted and organized. Critically, the compilation phase also identifies relationships to existing wiki pages and creates wikilinks connecting new content to the broader knowledge graph.

**Phase 3 - Lint (Self-Healing)**: Automated quality checks maintain wiki integrity. Broken wikilinks are detected and either fixed or stub pages are created. Missing frontmatter gets auto-filled from templates. Stale pages that haven't been updated in over 30 days get flagged for review. Orphan pages—those with no inbound links—get queued for relationship building. This self-healing mechanism ensures the wiki remains healthy without constant manual maintenance.

**Phase 4 - Query**: Natural language search through wiki files enables knowledge retrieval. The LLM reads relevant wiki pages as context rather than retrieving chunks, preserving full conversational and conceptual nuance that vector similarity would lose.

### Compounding Knowledge Graph

The wiki exhibits strong compounding effects as it grows. Early weeks might produce 10 pages with basic content, but by week four you could have 50 pages with dense cross-links. After three months, a 150-page knowledge graph emerges with compound knowledge relationships that weren't visible in any single source document.

This compounding happens through several mechanisms. Each new page typically links to 2-5 existing pages, automatically growing the density of the relationship graph. Backlink auto-generation scripts suggest missing bidirectional links. Quality improvement scripts score pages and flag low-scoring ones for human review. Gap analysis identifies under-covered topics and prioritizes their development.

### Wiki vs Vector RAG

The comparison between traditional RAG and the wiki approach reveals fundamental architectural differences. Traditional RAG relies on vector similarity search for retrieval, operates at chunk-level context, treats relationships as implicit through BM25 scoring, requires re-indexing on content changes, loses nuance through embedding compression, and organizes content in flat chunk spaces. The wiki approach provides direct LLM reading access, full page context, explicit wikilink relationships, simple add/edit maintenance, full text preservation without embedding loss, and hierarchical folder organization.

## Implementation

### Directory Structure

The implementation separates raw source material from synthesized knowledge:

**Raw Layer** (`raw/`): Contains unprocessed source material organized by type—transcripts from meetings and conversations, clipped web articles, academic papers converted from PDF to markdown, email imports, and associated assets like images and files.

**Synthesized Layer** (`concepts/`): Contains the actual wiki pages including system overview pages like `wiki.md` and `models.md`, topic-specific pages like `local-llm.md` and `karpathy-llm-wiki.md`, and synthesized knowledge pages for each major topic.

### Core Scripts

The automation relies on several key scripts working together:

`topic_workflow.py` handles the raw-to-concept synthesis pipeline, transforming unstructured source material into properly formatted wiki pages. `transcript_handler.py` specializes in converting meeting transcripts into searchable transcript pages. `ingest_article.py` transforms web URLs into markdown articles ready for wiki integration. `wiki_self_heal.py` runs automated fixes for lint issues including broken links, missing frontmatter, stale pages, and orphan pages. `semantic_search.py` enables content-based search across all wiki pages.

### Self-Healing Example

When the linting system detects a broken wikilink—perhaps `[[langgraph]]` in a page about multi-agent systems has no target—the self-healing pipeline activates automatically. First, `wiki_lint.py` detects that the link has no matching page. Then `wiki_self_heal.py` creates a stub page at the appropriate location with template frontmatter already filled in. The stub awaits human expansion when they encounter it during future work. Orphan resolution ensures pages with no inbound links get added to a task queue for relationship building.

### Daily Workflow

The practical daily workflow involves four steps. First, capture raw content into date-organized transcript folders. Second, process content through the topic workflow script or manual synthesis. Third, run the lint script and fix any issues it detects. Fourth, commit changes and push to the Git repository for backup and synchronization.

For deeper research work, the process involves creating detailed concept pages with dates, running gap analysis against the priority gaps file, and using the self-improvement mechanisms to expand under-covered topics.

## Related

- [[karpathy-llm-knowledge-base]] — Detailed breakdown of Karpathy's overall approach to LLM knowledge management
- [[karpathy-llm-wiki-architecture]] — Architecture deep-dive on the wiki system
- [[karpathy-llm-knowledge-bases]] — Additional resources and references
- [[karpathy-rag-vs-obsidian]] — Comparison between RAG and Obsidian-style wiki approaches
- [[andrej-karpathy]] — The person behind this approach
- [[autonomous-wiki-agent]] — Our implementation of a fully autonomous wiki maintenance agent
- [[self-healing-wiki]] — Detailed documentation of auto-fix mechanisms
- [[topic-workflow]] — Implementation details of the raw-to-concept pipeline
- [[llm-wiki]] — General concept of using LLMs with wiki systems
- [[wiki-self-evolution]] — How wikis can evolve autonomously over time

## Sources

- [What Is Andrej Karpathy's LLM Wiki?](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base-claude-code/)
- [Karpathy's LLM Knowledge Bases: The Post-Code AI Workflow](https://antigravity.codes/blog/karpathy-llm-knowledge-bases)
- [VentureBeat: Karpathy shares LLM Knowledge Base architecture](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)
