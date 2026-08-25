---
name: mcp-integration
description: Use MCP (Model Context Protocol) servers with Hermes — covers the native client that auto-registers MCP tools at startup AND the mcporter CLI for ad-hoc calls and discovery from the terminal. Load when working with MCP servers, configuring mcp_servers in config.yaml, or calling MCP tools from outside Hermes.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [MCP, Model-Context-Protocol, mcporter, native-mcp, tools, integrations, stdio, HTTP, oauth]
    related_skills: []
---

# MCP Integration

Two complementary ways to use MCP (Model Context Protocol) servers with Hermes. Pick by use case — they're not mutually exclusive, you can use both simultaneously.

## Which to Use

| Need | Use |
|------|-----|
| Configure MCP servers so their tools appear inside Hermes (auto-injected) | **Native MCP client** (Section 1) |
| Add a server to `~/.hermes/config.yaml` under `mcp_servers:` | **Native MCP client** (Section 1) |
| Debug "tool not appearing" / "MCP SDK not available" / connection issues | **Native MCP client** (Section 1) |
| Call an MCP tool from the terminal without configuring anything | **mcporter CLI** (Section 2) |
| Ad-hoc connect to an HTTP MCP server URL or run a stdio server on the fly | **mcporter CLI** (Section 2) |
| Generate a CLI wrapper or TypeScript types/client for a server | **mcporter CLI** (Section 2) |
| OAuth login flow / persistent daemon for a server | **mcporter CLI** (Section 2) |

Decision rule: if the goal is to give the agent new tools, use the native client. If the goal is to call MCP tools from a terminal/script without round-tripping through the agent, use mcporter.

---

## Section 1: Native MCP Client

Hermes Agent has a built-in MCP client that connects to MCP servers at startup, discovers their tools, and makes them available as first-class tools the agent can call directly. No bridge CLI needed — tools from MCP servers appear alongside built-in tools like `terminal`, `read_file`, etc.

### Prerequisites

- **mcp Python package** — optional dependency; install with `pip install mcp`. If not installed, MCP support is silently disabled.
- **Node.js** — required for `npx`-based MCP servers (most community servers)
- **uv** — required for `uvx`-based MCP servers (Python-based servers)

```bash
pip install mcp
# or
uv pip install mcp
```

### Quick Start

Add MCP servers to `~/.hermes/config.yaml` under the `mcp_servers` key:

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

Restart Hermes Agent. On startup it will:
1. Connect to the server
2. Discover available tools
3. Register them with the prefix `mcp_time_*`
4. Inject them into all platform toolsets

You can then use the tools naturally — just ask the agent to get the current time.

### Configuration Reference

Each entry under `mcp_servers` is a server name mapped to its config. Two transport types: **stdio** (command-based) and **HTTP** (url-based).

**Stdio Transport (command + args):**

```yaml
mcp_servers:
  server_name:
    command: "npx"             # (required) executable to run
    args: ["-y", "pkg-name"]   # (optional) command arguments, default: []
    env:                       # (optional) environment variables for the subprocess
      SOME_API_KEY: "value"
    timeout: 120               # (optional) per-tool-call timeout in seconds, default: 120
    connect_timeout: 60        # (optional) initial connection timeout in seconds, default: 60
```

**HTTP Transport (url):**

```yaml
mcp_servers:
  server_name:
    url: "https://my-server.example.com/mcp"   # (required) server URL
    headers:                                     # (optional) HTTP headers
      Authorization: "Bearer sk-..."
    timeout: 180               # (optional) per-tool-call timeout in seconds, default: 120
    connect_timeout: 60        # (optional) initial connection timeout in seconds, default: 60
```

**All Config Options:**

| Option            | Type   | Default | Description                                       |
|-------------------|--------|---------|---------------------------------------------------|
| `command`         | string | --      | Executable to run (stdio transport, required)     |
| `args`            | list   | `[]`    | Arguments passed to the command                   |
| `env`             | dict   | `{}`    | Extra environment variables for the subprocess    |
| `url`             | string | --      | Server URL (HTTP transport, required)             |
| `headers`         | dict   | `{}`    | HTTP headers sent with every request               |
| `timeout`         | int    | `120`   | Per-tool-call timeout in seconds                  |
| `connect_timeout` | int    | `60`    | Timeout for initial connection and discovery      |

