# Internals — Cheat Sheet

> One-page revision for **[Module 12 — Jetpack Compose Internals](../../modules/module-12-internals/README.md)**. Explain *why* a composable **skips, restarts, or recomposes** — compiler → slot table → snapshots.

---

## The pipeline

```text
@Composable fn ──[Compose compiler/K2 plugin]──▶ fn($composer, $changed) with group calls
        │
   $composer reads/writes ──▶ Slot Table (gap buffer = your UI's memory)
        │
   State reads tracked ──▶ Snapshot system (MVCC) ──▶ invalidates scopes
        │
   Recomposer schedules ──▶ recompose → measure → place → draw → apply
```

---

## 1. The compiler

Rewrites each `@Composable` to take a `$composer` and a `$changed: Int` bitmask, and wraps the body in **group calls**:
```kotlin
$composer.startRestartGroup(key)
if (inputsUnchanged($changed) && $composer.skipping) $composer.skipToGroupEnd()
else { /* body */ }
$composer.endRestartGroup()?.updateScope { … }   // how it re-invokes on change
```
- **Restartable** = runtime has a scope to re-invoke it.
- **Skippable** = a `$changed`-guarded `skipToGroupEnd()` branch exists.
- `inline @Composable` functions introduce **no skip boundary** — they recompose with the caller.

---

## 2. Runtime & slot table

- The **slot table** is a **gap buffer** storing groups, remembered values, and node references — the persistent memory of the composition.
- **Positional memoization**: `remember` finds last frame's value by the call's **position** in the table, not by name.
- Recomposition = re-walking the table, comparing, and updating only changed groups.

---

## 3. Groups & positional memoization

- Every composable call opens a **group** (a slot range) keyed by source position.
- Conditionals/loops change structure → use **`key(id) { }`** in lists so identity tracks the item, not the index (prevents state mix-ups on reorder/insert).
- `movableContentOf` lets a group move between parents **keeping its slots** (state + nodes).

---

## 4. Snapshot system (MVCC)

- State lives in **snapshots** — like database transactions (Multi-Version Concurrency Control).
- **Read** in composition → records a dependency (subscription). **Write** → creates a new version. **Apply** → commits and notifies readers, invalidating their scopes.
- Gives **isolation**: each thread sees a consistent snapshot; concurrent writes are mediated on apply.
- `Snapshot.withMutableSnapshot { }` batches writes atomically; `snapshotFlow { }` observes reads as a Flow.

---

## 5. Stability & immutability

| Compiler classification | Meaning |
|---|---|
| **stable** | public properties don't change without notifying Compose; `equals` is consistent |
| **unstable** | could change unseen → can't trust equality for skipping |

- **Inferred** automatically for types the compiler can see (all `val` of stable types → stable).
- **Promises** you make when it can't infer: `@Immutable` (never changes after construction) / `@Stable` (changes only via Compose-observable means).
- **`List`/`Map`/`Set` are unstable** (interfaces — could be mutable impls). `ImmutableList`/`persistentListOf()` are **stable**.
- Types from other modules without the Compose plugin are treated **unstable** → annotate or add the plugin.

---

## 6. How skipping works

```text
Parent recomposes → for each child:
 1. composer.skipping?  (a recomposition, not first compose) ── no → RUN
 2. all params unchanged?
      $changed bit = Static / Same        → unchanged (no compare)
      $changed bit = Uncertain + STABLE    → compare by ==      (trustworthy)
      $changed bit = Uncertain + UNSTABLE  → compare by INSTANCE (Strong Skipping)
 → all unchanged: skipToGroupEnd() (reuse last frame)   |  any changed: RUN body
```

**Strong Skipping (2026 default) changed two things:**
1. **Unstable params compared by referential (instance) equality** → every restartable composable becomes skippable. Same instance skips; a **new instance each frame** runs.
2. **Lambdas auto-`remember`ed** → `onClick = { vm.foo() }` no longer allocates a fresh instance each recompose that breaks the child's skip.

`skipToGroupEnd()` is a **slot-reader jump**, not a no-op: it advances past the group, reusing stored state and emitted nodes → genuinely free of composition cost.

---

## Why a composable still won't skip

| Cause | Fix |
|---|---|
| New instance every frame (`map`, `toUiModel()` inline, rebuilt object) | compute once / hoist; pass stable instances |
| Param of a type reported `unstable` you keep reallocating | `@Immutable` + immutable collections; add Compose plugin in that module |
| Lambda capturing fresh objects / crossing a non-Compose boundary | capture only stable values (ids); hoist a single lambda |
| Reading changing state in the body | that's a **correct subscription**, not a skip bug — don't "fix" it |
| `inline @Composable` | has no skip boundary by design |

> **Skip failure** (wasted work) ≠ **correct state subscription** (must recompose). Verify with the **report** + **recomposition counts**, never vibes.

---

## 7. The frame lifecycle

```text
state write ──▶ snapshot apply ──▶ invalidate scopes ──▶ RECOMPOSE
            ──▶ MEASURE ──▶ PLACE ──▶ DRAW ──▶ (frame presented)
```
Layout & draw have their **own** invalidation independent of composition — that's why deferring a read to draw skips composition entirely.

---

## Three mental models

| Model | Maps to |
|---|---|
| **City** | composition = a map of streets (groups = blocks) |
| **Database** | snapshots = MVCC transactions (read/write/apply) |
| **Operating system** | the Recomposer = a scheduler dispatching recomposition |

---

## Interview-ready one-liners

- *Slot table* = a **gap buffer** that is the composition's memory; `remember` is positional memoization into it.
- *Why is `List` unstable but `ImmutableList` stable?* `List` is an interface that **could** be a mutable impl, so equality isn't trustworthy; `ImmutableList` guarantees it can't change.
- *What did Strong Skipping change?* Unstable params compared by **instance** + **auto-remembered lambdas** → ~all restartable composables now skippable.
- *Snapshot isolation* = each reader sees a consistent version (MVCC); writes commit on **apply** and notify subscribers.
- *Restartable vs skippable* = "has a scope to re-invoke" vs "has a `$changed`-guarded skip branch."

➡️ Related: [Performance](performance.md) · [State](state.md) (stability in practice)
