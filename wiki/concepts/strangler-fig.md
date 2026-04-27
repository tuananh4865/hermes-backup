---
title: "Strangler Fig"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [software-architecture, migration, modernization, microservices, incremental-development]
---

# Strangler Fig

The Strangler Fig pattern is a software migration strategy that incrementally replaces a legacy system by gradually shifting functionality to a new system while keeping the old system running. Named after the strangler fig tree that germinates on another tree and eventually replaces it, this pattern enables modernization without risky big-bang rewrites. The approach transforms high-risk, multi-year migration projects into smaller, verifiable increments that deliver value throughout the transition.

## Overview

Legacy systems often contain decades of business logic encoded in outdated technologies—COBOL mainframes, older relational databases, or monolithic architectures that no longer serve modern needs. Rewriting such systems entirely is notoriously risky: the new system may take years to develop, business requirements change during development, and the old system's knowledge exists only in the heads of retiring engineers.

The Strangler Fig pattern addresses these risks by decomposing the migration into phases. Each phase identifies a bounded piece of functionality in the legacy system, implements it in the new system, and routes traffic to the new implementation. The old code remains operational but shrinks with each phase until it can be decommissioned entirely.

This pattern has been used successfully by major technology companies. Netflix used it to migrate from monolithic Java applications to microservices. Amazon used it to migrate their backend infrastructure. Microsoft used it for Azure's migration to its current platform. The common thread: none of these migrations required freezing feature development or taking systems offline.

## Key Concepts

### Incrementality

The core principle is small, deliverable increments. Each phase should be:
- **Bounded**: Clear scope that can be implemented in weeks, not months
- **Verifiable**: Functional and performance tested before going live
- **Reversible**: Can route traffic back to legacy if issues emerge

This approach reduces risk per release and provides frequent opportunities to validate direction.

### Traffic Splicing

Traffic routing mechanisms determine which system handles each request:

- **URL-based routing**: `/api/v2/orders` → new system, `/api/orders` → legacy
- **Header-based routing**: `X-API-Version: 2` → new system
- **Feature flags**: Toggle functionality between systems per user or request
- **Proxy/layer 7 routing**: nginx, HAProxy, or API gateway rules

### Feature Parity

Each migration phase must achieve functional equivalence with the legacy system before traffic switchover. This includes:
- Same inputs produce same outputs
- Error handling matches legacy behavior
- Side effects (database writes, external calls) occur at appropriate times
- Performance is within acceptable bounds

## How It Works

### Migration Phases

```
Phase 1: Analyze
├── Identify migration candidates (high-value, low-coupling)
├── Document legacy behavior (code analysis, testing, stakeholder interviews)
└── Design new system interface

Phase 2: Implement
├── Build new component with legacy interface
├── Connect to shared data store or create translation layer
└── Develop parallel operation capability

Phase 3: Validate
├── Shadow mode: new system processes requests but returns ignored
├── Compare outputs between legacy and new systems
└── Fix discrepancies until behavior matches

Phase 4: Switch
├── Route small percentage of traffic to new system
├── Monitor error rates and performance
└── Gradually increase traffic percentage

Phase 5: Decommission
├── Remove legacy code once traffic fully migrated
├── Archive old data in accessible format
└── Document final system architecture
```

### Anti-Corruption Layer

When migrating incrementally, the new system often cannot use the legacy data store directly. An anti-corruption layer translates between old and new schemas:

