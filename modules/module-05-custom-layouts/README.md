# Module 05 — Measurements, Advanced Layouts & Custom Modifiers

> Drop below the built-in layouts and place children yourself with the measure/place API.

**Status:** ✅ **Fully written** — all lessons authored to the [Authoring Guide](../../AUTHORING-GUIDE.md) standard.
**Prerequisites:** [Module 02](../module-02-layouts/README.md), [Module 04](../module-04-modifiers/README.md).
**Level:** 🔴 · **Est.:** 7–9 hrs

## What you'll be able to do
- Explain the layout phase: constraints down, sizes up, placement last.
- Use intrinsic measurements and `BoxWithConstraints` deliberately.
- Write a custom `Layout` and a `SubcomposeLayout`.
- Author custom `Modifier.Node` factories.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [The layout phase & constraints](01-layout-phase-and-constraints.md) | min/max width/height; single-measure rule. |
| 02 | [Intrinsic measurements](02-intrinsic-measurements.md) | when intrinsics run and what they cost. |
| 03 | [BoxWithConstraints](03-boxwithconstraints.md) | reading constraints to branch layout. |
| 04 | [onSizeChanged & onGloballyPositioned](04-onsizechanged-and-ongloballypositioned.md) | reacting to measured size/position safely. |
| 05 | [Custom `Layout`](05-custom-layout.md) | `measure` → `layout` → `place`. |
| 06 | [SubcomposeLayout](06-subcomposelayout.md) | composing children that depend on others' size. |
| 07 | [Custom `Modifier.Node`](07-custom-modifier-node.md) | modern modifier internals; layout/draw nodes. |

## Projects
Pinterest staggered grid · Timeline layout · Mind-map layout.

## Interview focus
Why Compose measures once; intrinsics cost; `Layout` vs `SubcomposeLayout`.

## AI assistant focus
Drafting a custom `Layout` from a sketch; reviewing for double-measure and constraint-violation bugs.
