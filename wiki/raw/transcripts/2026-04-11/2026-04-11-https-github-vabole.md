---
title: "Https Github Vabole - 2026-04-11"
date: 2026-04-11
type: transcript
tags: [github, git]
sources: [raw/transcripts/2026-04-11-https-github-vabole.md]
---

[[github]] [[transcript-system]]

# Https Github Vabole - 2026-04-11

[2026-04-11 17:48:59] 👤 Anh: https://github.com/vabole/apple-skills

Cài skill này
[2026-04-11 17:48:59] 💬 tool: {"error": "Error extracting content: Client error '432 ' for url 'https://api.tavily.com/extract'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/432"}
[2026-04-11 17:48:59] 🤖 Em: [CONTEXT COMPACTION] Earlier turns in this conversation were compacted to save context space. The summary below describes work that was already completed, and the current session state may still reflect that work (for example, files may already be changed). Use the summary and the current state to continue from where things left off, and avoid repeating work:
Summary generation was unavailable. 317 conversation turns were removed to free context space but could not be summarized. The removed turns contained earlier work in this session. Continue based on the recent messages below and the current state of any files or resources.
[2026-04-11 17:48:59] 👤 Anh: model chính vẫn là minimax 2.7 còn fall back là local model thôi chứ
[2026-04-11 17:48:59] 🤖 Em: ⚠️ Error code: 400
[2026-04-11 17:48:59] 👤 Anh: alo
[2026-04-11 17:48:59] 🤖 Em: Ừ, đợi đã — để tôi cài skill đó trực tiếp từ repo.

[2026-04-11 17:48:59] 💬 tool: {"output": "fatal: destination path 'apple-skills' already exists and is not an empty directory.", "exit_code": 128, "error": null}
[2026-04-11 17:48:59] 🤖 Em: Đã có thư mục `apple-skills` rồi. Kiểm tra xem nội dung đúng chưa:

[2026-04-11 17:48:59] 💬 tool: {"output": "total 184\ndrwxr-xr-x  19 tuananh4865  staff    608 Apr 11 13:52 .\ndrwxr-xr-x  99 tuananh4865  staff   3168 Apr 11 14:46 ..\ndrwxr-xr-x   4 tuananh4865  staff    128 Apr 11 13:52 .claude-plugin\ndrwxr-xr-x  12 tuananh4865  staff    384 Apr 11 13:52 .git\ndrwxr-xr-x   3 tuananh4865  staff     96 Apr 11 13:52 .github\n-rw-r--r--   1 tuananh4865  staff     14 Apr 11 13:52 .gitignore\n-rw-r--r--   1 tuananh4865  staff   5020 Apr 11 13:52 AGENTS.md\n-rw-r--r--   1 tuananh4865  staff   1772 Apr 11 13:52 CHANGELOG.md\n-rw-r--r--   1 tuananh4865  staff   1072 Apr 11 13:52 LICENSE\n-rw-r--r--   1 tuananh4865  staff   5133 Apr 11 13:52 MAINTAINING.md\n-rw-r--r--   1 tuananh4865  staff   4584 Apr 11 13:52 README.md\n-rw-r--r--   1 tuananh4865  staff   1222 Apr 11 13:52 biome.json\n-rw-r--r--   1 tuananh4865  staff    804 Apr 11 13:52 package.json\n-rw-r--r--   1 tuananh4865  staff  38266 Apr 11 13:52 pnpm-lock.yaml\ndrwxr-xr-x   6 tuananh4865  staff    192 Apr 11 13:52 scripts\ndrwxr-xr-x  34 tuananh4865  staff   1088 Apr 11 13:52 skills\ndrwxr-xr-x   3 tuananh4865  staff     96 Apr 11 13:52 tests\n-rw-r--r--   1 tuananh4865  staff    546 Apr 11 13:52 tsconfig.json\n-rw-r--r--   1 tuananh4865  staff    156 Apr 11 13:52 vitest.config.ts", "exit_code": 0, "error": null}

[Subdirectory context discovered: .hermes/skills/apple-skills/AGENTS.md]
# Apple Skills Maintainer Guide

This file is for agents maintaining this repository. It is not end-user documentation, and it is not the runtime instruction file for agents that install these skills into Claude Code, Codex, Cursor, or another coding agent.

## Table of Contents

| Need | Start Here | Notes |
|------|------------|-------|
| Explain the project to humans | `README.md` | Keep it brief, friendly, and installation-focused. Put copy-pasteable user commands here, not maintainer runbooks. |
| Understand install surfaces | `README.md` and `.claude-plugin/` | Claude Code installs via the plugin marketplace; Codex and Cursor use the Skills CLI to copy `skills/` entries into agent skill directories. |
| Maintain generated Apple docs | `MAINTAINING.md` | Refresh workflow, DocC rendering details, tooling, and repo structure live there. |
| Update skill behavior | `skills/<name>/SKILL.md` | These are the installed agent-facing instructions for a specific skill. Edit them deliberately; they are consumed by downstream agents. |
| Update generated reference docs | `skills/<name>/*.md` | Use the generated-vs-hand-authored rules below. Prefer refresh tooling over hand edits for generated files. |
| Work on doc rendering tooling | `scripts/apple-docs.ts` and `scripts/apple-docs/` | TypeScript tooling fetches Apple's DocC JSON and renders markdown. |
| Run checks | `package.json` | Use `pnpm check` for the full gate; individual commands are listed in `MAINTAINING.md`. |
| Validate install commands | `README.md` install blocks | Test in a temporary `HOME`/`XDG_CONFIG_HOME` so real agent configs are not modified. |
| Publish Claude Code plugin metadata | `.claude-plugin/` | Marketplace/plugin metadata for Claude Code lives here. |

## Generated vs Hand-Authored Files

Do not classify an entire skill directory as generated or hand-authored. A single `skills/<name>/` directory can contain both.

| Pattern | Ownership | How to Change |
|---------|-----------|---------------|
| `skills/**/SKILL.md` | Hand-authored | Edit directly when changing installed skill instructions. |
| `skills/**/*.md` with YAML frontmatter containing `source: https://developer.apple.com/...` | Generated from Apple's DocC JSON | Regenerate with the tooling in `MAINTAINING.md`; avoid hand edits except to repair the generator or unblock a refresh. |
| `skills/**/*.videos.md` | Generated sidecar for Apple DocC video references | Regenerate with the docs refresh flow; keep sidecar behavior generic. |
| `skills/**/references/**`, `skills/**/docs/**`, `skills/**/assets/**`, `skills/**/scripts/**`, `skills/**/agents/**` | Hand-authored unless the file itself has generated frontmatter | Edit directly, preserving local guide or asset conventions. |
| Root docs such as `README.md`, `MAINTAINING.md`, `AGENTS.md`, and `CHANGELOG.md` | Hand-authored | Edit directly for human or maintainer documentation. |
| `scripts/**`, `tests/**`, `package.json`, `biome.json`, `tsconfig.json` | Hand-authored tooling | Edit directly and run the relevant checks. |
| Generated-looking failure output or stale fetched content | Generated artifact to fix at the source | Do not polish it manually; refresh, remove, or fix the generator/source mapping. |

If a file does not match a generated pattern, treat it as hand-authored until `MAINTAINING.md` or the file itself says otherwise. Keep rules pattern-based so adding or removing skills does not require updating this file.

## Repository Roles

| File or Directory | Audience | Purpose |
|-------------------|----------|---------|
| `README.md` | Human users | What this repo is and how to install, update, or uninstall the skills. |
| `AGENTS.md` | Repo-maintainer agents | Navigation and boundaries for working in this repository. |
| `MAINTAINING.md` | Human and agent maintainers | Detailed maintainer runbooks and generated-doc workflow. |
| `skills/<name>/SKILL.md` | Downstream coding agents | Instructions loaded after a skill is installed. |
| `skills/<name>/*.md` | Downstream coding agents | Reference material used by installed skills. |
| `scripts/` | Repo maintainers | Fetching, rendering, and refresh automation. |
| `tests/` | Repo maintainers | Renderer smoke tests and regression coverage. |

## Maintainer Boundaries

- Do not turn `README.md` into a script or maintainer log. It should help a human quickly understand and install Apple Skills.
- Do not treat this repository's `skills/*/SKILL.md` files as instructions for your current maintainer task unless you are specifically editing or validating that skill.
- Do not hand-edit generated reference files when the refresh tooling can produce the change; fix the generator or source mapping instead.
- Keep maintainer details in `MAINTAINING.md`; keep this file as a navigation layer.
- Keep skill guidance generic. Do not list every current skill here when a `skills/<name>/...` pattern communicates the rule.
- When testing installs, use isolated temporary directories for `HOME` and `XDG_CONFIG_HOME`.
[2026-04-11 17:48:59] 🤖 Em: Repo đã clone sẵn rồi. Để xem hướng dẫn cài đặt:

