# Side Effects — Cheat Sheet

> One-page revision for **[Module 06 — Side Effects](../../modules/module-06-side-effects/README.md)**. Composition runs **often & order-free**; quarantine all I/O, subscriptions, and mutation of the outside world into effect APIs.

---

## Which effect API? (decision tree)

```text
Run SUSPEND work tied to the screen (start on enter, cancel on leave)?
 └─ LaunchedEffect(key)            key = "the reason to start over"

Launch a coroutine from a CALLBACK / user event (onClick)?
 └─ rememberCoroutineScope()       scope.launch { … } in the handler

Need register + CLEANUP on leave (listeners, callbacks, resources)?
 └─ DisposableEffect(key) { onDispose { unregister() } }

Publish a value to NON-Compose code on every successful composition?
 └─ SideEffect { analytics.setUser(user) }

Need the LATEST value of a changing lambda WITHOUT restarting an effect?
 └─ rememberUpdatedState(value)

Turn an ASYNC source (Flow/callback) into State<T>?
 └─ produceState(initial, key) { value = … ; awaitDispose { … } }

Compute State FROM State, notify only when result changes?
 └─ remember { derivedStateOf { … } }

Observe Compose State AS a Flow (debounce, distinctUntilChanged)?
 └─ snapshotFlow { state }
```

---

## `LaunchedEffect` — keys are everything

```kotlin
LaunchedEffect(userId) {                 // restart only when userId changes (by equals)
    ui = repo.load(userId)
}
```
| Key | Behavior |
|---|---|
| `Unit` / `true` | run **once** on enter; never restart (until leave + re-enter) |
| `id` / param | restart when that value changes |
| `(a, b)` | restart if **any** key changes |
| **lambda / fresh list** | ❌ restarts **every recomposition** — the #1 bug |

Lifecycle: **enter → launch · key change → cancel + relaunch · leave → cancel**. Runs on `Main` by default; `withContext(Dispatchers.Default/IO)` for CPU/blocking work.

---

## `rememberCoroutineScope` — event-driven

```kotlin
val scope = rememberCoroutineScope()
Button(onClick = { scope.launch { snackbar.showSnackbar("Saved") } }) { Text("Save") }
```
Use for work driven by **events** (taps), not by composition/state. Using `LaunchedEffect` for a button press is wrong (you'd flip a flag — awkward, re-entrant).

---

## `DisposableEffect` — register / unregister

```kotlin
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, e -> … }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }   // ❗ mandatory cleanup
}
```
Re-runs `onDispose` + re-registers when the key changes. **The home for cleanup**, not `LaunchedEffect`'s `finally`.

---

## `SideEffect` & `rememberUpdatedState`

```kotlin
SideEffect { analytics.setCurrentScreen(screenName) }   // every successful (re)composition, no coroutine
```
```kotlin
// Run once, but always call the LATEST callback:
val latestOnTimeout by rememberUpdatedState(onTimeout)
LaunchedEffect(Unit) { delay(3000); latestOnTimeout() }  // key stays stable; value stays fresh
```

---

## `produceState` & `snapshotFlow`

```kotlin
val user: State<UserUi> = produceState(UserUi.Loading, id) {
    value = runCatching { repo.load(id) }.fold({ UserUi.Ready(it) }, { UserUi.Error })
    awaitDispose { /* cancel subscriptions */ }
}
```
```kotlin
LaunchedEffect(Unit) {
    snapshotFlow { query }.debounce(300).distinctUntilChanged().collectLatest(::search)
}
```

---

## `derivedStateOf` vs `remember(key)`

| Use | When |
|---|---|
| `derivedStateOf` | **noisy input → quiet output** (scroll px → boolean); throttles *notifications* |
| `remember(key)` | recompute/cache a value when a specific key changes |
| inline | cheap value that changes together with its inputs |

`derivedStateOf` has overhead — wrapping a cheap, co-varying value is **worse** than inline. Always inside `remember`.

---

## Cancellation rules (LaunchedEffect / coroutines)

```kotlin
try {
    val r = withContext(Dispatchers.Default) { ensureActive(); heavyMap() }  // cooperate
} catch (e: CancellationException) {
    throw e                              // ❗ NEVER swallow cancellation
} catch (e: Exception) {
    ui = Error(e.message)
}
```
- Re-throw `CancellationException` (or branch it out of a generic `catch`) — swallowing turns a normal restart into a fake error.
- Long CPU loops need `ensureActive()` / `yield()` to notice cancellation.
- `LaunchedEffect` is **screen-scoped** — does NOT survive config change/process death. Long uploads → `viewModelScope` / WorkManager.

---

## Top gotchas

| Symptom | Cause | Fix |
|---|---|---|
| Network call fires in a loop | unstable key (lambda/fresh list) | key on stable ids only |
| Data never reloads on param change | `LaunchedEffect(Unit)` when a param matters | key on the param |
| Stale value inside a once-only effect | closure captured value at launch | `rememberUpdatedState` |
| Listener leak | no `onDispose` / used `LaunchedEffect` | `DisposableEffect { onDispose { … } }` |
| Spurious "error" on every navigation | caught `CancellationException` | re-throw it |
| UI freezes / ANR | blocking work in composition | suspend in `LaunchedEffect`, `withContext(IO)` |
| Work survives screen but shouldn't (or vice-versa) | wrong scope | screen → `LaunchedEffect`; outlives screen → `viewModelScope`/WorkManager |
| `derivedStateOf` adds cost, no benefit | wrapped a cheap co-varying value | compute inline |

---

## Golden rules

1. **No I/O or external mutation in the composition path** — use an effect.
2. The **key is the reason to restart** — exactly that, nothing more, nothing less.
3. **Event-driven** → `rememberCoroutineScope`; **state/composition-driven** → `LaunchedEffect`.
4. **Cleanup** → `DisposableEffect.onDispose`.
5. **Re-throw `CancellationException`**; stay main-safe & cancellation-cooperative.
6. Latest-without-restart → `rememberUpdatedState`.

➡️ Related: [State](state.md) · [Performance](performance.md) · [Animations](animations.md)
