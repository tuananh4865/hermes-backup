# Video Post Workflow — What WORKED May 20

## Session May 20: SUCCESSFUL Post

The repost workflow WORKED in session 20260520_234856:
- ✅ Export cookies from browser-harness
- ✅ Playwright with cookies → chromium launched
- ✅ Navigate to x.com/compose/post
- ✅ Video uploaded (100%)
- ✅ Caption typed correctly
- ✅ Post button ENABLED
- ✅ **Clicked Post → SUCCESS**

## Today's Session (May 21): FAILED

Same steps repeated but Post button was NEVER clicked after enabling:
- ✅ Video uploaded 100%
- ✅ Caption typed (Unicode corrupted but still)
- ✅ Post button enabled
- ❌ Kept debugging instead of clicking
- ❌ Button eventually disabled (inactivity timeout?)

## KEY LESSON

**When Post button enables → CLICK IMMEDIATELY, do not continue debugging.**

## Bot Detection Issue (May 21)

X appears to detect automated sessions for video+text combo:
- Video uploads 100%
- Text typed (may corrupt with `fill_input`)
- Post button enables briefly then disables
- Cookie auth works but behavior flagged

## For Video Posts: Use xurl API

browser-harness/Playwright is UNRELIABLE for video posts in 2026.
xurl API is the correct approach.

```bash
# Setup (once)
xurl auth apps add io2026 --client-id <ID> --client-secret <SECRET>
xurl auth oauth2 --app io2026

# Post
xurl post "caption" --media /tmp/google-io-2026-draft.mp4
```