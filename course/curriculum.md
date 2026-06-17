# Curriculum — Jetpack Compose Masterclass (2026 Edition)

The complete syllabus: what each module covers, what you'll be able to *do* after it, and the project that proves it.

**Format of every lesson:** Concept (🟢🟡🔴) → Visual Learning (ASCII + Mermaid + illustration) → Code (beginner/intermediate/production) → Interview Questions → AI Assistant. See [AUTHORING-GUIDE.md](../AUTHORING-GUIDE.md).

---

## Course-level outcomes

By the end you can:

1. **Think declaratively** — model UI as a function of state and predict recomposition.
2. **Build adaptive UIs** that work on phones, foldables, tablets, and desktop.
3. **Manage state correctly** — hoisting, UDF, single source of truth, immutability.
4. **Master the rendering pipeline** — composition, layout, draw, and custom layouts.
5. **Optimize performance** with profiling, baseline profiles, and stability fixes.
6. **Explain Compose internals** — slot table, snapshot system, skipping.
7. **Architect production apps** — Clean Architecture + MVI + offline-first.
8. **Test every layer** — unit, UI, screenshot, macrobenchmark.
9. **Engineer with AI** — agentic workflows that speed you up without lowering quality.
10. **Ship securely** — secure storage, encryption, OWASP Mobile Top 10.

---

## Part I — Foundations

### Module 01 — Introduction to Modern Android UI
**Topics:** Android UI evolution · Views/XML vs Compose · declarative UI · why Google built Compose · how Compose works (composition → recomposition) · the declarative mindset · common misconceptions.
**Outcomes:** Explain *why* declarative UI exists; read a `@Composable`; articulate the imperative→declarative shift.
**Project:** "Hello, declarative" — convert one XML screen mentally and in code.

### Module 02 — Basic Layouts & Responsive Design
**Topics:** layout principles & constraint thinking · `Row`/`Column`/`Box` · `Flow` layouts · `LazyColumn`/`LazyRow`/`LazyGrid` · `Scaffold` · Window Size Classes · adaptive UI · foldables · tablets · desktop Compose.
**Outcomes:** Build responsive screens that adapt across form factors.
**Projects:** E-commerce listing · banking dashboard · social feed (from Figma mockups).

### Module 03 — State Management ★ *(exemplar — fully written)*
**Topics:** state basics · `MutableState` · `remember` · `rememberSaveable` · state hoisting · Unidirectional Data Flow · MVI · MVVM · single source of truth · immutable state · state synchronization.
**Outcomes:** Decide where state lives, hoist correctly, and design a UDF screen with one source of truth.
**Project:** A correctly-hoisted, survives-rotation form + a UDF counter/cart screen.

### Module 04 — Modifiers Mastery
**Topics:** why modifiers exist · the modifier chain · modifier *order* · padding/insets/shapes/offset · `clickable` · interaction sources · focus · `draggable` · pointer input · nested scroll.
**Outcomes:** Predict the effect of modifier order; build custom interactions.
**Project:** A swipe-to-dismiss card with custom pointer handling.

---

## Part II — The Rendering Engine

### Module 05 — Measurements, Advanced Layouts & Custom Modifiers
**Topics:** layout phase · constraints · intrinsic measurements · `BoxWithConstraints` · `onSizeChanged` · `onGloballyPositioned` · custom `Layout` · `SubcomposeLayout` · modifier factories.
**Outcomes:** Write a custom layout from measure/place primitives.
**Projects:** Pinterest staggered grid · timeline layout · mind-map layout.

### Module 06 — Side Effects
**Topics:** why side effects exist · recomposition safety · `LaunchedEffect` · `rememberCoroutineScope` · `DisposableEffect` · `SideEffect` · `produceState` · `derivedStateOf` · `snapshotFlow` · `rememberUpdatedState`.
**Outcomes:** Run effects safely keyed to state; avoid leaks and redundant work.
**Project:** A search screen with debounced queries and lifecycle-safe effects.

### Module 07 — CompositionLocal
**Topics:** built-in CompositionLocals · custom CompositionLocals · `staticCompositionLocalOf` vs `compositionLocalOf` · DI alternatives & when *not* to use them.
**Outcomes:** Pass implicit dependencies without prop-drilling — and know the cost.
**Project:** A theming/locale provider via custom CompositionLocal.

### Module 08 — Compose Canvas & Graphics
**Topics:** the draw phase · Canvas API · drawing shapes/paths · custom charts · graphics-layer animations · vector graphics.
**Outcomes:** Draw custom visuals and charts efficiently.
**Projects:** Analytics dashboard · financial candlestick chart · interactive graph.

