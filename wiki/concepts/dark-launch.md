---
title: "Dark Launch"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [dark-launch, feature-deployment, release-management, devops, progressive-delivery, production-testing]
---

# Dark Launch

## Overview

Dark launch is a deployment technique where new software code is deployed to production environments but the new functionality is not visibly activated or exposed to users. The code exists in the production system, receives real production traffic, and operates correctly—but users continue experiencing the existing behavior without any indication that changes are occurring beneath the surface. The term "dark" refers to this hidden quality: the launch happens without fanfare, announcement, or visible change to the user experience. This approach allows teams to validate that new code performs correctly under authentic production conditions before making the feature visible, catching issues that only emerge with real traffic patterns that cannot be replicated in staging environments.

The practice emerged from the recognition that production environments contain a complexity and dynamism that no pre-production testing environment can fully capture. Real user traffic exhibits patterns—time-of-day fluctuations, geographic distributions, device diversity, interaction sequences—that are impossible to simulate accurately. Additionally, production systems have real dependencies on external services, databases, and caching layers that may behave differently when under genuine load versus synthetic load. Dark launching addresses these gaps by using production itself as a testing environment, but does so in a way that isolates the experimental code path from user-visible behavior until validation is complete.

Dark launch is closely related to [[feature toggles]], which provide the mechanism for controlling feature visibility independently of code deployment. While feature toggles are a general-purpose mechanism for managing feature state, dark launch is a specific pattern that uses toggles or similar mechanisms to achieve a controlled, invisible-to-users production validation phase. The pattern is a precursor to [[canary releases]], which share the philosophy of incremental exposure but differ in that canary releases do expose the new version to a small visible user group. Dark launch keeps the new version completely invisible until the team is confident it should proceed to visible rollout.

## Key Concepts

**Silent Production Validation** is the core value proposition of dark launch. By deploying code to production and routing real user traffic through it (in a dark capacity), teams can verify that the new code path handles production load, integrates correctly with dependencies, and doesn't introduce unexpected interactions with existing system components. This validation catches a category of issues that are fundamentally unobservable without production traffic: race conditions under concurrent load, memory leaks that only manifest over extended runtime, database query plans that perform differently at scale, and integration issues with third-party services that throttle or behave differently under real versus synthetic load.

**Traffic Duplication** or "shadow mode" is a variation where the dark launch code receives a copy of production requests alongside the existing system, but its responses are discarded. The dark code executes fully—hitting databases, calling downstream services, processing data—but the results don't affect users. This approach provides maximum production validation coverage because every request is passed through the new code, not just requests for users who have been selectively routed. Traffic duplication is more resource-intensive but catches issues that might only manifest on specific request types that wouldn't be captured by sampling.

**Blast Radius Minimization** is achieved through the dark launch mechanism itself— because users don't see the new code's behavior, any issues it encounters are invisible to users and can be addressed without user impact. However, careful consideration must be given to side effects: dark launch code that writes to databases, sends emails, or triggers notifications requires additional safeguards to prevent real-world consequences from experimental code paths. The principle is that dark launch should be read-heavy or have side effects carefully sandboxed; code that changes persistent state requires additional controls.

**Gradual Transition** is the natural follow-on to dark launch. Once the team has validated that the dark launch code performs correctly, the transition to visible release proceeds incrementally—perhaps first to internal users (a form of [[canary release]]), then to a small percentage of external users, then to full availability. This progression ensures that each stage of visibility is preceded by validation in the less visible stage, building confidence incrementally rather than making a big-bang transition from invisible to universal.

## How It Works

Dark launch implementation typically uses a configuration-driven approach where feature visibility is controlled separately from code deployment:

```python
# Dark launch pattern using feature flags
from dark_launch import DarkLaunch

# Initialize with flag configuration
dl = DarkLaunch(
    flags={
        'new_payment_flow': {
            'enabled': False,           # Dark: not visible to users
            'shadow_mode': True,        # Still execute, discard results
            'rollout_percentage': 0     # 0% visible rollout
        },
        'recommendation_v2': {
            'enabled': True,            # Production validated, keep dark
            'shadow_mode': True,
            'rollout_percentage': 0
        }
    }
)

def process_payment(order_id: str, user_id: str, payment_method: str):
    # Dark launch wrapper executes new code in shadow mode
    result = dl.execute('new_payment_flow', 
                        lambda: _process_payment_v2(order_id, user_id, payment_method),
                        default=_process_payment_legacy(order_id, user_id, payment_method))
    
    # User always sees legacy result until visible rollout
    return result.output if result.was_visible else result.fallback
```

