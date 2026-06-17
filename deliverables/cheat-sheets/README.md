# Cheat Sheets — *(done)*

One-page, printable references. ✅ All 7 sheets written — dense, scannable quick-reference for revising before an interview or while coding (compact tables, decision trees, top gotchas, minimal snippets). Each distills a module's 🔴-tier takeaways; **not** prose lessons.

| Sheet | Covers | Source module |
|---|---|---|
| [`state.md`](state.md) | `remember` vs `rememberSaveable`, hoisting rules, UDF/MVI/MVVM, `derivedStateOf`, SSOT, stability. | [Module 03 — State Management](../../modules/module-03-state-management/README.md) |
| [`modifiers.md`](modifiers.md) | Order rules (outside-in), canonical surface chain, `size` vs `requiredSize`, gestures & nested scroll. | [Module 04 — Modifiers](../../modules/module-04-modifiers/README.md) |
| [`side-effects.md`](side-effects.md) | Which effect API for which job, keying rules, cancellation discipline. | [Module 06 — Side Effects](../../modules/module-06-side-effects/README.md) |
| [`performance.md`](performance.md) | Cost model, stability/skipping wins, deferring reads, lazy lists, baseline profiles. | [Module 11 — Performance](../../modules/module-11-performance/README.md) |
| [`internals.md`](internals.md) | Compiler, slot table, snapshots (MVCC), stability, Strong Skipping — the one-pager. | [Module 12 — Internals](../../modules/module-12-internals/README.md) |
| [`animations.md`](animations.md) | Decision tree of animation APIs, `spring` vs `tween`, deferring animated reads. | [Module 10 — Animations](../../modules/module-10-animations/README.md) |
| [`testing.md`](testing.md) | Pyramid map, finders/actions/assertions, semantics tree, the idle contract. | [Module 14 — Testing](../../modules/module-14-testing/README.md) |

> Each sheet ends with cross-links to its sibling sheets. All code is 2026-idiomatic (Kotlin 2.x/K2, Material 3, Strong Skipping, `collectAsStateWithLifecycle`, immutable collections, Hilt, type-safe Navigation).