```python
# Anti-corruption layer example
class LegacyOrderRepository:
    def get_order(self, order_id: str) -> dict:
        # Old COBOL-era flat file format
        return self.flat_file.read_record(order_id)

class NewOrderRepository:
    def __init__(self, legacy_repo: LegacyOrderRepository):
        self._legacy = legacy_repo
        self._cache = RedisCache()

    def get_order(self, order_id: str) -> Order:
        # Check new format first
        cached = self._cache.get(f"order:{order_id}")
        if cached:
            return Order.from_dict(cached)

        # Fall back to legacy, convert to new format
        legacy_data = self._legacy.get_order(order_id)
        new_order = self._translate(legacy_data)

        # Store in new format for future reads
        self._cache.set(f"order:{order_id}", new_order.to_dict())
        return new_order

    def _translate(self, legacy_data: dict) -> Order:
        # Transform flat record to domain object
        return Order(
            id=legacy_data['ORDER-ID'],
            customer=Customer(id=legacy_data['CUST-NUM'], 
                           name=legacy_data['CUST-NAME']),
            items=[self._parse_line_item(l) for l in legacy_data['LINES']],
            # ... full translation logic
        )
```

## Practical Applications

### When to Use

- **Monolith to microservices migration**: Incrementally extract services
- **Legacy platform modernization**: Move from mainframe to cloud
- **Technology stack upgrades**: Python 2 to Python 3, Java 8 to Java 17
- **Database migrations**: Oracle to PostgreSQL, monolithic to event-driven

### Success Factors

- **Executive sponsorship**: Multi-year migrations require continued support
- **Comprehensive testing**: Automated tests verify legacy equivalence
- **Monitoring and rollback**: Observability enables quick problem detection
- **Parallel teams**: New development and migration can proceed simultaneously

## Examples

### Strangler Fig with API Gateway

```
                    ┌─────────────────┐
   Requests ───────▶│   API Gateway   │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                               │
              ▼                               ▼
    ┌─────────────────┐             ┌─────────────────┐
    │  Legacy System  │             │   New System    │
    │   (decreasing)   │             │  (increasing)    │
    └─────────────────┘             └─────────────────┘
```

Routing configuration:

```yaml
# nginx routing configuration
upstream legacy_backend {
    server legacy-app:8080;
}

upstream new_backend {
    server new-app:8080;
}

# Routes that haven't been migrated go to legacy
location /api/v1/ {
    proxy_pass http://legacy_backend;
}

location /api/v2/ {
    proxy_pass http://new_backend;
}

# Orders API migrated in v2
location /api/v1/orders {
    proxy_pass http://new_backend;
}
```

### Feature Flag Integration

```python
# Using feature flags for gradual traffic shifting
def get_order_handler(order_id: str) -> Order:
    if feature_flags.is_enabled('new-orders-api'):
        # Route to new service
        return new_order_client.get(order_id)
    else:
        # Legacy path
        return legacy_order_service.get(order_id)

# Traffic percentage increases as confidence grows
# Initially: 0% → new system (disabled)
# After validation: 5% → new system
# After stabilization: 25% → new system
# Final: 100% → new system
```

## Related Concepts

- [[Microservices Migration]] — Extracting services from monoliths
- [[Feature Flags]] — Controlling feature exposure dynamically
- [[Anti-Corruption Layer]] — Translating between system boundaries
- [[Legacy Modernization]] — General approaches to updating old systems
- [[Incremental Architecture]] — Building systems in small steps
- [[Database Migration]] — Schema and data migration patterns

## Further Reading

- Martin Fowler's original Strangler Fig article: https://martinfowler.com/bliki/StranglerFigApplication.html
- "Building Evolutionary Architectures" by Ford et al. — Supports incremental approaches
- Microsoft's eBook on enterprise migration patterns
- AWS Migration Hub documentation on strangler fig implementation

## Personal Notes

The Strangler Fig pattern's genius is its risk mitigation through incrementality. I've seen migrations fail when teams attempted big-bang cutovers—unexpected behavior emerged under real production load, and rolling back required running two full systems simultaneously under high pressure. The strangler approach makes rollback trivial: simply adjust the routing percentage. The pattern also provides psychological benefits: teams see regular progress, stakeholders see delivered value, and the migration never feels endless. My advice: resist the temptation to "fix everything at once." Focus each increment on a single bounded capability, get it working perfectly, then move on. The legacy system won't disappear overnight, but it will steadily shrink.
