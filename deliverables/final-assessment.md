# Final Assessment — Jetpack Compose Masterclass (2026 Edition)

> The capstone evaluation. It is **practical and project-based** — it proves you can *build, measure, test, and defend* a production Android app, not just recall how. Where the [Certification Exam](certification-exam.md) tests reasoning, this tests delivery.

**Format:** project submission + written artifacts, graded against a rubric. · **Pass bar: 80% overall, with no single dimension below its floor (see [Gate](#pass-gate-hard-requirements)).**

This assessment is built on top of the **[Module 19 — Production App](../modules/module-19-production-app/README.md)** capstone and reaches the depth set by the course exemplar, **[Module 03 — State Management](../modules/module-03-state-management/README.md)**.

---

## What you're proving

You ship one real app and five artifacts that demonstrate, with **evidence**, that you can:

1. Build a correct, offline-first Compose app with a clean single source of truth and UDF.
2. Structure it with real architectural boundaries (Clean Architecture + MVI).
3. **Measure** performance and prove a win — not claim one.
4. Test every layer with the right tool, green in CI.
5. Secure user data against the OWASP Mobile Top 10.
6. Keep the codebase clean enough that a reviewer can read it.

> The theme of the whole course holds here too: **AI drafts, you decide.** You may use the agentic workflow from [Module 16](../modules/module-16-ai-powered-dev/README.md) to scaffold — but every measurement, security decision, and architectural defense must be *yours*, and you must be able to explain any line a reviewer points at.

---

## Submission requirements

You submit **one Git repository** (with history) plus the artifacts below. Each artifact maps to modules you've completed.

### 1. The capstone app — [Module 19](../modules/module-19-production-app/README.md)

A complete, runnable app (e.g. a news / finance / fitness / saved-reader client) meeting Module 19's acceptance criteria.

**Required stack (2026-idiomatic):**
- Compose + **Material 3**; Strong Skipping on; `collectAsStateWithLifecycle`.
- **Type-safe Navigation** (serialization routes).
- **Room** (local source of truth) + **Retrofit/Ktor** + **kotlinx.serialization**.
- **Hilt** for DI; **WorkManager** for background sync.
- **Coroutines + Flow**, with `Dispatchers` discipline (main-safety).
- Immutable UI state (`@Immutable` `UiState`), immutable collections (`ImmutableList`).

**Functional acceptance criteria (all must hold):**
- [ ] **Works offline** — the local DB is the single source of truth; the network only syncs into it; the UI reads only the DB.
- [ ] **Survives process death** — restore the screen via `SavedStateHandle`/`rememberSaveable`; nothing critical is lost.
- [ ] **All UI states handled** — loading, error, empty, and content for every screen (no blank/stuck states).
- [ ] **Single source of truth** — no entity is stored in two places that can disagree; derived values are derived.
- [ ] **Background sync** — WorkManager with constraints + backoff; offline mutations queue and reconcile.
- [ ] **Baseline profile shipped** — generated and included in the release build.

### 2. Measured performance report — [Module 11](../modules/module-11-performance/README.md)

A short report (1–3 pages + raw artifacts) that **proves** a performance result with data:

- [ ] **Before/after recomposition counts** for at least one hot screen (Layout Inspector composition counts or composition tracing), showing the unstable-type/unkeyed-list fix and the drop.
- [ ] **A Macrobenchmark comparison** — startup (cold) and/or scroll **frame timing** (`frameDurationCpuMs` P50/P90/P99), before vs after, on a real device or emulator with the methodology stated.
- [ ] **Baseline profile impact** — startup with vs without the baseline profile.
- [ ] **Methodology** — device, build type (release/minified), iteration count, and what changed between runs. Numbers without methodology don't count.

> A claim like "I made it faster" with no measurement scores **zero** on the Performance dimension. The whole point of Module 11 is *data, not guesses*.

### 3. Test suite — [Module 14](../modules/module-14-testing/README.md)

Green in CI, covering the testing pyramid:

- [ ] **Unit tests** — at least one ViewModel/state flow tested with **Turbine + MockK** + coroutine test (assert state transitions, not implementation details).
- [ ] **Compose UI tests** — semantics-based (`createComposeRule`, finders, actions) for a key screen, including an error/empty state.
- [ ] **At least one screenshot test** — Paparazzi/Roborazzi, deterministic.
- [ ] **At least one Macrobenchmark** — startup or scroll, wired as a runnable benchmark.
- [ ] **CI green** — a GitHub Actions (or equivalent) run that builds, runs unit + UI tests, and reports status. Link the green run.

### 4. One-page architecture write-up — [Module 13](../modules/module-13-architecture/README.md)

**Exactly one page** defending your design. It must cover:

- [ ] **Layer boundaries** — UI / domain / data, and how the **dependency rule** (dependencies point inward) is enforced (module graph or package rule).
- [ ] **State model** — your `UiState` shape, how UDF/MVI flows, and where the single source of truth lives.
- [ ] **Offline-first strategy** — DB-as-truth, sync mechanism, and your **named conflict-resolution policy** with its trade-off.
- [ ] **One trade-off you'd revisit** — an honest "if I had more time / at 10× scale, I'd change X because Y." (Seniority shows in knowing the limits of your own design.)

### 5. OWASP security checklist — [Module 18](../modules/module-18-security/README.md)

Your app audited against the **OWASP Mobile Top 10**, as a filled-in checklist (not a generic copy). For each risk: **status** (mitigated / N/A / accepted-risk) and **where in the code** it's handled.

| OWASP Mobile risk | What to demonstrate in your app |
|---|---|
| M1 Improper credential usage | No hardcoded secrets/keys; tokens not in source or plaintext prefs. |
| M2 Inadequate supply-chain security | Pinned dependencies; no abandoned/unverified libs for security-critical paths. |
| M3 Insecure auth/authz | Sessions/tokens handled correctly; biometric/refresh handled per [Lesson 05](../modules/module-18-security/05-authentication-authorization.md). |
| M4 Insufficient input/output validation | Validate server input; safe deserialization. |
| M5 Insecure communication | TLS enforced; **certificate pinning** decision stated; no cleartext traffic. |
| M6 Inadequate privacy controls | Minimal data collection; no PII in logs. |
| M7 Insufficient binary protection | R8/minify on; no debug logging of secrets in release. |
| M8 Security misconfiguration | `network_security_config`; `allowBackup`/exported components reviewed. |
| M9 Insecure data storage | **Keystore-backed** encrypted storage for tokens/secrets; nothing sensitive in plain prefs/DB. |
| M10 Insufficient cryptography | Use platform crypto correctly; no home-rolled crypto; proper key management. |

> On crypto specifically: **never trust AI blindly** — you own these decisions ([Module 18 AI focus](../modules/module-18-security/README.md)).

### Code quality gate — [Module 17](../modules/module-17-code-quality/README.md)

- [ ] **Detekt** + **Ktlint** (and Android Lint) run in CI; **no Detekt errors**.
- [ ] No god composables, no state in the wrong place, no modifier soup (the Module 17 smells).

---

## Submission checklist (paste into your PR description)

```text
[ ] Repo link with commit history
[ ] App runs; release build installs
[ ] Offline mode demonstrated (screen recording or steps)
[ ] Process-death survival demonstrated (steps)
[ ] All loading/error/empty states reachable (how to reach each)
[ ] Performance report (before/after recomposition + Macrobenchmark + methodology)
[ ] Tests: unit + UI + screenshot + macrobenchmark — link to green CI run
[ ] One-page architecture write-up
[ ] OWASP Mobile Top 10 checklist (status + code locations)
[ ] Detekt/Ktlint clean (link to CI)
[ ] Baseline profile present in release build
```

---

## Scoring rubric

Six weighted dimensions. Each is scored on a **0–4 level scale**; the dimension's points = (level ÷ 4) × its weight. **Pass at 80/100 overall**, subject to the [hard gate](#pass-gate-hard-requirements).

| # | Dimension | Weight | Grounded in |
|---|---|---|---|
| 1 | Correctness & state management | 25 | [M03](../modules/module-03-state-management/README.md), [M06](../modules/module-06-side-effects/README.md) |
| 2 | Architecture & boundaries | 20 | [M13](../modules/module-13-architecture/README.md) |
| 3 | Performance (measured) | 20 | [M11](../modules/module-11-performance/README.md), [M12](../modules/module-12-internals/README.md) |
| 4 | Testing | 15 | [M14](../modules/module-14-testing/README.md) |
| 5 | Security | 10 | [M18](../modules/module-18-security/README.md) |
| 6 | Code quality | 10 | [M17](../modules/module-17-code-quality/README.md) |
| | **Total** | **100** | |

**Level scale:** **0** Missing · **1** Beginner (present but flawed) · **2** Competent (works, gaps) · **3** Proficient (solid, idiomatic) · **4** Exemplary (the quality bar of [Module 03](../modules/module-03-state-management/README.md)).

---

### Dimension 1 — Correctness & state management (25 pts)

| Level | Descriptor |
|---|---|
| **4 — Exemplary** | Flawless UDF: one immutable `UiState` per screen via a `StateFlow`, `collectAsStateWithLifecycle`. Survives rotation **and** process death with no loss. All loading/error/empty/content states handled everywhere. Derived values derived (no drift). Effects keyed correctly, lifecycle-safe, no leaks. Offline works because the DB is the sole source of truth. |
| **3 — Proficient** | Solid UDF and single source of truth; survives process death; states handled on main flows; effects mostly keyed correctly. Minor: a derived value stored once, or one screen missing an empty state. |
| **2 — Competent** | Works in the happy path; survives rotation but maybe not process death; some states unhandled; one half-hoisting or wrong-key effect bug. |
| **1 — Beginner** | Frequent state bugs: values reset, stale UI, missing states, leaked mutable state from a ViewModel. |
| **0** | Doesn't run, or no coherent state model. |

**Auto-deductions:** unremembered `mutableStateOf`, mutable state leaked from a ViewModel, `collectAsState` (not lifecycle-aware) on a hot screen, a stored value that should be derived, an effect keyed on `Unit` that needs an input key.

---

### Dimension 2 — Architecture & boundaries (20 pts)

| Level | Descriptor |
|---|---|
| **4 — Exemplary** | Clean separation of UI / domain / data with the **dependency rule** enforced at **build time** (`:feature:*`, `:core:*` modules). Repository is the single source of truth; use cases encapsulate rules; no data/network models leak into the UI; offline-first with an explicit, defensible **conflict-resolution policy**. The one-page write-up is crisp and honest about a trade-off. |
| **3 — Proficient** | Clear layers (at least package-enforced), repository pattern, UDF/MVI, offline-first with a stated conflict policy. Write-up covers boundaries + state model. |
| **2 — Competent** | Layers exist but leak (e.g. DTOs reach the UI, or the ViewModel calls Retrofit directly); offline-first partial. |
| **1 — Beginner** | God classes; UI talks to the network; no real boundaries. |
| **0** | No architecture; logic in composables. |

**Auto-deductions:** UI depends on a data/network model; ViewModel performs I/O without a repository; dependency rule violated (inner layer importing an outer one); no conflict policy stated for editable data.

---

### Dimension 3 — Performance, **measured** (20 pts)

| Level | Descriptor |
|---|---|
| **4 — Exemplary** | A complete before/after story **with data**: recomposition counts dropped via a real stability/skipping fix (unstable type → `ImmutableList`/`@Immutable`, or unkeyed list → keyed + `contentType`); Macrobenchmark frame timing (P50/P90/P99) and cold-start improved; baseline profile impact quantified; deferred reads where appropriate. Methodology fully stated (device, release build, iterations). Conclusions match the numbers. |
| **3 — Proficient** | A real measured win on at least one screen + a Macrobenchmark, with methodology. Baseline profile shipped. |
| **2 — Competent** | Some measurement (e.g. recomposition counts) but thin Macrobenchmark or weak methodology; baseline profile present. |
| **1 — Beginner** | Performance "improvements" asserted with little/no measurement. |
| **0** | No measurement at all. |

**Hard rule:** an unmeasured performance claim scores **0** on this dimension regardless of how fast the app feels — Module 11's entire discipline is *evidence, not guesses*.

---

### Dimension 4 — Testing (15 pts)

| Level | Descriptor |
|---|---|
| **4 — Exemplary** | The pyramid, done right: ViewModel/state tested with **Turbine + MockK** asserting state transitions; semantics-based Compose UI tests covering content **and** error/empty; a deterministic screenshot test; a Macrobenchmark. Tests assert behavior (not brittle selectors or implementation details). **CI green**, linked. |
| **3 — Proficient** | Unit + UI + one screenshot + one macrobenchmark, green in CI; mostly behavior-focused. |
| **2 — Competent** | Unit + some UI tests; missing screenshot or macrobenchmark; CI runs. |
| **1 — Beginner** | A few brittle/implementation-coupled tests; CI flaky or absent. |
| **0** | No meaningful tests. |

**Auto-deductions:** tests assert internal implementation rather than observable state; UI tests rely on indices/coordinates instead of semantics; no error/empty state tested; CI not green.

---

### Dimension 5 — Security (10 pts)

| Level | Descriptor |
|---|---|
| **4 — Exemplary** | Full OWASP Mobile Top 10 checklist with per-risk status **and code locations**. Tokens/secrets in **Keystore-backed** encrypted storage; no hardcoded secrets; TLS enforced with a **stated** cert-pinning decision; minify on; no PII in logs; crypto uses the platform correctly. Risk acceptances are explicit and justified. |
| **3 — Proficient** | Checklist complete; secure storage + TLS + no hardcoded secrets demonstrated; most risks addressed with locations. |
| **2 — Competent** | Checklist present but partly generic; secure storage in place but one gap (e.g. PII in logs, no pinning decision). |
| **1 — Beginner** | Minimal security; a hardcoded secret or plaintext token storage present. |
| **0** | No security consideration; sensitive data in plain prefs/logs. |

**Auto-fail of this dimension:** any **hardcoded secret/API key** in source, or a refresh/access token stored in plaintext `SharedPreferences`/DB — both are the canonical Module 18 failures.

---

### Dimension 6 — Code quality (10 pts)

| Level | Descriptor |
|---|---|
| **4 — Exemplary** | **Detekt/Ktlint/Lint clean** in CI (no errors). Composables have single responsibilities; state lives in the right place; no modifier soup; SOLID/KISS/DRY/YAGNI applied without over-abstraction. Reads cleanly cold. |
| **3 — Proficient** | Static analysis green; few smells; readable. |
| **2 — Competent** | Some Detekt warnings; a couple of god composables or DRY violations. |
| **1 — Beginner** | Static analysis failing or not configured; pervasive smells. |
| **0** | Unreadable; no static analysis. |

**Auto-deductions:** Detekt errors present; a god composable (hundreds of lines, many responsibilities); over-abstraction (interfaces/indirection with one impl and no need).

---

## Pass gate (hard requirements)

Scoring ≥ 80 is necessary but **not sufficient**. To pass, **all** of these must also be true (each is a course-defining acceptance criterion):

- [ ] **App works offline** (DB is source of truth).
- [ ] **Survives process death.**
- [ ] **All UI states handled** (loading/error/empty/content).
- [ ] **CI is green** (build + tests).
- [ ] **Baseline profile shipped.**
- [ ] **No Detekt errors.**
- [ ] **No hardcoded secrets; no plaintext token storage.**
- [ ] **At least a Competent (2) on every dimension** — no dimension may be 0 or 1.

If the total is ≥ 80 but any gate item fails, the result is **"Revise & resubmit"** with the specific gate item flagged. This mirrors a real PR review: strong overall work still doesn't merge with a shipped secret or a red pipeline.

---

## Worked grading example (illustrative)

> A candidate submits a saved-articles reader.

| Dimension | Level | Notes | Points |
|---|---|---|---|
| Correctness & state | 4 | Immutable `UiState`, survives process death, all states handled, derived totals. | 25.0 |
| Architecture | 3 | Clean layers (package-enforced, not multi-module), LWW conflict policy stated. | 15.0 |
| Performance (measured) | 4 | `List`→`ImmutableList` fix dropped `ArticleCard` recompositions; Macrobenchmark P90 frame time and cold start improved; methodology stated. | 20.0 |
| Testing | 3 | Turbine VM tests + semantics UI tests + 1 screenshot + 1 macrobenchmark; CI green. | 11.25 |
| Security | 3 | Tokens in Keystore-backed storage; full checklist; pinning decision stated; one PII-in-log gap noted. | 7.5 |
| Code quality | 3 | Detekt clean; one borderline large composable. | 7.5 |
| **Total** | | | **86.25 / 100** |

Gate: offline ✓, process death ✓, states ✓, CI green ✓, baseline profile ✓, no Detekt errors ✓, no secrets ✓, every dimension ≥ 2 ✓ → **PASS (86%)**.

---

## Result & certification

- **Total:** ___ / 100 (**Pass ≥ 80** + all gate items)
- **Gate:** ☐ all hard requirements met
- **Verdict:** ☐ Pass ☐ Revise & resubmit

A pass certifies you can **deliver** a production-grade Compose app — measured, tested, secured, and defensible — at the standard this course sets.

> **Full Masterclass certification requires both this Final Assessment *and* the [Certification Exam](certification-exam.md).** The exam proves you can reason; this proves you can build. Together they mirror a real senior Android loop: a knowledge screen *and* a portfolio/system-design bar.

➡️ Related: [Capstone project spec](capstone-project/) · [Module 19 — Build a Production App](../modules/module-19-production-app/README.md) · [Module 20 — Career & Interview Prep](../modules/module-20-career-interview/README.md)
