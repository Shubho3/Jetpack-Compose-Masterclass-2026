# Lesson 03 — Compose UI Testing

> After this lesson you can write Compose UI tests that render a real composable, find nodes through the **semantics tree** with finders, assert on them, and perform actions (click, type, scroll) — while understanding the **idle/synchronization** contract that keeps them stable.

**Module:** 14 · **Lesson:** 03 · **Level:** 🟢🟡🔴 · **Est. time:** 90–110 min

---

## 1. Concept

### 🟢 For beginners — *what is it and why do I care?*

A **Compose UI test** renders one of your `@Composable` functions and then *pokes at it like a user* — "find the button that says Submit, click it, now check the screen shows Saved." It's how you prove the UI actually shows the right things and reacts correctly, without you tapping through the app by hand.

But Compose has no XML and no view IDs to grab. So how does a test "find the button"? Through the **semantics tree**: a parallel description of the UI built for *accessibility*. Every meaningful element publishes semantics — its text, its role (button, checkbox), whether it's enabled, its state. Screen readers like TalkBack use this tree; **your tests use the exact same tree.** This is the big idea: *if a test can find it, a blind user can too.* Writing testable UI and writing accessible UI are the same skill.

A test reads like a sentence:
```kotlin
composeTestRule.onNodeWithText("Submit").performClick()
composeTestRule.onNodeWithText("Saved").assertIsDisplayed()
```
Three verbs repeat everywhere: **find** a node (`onNodeWith...`), **act** on it (`perform...`), **assert** something (`assert...`).

### 🟡 For intermediate devs — *the mechanism*

The entry point is a **test rule**:
- `createComposeRule()` — hosts your composable with no Activity. Use it for component/screen tests that don't need real Android resources or navigation.
- `createAndroidComposeRule<MyActivity>()` — runs inside a real Activity (for `activity`, resources, navigation — Lesson 04).

You call `rule.setContent { ... }` to render, then chain **finder → assertion/action**:

```kotlin
@get:Rule val rule = createComposeRule()

@Test fun submitEnablesAfterInput() {
    rule.setContent { LoginScreen() }
    rule.onNodeWithText("Email").performTextInput("a@b.com")
    rule.onNodeWithText("Submit").assertIsEnabled().performClick()
}
```

**Finders** select nodes by semantics:
- `onNodeWithText("…")`, `onNodeWithContentDescription("…")`, `onNodeWithTag("…")` for a single node.
- `onAllNodesWith…` for collections; index with `[0]`.
- `onNode(matcher)` with composable matchers: `hasText(...) and hasClickAction()`.

**Test tags** are an escape hatch: `Modifier.testTag("submit")` adds a *test-only* identifier you find with `onNodeWithTag("submit")`. Use tags when there's no natural semantic to match (e.g. a decorative container you need to scope to), *not* as a substitute for real semantics.

**Actions** simulate the user: `performClick()`, `performTextInput("…")`, `performScrollTo()`, `performTouchInput { swipeUp() }`.

**Assertions** check state: `assertIsDisplayed()`, `assertIsEnabled()/assertIsNotEnabled()`, `assertTextEquals("…")`, `assertIsOn()` (toggles), `assertCountEquals(n)` on collections.

**Synchronization is automatic.** Between actions, the test **waits for Compose to be idle** — recompositions settle, animations finish, `withFrameNanos` work drains — before the next assertion runs. You don't sleep; the framework does the waiting for you. (Except when it can't — see 🔴.)

### 🔴 For senior devs — *trade-offs, edges, internals*

The depth that prevents flaky, brittle UI suites:

