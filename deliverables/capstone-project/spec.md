# Capstone — Product Brief & Acceptance Criteria

> The single source of truth for *what* we're building and *when it's done*. Pair this with [`milestones.md`](milestones.md) (the build order) and [`architecture.md`](architecture.md) (the shape of the code).

**Project:** `Pulse` — an offline-first news client
**Level:** 🔴 Senior · **Estimated build:** 20–30 hrs (multi-week)
**Owns the stack from:** [Module 19 — Build a Production App](../../modules/module-19-production-app/README.md)

---

## 1. The decision (committed)

This capstone is **an offline-first news client.** Not finance, not fitness — a news reader, and every section below assumes that.

Why news, and why commit instead of leaving it open:

- **It exercises the whole production stack honestly.** A news feed is a *paged, syncing list of remote content the user also mutates locally* (bookmarks, read-state). That single sentence forces Room as the source of truth, Retrofit for refresh, WorkManager for background sync, optimistic writes with rollback, and a real conflict story — the exact spine of [Module 13](../../modules/module-13-architecture/README.md) and [Module 19](../../modules/module-19-production-app/README.md).
- **Offline-first is the *point*, not a bolt-on.** A subway commuter opening the app must see yesterday's headlines instantly and bookmark one with no signal. That requirement, taken seriously, is what separates a portfolio demo from a shipped app.
- **It stays in scope.** No payments (finance) or sensor/Health-Connect plumbing (fitness) to distract from the architecture lesson. The complexity lives where the course wants it: data flow, state, and testing.

> **Mental model for the whole capstone:** *the database is the truth the UI trusts; the network is a background courier that reconciles it.* (Straight from [Module 13 · Lesson 07 — Offline-First](../../modules/module-13-architecture/07-offline-first.md).)

### Data source

A public headlines API (e.g. a NewsAPI-style REST endpoint, or a self-hosted JSON feed). The contract we depend on:

- `GET /headlines?category=&cursor=` → a page of articles + a `nextCursor` (delta/keyset paging).
- `GET /changes?since=<cursor>` → articles changed since a cursor (delta sync).
- `POST /bookmarks` / `DELETE /bookmarks/{id}` → idempotent bookmark mutation.

The API key lives in `local.properties` → `BuildConfig`, never in source control (see [Module 18 — Security](../../modules/module-18-security/README.md)). If no live API is available, a bundled JSON fixture served by a fake `NewsApi` satisfies every acceptance criterion below — offline-first means the app never *needs* the network to be useful.

---

## 2. Personas & the job to be done

| Persona | Context | Job to be done |
|---|---|---|
| **Commuter Casey** | On the subway, no signal, 4 minutes | "Catch up on headlines and save two to read later." |
| **Skimmer Sam** | At a desk, good Wi-Fi, 30 seconds | "See what's new since this morning, fast." |
| **Returning Rae** | Reopens after a day, flaky 3G | "Pick up where I left off; my bookmarks are still here." |

Every feature below traces to one of these. If a proposed feature serves none of them, it's out of scope for the capstone.

---

## 3. Feature list

### Must-have (the graded surface)

1. **Headlines feed** — a scrollable list of articles (title, source, published time, thumbnail), grouped/filterable by category. Renders **instantly from cache**; refreshes in the background.
2. **Article detail** — full article view with source attribution and an external "open original" link.
3. **Bookmarks** — save/unsave an article. The toggle is **optimistic** (instant) and **survives offline**, syncing when connectivity returns.
4. **Offline reading** — everything already fetched is fully readable with **airplane mode on**. No blocking spinners, no dead screens.
5. **Background sync** — a WorkManager job pulls deltas and pushes pending bookmark writes on a schedule and on connectivity, idempotently.
6. **Pull-to-refresh + explicit sync status** — the user can force a refresh; the UI honestly shows `idle / syncing / offline · last updated 5m ago / error`.
7. **Search / filter** — filter the cached feed by category and free-text query (reads Room, works offline).
8. **All UI states handled** — every screen models **loading · content · empty · error**, with a *first-launch-no-cache* empty state distinct from an *offline-but-cached* state.

### Should-have (stretch, if time permits)

9. **Paging** — `RemoteMediator` (Paging 3) so the network fills Room pages and the user scrolls cached pages offline.
10. **Read/unread state** — mark-as-read on open, dim read items (another optimistic, synced write).
11. **Theming** — Material 3 dynamic color + light/dark, per [Module 09](../../modules/module-09-material3-theming/README.md).

