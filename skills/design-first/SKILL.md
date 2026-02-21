# Design-First

Wireframe screens using real UI components before implementing business logic. Creates a clickable prototype as the source of truth, locks the design, then implements against it. Use when starting new screens, features, or UI overhauls — before any business logic is written.

---

## Phase 1: Audit What Exists

1. **Inventory the design system** — which component library, shared components, theming/tokens, navigation patterns.
2. **Document the component palette** — available components with variants, custom components, gaps that need filling.
3. **Check existing screen patterns** — list rendering, form structure, loading/empty/error states, spacing/layout approach.

**Output:** A brief component inventory shared with the user. This becomes the palette for wireframing.

## Phase 2: Wireframe With Real Components

1. **Build screens using ONLY existing components** — real imports, not placeholder boxes. Wire up navigation. Use hardcoded/mock data only — no API calls, no business logic, no state management beyond navigation. Apply existing theme tokens.
2. **For each screen define:** layout structure, which components used, any NEW components needed (flag explicitly), navigation flow, states (loading, empty, error, populated).
3. **Get the prototype running** — tappable and navigable, every screen renders with mock data, navigation works between screens.
4. **Present for review** — walk through each screen, confirm layout/components/flow, note UX concerns. **Lock the design.**

## Phase 3: Design Lock

1. **Create a design spec** — screen descriptions, component inventory per screen, navigation map, new components needed, agreed deviations.
2. **Commit the wireframe:** `git commit -m "design(<ticket-id>): wireframe screens with mock data"`
3. **Rules from here:** wireframe is the source of truth. Implementation adds logic TO it, doesn't reshape it. If a design change is needed during implementation, flag it and discuss — don't silently change. New components need explicit approval.

## Phase 4: Implementation Against the Wireframe

1. **Replace mock data with real data, one screen at a time.** Keep layout identical. If real data doesn't fit the wireframe, STOP and discuss.
2. **Add business logic incrementally:** validation, API integration, state management, error handling, loading states.
3. **After each screen:** visual check against wireframe, run typecheck, run tests, confirm with user before next screen.
4. **If design needs to change:** explain why, get approval, update wireframe FIRST, then implementation, then design spec.

## Phase 5: Completion Checklist

- [ ] All screens match the locked wireframe (or deviations are approved and documented)
- [ ] No new components introduced without approval
- [ ] Existing component library used — no duplicate patterns
- [ ] Navigation matches wireframe map
- [ ] Loading, empty, error states implemented
- [ ] Dark mode works if supported
- [ ] Typecheck passes
- [ ] All tests pass

## Key Principles

- **Design before logic** — if you don't know what it looks like, you don't know what to build
- **Use what exists** — the component inventory is your palette, not npm
- **Lock before you build** — a committed wireframe prevents UX drift
- **The wireframe is the source of truth** — implementation conforms to it
- **Flag don't fix** — if design needs changing during implementation, discuss it
- **One screen at a time** — verify visually after each screen is wired up