- **The idling contract is the whole ballgame — and infinite animations break it.** Compose tests block until the `ComposeIdlingResource` reports idle. An **infinitely animating** composable (`rememberInfiniteTransition`, an indeterminate progress spinner, a looping Lottie) *never* idles, so the test **hangs until timeout**. The fix: disable the offending animation under test, or use `rule.mainClock.autoAdvance = false` and advance the clock manually (`mainClock.advanceTimeBy(ms)`) so you control frames. Knowing *which* construct never idles is senior knowledge.
- **Manual clock control unlocks animation and timing tests.** Set `mainClock.autoAdvance = false`, perform the action, then `advanceTimeBy(...)` and assert intermediate frames — e.g. "the FAB is half-faded at 150 ms." With auto-advance on, you can only see start and end states.
- **`waitForIdle()` vs `waitUntil { }`.** `waitForIdle()` waits for Compose's own work. But if your screen depends on something *outside* Compose's idle tracking — a `StateFlow` fed by a background coroutine the test doesn't drive, an `IdlingResource` you registered — use `rule.waitUntil(timeoutMillis) { rule.onAllNodesWithText("Done").fetchSemanticsNodes().isNotEmpty() }` to poll a condition. Prefer condition-based waits over fixed sleeps, always.
- **`useUnmergedTree`.** By default the semantics tree is *merged*: a `Button` merges its child `Text`/`Icon` into one node, so `onNodeWithText("Save")` finds the button. Sometimes you must inspect a child individually (assert an icon inside a merged button) — pass `useUnmergedTree = true` to finders. Understanding merge boundaries (set by `Modifier.semantics(mergeDescendants = true)` and components like `Button`) explains many "node not found" surprises.
- **Custom semantics for testability *is* a11y investment.** When a component lacks a natural label (an icon-only button, a custom slider), add `Modifier.semantics { contentDescription = "…"; stateDescription = "…" }` or `SemanticsProperties`. That single change makes the component testable *and* screen-reader-usable. Reaching for `testTag` instead is a smell — you've made it testable but still inaccessible.
- **Test behavior, not pixels or structure.** Asserting "a node with text X is displayed and enabled" survives a refactor from `Row` to `Box`. Asserting on tree *shape* or exact coordinates is brittle. Screenshot tests (Lesson 05) cover *pixel* correctness; semantics tests cover *behavioral* correctness — don't conflate them.
- **`printToLog` is your debugger.** `rule.onRoot().printToLog("TREE")` dumps the semantics tree so you can see exactly what's matchable. Most "no node matched" failures are solved by reading that dump — the text may be split, merged, or have a different content description than you assumed.
- **Robolectric makes these JVM-runnable.** With the right setup, `createComposeRule` tests can run under Robolectric on the JVM (no emulator), moving this layer's cost down — relevant to the pyramid shape from Lesson 01.

### Analogy

The semantics tree is the **stage-manager's cue sheet**, not the set itself. The audience (a sighted user) sees the painted scenery (pixels). The stage manager — and the *understudy who can't see the stage* (a screen reader) — works from the cue sheet: "Stage left, the SUBMIT button (enabled); center, the heading 'Welcome'." Your test is that stage manager: it never looks at the paint, it reads the cue sheet, finds "SUBMIT," and triggers it. If the cue sheet is missing an entry (no semantics), both the stage manager *and* the understudy are lost — which is why writing for the test writes for accessibility.

### Mental model

> **Tests drive the semantics tree, the same tree screen readers use. Find a node by its meaning, act on it, assert its state — and let the idle contract do the waiting (unless something never idles, then control the clock).**

### Real-world example

A sign-up form. A UI test renders `SignUpScreen`, types an invalid email, asserts the **Sign up** button `isNotEnabled` and an error node "Enter a valid email" `isDisplayed`; then types a valid email and asserts the button `isEnabled`. The same test would catch a regression where someone removes the disabled-while-invalid guard — a behavior the unit layer can't see (it has no button) and the E2E layer is too slow to check per-keystroke. And because every assertion goes through semantics, passing this test means TalkBack users get a labeled, state-announced form for free.

---

## 2. Visual Learning

**ASCII — find → act → assert over the semantics tree:**
```text
   @Composable UI            Semantics tree (what tests + TalkBack see)
   ┌───────────────┐         ┌───────────────────────────────────────┐
   │  [ Welcome ]  │  ─────▶  │ Node(text="Welcome", role=Heading)    │
   │  email: [___] │         │ Node(role=TextField, label="email")   │
   │  ( Sign up )  │         │ Node(role=Button,text="Sign up",       │
   └───────────────┘         │      enabled=false)                   │
                             └───────────────────────────────────────┘
   test:  onNodeWithText("Sign up")   →  find
          .assertIsNotEnabled()       →  assert
          performTextInput(...)       →  act  →  (Compose goes idle) → re-read tree
```

**Mermaid — the find/act/assert loop with synchronization:**
```mermaid
graph TD
    A[rule.setContent { Screen() }] --> B[Finder: onNodeWith...]
    B --> C{Node found in<br/>semantics tree?}
    C -->|no| E[printToLog to inspect tree<br/>add semantics / fix matcher]
    C -->|yes| D[Action: performClick / performTextInput]
    D --> S[[Framework waits for Compose IDLE<br/>recomposition + animations settle]]
    S --> F[Assertion: assertIsDisplayed / assertIsEnabled]
    F --> G{More steps?}
    G -->|yes| B
    G -->|no| H[Test passes]
```

