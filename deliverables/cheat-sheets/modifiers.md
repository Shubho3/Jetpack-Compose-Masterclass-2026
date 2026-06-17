# Modifiers — Cheat Sheet

> One-page revision for **[Module 04 — Modifiers Mastery](../../modules/module-04-modifiers/README.md)**. Read a chain **top-to-bottom = outside-to-inside**. Order is the layout algorithm, not decoration.

---

## The mental model

```text
parent constraints
      │ (down — constraints SHRINK)
   padding(16)    shrinks maxW by 32, offsets child +16
   background     paints the area it's handed
   size(100)      forces 100×100 within what it received
   content
      ▲ (up — sizes GROW back, padding re-added)
```
- **Constraints flow down** the chain (outer → inner).
- **Sizes flow up** the chain (inner → outer).
- Each `LayoutModifierNode` runs `measure(measurable, constraints)`; order = nesting order of those calls.

---

## Order matters — the canonical example

| Chain | Result |
|---|---|
| `padding(16).background(Yellow)` | 16dp **gap outside**, yellow fills inside → yellow box in a transparent margin |
| `background(Yellow).padding(16)` | yellow **to the edges**, text inset 16dp inside |
| `padding(16).fillMaxWidth()` | fills the **padded** (narrower) width |
| `fillMaxWidth().padding(16)` | fills **full** width, then insets → wider element |

> Rule of thumb: **layout** modifiers (padding/size/offset/fill) change geometry; **draw** modifiers (background/border/alpha/clip) change painting/clipping. Order affects both.

---

## `size` vs `requiredSize`

```text
Must it be EXACTLY this size, even if it overflows the parent?
 ├─ yes (dictate) ... requiredSize(x): IGNORES parent constraints, centers, may overflow
 └─ no (negotiate) .. size(x): requests x, but OBEYS parent min/max → coerceIn(min,max)
```
- Stacked `size`: the **outer** one wins (it constrains the inner). `size(200).size(100)` → 200.
- `requiredSize` overflowing is the classic "why is my view bigger than its container".
- `wrapContentSize` re-opens constraints so a child can measure at its natural size inside a fixed parent.

---

## Canonical surface order (rounded, clickable, bordered card)

```kotlin
Modifier
    .padding(8.dp)                      // 1. outer MARGIN between cards
    .clip(RoundedCornerShape(20.dp))    // 2. establish the rounded shape FIRST
    .background(colorScheme.surface)    // 3. fill respects the clip
    .clickable(onClickLabel = title) {} // 4. ripple + hit area follow the clip
    .border(1.dp, outline, RoundedCornerShape(20.dp)) // 5. border traces the clipped shape
    .padding(20.dp)                     // 6. inner CONTENT inset
```
Order memory aid: **margin padding → clip → background → clickable → border → content padding**.

- `clip` changes **both draw and hit-test** regions. `clickable` *before* `clip` = rectangular touch target on a rounded visual (a11y/UX bug). `clickable` *after* `clip` = touch follows the shape.
- `border` after `clip` traces the rounded edge; before `clip` it can get clipped off.
- Pass the **same shape** to `clip`/`background`/`border` so they line up.

---

## Common modifier groups

| Job | Modifiers |
|---|---|
| Spacing / size | `padding`, `size`/`requiredSize`, `width`/`height`, `fillMaxWidth/Height/Size`, `wrapContentSize`, `weight` (in Row/Column) |
| Position | `offset(x,y)` (value) · `offset { }` (lambda, layout-phase) |
| Shape / paint | `clip(shape)`, `background(color, shape)`, `border`, `alpha`, `graphicsLayer { }` |
| Insets | `windowInsetsPadding`, `systemBarsPadding`, `imePadding`, `safeDrawingPadding` |
| Interaction | `clickable`, `combinedClickable`, `toggleable`, `selectable` |
| Focus | `focusRequester`, `focusProperties`, `onFocusChanged`, `focusable` |
| Gestures | `draggable`, `scrollable`, `transformable`, `pointerInput { }` |

---

## `clickable` & interaction sources

```kotlin
val interaction = remember { MutableInteractionSource() }
val pressed by interaction.collectIsPressedAsState()   // also collectIsHoveredAsState / Focused
Box(Modifier.clickable(
    interactionSource = interaction,
    indication = ripple(),                  // M3: ripple(); null = no ripple
    onClickLabel = "Open",                  // a11y announcement
) { open() })
```
- Hoist a **`MutableInteractionSource`** to observe pressed/hovered/focused and drive visuals.
- Always give an `onClickLabel` (or `semantics`) so screen readers announce the action.

---

## Pointer input & gestures

```kotlin
Modifier.pointerInput(Unit) {
    detectDragGestures { change, drag ->
        change.consume()                    // ❗ consume so parents/nested-scroll don't also react
        offset += drag
    }
}
```
- Prebuilt detectors: `detectTapGestures`, `detectDragGestures(AfterLongPress)`, `detectTransformGestures`.
- Raw loop: `awaitPointerEventScope { awaitFirstDown(); … awaitPointerEvent() }`.
- **`change.consume()`** is mandatory to stop other handlers / nested scroll from double-handling.
- `pointerInput(keys)`: the gesture coroutine **restarts when keys change** — key on the state the gesture reads, or it captures stale values.

---

## Nested scroll (collapsing toolbars)

```kotlin
val connection = remember { object : NestedScrollConnection {
    override fun onPreScroll(available: Offset, source: NestedScrollSource): Offset { /* consume some */ }
}}
Modifier.nestedScroll(connection)
```
`onPreScroll` (before child) / `onPostScroll` (leftover) / `onPreFling`/`onPostFling`. Consume the part the toolbar uses; return it.

---

## Custom Modifier factories

```kotlin
fun Modifier.shimmer(active: Boolean): Modifier = this.then( /* drawWithContent / composed */ )
// Prefer Modifier.Node (createModifier) for stateful, perf-sensitive custom modifiers (2026).
```
Compose reusable behavior into one factory; avoid `composed { }` for hot paths — use the `Modifier.Node` API.

---

## Top gotchas

| Symptom | Cause | Fix |
|---|---|---|
| "Padding looks wrong" | read order inside→out instead of outside→in | read top-to-bottom = outer-to-inner |
| Background touches edges unexpectedly | `background` before `padding` | put `padding` first if you want a gap |
| View bigger than its container | `requiredSize` (or two `size` calls) | use `size`; remember outer `size` wins |
| Square ripple on a rounded card | `clickable`/`background` before `clip` | `clip` first, then bg/clickable/border |
| Border clipped off | `border` before `clip` | `border` after `clip`, same shape |
| Rounded button taps "outside" still fire | `clickable` outside the `clip` | move `clickable` after `clip` |
| Gesture fights the scroll | forgot `change.consume()` | consume the change |
| Gesture uses stale state | unkeyed `pointerInput` | key `pointerInput` on the read state |

➡️ Related: [State](state.md) · [Performance](performance.md) (defer reads via lambda modifiers) · [Animations](animations.md)