The infrastructure supporting dark launch includes deployment automation that pushes code to production as part of normal CI/CD pipelines, flag configuration systems that control visibility independently of deployment, and monitoring systems that compare dark code behavior against baseline without affecting user-visible metrics. The key insight is that deployment and visibility are two independent decisions made at different times by different mechanisms—deployment happens through the standard pipeline, visibility happens through configuration changes.

Monitoring during dark launch focuses on operational metrics that don't depend on user-visible behavior: response times, error rates, resource utilization, and log patterns. The team establishes baseline metrics for these operational indicators during the dark launch period and monitors for regressions. If the dark code begins exhibiting degraded performance or elevated errors, the configuration can be adjusted to route traffic back to the existing code path entirely, with no user impact because users never saw the dark code's output.

## Practical Applications

**Database Migration Validation** is a particularly valuable use case for dark launch. Schema changes to production databases carry inherent risk—changing column types, adding indexes, or partitioning tables can lock databases or degrade performance in ways that are impossible to fully predict without production load. A dark launch approach deploys the new schema alongside the existing one, with code that writes to both schemas during the dark period. This validates that the application correctly handles the new schema while users continue using the old schema, until the team is confident the migration is safe to complete.

**Dependency Upgrade Testing** allows teams to validate library, framework, or service upgrades in production before committing to them visibly. A team upgrading their message queue library from version 3 to version 4 can deploy the upgrade to production with the new library in dark mode, routing a percentage of message processing through the new library while the old library continues serving users. Any incompatibilities, performance regressions, or behavioral differences surface during the dark period and can be addressed before users are affected.

**Architecture Migration** supports gradual movement from legacy systems to modern implementations. Rather than a risky cutover where traffic is redirected from old to new, dark launch allows the new system to run in parallel, processing real requests in shadow mode. The team can compare outputs between old and new systems, verify that the new system handles the same inputs correctly, and identify any edge cases where behavior diverges. Only after thorough validation does traffic begin shifting to the new system.

## Examples

A social media platform deploying a new recommendation algorithm uses dark launch to validate that the new algorithm produces comparable quality outputs to the existing algorithm. During the dark period, the new algorithm processes every feed generation request but its output is compared against the legacy algorithm's output offline. The team discovers that the new algorithm produces significantly different recommendations for users with fewer than 10 connections—these users were a small fraction of total traffic but represented the majority of the divergence. The team adjusts the algorithm to handle low-connectivity users differently and continues the dark period for another week to validate the fix. Only after the recommendation quality metrics converge do they proceed to canary rollout.

A logistics company migrating from a legacy route optimization system to a new ML-based system uses dark launch to validate that the new system produces feasible routes. The new system processes all route requests in shadow mode while the legacy system continues generating the routes that drivers actually follow. After each route generation, the systems compare their outputs— if the new system produces a route more than 20% longer than the legacy system, that case is flagged for analysis. Over two weeks of dark launch, the team identifies and addresses 47 edge cases where the new system produces suboptimal routes, and confirms that the new system produces better routes for 73% of cases, improving expected delivery times.

## Related Concepts

- [[Feature Toggles]] - The primary mechanism used to implement dark launch patterns
- [[Canary Releases]] - A closely related progressive delivery pattern that differs by exposing changes to a small visible user group
- [[Progressive Delivery]] - The broader discipline that encompasses dark launch, canary releases, and feature toggles
- [[Continuous Delivery]] - Software delivery practice that dark launch enables by allowing deployment without visible release
- [[Blue-Green Deployment]] - Deployment strategy using two environments, sometimes combined with dark launch concepts
- [[Chaos Engineering]] - Uses similar philosophy of controlled experimentation in production but focuses on failure modes rather than feature validation

## Further Reading

- [Facebook's Dark Launch Practices](https://www.facebook.com/notes/) — Early practitioner of production validation techniques
- [Martin Fowler on Dark Launch](https://martinfowler.com/) — Feature flag patterns including dark launch
- [Google's Site Reliability Engineering](https://sre.google/sre-book/production/) — Production testing practices in SRE context

## Personal Notes

Dark launch represents a mature understanding that production is the only true test environment. The investment in building dark launch capability—robust flag systems, traffic duplication infrastructure, comparative monitoring— pays dividends far beyond the initial use case. Every significant production change becomes safer when you have a mechanism to validate it invisibly first. The discipline also has cultural benefits: it reduces the anxiety around production deployments because rollback is instantaneous (just disable the flag) and impact is zero (users never saw the change). Teams that adopt dark launch often find that their deployment frequency increases while their incident rate decreases—validation through production experimentation is simply more effective than validation through pre-production testing alone.
