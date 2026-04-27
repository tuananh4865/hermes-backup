---
confidence: medium
last_verified: 2026-04-10
relationships:
  - 🔍 Clippings (inferred)
relationship_count: 1
---

# Obsidian Web Clipper

## Bookmarklet Setup (30 seconds)

### Step 1: Create Bookmark
1. Open any browser (Chrome, Firefox, Safari)
2. Create new bookmark (Cmd+D on Mac)
3. Name it: `Clip to Obsidian`
4. Leave URL empty for now

### Step 2: Copy Bookmarklet Code

```javascript
javascript:(function(){Promise.all([import('https://unpkg.com/turndown@6.0.0?module'),import('https://unpkg.com/@tehshrike/readability@0.2.0')]).then(async([{default:Turndown},{default:Readability}])=>{const vault="";const folder="Clippings/";let tags="clippings";const{title,byline,content}=new Readability(document.cloneNode(true)).parse();const markdownBody=new Turndown({headingStyle:'atx',hr:'---',bulletListMarker:'-',codeBlockStyle:'fenced',emDelimiter:'*'}).turndown(content);var date=new Date();const today=date.toISOString().split('T')[0];const fileContent='---\ncategory: "[[Clippings]]"\ntitle: "'+title+'"\nsource: '+document.URL+'\nclipped: '+today+'\ntags: ['+tags+']\n---\n\n'+markdownBody;document.location.href="obsidian://new?file="+encodeURIComponent(folder+title)+"&content="+encodeURIComponent(fileContent)+vaultName;})})();
```

### Step 3: Paste into Bookmark
1. Edit the bookmark you just created
2. Paste the code into the URL field
3. Save

### Step 4: Test It
1. Go to any article online (e.g., a Medium post)
2. Click the bookmarklet
3. Obsidian should open with the article converted to markdown

---

## Alternative: Official Obsidian Web Clipper

If the bookmarklet doesn't work reliably, use the official extension:

**Chrome/Edge:**
- Install: [Obsidian Web Clipper](https://chrome.google.com/webstore/detail/obsidian-web-clipper/lehpbdmbliologhjdhhofohgkgecpbpc)
- One-click to clip any webpage to Obsidian

**Firefox:**
- Install: [Obsidian Web Clipper](https://addons.mozilla.org/en-US/firefox/addon/obsidian-web-clipper/)

---

## Troubleshooting

### Bookmarklet Not Working in Safari
Safari doesn't support dynamic imports in bookmarklets. Use the official extension instead.

### "obsidian://" Protocol Not Recognized
Make sure Obsidian is installed and the "Inter-note links" advanced option is enabled:
- Obsidian Settings → Advanced → "Enable the new link format"

### Content Looks Wrong
The clipper uses Readability to extract main content. Some sites (like Twitter, Reddit) don't work well. For those, use the selection mode:
1. Select text on page
2. Click bookmarklet
3. Only selected text will be clipped

---

## How It Works
- Uses Readability.js to parse article content
- Converts HTML to Markdown via Turndown
- Opens Obsidian with `obsidian://new` protocol
- Pre-fills YAML frontmatter with metadata

## Related

- [[automation]] — General automation patterns
- [[email]] — Email auto-ingest for alternative capture
- [[rss]] — RSS feed monitoring
