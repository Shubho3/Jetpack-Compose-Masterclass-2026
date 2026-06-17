# Lesson 05 — Dependency Injection (Hilt Across Modules)

> After this lesson you can wire a whole multi-module app with Hilt: bind repository interfaces to implementations, provide Room/Retrofit singletons, inject ViewModels into Compose, choose the right scope, and disambiguate with qualifiers — so the app assembles itself and stays testable.

**Module:** 19 · **Lesson:** 05 · **Level:** 🟢🟡🔴 · **Est. time:** 100–120 min

---

## 1. Concept

### 🟢 For beginners — *what is it and why do I care?*

We've built three layers — data, domain, UI — and each needs the one below it: the repository needs the Room DAO and the Retrofit API; the use case needs the repository; the ViewModel needs the use cases. Somebody has to **create all those objects and hand them to each other**. Doing it by hand (`HeadlinesViewModel(GetHeadlinesUseCase(DefaultNewsRepository(api, dao)))`) is tedious, repeated everywhere, and a nightmare to change.

**Dependency Injection (DI)** flips it around: instead of each class *making* what it needs, it just **declares** what it needs (in its constructor) and a framework **provides** it. **Hilt** is the standard DI framework for Android — built on Dagger, it generates all that wiring code for you at compile time.

In practice you write a class's constructor honestly ("I need a `NewsRepository`"), annotate things so Hilt knows how to build them, and Hilt assembles the whole object graph — including handing ViewModels to your Compose screens. You stop writing glue code; you describe the recipe once and the framework cooks.

Why care for a *production* app? Because the same wiring that's annoying by hand is exactly what makes the app **testable**: in a test you tell Hilt (or just the constructor) to use a *fake* repository instead of the real one. DI is what lets you swap the network for a fake without touching the screens.

### 🟡 For intermediate devs — *the mechanism*

Hilt's building blocks, mapped to our app:

- **`@Inject constructor(...)`** on classes you own (use cases, the repository impl) — Hilt knows how to build them by reading the constructor.
- **`@Module` + `@Binds`** to tell Hilt *which implementation* satisfies an interface: "`NewsRepository` → `DefaultNewsRepository`." Cheap, abstract-method binding.
- **`@Module` + `@Provides`** for things you **don't own** and can't annotate — building a Retrofit instance or the Room database.
- **`@InstallIn(SingletonComponent::class)`** etc. — declares *which Hilt component* (lifecycle scope) a binding lives in.
- **`@HiltViewModel`** + `hiltViewModel()` in Compose — injects ViewModels with their constructor dependencies, scoped to the nav back stack entry.
- **`@HiltAndroidApp`** on the `Application`, `@AndroidEntryPoint` on the activity — the entry points that bootstrap the graph.

A scope (`@Singleton`, `@ViewModelScoped`, …) means "**one instance per that lifetime**." The Room database and Retrofit are `@Singleton` (one for the whole app); a ViewModel is per-screen.

```text
   @HiltAndroidApp Application
        └─ SingletonComponent  → @Singleton: NewsDatabase, Retrofit, NewsApi, NewsRepository
              └─ ViewModelComponent → @HiltViewModel HeadlinesViewModel (per nav entry)
                    └─ injected use cases → injected repository → injected api/dao
```

### 🔴 For senior devs — *trade-offs, edges, internals*

- **`@Binds` vs `@Provides` is not interchangeable — pick correctly.** `@Binds` is an *abstract* method that maps an interface to an impl Hilt already knows how to build (because the impl has an `@Inject` constructor). It generates less code and is faster to process. `@Provides` is a *concrete* method that **constructs** an object — required for types you don't own (Retrofit, OkHttp, Room) or that need assembly logic. Using `@Provides` to new-up your own injectable class is wasteful; using `@Binds` for a Retrofit instance is impossible. Prefer `@Binds` for interface→impl, `@Provides` for third-party/assembled objects.

