# Recommended Resources

Curated, high-signal sources. Prefer **official docs** for APIs (they track the fast-moving toolchain) and the books/talks below for *understanding*.

## Official (always current — start here)
- **Android Developers — Compose** docs and pathways (developer.android.com/jetpack/compose).
- **Compose API reference** & the **Compose BOM** release notes — your source of truth for current versions.
- **Now in Android** (app + the open-source repo) — Google's reference architecture sample.
- **Android Developers Blog** & **Now in Android** updates — what changed each release.
- **Kotlin docs** (kotlinlang.org) — language, coroutines, Flow.

## Internals (Module 12 companions)
- *Jetpack Compose Internals* — Jorge Castillo (the definitive deep dive on the compiler/runtime/snapshots).
- Leland Richardson's talks on the Compose compiler & runtime.
- The **`androidx`** source itself — read `Composer`, `SnapshotState`, `SlotTable`.

## Architecture
- Google's **Guide to app architecture** (developer.android.com).
- **Now in Android** for a real modularized MVI/Clean example.
- *Architecting Android…* talks from Android Dev Summit.

## Performance
- Official **Compose performance** docs (stability, deferring reads, baseline profiles).
- **Macrobenchmark** & **Baseline Profiles** guides.
- Android Dev Summit performance sessions.

## Testing
- Official **Testing your Compose layout** guide.
- **Turbine** (Flow testing), **MockK**, **Paparazzi**/**Roborazzi** (screenshot) docs.

## AI-assisted development
- Tool docs: **Claude Code**, **Cursor**, **Gemini CLI**, **OpenAI Codex**, **Windsurf**, **GitHub Copilot**.
- Each tool's prompting/best-practices guide — patterns transfer across them.

## Communities & staying current
- **Kotlin Slack** (`#compose`), r/androiddev, Android Dev Summit talks (YouTube).
- **This Week in Android** / **Android Weekly** newsletters.

> Rule of thumb: **APIs from official docs, understanding from books/talks, currency from release notes.** Verify any version-specific detail in this course against the latest Compose BOM.
