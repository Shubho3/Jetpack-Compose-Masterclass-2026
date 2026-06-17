# Module 12 — Jetpack Compose Internals

> Explain *why* a composable skips, restarts, or recomposes — from compiler to slot table to snapshots.

**Status:** ✅ **Fully written** — all lessons authored to the [Authoring Guide](../../AUTHORING-GUIDE.md) standard.
**Prerequisites:** [Module 11 — Performance](../module-11-performance/README.md).
**Level:** 🔴 · **Est.:** 8–10 hrs

## What you'll be able to do
- Describe what the Compose compiler rewrites your functions into.
- Explain the slot table, groups, and positional memoization.
- Explain the snapshot system and how state changes propagate.
- Reason precisely about stability, immutability, and skipping.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [The Compose compiler](01-the-compose-compiler.md) | `$composer`, group calls, `Composable` lowering. |
| 02 | [The runtime & slot table](02-runtime-slot-table.md) | the gap buffer that *is* your UI's memory. |
| 03 | [Groups & positional memoization](03-groups-positional-memoization.md) | how `remember` finds last frame's value. |
| 04 | [The snapshot system](04-snapshot-system.md) | MVCC for state; reads, writes, apply. |
| 05 | [Stability & immutability](05-stability-immutability.md) | `@Stable`/`@Immutable`; the stability inference rules. |
| 06 | [How skipping works](06-how-skipping-works.md) | comparison & the skip decision; Strong Skipping. |
| 07 | [The frame lifecycle](07-frame-lifecycle.md) | recompose → measure → place → draw → apply. |

## Mental models
Explained three ways: a **city** (composition as a map of streets), a **database** (snapshots as MVCC transactions), and an **operating system** (the recomposer as a scheduler).

## Interview focus
Slot table; snapshot isolation; why `List` is unstable but `ImmutableList` is stable; what Strong Skipping changed.

## AI assistant focus
Using AI to decode compiler reports & stability metrics — and verifying its explanations against the metrics.
