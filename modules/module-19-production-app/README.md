# Module 19 — Build a Production App (Capstone)

> Ship a portfolio-grade app end to end: Compose + Room + Retrofit + Hilt + WorkManager, tested and CI'd.

**Status:** ✅ **Fully written** — every lesson follows the [Authoring Guide](../../AUTHORING-GUIDE.md) standard.
**Prerequisites:** Modules 03, 06, 11, 13, 14 (and ideally 17–18).
**Level:** 🔴 · **Est.:** 20–30 hrs (a multi-week build)

## What you'll build
A complete app (e.g., a news/finance/fitness client) with an offline-first repository, MVI screens, background sync, full tests, and CI/CD.

## Stack
Compose · Material 3 · Type-safe Navigation · Room · Retrofit · Coroutines · Flow · Hilt · WorkManager.

## Build phases
| # | Phase | Deliverable |
|---|---|---|
| 01 | [Project & module setup](01-project-module-setup.md) | `:app`, `:core:*`, `:feature:*` skeleton. |
| 02 | [Data layer](02-data-layer.md) | Room + Retrofit + repository (single source of truth). |
| 03 | [Domain layer](03-domain-layer.md) | use cases + models. |
| 04 | [UI layer](04-ui-layer.md) | Compose + MVI + Navigation; loading/error/empty states. |
| 05 | [DI](05-dependency-injection.md) | Hilt wiring across modules. |
| 06 | [Background work](06-background-work.md) | WorkManager sync, constraints, backoff. |
| 07 | [Testing](07-testing.md) | unit + UI + screenshot + one macrobenchmark. |
| 08 | [CI/CD & monitoring](08-ci-cd-monitoring.md) | GitHub Actions pipeline; crash/perf monitoring. |

## Acceptance criteria
Works offline · survives process death · all states handled · tests green in CI · baseline profile shipped.

## AI assistant focus
Driving a full agentic build loop (Module 16) to scaffold modules — with human validation at each phase gate.
