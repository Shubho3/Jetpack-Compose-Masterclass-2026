# Mind Maps — the whole course as pictures

> Every part of the course as a Mermaid diagram you can read at a glance. Start with the whole-course map, drill into a part, then study the "how the concepts connect" graph — that last one is the senior-level view.

**How to use these.** A mind map is for *retrieval*, not first learning. After you finish a module, cover the text and try to redraw its branch from memory; the gaps are what to re-read. The diagrams are Mermaid (text in version control) so they render in GitHub, IDEs, and most Markdown viewers. See the diagram conventions in the [Authoring Guide](../AUTHORING-GUIDE.md#section-2--visual-learning).

> **Rendering note.** These use Mermaid `mindmap` and `graph`/`flowchart` syntax. `mindmap` needs a recent Mermaid (v9.3+). If your viewer is older and a `mindmap` block doesn't render, the same content is mirrored as a `graph` immediately after the whole-course map, and the per-part maps degrade gracefully to indented text.

---

## 1. The whole course — one mind map

The five parts, their modules, and the one thing each module makes you able to do.

```mermaid
mindmap
  root((Jetpack Compose<br/>Masterclass 2026))
    Part I Foundations
      M01 Introduction
        declarative mindset
        recomposition basics
      M02 Layouts
        Row Column Box
        lazy lists and grids
        Window Size Classes
      M03 State ★ exemplar
        remember and saveable
        state hoisting
        UDF MVI MVVM
      M04 Modifiers
        the modifier chain
        order matters
        pointer input
    Part II Rendering Engine
      M05 Custom Layouts
        measure place
        SubcomposeLayout
      M06 Side Effects
        LaunchedEffect keys
        derivedStateOf
        snapshotFlow
      M07 CompositionLocal
        static vs dynamic
        implicit deps cost
      M08 Canvas
        draw phase
        custom charts
    Part III Polish and Performance
      M09 Material 3
        color roles
        dynamic color
      M10 Animations
        animate as state
        shared elements
      M11 Performance
        profiling
        stability
        baseline profiles
      M12 Internals
        compiler
        slot table
        snapshots
    Part IV Production Engineering
      M13 Architecture
        clean layers
        repository SSOT
      M14 Testing
        test pyramid
        semantics tree
      M15 Modern Android
        K2 Kotlin 2.x
        multiplatform
      M16 AI Dev
        agentic loop
        human gates
    Part V Craft and Capstone
      M17 Code Quality
        SOLID for Compose
        static analysis
      M18 Security
        secure storage
        OWASP top 10
      M19 Capstone
        offline first
        CI CD
      M20 Career
        system design
        interview prep
```

**Same map, as a graph** (fallback for older Mermaid, and easier to follow the part → module → skill nesting):

```mermaid
graph TD
    C(("Compose<br/>Masterclass 2026"))
    C --> P1["Part I<br/>Foundations"]
    C --> P2["Part II<br/>Rendering Engine"]
    C --> P3["Part III<br/>Polish & Performance"]
    C --> P4["Part IV<br/>Production Engineering"]
    C --> P5["Part V<br/>Craft & Capstone"]

    P1 --> M01["01 Intro<br/>declarative mindset"]
    P1 --> M02["02 Layouts<br/>adaptive UI"]
    P1 --> M03["03 State ★<br/>UDF + hoisting"]
    P1 --> M04["04 Modifiers<br/>order + gestures"]

    P2 --> M05["05 Custom Layouts<br/>measure/place"]
    P2 --> M06["06 Side Effects<br/>safe effects"]
    P2 --> M07["07 CompositionLocal<br/>implicit deps"]
    P2 --> M08["08 Canvas<br/>draw phase"]

    P3 --> M09["09 Material 3<br/>theming"]
    P3 --> M10["10 Animations<br/>motion APIs"]
    P3 --> M11["11 Performance<br/>measured wins"]
    P3 --> M12["12 Internals<br/>why it skips"]

    P4 --> M13["13 Architecture<br/>clean + MVI"]
    P4 --> M14["14 Testing<br/>pyramid"]
    P4 --> M15["15 Modern Android<br/>K2 + CMP"]
    P4 --> M16["16 AI Dev<br/>agentic loop"]

    P5 --> M17["17 Code Quality<br/>SOLID + gates"]
    P5 --> M18["18 Security<br/>OWASP"]
    P5 --> M19["19 Capstone<br/>ship it"]
    P5 --> M20["20 Career<br/>interviews"]
```

> **The critical spine** runs through this map: **01 → 03 → 04 → 06 → 11 → 12**. If you only have the diagrams for those six, you have the load-bearing 80%.

---

## 2. Part I — Foundations

> *Goal of the part:* ship a correct, adaptive screen whose UI is a pure function of state.

```mermaid
mindmap
  root((Part I<br/>Foundations))
    M01 Introduction
      imperative vs declarative
        XML and findViewById pain
        UI equals f of state
      how Compose works
        composition
        recomposition
      misconceptions
        do not mutate views
    M02 Layouts
      core containers
        Row Column Box
        arrangement and alignment
      lists
        LazyColumn LazyRow
        keys and contentType
      grids
        LazyVerticalGrid
        staggered grid
      app structure
        Scaffold top bar FAB
        insets
      adaptive
        Window Size Classes
        list detail pane
        foldables tablets desktop
    M03 State
      holding state
        remember
        mutableStateOf
        by delegate
      surviving config
        rememberSaveable
        custom Saver
      hoisting
        stateless composables
        value and onValueChange
      organizing
        UDF
        MVI vs MVVM
        single source of truth
        immutable state
    M04 Modifiers
      the chain
        decorate and wrap
        element vs modifier
      order matters
        padding vs background
        size vs requiredSize
      interaction
        clickable
        MutableInteractionSource
        focus
      gestures
        draggable
        pointerInput
        nested scroll
```

**Reading order inside Part I:** 01 → 02 and 01 → 03 in parallel, then 03 → 04. Don't rush 03 — it's the heart.

```mermaid
graph LR
    M01 --> M02
    M01 --> M03
    M03 --> M04
    M02 -.->|feeds| M05[to Part II]
    M04 -.->|feeds| M05
```

---

## 3. Part II — The Rendering Engine

> *Goal of the part:* drop below the built-ins — place children yourself, run effects safely, draw custom pixels.

```mermaid
mindmap
  root((Part II<br/>Rendering Engine))
    M05 Custom Layouts
      the layout phase
        constraints down
        sizes up
        placement last
      measuring
        intrinsic measurements
        BoxWithConstraints
        onSizeChanged
      custom layout
        measure then layout then place
        single measure rule
      SubcomposeLayout
        size depends on sibling
      Modifier Node
        custom factories
    M06 Side Effects
      why they exist
        composition is frequent
        order free
      effect APIs
        LaunchedEffect and keys
        rememberCoroutineScope
        DisposableEffect cleanup
        SideEffect
      bridging
        produceState
        snapshotFlow
        rememberUpdatedState
      computing
        derivedStateOf
    M07 CompositionLocal
      built in locals
        LocalContext
        LocalDensity
        LocalContentColor
      static vs dynamic
        recomposition scope
      custom locals
        CompositionLocalProvider
        default values
      decision
        local vs DI vs params
        implicit dependency cost
    M08 Canvas
      draw phase
        DrawScope
        drawBehind drawWithCache
      primitives
        shapes paths
        TextMeasurer
      transforms
        graphicsLayer
        cheap animations
      charts
        data to pixels
        axes gridlines
      vectors
        ImageVector
        animated vectors
```

**Dependency reality:** 05 needs 02 + 04; 06 needs 03; 07 needs 03 + 06; 08 needs 05.

```mermaid
graph LR
    S03[03 State] --> M06[06 Side Effects]
    M06 --> M07[07 CompositionLocal]
    L02[02 Layouts] --> M05[05 Custom Layouts]
    MOD04[04 Modifiers] --> M05
    M05 --> M08[08 Canvas]
```

---

## 4. Part III — Polish & Performance

> *Goal of the part:* make it beautiful, make it smooth, and understand *why* it's smooth.

```mermaid
mindmap
  root((Part III<br/>Polish and Performance))
    M09 Material 3
      theming model
        MaterialTheme
        color type shape
      color roles
        primary surface container
        contrast
      dynamic color
        Material You
        pre S fallback
      type and shape
        type scale
        shape scale
      themes
        light dark custom
        expressive notes
    M10 Animations
      value animation
        animate as state
      visibility and content
        AnimatedVisibility
        AnimatedContent
      precise motion
        Animatable
        gestures interruptible
      coordinated
        updateTransition
        infinite transitions
      advanced
        shared element transitions
        LookaheadScope
    M11 Performance
      cost model
        three phases
      profiling
        recomposition counts
        composition tracing
      fixing
        stability and skipping
        lazy list optimization
        deferring state reads
        image loading
        overdraw main thread
        movableContentOf
      shipping
        baseline profiles
        Macrobenchmark
    M12 Internals
      compiler
        composer
        group calls
      runtime
        slot table
        positional memoization
      snapshots
        MVCC for state
        read write apply
      stability
        Stable Immutable
        inference rules
      skipping
        comparison
        Strong Skipping
      frame lifecycle
        recompose measure place draw
```

**Why this order:** theming and animation are the polish; performance is where it gets real; internals is the *theory* that makes performance intuition click — so 11 → 12 (apply, then understand deeply).

```mermaid
graph LR
    M09[09 Material 3] --> M10[10 Animations]
    M11[11 Performance] --> M12[12 Internals]
    M12 -.->|theory feeds back into| M11
```

---

## 5. Part IV — Production Engineering

> *Goal of the part:* structure, test, modernize, and accelerate a real multi-feature app.

```mermaid
mindmap
  root((Part IV<br/>Production Engineering))
    M13 Architecture
      clean layers
        dependency rule
        module boundaries
      patterns
        MVVM in Compose
        MVI unidirectional
      data
        repository SSOT
        use cases
      scale
        feature modularization
        offline first
    M14 Testing
      the pyramid
        cost vs confidence
      unit
        ViewModels
        Turbine MockK
        coroutine test
      ui
        createComposeRule
        semantics tree
        finders and actions
      higher
        integration with fakes
        screenshot tests
        Macrobenchmark
    M15 Modern Android
      kotlin 2.x
        K2 compiler
        bundled compose plugin
      multiplatform
        shared vs platform
      surfaces
        foldables tablets
        Wear OS
        desktop
        Android XR
      ai native
        on device and cloud
    M16 AI Dev
      agentic basics
        tools loops autonomy
      coding agents
        Cursor Claude Code
        Gemini CLI Codex Windsurf
      the loop
        planner architect coder
        reviewer human
      scaling it
        multi agent
        automated refactor
        generated tests
```

**Dependency reality:** 13 anchors this part (needs 03 + 06); 14 and 19 build on 13; 15 → 16.

```mermaid
graph TD
    M03[03 State] --> M13[13 Architecture]
    M06[06 Effects] --> M13
    M13 --> M14[14 Testing]
    M13 --> M19[19 Capstone]
    M15[15 Modern Android] --> M16[16 AI Dev]
```

---

## 6. Part V — Craft & Capstone

> *Goal of the part:* keep it healthy, keep it secure, ship it, and get hired.

```mermaid
mindmap
  root((Part V<br/>Craft and Capstone))
    M17 Code Quality
      clean code
        naming
        function size
        composable responsibility
      principles
        SOLID for Android
        KISS DRY YAGNI
      smells
        god composables
        state in wrong place
        modifier soup
      automation
        Detekt Ktlint Lint
        SonarQube CI gates
        AI review
    M18 Security
      security model
        sandboxing
        permissions threat model
      storage
        Keystore
        encrypted DataStore
      crypto
        symmetric asymmetric
        key management
      api
        TLS
        certificate pinning
        token handling
      auth
        OAuth sessions
        biometric gating
      OWASP mobile top 10
    M19 Capstone
      setup
        app core feature modules
      data
        Room Retrofit
        repository SSOT
      domain and ui
        use cases
        MVI Navigation
        loading error empty
      di and work
        Hilt across modules
        WorkManager sync
      ship
        testing pyramid
        CI CD
        baseline profile
        monitoring
    M20 Career
      roadmap
        interview stages
      questions
        compose bank
        kotlin coroutines
      senior
        system design framework
        architecture discussions
      ai era
        changing role
      offer
        behavioral
        leveling negotiation
```

**Dependency reality:** 17 and 18 both build on 13; 19 is the integration of nearly everything; 20 caps it.

```mermaid
graph TD
    M13[13 Architecture] --> M17[17 Code Quality]
    M13 --> M18[18 Security]
    M17 --> M19[19 Capstone]
    M18 --> M19
    M14[14 Testing] --> M19
    M11[11 Performance] --> M19
    M19 --> M20[20 Career]
```

---

## 7. How the concepts connect — the senior map

This is the one to internalize. Modules are *chapters*; the real curriculum is a web of **concepts** that reinforce each other. Compose has one job — **turn state into UI** — and every concept below is in service of doing that *correctly, fast, and at scale*.

```mermaid
graph TD
    subgraph core["The one idea"]
        UI["UI = f(state)"]
    end

    subgraph state["State & data flow"]
        ST[State / MutableState]
        HO[State hoisting]
        UDF[UDF · MVI · MVVM]
        SSOT[Single source of truth]
        IMM[Immutability / stability]
    end

    subgraph render["The rendering pipeline"]
        REC[Recomposition]
        COMP[Composition phase]
        LAY[Layout phase]
        DRAW[Draw phase]
        SLOT[Slot table]
        SNAP[Snapshot system]
        SKIP[Skipping]
    end

    subgraph react["Reacting & decorating"]
        EFF[Side effects]
        MOD[Modifiers]
        ANIM[Animations]
        CL[CompositionLocal]
    end

    subgraph scale["Engineering at scale"]
        ARCH[Architecture / boundaries]
        PERF[Performance]
        TEST[Testing]
        SEC[Security]
        QUAL[Code quality]
        AIW[AI workflows]
    end

    UI --> ST
    UI --> REC

    ST --> HO --> UDF --> SSOT
    ST --> IMM
    UDF --> ARCH

    REC --> COMP --> LAY --> DRAW
    SNAP --> REC
    SLOT --> REC
    IMM --> SKIP
    SKIP --> REC
    SKIP --> PERF

    ST -->|read = subscription| REC
    EFF -->|quarantined from| COMP
    MOD --> LAY
    MOD --> DRAW
    ANIM --> DRAW
    CL -->|implicit deps| COMP

    IMM --> PERF
    REC --> PERF
    PERF --> SLOT
    PERF --> SNAP

    ARCH --> TEST
    ARCH --> SEC
    ARCH --> QUAL
    SSOT --> ARCH
    AIW -.->|accelerates, never replaces| ARCH
    AIW -.-> TEST
    AIW -.-> QUAL

    classDef idea fill:#1f2937,stroke:#60a5fa,color:#fff,stroke-width:2px;
    class UI idea;
```

### Reading the senior map — the load-bearing edges

These are the connections that, once they click, make the whole course feel like one idea:

- **`UI = f(state)` is the root.** Everything hangs off it. Modifiers decorate the `UI`; effects react to changes in it; architecture decides where the `state` lives.
- **A state *read* is a subscription.** Reading state in composition tells the runtime "re-run me when this changes" — that single fact links **State (M03)** to **Recomposition** to **Performance (M11)**. Reading the *same* state later (in layout or draw) is how you *defer* and save recompositions.
- **Immutability is a performance feature, not just hygiene.** Stable/immutable types let the runtime **skip** (M12), which is *the* lever in **Performance (M11)**. That's why `ImmutableList` shows up in M03's state and M11's fixes and M12's theory — it's one thread.
- **Effects are quarantined from composition.** **Side Effects (M06)** exist precisely because composition runs often and out of order — the same property of **Recomposition** that makes Compose fast makes naive side effects dangerous.
- **Single source of truth scales into architecture.** The discipline you learn in **State (M03)** — one owner per piece of state — is the same principle that, applied to *data*, becomes the **repository (M13)**, and applied to a *screen* becomes **MVI**.
- **Architecture is the substrate for the production concerns.** **Testing (M14)**, **Security (M18)**, and **Code Quality (M17)** all get easier with clean boundaries — and harder without them. That's why M13 sits upstream of all three.
- **AI accelerates every box but owns none of them.** The dashed edges are deliberate: **AI workflows (M16)** speed up architecture, testing, and quality work, but the decisions stay human. *AI drafts, you decide* — see [AI-assisted learning workflows](ai-assisted-learning-workflows.md).

### The three phases, end to end

If you remember one pipeline, remember this — it connects M01, M05, M06, M08, M11, and M12:

```text
state change
   │
   ▼
COMPOSITION ──▶ LAYOUT ──▶ DRAW ──▶ pixels
 (what to     (measure &   (paint
  show)        place)       it)
   │             │            │
 read here   read here    read here  ← read state as LATE as you can:
 (most         (cheaper)   (cheapest)   deferring a read down this pipe
  expensive)                            is the #1 performance trick
```

```mermaid
graph LR
    SC[State change] --> CO[Composition<br/>what to show]
    CO --> LA[Layout<br/>measure & place]
    LA --> DR[Draw<br/>paint pixels]
    DR --> PX[Pixels on screen]
    DR -. user/system event .-> SC
```

> **The takeaway:** state flows in, pixels come out, and the entire craft of Compose is keeping that path **correct** (state in one place), **minimal** (skip what didn't change), and **safe** (effects out of the hot path). Every module is a slice of that one sentence.

---

## Where to go next

- Build the maps into muscle memory with the **[practice projects](practice-projects.md)** and per-module **[assignments](assignments.md)**.
- Use AI to *quiz* yourself on these maps — prompts in **[AI-assisted learning workflows](ai-assisted-learning-workflows.md)**.
- See how these concepts become team rules in **[enterprise best practices](enterprise-best-practices.md)**.
- Module-level diagrams live in each module's README — start with the exemplar, **[Module 03](../modules/module-03-state-management/README.md)**.
