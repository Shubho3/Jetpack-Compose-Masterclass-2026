# Module 11 — Performance Optimization

> Find and fix the *real* performance problems with profiling data — not guesses.

**Status:** ✅ **Fully written** — all lessons authored to the [Authoring Guide](../../AUTHORING-GUIDE.md) standard.
**Prerequisites:** [Module 03](../module-03-state-management/README.md), [Module 06](../module-06-side-effects/README.md).
**Level:** 🔴 · **Est.:** 8–10 hrs

## What you'll be able to do
- Measure recomposition counts and frame timing.
- Cut needless recompositions with stability and deferred reads.
- Ship **baseline profiles** and verify wins with **Macrobenchmark**.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [The cost model](01-the-cost-model.md) | the three phases and what each costs. |
| 02 | [Profiling](02-profiling.md) | Layout Inspector recomposition counts; composition tracing. |
| 03 | [Stability & skipping (applied)](03-stability-skipping.md) | why a composable restarts; quick wins (full theory in M12). |
| 04 | [Lazy list optimization](04-lazy-list-optimization.md) | keys, `contentType`, stable items, avoiding full invalidation. |
| 05 | [Deferring state reads](05-deferring-state-reads.md) | lambda modifiers, `graphicsLayer`, read in draw not composition. |
| 06 | [Image loading](06-image-loading.md) | Coil config; sizing; avoiding decode jank. |
| 07 | [Overdraw & main-thread safety](07-overdraw-main-thread.md) | flatten layers; keep work off the UI thread. |
| 08 | [movableContentOf](08-movablecontentof.md) | moving subtrees without losing state. |
| 09 | [Baseline profiles & Macrobenchmark](09-baseline-profiles-macrobenchmark.md) | generate, ship, and measure startup/jank. |

## Deliverable
A benchmark report: before/after recomposition counts + a Macrobenchmark frame-timing comparison.

## Interview focus
What makes a type unstable; deferring reads; baseline profiles; how you'd diagnose jank.

## AI assistant focus
Generating a Macrobenchmark harness; reviewing a screen for unstable params and unkeyed lists.
