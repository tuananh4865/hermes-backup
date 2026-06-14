# Exa MCP Advanced Tools Configuration

## Problem
Exa MCP server has tools marked as "disabled" in `hermes mcp list` output — but they're not actually disabled, they're just not enabled in the URL.

## Root Cause
Default Exa MCP URL `https://mcp.exa.ai/mcp` only enables the 2 basic tools (`web_search_exa`, `web_fetch_exa`). Advanced tools require explicit opt-in via URL query parameter.

## Solution
Append `?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa` to the Exa MCP URL.

```bash
hermes config set mcp_servers.exa.url "https://mcp.exa.ai/mcp?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa"
```

## Available Exa MCP Tools

### Enabled by default
| Tool | Description |
|------|-------------|
| `web_search_exa` | Real-time web search, clean ready-to-use content |
| `web_fetch_exa` | Extract full webpage content as markdown |

### Available (require opt-in via `tools=` param)
| Tool | Description |
|------|-------------|
| `web_search_advanced_exa` | Advanced search with category filters, domain restrictions, date ranges, highlights, summaries, subpage crawling |

### Deprecated (use `web_search_advanced_exa` instead)
- `deep_researcher_start/check` → Exa Research API
- `company_research_exa` → `web_search_advanced_exa`
- `people_search_exa` → `web_search_advanced_exa`
- `deep_search_exa` → `web_search_advanced_exa`
- `crawling_exa` → `web_fetch_exa`
- `get_code_context_exa` → `web_search_exa`
- `linkedin_search_exa` → `web_search_advanced_exa`

## Verification
```bash
hermes mcp list
# Before: exa → all → ✓ enabled (only 2 tools active)
# After restart: exa → all → ✓ enabled (3 tools active)
```

## Apply Changes
MCP server config changes require gateway restart:
```bash
hermes gateway restart
```

## Exa API Docs
- https://exa.ai/docs/reference/exa-mcp
- Tool enable syntax: `https://mcp.exa.ai/mcp?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa`