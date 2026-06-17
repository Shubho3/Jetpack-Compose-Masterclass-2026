# Jetpack Compose Masterclass — 2026 Edition

[![Live site](https://img.shields.io/badge/live-course_site-2563eb)](https://shubho3.github.io/Jetpack-Compose-Masterclass-2026/) [![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-blue)](LICENSE) ![Modules](https://img.shields.io/badge/modules-20-brightgreen) ![Lessons](https://img.shields.io/badge/lessons-135-brightgreen) ![Words](https://img.shields.io/badge/words-471k-brightgreen)

**[📖 View the live course website →](https://shubho3.github.io/Jetpack-Compose-Masterclass-2026/)** — hosted on GitHub Pages, nothing to install.

> From "I can read XML" to **senior Android UI engineer** — declarative UI, Compose internals, performance, architecture, testing, security, and AI-assisted development, taught the way it's actually practiced in 2026.

This is a complete, project-based, industry-level curriculum. Every lesson is built to the same standard: a concept explained at three levels (beginner → intermediate → senior), visual learning (ASCII + Mermaid + illustration prompts), three tiers of runnable code (beginner → intermediate → production), interview questions, and an AI-assisted workflow section.

---

## 🌐 Read it as a website

The whole course is browsable as a single-page site — sidebar nav over all 20 modules and 135 lessons, full-text search, light/dark, syntax-highlighted Kotlin, and **live-rendered Mermaid diagrams**.

```bash
# from this folder (needs Python, which you already have):
python build-site.py        # generates course-data.json (re-run after adding content)
python -m http.server 8000  # then open http://localhost:8000
```

Or just run **`serve.bat`** (Windows) / **`./serve.sh`** (macOS·Linux) — it does both steps. The site reads the Markdown files over HTTP, so it must be *served*, not opened by double-clicking `index.html`.

**Hosting:** on every push to `main`, a GitHub Actions workflow ([`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)) rebuilds the manifest and redeploys to **GitHub Pages** automatically — so for the live version you never run `build-site.py` by hand.

---

## Who this is for

| You are… | This course… |
|---|---|
| **A beginner** (know Kotlin basics, new to Compose) | Starts from "what is declarative UI" and never skips a step. |
| **An intermediate dev** (shipped a Compose screen or two) | Fills the gaps: state correctness, modifiers, side effects, performance. |
| **A senior / staff engineer** | Goes deep on internals, architecture at scale, stability, and system design. |
| **Interview prep** | Every lesson ends with tiered interview questions; Module 20 is a full prep guide. |

**Prerequisite:** comfortable with Kotlin (data classes, lambdas, coroutines basics, `suspend`). If you're new to Kotlin, do a 1-week Kotlin primer first.

---

## What makes this different

- **2026 toolchain, not 2021 habits.** Kotlin 2.x + K2, the Compose compiler bundled with Kotlin, **Strong Skipping** on by default, Material 3 (expressive + adaptive), shared-element transitions, type-safe Navigation, Compose Multiplatform.
- **Internals before tricks.** You'll learn *why* recomposition skips, what the slot table is, and how the snapshot system works — so performance stops being guesswork.
- **AI-native engineering.** Every topic includes how to actually use ChatGPT / Claude / Gemini / Cursor / Windsurf / Copilot to go faster *without* shipping garbage — with prompt, review, and validation workflows.
- **Project-based.** You build real things: e-commerce, banking dashboard, social feed, analytics charts, and a full production app.

---

## How to use this course

1. **Read in order the first time.** Modules build on each other (state → modifiers → layout → side effects → internals).
2. **Do the code.** Type it, don't copy-paste. Break it on purpose. Each lesson lists *Common Mistakes* — reproduce them so you recognize them later.
3. **Answer the interview questions out loud** before reading further. Retrieval beats re-reading.
4. **Use the AI workflows as a force multiplier, not a crutch.** Generate, then *review against the lesson's best-practices list*.
5. **Build the projects.** Knowledge you don't apply evaporates in ~2 weeks.

See **[AUTHORING-GUIDE.md](AUTHORING-GUIDE.md)** for the exact structure every lesson follows.

---

## Course map (20 modules)

### Part I — Foundations
| # | Module | What you'll own |
|---|---|---|
| 01 | [Introduction to Modern Android UI](modules/module-01-introduction/README.md) | Declarative mindset; why Compose exists; Compose vs XML |
| 02 | [Basic Layouts & Responsive Design](modules/module-02-layouts/README.md) | Row/Column/Box, lazy lists/grids, Scaffold, adaptive/foldable UI |
| 03 | [State Management](modules/module-03-state-management/README.md) **★ exemplar** | `remember`, hoisting, UDF, MVI/MVVM, single source of truth |
| 04 | [Modifiers Mastery](modules/module-04-modifiers/README.md) | The modifier chain, order, pointer input, nested scroll |

### Part II — The Rendering Engine
| # | Module | What you'll own |
|---|---|---|
| 05 | [Measurements, Advanced & Custom Layouts](modules/module-05-custom-layouts/README.md) | Constraints, intrinsics, custom & subcompose layouts |
| 06 | [Side Effects](modules/module-06-side-effects/README.md) | `LaunchedEffect`, `DisposableEffect`, `derivedStateOf`, `snapshotFlow` |
| 07 | [CompositionLocal](modules/module-07-compositionlocal/README.md) | Implicit dependencies done right |
| 08 | [Canvas & Graphics](modules/module-08-canvas-graphics/README.md) | Draw phase, custom charts, vector graphics |

### Part III — Polish & Performance
| # | Module | What you'll own |
|---|---|---|
| 09 | [Material 3 Theming](modules/module-09-material3-theming/README.md) | Dynamic color, color roles, typography, shape system |
| 10 | [Animations Masterclass](modules/module-10-animations/README.md) | `animate*AsState`, `AnimatedContent`, shared elements, Lookahead |
| 11 | [Performance Optimization](modules/module-11-performance/README.md) | Profiling, Macrobenchmark, baseline profiles, deferring reads |
| 12 | [Jetpack Compose Internals](modules/module-12-internals/README.md) | Compiler, runtime, slot table, snapshots, stability |

### Part IV — Production Engineering
| # | Module | What you'll own |
|---|---|---|
| 13 | [Architecture for Real Apps](modules/module-13-architecture/README.md) | Clean Architecture, MVI, repository, offline-first |
| 14 | [Testing Jetpack Compose](modules/module-14-testing/README.md) | Unit, UI, screenshot, macrobenchmark testing |
| 15 | [Modern Android Development 2026](modules/module-15-modern-android-2026/README.md) | Kotlin 2.x, K2, Multiplatform, XR, Wear, desktop |
| 16 | [AI-Powered Android Development](modules/module-16-ai-powered-dev/README.md) | Agentic workflows, AI coding agents, automated refactor/test |

### Part V — Craft & Capstone
| # | Module | What you'll own |
|---|---|---|
| 17 | [Code Quality Engineering](modules/module-17-code-quality/README.md) | SOLID/KISS/DRY/YAGNI, Detekt, Ktlint, AI review |
| 18 | [Security for Android Apps](modules/module-18-security/README.md) | Secure storage, encryption, OWASP Mobile Top 10 |
| 19 | [Build a Production App](modules/module-19-production-app/README.md) | Compose + Room + Retrofit + Hilt + WorkManager + CI/CD |
| 20 | [Career & Interview Preparation](modules/module-20-career-interview/README.md) | Roadmap, system design, AI-era Android skills |

---

## Course-level materials

- **[Curriculum](course/curriculum.md)** — the complete syllabus with learning outcomes per module.
- **[Learning Path](course/learning-path.md)** — beginner → advanced track, with on/off-ramps.
- **[Weekly Study Plan](course/weekly-study-plan.md)** — a 16-week schedule (and a 10-week accelerated track).
- **[Deliverables](deliverables/)** — cheat sheets, interview prep, capstone, certification exam, final assessment, resources.

---

## Tech baseline (2026)

| Area | What we use |
|---|---|
| Language | Kotlin 2.x (K2 compiler default) |
| Compose | Compose BOM (Material 3), compiler plugin bundled with Kotlin (`org.jetbrains.kotlin.plugin.compose`) |
| Recomposition | **Strong Skipping** enabled by default |
| Design | Material 3 + Material 3 Expressive + `material3-adaptive` |
| Navigation | Type-safe Navigation Compose (Kotlin-serialization routes); Navigation 3 noted where relevant |
| Async | Coroutines + Flow |
| DI | Hilt |
| Local data | Room + DataStore |
| Network | Retrofit / Ktor + kotlinx.serialization |
| Background | WorkManager |
| Testing | JUnit, MockK, Turbine, Compose Testing APIs, Paparazzi/Roborazzi (screenshot), Macrobenchmark |
| Multiplatform | Compose Multiplatform (where called out) |

> Versions move fast. We pin concepts, not patch numbers — always cross-check the latest **Compose BOM** and **Android Gradle Plugin** when you build.

---

## Build status

**All 20 modules are written end-to-end** — **135 lessons, ~400,000 words**, every one built to the [authoring-guide](AUTHORING-GUIDE.md) standard and structurally verified (5 sections each; all internal links resolve).

- ✅ Course scaffold, README, authoring guide
- ✅ Curriculum, learning path, weekly study plan
- ✅ All 20 module hubs (lesson indexes)
- ✅ **All 20 modules — 135 full lessons** (Concept · Visual · Code · Interview · AI Assistant)
- ✅ **Module 03 — State Management** — the original hand-written exemplar that set the bar
- ✅ All 12 deliverable collections — cheat sheets, interview prep, capstone (`Pulse`), exam, assessment, projects, mind maps, more
- ✅ Browsable website — `index.html` (sidebar nav, search, syntax highlighting, live Mermaid)

New here? Start at **[Module 01 — Introduction](modules/module-01-introduction/README.md)**. Want to gauge the depth first? Read **[Module 03 — State Management](modules/module-03-state-management/README.md)**.

---

*Built as a living curriculum. Code is idiomatic to the 2026 Compose toolchain; verify exact dependency versions against the current Compose BOM when you implement.*

---

## License

Licensed under the **[Apache License 2.0](LICENSE)** — © 2026 Shubho3. You're free to use, modify, and distribute (including commercially), provided you preserve the license, copyright, and [NOTICE](NOTICE).

Jetpack Compose, Android, Kotlin, and Material are trademarks of their respective owners; this course is independent and not affiliated with or endorsed by Google.
