---
title: Feed Aggregator
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [rss, feed, aggregation, syndication, content, reader, atom]
---

# Feed Aggregator

## Overview

A feed aggregator (also called a feed reader, news reader, or RSS reader) is software or service that collects and consolidates content from multiple sources into a single unified interface. Users subscribe to feeds from websites, blogs, podcasts, and news sources, and the aggregator automatically fetches and displays new content as it's published.

Feed aggregators solve the "content fragmentation" problem—rather than visiting dozens of websites to check for updates, users receive everything in one place. This pull-based model contrasts with social media's algorithmic, push-based consumption.

RSS (Really Simple Syndication) and Atom are the primary feed standards enabling this functionality.

## Key Concepts

**Feed Format**: Structured XML documents that contain:
- Channel metadata (title, description, link)
- Item entries (title, content, publication date, author)
- Optional enclosures (podcasts, media attachments)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Example Blog</title>
    <link>https://example.com</link>
    <description>A sample feed</description>
    <item>
      <title>New Article</title>
      <link>https://example.com/article</link>
      <pubDate>Sun, 13 Apr 2026 12:00:00 GMT</pubDate>
      <description>Article content here...</description>
    </item>
  </channel>
</rss>
```

**OPML (Outline Processor Markup Language)**: XML format for sharing feed subscriptions. Export your feeds as OPML to import into another aggregator.

**Feed Discovery**: Mechanisms for finding feeds on websites:
- `<link rel="alternate" type="application/rss+xml">` in HTML headers
- Autodiscovery links
- Common paths (/feed, /rss, /atom)

**Polling vs Webhooks**: Traditional aggregators poll feeds at intervals; webhook-based systems receive instant notifications when content updates.

## How It Works

```python
import feedparser
from datetime import datetime

class FeedAggregator:
    def __init__(self):
        self.feeds = {}
    
    def add_feed(self, name: str, url: str):
        """Subscribe to a new feed"""
        self.feeds[name] = url
    
    def fetch_updates(self):
        """Check all feeds for new content"""
        updates = []
        for name, url in self.feeds.items():
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:5]:  # Latest 5 items
                updates.append({
                    "source": name,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "Unknown"),
                    "summary": entry.get("summary", "")[:200]
                })
        return updates
    
    def mark_read(self, item_id: str):
        """Track read items"""
        pass
```

## Practical Applications

- **Personal News Consumption**: Curating a customized information diet
- **Content Monitoring**: Tracking mentions of keywords across multiple sources
- **Research Aggregation**: Collecting academic papers, industry news
- **Podcast Subscription**: Many podcast apps use RSS feeds
- **Marketing Intelligence**: Monitoring competitor announcements

## Examples

**RSS Client Implementation**:
```python
import feedparser
import html2text

def fetch_and_clean(feed_url: str) -> list[dict]:
    """Fetch feed and clean HTML to markdown"""
    feed = feedparser.parse(feed_url)
    h2t = html2text.HTML2Text()
    
    items = []
    for entry in feed.entries:
        items.append({
            "title": entry.title,
            "content": h2t.handle(entry.description),
            "url": entry.link,
            "date": entry.published
        })
    return items

# Usage
articles = fetch_and_clean("https://example.com/feed.xml")
for article in articles:
    print(f"- {article['title']}")
```

**Browser Feed Reader (Bookmarklet)**:
```javascript
javascript:(function(){
  var feeds = document.querySelectorAll(
    'link[type="application/rss"], link[type="application/atom"]'
  );
  if(feeds.length) {
    alert('Feeds found: ' + Array.from(feeds).map(f=>f.href).join(', '));
  } else {
    alert('No feeds detected on this page');
  }
})();
```

## Related Concepts

- [[rss]] — RSS feed format specification
- [[atom]] — Atom feed format
- [[auto-ingest]] — Automated content ingestion
- [[content-syndication]] — Distributing content across platforms
- [[information-feed]] — Social media feeds (different concept)

## Further Reading

- RSS 2.0 Specification
- FeedValidator.org

## Personal Notes

Feeds represent "intentional" content consumption—you're choosing sources rather than letting algorithms decide. They're experiencing a renaissance as people grow tired of algorithm-driven social feeds. Self-hosted aggregators like Miniflux or FreshRSS offer privacy advantages over hosted services.
