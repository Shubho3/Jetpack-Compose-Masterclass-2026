# Module 04 — Modifiers Mastery

> Predict the effect of any modifier chain — and build custom interactions from pointer input up.

**Status:** ✅ **Fully written** — all 8 lessons authored per the [Authoring Guide](../../AUTHORING-GUIDE.md).
**Prerequisites:** [Module 03 — State](../module-03-state-management/README.md).
**Level:** 🟡 · **Est.:** 6–8 hrs

## What you'll be able to do
- Explain *why* modifiers are a chain and what each link does.
- Reason about **modifier order** (the single biggest beginner gotcha).
- Wire up `clickable`, interaction sources, focus, drag, and pointer input.
- Coordinate gestures with nested scroll.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [Why modifiers exist & the chain](01-why-modifiers-exist.md) | Decorate-and-wrap model; element vs modifier. |
| 02 | [Modifier order matters](02-modifier-order-matters.md) | `padding`→`background` vs `background`→`padding`; size vs requiredSize. |
| 03 | [Layout & visual modifiers](03-layout-visual-modifiers.md) | padding, size, offset, shapes, clip, background, border, insets. |
| 04 | [clickable & interaction sources](04-clickable-interaction-sources.md) | ripple, `MutableInteractionSource`, pressed/hovered state. |
| 05 | [Focus management](05-focus-management.md) | focus order, requesters, keyboard. |
| 06 | [draggable & pointerInput](06-draggable-pointerinput.md) | gesture detectors; `awaitPointerEventScope`. |
| 07 | [Nested scroll](07-nested-scroll.md) | `NestedScrollConnection`; collapsing toolbars. |
| 08 | [Custom Modifier factories](08-custom-modifier-factories.md) | composing reusable modifiers (bridge to Module 05). |

## Project
Swipe-to-dismiss card built on raw `pointerInput`, with correct modifier order.

## Interview focus
Modifier order semantics; `MutableInteractionSource`; pointer input vs gesture modifiers.

## AI assistant focus
Generating a custom gesture modifier; reviewing for order bugs and missed `consume()` calls.
