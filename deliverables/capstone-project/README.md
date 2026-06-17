# Capstone Project — ✅ done

The portfolio-grade build that ties the whole course together: **`Pulse`, an offline-first news client** — Compose + Room + Retrofit + Hilt + WorkManager, fully tested, CI'd, and shipped with a Baseline Profile. This folder holds the complete planning surface; the phase-by-phase teaching lives in [Module 19 — Build a Production App](../../modules/module-19-production-app/README.md).

## What's here
- **[`spec.md`](spec.md)** — the product brief (committed to an **offline-first news client**), personas, feature list, user stories, and the explicit **Definition of Done** / acceptance criteria.
- **[`milestones.md`](milestones.md)** — the **8-phase build checklist** (setup → data → domain → UI → DI → background → testing → CI/CD), each with a key deliverable, concrete done-criteria, and a gate.
- **[`architecture.md`](architecture.md)** — the **module graph** (`:app`, `:core:*`, `:feature:*`), the dependency rule, data/domain/UI layering, key interfaces, and the offline-first data flow — with Mermaid diagrams and representative Kotlin.

> Build it in the order of [`milestones.md`](milestones.md); when every phase gate is green, the acceptance criteria in [`spec.md`](spec.md §5) are met.

## Acceptance criteria
Works offline · survives process death · all loading/error/empty states handled · unit + UI + screenshot tests green in CI · baseline profile shipped · Detekt + Lint clean. Full, verifiable list in [`spec.md` §5](spec.md).

## Grounded in
[Module 13 — Architecture](../../modules/module-13-architecture/README.md) · [Module 14 — Testing](../../modules/module-14-testing/README.md) · [Module 19 — Build a Production App](../../modules/module-19-production-app/README.md). Authored to the [Authoring Guide](../../AUTHORING-GUIDE.md) standard.