### Explicit non-goals (out of scope on purpose)

- Authentication / accounts (a shared anonymous feed is enough).
- Push notifications (sync is pull + background, not FCM-driven).
- Comments, social, multi-device real-time collaboration (no CRDTs needed — last-write-wins is the chosen conflict policy).
- A backend. We consume an API; we don't build one.

> Cutting these is a *senior* move: scope is a feature. The capstone is graded on depth of the offline-first/architecture/testing spine, not breadth of features.

---

## 4. User stories with acceptance criteria

Stories use the `As a … I want … so that …` form; acceptance criteria are written **Given/When/Then** so they map 1:1 onto tests (see [Module 14 — Testing](../../modules/module-14-testing/README.md)).

### US-1 — Instant, offline feed

> *As Commuter Casey, I want the feed to appear immediately with no signal, so that I can read on the subway.*

- **AC-1.1 (offline render):** **Given** the app has cached articles and the device is in airplane mode, **When** I open the feed, **Then** cached articles render with **no blocking spinner**, and a non-blocking banner reads `Offline · last updated <relative time>`.
- **AC-1.2 (instant, not network-gated):** **Given** a warm cache, **When** the feed opens, **Then** the first frame shows content sourced from Room — the screen **never** awaits the network to display.
- **AC-1.3 (auto-refresh on connect):** **Given** the feed is open and the cache is stale, **When** connectivity returns, **Then** the list updates automatically (the Room `Flow` re-emits) without a manual action.

### US-2 — Offline bookmarking (optimistic + synced)

> *As Commuter Casey, I want to bookmark an article offline, so that I can find it later.*

- **AC-2.1 (instant toggle):** **Given** no network, **When** I tap bookmark, **Then** the UI reflects the bookmarked state **immediately** and the row is marked `PENDING` in Room.
- **AC-2.2 (eventual sync):** **Given** a `PENDING` bookmark, **When** connectivity returns, **Then** a WorkManager job uploads it, marks it `SYNCED`, and the change is durable across an app kill.
- **AC-2.3 (rollback on permanent failure):** **Given** the server rejects the bookmark permanently (e.g. `404`, article deleted), **When** the sync runs, **Then** the local row is **reverted** and a conflict is surfaced (banner/snackbar) — the DB never silently diverges.
- **AC-2.4 (idempotent retry):** **Given** the sync worker is killed mid-upload and retried, **When** it runs again, **Then** no duplicate server write occurs and the DB is consistent.

### US-3 — Fast morning catch-up

> *As Skimmer Sam, I want to see what's new since this morning quickly, so that I stay current.*

- **AC-3.1 (delta sync):** **Given** a prior sync cursor, **When** a sync runs, **Then** it requests **only changes since** that cursor (no full re-download) and advances the cursor.
- **AC-3.2 (pull-to-refresh):** **Given** the feed, **When** I pull to refresh, **Then** `syncing` is shown during the refresh and `idle` after, and any error becomes a retryable `error` state — without losing the currently-displayed cached content.

### US-4 — Returning after a day

> *As Returning Rae, I want my bookmarks and place preserved across restarts and flaky 3G, so that I don't lose my work.*

- **AC-4.1 (process death):** **Given** I scrolled the feed, applied a filter, and bookmarked an item, **When** the process is killed and restored (`Don't keep activities` / system kill), **Then** the filter, scroll position intent, and bookmark state are all restored — no lost work, no crash.
- **AC-4.2 (durable cache):** **Given** the app was force-stopped, **When** I reopen offline, **Then** previously-fetched articles and bookmarks are still present (Room persisted).

### US-5 — Honest empty & error states

> *As any user, I want the app to tell me the truth when there's nothing or something's wrong, so that I trust it.*

- **AC-5.1 (first-launch empty):** **Given** a fresh install with **no cache and no network**, **When** I open the feed, **Then** a distinct *first-run* empty state explains there's nothing yet and offers retry — **not** the "offline, showing cached" treatment.
- **AC-5.2 (error is retryable):** **Given** a refresh fails, **When** the error surfaces, **Then** it is non-destructive (cached content stays) and offers a **Retry**.
- **AC-5.3 (search empty):** **Given** a query matching nothing in cache, **When** results render, **Then** a search-specific empty state distinguishes "no matches" from "no data".

---

## 5. Definition of Done (the acceptance gate)