---

## Part III — Polish & Performance

### Module 09 — Material 3 Theming
**Topics:** dynamic color (Material You) · color roles · typography · shape system · light/dark themes.
**Outcomes:** Build a themable design system with dynamic color.
**Project:** A full light/dark/dynamic theme + component gallery.

### Module 10 — Animations Masterclass
**Topics:** `animate*AsState` · `AnimatedVisibility` · `AnimatedContent` · `Animatable` · infinite transitions · shared-element transitions · `LookaheadLayout`.
**Outcomes:** Choose the right animation API; build shared-element navigation.
**Projects:** Navigation transitions · onboarding · dashboard transitions.

### Module 11 — Performance Optimization
**Topics:** recomposition profiling · Layout Inspector · Macrobenchmark · baseline profiles · image loading · lazy-list optimization · overdraw · main-thread safety · `movableContentOf` · deferring state reads.
**Outcomes:** Find and fix the real performance problems with data, not vibes.
**Deliverables:** Benchmark report + before/after profile.

### Module 12 — Jetpack Compose Internals
**Topics:** the Compose compiler · runtime · slot table · snapshot system · stability & immutability · skipping · grouping · frame lifecycle.
**Outcomes:** Explain *why* a composable skips or restarts — and design for it.
**Analogies:** city / database / operating-system models of the runtime.

---

## Part IV — Production Engineering

### Module 13 — Architecture for Real Apps
**Topics:** Clean Architecture · MVVM · MVI · repository pattern · use cases · feature modules · offline-first.
**Outcomes:** Structure a multi-feature app with clear boundaries.
**Project:** Production-ready architecture skeleton.

### Module 14 — Testing Jetpack Compose
**Topics:** unit · UI · integration · screenshot · macrobenchmark testing. Tools: JUnit, MockK, Turbine, Compose Testing APIs.
**Outcomes:** Test state, UI, and performance with the right tool per layer.
**Project:** A tested feature with semantics-based UI tests.

### Module 15 — Modern Android Development 2026
**Topics:** Kotlin 2.x · K2 compiler · Compose Multiplatform · Android XR · foldables · Wear OS · desktop Compose · AI-native apps.
**Outcomes:** Place Compose in the wider 2026 ecosystem.

### Module 16 — AI-Powered Android Development
**Topics:** what agentic AI is · AI coding agents · multi-agent workflows. Tools: Cursor, Claude Code, Gemini CLI, OpenAI Codex, Windsurf.
**Outcomes:** Run a planner→architect→coder→reviewer→human workflow on real Android tasks.

---

## Part V — Craft & Capstone

### Module 17 — Code Quality Engineering
**Topics:** Clean Code · SOLID · KISS · DRY · YAGNI · code smells. Tools: Detekt, Ktlint, SonarQube, Android Lint. AI-powered review workflows.
**Outcomes:** Keep a codebase healthy and reviewable.

### Module 18 — Security for Android Apps
**Topics:** secure storage · encryption · API security · authentication · authorization · OWASP Mobile Top 10.
**Outcomes:** Ship an app that protects user data and secrets.

### Module 19 — Build a Production App (capstone)
**Stack:** Compose · Material 3 · Navigation · Room · Retrofit · Coroutines · Flow · Hilt · WorkManager.
**Includes:** architecture · testing · CI/CD · monitoring.
**Outcome:** A portfolio-grade, end-to-end application.

### Module 20 — Career & Interview Preparation
**Topics:** Android interview roadmap · Compose interview questions · senior system design · architecture discussions · AI-era Android engineering skills.
**Outcome:** Interview-ready, with a system-design playbook.

---

## Assessment & deliverables

| Deliverable | Where |
|---|---|
| Practice projects & assignments | per-module READMEs |
| Cheat sheets | [`deliverables/cheat-sheets/`](../deliverables/cheat-sheets/) |
| Interview prep guide | [`deliverables/interview-prep/`](../deliverables/interview-prep/) |
| Capstone project | [`deliverables/capstone-project/`](../deliverables/capstone-project/) |
| Certification exam | [`deliverables/certification-exam.md`](../deliverables/certification-exam.md) |
| Final assessment | [`deliverables/final-assessment.md`](../deliverables/final-assessment.md) |
| Recommended resources | [`deliverables/resources.md`](../deliverables/resources.md) |

See the **[Learning Path](learning-path.md)** for the recommended order and the **[Weekly Study Plan](weekly-study-plan.md)** for pacing.
