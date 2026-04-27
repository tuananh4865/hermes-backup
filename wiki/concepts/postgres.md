---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 mcp (extracted)
  - 🔗 hermes-agent (extracted)
  - 🔗 database-design (extracted)
relationship_count: 3
---

# PostgreSQL MCP Server

## Overview

PostgreSQL MCP servers enable AI assistants to query and manipulate databases using natural language — no SQL expertise required. The LLM generates SQL from conversational requests, executes it via the MCP server, and returns results in human-readable format.

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│ AI Client   │◄───────►│ MCP Server   │◄───────►│ PostgreSQL│
│ (Claude)   │   MCP    │ (pgmcp)      │  SQL    │ Database   │
└─────────────┘         └──────────────┘         └────────────┘
     ↑                         ↓
     │                   Natural Language
     └────────────────── SQL Generation
```

## How It Works

1. **User** submits natural language query: "What were our top 5 products last month?"
2. **AI Client** (MCP client) sends request to MCP server
3. **MCP Server** receives the request and forwards to PostgreSQL
4. **PostgreSQL** executes generated SQL
5. **Results** return through MCP to AI client
6. **AI** formats response for user

## Popular PostgreSQL MCP Servers

| Server | Description | GitHub |
|--------|-------------|--------|
| **pgmcp** | Query any Postgres database in natural language | subnetmarco/pgmcp |
| **dbhub** | Multi-database support with detailed metadata | dbhub.ai |
| **pgEdge** | Enterprise-grade with auth and multi-database | pgedge/mcp |
| **Postgres MCP** | Simple stdio-based server | modelcontextprotocol/servers |

## Setup with Claude Desktop

### Option 1: Using pgmcp

```bash
# Install pgmcp
pip install pgmcp

# Configure Claude Desktop (~/.claude.desktop/config.json)
{
  "mcpServers": {
    "postgres": {
      "command": "pgmcp",
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

### Option 2: Using pgEdge MCP Server

```yaml
# pgedge-mcp-server/config.yaml
http:
  enabled: true
  address: ":8080"
auth:
  enabled: true
  token_file: "./postgres-mcp-tokens.yaml"
databases:
  - name: "production"
    host: "prod-db.example.com"
    port: 5432
    database: "prod_db"
    user: "readonly_user"
    sslmode: "require"
    allow_writes: false
```

## Key Features

### Schema Introspection
MCP servers can automatically:
- List tables, views, and columns
- Show data types and constraints
- Display indexes and foreign keys

### Query Capabilities
- SELECT queries (read data)
- INSERT/UPDATE/DELETE (with proper permissions)
- Transaction support
- Query result formatting

### Security Considerations

| Concern | Mitigation |
|---------|------------|
| **SQL Injection** | Server sanitizes LLM-generated SQL |
| **Excessive Queries** | Rate limiting, query timeout |
| **Data Exposure** | Row-level permissions, column masking |
| **Write Operations** | Explicit allow_writes flag |

## Comparison: MCP vs Direct SQL

| Aspect | Direct SQL | MCP + Natural Language |
|--------|------------|------------------------|
| **Skill Required** | SQL expertise | Natural language |
| **Speed** | Fast | Slight overhead (LLM generation) |
| **Flexibility** | Exact control | Conversational |
| **Error Rate** | Syntax errors | LLM may generate incorrect SQL |
| **Use Case** | Precise queries | Exploration, ad-hoc questions |

## Enterprise Considerations

### Authentication
- OAuth 2.1 integration recommended
- JWT token validation for production
- Connection-level permissions (readonly vs read-write)

### Multi-Database Support
Some MCP servers support connecting to multiple Postgres instances:
```yaml
databases:
  - name: "production"
    host: "prod.example.com"
    # ...
  - name: "staging"
    host: "staging.example.com"
    # ...
```

### Performance
- Connection pooling (essential for production)
- Query timeout limits
- Result size limits to prevent token overflow

## Use Cases

| Scenario | Example |
|----------|---------|
| **Data exploration** | "Show me all users who signed up in the last 30 days" |
| **Analytics** | "What's our monthly revenue trend for Q1?" |
| **Data entry** | "Update all addresses for customer ID 12345" |
| **Reporting** | "Generate a summary of active subscriptions" |
| **Debugging** | "Find all orders with status 'pending' older than 7 days" |

## Limitations

1. **Complex queries** — LLM may struggle with very complex JOINs or window functions
2. **Performance** — Natural language processing adds latency
3. **Security** — Always validate generated SQL before execution
4. **Schema changes** — LLM may not immediately know new tables/columns

## Related

- [[mcp]] — Model Context Protocol overview
- [[hermes-agent]] — Hermes MCP tool support
- [[database-design]] — PostgreSQL best practices