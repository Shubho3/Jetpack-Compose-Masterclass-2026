# Capstone — Build Milestones (8 Phases)

> The build *order* for `Pulse`, the offline-first news client defined in [`spec.md`](spec.md). Each phase is a gate: you don't advance until its **done-criteria** are all true. The phases map 1:1 onto the [Module 19 build plan](../../modules/module-19-production-app/README.md).

**How to read this:** every phase has a **goal**, a single **key deliverable** (the artifact that proves the phase happened), concrete **done-criteria** (checkboxes), and a **gate** (the one thing that must be true to move on). Resist starting the next phase early — the offline-first spine breaks if the layers are built out of order.

```text
setup ──▶ data ──▶ domain ──▶ UI ──▶ DI ──▶ background ──▶ testing ──▶ CI/CD
  01      02        03        04     05        06            07          08
```

---

## Phase 01 — Project & Module Setup

**Goal:** Stand up the multi-module skeleton so the architecture is enforced by the *build*, not by hope.
**Key deliverable:** A compiling `:app` + `:core:*` + `:feature:*` graph with a version catalog and convention plugins.
**Reference:** [Module 19 · L01 — Project & Module Setup](../../modules/module-19-production-app/01-project-module-setup.md), [Module 13 · L06 — Feature Modularization](../../modules/module-13-architecture/06-feature-modularization.md).

**Done-criteria**
- [ ] Modules registered in `settings.gradle.kts`: `:app`, `:core:model`, `:core:common`, `:core:designsystem`, `:core:network`, `:core:database`, `:core:data`, `:core:domain`, `:feature:headlines`, `:feature:bookmarks`, `:feature:article`.
- [ ] `gradle/libs.versions.toml` is the single source of versions; **Compose BOM** governs Compose artifacts (no explicit versions on them).
- [ ] `:core:model` is a **pure `kotlin("jvm")`** module (no `android {}` block).
- [ ] Convention plugins in `build-logic` (`myapp.android.library`, `myapp.android.feature`, `myapp.android.compose`); each module applies one plugin line.
- [ ] `gradle.properties`: configuration cache, build cache, parallel, non-transitive R classes all enabled.
- [ ] Type-safe project accessors (`projects.core.data`) on.

**Gate:** `./gradlew help --configuration-cache` serializes, and an attempted `import androidx.room.Entity` inside `:feature:headlines` **fails to compile** (the boundary is real). No `:feature:*` depends on another `:feature:*`.

---

## Phase 02 — Data Layer

**Goal:** Make Room the single source of truth; the network only feeds it. This is where offline-first is won or lost.
**Key deliverable:** An `OfflineFirstArticleRepository` that exposes a `Flow` from Room and a `refresh()` that writes Room — plus DTO/Entity/domain models with boundary mappers.
**Reference:** [Module 19 · L02 — Data Layer](../../modules/module-19-production-app/02-data-layer.md), [Module 13 · L04 — Repository Pattern](../../modules/module-13-architecture/04-repository-pattern.md), [Module 13 · L07 — Offline-First](../../modules/module-13-architecture/07-offline-first.md).

**Done-criteria**
- [ ] `:core:network`: Retrofit `NewsApi` + `ArticleDto` (kotlinx.serialization); API key from `BuildConfig`, not source.
- [ ] `:core:database`: Room `ArticleEntity` (with `syncState` + `updatedAt`), `ArticleDao` exposing `observeAll(): Flow<List<ArticleEntity>>`, plus a sync-cursor store.
- [ ] Mappers `Dto→Entity`, `Entity→domain Article` live in the **data** layer; the domain never imports a DTO/Entity.
- [ ] `observeArticles()` reads **only** Room; `refresh()` fetches the API and writes Room (the `Flow` re-emits).
- [ ] Optimistic bookmark write: `upsert(pending=true)` → attempt upload → `SYNCED`/`FAILED`.
- [ ] I/O is off the main thread (`flowOn(io)` / `withContext(io)` with an injected `@IoDispatcher`).