[2026-04-11 17:48:59] 💬 tool: {"content": "     1|# Apple Skills\n     2|\n     3|Apple development skills for **Claude Code**, **Codex**, and other coding agents — current iOS 26+ APIs, SwiftUI, UIKit, Liquid Glass, Human Interface Guidelines, and practical workflow guides.\n     4|\n     5|## Install\n     6|\n     7|Pick your agent:\n     8|\n     9|<details open>\n    10|<summary>Claude Code</summary>\n    11|\n    12|```bash\n    13|claude plugin marketplace add vabole/apple-skills\n    14|claude plugin install apple-skills@apple-skills\n    15|```\n    16|\n    17|</details>\n    18|\n    19|<details>\n    20|<summary>Codex</summary>\n    21|\n    22|```bash\n    23|npx skills add vabole/apple-skills --agent codex --skill '*' -g -y\n    24|```\n    25|\n    26|</details>\n    27|\n    28|<details>\n    29|<summary>Cursor</summary>\n    30|\n    31|```bash\n    32|npx skills add vabole/apple-skills --agent cursor --skill '*' -g -y\n    33|```\n    34|\n    35|</details>\n    36|\n    37|## Update\n    38|\n    39|For Claude Code marketplace installs:\n    40|\n    41|```bash\n    42|claude plugin update apple-skills@apple-skills\n    43|```\n    44|\n    45|For Codex or Cursor, re-run the install command for your agent.\n    46|\n    47|## Uninstall\n    48|\n    49|For Claude Code marketplace installs:\n    50|\n    51|```bash\n    52|claude plugin uninstall apple-skills@apple-skills\n    53|```\n    54|\n    55|For Skills CLI installs, run the remover and select the Apple Skills entries:\n    56|\n    57|```bash\n    58|npx skills remove -g\n    59|```\n    60|\n    61|## What's Included\n    62|\n    63|### Framework Reference Docs\n    64|\n    65|| Skill | Description |\n    66||-------|-------------|\n    67|| **swiftui** | SwiftUI views, modifiers, navigation, state management, charts |\n    68|| **uikit** | UIKit views, controllers, controls, scenes, Auto Layout, presentation |\n    69|| **swift-testing** | Swift Testing framework (`@Test`, `@Suite`, `#expect`, `#require`) |\n    70|| **swift-concurrency** | async/await, Task, TaskGroup, Actor, AsyncSequence |\n    71|| **swiftdata** | @Model, ModelContext, @Query, schema migrations |\n    72|| **healthkit** | HKHealthStore, HKQuantitySample, workouts, health data |\n    73|| **combine** | Publishers, subscribers, operators |\n    74|| **storekit** | StoreKit 2 (Product, Transaction, SubscriptionStoreView) |\n    75|| **mapkit** | MapKit for SwiftUI (Map, Marker, Annotation, MapCameraPosition) |\n    76|| **tipkit** | TipKit (Tip protocol, TipView, TipUIPopoverViewController) |\n    77|| **appintents** | App Intents, Siri, Shortcuts, Spotlight integration |\n    78|| **widgetkit** | Widget timelines, entries, providers |\n    79|| **usernotifications** | Local/remote notifications, triggers |\n    80|| **eventkit** | EKEventStore, EKEvent, EKReminder, calendar access |\n    81|| **photosui** | PhotosPicker, photo selection |\n    82|| **corehaptics** | CHHapticEngine, haptic patterns |\n    83|| **backgroundtasks** | BGTaskScheduler, app refresh |\n    84|| **xcuitest** | XCUITest with Swift 6 @MainActor patterns |\n    85|\n    86|### Design & Guidelines\n    87|\n    88|| Skill | Description |\n    89||-------|-------------|\n    90|| **hig** | Apple Human Interface Guidelines |\n    91|| **ios-liquid-glass** | Liquid Glass API reference (iOS 26+) |\n    92|| **ios-design-consultant** | UX/design guidance for Liquid Glass apps |\n    93|| **ios-dev** | SwiftUI development patterns & aesthetics |\n    94|\n    95|### Workflow & Pattern Guides\n    96|\n    97|> Expert workflow/pattern guides that teach *how* to approach tasks, as opposed to the reference docs above which document *what APIs exist*.\n    98|> Originally from [Dimillian/Skills](https://github.com/Dimillian/Skills) by Thomas Ricouard. MIT License.\n    99|\n   100|| Skill | Description |\n   101||-------|-------------|\n   102|| **guide-swiftui-performance-audit** | Audit and improve SwiftUI runtime performance |\n   103|| **guide-swiftui-ui-patterns** | Best practices for building SwiftUI views and components |\n   104|| **guide-swiftui-view-refactor** | Refactor SwiftUI views for consistent structure and Observation usage |\n   105|| **guide-macos-spm-packaging** | Scaffold, build, and package SwiftPM-based macOS apps without Xcode |\n   106|\n   107|### Utilities\n   108|\n   109|| Skill | Description |\n   110||-------|-------------|\n   111|| **apple-docs-index** | Index of Apple developer documentation — start here to find what you need |\n   112|| **simulator-utils** | iOS Simulator commands, screenshots, device management |\n   113|| **apple-aso** | App Store Optimization for metadata |\n   114|| **ios-app-icon** | App icon generation workflow |\n   115|| **ios-app-assets** | In-app asset generation workflow |\n   116|\n   117|## Target Platform\n   118|\n   119|These skills intentionally target the latest Apple APIs and platform conventions.\n   120|\n   121|**Why bleeding edge?** LLMs already have plenty of legacy Apple APIs in their training data — when a project needs backward compatibility, agents can add it on their own. But for the newest APIs, agents need to be steered with up-to-date docs; without them, they'll hallucinate or fall back to deprecated patterns.\n   122|\n   123|**iOS 26+ / Swift 6** — no legacy patterns. Uses:\n   124|- `@Observable` macro (not `ObservableObject`)\n   125|- `NavigationStack` (not `NavigationView`)\n   126|- Swift concurrency (`async`/`await`, not completion handlers)\n   127|- Liquid Glass design system\n   128|- Swift Testing where applicable\n   129|\n   130|## License\n   131|\n   132|MIT\n   133|", "total_lines": 132, "file_size": 4584, "truncated": false, "is_binary": false, "is_image": false}
[2026-04-11 17:48:59] 👤 Anh: Stop requested
[2026-04-11 17:48:59] 🤖 Em: Dừng rồi. Cần gì thì bảo.