- **Scope is about *sharing and lifetime*, not "make it fast."** `@Singleton` means one instance for the app's life — correct for expensive, stateless, shared things (DB, networking, repositories). Over-scoping to `@Singleton` is a memory/correctness hazard (a `@Singleton` that holds an `Activity` context leaks; a `@Singleton` with mutable per-user state corrupts across accounts). Under-scoping (no scope) is usually *fine and cheap* — unscoped bindings just create a new instance per request, which is correct for stateless use cases. Reach for a scope only when you must **share one instance** within a lifetime.

- **Module placement and `@InstallIn` define visibility and lifetime.** A binding installed in `SingletonComponent` is app-wide; in `ViewModelComponent`, it lives and dies with the ViewModel. Put DB/network/repository modules in `SingletonComponent`. Don't install something needing an `Activity` in `SingletonComponent` — it can't see one, and you'll either fail to compile or leak.

- **Qualifiers disambiguate same-type bindings — and you *will* need them.** Two `OkHttpClient`s (authenticated vs not), two `CoroutineDispatcher`s (`IO` vs `Default`), two `String` base URLs — Hilt can't tell them apart by type. Define `@Qualifier annotation class AuthClient` / `@Dispatcher(IO)` and annotate both the provider and the injection point. Injecting `Dispatchers.IO` *directly* into classes (instead of a qualified, injected `CoroutineDispatcher`) is the subtle anti-pattern that makes those classes untestable — inject dispatchers so tests can substitute a `TestDispatcher`.

- **Multi-module DI: where do modules live?** In a feature-modularized app, Hilt modules typically live in the module that owns the implementation (`:core:data` provides the repository binding; `:core:network` provides Retrofit). Because Hilt aggregates all `@InstallIn` modules at the `:app` level via its Gradle plugin, the `:app` doesn't need to know the details — it just applies Hilt and the graph composes. Keep `@Provides`/`@Binds` next to what they build.

- **`@HiltViewModel` scoping is tied to the nav entry, which matters for state.** With Navigation Compose, `hiltViewModel()` scopes the VM to the current `NavBackStackEntry` — so it survives config changes but is cleared when you pop the destination. To **share** a VM across a nested graph (e.g. a multi-step flow), scope `hiltViewModel()` to the parent back stack entry deliberately; doing it accidentally (or grabbing the activity VM) leaks state between unrelated screens.

- **DI keeps the build honest about layering.** Because `:core:data` binds the repository and features depend only on the interface (from `:core:domain`/`:core:model`), a feature literally can't construct or even see `DefaultNewsRepository`. DI + module boundaries (Lesson 01) together make the architecture enforced rather than encouraged.

### Analogy

Hilt is the **stage crew of a theater production**. The actors (your classes) don't go hunting for their own props — each one's part (the constructor) lists what they need ("I need a sword, a lantern"). The **prop master (Hilt)** reads every part, builds or fetches each prop **once where it makes sense** (one shared throne for the whole play = `@Singleton`; a fresh letter for each scene = unscoped), and hands each actor exactly what their part declared as they step on stage. When two props are the same type but different ("the king's crown" vs "the jester's crown"), a **label** (qualifier) tells the crew which is which. The director (you) never carries props around — you write the parts, the crew provisions the show.

### Mental model

> **Classes declare what they need in their constructor; Hilt builds the object graph. `@Binds` maps interface→impl, `@Provides` builds things you don't own, scope decides how long an instance is shared, and qualifiers disambiguate same-type bindings.**

### Real-world example

