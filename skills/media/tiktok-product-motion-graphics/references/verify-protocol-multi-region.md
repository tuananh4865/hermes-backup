# ⚠️ CRITICAL: READ `references/motion-static-video-pitfall.md` BEFORE FINAL COMPOSITE

**This is the #1 most expensive failure mode in this skill (cost: 3 clip rebuilds + user frustration).** HyperFrames does NOT play HTML `<video>` in headless render — if you don't follow the 3-step fix (display:none bg-video-wrap + `--format mov` + ffmpeg yuva420p overlay), the final clip ships **statically frozen** while looking visually plausible. Diagnostic recipe + fix code are in that reference. **Do not ship without running the multi-region pixel diff check (face/chin/hand, threshold >100).**
