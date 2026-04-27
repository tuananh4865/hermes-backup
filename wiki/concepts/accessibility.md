---
title: Accessibility
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [accessibility, a11y, wcag, assistive-technology, inclusive-design, ui, ux]
---

# Accessibility

## Overview

Accessibility (often abbreviated as "a11y") is the practice of designing and building products, services, and environments so that they can be used by people with disabilities — including visual, auditory, motor, cognitive, and speech impairments. In the context of software and web development, accessibility specifically refers to ensuring that applications and websites are usable by the roughly 1 billion people worldwide with disabilities, including those who rely on assistive technologies like screen readers, keyboard navigation, or voice control.

Accessibility is not a niche concern — it intersects with every aspect of [[User Experience Design]]. Beyond the ethical imperative, accessibility is often legally mandated (Section 508 in the US, EN 301 549 in the EU, ADA lawsuits are increasingly common). Accessible design also frequently improves usability for everyone — curb cuts benefit wheelchair users but also parents with strollers and travelers with luggage; captions help deaf users but also people watching video in noisy environments.

## Key Concepts

**WCAG (Web Content Accessibility Guidelines):** The international standard for web accessibility, published by W3C. WCAG organizes accessibility requirements into four principles (POUR):

- **Perceivable:** Information must be presentable in ways users can perceive (e.g., alt text for images, captions for video, sufficient color contrast)
- **Operable:** Interface components must be operable (e.g., keyboard accessible, enough time to read content, no seizure-inducing flashes)
- **Understandable:** Information and UI operation must be understandable (e.g., readable text, predictable navigation, input assistance)
- **Robust:** Content must be robust enough for a wide variety of assistive technologies to interpret (e.g., valid HTML, proper ARIA usage)

WCAG conformance levels: A (minimum), AA (standard target for most organizations), AAA (highest, not always achievable for all content types).

**Assistive Technologies:** Tools that people with disabilities use to access digital content:
- **Screen readers:** NVDA, JAWS, VoiceOver — parse page structure and read content aloud; critical for blind users
- **Screen magnification:** ZoomText, built-in OS magnifiers — enlarge portions of the screen
- **Voice control:** Dragon NaturallySpeaking, native OS voice control — navigate and interact via voice commands
- **Switch access:** For users with severe motor impairments; single-switch navigation through page elements
- **Alternative input devices:** Eye trackers, head pointers, foot pedals

**Semantic HTML:** The foundation of web accessibility. Using the correct HTML element for the job (`<button>` for buttons, `<nav>` for navigation regions, `<h1>`-`<h6>` for headings) allows assistive technologies to properly convey structure. Custom-built interactive elements that don't use semantic HTML require extensive ARIA workarounds.

**ARIA (Accessible Rich Internet Applications):** A set of attributes that augment native HTML semantics to communicate widget roles, states, and properties to assistive technologies. ARIA is essential for custom interactive components (complex dropdowns, modals, sliders) but should never be used to fix missing semantic HTML — always prefer native elements first.

## How It Works

Accessibility implementation happens at multiple levels:

1. **Design level:** Color contrast checking, text sizing, clear focus indicators, logical information hierarchy, touch target sizing (minimum 44x44 CSS pixels for mobile)
2. **Development level:** Semantic HTML, keyboard navigation, ARIA attributes, form labels, alt text, caption tracks
3. **Testing level:** Automated testing catches ~30% of issues; manual testing with real assistive technologies is essential; user testing with disabled users provides the most valuable feedback

```html
<!-- Accessible button example: semantic HTML + ARIA for state -->
<!-- Native <button> is automatically keyboard-focusable and announces state -->

<!-- This button has a tooltip via ARIA -->
<button
  aria-describedby="delete-tooltip"
  aria-pressed="false"
  class="btn-icon"
  type="button">
  <svg aria-hidden="true" focusable="false">
    <use href="#icon-trash"/>
  </svg>
  <span class="sr-only">Delete item</span>
</button>
<span id="delete-tooltip" class="tooltip">Hold for 2 seconds to delete</span>
```

```css
/* Accessible focus indicator - never remove this without replacement */
*:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* Sufficient color contrast (WCAG AA requires 4.5:1 for normal text) */
.high-contrast-text {
  color: #1a1a1a;        /* on #ffffff background = 16:1 contrast */
  background-color: #fff;
}
```

## Practical Applications

- **Screen reader optimization:** Adding alt text to images, labeling form inputs, marking decorative elements as presentational, structuring content with proper heading hierarchy
- **Keyboard navigation:** Ensuring all interactive elements are reachable and operable via Tab, Shift+Tab, Enter, Space, and arrow keys
- **Video accessibility:** Adding closed captions, audio descriptions, and transcripts for deaf or hard-of-hearing users
- **Cognitive accessibility:** Simplifying language, providing clear instructions, avoiding time-pressure interactions
- **Mobile accessibility:** Touch target sizing, avoiding hover-only interactions, supporting pinch-to-zoom

## Examples

- **WAVE Web Accessibility Evaluator:** Browser extension that visually highlights accessibility issues on any web page
- **axe DevTools:** Industry-standard accessibility testing engine integrated into browser dev tools
- **VoiceOver on macOS/iOS:** Native screen reader; every Apple product is accessibility-tested extensively
- **Inclusive Components (GitHub):** Design pattern library showing accessible implementations of common UI components
- **GOV.UK Accessibility Blog:** Excellent real-world examples of accessibility improvements on government services

## Related Concepts

- [[WCAG]] — Web Content Accessibility Guidelines, the standard for web accessibility
- [[Assistive Technology]] — Tools like screen readers and voice control used by people with disabilities
- [[Screen Reader]] — The most common assistive technology for blind users
- [[ARIA]] — Accessible Rich Internet Applications spec for custom accessible widgets
- [[User Experience Design]] — Broader discipline that accessibility is a part of
- [[Design Systems]] — Accessibility should be built into design systems from the start
- [[User Testing]] — Testing with disabled users is essential for real-world accessibility

## Further Reading

- WCAG 2.2 Specification: https://www.w3.org/TR/WCAG22/
- WebAIM (Web Accessibility In Mind): https://webaim.org/
- A11Y Project Checklist: https://www.a11yproject.com/checklist/
- Inclusive Components by Hidde de Vries: https://inclusive-components.design/

## Personal Notes

The most common mistake I see is treating accessibility as a checklist to complete before launch rather than a continuous practice. Accessibility debt accumulates fast — retrofitting an inaccessible application is always more expensive than building it right from the start. The second most common mistake is relying solely on automated tools. Tools like axe catch syntax issues (missing alt text, insufficient contrast, unlabeled form controls) but can't evaluate whether an experience actually makes sense when navigated by screen reader or keyboard alone. Automated testing catches ~30% of issues; the rest requires human testing and ideally testing with actual disabled users. Also worth noting: accessibility and [[Internationalization]] often conflict — translated content can be 300% longer than the English source, breaking fixed layouts; plan for this.