Practically every modern Android app at scale (Google's own apps, *Now in Android*) is wired with Hilt: a `:core:network` module `@Provides` an `OkHttpClient` + `Retrofit` as `@Singleton`; a `:core:database` module `@Provides` the Room `@Singleton`; `:core:data` `@Binds` each repository interface to its impl; features inject `@HiltViewModel`s that take use cases. Swapping in a test double for instrumentation tests is a one-line `@TestInstallIn` — the payoff of doing DI properly.

---

## 2. Visual Learning

**ASCII — Hilt components (scopes) and what lives where:**
```text
   ┌──────────────────────── SingletonComponent (@Singleton) ─────────────────────────┐
   │  Retrofit  ──▶  NewsApi          NewsDatabase  ──▶  ArticleDao                     │
   │       └──────────────┬───────────────────────────────────┘                        │
   │                      ▼                                                             │
   │            DefaultNewsRepository  ──(@Binds)──▶  NewsRepository  (one for the app) │
   └───────────────────────────────┬──────────────────────────────────────────────────┘
                                    │ injected
   ┌──────────────────────── ViewModelComponent (@HiltViewModel) ─────────────────────┐
   │  HeadlinesViewModel(getHeadlines, refresh)   ← scoped to the nav back-stack entry │
   │        └─ GetHeadlinesUseCase (@Inject, unscoped — new per request, stateless)    │
   └───────────────────────────────────────────────────────────────────────────────────┘
```

**Mermaid — the object graph Hilt assembles:**
```mermaid
graph TD
    APP["@HiltAndroidApp Application"] --> SC[SingletonComponent]
    SC -->|@Provides| RT[Retrofit]
    RT -->|@Provides| API[NewsApi]
    SC -->|@Provides| DB[NewsDatabase]
    DB --> DAO[ArticleDao]
    API --> IMPL[DefaultNewsRepository]
    DAO --> IMPL
    IMPL -->|@Binds| REPO["NewsRepository (interface)"]
    REPO --> UC[GetHeadlinesUseCase @Inject]
    UC --> VM["@HiltViewModel HeadlinesViewModel"]
    VM -->|hiltViewModel| UI[HeadlinesRoute]
    style IMPL fill:#1f6feb,color:#fff
    style REPO fill:#238636,color:#fff
```

**Illustration prompt:**
```text
Illustration: backstage of a theater, a busy PROP MASTER's station labeled "Hilt".
Pinned scripts (labeled "constructors") list what each actor needs. The prop master hands
a single shared golden THRONE labeled "@Singleton (Database, Retrofit, Repository)" that
stays on a fixed pedestal, and fresh paper LETTERS labeled "unscoped (use cases)" to actors
as they pass. Two identical crowns sit in labeled bins "@AuthClient" and "@PlainClient"
(qualifiers). An actor steps onto a stage panel labeled "Compose screen" receiving a
"@HiltViewModel". Caption: "Declare what you need; the crew provisions the show." Warm
backstage lighting, clearly labeled, modern.
```

---

## 3. Code (Build steps)

> Wire the news app with Hilt across `:core:network`, `:core:database`, `:core:data`, and the feature. Hilt 2.5x, KSP, Compose `hiltViewModel()`, Kotlin 2.1.

### 🟢 Beginner — bootstrap Hilt and inject a ViewModel into Compose

The `Application` and entry point:
```kotlin
@HiltAndroidApp
class NewsApplication : Application()        // bootstraps the whole graph

@AndroidEntryPoint
class MainActivity : ComponentActivity() {   // entry point for Compose
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { NewsApp() }
    }
}
```

A ViewModel injected into a Composable:
```kotlin
@HiltViewModel
class HeadlinesViewModel @Inject constructor(
    private val getHeadlines: GetHeadlinesUseCase,    // Hilt provides these
    private val refreshHeadlines: RefreshHeadlinesUseCase,
) : ViewModel() { /* … from Lesson 04 … */ }

@Composable
fun HeadlinesRoute(
    vm: HeadlinesViewModel = hiltViewModel(),   // ← Hilt injects it, scoped to the nav entry
    onArticleClick: (String) -> Unit,
) { /* collect uiState, render … */ }
```

**Explanation.** `@HiltAndroidApp` generates the app-level component; `@AndroidEntryPoint` lets the activity (and its Composables) receive injections. `@HiltViewModel` + `hiltViewModel()` is all it takes to get a fully-wired ViewModel into a screen — Hilt builds its use cases, which build the repository, which build the API/DAO. You wrote *zero* `new`.

**Common mistakes.**
```kotlin
// ❌ Forgetting @HiltAndroidApp on the Application (or not registering it in the manifest)
//    → "hilt components not generated" at runtime.

// ❌ Constructing the ViewModel manually, bypassing Hilt's scoping & graph.
val vm = remember { HeadlinesViewModel(GetHeadlinesUseCase(...)) }   // defeats the point
```

**Best practices.**
- `@HiltAndroidApp` on the `Application` (registered in the manifest), `@AndroidEntryPoint` on activities.
- Use `@HiltViewModel` + `hiltViewModel()`; never construct ViewModels by hand.
- Annotate your own classes with `@Inject constructor` so Hilt can build them automatically.

---

### 🟡 Intermediate — `@Binds` (interface→impl) and `@Provides` (things you don't own)

Bind the repository interface to its implementation (`:core:data`):
```kotlin
@Module
@InstallIn(SingletonComponent::class)         // app-wide lifetime
abstract class DataModule {
    @Binds
    @Singleton
    abstract fun bindNewsRepository(impl: DefaultNewsRepository): NewsRepository   // interface → impl
}

class DefaultNewsRepository @Inject constructor(   // Hilt builds it from the constructor
    private val api: NewsApi,
    private val dao: ArticleDao,
) : NewsRepository { /* … */ }
```

Provide Retrofit and Room — types you don't own (`:core:network`, `:core:database`):
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl("https://api.example-news.com/")
        .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
        .build()

    @Provides @Singleton
    fun provideNewsApi(retrofit: Retrofit): NewsApi = retrofit.create(NewsApi::class.java)
}

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides @Singleton
    fun provideDatabase(@ApplicationContext context: Context): NewsDatabase =
        Room.databaseBuilder(context, NewsDatabase::class.java, "news.db")
            .addMigrations(MIGRATION_1_2)
            .build()

    @Provides
    fun provideArticleDao(db: NewsDatabase): ArticleDao = db.articleDao()   // unscoped: cheap accessor
}
```

**Explanation.** `@Binds` is the right tool for "this interface is satisfied by that impl" — Hilt already knows how to build `DefaultNewsRepository` (it has an `@Inject` constructor), so the binding is just a one-line abstract method. `@Provides` is required for **Retrofit and Room**, which you can't annotate with `@Inject` — you must *construct* them. `@ApplicationContext` injects the app context (never an activity context into a `@Singleton`). The DAO is unscoped — it's a trivial accessor off the singleton DB.

**Common mistakes.**
```kotlin
// ❌ Using @Provides to build your own injectable class (verbose, unnecessary).
@Provides fun provideRepo(api: NewsApi, dao: ArticleDao): NewsRepository =
    DefaultNewsRepository(api, dao)        // just use @Binds + @Inject constructor instead

