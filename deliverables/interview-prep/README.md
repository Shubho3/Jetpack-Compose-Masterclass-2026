# Interview Prep — *(done)*

Consolidated, ready-to-use Android interview prep that pulls together every module's questions plus a system-design playbook, concurrency Q&A, runnable AI mock scripts, and the behavioral + negotiation game. Built on and cross-linked to **[Module 20 — Career & Interview Preparation](../../modules/module-20-career-interview/README.md)**.

**Status:** ✅ **Done** — all five guides written to the [Authoring Guide](../../AUTHORING-GUIDE.md) voice and 2026 baseline (K2, Material 3, Strong Skipping, `collectAsStateWithLifecycle`, immutable collections, Hilt, type-safe Navigation).

## Contents
| File | Contents |
|---|---|
| [`question-bank.md`](question-bank.md) | 90+ curated questions by topic (state, recomposition, modifiers, layout, side effects, performance, internals, architecture, testing, coroutines, navigation/theming/lifecycle), each tagged 🟢🟡🔴 with a concise model answer, plus a rapid-fire round and a per-answer rubric. |
| [`system-design.md`](system-design.md) | The repeatable 5-step Android system-design framework (requirements → API/data → offline → architecture → trade-offs) + 3 fully worked examples (image feed, offline-first sync app, chat app) with Mermaid diagrams. |
| [`kotlin-coroutines.md`](kotlin-coroutines.md) | Language & concurrency Q&A — Kotlin fundamentals, structured concurrency, dispatchers, cancellation, Flow/StateFlow/SharedFlow — with answers and senior code-reading drills. |
| [`mock-interview-scripts.md`](mock-interview-scripts.md) | Copy-paste prompts to run an AI mock for every round (phone screen, deep-dive, coding, system design, behavioral, AI-era pairing, full loop) + self-grading rubrics. |
| [`behavioral.md`](behavioral.md) | STAR story templates, leveling junior→staff, failure/conflict stories, and a negotiation playbook with word-for-word scripts. |

## How to use
1. Answer **out loud** before reading the model answer — interviews test retrieval under pressure, not recognition.
2. Run a **timed AI mock** ([mock-interview-scripts.md](mock-interview-scripts.md)), then **self-grade at your target level** on the committee's rubric.
3. Your **weakest at-level signal** is the next sprint. Re-test on a spaced schedule (see the [weekly study plan](../../course/weekly-study-plan.md)).
4. Finish each phase with a **human** mock — AI can't replicate silence-pressure and skeptical follow-ups.

## Suggested path
```text
question-bank.md  ─▶  kotlin-coroutines.md  ─▶  system-design.md  ─▶  behavioral.md
        └──────────────  drill all four with  mock-interview-scripts.md  ──────────────┘
```

> **Theme of the whole course:** **AI drafts, you decide.** Use AI for infinite reps and to pressure-test your answers — then confirm the level, target the weakest signal, and own the verdict. For deeper teaching on any of these, jump to the matching **[Module 20](../../modules/module-20-career-interview/README.md)** lesson; for topic depth, see each module README's **Interview focus**. The fully-written **[Module 03](../../modules/module-03-state-management/README.md)** is the course's quality exemplar.
