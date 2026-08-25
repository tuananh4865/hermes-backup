# YouTube DOM Extraction — Concrete Code Snippets

Verified against the 2026 YouTube web layout. If YouTube redesigns again, dump one `ytd-rich-item-renderer` element's `outerHTML` to discover the new class names — the pattern (closed Shadow DOM with all rendered HTML in `outerHTML`) is stable, but class names shift every few months.

## 1. Video grid — extract title + view + age + duration + thumbnail

```javascript
JSON.stringify(Array.from(document.querySelectorAll('ytd-rich-item-renderer')).map(el => {
  const a = el.querySelector('a.ytLockupViewModelTitle, a.ytLockupViewModelContentImage');
  const metaSpans = el.querySelectorAll('.ytContentMetadataViewModelMetadataText');
  const metaAria = Array.from(metaSpans).map(s => s.getAttribute('aria-label'));
  const badge = el.querySelector('.ytBadgeShapeText');
  const thumb = el.querySelector('img.ytCoreImageHost');
  return {
    video_id: (a?.href || '').split('v=')[1]?.split('&')[0],
    href: a?.href,
    title: a?.title || el.querySelector('h3')?.getAttribute('title'),
    views: metaAria[0],      // "732 thousand views"
    ago:   metaAria[1],      // "4 days ago"
    duration: badge?.innerText,  // "23:49"
    thumb: thumb?.src        // includes ?sqp= cache buster
  };
}))
```

Returns array of 30 objects per page load (YouTube default grid size).

## 2. Title text only — for pattern frequency analysis

```javascript
JSON.stringify(Array.from(document.querySelectorAll('ytd-rich-item-renderer h3')).map(h => h.getAttribute('title')))
```

## 3. Watch-page description — expand + read

```javascript
// Click the "more" expander first
const exp = document.querySelector('ytd-text-inline-expander#description');
if (exp) exp.click();
JSON.stringify(document.querySelector('ytd-watch-metadata')?.innerText)
```

The metadata element lives in closed Shadow DOM but its `innerText` is exposed.

## 4. Playlist listing — extract playlist URLs only

```javascript
Array.from(document.querySelectorAll('a[href*="/playlist?list="]'))
  .map(a => a.href)
  .filter((v, i, a) => a.indexOf(v) === i)
```

To get playlist counts, must visit each playlist URL individually:
```
https://www.youtube.com/playlist?list=PLxxxxxxxx
```
Look for `N videos` + `M views` text in the heading group.

## 5. Thumbnail download — curl

```bash
curl -s -o v01.jpg "https://i.ytimg.com/vi/<VIDEO_ID>/maxresdefault.jpg"
# Check size: < 5KB means 404 placeholder, fallback to:
curl -s -o v01.jpg "https://i.ytimg.com/vi/<VIDEO_ID>/hqdefault.jpg"
```

## 6. Channel header info (verify section)

The channel header section exposes name, handle, sub count, video count, slogan in the page's `banner` region. Use `browser_snapshot` with `full: true` to read; or via JS:

```javascript
JSON.stringify({
  name: document.querySelector('ytd-channel-name yt-formatted-string')?.innerText,
  handle: document.querySelector('yt-channel-tagline-renderer #channel-handle, [class*="handle"]')?.innerText,
  subs: document.querySelector('#subscriber-count')?.innerText,
  videos: document.querySelector('#videos-count')?.innerText,
  slogan: document.querySelector('ytd-channel-tagline-renderer')?.innerText
})
```

## 7. Sub-channels & ecosystem — search description for handles

```javascript
const desc = document.querySelector('ytd-watch-metadata')?.innerText || '';
JSON.stringify({
  sub_channel_mentions: desc.match(/@[a-zA-Z0-9_]+/g),
  facebook: desc.match(/facebook\.com\/[^\s]+/g),
  zalo: desc.match(/Zalo:?\s*\+?\d[\d\s]*/g),
  emails: desc.match(/[\w.-]+@[\w.-]+\.\w+/g),
  phone: desc.match(/0\d{9,10}/g)
})
```

## Standardized vision prompt for thumbnails

```
Mô tả chi tiết thumbnail: màu nền chính, có illustration 2D/3D hay ảnh thật,
có khuôn mặt người không, có chữ overlay không (font/màu/vị trí),
có icon/symbol đặc trưng, có khung viền không, phong cách visual tổng thể.
Nếu là sponsored content thì nói rõ.
```

In English for non-Vietnamese channels, swap "Mô tả chi tiết" → "Describe in detail".