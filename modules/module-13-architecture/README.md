# Module 13 — Architecture for Real Apps

> Structure a multi-feature app with clear boundaries: Clean Architecture + MVI + offline-first.

**Status:** ✅ **Fully written**
**Prerequisites:** [Module 03](../module-03-state-management/README.md), [Module 06](../module-06-side-effects/README.md).
**Level:** 🟡🔴 · **Est.:** 8–10 hrs

## What you'll be able to do
- Separate UI, domain, and data with dependencies pointing inward.
- Implement MVI with a single immutable UI state and events.
- Design a repository and an offline-first sync strategy.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [Clean Architecture layers](01-clean-architecture-layers.md) | the dependency rule; module boundaries. |
| 02 | [MVVM in Compose](02-mvvm-in-compose.md) | `ViewModel` + `StateFlow` + `collectAsStateWithLifecycle`. |
| 03 | [MVI & unidirectional state](03-mvi-unidirectional-state.md) | one state, events in, effects out. |
| 04 | [Repository pattern](04-repository-pattern.md) | the single source of truth for data. |
| 05 | [Use cases / interactors](05-use-cases-interactors.md) | encapsulating business rules. |
| 06 | [Feature modularization](06-feature-modularization.md) | `:feature:*`, `:core:*`, build-time boundaries. |
| 07 | [Offline-first](07-offline-first.md) | local DB as source of truth; sync & conflict handling. |

## Project
A production-ready architecture skeleton you'll carry into the capstone (Module 19).

## Interview focus
Why dependencies point inward; MVI vs MVVM; offline-first source of truth; module boundaries.

## AI assistant focus
Generating layer scaffolding & use cases; reviewing for leaked data models across boundaries.