A server config must have either `command` (stdio) or `url` (HTTP), not both.

### How It Works

**Startup Discovery.** When Hermes Agent starts, `discover_mcp_tools()` is called during tool initialization:
1. Reads `mcp_servers` from `~/.hermes/config.yaml`
2. For each server, spawns a connection in a dedicated background event loop
3. Initializes the MCP session and calls `list_tools()` to discover available tools
4. Registers each tool in the Hermes tool registry

**Tool Naming Convention.** MCP tools are registered as:
```
mcp_{server_name}_{tool_name}
```
Hyphens and dots are replaced with underscores for LLM API compatibility.
- Server `filesystem`, tool `read_file` → `mcp_filesystem_read_file`
- Server `github`, tool `list-issues` → `mcp_github_list_issues`
- Server `my-api`, tool `fetch.data` → `mcp_my_api_fetch_data`

**Auto-Injection.** MCP tools are automatically injected into all `hermes-*` platform toolsets (CLI, Discord, Telegram, etc.) — available in every conversation without additional configuration.

**Connection Lifecycle.** Each server runs as a long-lived asyncio Task in a background daemon thread. Connections persist for the lifetime of the agent process. If a connection drops, automatic reconnection with exponential backoff kicks in (up to 5 retries, max 60s backoff). On agent shutdown, all connections are gracefully closed.

**Idempotency.** `discover_mcp_tools()` is idempotent — calling it multiple times only connects to servers that aren't already connected.

### Security

**Environment Variable Filtering.** For stdio servers, Hermes does NOT pass your full shell environment to MCP subprocesses. Only safe baseline variables are inherited:
- `PATH`, `HOME`, `USER`, `LANG`, `LC_ALL`, `TERM`, `SHELL`, `TMPDIR`
- Any `XDG_*` variables

All other environment variables (API keys, tokens, secrets) are excluded unless you explicitly add them via the `env` config key. This prevents accidental credential leakage to untrusted MCP servers.

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      # Only this token is passed to the subprocess
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."
```

**Credential Stripping in Error Messages.** If an MCP tool call fails, any credential-like patterns in the error message are automatically redacted before being shown to the LLM. Covers: GitHub PATs (`ghp_...`), OpenAI-style keys (`sk-...`), Bearer tokens, generic `token=`, `key=`, `API_KEY=`, `password=`, `secret=` patterns.

### Sampling (Server-Initiated LLM Requests)

Hermes supports MCP's `sampling/createMessage` capability — MCP servers can request LLM completions through the agent during tool execution. This enables agent-in-the-loop workflows.

Sampling is **enabled by default**. Configure per server:

```yaml
mcp_servers:
  my_server:
    command: "uvx"
    args: ["mcp-server-my-server"]
    sampling:
      enabled: true           # default: true
      model: "gemini-3-flash" # model override (optional)
      max_tokens_cap: 4096    # max tokens per request
      timeout: 30             # LLM call timeout (seconds)
      max_rpm: 10             # max requests per minute
      allowed_models: []      # model whitelist (empty = all)
      max_tool_rounds: 5      # tool loop limit (0 = disable)
      log_level: "info"       # audit verbosity