// ❌ Injecting an Activity Context into a @Singleton (provider/DB) → leaks the Activity.
fun provideDatabase(context: Context)      // must be @ApplicationContext
```

**Best practices.**
- **`@Binds`** for interface→impl (with `@Inject constructor` on the impl); **`@Provides`** for third-party/assembled objects (Retrofit, Room, OkHttp).
- Install DB/network/repository modules in **`SingletonComponent`** with `@Singleton`.
- Use **`@ApplicationContext`** for app-scoped Context; never leak an `Activity` into a singleton.

---

### 🔴 Production — qualifiers, injected dispatchers, and test swapping

Qualifiers for same-type bindings (dispatchers + an authenticated client):
```kotlin
@Qualifier @Retention(BINARY) annotation class Dispatcher(val type: AppDispatcher)
enum class AppDispatcher { Default, IO }

@Module @InstallIn(SingletonComponent::class)
object DispatchersModule {
    @Provides @Dispatcher(AppDispatcher.IO)
    fun provideIo(): CoroutineDispatcher = Dispatchers.IO

    @Provides @Dispatcher(AppDispatcher.Default)
    fun provideDefault(): CoroutineDispatcher = Dispatchers.Default
}

// Inject the dispatcher (don't hardcode Dispatchers.IO) → testable.
class SyncManager @Inject constructor(
    private val repo: NewsRepository,
    @Dispatcher(AppDispatcher.IO) private val ioDispatcher: CoroutineDispatcher,
) { /* uses ioDispatcher, swappable in tests */ }
```

Swapping a real binding for a fake in tests (`@TestInstallIn`):
```kotlin
@Module
@TestInstallIn(components = [SingletonComponent::class], replaces = [DataModule::class])
abstract class FakeDataModule {
    @Binds @Singleton
    abstract fun bindFakeRepo(fake: FakeNewsRepository): NewsRepository   // real repo replaced
}
```

**Explanation.** When two bindings share a type (`CoroutineDispatcher` for `IO` and `Default`), Hilt needs a **qualifier** to tell them apart — annotate both the provider and the injection site. Crucially, classes inject a **qualified `CoroutineDispatcher`** instead of referencing `Dispatchers.IO` directly, which is what makes them unit-testable (a test injects a `StandardTestDispatcher`). `@TestInstallIn(replaces = …)` swaps the entire `DataModule` for a fake in instrumentation tests — the whole app runs against a fake repository with **one annotation**, the real payoff of disciplined DI. (Testing is Lesson 07.)

**Common mistakes.**
```kotlin
// ❌ Two same-type providers with no qualifier → Hilt: "DuplicateBindings" compile error.
@Provides fun io(): CoroutineDispatcher = Dispatchers.IO
@Provides fun default(): CoroutineDispatcher = Dispatchers.Default   // which one?!