**Gate:** With the network stubbed to fail, `observeArticles()` still emits cached rows (offline read works), and a bookmark write updates Room immediately and is marked `PENDING`.

---

## Phase 03 — Domain Layer

**Goal:** Encode the business rules in framework-free Kotlin so they're testable in milliseconds and the UI stays thin.
**Key deliverable:** Use cases (`GetHeadlinesUseCase`, `ToggleBookmarkUseCase`, `SearchArticlesUseCase`, `SyncNewsUseCase`) over repository **interfaces** defined in the domain.
**Reference:** [Module 19 · L03 — Domain Layer](../../modules/module-19-production-app/03-domain-layer.md), [Module 13 · L05 — Use Cases](../../modules/module-13-architecture/05-use-cases-interactors.md), [Module 13 · L01 — Clean Architecture Layers](../../modules/module-13-architecture/01-clean-architecture-layers.md).

**Done-criteria**
- [ ] Repository **interfaces** (`ArticleRepository`, `BookmarkRepository`) live in `:core:domain` (or `:core:data`'s domain surface); the data layer *implements* them (dependency inversion).
- [ ] Use cases return domain `Article` types and `Flow`/`Result`; no `androidx`/Retrofit/Room import anywhere in the domain.
- [ ] Business rules that aren't trivial CRUD (e.g. "search filters cached items," "a bookmark toggle is optimistic") are expressed here, not in the ViewModel.
- [ ] Use cases are pure enough to unit-test with plain JUnit (no Robolectric, no device).

**Gate:** A JVM unit test exercises a use case against a **fake** repository with zero Android dependencies. If the domain needs a device to test, the layering is wrong — fix it before Phase 04.

---

## Phase 04 — UI Layer

**Goal:** Build the screens as MVI: one immutable `UiState`, events in, effects out — every state handled.
**Key deliverable:** `HeadlinesScreen`, `ArticleScreen`, `BookmarksScreen` with ViewModels exposing `StateFlow<UiState>`, consumed via `collectAsStateWithLifecycle()`, wired with **type-safe Navigation**.
**Reference:** [Module 19 · L04 — UI Layer](../../modules/module-19-production-app/04-ui-layer.md), [Module 13 · L02 — MVVM](../../modules/module-13-architecture/02-mvvm-in-compose.md), [Module 13 · L03 — MVI](../../modules/module-13-architecture/03-mvi-unidirectional-state.md), [Module 03 — State Management](../../modules/module-03-state-management/README.md), [Module 09 — Material 3 Theming](../../modules/module-09-material3-theming/README.md).

**Done-criteria**
- [ ] Each screen models **loading · content · empty · error**, with *first-launch-empty* distinct from *offline-but-cached* (AC-5.1).
- [ ] `UiState` is a single immutable type; lists use immutable/stable collections (Strong Skipping friendly, per [Module 11 — Performance](../../modules/module-11-performance/README.md)).
- [ ] State consumed with `collectAsStateWithLifecycle()`; `viewModelScope` + `stateIn(WhileSubscribed(5_000))`.
- [ ] Transient one-off effects (navigation, snackbars) flow through a `Channel`/effects stream, not as state ([Module 06 — Side Effects](../../modules/module-06-side-effects/README.md)).
- [ ] UI-relevant state survives config change/process death via `SavedStateHandle`/`rememberSaveable` (AC-4.1).
- [ ] Type-safe `@Serializable` routes in `:core:navigation`; `:app` owns the `NavHost`; features navigate by route/lambda, never by importing each other.
- [ ] Material 3, dynamic color + light/dark.

**Gate:** With a fake repository, you can drive each screen through all four states by hand; the offline banner shows `last updated` from cache; no Composable references `NewsApi`.

---

## Phase 05 — Dependency Injection

**Goal:** Wire the graph with Hilt so callers depend on **abstractions** and implementations are constructed only in the DI graph.
**Key deliverable:** Hilt modules binding repository interfaces to impls and providing Retrofit/Room/dispatchers across module boundaries.
**Reference:** [Module 19 · L05 — Dependency Injection](../../modules/module-19-production-app/05-dependency-injection.md), [Module 13 · L01 — Clean Architecture Layers](../../modules/module-13-architecture/01-clean-architecture-layers.md).

**Done-criteria**
- [ ] `@HiltAndroidApp` on `NewsApplication`; `@AndroidEntryPoint` on the host Activity; `@HiltViewModel` ViewModels with `@Inject` constructors.
- [ ] `@Binds` binds `ArticleRepository → OfflineFirstArticleRepository` (callers never see the Impl).
- [ ] `@Provides` for Retrofit, Room (`@Singleton`), `@IoDispatcher` qualifier.
- [ ] `@HiltWorker` + `HiltWorkerFactory` wired so WorkManager can inject the sync worker (used in Phase 06).
- [ ] DI modules are installed in the right component scope; no leaked `Context` into `:core:domain`/`:core:model`.

**Gate:** The app launches end to end on real wiring (no manual construction in screens); swapping a binding to a fake repository in a test changes the data with **no UI change** — proof the UI depends on the interface.

---

## Phase 06 — Background Work

**Goal:** Make sync guaranteed, idempotent, delta-based, and connectivity-aware with WorkManager.
**Key deliverable:** A `@HiltWorker SyncWorker` that pushes pending bookmark writes and pulls deltas, scheduled as **unique** periodic work with constraints + backoff.
**Reference:** [Module 19 · L06 — Background Work](../../modules/module-19-production-app/06-background-work.md), [Module 13 · L07 — Offline-First](../../modules/module-13-architecture/07-offline-first.md).

**Done-criteria**
- [ ] Worker **pushes** outbox/pending rows (idempotent — safe to retry; drained in dependency order).
- [ ] Worker **pulls** only changes since a **persisted cursor** (delta sync), then advances the cursor.
- [ ] Failure mapping: `IOException`/5xx → `Result.retry()`; 4xx → `Result.failure()` + revert/flag the local row.
- [ ] Conflict policy applied: **last-write-wins by `updatedAt`**, documented and detectable (every row stores `updatedAt`).
- [ ] Scheduling: `enqueueUniquePeriodicWork(..., KEEP)`, `NetworkType.CONNECTED` constraint, `BackoffPolicy.EXPONENTIAL`; plus an expedited one-off sync on app open when stale.

**Gate:** Airplane-mode → bookmark → reconnect: the worker uploads the pending write, marks it `SYNCED`, and survives an app kill mid-sync **without** a duplicate server write (idempotency proven). A stubbed `404` reverts the row.

---

## Phase 07 — Testing

**Goal:** Prove every layer with the cheapest test that catches each bug class — a fast, trustworthy suite, not a slow flaky one.
**Key deliverable:** A layered suite: unit (ViewModels/use cases/flows) + Compose UI (semantics) + integration (nav + fakes) + screenshot (Roborazzi) + one Macrobenchmark.
**Reference:** [Module 14 — Testing](../../modules/module-14-testing/README.md) — [L01 Pyramid](../../modules/module-14-testing/01-testing-pyramid.md), [L02 Unit](../../modules/module-14-testing/02-unit-testing-state.md), [L03 UI](../../modules/module-14-testing/03-compose-ui-testing.md), [L05 Screenshot](../../modules/module-14-testing/05-screenshot-testing.md), [L06 Macrobenchmark](../../modules/module-14-testing/06-macrobenchmark-testing.md); [Module 19 · L07 — Testing](../../modules/module-19-production-app/07-testing.md).

**Done-criteria**
- [ ] **Unit (`src/test/`):** ViewModel reducers (event→state), `StateFlow` emissions via **Turbine**, use cases with **MockK** fakes, all under `runTest`. The bulk of the suite.
- [ ] **Screenshot (`src/test/`, Roborazzi/Paparazzi):** each screen's loading/content/empty/error in light **and** dark, deterministic rendering.
- [ ] **Compose UI (`src/androidTest/`):** semantics tests — e.g. bookmark toggle reflects state, offline banner appears, error state offers Retry. Behavior, not implementation.
- [ ] **Integration (`src/androidTest/`):** navigation feed→detail with fake repositories; process-death restoration of filter/selection.
- [ ] **Macrobenchmark module:** startup + feed-scroll frame timing; generates the **Baseline Profile** artifact.
- [ ] No real network anywhere in tests; each test asserts **one** behavior; zero flaky tests (a flake is a P1).

**Gate:** `./gradlew testDebugUnitTest verifyRoborazziDebug` is green and runs in **seconds**; the `androidTest` suite is small and green; the Macrobenchmark produces a `baseline-prof.txt`. The suite shape is a pyramid/trophy, not an ice-cream cone.

---

## Phase 08 — CI/CD & Monitoring

**Goal:** Ship it for real — gated PRs, a signed App Bundle with its Baseline Profile, and monitoring so you learn of problems from dashboards, not reviews.
**Key deliverable:** A GitHub Actions pipeline (required check) + a signed `bundleRelease` with R8, Baseline Profile, mapping upload, and Crashlytics.
**Reference:** [Module 19 · L08 — CI/CD & Monitoring](../../modules/module-19-production-app/08-ci-cd-monitoring.md), [Module 17 — Code Quality](../../modules/module-17-code-quality/README.md), [Module 18 — Security](../../modules/module-18-security/README.md).

**Done-criteria**
- [ ] `.github/workflows/ci.yml` on `pull_request` + push to `main`: JDK 17, **Gradle cache**, runs `assembleDebug testDebugUnitTest lintDebug detekt verifyRoborazziDebug`.
- [ ] The CI check is **required** in branch protection (a red build blocks merge); slow device tests/Macrobenchmarks run on a schedule, **not** the per-PR path.
- [ ] Release job (`needs: ci`, `main` only): decode keystore from **Secrets**, `bundleRelease` with `isMinifyEnabled` + `isShrinkResources`; signing creds via env from Secrets, never hardcoded.
- [ ] **Baseline Profile wired** into the release (`androidx.baselineprofile` + `baselineProfile(projects.macrobenchmark)` + ProfileInstaller) and verified present in the `.aab`.
- [ ] **R8 mapping uploaded** to Crashlytics (`-keepattributes SourceFile,LineNumberTable`); Crashlytics + Performance + custom keys/breadcrumbs wired.
- [ ] Detekt + Lint clean on the changed surface; staged-rollout step to the internal track gated on crash-free %.

**Gate:** A throwaway PR with a failing test goes **red and blocks merge**; a passing PR's CI is fast (cache hit); `bundleRelease` produces a **signed** `.aab` containing the Baseline Profile; a release-build test crash shows a **deobfuscated** trace with custom keys in Crashlytics.

---

## Phase summary

| # | Phase | Key deliverable | Gate (one-liner) |
|---|---|---|---|
| 01 | Setup | Multi-module skeleton + catalog + convention plugins | CC serializes; feature can't import another feature/Room |
| 02 | Data | `OfflineFirstArticleRepository` (Room SSOT) | Offline read works with network stubbed to fail |
| 03 | Domain | Use cases over repo interfaces, framework-free | Use case unit-tested with a fake, zero Android deps |
| 04 | UI | MVI screens, all 4 states, type-safe Nav | Drive every state via a fake; offline banner shows |
| 05 | DI | Hilt binds interfaces → impls across modules | App runs on real wiring; fake swaps with no UI change |
| 06 | Background | Idempotent, delta `SyncWorker` (unique work) | Airplane→bookmark→reconnect syncs, no dup on retry |
| 07 | Testing | Layered suite + Macrobenchmark + profile | Unit+screenshot green in seconds; profile generated |
| 08 | CI/CD | Gated pipeline + signed `.aab` + monitoring | Failing PR blocked; signed bundle ships the profile |

> Each gate is also an **acceptance criterion** in [`spec.md`](spec.md §5). When all eight gates are green, the Definition of Done is met.

---

➡️ The code shape that makes these phases buildable lives in **[`architecture.md`](architecture.md)**.
