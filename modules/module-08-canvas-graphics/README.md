# Module 08 — Compose Canvas & Graphics

> Drop into the draw phase and render custom visuals and charts efficiently.

**Status:** ✅ **Fully written**
**Prerequisites:** [Module 05](../module-05-custom-layouts/README.md).
**Level:** 🟡🔴 · **Est.:** 6–8 hrs

## What you'll be able to do
- Use `DrawScope` to draw shapes, paths, and text.
- Apply `graphicsLayer` transforms and cheap animations.
- Build a custom chart from scratch.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [The draw phase & DrawScope](01-draw-phase-drawscope.md) | `Canvas`, `Modifier.drawBehind`/`drawWithContent`. |
| 02 | [Shapes, paths & text](02-shapes-paths-text.md) | lines, arcs, `Path`, `drawText` with a measurer. |
| 03 | [graphicsLayer & transforms](03-graphicslayer-transforms.md) | scale/rotate/alpha; why it's draw-only & cheap. |
| 04 | [Building a custom chart](04-custom-chart.md) | mapping data → pixels; axes, gridlines. |
| 05 | [Vector graphics](05-vector-graphics.md) | `ImageVector`, `painterResource`, animated vectors. |

## Projects
Analytics dashboard · Financial candlestick chart · Interactive graph (drag to inspect).

## Interview focus
Why drawing in a lambda defers reads; `graphicsLayer` vs recomposition; text measurement.

## AI assistant focus
Generating chart math; reviewing for per-frame allocations and unscaled densities.
