# Authoring Guide — the standard every lesson meets

This is the contract. **Every lesson in every module follows this exact structure.** It exists so a beginner is never lost, a senior is never bored, and quality never drifts between modules. If you (or an AI assistant) expand a stubbed module, match this guide.

---

## File & folder conventions

```
modules/module-NN-topic/
├─ README.md            ← module hub: overview, outcomes, prerequisites, lesson index, module-level diagrams, project
├─ 01-lesson-slug.md    ← one lesson per file, numbered
├─ 02-lesson-slug.md
└─ …
```

- **One lesson per file.** Files stay focused and reviewable. If a file grows past ~400 lines, it's probably two lessons.
- **Slugs are kebab-case**, prefixed with a two-digit order number.
- **Module READMEs link every lesson** in reading order.
- Diagrams live inline (ASCII + Mermaid). Illustration *prompts* are inline too, in fenced ```text blocks, ready to paste into an image generator.

---

## The lesson template

Each lesson file has this skeleton, in this order:

```markdown
# <Lesson title>

> One-sentence "what you'll be able to do after this" outcome.

**Module:** NN · **Lesson:** NN · **Level:** Beginner→Senior · **Est. time:** N min

## 1. Concept
## 2. Visual Learning
## 3. Code (Beginner → Intermediate → Production)
## 4. Interview Questions
## 5. AI Assistant
## Recap / Key takeaways
```

The five numbered sections are **mandatory**. Details below.

---

### Section 1 — Concept

Teach the same idea three times, getting deeper each pass. Never assume the reader read the deeper tier; never make the beginner tier wrong-but-simple (simplify, don't lie).

- **🟢 For beginners** — plain language, no jargon without defining it. Answer "what is it and why do I care?"
- **🟡 For intermediate devs** — the mechanism. How it actually works, the API surface, when to reach for it.
- **🔴 For senior devs** — trade-offs, edge cases, performance/correctness implications, how it interacts with the rest of the system.

Then always include:

- **Analogy** — a concrete real-world comparison.
- **Mental model** — the one sentence to remember when half-asleep at 2am.
- **Real-world example** — where this shows up in a shipped app.

> Rule: if a senior can't learn something new from the 🔴 tier, the lesson isn't done.

---

### Section 2 — Visual Learning

Three artifacts, minimum:

1. **ASCII diagram** — for flow/sequence/phase pipelines. Fast to scan, renders everywhere.
   ```text
   State change ──▶ Recomposition ──▶ Layout ──▶ Draw
   ```
2. **Mermaid diagram** — for graphs/relationships/state machines.
   ````markdown
   ```mermaid
   graph TD
     State --> Recomposition --> Layout --> Draw
   ```
   ````
3. **Illustration prompt** — paste-ready instructions for a designer or image generator, in a ```text block. Describe scene, metaphor, labels, and style.

For **complex topics**, add as needed: **mind map**, **flow diagram**, **architecture diagram**, **process diagram**. Prefer Mermaid for these so they live in version control as text.

> Rule: a reader should be able to understand the shape of the idea from the diagrams alone, before reading a line of prose.

---

### Section 3 — Code (three tiers)

Three runnable examples, increasing in realism. **Each tier** carries the same three sub-parts:

- **Explanation** — what the code does and why it's written this way.
- **Common mistakes** — the specific traps (with the wrong code shown briefly), so readers recognize them in review.
- **Best practices** — the rules to internalize.

| Tier | Goal |
|---|---|
| **Beginner** | Smallest correct example that demonstrates the concept. |
| **Intermediate** | Realistic usage: hoisted state, a ViewModel, a list — closer to real screens. |
| **Production** | What you'd actually merge: error/loading/empty states, stability, testability, accessibility, performance-aware. |

Code rules:
- **2026 idioms only** (see baseline below). No deprecated APIs without a "❌ don't do this anymore" label.
- Compose functions are `@Composable`, PascalCase, return `Unit`, and are side-effect-free in the composition path.
- Show imports only when non-obvious.
- Prefer `StateFlow`/immutable state + state hoisting over hidden mutable singletons.

---

### Section 4 — Interview Questions

Three tiers, with **model answers** (folded behind a "▸ Answer" cue or shown after). Questions must be answerable from the lesson.

- **🟢 Beginner** — recall & definitions ("What does `remember` do?").
- **🟡 Intermediate** — application & comparison ("`remember` vs `rememberSaveable` — when each?").
- **🔴 Senior** — design & trade-offs ("How would you guarantee a single source of truth across two screens that edit the same entity?").

---

### Section 5 — AI Assistant

How to use AI on *this* topic without shipping slop. Cover the relevant tools — **ChatGPT, Claude, Gemini, Cursor, Windsurf, Copilot** — and show four things:

1. **Prompt examples** — copy-paste prompts that produce good Compose code (with context the model needs: target API, state model, constraints).
2. **AI workflow** — where AI fits (scaffolding, boilerplate, refactors) vs. where it doesn't (stability decisions, perf-critical paths) for this topic.
3. **Review workflow** — what to check in AI output, mapped to this lesson's *Common Mistakes*.
4. **Validation workflow** — how to prove it works: compile, preview, test, profile.

> Theme of the whole course: **AI drafts, you decide.** Every AI section ends by routing output back through the lesson's best-practices checklist.

---

## The three-tier teaching model (voice)

| Tier | Reader question | Your job |
|---|---|---|
| 🟢 Beginner | "What is this?" | Remove fear. One concept at a time. Define every term. |
| 🟡 Intermediate | "How do I use it well?" | Mechanism + idiomatic usage + the API. |
| 🔴 Senior | "When does it break?" | Trade-offs, internals, scale, failure modes. |

Use emoji tier markers (🟢🟡🔴) consistently so readers can self-select depth.

---

## Per-lesson quality checklist

A lesson is **done** only when all are true:

- [ ] All 5 sections present and non-trivial.
- [ ] Concept taught at 3 levels + analogy + mental model + real example.
- [ ] At least 1 ASCII **and** 1 Mermaid diagram **and** 1 illustration prompt.
- [ ] 3 code tiers, each with Explanation · Common Mistakes · Best Practices.
- [ ] Code uses 2026 idioms (no silent deprecated APIs).
- [ ] 3 tiers of interview questions **with answers**.
- [ ] AI section: prompt + workflow + review + validation.
- [ ] A senior learns something from 🔴 tiers.
- [ ] Recap with key takeaways.

---

## Tech baseline (keep code honest)

| Area | Default |
|---|---|
| Language | Kotlin 2.x, K2 compiler |
| Compose | Compose BOM, Material 3; compiler via `org.jetbrains.kotlin.plugin.compose` |
| Recomposition | Strong Skipping default; favor stable/immutable types |
| State | `State`/`MutableState`, `StateFlow`; hoist by default; UDF |
| Navigation | Type-safe Navigation Compose (serialization routes) |
| Async | Coroutines + Flow; `Dispatchers` discipline; main-safety |
| DI | Hilt |
| Data | Room + DataStore; Retrofit/Ktor + kotlinx.serialization |
| Testing | JUnit, MockK, Turbine, Compose Testing APIs, screenshot + Macrobenchmark |

When unsure about a current API name or signature, **verify against the latest Compose BOM** rather than guessing — and label anything version-sensitive.
