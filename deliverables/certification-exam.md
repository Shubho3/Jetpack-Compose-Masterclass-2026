# Certification Exam — Jetpack Compose Masterclass (2026 Edition)

> The timed exam that certifies completion of the Masterclass. It proves you can **reason** about Compose — recomposition, state, performance, architecture, security — not just recognize syntax.

**Pass bar: 80%.** · **Time: 120 minutes.** · **Open-docs, not open-AI** (official Android/Kotlin docs allowed; no LLMs, no peers).

This exam draws its depth from the fully-written modules. The exemplar is **[Module 03 — State Management](../modules/module-03-state-management/README.md)**; every question here is answerable from the module READMEs and lessons. Where a question maps to a module, the module is linked.

---

## How this exam is structured

| Part | Content | Items | Points | Weight |
|---|---|---|---|---|
| **A** | Multiple-choice, grouped by area | 50 MCQ | 50 | 50% |
| **B** | Practical: spot-the-bug / code-fix | 5 tasks | 30 | 30% |
| **C** | Senior system design | 1 prompt | 20 | 20% |
| | **Total** | | **100** | **100%** |

**Scoring.** Each MCQ is 1 point. Each practical task is 6 points (graded by the rubric in Part B). The design prompt is 20 points (graded by the rubric in Part C). **You pass at 80/100.** There is no negative marking — answer every question.

**Suggested time budget:** Part A 45 min · Part B 45 min · Part C 30 min.

> **Integrity note.** This is a *thinking* exam. The MCQ distractors are real misconceptions taught against in the course; the practical tasks are bugs every Compose developer ships at least once. Closed-AI is the point — an interviewer will not let you prompt a model mid-question.

---

# Part A — Multiple Choice (50 questions, 50 points)

Choose the single best answer. Questions are grouped by area; the answer key with one-line rationales is at the end of this document.

## A1 · Fundamentals & the declarative model — Modules [01](../modules/module-01-introduction/README.md), [02](../modules/module-02-layouts/README.md) (Q1–Q10)

**Q1.** In Compose, the relationship between UI and state is best summarized as:
- A. `state = f(UI)`
- B. `UI = f(state)` — UI is re-derived from state
- C. UI and state are mutated together, imperatively
- D. State is a side effect of UI events

**Q2.** "Recomposition" means:
- A. The app process restarts
- B. Compose re-runs the composable functions that read state which changed
- C. The view hierarchy is rebuilt from XML
- D. The Activity is recreated on configuration change

**Q3.** Which statement about the **declarative** mindset is correct?
- A. You call `findViewById` and mutate widgets in response to events
- B. You describe UI for a given state; you do **not** imperatively mutate views
- C. You must manually diff old and new UI trees yourself
- D. Declarative UI cannot interoperate with the View system

**Q4.** A `@Composable` function should:
- A. Return a `View` object
- B. Return `Unit`, be PascalCase, and be side-effect-free in the composition path
- C. Perform network calls directly in its body
- D. Always be `private` and `suspend`

**Q5.** The three phases of a Compose frame, in order, are:
- A. Draw → Measure → Composition
- B. Composition → Layout (measure/place) → Drawing
- C. Layout → Composition → Drawing
- D. Measure → Composition → Place

**Q6.** Why does a `LazyColumn` outperform a `Column` with a `verticalScroll` for a long list?
- A. `Column` cannot scroll at all
- B. `LazyColumn` only composes and lays out the items currently visible (plus a small buffer)
- C. `LazyColumn` runs entirely off the main thread
- D. `Column` re-measures every frame but `LazyColumn` never measures

**Q7.** In a `LazyColumn`, providing a stable `key` for each item primarily:
- A. Sorts the list automatically
- B. Lets Compose preserve item state and animate correctly when the list changes
- C. Disables recomposition for that item forever
- D. Is required or the list will not compile

**Q8.** `contentType` in a Lazy list is used to:
- A. Force all items to the same height
- B. Let the runtime reuse compositions across items of the same type, reducing work
- C. Set the MIME type for image loading
- D. Replace the need for a `key`

**Q9.** Window Size Classes (`Compact` / `Medium` / `Expanded`) are the recommended way to:
- A. Detect the exact device model
- B. Make a layout adaptive across phones, foldables, tablets, and desktop using coarse breakpoints
- C. Measure recomposition counts
- D. Choose between light and dark themes

**Q10.** `Scaffold` exists to:
- A. Replace the need for a `ViewModel`
- B. Provide standard app structure slots (top bar, FAB, snackbar host, content) and handle insets
- C. Lazily load list items
- D. Persist state across process death

---

## A2 · State management — Module [03](../modules/module-03-state-management/README.md) (Q11–Q20)

