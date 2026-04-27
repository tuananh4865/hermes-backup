---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 karpathy-llm-wiki (extracted)
  - 🔗 autonomous-wiki-agent (extracted)
  - 🔗 wiki-self-evolution (extracted)
relationship_count: 3
---

# LLM Knowledge Bases

**Author:** Andrej Karpathy  
**Source:** X/Twitter Post  
**Date:** April 10, 2026  
**URL:** https://x.com/karpathy/status/2039805659525644595

---

## Post Content

LLM Knowledge Bases Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge (stored as markdown and images). The latest LLMs are quite good at it.

## Data Ingest

- Index source documents (articles, papers, repos, datasets, images, etc.) into a `raw/` directory
- Use an LLM to incrementally "compile" a wiki
- Wiki = collection of `.md` files in a directory structure
- Includes: summaries of all data in raw/, backlinks, categorized concepts, articles, links
- Convert web articles into .md files using Obsidian Web Clipper extension
- Download related images locally so LLM can easily reference them

## IDE Frontend

- **Obsidian** is the IDE "frontend" where I can view:
  - Raw data
  - Compiled wiki
  - Derived visualizations
- **Important:** The LLM writes and maintains all the data of the wiki. I rarely touch it directly.
- Plugins: Marp for slides, and other data viewing formats

## Q&A — Where Things Get Interesting

- When wiki is big enough (~100 articles, ~400K words)
- Ask LLM agent complex questions against the wiki
- LLM will go off, research the answers, etc.
- **"I thought I had to reach for fancy RAG, but the LLM has been pretty good about auto-maintaining index files and brief summaries of all the documents"**
- LLMs read all important related data fairly easily at this ~small scale

## Output Formats

Instead of getting answers in text/terminal:
- Markdown files
- Slide shows (Marp format)
- Matplotlib images
- All viewable in Obsidian
- Often "file" outputs back into wiki to enhance for further queries
- **Explorations always "add up" in the knowledge base**

## Linting / Health Checks

Run LLM "health checks" over the wiki to:
- Find inconsistent data
- Impute missing data (with web searchers)
- Find interesting connections for new article candidates
- Incrementally clean up wiki and enhance data integrity
- **"The LLMs are quite good at suggesting further questions to ask and look into"**

## Extra Tools

- Develop additional tools to process data
- Vibe coded a small, naive search engine over the wiki
- Both use directly (web UI) and hand off to LLM via CLI as a tool for larger queries

## Further Explorations

As the repo grows, natural desire to think about:
- Synthetic data generation
- Finetuning to have LLM "know" the data in its weights instead of just context windows

## TLDR

> "raw data from a given number of sources is collected, then compiled by an LLM into a .md wiki, then operated on by various CLIs by the LLM to do Q&A and to incrementally enhance the wiki, and all of it viewable in Obsidian. You rarely ever write or edit the wiki manually, it's the domain of the LLM. I think there is room here for an incredible new product instead of a hacky collection of scripts."

---

## Key Takeaways for Our Wiki Agent

1. **LLM writes and maintains wiki** — human rarely touches directly
2. **No fancy RAG needed** — LLM auto-maintains index files and summaries
3. **Wiki grows through use** — explorations always "add up"
4. **Health checks + linting** — LLM suggests further questions
5. **Output formats** — markdown, slides, visualizations all viewable in Obsidian
6. **Synthetic data + finetuning** — potential to encode wiki knowledge in model weights

## Related

- [[karpathy-llm-wiki]] — Karpathy's LLM Wiki approach
- [[autonomous-wiki-agent]] — Our implementation
- [[wiki-self-evolution]] — Wiki self-improvement pipeline
