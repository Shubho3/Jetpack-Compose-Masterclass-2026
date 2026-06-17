# Performance — Cheat Sheet

> One-page revision for **[Module 11 — Performance Optimization](../../modules/module-11-performance/README.md)**. **Measure first.** Fix what profiling flags, not hunches.

---

## The cost model — three phases

```text
Composition ──▶ Layout (measure + place) ──▶ Draw
 (build/skip)     (size & position)           (paint)
```
**Where you read a value decides what a change re-runs:**

| Read happens in | A change re-runs |
|---|---|
| **Composition** (value-form modifier, body) | composition **+** layout **+** draw |
| **Layout** (`offset { }`, `layout { }`) | layout + draw (skips composition) |
| **Draw** (`graphicsLayer { }`, `drawBehind { }`) | draw only ← cheapest |

---

## Profiling — find the real problem

| Tool | Tells you |
|---|---|
| **Layout Inspector → recomposition counts** | which composables recompose (and how often) |
| **Composition tracing** (system trace) | named composable timings on a timeline |
| **Animation Inspector** | scrub animations by `label` |
| **Macrobenchmark** (`FrameTimingMetric`, `StartupTimingMetric`) | P50/P90/P99 frame time & startup, on a **release-like** build |
| Compose **compiler/stability report** | which params/types are `stable` vs `unstable` |

Workflow: **reproduce → profile → identify hot composable → fix the cause → re-measure**.

---

## Stability & skipping (quick wins — full theory in [Internals](internals.md))

- A composable **skips** when all inputs are provably unchanged. Strong Skipping (2026) makes ~all restartable composables skippable; unstable params compared by **instance**.
- **Breaks skipping:** `List`/`Map`/`Set` fields, types the compiler can't prove stable, a **new instance every frame** (`items.map { }`, `obj.toUiModel()` inline), lambdas across non-Compose boundaries.
- **Fixes:** `@Immutable`/`@Stable` data classes, `kotlinx.collections.immutable` (`ImmutableList`, `persistentListOf()`), hoist a **single stable lambda**, compute UI models once.

```kotlin
@Immutable data class Row(val id: String, val tags: ImmutableList<String>)
```

---

## Lazy list optimization

```kotlin
LazyColumn {
    items(rows, key = { it.id }, contentType = { it.kind }) { Row(it) }
}
```
| Lever | Why |
|---|---|
| **`key = { it.id }`** | stable identity → reuse slots across reorders/inserts; avoids full invalidation |
| **`contentType = { … }`** | lets Compose reuse compositions across item types |
| **stable item type** | rows skip when their data didn't change |
| avoid `Modifier` w/ unstable captures per item | prevents per-frame new instances |
| don't read changing list-wide state in each item | keep item recomposition independent |

---

## Defer state reads (the biggest jank fix)

```text
Modifier.offset(x = v.dp)                  → reads v in COMPOSITION  (slow)
Modifier.offset { IntOffset(v.roundToPx(),0) } → reads v in LAYOUT   (skips composition)
Modifier.graphicsLayer { translationX = v }    → reads v in DRAW     (skips comp + layout) ✅
```
- For **continuous** values (scroll offset, animation, drag) → read inside `graphicsLayer { }` / `drawBehind { }`.
- The read must be **physically inside the lambda**. `val px = state.value` in the body then `offset { px }` = **already read in composition** (deferral lost).
- Pass hot values as **lambdas** (`() -> Float`) to children so even the caller doesn't read in composition.
- Prefer draw-phase transforms (`scaleX/Y`, `alpha`, `translationX/Y`, `rotationZ`) over layout-affecting props (`size`, `padding`) for pure visuals.
- `derivedStateOf` (how often it changes) and deferral (which phase) are **complementary**; for parallax use deferral alone — `derivedStateOf` on a continuous value adds cost.

---

## Image loading (Coil) — avoid decode jank

- Size the request to the target (`.size(...)` / let the layout constrain) — never decode full-res into a thumbnail.
- Use `contentScale`, crossfade sparingly, a memory + disk cache, and placeholders.
- Decoding is off the main thread by default; don't force synchronous decode in composition.

---

## Overdraw & main-thread safety

- **Flatten layers:** drop redundant `background`s, opaque-over-opaque draws; one fill, not three.
- Keep all I/O / parsing / sorting **off the UI thread** (`Dispatchers.Default`/`IO`); composition + the frame run on Main.
- Don't allocate in tight draw loops; hoist `Paint`/`Path`.

---

## `movableContentOf` — move a subtree without losing state

```kotlin
val item = remember { movableContentOf { ExpensiveCard(state) } }
if (wide) Row { item() } else Column { item() }   // moves between parents, keeps state/nodes
```
Preserves remembered state and emitted nodes when a child moves between layouts (e.g. orientation/master-detail).

---

## Baseline profiles & Macrobenchmark

- **Baseline profile**: ship AOT-compiled hot paths → faster startup & smoother first scrolls. Generate with the `BaselineProfileRule`, ship `baseline-prof.txt` in the app module.
- **Macrobenchmark**: measure `StartupTimingMetric` and `FrameTimingMetric` on a release build; compare **before/after** to *prove* a win.

---

## Top gotchas

| Symptom | Cause | Fix |
|---|---|---|
| Scrolling janks | reading scroll offset in composition | defer to `graphicsLayer { }` |
| All list rows recompose | unstable item type / unkeyed list / per-frame instances | `@Immutable`+`ImmutableList`, `key`, compute model once |
| "Optimized" but no change | deferral leaked back to composition (pre-read in body) | read inside the lambda; confirm flat composition count |
| Slow startup | no baseline profile | generate + ship one |
| Frame drops on images | decoding full-res / sync decode | size requests, async, cache |
| Optimizing the wrong thing | guessed instead of profiled | Layout Inspector + Macrobenchmark first |
| `derivedStateOf` everywhere | used on continuous/cheap values | only noisy→quiet; defer continuous values |

---

## Golden rules

1. **Profile before optimizing**; verify wins with Macrobenchmark.
2. **Stability** keeps skipping: immutable collections + `@Immutable`, stable lambdas, no per-frame instances.
3. **Defer hot reads** to layout/draw; the read must be inside the lambda.
4. Lazy lists: **`key` + `contentType` + stable items**.
5. Keep work **off the main thread**; flatten overdraw.
6. Don't micro-optimize cheap composables — chase what profiling flags hot.

➡️ Related: [Internals](internals.md) · [State](state.md) · [Animations](animations.md) · [Testing](testing.md) (Macrobenchmark)