The capstone is **done** only when **every** box is checked. These mirror the [Module 19 acceptance criteria](../../modules/module-19-production-app/README.md) and expand them into verifiable checks.

- [ ] **Works offline.** With airplane mode on from a cold start (warm cache), the feed, detail, bookmarks, and search are all fully usable. *Verify:* enable airplane mode → open app → read + bookmark + filter; everything works (the airplane-mode test from [Module 13 · L07](../../modules/module-13-architecture/07-offline-first.md)).
- [ ] **Survives process death.** State (filter, selection, in-flight UI) is restored after a system-initiated kill. *Verify:* enable Developer Options → *Don't keep activities*; set state; background/foreground; assert restoration (`SavedStateHandle` / `rememberSaveable`, per [Module 03 — State Management](../../modules/module-03-state-management/README.md)).
- [ ] **All UI states handled.** Every screen renders **loading · content · empty · error**, with first-launch-empty ≠ offline-cached, proven by screenshot tests across light/dark.
- [ ] **Single source of truth.** The UI reads **only** from Room; no Composable or ViewModel calls the network for display. *Verify:* grep/architecture-test that no `:feature:*` imports `NewsApi`; the UI observes `Flow` from the repository.
- [ ] **Optimistic writes are safe.** Bookmarks are instant, marked with a `syncState`, retried idempotently, and **rolled back** on permanent failure (no silent divergence).
- [ ] **Background sync is correct.** WorkManager job is **idempotent**, **delta-synced** (persisted cursor), maps **transient→`retry()`** / **permanent→`failure()`**, uses **unique work** + a `CONNECTED` constraint + exponential backoff.
- [ ] **Tests green in CI.** Unit (ViewModels/flows via Turbine + MockK), Compose UI (semantics), integration (nav + fakes), and screenshot (Roborazzi) all pass on every PR; CI is the **required check** for merge (per [Module 14](../../modules/module-14-testing/README.md) + [Module 19 · L08](../../modules/module-19-production-app/08-ci-cd-monitoring.md)).
- [ ] **Baseline Profile shipped.** A Macrobenchmark generates the profile **and** it is wired into the release (`baselineProfile(...)` + ProfileInstaller) and verified present in the `.aab`.
- [ ] **Release is shippable.** Signed App Bundle, R8 + resource shrinking on, **R8 mapping uploaded** to Crashlytics (deobfuscated traces), secrets only in CI Secrets.
- [ ] **Static analysis clean.** Detekt + Android Lint pass with zero new warnings on the changed surface (per [Module 17 — Code Quality](../../modules/module-17-code-quality/README.md)).
- [ ] **Accessibility baseline.** Content descriptions on images/icons, semantics on actionable nodes, 48dp touch targets, passes the Accessibility Scanner on the feed and detail screens.

---

## 6. Quality bar & non-functional requirements

| Dimension | Target |
|---|---|
| **Cold start (warm cache)** | Feed's first content frame is visibly instant; Baseline Profile shipped to keep it that way. Measured by Macrobenchmark, not vibes. |
| **Scroll** | No dropped frames on a mid-tier device while flinging the feed (Macrobenchmark `FrameTimingMetric`). Strong Skipping on; immutable list state. |
| **Min SDK / Target SDK** | `minSdk 24`, `targetSdk` = latest stable (per [Module 15](../../modules/module-15-modern-android-2026/README.md)). |
| **Crash-free users** | ≥ 99% on the internal track before promoting a staged rollout. |
| **Determinism** | No real network in tests; fakes/MockK only — a flaky test is a P1, not a nuisance. |

---

## 7. Risks & explicit decisions

- **Conflict policy is chosen, not defaulted:** **last-write-wins by `updatedAt`** for article content and bookmark state. News is single-user, independent data; LWW is the deliberate, documented choice (collaborative CRDTs are a non-goal). Every entity stores `updatedAt`/`version` so conflicts are *detectable* at all.
- **Outbox ordering:** bookmark writes drain in dependency order; a create-then-edit never uploads the edit first.
- **API instability:** the data layer maps DTO→entity→domain at every boundary, so a renamed API field is a one-mapper fix and never reaches the UI ([Module 13 · L01](../../modules/module-13-architecture/01-clean-architecture-layers.md)).
- **Empty-vs-offline confusion** is the most common offline-first UX bug; it is called out as its own acceptance criterion (AC-5.1) so it can't be skipped.

---

➡️ Next: the build order in **[`milestones.md`](milestones.md)**, then the code shape in **[`architecture.md`](architecture.md)**.