**Illustration prompt (paste into an image generator):**
```text
Illustration: split scene. LEFT half shows a colorful rendered phone screen with a heading,
a text field, and a "Sign up" button (greyed out). RIGHT half shows the SAME screen as a
glowing wireframe "x-ray" labeled "SEMANTICS TREE" — each element is a labeled node card
(text="Sign up", role=Button, enabled=false). A robot hand labeled "TEST" and a separate
white cane icon labeled "SCREEN READER" both read from the RIGHT x-ray side, not the left pixels,
connected by light beams to the same nodes. Caption: "Tests and a11y share one tree."
Modern, vibrant, crisp labels, soft studio gradients.
```

---

## 3. Code

> Tests live in `src/androidTest/` (or run under Robolectric on the JVM). Dependency: `androidx.compose.ui:ui-test-junit4`; debug-only `ui-test-manifest` to host content.

### 🟢 Beginner — find, act, assert

```kotlin
class CounterScreenTest {
    @get:Rule val rule = createComposeRule()

    @Test fun `tapping increment shows one`() {
        rule.setContent { CounterScreen() }                  // render the real composable

        rule.onNodeWithText("Count: 0").assertIsDisplayed()  // initial state
        rule.onNodeWithText("Increment").performClick()      // act like a user
        rule.onNodeWithText("Count: 1").assertIsDisplayed()  // result after recomposition
    }
}
```

**Explanation.** `createComposeRule()` hosts the composable without an Activity. `setContent` renders it. We *find* by visible text, *act* with `performClick()`, and *assert* the new text is displayed. The test automatically waits for recomposition between the click and the assertion — no sleep.

**Common mistakes.**
```kotlin
// ❌ Sleeping to "wait for" the UI — flaky and slow.
rule.onNodeWithText("Increment").performClick()
Thread.sleep(500)                                   // unnecessary; Compose already syncs
rule.onNodeWithText("Count: 1").assertExists()
```
The framework already waits for idle between steps. `Thread.sleep` adds flakiness (too short) or slowness (too long) for nothing.

**Best practices.**
- Match on what the user sees (`onNodeWithText`) before reaching for tags.
- Trust automatic synchronization; never `Thread.sleep`.

---

### 🟡 Intermediate — input, enabled-state, and a test tag

```kotlin
@Composable
fun LoginScreen(onSubmit: (String) -> Unit = {}) {
    var email by rememberSaveable { mutableStateOf("") }
    val valid = email.contains("@")
    Column {
        OutlinedTextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier.testTag("emailField"),       // tag for the field container
        )
        if (email.isNotEmpty() && !valid) Text("Enter a valid email")
        Button(onClick = { onSubmit(email) }, enabled = valid) {
            Text("Sign in")
        }
    }
}
```

```kotlin
class LoginScreenTest {
    @get:Rule val rule = createComposeRule()

    @Test fun `submit is gated on a valid email`() {
        rule.setContent { LoginScreen() }

        // Button starts disabled, no error shown yet.
        rule.onNodeWithText("Sign in").assertIsNotEnabled()
        rule.onNodeWithText("Enter a valid email").assertDoesNotExist()

        // Invalid input → error appears, button stays disabled.
        rule.onNodeWithTag("emailField").performTextInput("nope")
        rule.onNodeWithText("Enter a valid email").assertIsDisplayed()
        rule.onNodeWithText("Sign in").assertIsNotEnabled()

        // Valid input → error gone, button enabled.
        rule.onNodeWithTag("emailField").performTextClearance()
        rule.onNodeWithTag("emailField").performTextInput("a@b.com")
        rule.onNodeWithText("Enter a valid email").assertDoesNotExist()
        rule.onNodeWithText("Sign in").assertIsEnabled()
    }
}
```

**Explanation.** This asserts *behavioral* state, not pixels: the button's `enabled` flag and the error text's existence as input changes. The text field is found via a `testTag` (its label "Email" is also matchable, but a tag scopes the field unambiguously). Each `performTextInput`/`performTextClearance` triggers recomposition; the framework syncs before the next assertion.

