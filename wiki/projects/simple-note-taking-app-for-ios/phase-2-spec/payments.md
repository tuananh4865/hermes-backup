---
title: "Payments: simple-note-taking-app-for-ios"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [auto-filled]
---

# Payments: simple-note-taking-app-for-ios

## Revenue Model

**Type**: Subscription (freemium model)

### Tier Structure

| Tier | Price (USD) | Features |
|------|-------------|----------|
| Free | $0 | Basic features, limited usage |
| Premium Monthly | $4.99/mo | Full features |
| Premium Yearly | $29.99/yr | Full features, 50% off |

### Subscription Group
- Group ID: group.com.[bundle-id].subscription
- Product IDs:
  - com.[bundle-id].premium.monthly
  - com.[bundle-id].premium.yearly

## StoreKit 2 Integration

### Implementation Checklist

- [ ] Create subscription products in App Store Connect
- [ ] Add StoreKit configuration file (StoreKit.storekit)
- [ ] Implement `Product` enumeration
- [ ] Implement `StoreKitManager` (singleton)
- [ ] Add purchase flow with proper error handling
- [ ] Implement `Transaction` verification
- [ ] Handle subscription status changes
- [ ] Implement restore purchases
- [ ] Add paywall view with proper sizing
- [ ] Test with StoreKit in Xcode

### StoreKitManager API

```swift
class StoreKitManager: ObservableObject {
    @Published var products: [Product] = []
    @Published var purchasedProductIDs: Set<String> = []
    @Published var subscriptionStatus: SubscriptionStatus = .none
    
    func loadProducts() async
    func purchase(_ product: Product) async throws -> Transaction
    func restorePurchases() async
    func isPurchased(_ productID: String) -> Bool
}
```

### Paywall Design Guidelines

1. **Clear value proposition** at top
2. **3-tier display**: Free / Monthly / Yearly
3. **Yearly highlight**: "Best Value" badge, show savings
4. **CTA button**: "Start Free Trial" or "Subscribe"
5. **Legal links**: Terms, Privacy, Restore Purchases
6. **Safe area respect**: iPhone X+ notch handling

## Revenue Targets

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Downloads | 1,000 | 5,000 | 15,000 |
| DAU | 200 | 1,500 | 5,000 |
| Conversion | 2% | 3% | 4% |
| MRR | $100 | $450 | $3,000 |