```

Disable sampling for untrusted servers with `sampling: { enabled: false }`.

### Troubleshooting

**"MCP SDK not available — skipping MCP tool discovery"** — `mcp` Python package not installed:
```bash
pip install mcp
```

**"No MCP servers configured"** — no `mcp_servers` key in `~/.hermes/config.yaml`, or it's empty. Add at least one server.

**"Failed to connect to MCP server 'X'"** — common causes:
- **Command not found**: the `command` binary isn't on PATH. Ensure `npx`, `uvx`, or the relevant command is installed.
- **Package not found**: for npx servers, the npm package may not exist or need `-y` in args to auto-install.
- **Timeout**: server took too long to start. Increase `connect_timeout`.
- **Port conflict**: for HTTP servers, the URL may be unreachable.

**"MCP server 'X' requires HTTP transport but mcp.client.streamable_http is not available"** — upgrade:
```bash
pip install --upgrade mcp
```

**Tools not appearing** — check that the server is listed under `mcp_servers` (not `mcp` or `servers`), YAML indentation is correct, and look at Hermes Agent startup logs. Tool names are prefixed with `mcp_{server}_{tool}`.

**KNOWN BUG (Hermes v0.15.x): HTTP Transport Test Passes But Tool Calls Fail.**
`hermes mcp test <server>` shows ✅ Connected and discovers tools, but actual tool calls fail with `"MCP server 'X' is not connected"`. Root cause: transport mismatch — the test uses HTTP GET, but tool calls use JSON-RPC over HTTP POST. For HTTP servers like Exa, the test succeeds but tool calls fail.
**Workaround**: use stdio-based MCP servers when possible. For HTTP servers, no workaround is currently available in v0.15.x.
Tracking: https://github.com/NousResearch/hermes-agent/issues/36264

**Connection keeps dropping** — client retries up to 5 times with exponential backoff (1s, 2s, 4s, 8s, 16s, capped at 60s). Gives up after 5 attempts.

**MCP web search returns `1027-output new_sensitive` for `site:` operator** — the backend's content moderation layer flags Google `site:` queries with trending/product keywords. Workaround: use the brand name as a plain keyword (e.g., "findniche tiktok shop" instead of `site:findniche.com`). Date filtering also doesn't work via `maxAgeHours` parameter — use natural language date hints ("june 2026", "last 30 days") instead. See `references/mcp-search-content-moderation-quirks.md` for the full 4-quirk reference with verification table (tested 2026-06-16).

## Social Media Aggregator MCP Servers

When the user asks "kết nối tất cả mạng xã hội", "post to all platforms", "post and read analytics", or "unified social media API" — they want a single MCP server that fronts multiple platforms (TikTok, Instagram, Facebook, YouTube, X, LinkedIn, etc.). Three real options as of June 2026 (full breakdown in `references/social-media-aggregators-mcp.md`):

| Server | Transport | Free tier | Best for |
|---|---|---|---|
| **Postiz MCP** | HTTP `https://api.postiz.com/mcp/{api-key}` | 5 channels, 400 posts/mo (cloud); unlimited (self-host Docker) | Most flexible — 30 platforms, open-source, MCP-native |
| **Zernio MCP** | HTTP `https://mcp.zernio.com` + Bearer token | Tiered; cheaper than Ayrshare ~82% | 15 platforms + 7 ad platforms; rate limit 1200/min |
| **Ayrshare MCP** | HTTP `https://api.ayrshare.com/mcp` + Bearer token | 20 posts/mo (image only) | Premium brand, 10 platforms, paid only after free tier |

**Default recommendation: Postiz Cloud Free tier** for personal creators — $0/mo, 5 channels, MCP-native, no Docker setup. Upgrade path: Pro $49/mo for 30 channels + 300 AI images + 30 AI videos.

### Config pattern (Hermes-specific, verified against current `config.yaml`)

```yaml
mcp_servers:
  postiz:
    url: https://api.postiz.com/mcp/<PASTE_API_KEY>
    timeout: 180
    connect_timeout: 60
```

Tools auto-register as `mcp_postiz_*` (e.g., `mcp_postiz_integrationList`, `mcp_postiz_schedulePost`, `mcp_postiz_uploadMedia`, `mcp_postiz_getAnalytics`). For Bearer token variant instead of URL-embedded key:

```yaml
mcp_servers:
  postiz:
    url: https://api.postiz.com/mcp
    headers:
      Authorization: Bearer <POSTIZ_API_KEY>
    timeout: 180
    connect_timeout: 60
```

### ⚠️ PITFALLS (verified 2026-06-25)

1. **TikTok OAuth REQUIRES HTTPS public domain** — TikTok does NOT accept `localhost` or `127.0.0.1` callback URLs (confirmed Stack Overflow 2022, still enforced 2026). For self-hosted Postiz, you need a real domain + Let's Encrypt + Cloudflare Tunnel. **For local dev / personal use → always use Hosted Cloud Postiz (`postiz.com`)**, not self-hosted.

