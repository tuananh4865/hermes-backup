# X/Twitter Video Viewing

## Key Finding (2026-05-31)

**X/Twitter videos ARE viewable through the Hermes browser tool**, even when the main page shows auth wall. The video loads inside a dialog/modal.

### How it works

1. Navigate to `https://x.com/{user}/status/{id}/video/1`
2. A modal dialog opens with the video player
3. The video element exists: `document.querySelector('video')?.src`
4. Video URL is a `blob:` URL — not extractable as standalone URL, but video content IS visible in the browser

### Video metadata available

```javascript
// Get video element info
const v = document.querySelector('video');
v ? {src: v.src, width: v.offsetWidth, height: v.offsetHeight} : "no video"

// Get post stats from innerText
document.body.innerText  
// → "1.1M\nViews\n130\n621\n6.3K\n..." (views, replies, reposts, likes, bookmarks)
```

### What to do

- Use `browser_vision` to see the video frame/thumbnail
- Use `browser_console` to get video element info
- The Play button exists inside the modal — click via `browser_click` on the play button element

### Fallback

If browser harness daemon is down (CDP handshake error), the `browser_navigate` tool still works independently and can load pages with embedded videos.

## Related

- [[browser-harness]] — parent skill
- `references/tiktok-limitation.md` — TikTok comparison