**Common mistakes.**
```kotlin
// ❌ assertExists() when you mean assertIsDisplayed().
rule.onNodeWithText("Sign in").assertExists()   // exists in tree even if scrolled off-screen
// ❌ Using a testTag where a real semantic exists, leaving the UI inaccessible.
IconButton(onClick = …, modifier = Modifier.testTag("fav")) { Icon(..., contentDescription = null) }
//                                                                              ^ no a11y label
```
`assertExists` passes for off-screen nodes; `assertIsDisplayed` checks visibility. And tagging an icon button while leaving `contentDescription = null` makes it testable-but-inaccessible — add the description and you get both.

**Best practices.**
- Use `assertIsDisplayed` for "the user can see it"; `assertExists`/`assertDoesNotExist` for presence in the tree.
- Prefer real semantics (label, content description) over tags; reach for `testTag` only when no natural semantic fits.
- Assert *enabled/state*, not layout coordinates.

---

### 🔴 Production — scrolling lists, unmerged tree, and taming an animation

```kotlin
class FeedScreenTest {
    @get:Rule val rule = createComposeRule()

    @Test fun `scroll to an item far down and open it`() {
        val items = List(100) { "Post #$it" }
        var opened: String? = null
        rule.setContent { FeedScreen(items = items, onOpen = { opened = it }) }

        // Scroll the lazy list to a node that isn't composed yet, then click it.
        rule.onNodeWithText("Post #80").performScrollTo().performClick()
        // (For LazyColumn, scroll by the list node:)
        // rule.onNode(hasScrollAction()).performScrollToIndex(80)

        assertEquals("Post #80", opened)
    }

    @Test fun `count badge inside a merged button is readable via unmerged tree`() {
        rule.setContent { CartButton(count = 3) }   // a Button merging an icon + a "3" badge

        // Merged tree: the Button is one node. Reach the child badge explicitly.
        rule.onNodeWithText("3", useUnmergedTree = true).assertIsDisplayed()
        rule.onNodeWithContentDescription("Cart").assertHasClickAction()
    }

    @Test fun `indeterminate spinner does not hang the test (manual clock)`() {
        rule.mainClock.autoAdvance = false          // we drive time; infinite anim won't block
        rule.setContent { LoadingThenContent() }    // shows an infinite spinner, then content

        rule.onNodeWithTag("spinner").assertIsDisplayed()
        rule.mainClock.advanceTimeBy(2_000)         // advance past the simulated load
        rule.waitUntil(timeoutMillis = 1_000) {
            rule.onAllNodesWithText("Loaded").fetchSemanticsNodes().isNotEmpty()
        }
        rule.onNodeWithText("Loaded").assertIsDisplayed()
    }
}
```

**Explanation.** Three production realities. **Scrolling:** `performScrollTo()` (or `performScrollToIndex` on the scrollable node) brings an off-screen lazy item into composition before acting — you can't click what isn't composed. **Unmerged tree:** a `Button` merges its children into one node, so to assert the inner "3" badge you pass `useUnmergedTree = true`. **Animation:** an indeterminate spinner never idles, so auto-advance would hang the test; we turn it off, advance the clock manually, and poll with `waitUntil` for a condition outside Compose's idle tracking.

**Common mistakes.**
```kotlin
// ❌ Asserting a lazy item that's never been scrolled into view.
rule.onNodeWithText("Post #80").assertIsDisplayed()  // not composed yet → no node → fails

// ❌ Letting an infinite animation run with autoAdvance = true.
rule.setContent { InfiniteSpinner() }
rule.onNodeWithText("Done").assertIsDisplayed()      // test hangs to timeout — never idles
```
LazyColumn only composes visible items, so off-screen nodes don't exist until scrolled to. And any infinitely-animating content blocks the idle resource forever unless you control the clock.

**Best practices.**
- For lazy lists, `performScrollTo`/`performScrollToIndex` before asserting/acting on off-screen items.
- Use `useUnmergedTree = true` to reach children of merged nodes (badges, icons inside buttons).
- For infinite/indeterminate animations, set `mainClock.autoAdvance = false` and advance manually; use `waitUntil { }` for non-Compose conditions.
- Debug "no node matched" with `rule.onRoot().printToLog("TREE")`.

---

## 4. Interview Questions

**🟢 Beginner**

1. *How does a Compose UI test find an element if there are no view IDs?*
   > Through the **semantics tree** — the accessibility description of the UI. Finders like `onNodeWithText`, `onNodeWithContentDescription`, and `onNodeWithTag` match nodes by their semantics, the same data screen readers use.
2. *What are the three kinds of operations in a Compose UI test?*
   > **Finders** (`onNodeWith…`) to select a node, **actions** (`performClick`, `performTextInput`) to interact, and **assertions** (`assertIsDisplayed`, `assertIsEnabled`) to verify state.

