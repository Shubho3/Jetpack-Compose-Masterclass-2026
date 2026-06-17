# Module 07 — CompositionLocal

> Pass implicit dependencies down the tree without prop-drilling — and know exactly when *not* to.

**Status:** ✅ **Fully written**
**Prerequisites:** [Module 03](../module-03-state-management/README.md), [Module 06](../module-06-side-effects/README.md).
**Level:** 🟡🔴 · **Est.:** 3–4 hrs

## What you'll be able to do
- Use built-in CompositionLocals (context, density, content color…).
- Create and provide your own — and choose `static` vs dynamic correctly.
- Decide between CompositionLocal, parameters, and DI.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [Built-in CompositionLocals](01-built-in-compositionlocals.md) | `LocalContext`, `LocalDensity`, `LocalContentColor`, etc. |
| 02 | [compositionLocalOf vs staticCompositionLocalOf](02-compositionlocalof-vs-static.md) | recomposition scope trade-offs. |
| 03 | [Creating & providing custom locals](03-creating-providing-custom-locals.md) | `CompositionLocalProvider`, default values. |
| 04 | [CompositionLocal vs DI vs params](04-compositionlocal-vs-di-vs-params.md) | the decision rule; the implicit-dependency cost. |

## Project
A locale/theme provider exposed through a custom CompositionLocal.

## Interview focus
`static` vs dynamic local; why over-using locals hurts testability; when DI is better.

## AI assistant focus
Scaffolding a provider; reviewing for hidden coupling and wrong `static` choice.
