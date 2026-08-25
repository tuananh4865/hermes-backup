# Social Media Aggregator MCP Servers — Knowledge Bank

> Verified June 25, 2026. Use when user asks about connecting/posting/reading analytics across multiple social platforms through a single MCP server.

## The Three Real Options (June 2026)

### 1. Postiz MCP ⭐ DEFAULT RECOMMEND

- **Official site**: https://postiz.com
- **MCP setup docs**: https://docs.postiz.com/mcp/setup
- **GitHub**: https://github.com/gitroomhq/postiz-app (32.3K stars)
- **License**: AGPL-3.0 (open source)
- **Latest**: v2.21.9 (June 18, 2026)
- **Stack**: NextJS + NestJS + Prisma + PostgreSQL + Temporal
- **Platforms**: 30+ (TikTok, Instagram, Facebook, YouTube, X, LinkedIn, Threads, Pinterest, Reddit, Bluesky, Mastodon, Discord, Slack, Telegram, WhatsApp, GMB, Dribbble, Vk, Lemmy, MeWe, Nostr, Listmonk, WordPress, Medium, Hashnode, Dev.to, Whop, Twitch, Skool, Kick, Warpcast)

**Hosted Cloud pricing** (https://postiz.com/pricing):
| Plan | Price/mo | Channels | Posts/mo | Notable |
|---|---|---|---|---|
| Free | $0 | 5 | 400 | 7-day trial of paid features |
| Standard | $29 | 5 | 400 | Best for content creators, 3 AI videos/mo |
| Team | $39 | 10 | Unlimited | 100 AI images + 10 AI videos/mo |
| Pro | $49 | 30 | Unlimited | 300 AI images + 30 AI videos/mo |
| Ultimate | $99 | 100 | Unlimited | 500 AI images + 60 AI videos/mo (agencies) |

**Self-hosted**: FREE software + VPS $5-20/mo. Need Docker, Postgres, Redis, Temporal, reverse proxy for HTTPS callback.

**MCP URL pattern**:
- Cloud: `https://api.postiz.com/mcp/{api-key}`
- Self-host: `https://{your-server}/mcp/{api-key}`
- Bearer alt: `https://api.postiz.com/mcp` + `Authorization: Bearer {api-key}`

**Tools exposed** (registered as `mcp_postiz_*`):
- `integrationList` — list connected social accounts
- `schedulePost` — schedule content to multiple platforms in one request
- `uploadMedia` — upload images/videos to Postiz CDN
- `listPosts` — list scheduled + published posts
- `deletePost` — delete scheduled post
- `getAnalytics` — pull per-platform analytics

**Rate limit**: 100 req/hour on cloud (create-post endpoint). Self-hosters tune via `API_LIMIT` env var.

**Authentication for API key**: `Settings > Developers > Public API` in Postiz UI.

---

### 2. Zernio MCP

- **Official site**: https://zernio.com
- **Setup guide**: https://zernio.com/blog/social-media-mcp
- **Platforms**: 15 social + 7 ad (TikTok, Instagram, YouTube, X, LinkedIn, FB, Threads, Pinterest, Bluesky, Reddit, Snapchat, WhatsApp + Meta/LinkedIn/TikTok/X/Reddit Ads)
- **Tools**: 280+ exposed via MCP
- **MCP URL**: `https://mcp.zernio.com` + Bearer token
- **Rate limit**: 1200 req/min (720x faster than Postiz Cloud)
- **Pricing**: ~$49/mo (tiered), reportedly 82% cheaper than Ayrshare
- **Use when**: Need ad-platform integration, or rate limit matters (Zernio = 72,000 req/hour vs Postiz = 100)

---

### 3. Ayrshare MCP

- **Official site**: https://www.ayrshare.com
- **MCP docs**: https://www.ayrshare.com/docs/whatsnew/latest (released June 17, 2026)
- **Platforms**: 10 (FB, X, LinkedIn, IG, TikTok, YouTube, Pinterest, Reddit, Threads, GMB)
- **Pricing**:
  - Free: 20 posts/mo, **image only**
  - Premium: $149/mo (individual)
  - Launch: $299/mo (MVPs)
  - Business: $599/mo (agencies, 30 profiles, $2.49-8.99 per extra profile)
- **Use when**: Premium brand + SLA + need established vendor. Not for budget-sensitive personal creators.

---

## Feature Matrix

| Feature | Postiz | Zernio | Ayrshare |
|---|---|---|---|
| MCP native | ✅ | ✅ | ✅ |
| Self-host option | ✅ Docker | ❌ | ❌ |
| Free tier | ✅ 5 channels | ✅ tiered | ✅ 20 posts (image only) |
| Platforms | 30+ | 15 | 10 |
| Ad platforms | ❌ | ✅ 7 | ❌ |
| Rate limit | 100/h | 1200/min | varies by plan |
| Video uploads (free tier) | ✅ | ✅ | ❌ image only |
| AI image gen | 100-500/mo | varies | ❌ |
| AI video gen | 3-60/mo | varies | ❌ |
| OAuth flow built-in | ✅ | ✅ | ✅ |
| Setup time | 5-10 min | 5-10 min | 5-10 min |
| Self-host difficulty | High (Reddit: "convoluted") | N/A | N/A |

---

## OAuth Quirks Per Platform (Critical for Setup)

### TikTok ⚠️ HARDEST
- **Does NOT accept `localhost` or `127.0.0.1` as callback URL** — verified Stack Overflow 2022, still enforced 2026
- **Requires HTTPS public domain** — needs real domain + Let's Encrypt + Cloudflare Tunnel for self-host
- **Developer app approval is slow + can be rejected** — use-case description must be specific. n8n community (Nov 2025): "Can't get a TikTok app approved for posting"
- **Self-host Postiz GitHub issue #1161 (Jan 2026)**: OAuth URL may have missing client_key, or redirect config mismatch
- **Workaround for personal use**: Use Hosted Cloud Postiz — they handle the developer app for you
- Source: https://developers.tiktok.com/doc/login-kit-web/, https://developers.tiktok.com/doc/login-kit-desktop/

### Instagram
- Two paths: Facebook Business OAuth OR standalone flow
- Source: https://docs.postiz.com/providers/instagram
- Business account required for analytics

### Facebook / GMB
- Facebook Business integration required for full features
- GMB = Google My Business (separate OAuth)

### X / Twitter
- Standard OAuth 2.0, callback URL must be HTTPS
- Self-host: also requires public domain

### YouTube / Google
- Google Cloud Console project + OAuth client ID
- Domain verification step

### LinkedIn
- LinkedIn Developer App + product approval (can take days)
- Marketing Developer Platform access needed for full posting

### Pinterest / Reddit / Threads
- Standard OAuth, easier than TikTok
- Reddit: 60-sec rate limit per endpoint

### Bluesky / Mastodon
- Open protocols, easiest OAuth of all
- Bluesky uses App Passwords (not OAuth) for some flows

---

## Self-Hosting Postiz — Docker Compose Recipe

Source: https://docs.postiz.com/installation/docker-compose

### Prerequisites
- Docker + Docker Compose
- 2GB RAM minimum (2 vCPU)
- Domain + HTTPS (Let's Encrypt or Cloudflare Tunnel)
- Reverse proxy (Caddy, Traefik, or nginx)

### Quick Start

```bash
# 1. Clone the docker compose repo
git clone https://github.com/gitroomhq/postiz-docker-compose
cd postiz-docker-compose

# 2. Configure environment
# Option A: edit docker-compose.yml directly
# Option B: create postiz.env (mounted to /config in container)
# Option C: create .env (not recommended)

# Required env vars (example):
# NEXT_PUBLIC_BACKEND_URL=https://postiz.yourdomain.com
# JWT_SECRET=<random-string>
# DATABASE_URL=postgresql://user:pass@postgres:5432/postiz
# REDIS_URL=redis://redis:6379
# API_LIMIT=100

# 3. Start
docker compose up -d

# 4. Access
# Frontend: http://localhost:4007
# Temporal UI: http://localhost:8080
```

### Self-host Cost Breakdown
- VPS (Hostinger/Hetzner): $5-20/mo
- Domain: $10-15/year
- Cloudflare Tunnel: FREE
- Maintenance time: 2-4h/month (OAuth refresh, updates)

### When to NOT Self-Host
- User is in a hurry to start
- User doesn't have a public domain
- User has never self-hosted anything (Reddit wisdom: setup is "convoluted")
- TikTok is a must-have (developer app approval is hard)

---

## MCP-Specific Issues in Hermes

### Known Bug v0.15.x: HTTP Transport Test Pass, Tool Calls Fail

`hermes mcp test <server>` shows ✅ connected + discovers tools, but actual tool calls return `"MCP server 'X' is not connected"`. Root cause: transport mismatch — test uses HTTP GET, tool calls use JSON-RPC over HTTP POST.

**Workaround** (verified):
1. After editing `config.yaml`, run `~/.hermes/restart_gateway.sh` (NOT just `hermes gateway restart`)
2. Test by asking agent to call a tool directly (e.g., "List my Postiz integrations")
3. If still failing, check `~/.hermes/gateway.log` for connection errors

Tracking: https://github.com/NousResearch/hermes-agent/issues/36264

### Secret Hygiene for `config.yaml`

Telegram bot tokens and MiniMax sk-cp keys have been leaked by tools that inline secrets into f-strings. For Postiz API key:

**Option A: URL-embed** (less safe — visible in process list)
```yaml
mcp_servers:
  postiz:
    url: https://api.postiz.com/mcp/<PASTE_KEY_HERE>
```

**Option B: Bearer via env** (preferred)
```yaml
mcp_servers:
  postiz:
    url: https://api.postiz.com/mcp
    headers:
      Authorization: Bearer ${POSTIZ_API_KEY}
```

Then in `~/.zshrc` or shell init:
```bash
export POSTIZ_API_KEY="your-key-here"
```

Hermes auto-strips credential patterns from error messages (ghp_, sk-, Bearer tokens). See SKILL.md "Security" section for full redaction list.

---

## Decision Tree — Which Server for Which User

```
User wants multi-platform posting + analytics
├─ Has VPS + domain + 4h setup time?
│   ├─ YES → Self-hosted Postiz (cheapest long-term)
│   └─ NO ↓
├─ Needs ad-platform integration?
│   ├─ YES → Zernio
│   └─ NO ↓
├─ Budget < $50/mo, needs > 5 channels?
│   ├─ YES → Zernio or Postiz Pro $49
│   └─ NO ↓
├─ TikTok is must-have + no dev experience?
│   ├─ YES → Postiz Cloud Free (5 channels includes TikTok)
│   └─ NO ↓
├─ Needs premium SLA + willing to pay $149+/mo?
│   ├─ YES → Ayrshare
│   └─ NO → Postiz Cloud Free tier ($0/mo)
```

---

## Sources (verified 2026-06-25)

- Postiz GitHub: https://github.com/gitroomhq/postiz-app
- Postiz MCP docs: https://docs.postiz.com/mcp/setup
- Postiz Docker docs: https://docs.postiz.com/installation/docker-compose
- Postiz pricing: https://postiz.com/pricing
- Postiz API: https://docs.postiz.com/public-api/introduction
- Postiz OAuth 2.0 blog: https://postiz.com/blog/direct-postiz-integration-oauth-api
- Zernio setup: https://zernio.com/blog/social-media-mcp
- Zernio Postiz comparison: https://zernio.com/blog/postiz-alternative
- Ayrshare MCP release: https://www.ayrshare.com/docs/whatsnew/latest
- Ayrshare pricing: https://www.ayrshare.com/pricing/
- TikTok Login Kit Desktop: https://developers.tiktok.com/doc/login-kit-desktop/
- TikTok Login Kit Web: https://developers.tiktok.com/doc/login-kit-web/
- Self-host Reddit thread: https://www.reddit.com/r/selfhosted/comments/1m8043i/
- GitHub issue #1161 (TikTok OAuth in self-hosted Postiz): https://github.com/gitroomhq/postiz-app/issues/1161
- Hermes bug tracking: https://github.com/NousResearch/hermes-agent/issues/36264

---

*Last verified: 2026-06-25 by Hermes Agent session with Tuấn Anh*