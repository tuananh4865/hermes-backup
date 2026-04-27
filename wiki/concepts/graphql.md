---
title: GraphQL
description: Query language for APIs and a runtime for fulfilling those queries. GraphQL AI Working Group (2026) advancing AI agent integration, MCP server discovery, and enterprise federation.
tags:
  - api
  - graphql
  - ai-agents
  - mcp
  - federation
  - data-fetching
created: 2026-04-20
---

# GraphQL

GraphQL is a query language for APIs and a runtime for fulfilling those queries with existing data. It provides a complete description of the data in your API, gives clients the power to ask for exactly what they need, and enables powerful tooling for API development.

## GraphQL AI Working Group (January 2026)

In January 2026, the **GraphQL AI Working Group** met to advance foundational building blocks that enable agentic AI systems to safely and effectively interact with GraphQL APIs.

Key focus areas:
- **Tool discovery** — How AI agents find and use GraphQL endpoints as tools
- **Schema introspection** — Standardized schema sharing for agent comprehension
- **MCP integration** — Model Context Protocol compatibility for GraphQL servers
- **Security** — Authentication and rate limiting for AI-to-API calls

## GraphQL + AI Agents

### Why GraphQL Works for AI Agents

AI agents need to query data from external systems. GraphQL provides:

1. **Introspection** — Agents can query the schema itself to understand available data
2. **Single endpoint** — One `/graphql` endpoint for all data needs
3. **Structured responses** — Predictable JSON structure for parsing
4. **Nested data** — Fetch related data in one round-trip

### Building AI Agents with GraphQL Schemas

```typescript
// Apollo GraphQL + AI Agent integration
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';
import { Agent } from 'your-agent-framework';

const client = new ApolloClient({
  uri: 'https://api.example.com/graphql',
  cache: new InMemoryCache(),
});

// Agent discovers available data via introspection
const schemaQuery = gql`
  query IntrospectSchema {
    __schema {
      types {
        name
        fields {
          name
          type { name kind }
          args { name type { name kind } }
        }
      }
    }
  }
`;

// Agent uses schema to construct queries
const query = gql`
  query GetUserWithPosts($userId: ID!) {
    user(id: $userId) {
      name
      email
      posts {
        title
        content
        tags
      }
    }
  }
`;
```

### GraphQL + MCP (Model Context Protocol)

The Model Context Protocol enables AI systems to connect to GraphQL APIs as external tools:

```typescript
// MCP Server exposing GraphQL as a tool
import { MCPServer } from '@modelcontextprotocol/sdk/server';
import { ApolloClient } from '@apollo/client';

const server = new MCPServer({
  tools: [
    {
      name: 'graphql_query',
      description: 'Execute a GraphQL query against the user database',
      inputSchema: {
        type: 'object',
        properties: {
          query: { type: 'string' },
          variables: { type: 'object' }
        }
      },
      handler: async ({ query, variables }) => {
        const result = await client.query({ query, variables });
        return result.data;
      }
    }
  ]
});
```

## Enterprise GraphQL in 2026

### Federation

GraphQL Federation allows composing multiple GraphQL services into a single unified graph:

```graphql
# Subgraph A: Users
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

# Subgraph B: Products
type Product @key(fields: "id") {
  id: ID!
  name: String!
  price: Float!
}

# Subgraph C: Orders (references User and Product)
type Order @key(fields: "id") {
  id: ID!
  user: User!
  items: [OrderItem!]!
  total: Float!
}
```

### Performance Optimization

```typescript
// DataLoader: solve N+1 problem
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await User.findByIds(ids);
  return ids.map(id => users.find(u => u.id === id));
});

// In resolver
const resolvers = {
  Order: {
    user: (order) => userLoader.load(order.userId)
  }
};
```

## REST vs GraphQL for AI Agents

| Aspect | REST | GraphQL |
|--------|------|---------|
| **Tool discovery** | Manual/OpenAPI | Self-documenting via introspection |
| **Data fetching** | Multiple endpoints | Single endpoint, exact data |
| **Caching** | HTTP caching | Manual cache management |
| **Learning curve** | Simple | Steeper |
| **AI agent support** | Good with OpenAPI | Excellent schema introspection |
| **File uploads** | Native | Requires extensions |

## GraphQL Clients for AI Applications

| Client | Language | Best For |
|--------|----------|----------|
| **Apollo Client** | TypeScript/JS | React apps, caching |
| **urql** | TypeScript/JS | Lightweight, React |
| **gqlgen** | Go | Type-safe Go clients |
| ** Strawberry** | Python | Pythonic GraphQL |
| **Absinthe** | Elixir | Functional GraphQL |

## See Also

- [[MCP]] — Model Context Protocol for AI tool integration
- [[API-design]] — API best practices
- [[ai-agent]] — AI agent architectures
- [[api-gateway]] — API gateway patterns
