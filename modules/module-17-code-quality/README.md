# Module 17 — Code Quality Engineering

> Keep a Compose codebase healthy, readable, and reviewable as it scales.

**Status:** ✅ **Fully written**
**Prerequisites:** [Module 13 — Architecture](../module-13-architecture/README.md).
**Level:** 🟡 · **Est.:** 4–6 hrs

## What you'll be able to do
- Apply SOLID/KISS/DRY/YAGNI to Compose code specifically.
- Recognize Compose code smells.
- Automate quality gates with static analysis + AI review.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [Clean Code in Kotlin/Compose](01-clean-code.md) | naming, function size, composable responsibilities. |
| 02 | [SOLID for Android](02-solid-for-android.md) | applied to ViewModels, repositories, composables. |
| 03 | [KISS, DRY, YAGNI](03-kiss-dry-yagni.md) | with Compose-specific examples (and over-abstraction traps). |
| 04 | [Compose code smells](04-compose-code-smells.md) | god composables, state in the wrong place, modifier soup. |
| 05 | [Static analysis](05-static-analysis.md) | Detekt, Ktlint, Android Lint, SonarQube; CI gates. |
| 06 | [AI-powered code review](06-ai-powered-code-review.md) | prompts and guardrails for review automation. |

## Interview focus
SOLID applied to a ViewModel; identifying a smell; what a static-analysis gate should block.

## AI assistant focus
Configuring AI review against your rules; verifying it doesn't "approve" real smells.