2. **TikTok developer app approval is slow + rejection-prone** — even when you have a domain, TikTok may reject the app if use-case description is too vague. For n8n community (Nov 2025): "Can't get a TikTok app approved for posting". For personal creators, hosted Postiz handles this for you.

3. **KNOWN BUG v0.15.x still applies to HTTP transport** — `hermes mcp test postiz` may show ✅ connected + list tools, but actual tool calls fail with `"MCP server 'postiz' is not connected"`. **Workaround**: after editing `config.yaml`, run `~/.hermes/restart_gateway.sh` (NOT just `hermes gateway restart`), then test by asking the agent to call a tool directly. The gateway restart is what loads the new transport into the persistent event loop.

4. **Postiz Cloud rate limit: 100 req/hour on create-post endpoint** — not per-channel, but GLOBAL for the instance. One API call = one request even if scheduling to 5 channels. Self-hosters can bump via `API_LIMIT` env var. Zernio is 720x faster (1200/min) if rate limit matters.

5. **Self-hosted Postiz setup is genuinely difficult** — Reddit r/selfhosted (June 2025): "I selfhost a ton of stuff and Postiz have been by been the most convoluted and difficult to set up, even with docker". Needs: Docker + Postgres + Redis + Temporal + reverse proxy for HTTPS. **Recommend hosted cloud unless user explicitly wants self-host + has time**.

6. **Secret hygiene for API keys in `config.yaml`** — Telegram bot tokens and MiniMax sk-cp keys have been leaked by tools that inline secrets into f-strings (see `references/mcp-search-content-moderation-quirks.md` + `writing-secrets-to-files` skill). For Postiz API key: either URL-embed (less safe — visible in process list) OR use `env:POSTIZ_API_KEY` pattern with `headers:` block (preferred). See "Credential Stripping" section above for what gets auto-redacted in error messages.

### Setup workflow (Hosted Cloud — recommended for creators)

```
1. Sign up at https://postiz.com (Google OAuth)
2. Settings → Developers → Public API → Copy API key
3. Settings → Channels → Connect each platform (TikTok, IG, FB, YouTube, X...)
4. Backup config:
   cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak-pre-postiz-$(date +%Y%m%d)
5. Edit ~/.hermes/config.yaml → add `mcp_servers.postiz` block (see pattern above)
6. Restart gateway (NOT just agent):
   ~/.hermes/restart_gateway.sh
7. Verify in session: "List my connected social media accounts"
   → mcp_postiz_integrationList should return connected channels
8. Test post: "Schedule a test post 'hello from hermes' to my X account for 1 minute from now"
   → mcp_postiz_schedulePost → check X feed
```

### When to recommend which option

- **Default → Postiz Cloud Free** (5 channels, $0, MCP-native, 10-min setup)
- **Scale → Postiz Cloud Pro $49/mo** (30 channels, AI images/videos, unlimited posts)
- **Budget-sensitive + scale → Zernio** (cheaper than Ayrshare, fewer platforms but faster rate limit)
- **Premium brand + budget → Ayrshare** (longest-standing, SLA, but expensive)
- **Self-host + full control → Postiz Docker** (only if user has 4-6h + VPS + domain + likes maintenance)

See `references/social-media-aggregators-mcp.md` for full feature matrix, pricing tables, OAuth quirks per platform, and self-host Docker compose recipe.

### Examples

**Time Server (uvx):**
```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```
Registers tools like `mcp_time_get_current_time`.

**Filesystem Server (npx):**
```bash
# 1) Scaffold a project workspace
mkdir -p ~/Projects/mcp-sandbox && cd ~/Projects/mcp-sandbox
# 2) Add the server to config.yaml
cat >> ~/.hermes/config.yaml <<'YAML'
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"]
    timeout: 30
YAML
# 3) Restart Hermes Agent — tools appear prefixed `mcp_filesystem_*`
```
Tool surface includes `mcp_filesystem_read_file`, `mcp_filesystem_write_file`, `mcp_filesystem_list_directory`.