// ❌ Hardcoding Dispatchers.IO inside a class instead of injecting it → can't make tests deterministic.
class SyncManager @Inject constructor(repo: NewsRepository) {
    suspend fun sync() = withContext(Dispatchers.IO) { … }   // untestable timing
}
```

**Best practices.**
- Use **`@Qualifier`** annotations for any same-type bindings (dispatchers, multiple clients/URLs).
- **Inject dispatchers**; never hardcode `Dispatchers.IO`/`Default` in injectable classes.
- Use **`@TestInstallIn(replaces = …)`** to swap real modules for fakes in tests — design DI so this is a one-liner.
- Scope deliberately: `@Singleton` only for shared, stateless, expensive things; leave stateless use cases **unscoped**.

---

## 4. Interview Questions

**🟢 Beginner**

1. *What problem does dependency injection solve, and what is Hilt?*
   > DI removes the boilerplate and tight coupling of classes constructing their own dependencies — a class declares what it needs in its constructor and a framework provides it. Hilt is the standard Android DI framework (built on Dagger) that generates the wiring at compile time and integrates with Android components and Compose.
2. *How do you get a ViewModel into a Composable with Hilt?*
   > Annotate the ViewModel with `@HiltViewModel` and an `@Inject constructor`, ensure the host activity is `@AndroidEntryPoint` and the `Application` is `@HiltAndroidApp`, then call `hiltViewModel()` in the Composable.

**🟡 Intermediate**

3. *When do you use `@Binds` vs `@Provides`?*
   > `@Binds` (an abstract method) maps an interface to an implementation that already has an `@Inject` constructor — less generated code, faster. `@Provides` (a concrete method) **constructs** objects you don't own or that need assembly logic (Retrofit, OkHttp, Room). Use `@Binds` for interface→impl, `@Provides` for third-party/assembled types.
4. *What does a Hilt scope like `@Singleton` actually mean, and what's the risk of over-scoping?*
   > It means one instance for that component's lifetime (`@Singleton` = the whole app). Over-scoping is a hazard: a `@Singleton` holding an `Activity` context leaks it; a `@Singleton` with mutable per-user state corrupts across accounts. Unscoped bindings are cheap and correct for stateless classes; scope only to **share** one instance within a lifetime.

**🔴 Senior**

5. *Why and how do you inject `CoroutineDispatcher`s instead of using `Dispatchers.IO` directly?*
   > Hardcoding `Dispatchers.IO` makes a class's threading untestable — tests can't substitute a deterministic dispatcher. Instead, provide qualified dispatchers (`@Dispatcher(IO)` / `@Dispatcher(Default)`) via a Hilt module and inject them. Tests then inject a `StandardTestDispatcher`/`TestScope` for controllable, deterministic timing. Qualifiers are needed because both are the same type.
6. *In a multi-module app, where do Hilt modules live and how does `:app` get the full graph?*
   > Modules live next to the implementation they wire — `:core:network` provides Retrofit, `:core:data` binds the repository — each annotated with `@InstallIn`. Hilt's Gradle plugin aggregates all `@InstallIn` modules at the `:app`/component-root level, so `:app` just applies Hilt and the graph composes without knowing the details. This keeps providers cohesive with what they build and preserves module boundaries (features see only the interface).

---

## 5. AI Assistant

**Prompt example (wiring a module with Hilt):**
```text
Wire a multi-module news app with Hilt (2.52, KSP, Kotlin 2.1).
- :core:network NetworkModule (@InstallIn SingletonComponent, object, @Provides @Singleton):
  Retrofit with kotlinx.serialization converter, and NewsApi from it.
