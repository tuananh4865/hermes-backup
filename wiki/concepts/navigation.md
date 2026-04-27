---
title: "Navigation"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [navigation, ui, ux, mobile, ios]
---

# Navigation

## Overview

Navigation in UI/UX refers to the system of components and interactions that allow users to move through an application, access different screens or content, and accomplish their goals efficiently. Good navigation is fundamental to user experience—it determines how intuitively users can find information, how oriented they feel within the app, and ultimately whether they complete tasks or abandon the product. Navigation design must balance accessibility with visual cleanliness, ensuring users always know where they are and how to get where they want to go without overwhelming the interface with controls.

## Patterns

### Tab Bar

Tab bars present a horizontal row of icons with optional labels at the bottom (iOS) or top (Android/web) of the screen. They provide persistent access to four to five primary destinations, making them ideal for apps with a limited number of top-level sections. Tab bars remain visible during scrolling and throughout the app session, offering constant wayfinding cues. iOS Human Interface Guidelines recommend tab bars for apps with three to five main sections.

### Navigation Drawer

Also known as hamburger menus or side menus, navigation drawers slide in from the left edge and contain navigation links to secondary screens or less-frequently accessed sections. While once ubiquitous, drawers have fallen out of favor on mobile due to hidden navigation costs—they require two taps instead of one for primary destinations. Drawers remain common in tablet layouts and certain productivity apps where screen space allows side-by-side content.

### Stack Navigation

Stack-based navigation (hierarchical or drill-down) presents one screen at a time with a back button to return to the previous level. This pattern creates a clear linear path through content and works well for workflows like wizards, checkout processes, or content organized in categories. Mobile operating systems typically provide system-level back gestures, making stack navigation feel natural and consistent.

### Modal

Modals (also called dialogs or sheets) overlay the current screen to present focused tasks, confirmations, or quick input without fully leaving context. iOS presents modals as sheets that slide up from the bottom, while Android uses full-screen dialogs or bottom sheets. Modals interrupt the user's flow, so they should be reserved for actions that are temporary, secondary, or require quick completion before returning to the main task.

## Best Practices

- **Provide clear wayfinding**: Users should always know their current location within the app hierarchy. Use breadcrumbs, highlighted active states, or breadcrumb trails to communicate position.

- **Limit primary destinations**: Aim for three to five top-level items in navigation to reduce cognitive load. Group related items or use progressive disclosure for smaller features.

- **Make touch targets accessible**: Navigation elements should be at least 44x44 points on iOS and 48x48dp on Android to ensure comfortable tapping.

- **Support system navigation**: Respect platform conventions like iOS swipe-back gestures and Android system back buttons rather than overriding them inconsistently.

- **Use familiar patterns**: Stick to established conventions for each platform. Users transfer expectations from other apps—deviating requires clear justification.

- **Ensure escape routes**: Every screen should have a clear path back to the main navigation without requiring the user to restart the app or lose progress.

## Related

- [[user-experience]]
- [[mobile-design]]
- [[ios-design-guidelines]]
- [[information-architecture]]
- [[interaction-design]]