**GitHub Server with Authentication:**
```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xx...xxxx"
    timeout: 60
```

**Remote HTTP Server:**
```yaml
mcp_servers:
  company_api:
    url: "https://mcp.mycompany.com/v1/mcp"
    headers:
      Authorization: "Bearer sk-xxx...xxxx"
      X-Team-Id: "engineering"
    timeout: 180
    connect_timeout: 30
```

### Notes

- MCP tools are called synchronously from the agent's perspective but run asynchronously on a dedicated background event loop
- Tool results are returned as JSON with either `{"result": "..."}` or `{"error": "..."}`
- The native MCP client is independent of `mcporter` — you can use both simultaneously
- Server connections are persistent and shared across all conversations in the same agent process
- Adding or removing servers requires restarting the agent (no hot-reload currently)

---

## Section 2: mcporter CLI

Use `mcporter` to discover, call, and manage [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) servers and tools directly from the terminal.

### Prerequisites

Requires Node.js:
```bash
# No install needed (runs via npx)
npx mcporter list

# Or install globally
npm install -g mcporter
```

### Quick Start

```bash
# List MCP servers already configured on this machine
mcporter list

# List tools for a specific server with schema details
mcporter list <server> --schema

# Call a tool
mcporter call <server.tool> key=value
```

### Discovering MCP Servers

mcporter auto-discovers servers configured by other MCP clients (Claude Desktop, Cursor, etc.) on the machine. Browse registries like [mcpfinder.dev](https://mcpfinder.dev) or [mcp.so](https://mcp.so), then connect ad-hoc:

```bash
# Connect to any MCP server by URL (no config needed)
mcporter list --http-url https://some-mcp-server.com --name my_server

# Or run a stdio server on the fly
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

### Calling Tools

```bash
# Key=value syntax
mcporter call linear.list_issues team=ENG limit:5

# Function syntax
mcporter call "linear.create_issue(title: \"Bug fix needed\")"

# Ad-hoc HTTP server (no config needed)
mcporter call https://api.example.com/mcp.fetch url=https://example.com

# Ad-hoc stdio server
mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com

# JSON payload
mcporter call <server.tool> --args '{"limit": 5}'

# Machine-readable output (recommended for Hermes)
mcporter call <server.tool> key=value --output json
```

### Auth and Config

```bash
# OAuth login for a server
mcporter auth <server | url> [--reset]

# Manage config
mcporter config list
mcporter config get <key>
mcporter config add <server>
mcporter config remove <server>
mcporter config update <server>
mcporter config import <path>
```

Config file location: `./config/mcporter.json` (override with `--config`).

### Daemon

For persistent server connections:
```bash
mcporter daemon start
mcporter daemon status
mcporter daemon stop
mcporter daemon restart
```

### Code Generation

```bash
# Generate a CLI wrapper for an MCP server
mcporter generate-cli --server <name>
mcporter generate-cli --command <url>

# Inspect a generated CLI
mcporter inspect-cli <path> [--json]

# Generate TypeScript types/client
mcporter emit-ts <server> --mode client
mcporter emit-ts <server> --mode types
```

### Notes

- Use `--output json` for structured output that's easier to parse
- Ad-hoc servers (HTTP URL or `--stdio` command) work without any config — useful for one-off calls
- OAuth auth may require interactive browser flow — use `terminal(command="mcporter auth <server>", pty=true)` if needed

---

## References

- `references/exa-mcp-advanced-tools.md` — How to enable Exa advanced tools (`web_search_advanced_exa`) via URL query param config
- `references/mcp-search-content-moderation-quirks.md` — Backend moderation quirks: `site:` operator blocked, `maxAgeHours` ignored, stale results, mixed-language bias. 4 workarounds with verification table.
- `references/social-media-aggregators-mcp.md` — Postiz / Zernio / Ayrshare: full feature matrix, pricing tables, OAuth quirks per platform (TikTok/IG/FB/YouTube), self-host Docker compose recipe, rate limits, known MCP bugs. Knowledge bank for "kết nối tất cả MXH" use case.