**Q11.** What does `remember` do?
- A. Persists state across process death
- B. Caches a value across recompositions so it isn't recomputed each time
- C. Makes a value observable
- D. Survives configuration changes by itself

**Q12.** `var count = mutableStateOf(0)` written **without** `remember` inside a composable will:
- A. Survive rotation
- B. Reset to `0` on every recomposition
- C. Throw a compile error
- D. Work correctly, because `mutableStateOf` already remembers

**Q13.** The difference between `remember` and `rememberSaveable` is:
- A. `rememberSaveable` additionally survives configuration change and process death (via a `Bundle`/`Saver`)
- B. `remember` survives process death; `rememberSaveable` does not
- C. They are identical
- D. `rememberSaveable` only works for `Int`

**Q14.** State hoisting means:
- A. Moving state **up** to a caller so the composable becomes stateless (`value` down, events up)
- B. Caching state on disk
- C. Moving state into a `CompositionLocal`
- D. Deferring a state read into the draw phase

**Q15.** A **stateless** composable is desirable because it is:
- A. Faster to compile
- B. Reusable, previewable in any state, and testable by passing values
- C. Automatically thread-safe
- D. Exempt from recomposition

**Q16.** You should hoist a piece of state to:
- A. The application root, always
- B. The lowest common ancestor of every composable that reads or writes it
- C. A global singleton
- D. The deepest leaf that uses it

**Q17.** A "half-hoisting" bug occurs when a composable:
- A. Has no parameters at all
- B. Takes `value` as a parameter but **also** keeps its own internal `remember`ed copy, so the two desync
- C. Hoists state too high
- D. Uses `rememberSaveable` instead of `remember`

**Q18.** A screen's total (e.g. a cart total) should be:
- A. Stored as its own `mutableStateOf` and updated manually
- B. **Derived** from the source state so it cannot drift out of sync
- C. Recomputed in a `LaunchedEffect`
- D. Kept in a `CompositionLocal`

**Q19.** To avoid callers mutating a ViewModel's source of truth, you should expose:
- A. A `MutableStateFlow` directly
- B. A read-only `StateFlow` (or `State`), mutating internally only
- C. A public `var`
- D. A `CompositionLocal`

**Q20.** From the UI, the correct way to collect a ViewModel `StateFlow` is:
- A. `collectAsState()` always
- B. `collectAsStateWithLifecycle()` so collection stops when the UI is not at least `STARTED`
- C. `flow.value` polled in a loop
- D. `LaunchedEffect { flow.collect { } }` with no lifecycle awareness

---

## A3 · Modifiers, layouts & graphics — Modules [04](../modules/module-04-modifiers/README.md), [05](../modules/module-05-custom-layouts/README.md), [08](../modules/module-08-canvas-graphics/README.md) (Q21–Q28)

**Q21.** Modifier **order** matters because:
- A. Modifiers are sorted alphabetically at runtime
- B. Each modifier wraps the next; e.g. `padding` then `background` paints the background **inside** the padding, while `background` then `padding` paints it **outside**
- C. Only the first modifier in a chain is applied
- D. Order only affects accessibility, not layout

**Q22.** `Modifier.size(48.dp)` vs `Modifier.requiredSize(48.dp)`:
- A. They are identical
- B. `size` is a *preferred* size the parent can override via constraints; `requiredSize` forces the size, ignoring incoming constraints
- C. `requiredSize` is deprecated
- D. `size` ignores the parent's constraints

**Q23.** To observe a `clickable`'s pressed/hovered state for custom visuals, you:
- A. Read a global variable
- B. Pass a `MutableInteractionSource` and collect its interactions (e.g. `collectIsPressedAsState()`)
- C. Override `onTouchEvent`
- D. Use `rememberSaveable`

**Q24.** When handling raw gestures with `pointerInput`, forgetting to call `consume()` on a change typically causes:
- A. A compile error
- B. The gesture to also be handled by parent/ancestor handlers (e.g. a parent scroll steals it)
- C. The app to crash
- D. The pointer event to be dropped entirely

**Q25.** Compose layouts measure each child **once** per layout pass primarily to:
- A. Save memory
- B. Guarantee linear-time layout and avoid the exponential cost of multi-pass measurement
- C. Support XML interop
- D. Allow infinite constraints

**Q26.** Using **intrinsic measurements** has a cost because:
- A. They never terminate
- B. They run an extra measurement pass to query a child's intrinsic size before the real measure
- C. They allocate a new thread
- D. They disable skipping

**Q27.** You'd reach for `SubcomposeLayout` (over a plain `Layout`) when:
- A. You never need it; `Layout` always suffices
- B. The composition of some children must **depend on the measured size** of others
- C. You want to draw custom graphics
- D. You need to survive process death

