---
title: "Feed"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [rss, feed, aggregation, syndication]
---

# Feed

## Overview

A feed is a data format that allows websites and applications to publish content updates in a standardized, machine-readable format. Feeds enable users to subscribe to content sources and receive updates without manually visiting each website. The technology behind feeds forms the backbone of content syndication on the web, allowing information to flow between platforms and enabling automated content monitoring at scale.

Feeds work on a simple publish-subscribe model: content publishers generate a feed file (typically XML-based) that contains their latest content items, and subscribers use feed readers or aggregators to check for and retrieve new content automatically. This decouples content consumption from the traditional browser-based model of visiting websites directly.

## Feed Types

### RSS (Really Simple Syndication)

RSS is the most widely adopted feed format, with several versions including RSS 2.0 and various predecessors. An RSS feed contains a list of items with metadata including title, description, publication date, and link to the original content. RSS feeds are typically identified by URLs ending in `.rss` or `.xml`.

### Atom

Atom was developed as a more rigorous and extensible alternative to RSS. The Atom Syndication Format (RFC 4287) provides a standardized format for web feeds that handles internationalization better and offers a cleaner specification. Atom feeds are commonly used by content management systems and API-driven applications.

### JSON Feed

A newer format that delivers feed content in JSON instead of XML, making it easier to parse in JavaScript-heavy applications while maintaining compatibility with existing feed readers through transformation layers.

## Aggregation

Feed aggregation is the process of collecting and consolidating multiple feeds into a single view. A feed aggregator or feed reader is software that:

- Subscribes to multiple feed sources
- Periodically checks each source for new content
- Organizes and displays items chronologically
- Marks items as read or starred
- Handles authentication for private feeds

Popular feed aggregators include [[logseq]] (which supports feed syncing), dedicated applications like FreshRSS, Inoreader, and Feedly, as well as browser-based and email-based solutions. Some [[agent-frameworks]] incorporate feed aggregation for content monitoring tasks.

## Use Cases

**Content Monitoring**: Feeds enable systematic monitoring of news sites, blogs, research publications, and competitor websites without manual checking. This is particularly valuable for [[deep-research]] workflows and competitive intelligence.

**Information Aggregation**: Researchers and professionals aggregate feeds from multiple sources to build personalized information pipelines, reducing noise and staying current in their fields.

**Automation Triggers**: Feed items can trigger automated workflows—when new content matching certain criteria appears, [[agent-frameworks]] can execute predefined actions like notifications, content summarization, or data extraction.

**Knowledge Management**: Tools like Obsidian and [[logseq]] can ingest feed content directly into personal knowledge bases, creating a seamless bridge between external content and private notes.

**Social Media Syndication**: Many social media tools use feeds to cross-post content or monitor brand mentions and industry trends.

## Related

- [[logseq]]
- [[deep-research-karpathy-agentic-workflows]]
- [[agent-frameworks]]
- [[search]]
- [[self-healing-wiki]]
- [[markdown]]
