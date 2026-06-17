# Testing — Cheat Sheet

> One-page revision for **[Module 14 — Testing Jetpack Compose](../../modules/module-14-testing/README.md)**. Test each layer with the right tool. Tests drive the **semantics tree** — the same tree screen readers use.

---

## The testing pyramid (what to test where)

```text
        ▲ confidence / cost
   E2E / Macrobenchmark   few — startup, frame timing, critical flows
   ───────────────────
   Integration (nav+VM+fakes)   some — screens wired together
   ───────────────────
   Compose UI (semantics)        more — a screen's behavior
   ───────────────────
   Unit (ViewModel/state)        many, fast — logic & state flows
        ▼ speed / volume
```
Map: **logic → unit · screen behavior → Compose UI · pixels → screenshot · speed → Macrobenchmark.**

---

## Unit testing state (ViewModel / Flow)

```kotlin
@Test fun `adds item updates total`() = runTest {           // kotlinx-coroutines-test
    val repo = mockk<CartRepo>(relaxed = true)              // MockK
    val vm = CartViewModel(repo)
    vm.state.test {                                          // Turbine
        assertEquals(0L, awaitItem().total)
        vm.add(item)
        assertEquals(item.price, awaitItem().total)
        cancelAndConsumeRemainingEvents()
    }
}
```
| Tool | Role |
|---|---|
| **Turbine** | assert `Flow`/`StateFlow` emissions in order (`test { awaitItem() }`) |
| **MockK** | mock/stub collaborators (`coEvery`, `relaxed = true`) |
| **`runTest` + `StandardTestDispatcher`** | virtual-time coroutines; inject the dispatcher |
| **`MainDispatcherRule`** | swap `Dispatchers.Main` for a test dispatcher |

