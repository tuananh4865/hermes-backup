---
title: "Tun Dng Browser - 2026-04-16"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: ['concept']
---



---
title: "Tun Dng Browser - 2026-04-16"
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [browser], [automation tools], [macOS Safari]
---

# Tun Dng Browser - 2026-04-16

## Summary
This concept page documents a failed attempt by user Anh to control Safari using browser connect, resulting in an MCP session error due to no active tab. The page recommends opening the browser to verify tabs before attempting automation tools, suggesting preference for `text` parameters over `execute` for browser inspection.

## Key Insights
*   MCP tools require an active session to function without `open`.
*   Visual verification should prioritize `scroll` and `screenshot` over simple text matching.

## Analysis
The raw content reveals that the user attempted to launch Safari using a browser connect mechanism, but encountered an immediate error: "No active session, use `open` tool first." This indicates the browser could not initialize without an existing tab or session, a common limitation in MCP servers where `open` is mandatory before other tools. The user's solution involved opening the browser and using the MCP server to inspect tabs, acknowledging this recommended approach despite still failing. The subsequent advice highlights a critical distinction between text operations (`text`, `click`) and structural inspection (`execute`, `scroll`), emphasizing that for complex interactions like DOM manipulation or precise navigation, the primary tool should be `click` with descriptive text parameters rather than executing arbitrary JavaScript. Future iterations should utilize the `scroll` tool to position the viewport before capturing screenshots for visual confirmation, while avoiding `execute` tools for debugging page elements to prevent ambiguous match failures.

## Related
- [[transcript-system]]