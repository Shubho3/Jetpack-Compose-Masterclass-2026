# Animations — Cheat Sheet

> One-page revision for **[Module 10 — Animations Masterclass](../../modules/module-10-animations/README.md)**. Set the **destination, not the path** — and keep hot reads out of composition.

---

## Which animation API? (decision tree)

```text
Animate a single value from state, fire-and-forget? ........ animate*AsState(target)
Animate content as it ENTERS / LEAVES the screen? .......... AnimatedVisibility(visible) { … }
Swap BETWEEN content states (text/number/layout)? .......... AnimatedContent(targetState) { … }
Need imperative / GESTURE-driven / interruptible control? .. Animatable + coroutine
Loop forever (loader, pulse, shimmer)? ..................... rememberInfiniteTransition()
Coordinate SEVERAL values off one state? ................... updateTransition(state)
Match an element across destinations? ...................... SharedTransitionLayout + sharedElement
Animate LAYOUT/size changes smoothly? ...................... LookaheadScope (+ animateBounds)
```

---

## `animate*AsState` — fire-and-forget

```kotlin
val size by animateDpAsState(if (expanded) 200.dp else 100.dp, label = "size")
val alpha by animateFloatAsState(if (visible) 1f else 0f, animationSpec = tween(250), label = "a")
```
Family: `animateDpAsState`, `animateColorAsState`, `animateFloatAsState`, `animateIntAsState`, `animateOffsetAsState`, …

- Read the **returned** value — feeding the raw `if` back into the modifier re-introduces the snap.
- Retargets smoothly mid-flight (springs carry **velocity**) but **can't pause/reverse/drag** → that's `Animatable`.
- `label` shows it in the Animation Inspector; `finishedListener` fires once on settle.
- `animateColorAsState` interpolates in a **perceptual color space** (Oklab) — don't roll your own ARGB lerp.

---

## `spring` vs `tween` vs `snap`

| Spec | Personality | Use for |
|---|---|---|
| **`spring()`** *(default)* | duration-less, **velocity-aware** | anything **interruptible** / fast-changing targets |
| **`tween(ms, easing)`** | fixed duration + easing curve | **one-shot**, precise timing (e.g. 250ms `FastOutSlowInEasing`) |
| **`snap(delayMs)`** | no animation | conditionally disable motion |
| `keyframes { }` | per-time-fraction control | multi-stop bespoke curves |

> A `tween` **restarts its clock** on retarget (can look like a stutter); a `spring` flows from current value + velocity. Interruptible → prefer `spring`.

---

## `AnimatedVisibility` & `AnimatedContent`

```kotlin
AnimatedVisibility(visible, enter = fadeIn() + expandVertically(), exit = fadeOut() + shrinkVertically()) {
    Banner()
}
AnimatedContent(targetState = count, transitionSpec = {
    (slideInVertically { it } + fadeIn()) togetherWith (slideOutVertically { -it } + fadeOut())
}, label = "count") { Text("$it") }
```
- Enter/exit combine with `+`: `fadeIn/Out`, `slideIn/Out`, `expand/shrink`, `scaleIn/Out`.
- `AnimatedContent` uses `togetherWith` to pair enter & exit; add `.using(SizeTransform())` for size morphs.
- For numbers/counters consider `Crossfade` (simplest) or `AnimatedContent` for directional motion.

---

## `Animatable` — precise, interruptible, gesture-driven

```kotlin
val offsetX = remember { Animatable(0f) }
Modifier.pointerInput(Unit) {
    detectHorizontalDragGestures(
        onDrag = { _, dx -> scope.launch { offsetX.snapTo(offsetX.value + dx) } },
        onDragEnd = { scope.launch { offsetX.animateTo(0f, spring()) } },   // settle back
    )
}
```
- `snapTo()` (instant), `animateTo()` (animated), `stop()`, `animateDecay()` (fling with velocity).
- Reach here when you need: dragging, pause/reverse, seed/read **velocity**, snap-then-animate, coordinate with `suspend` logic.

---

## `updateTransition` & infinite transitions

```kotlin
val t = updateTransition(selected, label = "tab")
val color by t.animateColor(label = "color") { if (it) Primary else Surface }
val pad by t.animateDp(label = "pad") { if (it) 16.dp else 8.dp }   // both driven by one state
```
```kotlin
val inf = rememberInfiniteTransition(label = "shimmer")
val x by inf.animateFloat(0f, 1000f, infiniteRepeatable(tween(1200), RepeatMode.Restart), label = "x")
```
`updateTransition` keeps several values **in lockstep** off one state. ⚠️ Infinite transitions **never idle** → hang UI tests (control the clock — see [Testing](testing.md)).

---

## Shared elements & lookahead (2026)

```kotlin
SharedTransitionLayout {
    // in each destination:
    Modifier.sharedElement(rememberSharedContentState(key = "avatar-$id"), animatedVisibilityScope)
}
```
- Match by a **stable key** across screens; bounds animate automatically. Integrates with type-safe Navigation transitions.
- `LookaheadScope` runs a **lookahead pass** to know final positions/sizes, so layout changes (reflow, expand) animate; `Modifier.animateBounds(lookaheadScope)` tweens position+size.

---

## Performance: defer the read (critical for 60–120fps)

```kotlin
// ❌ reads in composition → recomposes ~every frame
Surface(Modifier.scale(scale)) { … }
// ✅ reads in DRAW → animation runs without recomposing the tree
Surface(Modifier.graphicsLayer { scaleX = scale; scaleY = scale }) { … }
```
- `animate*AsState` recomposes **at the read site** every frame. Move the read into `graphicsLayer { }` / `offset { }` / `drawBehind { }`.
- Prefer draw-phase transforms (`scaleX/Y`, `alpha`, `translation`, `rotationZ`) over **layout** props (`size`, `padding`) for pure visual feedback — `size` re-runs layout every frame.
- Pass animated values to children as **lambdas** (`() -> Float`) so the caller doesn't read them in composition.

---

## Top gotchas

| Symptom | Cause | Fix |
|---|---|---|
| Value snaps, no animation | placed raw `if` target in modifier | read the **returned** animated value |
| Animation stutters on rapid toggle | `tween` restarts its clock | use `spring` (velocity-preserving) |
| List/animation janks | animated value read in composition | defer to `graphicsLayer { }` |
| Layout thrash on "feedback" | animating `size`/`padding` | animate `scale`/`alpha` in draw |
| Can't drag / pause it | used `animate*AsState` | use `Animatable` |
| UI test hangs forever | infinite transition never idles | `mainClock.autoAdvance = false`, advance manually |
| Muddy color midpoints | manual ARGB lerp | `animateColorAsState` (Oklab) |
| Accessibility stale | `contentDescription` didn't change with state | update it with the animated state |

---

## Golden rules

1. **Set the target, not the frames** — `animate*AsState` for state-derived values.
2. **`spring` for interruptible, `tween` for one-shot.**
3. **Defer hot reads** into `graphicsLayer`/draw; prefer draw-phase transforms over layout props.
4. **`Animatable`** when you need imperative/gesture control.
5. **`updateTransition`** to coordinate several values off one state.
6. Label animations; mind that **infinite animations hang tests**.

➡️ Related: [Side Effects](side-effects.md) · [Performance](performance.md) · [Modifiers](modifiers.md) · [Testing](testing.md)