- :core:database DatabaseModule: provide NewsDatabase via Room (use @ApplicationContext) with
  addMigrations(MIGRATION_1_2); provide ArticleDao (unscoped).
- :core:data DataModule (abstract, @Binds): bind NewsRepository → DefaultNewsRepository (@Inject ctor),
  @Singleton.
- A DispatchersModule providing qualified @Dispatcher(IO)/@Dispatcher(Default) CoroutineDispatchers;
  inject the qualified dispatcher into a SyncManager (don't hardcode Dispatchers.IO).
- @HiltViewModel HeadlinesViewModel injected via hiltViewModel(); @HiltAndroidApp Application;
  @AndroidEntryPoint MainActivity.
Show a @TestInstallIn module that replaces DataModule with a FakeNewsRepository binding.
```

**AI workflow — where it helps on *this* topic.**
- ✅ Great for: generating the module boilerplate (`@Provides`/`@Binds`), the `@HiltAndroidApp`/`@AndroidEntryPoint` wiring, qualifier annotations, and `@TestInstallIn` test modules.
- ⚠️ Not for: your **scoping decisions** (what truly deserves `@Singleton`) — models over-scope, sometimes leak an `Activity` context into singletons, use `@Provides` where `@Binds` belongs, and hardcode `Dispatchers.IO`.

**Review workflow — check AI output against this lesson's *Common Mistakes*:**
- **`@Binds`** used for interface→impl (impl has `@Inject` constructor), **`@Provides`** only for third-party/assembled types?
- Is `@ApplicationContext` used for Context (no `Activity` leaked into a `@Singleton`)? Any **over-scoping**?
- Are same-type bindings **qualified**, and are **dispatchers injected** (not hardcoded `Dispatchers.IO`)?
- Are modules `@InstallIn` the correct component and placed next to their implementation?

**Validation workflow — prove it actually works:**
1. **Compile** — Hilt validates the graph at compile time; a missing/duplicate binding fails the build (read the Dagger error carefully).
2. Run the app — the screen appears with a real repository, no manual construction anywhere (proves the graph composes).
3. **Instrumentation test with `@TestInstallIn`** replacing `DataModule` with a fake — the whole app runs against the fake repository, confirming the seams.
4. **Unit-test** a class that injects a dispatcher by passing a `StandardTestDispatcher` — proves dispatchers are injectable, not hardcoded.
5. Check for leaks with **LeakCanary** — a `@Singleton` holding an `Activity`/`View` shows up immediately.

> **AI drafts, you decide.** Hilt boilerplate is exactly the kind of repetitive code AI nails — but scope and context choices are correctness decisions it gets wrong (leaky singletons, `@Provides` bloat, hardcoded dispatchers). Run every generated module through the `@Binds`/scope/qualifier checklist before trusting it.

---

## Recap / Key takeaways

- **Hilt** wires the app: classes declare dependencies in their constructor (`@Inject`), and Hilt builds the object graph at compile time.
- **`@Binds`** maps interface→impl (impl has an `@Inject` constructor); **`@Provides`** constructs things you don't own (Retrofit, Room, OkHttp).
- **Scope = shared lifetime**: `@Singleton` for expensive/stateless/shared (DB, network, repositories); leave stateless use cases **unscoped**; never over-scope or leak an `Activity` into a singleton.
- **Qualifiers** disambiguate same-type bindings; **inject dispatchers** (`@Dispatcher(IO)`) instead of hardcoding `Dispatchers.IO`.
- In a multi-module app, modules live **next to their implementation** and Hilt aggregates them at `:app`; **`@TestInstallIn`** swaps real bindings for fakes in one line.

➡️ Next: **[Lesson 06 — Background Work](06-background-work.md)** — WorkManager sync with constraints, backoff, and Hilt-injected workers, to keep the offline cache fresh.
