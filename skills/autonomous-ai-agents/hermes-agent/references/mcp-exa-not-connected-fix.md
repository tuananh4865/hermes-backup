# MCP Server "Not Connected" After Config Change (Hermes v0.15.x)

## Symptom
- `hermes mcp test exa` → ✅ Connected, discovers tools correctly
- Actual tool call → ❌ `"MCP server 'exa' is not connected"` or `"unreachable after N consecutive failures"`
- Config shows correct URL with `?tools=...` params

## Root Cause
Hermes v0.15.x changed MCP tool handling:
- **Test connection** (`hermes mcp test`) uses HTTP GET to verify endpoint is reachable
- **Actual tool calls** use JSON-RPC over HTTP POST

For HTTP-based MCP servers (like Exa at `https://mcp.exa.ai/mcp`), the test passes but subsequent tool calls may fail if the gateway hasn't picked up the new config properly.

## Fix Sequence

```bash
# 1. Update config with tools parameter
hermes config set mcp_servers.exa.url "https://mcp.exa.ai/mcp?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa"

# 2. Restart gateway to apply new config
hermes gateway restart

# 3. Wait 5-10 seconds for MCP server to reconnect

# 4. Test with actual tool call (not just hermes mcp test)
```

## Key Insight
`hermes mcp test` is NOT sufficient to verify MCP tools work. It only verifies the transport layer. Always do an actual tool call to verify end-to-end functionality.

## Related
- Hermes v0.15.x MCP breaking change: tool discovery moved to transport-level verification
- HTTP-based MCP servers (web-based) vs stdio-based servers behave differently post-restart