Inject dispatchers (don't hardcode `Dispatchers.IO`) so tests control time.

---

## Compose UI testing — find → act → assert

```kotlin
@get:Rule val rule = createComposeRule()                    // no Activity
// createAndroidComposeRule<MyActivity>()                   // when you need Activity/resources/nav

@Test fun `submit gated on valid email`() {
    rule.setContent { LoginScreen() }
    rule.onNodeWithText("Sign in").assertIsNotEnabled()
    rule.onNodeWithTag("emailField").performTextInput("a@b.com")
    rule.onNodeWithText("Sign in").assertIsEnabled().performClick()
}
```

**Finders** (by semantics):
`onNodeWithText` · `onNodeWithContentDescription` · `onNodeWithTag` · `onAllNodesWith…[i]` · `onNode(hasText(…) and hasClickAction())`

**Actions:**
`performClick` · `performTextInput` / `performTextClearance` · `performScrollTo` / `performScrollToIndex` · `performTouchInput { swipeUp() }`

**Assertions:**
`assertIsDisplayed` · `assertExists` / `assertDoesNotExist` · `assertIsEnabled` / `assertIsNotEnabled` · `assertTextEquals` · `assertIsOn`/`assertIsOff` · `assertCountEquals(n)` · `assertHasClickAction`

> `assertExists` = node in the tree (may be off-screen). `assertIsDisplayed` = actually visible.

---

## Semantics: merged vs unmerged & tags

- Default tree is **merged**: a `Button` merges its `Text`/`Icon` into one node (so `onNodeWithText("Save")` finds the button).
- Reach a child (badge inside a button) with `useUnmergedTree = true`.
- **Prefer real semantics** (text, `contentDescription`) over `testTag` — they double as accessibility. Use `testTag("…")` only when no natural semantic fits (e.g. scoping a decorative container). Tag-only = testable but **inaccessible** (a smell).
- Add custom semantics for testability *and* a11y: `Modifier.semantics { contentDescription = "…"; stateDescription = "…" }`.

---

## Synchronization — the idle contract

- The framework **auto-waits for idle** between steps (recomposition, animations, `withFrameNanos`). **Never `Thread.sleep`.**
- **Infinite/indeterminate animations never idle → the test hangs to timeout.** Fix:
  ```kotlin
  rule.mainClock.autoAdvance = false
  rule.setContent { LoadingThenContent() }
  rule.mainClock.advanceTimeBy(2_000)            // you drive frames
  rule.waitUntil(1_000) { rule.onAllNodesWithText("Loaded").fetchSemanticsNodes().isNotEmpty() }
  ```
- `waitForIdle()` waits for Compose's own work; `waitUntil { condition }` polls for state **outside** Compose's idle tracking. Prefer condition waits over fixed sleeps.

---

## Lazy lists & debugging

```kotlin
rule.onNodeWithText("Post #80").performScrollTo().performClick()   // scroll off-screen item into view first
rule.onRoot().printToLog("TREE")                                  // dump the semantics tree to debug "no node matched"
```
LazyColumn only composes visible items — assert/act on off-screen items only **after** scrolling to them.

---

## Integration testing

`createAndroidComposeRule<MyActivity>()` + a **test `NavHost`** + **fakes** (fake repo/use-cases). Drive a real flow: tap → navigate → assert the next screen's semantics. Use fakes over mocks for state-bearing collaborators.

---

## Screenshot testing (pixels)

| Tool | Runs on |
|---|---|
| **Paparazzi** | JVM (no device) — fast, render-only |
| **Roborazzi** | Robolectric JVM — works with Compose test APIs |

- Make rendering **deterministic**: fixed seeds, disabled animations, fixed clock, fixed locale/density, test fonts.
- Screenshot tests cover **pixel** correctness; semantics tests cover **behavioral** correctness — don't conflate.

---

## Macrobenchmark testing (performance as a test)

```kotlin
@get:Rule val rule = MacrobenchmarkRule()
@Test fun scroll() = rule.measureRepeated(
    packageName = "…", metrics = listOf(FrameTimingMetric()),
    iterations = 10, startupMode = StartupMode.COLD,
) { startActivityAndWait(); /* scroll */ }
```
Measure `StartupTimingMetric` / `FrameTimingMetric` on a **release-like** build; compare before/after. Also where you generate **baseline profiles**.

---

## Top gotchas

| Symptom | Cause | Fix |
|---|---|---|
| Flaky / slow test | `Thread.sleep` | trust auto-sync; `waitUntil { }` |
| Test hangs to timeout | infinite animation never idles | `mainClock.autoAdvance = false` + advance |
| "No node matched" | merged tree / wrong matcher / split text | `printToLog`, `useUnmergedTree`, fix matcher |
| Passes for hidden node | `assertExists` instead of `assertIsDisplayed` | use the right assertion |
| Lazy item not found | never scrolled into view | `performScrollTo` / `performScrollToIndex` first |
| Brittle on refactor | asserted tree shape / coordinates | assert **behavior** (text/enabled/state) |
| Testable but inaccessible | `testTag` instead of semantics | real `contentDescription`/text |
| Flaky ViewModel test | hardcoded dispatcher / real time | inject dispatcher; `runTest` + Turbine |

---

## What NOT to assert

- Exact pixel coordinates or tree structure (use screenshot tests for pixels).
- Implementation details that survive no refactor.
- Recomposition counts in a behavioral test (that's profiling — see [Performance](performance.md)).

---

## Golden rules

1. **Right layer, right tool**: unit (logic) → UI semantics (behavior) → screenshot (pixels) → Macrobenchmark (speed).
2. **Semantics-first** selectors; `testTag` only as a scoped escape hatch — testable UI *is* accessible UI.
3. **No `Thread.sleep`** — trust idle sync; control the clock for animations.
4. **Inject dispatchers**; `runTest` + Turbine + MockK for state.
5. Make screenshots **deterministic**; benchmark on **release** builds.
6. Assert **behavior**, not structure or pixels.

➡️ Related: [State](state.md) · [Performance](performance.md) · [Side Effects](side-effects.md)
