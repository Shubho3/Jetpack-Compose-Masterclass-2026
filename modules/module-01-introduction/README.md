# Module 01 — Introduction to Modern Android UI

> Understand *why* declarative UI exists and read your first `@Composable` with confidence.

**Status:** ✅ **Fully written** — all lessons built to the [Authoring Guide](../../AUTHORING-GUIDE.md).
**Prerequisites:** Kotlin basics. None within the course.
**Level:** 🟢 mostly · **Est.:** 3–4 hrs

## What you'll be able to do
- Tell the story of Android UI: Views → XML → Compose, and what each fixed.
- Explain imperative vs **declarative** UI without hand-waving.
- Read a composable and predict what recomposition does.
- Spot and correct the common "XML brain" misconceptions.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [The evolution of Android UI](01-evolution-of-android-ui.md) | Views, `findViewById`, XML, and the pain that motivated Compose. |
| 02 | [Imperative vs declarative UI](02-imperative-vs-declarative.md) | The core mental shift; UI as a function of state. |
| 03 | [Compose vs XML — head to head](03-compose-vs-xml.md) | Where each wins; interop; migration reality. |
| 04 | [Why Google built Compose](04-why-google-built-compose.md) | The problems with the View system at scale. |
| 05 | [How Compose works](05-how-compose-works.md) | Composition → recomposition; the 3 phases at a glance. |
| 06 | [The declarative mindset & misconceptions](06-declarative-mindset-misconceptions.md) | "Don't mutate views"; thinking in state, not widgets. |

## Visual anchor
```text
Traditional UI                     Compose
User action                        State change
   ↓                                  ↓
Update View                        Recomposition
   ↓                                  ↓
findViewById → mutate UI           UI re-derived from state
```

## Project
"Hello, declarative" — take one XML screen and re-express it as state + composables.

## Interview focus
Declarative vs imperative; what recomposition is; why Compose exists.

## AI assistant focus
Using AI to *explain* unfamiliar Compose code and to translate an XML layout into a composable — then verifying the translation.