**Q28.** In the draw phase, reading a frequently-changing value **inside** a `drawBehind { }`/`Canvas` lambda (rather than in composition) is good because:
- A. It makes the value immutable
- B. The read is deferred to draw, so a change skips recomposition and layout — only redraw runs
- C. It moves work off the main thread
- D. It is required for `graphicsLayer`

---

## A4 · Side effects, animation, theming & CompositionLocal — Modules [06](../modules/module-06-side-effects/README.md), [07](../modules/module-07-compositionlocal/README.md), [09](../modules/module-09-material3-theming/README.md), [10](../modules/module-10-animations/README.md) (Q29–Q38)

**Q29.** Side effects must be quarantined from the composition path because composition is:
- A. Always single-threaded and ordered
- B. Frequent, can run in any order, may be skipped or cancelled, and can run in parallel — so unguarded effects would run unpredictably
- C. Run only once per screen
- D. Performed on a background thread

**Q30.** Changing the **key** of a `LaunchedEffect` causes Compose to:
- A. Ignore the change
- B. Cancel the running coroutine and relaunch the effect with the new key
- C. Crash if the key is a `String`
- D. Defer the effect to the draw phase

**Q31.** To launch a coroutine from a **callback** (e.g. a button's `onClick`, not from composition), you use:
- A. `LaunchedEffect(Unit)`
- B. `rememberCoroutineScope()`
- C. `produceState`
- D. `SideEffect`

**Q32.** `DisposableEffect` is the right tool when you must:
- A. Compute a derived value
- B. Register something and **clean it up** when the composable leaves or a key changes (e.g. add/remove a listener)
- C. Publish to a non-Compose object every recomposition
- D. Turn a `Flow` into `State`

**Q33.** `rememberUpdatedState` is used to:
- A. Persist state to disk
- B. Capture the **latest** value inside a long-lived effect **without** restarting that effect
- C. Replace `remember`
- D. Make a `List` stable

**Q34.** `derivedStateOf` is preferable to a plain computation when:
- A. You never read other state
- B. You compute a value from frequently-changing state but the **result** changes rarely, so you want to avoid recomposing on every input change
- C. You need to survive process death
- D. You want to run a coroutine

**Q35.** `staticCompositionLocalOf` differs from `compositionLocalOf` in that, when its value changes:
- A. Only composables that **read** the local recompose
- B. The **entire** subtree under the provider recomposes (no read-tracking) — so it's for rarely/never-changing values
- C. Nothing recomposes
- D. It throws

**Q36.** A good reason to prefer **dependency injection** over a `CompositionLocal` for a dependency is:
- A. CompositionLocal cannot hold objects
- B. CompositionLocal creates an implicit dependency that hurts testability and hides coupling; DI makes dependencies explicit
- C. DI is faster at runtime
- D. CompositionLocal does not work in previews

**Q37.** In Material 3, you should style with **color roles** (e.g. `primary`, `surface`, `onSurface`) rather than hardcoded colors because:
- A. Hardcoded colors don't compile
- B. Roles adapt to light/dark and dynamic color, and keep contrast correct across themes
- C. Roles are faster to render
- D. Roles disable recomposition

**Q38.** `animate*AsState` vs `Animatable`:
- A. They are identical
- B. `animate*AsState` is fire-and-forget for a target value; `Animatable` gives precise, interruptible, gesture-driven control (e.g. `snapTo`, `animateTo`)
- C. `Animatable` cannot be interrupted
- D. `animate*AsState` runs on a background thread

---

## A5 · Performance & internals — Modules [11](../modules/module-11-performance/README.md), [12](../modules/module-12-internals/README.md) (Q39–Q45)

**Q39.** A type is **unstable** to the Compose compiler when:
- A. It is a primitive
- B. It might change without notifying Compose — e.g. a `List` interface (could be a mutable `ArrayList`), a `var` field, or a type from a module not compiled with the Compose plugin
- C. It is annotated `@Immutable`
- D. It is a `String`

**Q40.** `@Immutable` vs `@Stable`:
- A. `@Immutable` allows mutation; `@Stable` forbids it
- B. `@Immutable` promises the object never changes after construction; `@Stable` promises changes happen **only through Compose `State`**
- C. They are interchangeable
- D. Both are deprecated under Strong Skipping

**Q41.** Annotating a class `@Immutable` when it actually holds a `MutableList` causes:
- A. A compile error
- B. **Under-recomposition** — Compose trusts the annotation, skips, and the UI silently shows stale data
- C. Over-recomposition only
- D. Nothing; the annotation is ignored

**Q42.** Under **Strong Skipping** (the 2026 default), a composable with an **unstable** parameter:
- A. Can never be skipped
- B. Becomes skippable using **referential (instance) equality** for that param — so reallocating a new instance each frame still breaks skipping
- C. Always crashes
- D. Ignores the parameter entirely

**Q43.** The **slot table** is best described as:
- A. A database table in Room
- B. The runtime's positional memory of the composition — where `remember`ed values and group data live
- C. A thread pool
- D. The list of pending recompositions

**Q44.** The snapshot system gives Compose state:
- A. Disk persistence
- B. MVCC-style isolation — reads are tracked, writes are applied atomically, and concurrent readers see a consistent view
- C. Encryption at rest
- D. Automatic pagination

**Q45.** To defer a state read out of composition for a frequently-changing value (e.g. scroll offset driving an offset/alpha), you should:
- A. Read it directly in the composable body
- B. Use a **lambda-based** modifier (e.g. `Modifier.offset { }` / `graphicsLayer { }`) so the read happens at layout/draw, not composition
- C. Wrap it in `rememberSaveable`
- D. Move it into a `CompositionLocal`

---

## A6 · Architecture, testing, security & MAD-2026 — Modules [13](../modules/module-13-architecture/README.md), [14](../modules/module-14-testing/README.md), [15](../modules/module-15-modern-android-2026/README.md), [17](../modules/module-17-code-quality/README.md), [18](../modules/module-18-security/README.md) (Q46–Q50)

**Q46.** In Clean Architecture, the **dependency rule** says dependencies point:
- A. Outward, from domain toward UI
- B. Inward — UI and data depend on the domain; the domain depends on nothing outer (it owns the models and rules)
- C. In both directions freely
- D. From data directly into the UI

**Q47.** "Offline-first" means the single source of truth for the UI is:
- A. The network response
- B. The **local database**; the network is a sync mechanism that writes into the DB, and the UI only reads the DB
- C. A `CompositionLocal`
- D. In-memory state that is lost on process death

**Q48.** Compose **UI tests** primarily assert against:
- A. Pixel colors
- B. The **semantics tree** (nodes, their properties, and actions) via finders like `onNodeWithText`
- C. The slot table directly
- D. Logcat output

**Q49.** Where should a long-lived **refresh token** be stored on Android?
- A. In `SharedPreferences` as plain text
- B. In Keystore-backed encrypted storage (e.g. encrypted DataStore / Keystore-wrapped key) — never plaintext, never hardcoded
- C. Hardcoded in the APK
- D. In a `CompositionLocal`

**Q50.** What did the **K2 compiler / Kotlin 2.x** change for Compose builds?
- A. It removed `@Composable`
- B. The Compose compiler ships as a **Kotlin plugin** (`org.jetbrains.kotlin.plugin.compose`) versioned with Kotlin, replacing the separately-versioned `composeOptions` compiler-extension dance
- C. It made Compose XML-based again
- D. It disabled Strong Skipping

---

# Part B — Practical: spot-the-bug / code-fix (5 tasks, 30 points)

For each task: **(1)** identify the bug in one or two sentences, **(2)** explain the consequence, **(3)** write the corrected code. Each task is **6 points**: 2 for correct diagnosis, 1 for the consequence, 3 for a correct, idiomatic fix.

> Grading rubric (per task): **6** flawless diagnosis + consequence + idiomatic 2026 fix · **4–5** correct fix, minor gaps · **2–3** identifies the bug but the fix is wrong/non-idiomatic · **0–1** misdiagnosis.

---

## Task B1 — State that resets every recomposition

**Buggy snippet:**
```kotlin
@Composable
fun Counter() {
    var count = mutableStateOf(0)          // 🐞
    Button(onClick = { count.value++ }) {
        Text("Count: ${count.value}")
    }
}
```
The button text never increments past `1` (and often appears stuck at `0`). Why, and how do you fix it?

<details>
<summary><strong>Model solution</strong></summary>

**Diagnosis.** `mutableStateOf(0)` is created **without `remember`**. A fresh `MutableState` is allocated on **every recomposition**, so the increment is discarded and the value resets.

**Consequence.** Tapping schedules a recomposition; the recomposition re-creates `count` at `0`, so the UI never reflects the increment. State that isn't `remember`ed is effectively write-only.

**Fix.**
```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }   // remembered across recompositions
    Button(onClick = { count++ }) {
        Text("Count: $count")
    }
}
```
For state that must also survive rotation/process death, use `rememberSaveable { mutableStateOf(0) }`. See [Module 03 · Lesson 02](../modules/module-03-state-management/02-remember-mutablestate.md).
</details>

---

## Task B2 — Half-hoisting: the field that won't clear

**Buggy snippet:**
```kotlin
@Composable
fun SearchField(value: String, onValueChange: (String) -> Unit) {
    var internal by remember { mutableStateOf(value) }     // 🐞 second source of truth
    OutlinedTextField(
        value = internal,
        onValueChange = { internal = it; onValueChange(it) },
    )
}

// Caller:
var query by rememberSaveable { mutableStateOf("") }
Column {
    SearchField(value = query, onValueChange = { query = it })
    Button(onClick = { query = "" }) { Text("Clear") }   // pressing this does NOT clear the field
}
```
Pressing **Clear** sets `query = ""`, but the text field still shows the old text. Why, and how do you fix it?

<details>
<summary><strong>Model solution</strong></summary>

**Diagnosis.** `SearchField` is **half-hoisted**: it accepts `value` but also keeps its own `remember`ed `internal` copy and renders *that*. When the parent changes `value` externally (Clear → `query = ""`), `internal` is not updated, so the field shows stale text — two sources of truth.

**Consequence.** Any external mutation of the hoisted state (reset, programmatic set, restoring saved state) is silently ignored by the field; the UI disagrees with its owner.

**Fix.** A hoisted component must render `value` **directly** and own nothing.
```kotlin
@Composable
fun SearchField(value: String, onValueChange: (String) -> Unit) {
    OutlinedTextField(value = value, onValueChange = onValueChange)
}
```
See [Module 03 · Lesson 04](../modules/module-03-state-management/04-state-hoisting.md) (the "TV and remote" analogy).
</details>

---

## Task B3 — `LaunchedEffect` with the wrong key

**Buggy snippet:**
```kotlin
@Composable
fun UserScreen(userId: String, repo: UserRepository) {
    var user by remember { mutableStateOf<User?>(null) }
    LaunchedEffect(Unit) {                       // 🐞 keyed on Unit
        user = repo.fetchUser(userId)
    }
    UserContent(user)
}
```
The screen loads the first user correctly, but when `userId` changes (the same composable is reused with a new id), it keeps showing the **old** user. Why, and how do you fix it?

<details>
<summary><strong>Model solution</strong></summary>

**Diagnosis.** The effect is keyed on `Unit`, so it runs **once** and never relaunches when `userId` changes. The stale fetch result is kept.

**Consequence.** Navigating to a different user (or any recomposition that swaps `userId` without leaving the composition) never re-fetches; the UI shows data for the previous id. It can also leak the wrong result if the composable is reused across ids.

**Fix.** Key the effect on the input it depends on, so it cancels and relaunches when that input changes.
```kotlin
@Composable
fun UserScreen(userId: String, repo: UserRepository) {
    var user by remember(userId) { mutableStateOf<User?>(null) }  // reset while loading
    LaunchedEffect(userId) {                                      // relaunch on change
        user = repo.fetchUser(userId)
    }
    UserContent(user)
}
```
(In production this state usually lives in a `ViewModel` keyed by `userId`, exposing a `StateFlow<UiState>`.) See [Module 06 · Lesson 02](../modules/module-06-side-effects/02-launchedeffect-and-keys.md).
</details>

---

## Task B4 — Unstable parameter causing constant recomposition

**Buggy snippet:**
```kotlin
// :core:model  (NO Compose compiler plugin applied)
data class Product(
    val id: String,
    val name: String,
    val tags: List<String>,          // 🐞 interface type → unstable
)

// :feature:catalog
@Composable
fun ProductCard(product: Product, onOpen: (String) -> Unit) {
    Card(onClick = { onOpen(product.id) }) {
        Text(product.name)
        Row { product.tags.forEach { Text(it) } }
    }
}
```
`ProductCard` recomposes on **every scroll frame** even though the product data hasn't changed. The Layout Inspector shows high recomposition counts. Why, and how do you make it skippable?

<details>
<summary><strong>Model solution</strong></summary>

**Diagnosis.** `product` is reported **unstable** for two reasons: `tags: List<String>` is an interface (could be a mutable `ArrayList`, so the compiler assumes the worst), and the model lives in a module **not compiled with the Compose compiler plugin**, so the compiler can't infer the class's stability and assumes unstable. An unstable parameter defeats skipping.

**Consequence.** Because the param can't be trusted, `ProductCard` re-runs whenever its parent recomposes (e.g. during scroll), wasting work and causing jank on long lists.

**Fix — at the type and module level (not `remember`):**
```kotlin
// :core:model/build.gradle.kts — let the compiler INFER stability here
plugins { id("org.jetbrains.kotlin.plugin.compose") }

// :core:model
import kotlinx.collections.immutable.ImmutableList
import kotlinx.collections.immutable.persistentListOf

@Immutable
data class Product(
    val id: String,
    val name: String,
    val tags: ImmutableList<String> = persistentListOf(),   // stable collection
)
```
Now `product` is reported `stable`, `ProductCard` becomes `restartable skippable`, and the jank disappears. Verify by re-running the **stability report** and watching recomposition counts drop. See [Module 12 · Lesson 05](../modules/module-12-internals/05-stability-immutability.md) and [Module 11 · Lesson 03](../modules/module-11-performance/03-stability-skipping.md).

**Reject** any "fix" that slaps `@Immutable` on a class still holding `List`/`MutableList`, or that only wraps callsites in `remember` — that trades visible jank for invisible **stale UI**.
</details>

---

## Task B5 — Leaked mutable state from a ViewModel + lifecycle-unaware collection

**Buggy snippet:**
```kotlin
class CartViewModel : ViewModel() {
    val state = MutableStateFlow(CartUiState())     // 🐞 exposed as mutable
    fun add(item: Item) { state.value = state.value.copy(items = state.value.items + item) }
}

@Composable
fun CartScreen(vm: CartViewModel = hiltViewModel()) {
    val state by vm.state.collectAsState()          // 🐞 not lifecycle-aware
    // …renders state…
}
```
Two issues: any caller can mutate `state` directly, and the flow keeps collecting while the screen is in the background. Fix both.

<details>
<summary><strong>Model solution</strong></summary>

**Diagnosis.**
1. `state: MutableStateFlow` is **public**, so any caller can write `vm.state.value = …`, bypassing the ViewModel's logic and breaking the single source of truth.
2. `collectAsState()` is **not lifecycle-aware**; it keeps collecting when the UI is `STOPPED` (backgrounded), wasting work and risking updates to an off-screen UI.

**Consequence.** Truth can be corrupted from outside the ViewModel; background collection burns CPU/battery and can process emissions the user can't see.

**Fix.** Expose a **read-only** `StateFlow`, mutate only internally, and collect with lifecycle awareness.
```kotlin
class CartViewModel : ViewModel() {
    private val _state = MutableStateFlow(CartUiState())
    val state: StateFlow<CartUiState> = _state.asStateFlow()       // read-only to callers

    fun add(item: Item) { _state.update { it.copy(items = it.items + item) } }
}

@Composable
fun CartScreen(vm: CartViewModel = hiltViewModel()) {
    val state by vm.state.collectAsStateWithLifecycle()            // stops when not STARTED
    // …renders state…
}
```
See [Module 03 · Lesson 05](../modules/module-03-state-management/05-udf-mvi-mvvm.md) and [Module 13 · Lesson 02](../modules/module-13-architecture/02-mvvm-in-compose.md).
</details>

---

# Part C — Senior system design (1 prompt, 20 points)

You have **30 minutes**. Design out loud and on a whiteboard (or in writing). You are graded on **reasoning and trade-offs**, not on a perfect drawing.

## The prompt

> **Design an offline-first "saved articles" reader.** Users browse an infinite article feed, tap to read, and **save** articles for offline reading. Saved articles (and read/unread state) must sync across the user's devices and remain available with **no network**. Likes/saves must feel **instant**. Walk through your design end to end and call out where it can fail.

Use the 5-step framework from **[Module 20 · Lesson 04](../modules/module-20-career-interview/04-system-design-for-android.md)**: **Clarify → API → Data → Arch → Scale.**

### Model-answer outline

**1. Clarify (state requirements, functional + non-functional).**
- Infinite feed? (yes — paged) · Save for offline = full article body cached? · Cross-device sync of saves & read state? (yes) · Freshness SLA for the feed? · Auth/multi-device? · What shows when offline / when sync fails?
- NFRs: works fully offline for saved content; saves feel instant (<100 ms perceived); eventual consistency across devices; respect battery/Doze.

**2. API (data contract).**
- `GET /feed?cursor={c}&limit=20 → { items:[Article], nextCursor }` — **cursor/keyset** paging, not offset.
- `Article { id, title, summary, bodyUrl|body, updatedAt, … }`.
- `POST /saves { articleId, clientId(UUID), savedAt }` and `DELETE /saves/{articleId}` — **idempotency key** (`clientId`) so retries don't double-save.
- `GET /saves?since={cursor} → { changes, nextCursor }` — **delta sync** of saves + read state.

**3. Data (source of truth = local DB).**
- Room: `ArticleEntity`, `SaveEntity { articleId, status: PENDING|SYNCED|FAILED, readState }`, `RemoteKeys` for paging cursors.
- The **UI only reads Room** (via `Flow`); the network **writes into Room**. Saved article bodies are persisted so offline reading works.

**4. Arch (layers + UDF).**
- UI (Compose + MVI, `FeedUiState`/`ReaderUiState`) ← `StateFlow` ← ViewModel ← UseCases ← Repository ← Room (truth) + Retrofit/Ktor.
- Feed paging via **Paging 3 + `RemoteMediator`** (network → Room; UI pages from Room).
- Images via **Coil** (downsample, memory+disk cache).
- Background sync via **WorkManager** (constraints, backoff) draining a **save outbox**.

**5. Scale / sync / conflicts / edges.**
- **Optimistic save:** insert `SaveEntity(status = PENDING)` immediately → UI flips instantly; outbox + WorkManager push to server with backoff; server **dedupes on `clientId`**; mark `SYNCED`/`FAILED`.
- **Conflict policy (state it):** read/save state is largely additive; for genuine conflicts use **last-write-wins by `updatedAt`** or **server-authoritative**; name the trade-off (LWW can lose an edit).
- **Delta sync** on reconnect (`since` cursor), not full refresh.
- **Cursor paging** avoids offset duplicate/skip bugs on inserts.
- **Offline behavior:** saved articles fully readable; feed serves cached pages; show stale-while-revalidate; clear empty/error/offline states.
- **Platform constraints:** Doze/background limits → WorkManager with network constraint; cap outbox (backpressure); avoid loading full-res images.
- **What you'd measure:** sync success rate, frame time (Macrobenchmark/JankStats), cache hit rate, cold start, % saved-article opens served offline.

### Scoring guide (20 points)

| Dimension | Pts | What full marks looks like |
|---|---|---|
| **Requirement clarification** | 4 | Clarifies before designing; states functional **and** non-functional reqs (offline duration, freshness, instant-save target, failure behavior). |
| **Data modeling & source of truth** | 4 | Local DB is the single source of truth; network writes into it; UI reads only the DB; persists saved bodies for offline. |
| **Sync, conflicts & idempotency** | 4 | Optimistic update with persisted status; **idempotency key**; **delta sync**; a **named conflict-resolution policy** with its trade-off. |
| **Mobile-platform awareness** | 4 | Cursor (not offset) paging + Paging 3/`RemoteMediator`; Coil/memory; **WorkManager + Doze** for background sync; backpressure. |
| **Trade-off articulation & communication** | 4 | Surfaces trade-offs **unprompted**, defends choices, draws the layers, knows **what to measure**, handles "what about offline/retry/conflict?" without hand-waving. |

**Part C pass guidance:** 16/20 is a confident senior pass. **Below 10** typically means the candidate jumped to a solution without clarifying, let the UI read the network directly, or hand-waved sync ("it'll just sync") with no idempotency or conflict policy — the disqualifying patterns called out in Module 20.

---

# Answer key — Part A

> One-line rationale each. Letters only in the quick grid first, full rationale below.

**Quick grid**

| Q | Ans | Q | Ans | Q | Ans | Q | Ans | Q | Ans |
|---|---|---|---|---|---|---|---|---|---|
| 1 | B | 11 | B | 21 | B | 31 | B | 41 | B |
| 2 | B | 12 | B | 22 | B | 32 | B | 42 | B |
| 3 | B | 13 | A | 23 | B | 33 | B | 43 | B |
| 4 | B | 14 | A | 24 | B | 34 | B | 44 | B |
| 5 | B | 15 | B | 25 | B | 35 | B | 45 | B |
| 6 | B | 16 | B | 26 | B | 36 | B | 46 | B |
| 7 | B | 17 | B | 27 | B | 37 | B | 47 | B |
| 8 | B | 18 | B | 28 | B | 38 | B | 48 | B |
| 9 | B | 19 | B | 29 | B | 39 | B | 49 | B |
| 10 | B | 20 | B | 30 | B | 40 | B | 50 | B |

**Rationales**

1. **B** — `UI = f(state)`; UI is re-derived from state, never mutated imperatively. (M01)
2. **B** — Recomposition re-runs composables that read changed state; it is **not** a process/Activity restart. (M01)
3. **B** — Declarative = describe UI for a state; don't `findViewById`/mutate. (M01)
4. **B** — Composables return `Unit`, are PascalCase, side-effect-free in composition. (Authoring baseline / M01)
5. **B** — Composition → Layout (measure + place) → Drawing. (M01/M11)
6. **B** — Lazy lists only compose/lay out visible items + buffer. (M02)
7. **B** — Keys preserve item identity/state and correct animations on change. (M02)
8. **B** — `contentType` enables composition reuse across same-type items. (M02/M11)
9. **B** — Window Size Classes give coarse adaptive breakpoints. (M02/M15)
10. **B** — `Scaffold` provides standard structure slots + insets. (M02)
11. **B** — `remember` caches across recompositions; it does **not** survive process death. (M03)
12. **B** — Without `remember`, the state is re-created each recomposition → resets. (M03)
13. **A** — `rememberSaveable` additionally survives config change/process death via `Bundle`/`Saver`. (M03)
14. **A** — Hoisting moves state up; the composable becomes stateless (`value` down, events up). (M03)
15. **B** — Stateless = reusable, previewable, testable. (M03)
16. **B** — Hoist to the lowest common ancestor that reads/writes it. (M03)
17. **B** — Half-hoisting keeps an internal copy of `value` → two sources of truth. (M03)
18. **B** — Derive totals so they can't drift; never store derived data separately. (M03)
19. **B** — Expose a read-only `StateFlow`/`State`; mutate internally. (M03/M13)
20. **B** — `collectAsStateWithLifecycle()` stops collection below `STARTED`. (M03/M13)
21. **B** — Modifiers wrap; order changes where padding/background apply. (M04)
22. **B** — `size` is a preferred size (overridable); `requiredSize` forces it. (M04)
23. **B** — Pass a `MutableInteractionSource`; collect pressed/hovered. (M04)
24. **B** — Not consuming lets ancestors (e.g. parent scroll) also handle the gesture. (M04)
25. **B** — Single-measure keeps layout linear-time, avoiding exponential multi-pass cost. (M05)
26. **B** — Intrinsics add an extra measurement pass → cost. (M05)
27. **B** — `SubcomposeLayout` when some children's composition depends on others' measured size. (M05)
28. **B** — Reading in the draw lambda defers the read → only redraw, skipping recomposition/layout. (M08/M11)
29. **B** — Composition is frequent, order-free, skippable/cancellable, possibly parallel → effects must be quarantined. (M06)
30. **B** — Changing a `LaunchedEffect` key cancels and relaunches it. (M06)
31. **B** — `rememberCoroutineScope()` launches from callbacks/events. (M06)
32. **B** — `DisposableEffect` registers + cleans up on leave/key change. (M06)
33. **B** — `rememberUpdatedState` captures the latest value without restarting a long-lived effect. (M06)
34. **B** — `derivedStateOf` avoids recomposing on every input when the derived result rarely changes. (M06)
35. **B** — `staticCompositionLocalOf` recomposes the whole subtree on change (no read tracking). (M07)
36. **B** — CompositionLocal hides coupling and hurts testability; DI is explicit. (M07)
37. **B** — Color roles adapt to light/dark/dynamic color and keep contrast. (M09)
38. **B** — `animate*AsState` is fire-and-forget; `Animatable` is precise/interruptible. (M10)
39. **B** — Unstable = may change without notice (`List`, `var`, non-Compose-module type). (M11/M12)
40. **B** — `@Immutable` = never changes; `@Stable` = changes only via `State`. (M12)
41. **B** — A false `@Immutable` causes under-recomposition (silent stale UI). (M12)
42. **B** — Strong Skipping makes unstable-param composables skippable by referential equality. (M11/M12)
43. **B** — The slot table is the runtime's positional memory of the composition. (M12)
44. **B** — Snapshots give MVCC-style isolation: tracked reads, atomic apply. (M12)
45. **B** — Use lambda modifiers (`offset { }`, `graphicsLayer { }`) to defer reads to layout/draw. (M11)
46. **B** — Dependencies point inward toward the domain. (M13)
47. **B** — Offline-first: local DB is the source of truth; network syncs into it; UI reads the DB. (M13)
48. **B** — Compose UI tests assert against the semantics tree. (M14)
49. **B** — Store tokens in Keystore-backed encrypted storage; never plaintext/hardcoded. (M18)
50. **B** — K2/Kotlin 2.x ships the Compose compiler as a Kotlin plugin versioned with Kotlin. (M15)

---

## Result & certification

- **Part A:** ___ / 50
- **Part B:** ___ / 30
- **Part C:** ___ / 20
- **Total:** ___ / 100 — **Pass ≥ 80.**

A pass certifies you can reason about Compose at a professional level across the whole course. If you score **70–79**, you're close — review the areas where you lost MCQ points and re-attempt the practical tasks; the bugs in Part B are the ones that matter most on real teams.

> **Pair this with the [Final Assessment](final-assessment.md)** — the project-based capstone evaluation. The exam proves you can *reason*; the final assessment proves you can *build*. Full certification requires both.

➡️ Related: [Interview prep](interview-prep/) · [Capstone project](capstone-project/) · [Module 20 — Career & Interview Prep](../modules/module-20-career-interview/README.md)