**🟡 Intermediate**

3. *When should you use `testTag` versus matching on text or content description?*
   > Prefer real semantics (text, content description) because they double as accessibility and test the user-visible meaning. Use `testTag` only when there's no natural semantic to match — e.g. scoping a decorative container — never as a shortcut that leaves the UI inaccessible.
4. *Difference between `assertExists()` and `assertIsDisplayed()`?*
   > `assertExists` checks the node is present in the semantics tree (could be scrolled off-screen). `assertIsDisplayed` additionally checks it's actually visible on screen. Use the latter for "the user can see it."

**🔴 Senior**

5. *Your Compose UI test hangs until timeout on a screen with a loading spinner. Why, and how do you fix it?*
   > Compose tests block until the app is **idle**, but an indeterminate/infinite animation never idles, so the test waits forever. Fix by disabling that animation under test, or set `rule.mainClock.autoAdvance = false` and advance time manually with `advanceTimeBy`, optionally polling with `waitUntil { }` for conditions outside Compose's idle tracking.
6. *What is the merged vs unmerged semantics tree, and when do you need `useUnmergedTree`?*
   > By default Compose merges a component's descendants into one node (a `Button` merges its `Text`/`Icon`) so finders match the whole control. To assert on an individual child — e.g. a count badge inside a merged button — pass `useUnmergedTree = true` so the child node is visible to the finder. Merge boundaries come from `Button` and `Modifier.semantics(mergeDescendants = true)`.

---

## 5. AI Assistant

**Prompt example (generating a UI test):**
```text
Write a Compose UI test (androidTest, createComposeRule) for this screen. Use semantics finders
(onNodeWithText / onNodeWithContentDescription), not testTags unless no semantic exists.
Assert: button is disabled with an invalid email and an error is shown; enabled with a valid one.
Drive input with performTextInput. Don't use Thread.sleep — rely on automatic synchronization.
Target Compose 2026, Kotlin 2.x.
[paste the @Composable]
```

**AI workflow.**
- ✅ Good for: scaffolding find/act/assert chains, enumerating state assertions (enabled/error/displayed), and suggesting which nodes to target.
- ⚠️ Watch: models often **sprinkle `testTag` everywhere** (instead of real semantics), add **`Thread.sleep`**, confuse `assertExists` with `assertIsDisplayed`, forget to **scroll lazy items into view**, and ignore that **infinite animations hang the test**.

**Review workflow — map to this lesson's *Common Mistakes*:**
- Does it match on real semantics where possible, with tags only as a last resort (and is the UI still accessible)?
- Any `Thread.sleep`? Replace with the built-in idle sync or `waitUntil { }`.
- Right assertion for the intent (`assertIsDisplayed` vs `assertExists`)?
- Are off-screen lazy items scrolled to before acting?
- Does any infinite animation need `autoAdvance = false`?

**Validation workflow — prove the test is real:**
1. Run it; if a finder fails, `rule.onRoot().printToLog("TREE")` and read what's actually matchable.
2. Break the production guard (e.g. always-enable the button); the test should fail — if not, it asserts nothing useful.
3. Turn on TalkBack on the same screen — if your finders rely on real semantics, the screen is also navigable. (Tags-only = a red flag for both.)
4. Re-run the test 30× to confirm it's stable (no hidden timing dependency).

> **AI drafts, you decide.** The model writes the chains; you enforce *semantics-first* selectors and the *no-sleep, control-the-clock* discipline it tends to ignore.

---

## Recap / Key takeaways

- Compose UI tests drive the **semantics tree** — the same tree screen readers use; testable UI *is* accessible UI.
- The loop is **find** (`onNodeWith…`) → **act** (`perform…`) → **assert** (`assert…`); the framework **waits for idle** between steps.
- Prefer **real semantics** (text, content description) over `testTag`; tags are a scoped escape hatch, not a substitute for accessibility.
- **Infinite/indeterminate animations never idle** and hang tests — set `mainClock.autoAdvance = false` and advance manually; use `waitUntil { }` for non-Compose conditions.
- **Scroll lazy items** into view before acting; use `useUnmergedTree = true` to reach children of merged nodes; `printToLog` to debug.

➡️ Next: **[Lesson 04 — Integration testing](04-integration-testing.md)** — wiring navigation, a real `ViewModel`, and fakes together with `createAndroidComposeRule`.
