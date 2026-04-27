---
title: "Knowledge Management"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [information-science, organizational-knowledge, documentation, learning, productivity]
---

# Knowledge Management

## Overview

Knowledge management is the discipline of capturing, organizing, storing, sharing, and maintaining the information and expertise that exists within an organization or individual. It encompasses both explicit knowledge—information that can be easily documented, codified, and transmitted (like manuals, policies, and databases)—and tacit knowledge—intuitive, experiential knowledge held in people's heads (like judgment, context, and institutional memory). Effective knowledge management enables individuals and organizations to learn from experience, avoid repeating mistakes, accelerate decision-making, and scale expertise across teams and time.

The field emerged in the 1990s as organizations recognized that knowledge, like physical assets, could be managed to create value. Peter Drucker popularized the concept of the "knowledge worker," and subsequently Nonaka and Takeuchi's work on organizational knowledge creation provided a influential theoretical framework. Today, knowledge management is increasingly relevant as organizations grapple with information overload, the need to onboard quickly in a distributed work environment, and the challenge of preserving institutional knowledge as employees transition.

## Key Concepts

**The SECI Model** — Nonaka and Takeuchi's framework describes how knowledge converts between forms. Socialization (tacit to tacit) happens through shared experiences. Externalization (tacit to explicit) is the process of articulating tacit knowledge into documented form. Combination (explicit to explicit) merges and reorganizes explicit knowledge. Internalization (explicit to tacit) is the process of learning from documents and making knowledge personal.

**Knowledge Capture** — Techniques for preserving undocumented knowledge: after-action reviews, retrospectives, pair programming, mentorship programs, recorded demos, and structured interviews with departing employees.

**Taxonomy and Ontology** — How knowledge is categorized. A taxonomy is a hierarchical classification scheme (this document belongs in "Engineering > Backend > Databases"). An ontology defines relationships between concepts (PostgreSQL is a type of relational database; it uses SQL; it supports ACID transactions).

**Knowledge Bases** — Centralized repositories for storing and retrieving information. Tools range from simple wikis and shared drives to sophisticated enterprise knowledge management systems like Confluence, Notion, and SharePoint.

**Knowledge Loops** — The continuous cycle of knowledge creation, sharing, and re-creation. Organizations that close this loop effectively develop a learning culture where insights flow freely and are continuously refined.

## How It Works

At an organizational level, knowledge management involves creating systems and processes that make it easy to capture knowledge when it's created, store it in accessible locations, connect it to related knowledge, and retrieve it when needed. This requires both technology (wikis, search, tagging systems) and culture (norms around documentation, psychological safety to share mistakes and lessons learned).

At an individual level, personal knowledge management (PKM) involves practices like note-taking (with tools like Obsidian, Roam Research, or plain text), Zettelkasten-style linking of ideas, regular review and synthesis, and deliberate practice of applying learned concepts. The goal is to build a connected body of knowledge that grows more valuable over time rather than a collection of isolated notes that are never revisited.

The biggest challenge in knowledge management is the knowledge graph problem—ensuring that knowledge is findable when someone needs it. This requires thoughtful tagging, good search infrastructure, and active curation to remove outdated information. Without these, well-intentioned knowledge bases devolve into "knowledge graveyards" where information goes to die.

## Practical Applications

Organizations use knowledge management to onboard new employees faster by providing structured learning paths and accessible documentation, to reduce rework by making past lessons learned accessible, to improve customer support by equipping agents with well-organized knowledge bases, to preserve institutional memory during team restructuring, and to accelerate research by making internal studies and findings searchable. In software teams, knowledge management practices manifest as runbooks, architecture decision records (ADRs), internal wikis, and post-mortem documentation.

## Examples

A simple architecture decision record (ADR):

```markdown
# ADR-042: Use PostgreSQL for the Primary Data Store

## Status
Accepted

## Context
We need a primary database for the customer management service.
We expect high write throughput with complex query patterns.

## Decision
We will use PostgreSQL 15 with the Citus extension for
horizontal scaling if needed.

## Consequences
- Pro: ACID compliance ensures data integrity
- Pro: Rich indexing options for query performance
- Con: Requires operational expertise for high availability
- Con: Horizontal scaling requires the Citus extension

## Alternatives Considered
- MySQL: Less JSON support, similar operational complexity
- MongoDB: Flexible schema but weaker relational integrity
```

A Zettelkasten-style note link structure:
```
- [[knowledge-management]] (this file)
  - links to: [[documentation-quality]], [[technical-writing]], [[skill-acquisition]]
  - tagged: #information-science #org-knowledge
```

## Related Concepts

- [[documentation-quality]] — Ensuring captured knowledge is high quality
- [[technical-writing]] — Skills for articulating knowledge clearly
- [[skill-acquisition]] — How individuals build knowledge over time
- [[knowledge-management]] — This concept itself relates to learning systems

## Further Reading

- Ikujiro Nonaka and Hirotaka Takeuchi, *The Knowledge-Creating Company* (1995)
- Thomas Davenport and Laurence Prusak, *Working Knowledge* (1997)
- Sönke Ahrens, *How to Take Smart Notes* — on personal knowledge management
- "Building a Knowledge Graph" — Neo4j documentation on knowledge representation

## Personal Notes

I've become an obsessive note-taker and knowledge archivist, but I'm still learning the difference between collecting notes and actually building knowledge. My biggest failure is "collector's fallacy"—the feeling of learning just from saving something interesting, without actually processing and connecting it. The Zettelkasten idea of treating notes as a thinking tool rather than an archive resonates with me. A good knowledge system should make you smarter, not just more organized.
