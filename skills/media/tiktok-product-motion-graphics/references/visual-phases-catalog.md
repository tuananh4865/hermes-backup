# Visual Phases Catalog — 8-phase animation snippets

Each phase has 3 animation techniques to mix. Pick the right one per content type.

## Phase 1: HOOK pulse text (0–2s)

```javascript
// Big yellow scale pulse
tl.fromTo(hook,
  { opacity: 0, scale: 0.5 },
  { opacity: 1, scale: 1.1, duration: 0.3, ease: "back.out(2)" },
  0
);
tl.to(hook, { scale: 1, duration: 0.2 }, 0.4);
tl.to(hook, { opacity: 0, scale: 0.8, duration: 0.3 }, 1.7);
```

Alternative — Slide from top:
```javascript
tl.fromTo(hook, { opacity: 0, y: -200 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0);
tl.to(hook, { opacity: 0, y: 100, duration: 0.4 }, 1.7);
```

## Phase 2: PROBLEM text (2–7s)

```javascript
// Container + typewriter on highlight
tl.fromTo(problem, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }, 2.3);
tl.fromTo(".problem-highlight",
  { clipPath: "inset(0 100% 0 0)" },
  { clipPath: "inset(0 0% 0 0)", duration: 1.2, ease: "power1.inOut" },
  3.0
);
tl.to(problem, { opacity: 0, y: -30, duration: 0.4 }, 6.8);
```

Alternative — Stagger lines:
```javascript
tl.fromTo(".problem-eyebrow", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3 }, 2.3);
tl.fromTo(".problem-highlight", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.5)" }, 2.6);
tl.fromTo(".problem-sub", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4 }, 3.2);
tl.to(problem, { opacity: 0, duration: 0.5 }, 6.5);
```

## Phase 3: BAR CHART (7–13s)

```javascript
// Show PIP (talking head left half)
tl.fromTo(pip, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power2.out" }, 7.3);

// Show chart card from right
tl.fromTo(barChart,
  { opacity: 0, x: 100, scale: 0.9 },
  { opacity: 1, x: 0, scale: 1, duration: 0.5, ease: "back.out(1.2)" },
  7.5
);

// Bar OLD grows to 100%
tl.to(barOld, { width: "100%", duration: 2.5, ease: "power1.inOut" }, 8.0);

// Bar NEW grows to 16% (proportional)
tl.to(barNew, { width: "16%", duration: 2.5, ease: "power1.inOut" }, 9.0);

// Hide chart + PIP
tl.to(barChart, { opacity: 0, x: 60, duration: 0.4 }, 12.8);
tl.to(pip, { opacity: 0, duration: 0.3 }, 12.9);
```

Alternative — Pie chart rotation:
```javascript
tl.fromTo(pieChart, { opacity: 0, rotation: -180 }, { opacity: 1, rotation: 0, duration: 0.6, ease: "back.out(1.5)" }, 7.3);
tl.to(pieFill, { strokeDasharray: [0, 502], duration: 2.5, ease: "power1.inOut" }, 8.0);
```

## Phase 4: STAMP (13–17s)

```javascript
// Pop in with rotation + bounce
tl.fromTo(stamp,
  { opacity: 0, scale: 2, rotation: 15 },
  { opacity: 1, scale: 1, rotation: -15, duration: 0.4, ease: "back.out(1.5)" },
  13.3
);
// Bounce wobble
tl.to(stamp, { scale: 1.1, rotation: -10, duration: 0.15, yoyo: true, repeat: 1 }, 14.5);
tl.to(stamp, { opacity: 0, scale: 0.7, duration: 0.3 }, 16.4);
```

## Phase 5: PRODUCT CARD (17–19s)

```javascript
// iOS 26 glass slide from right
tl.fromTo(productCard,
  { opacity: 0, x: 200 },
  { opacity: 1, x: 0, duration: 0.6, ease: "back.out(1.2)" },
  17.0
);
tl.to(productCard, { opacity: 0, x: 100, duration: 0.4 }, 18.6);
```

Alternative — Card swap in-place:
```javascript
tl.fromTo(productCard,
  { opacity: 0, scale: 0.6, rotation: -15 },
  { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.7)" },
  17.0
);
```

## Phase 6: iPhone MOCKUP (19–28s)

```javascript
// Show PIP again (chart mockup needs face left)
tl.fromTo(pip, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.5 }, 18.9);

// Slide iPhone from right with bounce
tl.fromTo(iphoneMock,
  { opacity: 0, x: 100, scale: 0.85 },
  { opacity: 1, x: 0, scale: 1, duration: 0.6, ease: "back.out(1.2)" },
  19.5
);

// iPhone wobble (rotate to simulate handheld)
tl.to(".iphone-frame", { rotation: -3, duration: 0.3 }, 22.0);
tl.to(".iphone-frame", { rotation: 3, duration: 0.3 }, 22.5);
tl.to(".iphone-frame", { rotation: 0, duration: 0.3 }, 23.0);

// Charger bolt flash (pulse to indicate "charging")
tl.fromTo(".charger-attached",
  { scale: 1 },
  { scale: 1.2, duration: 0.15, yoyo: true, repeat: 5 },
  23.5
);

// Hide
tl.to(iphoneMock, { opacity: 0, x: 50, duration: 0.4 }, 27.3);
tl.to(pip, { opacity: 0, duration: 0.3 }, 27.4);
```

## Phase 7: USP LIST (27.8–30s)

```javascript
// Container visible
tl.fromTo(uspList, { opacity: 0 }, { opacity: 1, duration: 0.3 }, 27.8);

// Stagger 4 bullets, each delayed 0.5s
tl.fromTo(usp1, { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.5)" }, 27.9);
tl.fromTo(usp2, { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.5)" }, 28.4);
tl.fromTo(usp3, { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.5)" }, 28.9);
tl.fromTo(usp4, { opacity: 0, x: 80 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(1.5)" }, 29.4);
```

Alternative — Slide up from bottom:
```javascript
tl.fromTo(usp1, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.5)" }, 27.9);
tl.fromTo(usp2, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.5)" }, 28.3);
tl.fromTo(usp3, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.5)" }, 28.7);
tl.fromTo(usp4, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.5)" }, 29.1);
```

## Phase 8: CTA (29.8–32s)

```javascript
tl.fromTo(cta,
  { opacity: 0, y: 80, scale: 0.8 },
  { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.5)" },
  29.8
);
```

Alternative — Heartbeat pulse:
```javascript
tl.fromTo(ctaButton, { scale: 1 }, { scale: 1.05, duration: 0.4, yoyo: true, repeat: 3 }, 30.5);
```

## Watermark (always on after 0.3s)

```javascript
tl.fromTo(watermark, { opacity: 0 }, { opacity: 0.85, duration: 0.4 }, 0.3);
```

## Audio sync (window.__seekTo)

```javascript
function syncVideo(timeSec) {
  videos.forEach(v => {
    if (v.duration > 0) v.currentTime = Math.min(timeSec, v.duration);
  });
}

function seekTo(timeSec) {
  tl.seek(timeSec);
  syncVideo(timeSec);
}

window.__seekTo = seekTo;
window.__compositionReady = true;
window.__timelines = window.__timelines || {};
window.__timelines[COMPOSITION_ID] = tl;
tl.seek(0);
```
