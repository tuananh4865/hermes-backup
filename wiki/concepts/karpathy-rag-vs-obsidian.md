---
title: X.com datachaz - Karpathy RAG vs Obsidian
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [transcript, twitter, carpathy, rag, obsidian]
---

# X.com datachaz - Karpathy RAG vs Obsidian

## Summary
In an autonomous file system, Karpathy replaces vector databases with markdown wiki pages to store raw AI research. Instead of writing code, he dumps raw data into a folder of markdown files for easier maintenance and retrieval.

## Key Insights
*   The system eliminates the need for complex vector storage by using a persistent markdown file structure.
*   The LLM functions as a research librarian, taking raw data and organizing it into a structured wiki format.
*   This method allows for more flexible retrieval of research compared to traditional vector databases.

## Analysis
1.  Karpathy's approach represents a significant architectural shift away from the traditional vector database model used for keyword search and similarity finding. By eradicating this, he simplifies the data storage layer while maintaining a robust foundation for knowledge extraction.
2.  The implementation of a three-stage workflow—raw ingest, compilation, and linting—ensures that the data remains clean and coherent before being fed into the AI engine. This disciplined approach helps prevent the "garbage in, garbage out" problem associated with unstructured text ingestion.
3.  The role of the LLM as a "research librarian" suggests that knowledge is not static but active and dynamic, evolving through the curated documentation process. This allows for continuous learning without requiring permanent server data retention, which is often a constraint in modern cloud-based research assistants.
4.  The replacement of a complex vector search algorithm with a simple markdown