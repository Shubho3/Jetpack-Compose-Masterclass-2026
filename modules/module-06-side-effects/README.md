# Module 06 — Side Effects

> Run coroutines, subscriptions, and one-shot work from composables — safely, keyed correctly, with no leaks.

**Status:** ✅ **Fully written**
**Prerequisites:** [Module 03 — State](../module-03-state-management/README.md).
**Level:** 🟡🔴 · **Est.:** 7–9 hrs

## What you'll be able to do
- Explain why effects must be quarantined from the composition path.
- Pick the right effect API for each job and key it correctly.
- Bridge Compose state to/from Flows and callbacks without leaks.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [Why side effects exist](01-why-side-effects-exist.md) | recomposition is frequent & order-free; what's unsafe in composition. |
| 02 | [LaunchedEffect & keys](02-launchedeffect-and-keys.md) | running suspend work; what re-launches on key change. |
| 03 | [rememberCoroutineScope](03-remembercoroutinescope.md) | launching from callbacks/events. |
| 04 | [DisposableEffect](04-disposableeffect.md) | register/unregister; cleanup on leave. |
| 05 | [SideEffect & rememberUpdatedState](05-sideeffect-and-rememberupdatedstate.md) | publishing to non-Compose; capturing latest without restart. |
| 06 | [produceState](06-producestate.md) | turning async sources into `State`. |
| 07 | [derivedStateOf](07-derivedstateof.md) | computing state from state without extra recompositions. |
| 08 | [snapshotFlow](08-snapshotflow.md) | observing Compose state as a Flow. |

## Project
Debounced search screen: type → debounce → query → results, lifecycle-safe.

## Interview focus
`LaunchedEffect` keys; `derivedStateOf` vs `remember(key)`; `rememberUpdatedState` use case; leak avoidance.

## AI assistant focus
Generating effect-heavy screens; reviewing for wrong keys, missing cleanup, and `derivedStateOf` misuse.
