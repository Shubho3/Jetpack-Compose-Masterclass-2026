# State — Cheat Sheet

> One-page revision for **[Module 03 — State Management](../../modules/module-03-state-management/README.md)**. `UI = f(state)`. Make state **correct, minimal, owned in one place**.

---

## The one loop

```text
state ──read──▶ Composable f(state) ──emits──▶ UI
  ▲                                              │
  └────────── event (user/system) ◀──────────────┘
                  updates state
```
A **read is a subscription**: reading a `State` inside composition subscribes that scope to recompose when it changes.

---

## Where should this state live? (decision tree)

```text
Is it UI-only & ephemeral? (expanded, scroll pos, text-in-progress)
 ├─ yes, fine to lose on rotation ........ remember { mutableStateOf(...) }
 └─ yes, must survive rotation/proc-death  rememberSaveable { mutableStateOf(...) }
Is it business/screen state? ............. ViewModel + StateFlow<UiState>
Is it app-wide / persisted? .............. Repository → DataStore / Room (SSOT)
Needs a parent or sibling to see it? ..... HOIST it up to the lowest common owner
```

---

## `remember` family — what each forgets

| API | Survives recomposition | Survives config change / process death | Use for |
|---|:--:|:--:|---|
| `mutableStateOf(x)` *(no remember)* | ❌ resets every recompose | ❌ | **never alone** — the #1 beginner bug |
| `remember { mutableStateOf(x) }` | ✅ | ❌ | ephemeral UI state |
| `rememberSaveable { mutableStateOf(x) }` | ✅ | ✅ (Bundle/Saver) | form fields, selected tab |
| `remember(key) { … }` | ✅ until `key` changes | ❌ | recompute cached value when an input changes |
| ViewModel `StateFlow` | ✅ | ✅ config change (not process death w/o SavedStateHandle) | screen/business state |

`rememberSaveable` needs a **`Saver`** for non-`Parcelable`/non-primitive types:
```kotlin
val state = rememberSaveable(stateSaver = MyType.Saver) { mutableStateOf(MyType()) }
// or: rememberSaveable(saver = listSaver(save = {…}, restore = {…})) { … }
```

---

## State hoisting pattern

```kotlin
// Stateless: value down, events up → reusable, testable, single source of truth.
@Composable fun NameField(value: String, onValueChange: (String) -> Unit) =
    OutlinedTextField(value, onValueChange, label = { Text("Name") })
```
**Hoist to the lowest common ancestor** that needs the state. Stateless composables take `value` + `onValueChange`.

---

## UDF / MVI / MVVM at a glance

| | What | Compose shape |
|---|---|---|
| **UDF** | state flows down, events flow up | `state: UiState`, `onEvent: (Event) -> Unit` |
| **MVVM** | ViewModel exposes observable state | `val state: StateFlow<UiState>` |
| **MVI** | single immutable state + explicit intents | one `UiState`, `sealed interface Event`, reducer |

```kotlin
@Immutable
data class CartUiState(val items: ImmutableList<CartItem> = persistentListOf()) {
    val total: Long get() = items.sumOf { it.unitPrice * it.qty }   // ✅ DERIVED, can't drift
}
class CartViewModel : ViewModel() {
    private val _state = MutableStateFlow(CartUiState())
    val state: StateFlow<CartUiState> = _state.asStateFlow()        // expose read-only
    fun add(i: CartItem) = _state.update { it.copy(items = (it.items + i).toImmutableList()) }
}
```
Collect with lifecycle: `val ui by viewModel.state.collectAsStateWithLifecycle()`.

---

## `derivedStateOf` vs `remember(key)` vs inline

```text
Does INPUT change MORE OFTEN than OUTPUT?  (scroll px → boolean)
 ├─ yes ............. derivedStateOf { … }   (always wrapped in remember!)
Recompute when a specific KEY changes?
 ├─ yes ............. remember(key) { … }
Cheap & changes together with inputs?
 └─ yes ............. just compute inline (no wrapper)
```
```kotlin
val showFab by remember { derivedStateOf { listState.firstVisibleItemIndex > 5 } }
```
`derivedStateOf` notifies readers **only when the result changes** — not on every input change.

---

## Stability & immutable collections (keeps skipping alive)

- `List<T>` / `Map` / `Set` params are **unstable** (interfaces; could be mutable) → can defeat skipping in hot `LazyColumn`s.
- Fix at the source: `kotlinx.collections.immutable` → `ImmutableList` / `persistentListOf()`, and `@Immutable` / `@Stable` on UI state.
- Strong Skipping (2026) compares unstable params by **instance** — but a fresh `List` each emission is a new instance → recomposes every row. Immutable types fix it.

---

## `snapshotFlow` — Compose State → Flow

```kotlin
LaunchedEffect(Unit) {
    snapshotFlow { query }.debounce(300).distinctUntilChanged().collectLatest(::search)
}
```
Bridges UI-owned `State` into the Flow world for `debounce`/`distinctUntilChanged`. Mind the collecting scope's lifecycle.

---

## Top gotchas

| Symptom | Cause | Fix |
|---|---|---|
| Value resets every recompose | `mutableStateOf` without `remember` | wrap in `remember` |
| Value resets on rotation | used `remember`, not `rememberSaveable` | `rememberSaveable` (+ `Saver` if complex) |
| UI never updates | mutated a plain list / read a non-observable | replace with new value via `copy()`; use `mutableStateOf` |
| Total/count drifts | stored a derived value as separate state | derive it (computed property) |
| Two screens disagree | each holds its own copy | one SSOT (repository `Flow`); both observe it |
| Caller mutates your truth | exposed `MutableState`/`MutableStateFlow` | expose `State`/`StateFlow` (`asStateFlow()`) |
| `derivedStateOf` "does nothing" | not inside `remember` (new one each frame) | `remember { derivedStateOf { … } }` |
| List rows recompose constantly | unstable item type / `List` field | `@Immutable` + `ImmutableList`, stable `key` |

---

## Golden rules

1. **One home per fact** (SSOT); ViewModels *project* the repository, never duplicate it.
2. **Derive, don't duplicate. Replace, don't mutate** (`copy()` + new collections).
3. **Hoist** by default; stateless composables = reusable + testable.
4. Expose **read-only** state; keep `Mutable*` private.
5. `derivedStateOf` only when **noisy input → quiet output**, always inside `remember`.
6. Immutable, **stable** state keeps `LazyColumn` skipping.

➡️ Related: [Side Effects](side-effects.md) · [Performance](performance.md) · [Internals](internals.md)
