---
title: "Feature Flags"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [deployment, software-engineering, devops, release-management, continuous-deployment]
---

# Feature Flags

Feature flags (also called feature toggles, feature switches, or release toggles) are a software development technique that enables code to be deployed to production while keeping features disabled. By wrapping functionality in conditional branches controlled by external configuration, teams can decouple deployment from release—code can be shipped days, weeks, or months before users interact with it. This separation transforms deployment from a one-way door into a reversible, controllable event.

## Overview

Feature flags represent one of the most impactful DevOps practices for enabling continuous delivery and reducing deployment risk. Instead of bundling features into large releases that are difficult to rollback, development teams ship code incrementally, enabling features only when ready. The flag acts as a circuit breaker between code and user experience.

This technique has become foundational at modern software organizations. Netflix, Facebook, LinkedIn, and Split.io pioneered sophisticated feature flag systems at scale. The practice enables:

- **Decoupled deployment and release**: Deploy code anytime; enable features when ready
- **Gradual rollouts**: Start with 1% of users, monitor, then expand
- **Instant rollbacks**: Disable problematic features without redeployment
- **A/B testing**: Compare user behavior across different feature variants
- **Parallel development**: Merge incomplete features without breaking production

Feature flags introduce complexity—every conditional branch is technical debt that must eventually be removed. Managing flag lifecycles (creation, targeting, monitoring, cleanup) requires discipline and tooling.

## Key Concepts

### Flag Types

Feature flags serve different purposes and have different lifecycle expectations:

| Type | Purpose | Typical Lifespan | Example |
|------|---------|------------------|---------|
| Release flags | Safely merge incomplete features | Days to weeks | `new-checkout-flow` |
| Experiment flags | A/B testing | Days to weeks | `pricing-variant-b` |
| Ops flags | Operational control | Variable | `maintenance-mode` |
| Permission flags | User segment targeting | Long-lived | `premium-features` |
| Kill switches | Emergency disable | Emergency only | `disable-payment` |

### Targeting Rules

Modern feature flag systems allow sophisticated targeting:

```yaml
# Example: LaunchDarkley targeting configuration
flag: new-recommendation-engine
default: false  # Everyone gets old behavior

rules:
  - name: Internal users
    targeting:
      - attribute: user_type
        operator: equals
        value: internal
    serve: true

  - name: Beta users
    targeting:
      - attribute: email
        operator: ends_with
        value: "@company.com"
    serve: true

  - name: 10% gradual rollout
    targeting:
      - attribute: user_id
        operator: percentage
        value: 10
    serve: true
```

### Flag Hierarchy

Organizations typically manage flags at multiple levels:

- **Global flags**: Affect all users (maintenance mode)
- **Application flags**: Per-application configuration
- **User flags**: Individual user preferences
- **Session flags**: Temporary state within a session

## How It Works

### Basic Implementation

```python
# Simple feature flag implementation
class FeatureFlags:
    def __init__(self, config_provider):
        self._config = config_provider

    def is_enabled(self, flag_name: str, user_id: str = None) -> bool:
        """Check if a feature flag is enabled.

        Args:
            flag_name: Name of the feature flag
            user_id: Optional user identifier for per-user targeting
        """
        return self._config.get(flag_name, default=False)

    def get_value(self, flag_name: str, default: Any = None) -> Any:
        """Get a flag's value (not just boolean)."""
        return self._config.get(flag_name, default=default)

# Usage in code
class RecommendationEngine:
    def __init__(self, flags: FeatureFlags):
        self._flags = flags

    def get_recommendations(self, user_id: str) -> list:
        if self._flags.is_enabled('new-recommendation-engine', user_id):
            return self._new_algorithm(user_id)
        return self._legacy_algorithm(user_id)

    def _legacy_algorithm(self, user_id: str) -> list:
        # Original recommendation logic
        pass

    def _new_algorithm(self, user_id: str) -> list:
        # New ML-based recommendations
        pass
```

### Flag Evaluation Flow

