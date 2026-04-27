---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 feed (extracted)
  - 🔗 blogwatcher (extracted)
  - 🔗 syndication (inferred)
last_updated: 2026-04-11
tags:
  - RSS
  - feeds
  - content
  - aggregation
---

# RSS (Really Simple Syndication)

> RSS feeds let you subscribe to website updates and aggregate content from multiple sources.

## Overview

RSS (Really Simple Syndication) is a format for publishing regularly updated content:
- Blog posts, articles, podcasts
- Any content with a feed URL

Subscribers use feed readers to aggregate content from many sources in one place.

## RSS Feed Format

### XML Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>My Blog</title>
    <link>https://example.com</link>
    <description>Tech articles and tutorials</description>
    <item>
      <title>Understanding RAG</title>
      <link>https://example.com/rag-explained</link>
      <pubDate>Sat, 11 Apr 2026 12:00:00 GMT</pubDate>
      <description>Retrieval-Augmented Generation explained...</description>
    </item>
  </channel>
</rss>
```

### Atom Format (Alternative)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>My Blog</title>
  <subtitle>Tech articles and tutorials</subtitle>
  <link href="https://example.com/feed.xml" rel="self"/>
  <entry>
    <title>Understanding RAG</title>
    <link href="https://example.com/rag-explained"/>
    <updated>2026-04-11T12:00:00Z</updated>
  </entry>
</feed>
```

## Reading RSS with Python

### feedparser
```python
import feedparser

# Parse RSS feed
feed = feedparser.parse("https://example.com/feed.xml")

print(f"Title: {feed.feed.title}")
for entry in feed.entries:
    print(f"- {entry.title}: {entry.link}")
```

### With Requests
```python
import requests
import feedparser

response = requests.get("https://example.com/feed.xml")
feed = feedparser.parse(response.content)
```

## RSS in Wiki

### Blogwatcher Skill

Our [[blogwatcher]] skill monitors RSS feeds:
```bash
python3 skills/blogwatcher/blogwatcher.py --add https://example.com/feed.xml
python3 skills/blogwatcher/blogwatcher.py --check
```

### Feed Discovery
```python
# Auto-discover RSS from website
from bs4 import BeautifulSoup

def find_rss_feeds(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    feeds = []
    for link in soup.find_all('link', type='application/rss+xml'):
        feeds.append(link.get('href'))
    return feeds
```

## RSS Aggregators

### Self-hosted
| Aggregator | Description |
|------------|-------------|
| **Miniflux** | Minimal, fast, SQLite |
| **FreshRSS** | Full-featured, PHP |
| **Newsboat** | Terminal-based, Linux |
| **NetNewsWire** | Mac/iOS, sync |

### Cloud Services
- **Feedly**: Popular, free tier
- **Inoreader**: Feature-rich
- **The Old Reader**: Social, free

## RSS Generation

### Static Site Generation
Most static site generators have RSS plugins:
```bash
# Hugo
hugo --renderToDisc  # Generates RSS at /index.xml

# Next.js
# Add feed.xml to public/
```

### Python Feed Generation
```python
from feedgen.feed import FeedGenerator

fg = FeedGenerator()
fg.title("My Blog")
fg.link(href="https://example.com")
fg.description("Tech articles")

entry = fg.add_entry()
entry.title("Understanding RAG")
entry.link(href="https://example.com/rag")
entry.description("RAG explained...")

fg.rss_str()  # Returns RSS XML
fg.atom_str()  # Returns Atom XML
```

## RSS Best Practices

### Feed Quality
1. **Valid XML**: Use validators
2. **Consistent format**: Choose RSS or Atom, stick with it
3. **Full content**: Include full article, not just summary
4. **Proper dates**: Use RFC 2822 format

### Feed Metadata
```xml
<channel>
  <title>Clear, descriptive title</title>
  <link>Canonical URL</link>
  <description>What this feed is about</description>
  <language>en-us</language>
  <image>
    <url>https://example.com/icon.png</url>
    <title>Site Icon</title>
  </image>
</channel>
```

## Related Concepts

- [[blogwatcher]] — Our RSS monitoring skill
- [[feed]] — General feed concept
- [[syndication]] — Content syndication
- [[content]] — Content aggregation

## External Resources

- [RSS 2.0 Spec](https://www.rssboard.org/rss-specification)
- [Atom Spec](https://datatracker.ietf.org/doc/html/rfc4287)
- [feedvalidator](https://feedvalidator.org/)