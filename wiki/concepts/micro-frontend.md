---
title: "Micro-Frontend"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [micro-frontend, web-development, architecture, frontend, javascript]
---

# Micro-Frontend

## Overview

Micro-Frontend architecture extends the principles of [[Microservices]] to the frontend, decomposing a large, monolithic frontend application into smaller, independently deployable pieces that can be developed, tested, and deployed by separate teams. Each micro-frontend owns a discrete piece of the user interface—from a single feature to an entire page—and these pieces are composed at runtime to form a cohesive application. The term was popularized in a 2016 ThoughtWorks Technology Radar article, though the approach predates the naming.

The motivation for micro-frontends mirrors microservices: at a certain scale, a monolithic frontend becomes a bottleneck. Large teams step on each other's code, deployment cycles are coupled, and technology upgrades become risky multi-month projects. Micro-frontends allow teams to work autonomously, choose their own technology stacks within constraints, and deploy independently.

Micro-frontends don't require any specific framework—teams might use [[React]], [[Vue]], [[Angular]], or [[Svelte]] for different parts of the same application. The challenge becomes integration: how do independently developed pieces work together seamlessly? This is both a technical problem (how do they communicate? how do they share state?) and an organizational one (how do teams coordinate? how do they maintain a consistent user experience?).

## Key Concepts

**Independent Deployability** is the core value proposition. Each micro-frontend should be deployable without coordinating with other teams or requiring a full application release. This implies that each micro-frontend has its own source repository, CI/CD pipeline, and production environment. If Team A fixes a bug, they can ship that fix immediately—not tied to Team B's release schedule.

**Domain Ownership** means each micro-frontend team owns a specific business domain end-to-end: from the database or API to the UI. A team might own the entire "Checkout" flow: the backend services that handle payments and inventory, the API endpoints, and the React components that render the checkout UI. This reduces hand-offs and aligns teams around business outcomes.

**Runtime Integration** distinguishes micro-frontends from simple module composition. Because each micro-frontend loads separately in the browser, they must be integrated at runtime rather than at build time. This can be done via iframes (the most isolated approach), [[Web Components]] (using custom elements), JavaScript modules loaded dynamically, or module federation (webpack 5's approach).

**Shared Dependencies** present a trade-off. Loading a separate copy of [[React]] for every micro-frontend is wasteful. Most implementations share common libraries through Module Federation, single-spa's shared dependencies, or by having micro-frontends declare peer dependencies that are resolved to a single instance at runtime.

## How It Works

There are several patterns for implementing micro-frontends, each with different trade-offs:

**Build-Time Composition**: Micro-frontends are built and bundled, then combined by a shell application at build time. This is the simplest approach but sacrifices independent deployability—any change requires rebuilding the shell.

**Runtime Composition via Module Federation** (Webpack 5): Each micro-frontend is a separately built bundle that can be loaded dynamically:

```javascript
// webpack.config.js (Micro-Frontend Host)
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin');

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'host',
      remotes: {
        checkout: 'checkout@https://checkout.example.com/remoteEntry.js',
        profile: 'profile@https://profile.example.com/remoteEntry.js',
      },
      shared: { react: { singleton: true }, 'react-dom': { singleton: true } },
    }),
  ],
};
```

```javascript
// webpack.config.js (Checkout Micro-Frontend)
new ModuleFederationPlugin({
  name: 'checkout',
  filename: 'remoteEntry.js',
  exposes: { './Checkout': './src/Checkout' },
  shared: { react: { singleton: true } },
});
```

**iframe-based Approach**: Each micro-frontend runs in its own iframe, providing complete isolation. Communication happens via postMessage:

```html
<!-- Shell application -->
<iframe src="https://checkout.example.com" id="checkout-frame"></iframe>

<script>
  document.getElementById('checkout-frame').contentWindow.postMessage(
    { type: 'USER_DATA', payload: userData },
    'https://checkout.example.com'
  );
</script>
```

## Practical Applications

**Large E-commerce Platforms** are a natural fit for micro-frontends. A marketplace like Amazon or eBay involves vastly different domains—search, product listings, cart, checkout, user accounts, reviews—developed by different teams. Micro-frontends let each team own their domain completely.

**Enterprise Dashboards** that aggregate data from multiple sources can use micro-frontends where each widget is a separately developed application. Teams can update their widgets independently without risking breaking other parts of the dashboard.

**Migration from Legacy Monoliths** is a compelling use case. Organizations can incrementally replace a legacy frontend by adding new micro-frontends alongside existing code, eventually decommissioning the old system once all features are migrated.

**Multi-Tenant SaaS Products** where different customers need different feature sets can use micro-frontends to compose the right feature set for each tenant, loading only what's needed.

## Examples

**Zalando** is often cited as a pioneering company for micro-frontend architecture. They developed their own solution called [[Module Federation]] (which was later open-sourced to webpack) and now run thousands of frontend developers across hundreds of independently deployable micro-frontends.

**Spotify** uses a similar approach with their "squad" model, where small autonomous teams own specific features end-to-end, including the frontend components.

**Single-Spa** is a popular JavaScript framework for micro-frontend architectures. It allows multiple [[JavaScript]] frameworks to coexist in the same page:

```javascript
import { registerApplication, start } from 'single-spa';

registerApplication({
  name: 'checkout',
  app: () => System.import('checkout'),
  activeWhen: '/checkout'
});

start();
```

## Related Concepts

- [[Microservices]] — The backend analogue to micro-frontend architecture
- [[Module Federation]] — Webpack 5's approach to sharing code between micro-frontends
- [[Web Components]] — Browser standard for creating encapsulated UI elements
- [[React]] — Commonly used framework for building micro-frontends
- [[Micro-Frontend Architecture]] — Alternative term for the same concept

## Further Reading

- [Micro Frontends](https://micro-frontends.org/) — Comprehensive resource and pattern catalog
- [Module Federation](https://module-federation.github.io/) — Official documentation for webpack's federated modules
- [single-spa](https://single-spa.js.org/) — Framework-agnostic micro-frontend framework

## Personal Notes

Micro-frontends solve a real problem but introduce significant complexity. The first question I ask when someone proposes micro-frontends is: "Do you actually have multiple teams developing the frontend independently?" If the answer is no, micro-frontends will likely create more problems than they solve. The coordination overhead, the need for robust CI/CD, the consistent design system—all of this is non-trivial. For most organizations, a well-structured monolith with clear module boundaries (but still one deployable unit) serves them better until they genuinely hit the scaling problem micro-frontends address.