```
Request → Feature Flag SDK → Local Cache
                         ↓
              ┌─── Flag Config Service ───┐
              │   (evaluates rules,      │
              │    percentage splits,     │
              │    targeting)            │
              └───────────────────────────┘
                         ↓
              Return boolean/value
                         ↓
              Feature code executes or skips
```

### Gradual Rollout Implementation

```python
import hashlib

def should_enable_for_user(flag_name: str, user_id: str, percentage: float) -> bool:
    """Determine if a user falls within rollout percentage.

    Uses consistent hashing so same user always gets same result.
    """
    # Create a deterministic hash of flag name + user
    hash_input = f"{flag_name}:{user_id}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)

    # Normalize to 0-100 range
    bucket = (hash_value % 10000) / 100.0

    return bucket < percentage

# Example:
# "new-feature" for user "abc123" at 25% rollout
should_enable_for_user("new-feature", "abc123", 25.0)
```

## Practical Applications

### Continuous Deployment

Feature flags enable deploying未完成的代码:

```python
# @router.post("/orders")
# async def create_order(order: Order):
#     if flags.is_enabled('new-order-service'):
#         return await new_order_handler(order)
#     return await legacy_order_handler(order)

# Both handlers can be deployed; flag controls which executes
```

### A/B Testing

```python
def test_pricing_page():
    variant = flags.get_value('pricing-experiment', user_id, default='control')

    if variant == 'control':
        page = render_pricing_control()
    elif variant == 'variant_a':
        page = render_pricing_a()
    else:  # variant_b
        page = render_pricing_b()

    # Track which variant each user saw and their conversion
    analytics.track('pricing_page_view', {
        'user_id': user_id,
        'variant': variant,
        'session_id': session_id
    })
```

### Operational Resilience

```python
# Kill switch for critical external dependency
def call_payment_gateway(transaction):
    if not flags.is_enabled('payment-gateway'):
        raise ServiceUnavailable("Payments temporarily disabled")

    try:
        return payment_client.charge(transaction)
    except PaymentError as e:
        # Could enable fallback based on flag
        if flags.is_enabled('fallback-payment-provider'):
            return fallback_provider.charge(transaction)
        raise
```

## Examples

### LaunchDarkly SDK Integration

```python
import launchdarkly_sdk as ld

# Initialize client
client = ld.init("sdk-key-xxxxx")

# Identify user for targeting
user = {
    "key": "user-123",
    "email": "user@example.com",
    "custom": {
        "plan": "enterprise",
        "signup_date": "2024-01-15"
    }
}

# Evaluate flag with user context
show_new_dashboard = client.variation("new-dashboard", user, False)

if show_new_dashboard:
    return render_new_dashboard()
return render_legacy_dashboard()
```

### Unleash SDK Example

```python
from unleash_client import Unleash

unleash = Unleash(
    url="https://unleash.example.com/api/",
    app_name="my-app",
    instance_token="*:*"
)

# Check flag status
if unleash.is_enabled("dark-mode"):
    apply_dark_theme()
```

## Related Concepts

- [[Continuous Deployment]] — Automated deployment pipelines
- [[ab-testing]] — Comparing variants through controlled experiments
- [[Blue-Green Deployment]] — Parallel environment switching
- [[Canary Deployments]] — Gradual rollout to subset of users
- [[Dark Launching]] — Releasing to hidden users before general availability
- [[Progressive Enhancement]] — Adding features for capable clients

## Further Reading

- Martin Fowler's Feature Toggles article: https://martinfowler.com/articles/feature-toggles.html
- "Feature Flags for Dummies" — LaunchDarkly eBook
- Pete Hodgson's blog on feature flag practices
- Split.io's feature flag fundamentals documentation

## Personal Notes

Feature flags are powerful but introduce hidden costs. Every conditional branch is complexity that accumulates interest. I've seen teams ship a feature behind a flag, forget about it, and then spend weeks untangling 47 active flags when the feature finally graduated. Flag hygiene matters: establish naming conventions, require flag descriptions, set expiration reminders, and delete flags within sprint of their full rollout. Also be cautious about nesting flags—if flag A enables flag B, the interaction becomes exponentially harder to reason about. One pattern that worked for us: dedicated "flag owner" role who reviews flag health monthly and proposes cleanup sprints.
