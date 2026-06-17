# Module 14 — Testing Jetpack Compose

> Test each layer with the right tool: state, UI semantics, screenshots, and performance.

**Status:** ✅ **Fully written**
**Prerequisites:** [Module 13 — Architecture](../module-13-architecture/README.md).
**Level:** 🟡🔴 · **Est.:** 6–8 hrs

## What you'll be able to do
- Unit-test ViewModels and state flows with Turbine + MockK.
- Write Compose UI tests against the semantics tree.
- Add screenshot and macrobenchmark coverage.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [The testing pyramid for Compose](01-testing-pyramid.md) | what to test where; cost vs confidence. |
| 02 | [Unit testing state](02-unit-testing-state.md) | ViewModels, `StateFlow`, Turbine, MockK, coroutine test. |
| 03 | [Compose UI testing](03-compose-ui-testing.md) | `createComposeRule`, finders, semantics, actions. |
| 04 | [Integration testing](04-integration-testing.md) | navigation + ViewModel + fakes. |
| 05 | [Screenshot testing](05-screenshot-testing.md) | Paparazzi / Roborazzi; deterministic rendering. |
| 06 | [Macrobenchmark testing](06-macrobenchmark-testing.md) | startup & frame timing as a test. |

## Project
A feature with a tested ViewModel and semantics-based UI tests.

## Interview focus
Semantics tree; testing recomposition behavior; flaky-test avoidance; what *not* to assert.

## AI assistant focus
Generating test cases & fakes; reviewing for brittle selectors and untested edge states.
